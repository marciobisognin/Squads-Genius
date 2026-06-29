"""Generate task YAML files."""
from __future__ import annotations

from typing import Any, Dict, List

import yaml


def generate_task_files(tasks: List[Dict[str, Any]]) -> Dict[str, str]:
    return {f"tasks/{task['id']}.yaml": yaml.safe_dump(task, allow_unicode=True, sort_keys=False) for task in tasks}
