#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='VetorViveiro CLI — gera pacote operacional demonstrativo')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    data=json.loads(Path(args.input).read_text(encoding='utf-8'))
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    (out/'diagnostico.md').write_text('# Diagnóstico VetorViveiro\n\nProjeto: '+data.get('projeto','')+'\n\n## Achado central\nTransformar documentação institucional em sistema operacional auditável.\n',encoding='utf-8')
    (out/'plano_operacional.md').write_text('# Plano operacional\n\n1. Governança\n2. Seleção\n3. Pré-incubação\n4. Incubação\n5. Graduação\n6. Indicadores\n7. Portal público\n',encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps({'ok':True,'files':['diagnostico.md','plano_operacional.md']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'ok':True,'output':str(out)},ensure_ascii=False))
if __name__=='__main__': main()
