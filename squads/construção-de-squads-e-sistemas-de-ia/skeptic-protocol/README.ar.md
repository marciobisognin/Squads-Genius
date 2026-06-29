# SKEPTIC Protocol

تنفيذ بروتوكول SKEPTIC (الشك البناء) عبر 5 مراحل صارمة لهندسة البرمجيات الوقائية.

## التثبيت

1. انقل أو استنسخ المجلد `skeptic-protocol` إلى مسار squads في AIOX.
2. تأكد من أن AIOX CLI يتعرف على الحزمة.
3. استدعِ الوكلاء باستخدام البادئة `/sk`.

## ما الذي يفعله

يطبق هذا الفريق الشك البناء من خلال إجبار النظام على التعرف على جميع العيوب الأمنية والتصميمية المحتملة قبل كتابة السطر الأول من الكود البرمجي. يحل محل نهج "ابنِ ثم اختبر" ليصبح "توقع العيوب، أثبتها باختبارات فاشلة، ثم قم بتنفيذ الحل".

## Pipeline

| المرحلة | الوكيل | الدور | النموذج |
|---------|--------|-------|---------|
| 1 | `failure-predictor` | Accusation Specialist | Guardian |
| 2 | `test-engineer` | Defense Specialist | Builder |
| 3 | `solution-implementer` | Trial Developer | Builder |
| 4 | `red-teamer` | Appeal Challenger | Balancer |
| 5 | `skeptic-orchestrator`| Verdict & Protocol Manager | Flow_Master |

## Agents

| الوكيل | العنوان | Archetype | الوصف |
|--------|---------|-----------|-------|
| `failure-predictor` | Accusation Specialist | Guardian | يحدد أوضاع الفشل بشكل شامل دون إنشاء أكواد. |
| `test-engineer` | Defense Specialist | Builder | ينشئ حزم اختبار تركز على الاتهامات وتفشل عمداً (Red Phase). |
| `solution-implementer` | Trial Developer | Builder | يكتب كود البرمجة لاجتياز الاختبارات فقط. |
| `red-teamer` | Appeal Challenger | Balancer | يتصرف كخصم قاسي لكسر الكود باستخدام حالات الحافة (edge cases). |
| `skeptic-orchestrator` | Verdict & Protocol Manager | Flow_Master | يضمن سيولة البروتوكول ويقوم بإنشاء السجل الرسمي SKEPTIC_REPORT.md. |

## Tasks

| المهمة | المسؤول | Atomic Layer | الوصف |
|--------|---------|-------------|-------|
| `generateAccusations()` | `FailurePredictor` | Organism | يجمع الثغرات الأمنية مفصلاً مستوى الخطورة والاحتمال. |
| `writeFailingTests()` | `TestEngineer` | Organism | يحول الثغرات إلى اختبارات عملية سلبية. |
| `implementTrialCode()` | `SolutionImplementer` | Organism | يبرمج الحل لتلبية قيود الدفاع فقط. |
| `executeAppeal()` | `RedTeamer` | Molecule | يتحدى بنشاط الكود البرمجي المعتمد. |
| `generateVerdictReport()`| `SkepticOrchestrator` | Molecule | يقيم الإحصائيات النهائية ويقوم بإنشاء الوثائق. |

## Workflows

| سير العمل | Pattern | الوكلاء | الوصف |
|----------|---------|---------|-------|
| `skeptic_pipeline_execution` | Pipeline | الـ 5 وكلاء | التنفيذ الرئيسي للمراحل الخمس المتسلسلة. |
| `red_team_feedback_loop` | Evaluator-Optimizer | `red-teamer`, `failure-predictor`, `solution-implementer` | حلقة ردود الفعل في حال كسرت مرحلة الاستئناف (Appeal) الكود. |

## التكوين

- config/coding-standards.md
- config/tech-stack.md
- config/source-tree.md

## الاستخدام

### الأوامر المتاحة

- `*generate-accusations`: يقيم المتطلبات وينشئ الاستنتاجات في شكل Markdown.
- `*write-failing-tests`: يبني حزم الاختبار الأساسية.
- `*implement-trial-code`: ينفذ روتين الأكواد المنتجة.
- `*execute-appeal`: ينفذ اختبار الاختراق (pentest).
- `*generate-verdict-report`: يجمع تقرير دورة SKEPTIC النهائي.

### أمثلة

```bash
# لبدء العمل من الصفر
/sk:failure-predictor
*generate-accusations --objective="تطوير نظام تسجيل الدخول"
```

## Autor

Marcio Bisognin

[Squads Platform](https://squads.sh/pt)
[Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## الترخيص

MIT
