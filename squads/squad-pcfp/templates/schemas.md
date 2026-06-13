# Schemas principais (seção 5 do PRD — handoffs schema-first)

Contratos JSON validados entre agentes. Na implementação de produção do PRD: Pydantic.

## ServiceProfile (A2 → todos)
```python
class ServiceProfile(BaseModel):
    tipo_servico: str                  # vigilancia, limpeza, recepcao...
    cbo: str                           # obrigatório (IN 176/2024)
    municipio: str
    uf: str
    escala: Literal["44h", "12x36_diurno", "12x36_noturno", ...]
    qtd_postos: int
    adicionais: list[Adicional]        # insalubridade, periculosidade...
    vigencia_meses: int
    cobertura_ininterrupta: bool       # habilita reposição/intrajornada (Módulo 4)
```

## CCTProfile (A4 → A5/A7, pós HITL Gate 1)
```python
class CCTProfile(BaseModel):
    registro_mediador: str             # número no Mediador/MTE
    vigencia: tuple[date, date]
    data_base: str                     # mês da data-base
    sindicatos: dict                   # laboral e patronal
    piso_por_funcao: dict[str, Decimal]
    adicionais: list[Adicional]        # com cláusula de origem
    beneficios: list[Beneficio]        # cada um com cláusula e valor
    clausulas_excluidas: list[str]     # art. 6º IN 05/2017 (PLR etc.), com motivo
    aprovacao_hitl1: Aprovacao         # responsável + data — obrigatório
```

## Rubrica (célula da CostSheet — A5)
```python
class Rubrica(BaseModel):
    modulo: str                        # "2.2"
    nome: str                          # "FGTS"
    valor: Decimal
    formula: str                       # "0.08 * (M1 + S2.1)"
    fundamento: list[Citacao]          # norma, artigo, redação vigente
    renovavel: bool                    # IN 07/2018
    conta_vinculada: bool              # Anexo XII
```

## ComplianceFinding (A6)
```python
class ComplianceFinding(BaseModel):
    severidade: Literal["info", "alerta", "critico"]
    rubrica: str | None
    descricao: str
    fundamento: Citacao
    recomendacao: str
```

## Aprovações HITL (Gates 1 e 2)
```python
class Aprovacao(BaseModel):
    gate: Literal["hitl1_enquadramento_sindical", "hitl2_aprovacao_final"]
    responsavel: str                   # obrigatório — "responsável pela validação"
    data: datetime
    decisao: str                       # aprovado / aprovado com ressalvas / reprovado
    observacoes: str | None
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
