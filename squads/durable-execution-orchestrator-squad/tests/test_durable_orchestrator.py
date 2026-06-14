from pathlib import Path
import importlib.util, sys
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "durable_orchestrator.py"
spec = importlib.util.spec_from_file_location("durable_orchestrator", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
sys.modules["durable_orchestrator"] = module
spec.loader.exec_module(module)

def test_run_example_completes_after_human_signal(tmp_path):
    result = module.run_example(tmp_path / "demo")
    assert result["final_status"] == "completed"
    assert result["metrics"]["tokens_in"] > 0
    assert (tmp_path / "demo" / "result.json").is_file()

def test_resume_does_not_duplicate_completed_steps(tmp_path):
    db = tmp_path / "orchestrator.db"; conn = module.connect(db); module.init_db(conn)
    module.register_workflow(conn, ROOT / "examples" / "lead_research_workflow.yaml")
    instance_id = module.start_instance(conn, "lead-research-hitl", {"topic":"leads"})
    first = module.run_instance(conn, instance_id); assert first["instance"]["status"] == "paused"
    completed_before = [t for t in first["tasks"] if t["status"] == "completed"]
    second = module.run_instance(conn, instance_id); completed_after = [t for t in second["tasks"] if t["status"] == "completed"]
    assert len(completed_after) == len(completed_before)
    assert all(t["attempts"] == 1 for t in completed_after)
    module.send_signal(conn, instance_id, "approval", {"approved": True})
    assert module.run_instance(conn, instance_id)["instance"]["status"] == "completed"

def test_cancel_triggers_compensations(tmp_path):
    db = tmp_path / "orchestrator.db"; conn = module.connect(db); module.init_db(conn)
    module.register_workflow(conn, ROOT / "examples" / "lead_research_workflow.yaml")
    instance_id = module.start_instance(conn, "lead-research-hitl", {"topic":"leads"})
    module.run_instance(conn, instance_id)
    assert module.cancel_instance(conn, instance_id)["instance"]["status"] == "cancelled"
    assert conn.execute("select * from compensations where instance_id=?", (instance_id,)).fetchall()

def test_status_exposes_metrics(tmp_path):
    result = module.run_example(tmp_path / "metrics")
    conn = module.connect(Path(result["db"]))
    status = module.status(conn, result["instance_id"])
    assert status["metrics"]["estimated_cost"] > 0
    assert any(event["event_type"] == "signal_received" for event in status["events"])
