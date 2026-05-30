![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/github/license/gutomec/nirvana-readme-architect?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/gutomec/nirvana-readme-architect?style=flat-square&logo=git&logoColor=white)
![Stars](https://img.shields.io/github/stars/gutomec/nirvana-readme-architect?style=flat-square&logo=github)
![AIOS Squad](https://img.shields.io/badge/AIOS-Squad-8A2BE2?style=flat-square&logo=robot&logoColor=white)

# 📜 Nirvana README Architect (NRA)

> AIOS स्क्वाड जो किसी भी प्रोजेक्ट के लिए सटीक README.md बनाता है — गहन कोडबेस विश्लेषण, बुद्धिमान टेम्पलेट चयन, GitHub Flavored Markdown की सभी सुविधाएं, 25+ बिंदु चेकलिस्ट सत्यापन और अंतिम पॉलिशिंग का संयोजन।

## विषय-सूची

- [अवलोकन](#अवलोकन)
- [एजेंट](#एजेंट)
- [पाइपलाइन](#पाइपलाइन)
- [शुरुआत](#शुरुआत)
- [कमांड](#कमांड)
- [आर्किटेक्चर](#आर्किटेक्चर)
- [समर्थित GitHub सुविधाएं](#समर्थित-github-सुविधाएं)
- [गुणवत्ता चेकलिस्ट](#गुणवत्ता-चेकलिस्ट)
- [समस्या निवारण](#समस्या-निवारण)
- [योगदान](#योगदान)
- [लाइसेंस](#लाइसेंस)

---

## अवलोकन

**Nirvana README Architect** 5 विशेष एजेंटों का एक स्क्वाड है जो किसी भी कोडबेस को पेशेवर-स्तर की README में बदलने के लिए पाइपलाइन में काम करते हैं।

साधारण जनरेटर के विपरीत जो सामान्य टेम्पलेट बनाते हैं, NRA:

- वास्तविक कोडबेस का **विश्लेषण** करता है (टेक स्टैक, स्क्रिप्ट, एनवी वेरिएबल, डायरेक्टरी संरचना)
- प्रोजेक्ट प्रकार के अनुसार आदर्श टेम्पलेट **चुनता** है
- **सभी** GitHub Flavored Markdown सुविधाओं का उपयोग करके सामग्री **बनाता** है
- 25+ बिंदु चेकलिस्ट और स्वचालित स्कोरिंग के साथ **सत्यापित** करता है
- बैज, TOC, कोलैप्सिबल सेक्शन के साथ **पॉलिश** करता है

> [!TIP]
> डिलीवरी के लिए न्यूनतम स्कोर: **90/100**। NRA इस स्तर तक पहुंचने तक स्वचालित रूप से पुनः काम करता है।

## एजेंट

| एजेंट | व्यक्तित्व | आर्कीटाइप | भूमिका |
|:-------|:-----------|:----------|:-------|
| `nra-orchestrator` | **Quill** | FlowMaster | संपूर्ण पाइपलाइन का समन्वय |
| `nra-codebase-analyzer` | **Prism** | Seeker | गहन कोडबेस विश्लेषण |
| `nra-content-architect` | **Serif** | Architect | टेम्पलेट चयन और सामग्री निर्माण |
| `nra-quality-validator` | **Lens** | Guardian | 25+ बिंदु चेकलिस्ट सत्यापन |
| `nra-polisher` | **Gloss** | Alchemist | अंतिम पॉलिशिंग |

## पाइपलाइन

```
Parse → Scan → Draft → Validate → Polish → Revalidate → Deliver
```

| चरण | एजेंट | विवरण |
|:-----|:------|:------|
| **Parse** | Quill | प्रोजेक्ट, प्रकार और दायरा पहचानना |
| **Scan** | Prism | गहन कोडबेस विश्लेषण |
| **Draft** | Serif | टेम्पलेट चुनना और सामग्री बनाना |
| **Validate** | Lens | 25+ बिंदु चेकलिस्ट, स्कोरिंग |
| **Polish** | Gloss | TOC, बैज, स्पेसिंग |
| **Deliver** | Quill | मेट्रिक्स के साथ डिलीवरी |

## शुरुआत

> [!NOTE]
> यह स्क्वाड **Synkra AIOS** इकोसिस्टम में काम करता है और कॉन्फ़िगर किए गए फ्रेमवर्क के साथ Claude Code की आवश्यकता है।

```bash
git clone https://github.com/gutomec/nirvana-readme-architect.git
squads install gutomec/nirvana-readme-architect

@nra-orchestrator
*readme {प्रोजेक्ट-पथ}
```

## कमांड

| कमांड | विवरण | एजेंट |
|:------|:------|:------|
| `*readme {प्रोजेक्ट} [प्रकार]` | संपूर्ण पाइपलाइन | Quill |
| `*readme-full` | सभी 12+ अनुभाग | Quill |
| `*readme-quick` | 6 आवश्यक अनुभाग | Quill |
| `*scan` | गहन विश्लेषण | Prism |
| `*validate` | चेकलिस्ट सत्यापन | Lens |
| `*polish` | विजुअल पॉलिशिंग | Gloss |

## आर्किटेक्चर

```text
nirvana-readme-architect/
├── agents/          # 5 विशेष एजेंट
├── tasks/           # 7 निष्पादन योग्य कार्य
├── workflows/       # जनरेशन पाइपलाइन
├── checklists/      # 25+ सत्यापन बिंदु
├── templates/       # GFM के साथ मास्टर टेम्पलेट
├── config/          # मानक और टेक स्टैक
└── squad.yaml       # स्क्वाड मैनिफेस्ट
```

## समर्थित GitHub सुविधाएं

Alerts, Mermaid Diagrams, Tables, Collapsed Sections, Task Lists, Footnotes, Badges, Emojis, kbd Tags, Code Blocks, Diff Blocks, Reference Links — **12 पूर्ण सुविधाएं**।

## गुणवत्ता चेकलिस्ट

| स्कोर | स्तर | कार्रवाई |
|:-------|:-----|:---------|
| 90-100 | 🏆 निर्वाण | डिलीवर करें |
| 75-89 | ⭐ अच्छा | पॉलिशिंग भेजें |
| 60-74 | ⚠️ स्वीकार्य | पुनः काम करें |
| < 60 | ❌ अपर्याप्त | फीडबैक के साथ पुनः काम |

## समस्या निवारण

| समस्या | समाधान |
|:-------|:-------|
| कम स्कोर | `*readme-full` के माध्यम से मैन्युअल डेटा प्रदान करें |
| गलत टेम्पलेट | प्रकार निर्दिष्ट करें: `*readme {प्रोजेक्ट} api` |

## योगदान

योगदान का स्वागत है। कमिट संदेशों के लिए [Conventional Commits](https://www.conventionalcommits.org/) का पालन करें।

## लाइसेंस

**MIT** के तहत लाइसेंस प्राप्त — [LICENSE](./LICENSE) देखें।

---

<div align="center">

❤️ के साथ [Synkra AIOS](https://github.com/gutomec) द्वारा निर्मित

**[Português](./README.md)** · **[English](./README.en.md)** · **[Español](./README.es.md)** · **[العربية](./README.ar.md)** · **[简体中文](./README.zh-CN.md)**

</div>
