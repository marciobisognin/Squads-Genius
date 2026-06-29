#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
cmd=[sys.executable, str(root/'scripts/formulate_case.py'), '--input', str(root/'examples/caso_funcionario.txt'), '--output', str(root/'output/demo')]
raise SystemExit(subprocess.call(cmd))
