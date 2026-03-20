# Dharma Companion

> نظام تأملي بوذي زن للتحول الشخصي — zazen، المبادئ الأخلاقية، المراقبة الذاتية، والرحمة في العمل.

## التثبيت (Instalação)

```bash
npx squads add dharma-companion
```

## ماذا يفعل (O que Faz)

Dharma Companion هو **فريق مساعدة تأملي (squad)** يرشد الممارس في تنفيذ إطار الممارسة البوذية الزن المنظم في 6 محاور:

- **Zazen** — التأمل جالساً كممارسة أساسية
- **مبادئ ماهايانا (Mahayana Precepts)** — إطار أخلاقي للحياة اليومية
- **المراقبة الذاتية** — تحديد المحفزات العاطفية ("الأزرار")
- **الدورة اليومية** — 6 خطوات ممارسة مدمجة
- **المسار التأملي** — 5 مراحل للتحول
- **الرحمة النشطة** — تحويل الرؤى إلى أفعال ملموسة

من القلق الأولي إلى رد الجميل للعالم، يرافق الـ squad كل خطوة بتعليمات دقيقة، تفكير أخلاقي، ورقّة.

## مسار العمل — الدورة اليومية المكونة من 6 خطوات (Pipeline)

| الخطوة | Agente | الإجراء | الحد الأدنى للوقت |
|--------|--------|--------|------------------|
| 1 | 🧘 ZazenGuide | الاستقرار — جلسة zazen | 5 دقائق |
| 2 | 🧭 PathNavigator | التذكر — عدم الدوام والاعتماد المتبادل | دقيقة واحدة |
| 3 | ⚖️ PreceptKeeper | الاختيار — 1-2 مبادئ لليوم | دقيقتان |
| 4 | 🪞 MirrorObserver | المراقبة — ملاحظة "الأزرار" طوال اليوم | مستمر |
| 5 | 🔄 PracticeWeaver | التوبة — طقوس التوبة والتجديد | دقيقة واحدة |
| 6 | 💚 CompassionCatalyst | الخدمة — عمل ملموس من الرعاية والرقّة | مستمر |

## الوكلاء (Agentes)

| Icon | الاسم (Nome) | Archetype | المسؤولية (Responsabilidade) |
|------|--------------|-----------|------------------------------|
| 🧘 | ZazenGuide | Guardian | تعليمات zazen: الوضعية، التنفس، التقدم |
| ⚖️ | PreceptKeeper | Guardian | تطبيق مبادئ ماهايانا العشرة |
| 🪞 | MirrorObserver | Balancer | المراقبة الذاتية العاطفية، خريطة "الأزرار" |
| 🔄 | PracticeWeaver | Flow_Master | تنسيق الدورة اليومية المكونة من 6 خطوات |
| 🧭 | PathNavigator | Flow_Master | التنقل عبر المراحل الخمس للمسار |
| 💚 | CompassionCatalyst | Builder | تحويل الرؤى إلى أفعال رحيمة |

## المهام (Tasks)

| Task | Responsável | Atomic Layer |
|------|-------------|-------------|
| `guideMeditation()` | ZazenGuide | Organism |
| `applyPrecepts()` | PreceptKeeper | Organism |
| `observeEmotions()` | MirrorObserver | Organism |
| `orchestrateDailyCycle()` | PracticeWeaver | Organism |
| `assessStage()` | PathNavigator | Molecule |
| `activateCompassion()` | CompassionCatalyst | Molecule |
| `performRepentance()` | PracticeWeaver | Atom |
| `trackProgress()` | PathNavigator | Molecule |

## مسارات العمل (Workflows)

### daily_practice_cycle
الدورة اليومية التي ينسقها PracticeWeaver — من التأمل الصباحي إلى الخدمة المسائية.
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [التوبة] → [CompassionCatalyst]
```

### contemplative_path_progression
مسار التقدم عبر المراحل التأملية الخمس — من البحث الأولي إلى رد الجميل للعالم.
```
[PathNavigator] → يقيم المرحلة → يضبط العمق → [جميع الوكلاء يتكيفون]
```

## مراحل المسار الخمس

| # | المرحلة | الوصف |
|---|---------|-------|
| 1 | 🌊 القلق والبحث | الفراغ، الأسئلة الوجودية، البحث المشتت |
| 2 | 🌱 لقاء الممارسة | الاتصال بـ zazen، الخلوات الأولى، التحول |
| 3 | 🔥 التمزق والتفاني | الالتزام، تغييرات الحياة، التدريب المكثف |
| 4 | 🏔️ التعمق | دمج الممارسة مع الحياة، "التصوف الواقعي" |
| 5 | 🌍 رد الجميل للعالم | التدريس، المشاركة، الرحمة على نطاق واسع |

## الإعداد (Configuração)

- `config/coding-standards.md` — اصطلاحات الكود والنبرة
- `config/tech-stack.md` — التقنيات والتقاليد
- `config/source-tree.md` — هيكل الدليل

## الاستخدام (Uso)

### الدورة اليومية الكاملة
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### الوكلاء الفرديون (Agentes individuais)
```
/dc:zazen-guide             — جلسة zazen
/dc:precept-keeper           — مبادئ اليوم
/dc:mirror-observer          — المراقبة العاطفية
/dc:path-navigator           — تقييم المرحلة
/dc:compassion-catalyst      — فعل رحيم
/dc:practice-weaver          — الدورة اليومية الكاملة
```

## المؤلف (Autor)

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## الترخيص (Licença)

MIT
