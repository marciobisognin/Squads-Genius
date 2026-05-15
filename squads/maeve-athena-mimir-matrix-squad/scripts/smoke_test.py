#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'output/demo'
res=subprocess.run([sys.executable, str(root/'scripts/value_canvas_visual_forge.py'), '--case', str(root/'examples/caso-demo.json'), '--output', str(out)], text=True, capture_output=True)
if res.returncode: print(res.stderr); sys.exit(res.returncode)
required=['customer-profile.md','value-map.md','fit-matrix.md','hypothesis-backlog.md','experiment-sprint.md','visual-canvas-brief.md','carousel-outline.md','pitch-storyboard.md','executive-decision-report.md']
missing=[f for f in required if not (out/f).exists() or (out/f).stat().st_size<80]
if missing:
    print({'ok':False,'missing':missing}); sys.exit(2)
print('SMOKE_TEST_OK')
