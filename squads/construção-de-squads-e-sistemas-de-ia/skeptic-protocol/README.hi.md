# SKEPTIC Protocol

प्रिवेंटिव सॉफ्टवेयर इंजीनियरिंग (preventive software engineering) के लिए SKEPTIC Protocol (Constructive Skepticism) के 5 कठोर चरणों का कार्यान्वयन।

## स्थापना (Installation)

1. अपनी AIOX squads डायरेक्टरी में `skeptic-protocol` फोल्डर को मूव या क्लोन करें।
2. सुनिश्चित करें कि AIOX CLI पैकेज को पहचानता है।
3. `/sk` प्रिफिक्स (prefix) का उपयोग करके एजेंटों (agents) को इन्वोक (invoke) करें।

## यह क्या करता है

यह squad रचनात्मक संशयवाद लागू करता है जो implementation कोड की पहली लाइन लिखे जाने से पहले सभी संभावित कोड खामियों को पहचानने के लिए मजबूर करता है। यह साधारण "build and test" नजरिए को "flaws को पहले प्रेडिक्ट (predict) करें, विफल होने वाले टेस्ट्स के साथ साबित करें और उसके बाद ही समाधान (solution) लागू करें" के साथ बदलता है।

## Pipeline

| चरण | एजेंट | भूमिका | मॉडल |
|-----|--------|-------|--------|
| 1 | `failure-predictor` | Accusation Specialist | Guardian |
| 2 | `test-engineer` | Defense Specialist | Builder |
| 3 | `solution-implementer` | Trial Developer | Builder |
| 4 | `red-teamer` | Appeal Challenger | Balancer |
| 5 | `skeptic-orchestrator`| Verdict & Protocol Manager | Flow_Master |

## Agents

| एजेंट | टाइटल | Archetype | विवरण |
|--------|--------|-----------|-----------|
| `failure-predictor` | Accusation Specialist | Guardian | बिना कोड बनाए फेल्योर मोड्स (failure modes) को विस्तार से पहचानता है। |
| `test-engineer` | Defense Specialist | Builder | Accusations पर केंद्रित टेस्ट सूट (test suite) बनाता है, जो जानबूझकर विफल होते हैं (Red Phase)। |
| `solution-implementer` | Trial Developer | Builder | टेस्ट सूट पास करने के एकमात्र उद्देश्य से कोड को लागू और रिफैक्टर करता है। |
| `red-teamer` | Appeal Challenger | Balancer | एज केसेस (edge cases) के माध्यम से बनाए गए समाधान (solution) को तोड़ने का प्रयास करता है। |
| `skeptic-orchestrator` | Verdict & Protocol Manager | Flow_Master | प्रोटोकॉल में सुगमता सुनिश्चित करता है और SKEPTIC_REPORT.md रिपोर्ट तैयार करता है। |

## Tasks

| टास्क | जिम्मेदार | Atomic Layer | विवरण |
|------|-------------|-------------|-----------|
| `generateAccusations()` | `FailurePredictor` | Organism | गंभीरताओं (severity) और संभावनाओं के विवरण के साथ कमजोरियों (vulnerabilities) को इकट्ठा करता है। |
| `writeFailingTests()` | `TestEngineer` | Organism | कमजोरियों को व्यावहारिक नेगेटिव टेस्ट्स (negative tests) में ट्रांसक्राइब करता है। |
| `implementTrialCode()` | `SolutionImplementer` | Organism | डिफेंस (Defense) के नियमों को संतुष्ट करने के लिए समाधान को कोड करता है। |
| `executeAppeal()` | `RedTeamer` | Molecule | ट्रायल (Trial) चरण में स्वीकृत कोडबेस को सक्रिय रूप से चुनौती देता है। |
| `generateVerdictReport()`| `SkepticOrchestrator` | Molecule | अंतिम आंकड़ों का मूल्यांकन और दस्तावेज़ीकरण (documentation) जनरेट करता है। |

## Workflows

| वर्कफ़्लो | Pattern | एजेंट | विवरण |
|----------|---------|---------|-----------|
| `skeptic_pipeline_execution` | Pipeline | सभी 5 | कार्यप्रणाली (methodology) के 5 चरणों का मुख्य, रेखीय (linear) निष्पादन। |
| `red_team_feedback_loop` | Evaluator-Optimizer | `red-teamer`, `failure-predictor`, `solution-implementer` | अपील (Appeal) के द्वारा कोड तोड़े जाने पर एडवरसेरियल लूप चालू होता है। |

## कॉन्फ़िगरेशन (Configuration)

- config/coding-standards.md
- config/tech-stack.md
- config/source-tree.md

## उपयोग (Usage)

### उपलब्ध कमांड्स (Available Commands)

- `*generate-accusations`: आवश्यकताओं (requirements) का मूल्यांकन और Markdown में एक्यूज़ेशन्स बनाता है।
- `*write-failing-tests`: एक्यूज़ेशन्स के आधार पर प्रारंभिक टेस्ट सूट (test suite) बनाता है।
- `*implement-trial-code`: कोड को लागू करने की दिनचर्या।
- `*execute-appeal`: आंतरिक पेंटेस्ट (pentest) या एज केस समीक्षा करता है।
- `*generate-verdict-report`: SKEPTIC चक्र (cycle) की अंतिम रिपोर्ट (report) को संकलित करता है।

### उदाहरण (Examples)

```bash
# शुरू से पाइपलाइन (pipeline) को लॉन्च करने के लिए
/sk:failure-predictor
*generate-accusations --objective="MFA लॉगिन सिस्टम विकसित करें"
```

## Autor

Marcio Bisognin

[Squads Platform](https://squads.sh/pt)
[Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## लाइसेंस (License)

MIT
