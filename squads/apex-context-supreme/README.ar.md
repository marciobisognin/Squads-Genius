# apex-context-supreme

فريق هندسة السياق الأسمى، والإثراء، وتحسين نافذة السياق. يحول المشاريع غير المنظمة إلى قواعد معرفية عالية الأداء لعملاء الذكاء الاصطناعي، مما يضمن أقصى كثافة دلالية بأقل عدد من الرموز (Tokens).

متوافق تمامًا مع Claude و Gemini و Codex و Antigravity.

## التثبيت

```bash
npx squads add olympus-forge/apex-context-supreme
```

## ماذا يفعل

يقوم **APEX-CONTEXT SUPREME** بأتمتة إنشاء قواعد السياق (`CLAUDE.md`, `GEMINI.md`, إلخ) من خلال خط أنابيب (Pipeline) مكون من 4 مراحل:

- **الهندسة التقنية**: المسح المتكرر ورسم خرائط المكدس التقني (Tech Stack).
- **الإثراء الدلالي (Semantic Enrichment)**: حقن حكمة تقنية عميقة وتعليمات قابلة للتنفيذ.
- **نحت الرموز (Token Sculpting)**: إزالة التكرار عبر المنصات وتقليم الضوضاء.
- **التحقق من الجودة**: الامتثال لمعايير AIOS وسلامة الروابط.

## خط الأنابيب (Pipeline)

| المرحلة | العميل (Agent) | الدور | النموذج |
|-------|-------|------|-------|
| 1 | 🏛️ Maven | Blueprint Architect | Sonnet |
| 2 | ✨ Spark | Context Alchemist | Opus |
| 3 | ✂️ Trim | Token Sculptor | Sonnet |
| 4 | ⚖️ Vigil | Quality Guardian | Flash |

## العملاء (Agents)

| الأيقونة | العميل | العنوان | النمط الفني (Archetype) | الوصف |
|------|-------|-------|-----------|-------------|
| 🚀 | apex-orquestrista | Context Orchestration Specialist | Flow_Master | العقل المركزي ومنسق خط الأنابيب |
| 🏛️ | maven-arquiteta | Technical Blueprint Architect | Builder | يمسح المشروع ويحدد المخطط التقني |
| ✨ | spark-alquimista | Context Enrichment Specialist | Builder | يولد قواعد دلالية كثيفة |
| ✂️ | trim-escultor | Context Window Optimizer | Balancer | يحسن الكثافة ويزيل التكرار |
| ⚖️ | vigil-validadora | Quality Assurance Specialist | Guardian | يتحقق من السلامة والامتثال لـ AIOS |

## المهام (Tasks)

| المهمة | المسؤول | الطبقة الذرية (Atomic Layer) | الوصف |
|------|-------------|--------------|-------------|
| `arquitetarContexto()` | maven-arquiteta | Molecule | يولد blueprint.yaml و inventory.json |
| `enriquecerContexto()` | spark-alquimista | Organism | ينشئ ملفات قواعد (.md) غنية |
| `otimizarContexto()` | trim-escultor | Molecule | يقلل الضوضاء ويحسن الرموز (Tokens) |
| `validarContexto()` | vigil-validadora | Molecule | ينفذ بوابة الجودة وفحص الامتثال |

## سير العمل (Workflows)

| سير العمل | النمط (Pattern) | العملاء | الوصف |
|----------|---------|---------|-------------|
| `apex_context_pipeline` | Sequential Pipeline | Maven → Spark → Trim → Vigil | تدفق كامل من 4 مراحل |

## التكوين (Config)

- `config/coding-standards.md` — اتفاقيات التسمية والوثائق
- `config/tech-stack.md` — البرمجيات والأطر المدعومة
- `config/source-tree.md` — الهيكل التنظيمي للفريق

## الاستخدام (Usage)

### الأوامر الرئيسية

| الأمر | الوصف | مثال |
|---------|-----------|---------|
| `*iniciar-pipeline` | يبدأ التدفق الكامل | `/apex:iniciar-pipeline` |
| `*status-apex` | يظهر حالة السياق | `/apex:status-apex` |
| `*set-platform` | يحدد تركيز التحسين | `/apex:set-platform --name=gemini` |

## المؤلف

تم إنشاؤه بواسطة **Nirvana Squad Creator** (تم تنقيحه بواسطة Antigravity)

## الترخيص

MIT
