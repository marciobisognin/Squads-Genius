# Validation Report — PrismaFrame Executive Cinema Suite

## Smoke test

Command:

```bash
python3 scripts/smoke_test.py
```

Result: PASS.

Generated final demo files:

- `generated/demo/final/index.html`
- `generated/demo/final/deck.html`
- `generated/demo/final/motion-composition.html`
- `generated/demo/final/print-ready.html`
- `generated/demo/final/presentation.pdf`
- `generated/demo/final/final-manifest.json`
- `generated/demo/final/qa-cleanroom-report.json`

## Cleanroom QA

Result: PASS.

The generated public-facing files were scanned for process/bastidor markers configured in `scripts/build_product.py`; no forbidden marker was found in the generated final HTML outputs.

## Structure validation

Command:

```bash
python3 scripts/validate_squad.py
```

Result: PASS.

Verified:

- `squad.yaml`
- 16 agents
- 9 tasks
- 3 workflows
- required scripts
- templates
- contracts
- IP/license files
- universal `*help` and `*exit` commands in agents
- basic secret scan

## PDF validation

Command:

```bash
qpdf --check generated/demo/final/presentation.pdf
mutool draw -o validation/pdf-preview/page-%02d.png generated/demo/final/presentation.pdf 1-3
```

Result: PASS.

- PDF header: `%PDF-`
- EOF marker: present
- `qpdf --check`: no syntax or stream encoding errors
- Rendered preview pages: 2
- Preview images:
  - `validation/pdf-preview/page-01.png`
  - `validation/pdf-preview/page-02.png`

## HyperFrames-inspired composition validation

The generated `motion-composition.html` contains:

- root timed composition with `data-composition-id`;
- `data-width="1920"` and `data-height="1080"`;
- timed `.clip` scenes;
- deterministic CSS animation timing;
- no external CDN requirement.

Full MP4 rendering is intentionally optional because it depends on HyperFrames CLI availability in the execution environment. The squad provides a clean HTML-native composition ready for preview/render handoff.
