"""Generate workflow YAML files."""
from __future__ import annotations

from typing import Any, Dict, List

import yaml


def generate_workflow_files(workflows: List[Dict[str, Any]]) -> Dict[str, str]:
    return {f"workflows/{workflow['id']}.yaml": yaml.safe_dump(workflow, allow_unicode=True, sort_keys=False) for workflow in workflows}
