"""30 Fixtures de roteamento para validação da Fase 2.

Cada fixture mapeia uma demanda textual aos squads esperados.
Ground truth baseado em SQUAD_INDEX.md e descrições reais dos squads.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class RoutingFixture:
    """Uma fixture de roteamento com demanda e squads esperados."""

    id: str
    task_description: str
    expected_top_squads: List[str]  # IDs esperados no Top-3
    category: str  # conteudo, desenvolvimento, iffar, financeiro, etc


FIXTURES = [
    # ===== CONTEÚDO & MARKETING =====
    RoutingFixture(
        id="F001",
        task_description="Preciso criar um carrossel para Instagram com design profissional",
        expected_top_squads=[
            "instagram-carrossel-visual-pro",
            "Maeve Carrossel Premium Instagram PT-BR",
            "VetorNexo",
        ],
        category="conteudo"
    ),

    RoutingFixture(
        id="F002",
        task_description="Transformar artigos científicos em conteúdo didático para educação",
        expected_top_squads=[
            "Copo de Cafe Academico Squad",
            "Revisao Bibliografica Automatizada Squad",
            "Mentor IA Educacao Squad",
        ],
        category="conteudo"
    ),

    RoutingFixture(
        id="F003",
        task_description="Produzir podcast acadêmico com disseminação científica",
        expected_top_squads=[
            "copo-de-cafe-podcast-squad",
            "Manim Science Studio Squad",
            "SCRIPTORIUM Squad",
        ],
        category="conteudo"
    ),

    RoutingFixture(
        id="F004",
        task_description="Gerar vídeos educacionais estilo 3Blue1Brown com Manim",
        expected_top_squads=[
            "manim-science-studio-squad",
            "THEORÍA",
            "ARKHEION",
        ],
        category="conteudo"
    ),

    RoutingFixture(
        id="F005",
        task_description="Criar dossiê audiovisual confidencial com estética arquivo",
        expected_top_squads=[
            "ARKHEION",
            "THEORÍA",
            "manim-science-studio-squad",
        ],
        category="conteudo"
    ),

    # ===== DESENVOLVIMENTO & SISTEMAS =====
    RoutingFixture(
        id="F006",
        task_description="Construir novo squad com CLI, workflows e validação determinística",
        expected_top_squads=[
            "maeve-genius-forge-squad",
            "Forge of Solus Prime",
            "Primus",
        ],
        category="desenvolvimento"
    ),

    RoutingFixture(
        id="F007",
        task_description="Transformar um vídeo em ferramental IA com PRD e squad.yaml",
        expected_top_squads=[
            "dedalo-fabrica-ferramentas-ia-squad",
            "forge-of-solus-prime",
            "harness-foundry-squad",
        ],
        category="desenvolvimento"
    ),

    # ===== INTELIGÊNCIA & ANÁLISE =====
    RoutingFixture(
        id="F008",
        task_description="Analisar competidores, detectar sinais fracos e monitorar ameaças",
        expected_top_squads=[
            "darkhold-competitive-intelligence-squad",
            "mobius-chair-strategic-foresight-squad",
            "skeptic-protocol",
        ],
        category="inteligencia"
    ),

    RoutingFixture(
        id="F009",
        task_description="Mapear talentos, competências, risco de retenção e sucessão",
        expected_top_squads=[
            "allspark-talent-intelligence-squad",
            "matrix-of-leadership-squad",
            "nexum-cognitivo",
        ],
        category="inteligencia"
    ),

    RoutingFixture(
        id="F010",
        task_description="Amplificar inteligência de vendas e identificar oportunidades invisíveis",
        expected_top_squads=[
            "cerebro-sales-intelligence-squad",
            "squ-oraculo-aion-finance-super-squad",
            "darkhold-competitive-intelligence-squad",
        ],
        category="inteligencia"
    ),

    RoutingFixture(
        id="F011",
        task_description="Transformar dados brutos em inteligência de negócio viva com pipelines",
        expected_top_squads=[
            "vector-sigma-data-forge-squad",
            "squ-oraculo-aion-finance-super-squad",
            "atlas-visual-reports-squad-v1.2.0",
        ],
        category="inteligencia"
    ),

    RoutingFixture(
        id="F012",
        task_description="Mapear jornada do cliente, detectar fricções e projetar blueprints",
        expected_top_squads=[
            "mother-box-experience-squad",
            "skeptic-protocol",
            "prisma-real-problem-squad",
        ],
        category="inteligencia"
    ),

    # ===== JURÍDICO & CONFORMIDADE =====
    RoutingFixture(
        id="F013",
        task_description="Analisar contratos administrativos públicos conforme CGU e TCU",
        expected_top_squads=[
            "themis-contratos-publicos-squad",
            "scriba-contratos-squad",
            "farol-contratos-licitacoes-iffar",
        ],
        category="juridico"
    ),

    RoutingFixture(
        id="F014",
        task_description="Gerar minuta de contrato administrativo federal com Lei 14.133/2021",
        expected_top_squads=[
            "scriba-contratos-squad",
            "pearson-specter-nova-legal-squad",
            "themis-contratos-publicos-squad",
        ],
        category="juridico"
    ),

    RoutingFixture(
        id="F015",
        task_description="Gerir ciclo de vida de contratos: extração, classificação, conformidade",
        expected_top_squads=[
            "projur-contracts-squad",
            "farol-contratos-licitacoes-iffar",
            "scriba-contratos-squad",
        ],
        category="juridico"
    ),

    RoutingFixture(
        id="F016",
        task_description="Detectar e gerenciar crises corporativas com plano de comunicação",
        expected_top_squads=[
            "omega-lock-crisis-management-squad",
            "soulsword-personal-branding-squad",
            "matrix-of-leadership-squad",
        ],
        category="juridico"
    ),

    # ===== LICITAÇÕES & ORÇAMENTO =====
    RoutingFixture(
        id="F017",
        task_description="Montar processo de licitação completo: DFD, ETP, TR, edital",
        expected_top_squads=[
            "hefesto-forja-licitatoria-squad",
            "farol-contratos-licitacoes-iffar",
            "farol-pcfp-squad",
        ],
        category="iffar"
    ),

    RoutingFixture(
        id="F018",
        task_description="Calcular PCFP (Planilha de Custos e Formação de Preços) com TCU",
        expected_top_squads=[
            "farol-pcfp-squad",
            "squad-pcfp",
            "squ-tesouraria-publica-squad",
        ],
        category="iffar"
    ),

    RoutingFixture(
        id="F019",
        task_description="Gerenciar execução orçamentária, restos a pagar e prestação de contas",
        expected_top_squads=[
            "squ-tesouraria-publica-squad",
            "farol-contratos-licitacoes-iffar",
            "compliance-ia-iffar-squad",
        ],
        category="iffar"
    ),

    # ===== EDUCAÇÃO & RECURSOS HUMANOS =====
    RoutingFixture(
        id="F020",
        task_description="Automatizar ciclo acadêmico: PPC, integralização, matrícula",
        expected_top_squads=[
            "bussola-academica-iffar-squad",
            "squad-docente-iffar",
            "mentor-ia-educacao-squad",
        ],
        category="iffar"
    ),

    RoutingFixture(
        id="F021",
        task_description="Reforço neurocognitivo para crianças com atividades adaptativas",
        expected_top_squads=[
            "reforco-neurocognitivo-infantil-squad",
            "maeve-lumen-leitura-squad",
            "mentor-ia-educacao-squad",
        ],
        category="educacao"
    ),

    RoutingFixture(
        id="F022",
        task_description="Automação do trabalho docente: plano, materiais, avaliações, AEE",
        expected_top_squads=[
            "squad-docente-iffar",
            "bussola-academica-iffar-squad",
            "reforco-neurocognitivo-infantil-squad",
        ],
        category="iffar"
    ),

    RoutingFixture(
        id="F023",
        task_description="Treinar liderança executiva com coaching, 360° e planejamento de sucessão",
        expected_top_squads=[
            "matrix-of-leadership-squad",
            "maeve-neurocognitive-intelligence-trainer-squad",
            "allspark-talent-intelligence-squad",
        ],
        category="desenvolvimento"
    ),

    # ===== PESQUISA & CONHECIMENTO =====
    RoutingFixture(
        id="F024",
        task_description="Pesquisa científica com síntese de evidências e artigo acadêmico",
        expected_top_squads=[
            "Maeve Atena Mimir",
            "Revisao Bibliografica Automatizada Squad",
            "SCRIPTORIUM Squad",
        ],
        category="pesquisa"
    ),

    RoutingFixture(
        id="F025",
        task_description="Transformar Obsidian Vault em base de conhecimento pesquisável",
        expected_top_squads=[
            "universal-obsidian-knowledge-squad",
            "maeve-knowledge-graph-forge-squad",
            "notion-second-brain-squad",
        ],
        category="conhecimento"
    ),

    RoutingFixture(
        id="F026",
        task_description="Produção acadêmica fim-a-fim com verificação de citações",
        expected_top_squads=[
            "scriptorium-squad",
            "maeve-atena-mimir-scienceclaw-research",
            "revisao-bibliografica-automatizada-squad",
        ],
        category="pesquisa"
    ),

    # ===== INCUBAÇÃO & NEGÓCIOS =====
    RoutingFixture(
        id="F027",
        task_description="Transformar ideias em negócios AI Native: MVP, go-to-market, roadmap",
        expected_top_squads=[
            "manopla-da-forja-venture-squad",
            "maeve-athena-mimir-venture-forge-squad",
            "anvil-of-annwn-super-squad-system",
        ],
        category="negocio"
    ),

    RoutingFixture(
        id="F028",
        task_description="Operacionalizar pipeline TRL e Lean Canvas da incubadora",
        expected_top_squads=[
            "integra-incubadora-ops-squad",
            "orbita-incubadora-squad",
            "manopla-da-forja-venture-squad",
        ],
        category="iffar"
    ),

    # ===== GOVERNANÇA & ESTRATÉGIA =====
    RoutingFixture(
        id="F029",
        task_description="Governança do PDI com metas, indicadores, riscos e pactos por campus",
        expected_top_squads=[
            "pdi-vivo-iffar-squad",
            "vector-sigma-data-forge-squad",
            "mobius-chair-strategic-foresight-squad",
        ],
        category="iffar"
    ),

    RoutingFixture(
        id="F030",
        task_description="Planejamento de cenários, prospeção estratégica e inteligência de futuros",
        expected_top_squads=[
            "mobius-chair-strategic-foresight-squad",
            "darkhold-competitive-intelligence-squad",
            "skeptic-protocol",
        ],
        category="estrategia"
    ),
]


def get_fixture_by_id(fixture_id: str) -> RoutingFixture:
    """Retorna uma fixture pelo ID."""
    for f in FIXTURES:
        if f.id == fixture_id:
            return f
    raise ValueError(f"Fixture não encontrada: {fixture_id}")


def get_fixtures_by_category(category: str) -> list[RoutingFixture]:
    """Retorna todas as fixtures de uma categoria."""
    return [f for f in FIXTURES if f.category == category]


def all_fixtures() -> list[RoutingFixture]:
    """Retorna todas as 30 fixtures."""
    return FIXTURES
