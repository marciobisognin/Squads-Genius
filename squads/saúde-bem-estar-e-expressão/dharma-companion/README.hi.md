# Dharma Companion

> व्यक्तिगत परिवर्तन के लिए ज़ेन बौद्ध चिंतन प्रणाली — zazen, नैतिक नियम, आत्म-निरीक्षण और कार्य में करुणा।

## स्थापना (Installation)

```bash
npx squads add dharma-companion
```

## यह क्या करता है (What It Does)

Dharma Companion एक **चिंतनशील सहायता squad** है जो अभ्यासकर्ता का 6 धुरियों पर आधारित ज़ेन बौद्ध अभ्यास ढांचे को लागू करने में मार्गदर्शन करता है:

- **Zazen** — मुख्य अभ्यास के रूप में बैठकर ध्यान करना
- **महायान शील (Mahayana Precepts)** — दैनिक जीवन के लिए नैतिक ढांचा
- **आत्म-निरीक्षण** — भावनात्मक ट्रिगर्स ("buttons") की पहचान
- **दैनिक चक्र** — 6 एकीकृत अभ्यास चरण
- **चिंतनशील मार्ग** — परिवर्तन के 5 चरण
- **सक्रिय करुणा** — अंतर्दृष्टि को ठोस कार्यों में बदलना

प्रारंभिक बेचैनी से लेकर दुनिया को वापस देने तक, squad सटीक निर्देश, नैतिक प्रतिबिंब और कोमलता के साथ हर कदम पर साथ चलता है।

## Pipeline — 6-चरणीय दैनिक चक्र

| चरण | Agente | कार्रवाई | न्यूनतम समय |
|-----|--------|----------|-------------|
| 1 | 🧘 ZazenGuide | स्थिर होना — zazen सत्र | 5 मिनट |
| 2 | 🧭 PathNavigator | याद रखना — अनित्यता और अन्योन्याश्रयता | 1 मिनट |
| 3 | ⚖️ PreceptKeeper | चुनना — दिन के लिए 1-2 शील | 2 मिनट |
| 4 | 🪞 MirrorObserver | निरीक्षण करना — दिन भर "buttons" पर ध्यान देना | निरन्तर |
| 5 | 🔄 PracticeWeaver | पश्चाताप — पश्चाताप और नवीनीकरण का अनुष्ठान | 1 मिनट |
| 6 | 💚 CompassionCatalyst | सेवा करना — देखभाल और कोमलता की ठोस कार्रवाई | निरन्तर |

## Agents

| Icon | नाम | Archetype | जिम्मेदारी |
|------|-----|-----------|------------|
| 🧘 | ZazenGuide | Guardian | zazen निर्देश: आसन, सांस लेना, प्रगति |
| ⚖️ | PreceptKeeper | Guardian | 10 महायान शीलों का अनुप्रयोग |
| 🪞 | MirrorObserver | Balancer | भावनात्मक आत्म-निरीक्षण, "buttons" मानचित्र |
| 🔄 | PracticeWeaver | Flow_Master | 6-चरणीय दैनिक चक्र का समन्वय |
| 🧭 | PathNavigator | Flow_Master | मार्ग के 5 चरणों के माध्यम से नेविगेशन |
| 💚 | CompassionCatalyst | Builder | अंतर्दृष्टि को दयालु कार्यों में परिवर्तित करना |

## Tasks

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

## Workflows

### daily_practice_cycle
PracticeWeaver द्वारा समन्वित दैनिक चक्र — सुबह के ध्यान से शाम की सेवा तक।
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [पश्चाताप] → [CompassionCatalyst]
```

### contemplative_path_progression
5 चिंतनशील चरणों के माध्यम से प्रगति पाइपलाइन — प्रारंभिक खोज से लेकर दुनिया को वापस देने तक।
```
[PathNavigator] → चरण का आकलन → गहराई को समायोजित करना → [सभी agents अनुकूलित होते हैं]
```

## मार्ग के 5 चरण

| # | चरण | विवरण |
|---|-----|-------|
| 1 | 🌊 बेचैनी और खोज | शून्यता, अस्तित्व संबंधी प्रश्न, बिखरी हुई खोज |
| 2 | 🌱 अभ्यास का सामना | zazen के साथ संपर्क, पहले वापसी, परिवर्तन |
| 3 | 🔥 टूटना और समर्पण | प्रतिबद्धता, जीवन में बदलाव, गहन प्रशिक्षण |
| 4 | 🏔️ गहरा करना | अभ्यास-जीवन एकीकरण, "यथार्थवादी रहस्यवाद" |
| 5 | 🌍 दुनिया को वापस देना | पढ़ाना, साझा करना, बड़े पैमाने पर करुणा |

## विन्यास (Configuration)

- `config/coding-standards.md` — कोडिंग परंपराएं और टोन
- `config/tech-stack.md` — प्रौद्योगिकियां और परंपरा
- `config/source-tree.md` — निर्देशिका संरचना

## उपयोग (Usage)

### पूरा दैनिक चक्र
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### व्यक्तिगत Agentes
```
/dc:zazen-guide             — zazen सत्र
/dc:precept-keeper           — दिन के लिए शील
/dc:mirror-observer          — भावनात्मक अवलोकन
/dc:path-navigator           — चरण का आकलन
/dc:compassion-catalyst      — दयालु कार्रवाई
/dc:practice-weaver          — पूरा दैनिक चक्र
```

## लेखक (Author)

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## लाइसेंस (License)

MIT
