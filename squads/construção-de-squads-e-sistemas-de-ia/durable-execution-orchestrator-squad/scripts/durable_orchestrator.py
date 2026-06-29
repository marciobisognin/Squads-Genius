#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sqlite3, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
try:
    import yaml
except Exception:
    yaml = None
TERMINAL_TASK_STATUSES = {"completed", "compensated", "skipped"}
def now() -> str: return datetime.now(timezone.utc).isoformat()
def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True); conn = sqlite3.connect(db); conn.row_factory = sqlite3.Row; return conn
def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    create table if not exists workflows (id text not null, version text not null, definition_json text not null, created_at text not null, primary key (id, version));
    create table if not exists instances (id text primary key, workflow_id text not null, workflow_version text not null, status text not null, input_json text not null, current_step text, created_at text not null, updated_at text not null);
    create table if not exists task_instances (id text primary key, instance_id text not null, step_id text not null, status text not null, attempts integer not null default 0, result_json text, error text, started_at text, completed_at text, unique(instance_id, step_id));
    create table if not exists signals (id text primary key, instance_id text not null, type text not null, payload_json text not null, created_at text not null);
    create table if not exists compensations (id text primary key, instance_id text not null, step_id text not null, action text not null, status text not null, created_at text not null);
    create table if not exists event_log (id text primary key, instance_id text, task_id text, event_type text not null, metadata_json text not null, created_at text not null);
    """); conn.commit()
def event(conn: sqlite3.Connection, event_type: str, instance_id: str|None=None, task_id: str|None=None, **metadata: Any) -> None:
    conn.execute("insert into event_log values (?, ?, ?, ?, ?, ?)", (str(uuid.uuid4()), instance_id, task_id, event_type, json.dumps(metadata, ensure_ascii=False), now()))
def load_workflow_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) if path.suffix.lower() in {".yaml", ".yml"} and yaml else json.loads(text)
    if not isinstance(data, dict) or not data.get("id") or not data.get("steps"): raise ValueError("workflow deve conter id e steps")
    data.setdefault("version", "1.0.0"); return data
def register_workflow(conn: sqlite3.Connection, workflow_path: Path) -> dict[str, Any]:
    workflow = load_workflow_file(workflow_path)
    conn.execute("insert or replace into workflows values (?, ?, ?, ?)", (workflow["id"], workflow["version"], json.dumps(workflow, ensure_ascii=False), now()))
    event(conn, "workflow_registered", workflow_id=workflow["id"], version=workflow["version"]); conn.commit(); return workflow
def get_workflow(conn: sqlite3.Connection, workflow_id: str, version: str|None=None) -> dict[str, Any]:
    row = conn.execute("select * from workflows where id=? and version=?", (workflow_id, version)).fetchone() if version else conn.execute("select * from workflows where id=? order by created_at desc limit 1", (workflow_id,)).fetchone()
    if not row: raise KeyError(f"workflow não registrado: {workflow_id}")
    return json.loads(row["definition_json"])
def start_instance(conn: sqlite3.Connection, workflow_id: str, input_data: dict[str, Any], version: str|None=None) -> str:
    workflow = get_workflow(conn, workflow_id, version); instance_id = str(uuid.uuid4())
    conn.execute("insert into instances values (?, ?, ?, ?, ?, ?, ?, ?)", (instance_id, workflow["id"], workflow["version"], "running", json.dumps(input_data, ensure_ascii=False), None, now(), now()))
    for step in workflow["steps"]: conn.execute("insert into task_instances(id, instance_id, step_id, status, attempts) values (?, ?, ?, ?, ?)", (str(uuid.uuid4()), instance_id, step["id"], "pending", 0))
    event(conn, "instance_started", instance_id=instance_id, workflow_id=workflow_id, version=workflow["version"]); conn.commit(); return instance_id
def signal_exists(conn: sqlite3.Connection, instance_id: str, signal_type: str) -> bool:
    return bool(conn.execute("select 1 from signals where instance_id=? and type=? limit 1", (instance_id, signal_type)).fetchone())
def dependencies_completed(conn: sqlite3.Connection, instance_id: str, step: dict[str, Any]) -> bool:
    for dep in step.get("depends_on", []):
        row = conn.execute("select status from task_instances where instance_id=? and step_id=?", (instance_id, dep)).fetchone()
        if not row or row["status"] not in TERMINAL_TASK_STATUSES: return False
    return True
def execute_activity(step: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    action = step.get("action", "noop"); time.sleep(0.001)
    return {"action": action, "step_id": step["id"], "summary": f"atividade {action} executada com checkpoint durável", "tokens_in": int(step.get("tokens_in", 120)), "tokens_out": int(step.get("tokens_out", 80)), "estimated_cost": float(step.get("estimated_cost", 0.001)), "idempotency_key": f"{context['instance_id']}:{step['id']}"}
def run_instance(conn: sqlite3.Connection, instance_id: str) -> dict[str, Any]:
    inst = conn.execute("select * from instances where id=?", (instance_id,)).fetchone()
    if not inst: raise KeyError(f"instância não encontrada: {instance_id}")
    if inst["status"] in {"completed", "cancelled", "failed"}: return status(conn, instance_id)
    workflow = get_workflow(conn, inst["workflow_id"], inst["workflow_version"]); conn.execute("update instances set status=?, updated_at=? where id=?", ("running", now(), instance_id))
    for step in workflow["steps"]:
        task = conn.execute("select * from task_instances where instance_id=? and step_id=?", (instance_id, step["id"])).fetchone()
        if task and task["status"] in TERMINAL_TASK_STATUSES: continue
        if not dependencies_completed(conn, instance_id, step): continue
        required_signal = step.get("requires_signal")
        if required_signal and not signal_exists(conn, instance_id, required_signal):
            conn.execute("update task_instances set status=? where instance_id=? and step_id=?", ("waiting_signal", instance_id, step["id"])); conn.execute("update instances set status=?, current_step=?, updated_at=? where id=?", ("paused", step["id"], now(), instance_id)); event(conn, "instance_paused_for_signal", instance_id=instance_id, task_id=step["id"], signal_type=required_signal); conn.commit(); return status(conn, instance_id)
        conn.execute("update task_instances set status=?, attempts=attempts+1, started_at=? where instance_id=? and step_id=?", ("running", now(), instance_id, step["id"])); event(conn, "task_started", instance_id=instance_id, task_id=step["id"], action=step.get("action"))
        result = execute_activity(step, {"instance_id": instance_id, "input": json.loads(inst["input_json"])}); conn.execute("update task_instances set status=?, result_json=?, completed_at=? where instance_id=? and step_id=?", ("completed", json.dumps(result, ensure_ascii=False), now(), instance_id, step["id"])); event(conn, "task_completed", instance_id=instance_id, task_id=step["id"], result=result); conn.execute("update instances set current_step=?, updated_at=? where id=?", (step["id"], now(), instance_id)); conn.commit()
    remaining = conn.execute("select count(*) as c from task_instances where instance_id=? and status not in ('completed','compensated','skipped')", (instance_id,)).fetchone()["c"]
    if remaining == 0: conn.execute("update instances set status=?, updated_at=? where id=?", ("completed", now(), instance_id)); event(conn, "instance_completed", instance_id=instance_id); conn.commit()
    return status(conn, instance_id)
def send_signal(conn: sqlite3.Connection, instance_id: str, signal_type: str, payload: dict[str, Any]) -> None:
    conn.execute("insert into signals values (?, ?, ?, ?, ?)", (str(uuid.uuid4()), instance_id, signal_type, json.dumps(payload, ensure_ascii=False), now())); conn.execute("update instances set status=?, updated_at=? where id=? and status=?", ("running", now(), instance_id, "paused")); event(conn, "signal_received", instance_id=instance_id, signal_type=signal_type, payload=payload); conn.commit()
def compensate(conn: sqlite3.Connection, instance_id: str) -> None:
    inst = conn.execute("select * from instances where id=?", (instance_id,)).fetchone(); workflow = get_workflow(conn, inst["workflow_id"], inst["workflow_version"]); completed = {row["step_id"] for row in conn.execute("select step_id from task_instances where instance_id=? and status='completed'", (instance_id,)).fetchall()}
    for step in reversed(workflow["steps"]):
        action = step.get("compensation")
        if action and step["id"] in completed: conn.execute("insert into compensations values (?, ?, ?, ?, ?, ?)", (str(uuid.uuid4()), instance_id, step["id"], action, "completed", now())); event(conn, "task_compensated", instance_id=instance_id, task_id=step["id"], action=action)
    conn.commit()
def cancel_instance(conn: sqlite3.Connection, instance_id: str) -> dict[str, Any]:
    compensate(conn, instance_id); conn.execute("update instances set status=?, updated_at=? where id=?", ("cancelled", now(), instance_id)); event(conn, "instance_cancelled", instance_id=instance_id); conn.commit(); return status(conn, instance_id)
def status(conn: sqlite3.Connection, instance_id: str) -> dict[str, Any]:
    inst = conn.execute("select * from instances where id=?", (instance_id,)).fetchone()
    if not inst: raise KeyError(f"instância não encontrada: {instance_id}")
    tasks = [dict(row) for row in conn.execute("select step_id, status, attempts, result_json, error from task_instances where instance_id=? order by rowid", (instance_id,)).fetchall()]
    events = [dict(row) for row in conn.execute("select event_type, task_id, metadata_json, created_at from event_log where instance_id=? order by created_at", (instance_id,)).fetchall()]
    metrics = {"tokens_in":0,"tokens_out":0,"estimated_cost":0.0,"retries":0}
    for task in tasks:
        metrics["retries"] += max(0, int(task["attempts"] or 0) - 1)
        if task.get("result_json"):
            result = json.loads(task["result_json"]); metrics["tokens_in"] += int(result.get("tokens_in", 0)); metrics["tokens_out"] += int(result.get("tokens_out", 0)); metrics["estimated_cost"] += float(result.get("estimated_cost", 0.0))
    return {"instance": dict(inst), "tasks": tasks, "events": events, "metrics": metrics}
def run_example(workdir: Path) -> dict[str, Any]:
    workdir.mkdir(parents=True, exist_ok=True); db = workdir / "orchestrator.db"
    if db.exists(): db.unlink()
    conn = connect(db); init_db(conn); base = Path(__file__).resolve().parents[1]; register_workflow(conn, base / "examples" / "lead_research_workflow.yaml"); input_data = json.loads((base / "examples" / "sample_input.json").read_text(encoding="utf-8")); instance_id = start_instance(conn, "lead-research-hitl", input_data); first = run_instance(conn, instance_id)
    if first["instance"]["status"] != "paused": raise RuntimeError("exemplo deveria pausar para aprovação humana")
    send_signal(conn, instance_id, "approval", {"approved": True, "approver":"human-reviewer"}); final = run_instance(conn, instance_id); out = {"db": str(db), "instance_id": instance_id, "final_status": final["instance"]["status"], "metrics": final["metrics"]}; (workdir / "result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); return out
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Protótipo local do Orquestrador de Execução Durável para Squads"); sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ["init-db","register","start","run","signal","cancel","status","run-example"]: sub.add_parser(name)
    parser = argparse.ArgumentParser(description="Protótipo local do Orquestrador de Execução Durável para Squads"); sub = parser.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("init-db"); p.add_argument("--db", required=True)
    p=sub.add_parser("register"); p.add_argument("--db", required=True); p.add_argument("--workflow", required=True)
    p=sub.add_parser("start"); p.add_argument("--db", required=True); p.add_argument("--workflow-id", required=True); p.add_argument("--input", required=True)
    p=sub.add_parser("run"); p.add_argument("--db", required=True); p.add_argument("--instance", required=True)
    p=sub.add_parser("signal"); p.add_argument("--db", required=True); p.add_argument("--instance", required=True); p.add_argument("--type", required=True); p.add_argument("--payload", default="{}")
    p=sub.add_parser("cancel"); p.add_argument("--db", required=True); p.add_argument("--instance", required=True)
    p=sub.add_parser("status"); p.add_argument("--db", required=True); p.add_argument("--instance", required=True)
    p=sub.add_parser("run-example"); p.add_argument("--workdir", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "run-example": print(json.dumps(run_example(Path(args.workdir)), ensure_ascii=False, indent=2)); return 0
    conn = connect(Path(args.db)); init_db(conn)
    if args.cmd == "init-db": print(json.dumps({"db": args.db, "status":"initialized"}, ensure_ascii=False)); return 0
    if args.cmd == "register": print(json.dumps(register_workflow(conn, Path(args.workflow)), ensure_ascii=False, indent=2)); return 0
    if args.cmd == "start": print(json.dumps({"instance_id": start_instance(conn, args.workflow_id, json.loads(Path(args.input).read_text(encoding="utf-8")))}, ensure_ascii=False)); return 0
    if args.cmd == "run": print(json.dumps(run_instance(conn, args.instance), ensure_ascii=False, indent=2)); return 0
    if args.cmd == "signal": send_signal(conn, args.instance, args.type, json.loads(args.payload)); print(json.dumps({"status":"signal_received"}, ensure_ascii=False)); return 0
    if args.cmd == "cancel": print(json.dumps(cancel_instance(conn, args.instance), ensure_ascii=False, indent=2)); return 0
    if args.cmd == "status": print(json.dumps(status(conn, args.instance), ensure_ascii=False, indent=2)); return 0
    return 2
if __name__ == "__main__": raise SystemExit(main())
