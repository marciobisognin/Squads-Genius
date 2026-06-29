# BUMBLEBEE

> **Personagem:** Mensageiro e courier, leva e entrega
> **Ato do Anel:** `praxis` (πρᾶξις — ação) · **Estrato:** `KYKLOS` · **Tipo:** python

## 🎯 Missão
Empacota o squad validado em um ZIP com manifesto neutro (AGENTS.md + contratos SACP + LOOP.md), instalável em qualquer runtime de agente compatível.

## 📥 Entrada (SACP)
Squad validado (run aprovada).

## 📤 Saída (SACP)
Pacote final (ZIP) + manifesto neutro + relatório de entrega.

## ⚖️ Regras invariantes
- RF-14: manifesto neutro, sem acoplamento a runtime específico.
- Nunca publica/empurra sem aprovação humana registrada.
- Checksums (sha256) por arquivo no manifesto.

## ▶️ Comandos / acionamento
- `build_pack.py --root runs/<id> --output runs/<id>/pack.zip`.

---

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
