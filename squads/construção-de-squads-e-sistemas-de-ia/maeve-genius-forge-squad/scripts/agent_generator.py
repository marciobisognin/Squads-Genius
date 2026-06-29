"""Agent file generation for produced squads."""
from __future__ import annotations

from typing import Any, Dict, List

import yaml


def generate_agent_files(agents: List[Dict[str, Any]]) -> Dict[str, str]:
    return {f"agents/{agent['id']}.yaml": yaml.safe_dump(agent, allow_unicode=True, sort_keys=False) for agent in agents}
