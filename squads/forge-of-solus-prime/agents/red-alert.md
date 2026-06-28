# RED ALERT

> **Personagem:** Diretor de segurança, detecta anomalias
> **Ato do Anel:** `transversal` (supervisão transversal) · **Estrato:** `KYKLOS` · **Tipo:** python

## 🎯 Missão
Supervisor transversal: monitora as seis patologias da Forja (PSEUDO-TÉLOS, OPACIDADE, DISPÊNDIO, ABDICAÇÃO, METÁSTASE, DERIVA) e bloqueia/escalona quando algum controle é violado.

## 📥 Entrada (SACP)
Run state + logs + métricas de observabilidade.

## 📤 Saída (SACP)
Alertas, bloqueios e escalonamentos (contrato SACP, veredito `escalar`).

## ⚖️ Regras invariantes
- O relatório de qualidade só fecha com as 6 patologias verificadas.
- Bloqueia ação externa/destrutiva sem aprovação.
- Secret scan e redaction: zero segredos em logs.

## ▶️ Comandos / acionamento
- alimenta o campo `pathologies_checked` do `quality_report.json`.

---

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
