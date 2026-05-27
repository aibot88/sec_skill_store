---
name: patent-source-analyzer
description: |
  ניתוח מקורות אמנות קודמת מ-URL לבוחני פטנטים. הפעל סקיל זה בכל פעם שמשתמש מספק קישור (URL) למקור כלשהו — פטנט, מאמר מדעי, דף אינטרנט, או כל מסמך אחר — ורוצה לנתח אותו לצורך חיפוש אמנות קודמת, הפקת ציטוטים, או הכנת דוח ניתוח. הסקיל מוריד את המקור, מנתח אותו בשפה משפטית מדויקת של פטנטים, ומייצר שני קבצי Word (.docx): אחד באנגלית ואחד בעברית עם ציטוטים מדויקים לעמודים ושורות. Use this skill when the user provides any URL for patent prior art analysis, even if they just say "analyze this", "what does this say", or "check this source".
---

# ניתוח מקורות פטנטים — Patent Source Analyzer

## מבוא

סקיל זה מיועד לבוחני פטנטים. בהינתן URL למקור, הסקיל:
1. מוריד ומעבד את תוכן המקור
2. מנתח אותו בשפה משפטית מדויקת של פטנטים
3. מייצר מסמך Word מפורט **באנגלית** עם ציטוטים מדויקים
4. מייצר מסמך Word **בעברית** עם מינוח משפטי ישראלי מדויק ועיצוב RTL
5. שומר את שני קבצי ה-DOCX בתיקיית `source_analyses/` בפרויקט

---

## שלב 1: הורדת המקור

השתמש ב-`WebFetch` להורדת תוכן ה-URL שסופק.

- אם ה-URL מסתיים ב-`.pdf` או שהתוכן מוחזר כ-PDF: נסה להוריד גם כ-HTML וגם כ-PDF. רוב APIs של פטנטים (Google Patents, Espacenet, USPTO) מאפשרים גישה ל-HTML.
- אם `WebFetch` מחזיר שגיאה או תוכן ריק: הודע למשתמש ובקש ממנו להוריד את הקובץ ידנית ולספק את הנתיב המקומי.

**URL נפוצים:**
- `patents.google.com` — גוגל פטנטים (HTML)
- `worldwide.espacenet.com` — אספייסנט (HTML)
- `patents.justia.com` — ג'וסטיה (HTML)
- `ncbi.nlm.nih.gov/pmc/` — מאמרי PubMed (HTML)
- `arxiv.org` — ArXiv (HTML ו-PDF)
- `ieeexplore.ieee.org` — IEEE (HTML)

---

## שלב 2: עיבוד ועיכול התוכן

לאחר ההורדה, נתח את הטקסט הגולמי כדי לזהות:

1. **כותרת** (Title)
2. **אבסטרקט** (Abstract) — אם קיים
3. **תאריך פרסום** — חיוני לקביעת רלוונטיות כ-Prior Art
4. **מחברים / ממציאים**
5. **מספר פטנט / DOI / מזהה מסמך**
6. **גוף המסמך** — תוכן מלא עם סימון עמודים/שורות אם זמין

---

## שלב 3: הכנת תוכן הניתוח

הכן את כל תוכן הניתוח בזיכרון לפי המבנה הבא. **אל תכתוב קבצי markdown** — כל התוכן ייכנס לסקריפט Python בשלב 4.

### מבנה הדוח:

```
Section 1 – Title
Section 2 – Abstract
Section 3 – Technical Summary (3-6 paragraphs)
Section 4 – Findings (per finding: title, disclosure, exact quote + location, anticipation analysis, obviousness analysis, classification X/Y/I/A)
Section 5 – Key Technical Features (numbered list, phrased as claim elements)
Section 6 – Limitations and Gaps
Section 7 – Recommended Classification (table + recommendation)
Section 8 – Full Bibliographic Reference (APA or IEEE)
```

### מינוח משפטי עברי — מילון מחייב:

| אנגלית | עברית |
|---|---|
| Prior art | אמנות קודמת |
| Claim | תביעה |
| Claims | תביעות |
| Discloses / teaches | מגלה / מלמד |
| Disclosure | גילוי |
| Anticipation | פסילה / פסילה עצמאית |
| Anticipates | פוסל |
| Obviousness | אי-יצירתיות |
| Obvious | חסר יצירתיות |
| Embodiment | גילום / ביצוע |
| Prior art reference | מסמך קדם / מקור קדם |
| Claim element | פריט תביעה / אלמנט תביעה |
| Claim limitation | הגבלת תביעה |
| Independent claim | תביעה עצמאית |
| Dependent claim | תביעה תלויה |
| Specification | מפרט |
| Abstract | תקציר |
| Inventor | ממציא |
| Applicant | מבקש |
| Filing date | תאריך הגשה |
| Priority date | תאריך עדיפות |
| Publication date | תאריך פרסום |
| Novelty | חידוש / חדשנות |
| Inventive step | צעד המצאתי |
| Reads on | חל על / מכסה |
| Teaching, suggestion, motivation | הוראה, הצעה, מניע |
| Prima facie | לכאורה |
| In combination with | בשילוב עם |
| Technical field | תחום טכני |
| Background art | רקע טכנולוגי |
| Summary of invention | תמצית ההמצאה |
| Detailed description | תיאור מפורט |
| Drawing | איור |
| Figure | איור / צורה |
| Patent application | בקשת פטנט |
| Granted patent | פטנט מוענק |

---

## שלב 4: יצירת קבצי DOCX באמצעות סקריפט Python

לאחר שהכנת את כל תוכן הניתוח, **כתוב סקריפט Python** שיוצר את שני קבצי ה-DOCX ובצע אותו עם `Bash`.

**דרישות:**
- `python-docx` גרסה 1.x מותקנת במערכת
- שמור כ-`source_analyses/gen_docx_temp.py`, הרץ, ואז מחק

### תבנית הסקריפט המלאה — העתק והתאם:

```python
#!/usr/bin/env python3
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_DIR = "source_analyses"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── RTL / formatting helpers ───────────────────────────────

def set_rtl(p):
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    pPr.insert(0, bidi)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def rtl_run(p, text, bold=False, italic=False):
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    rPr = run._r.get_or_add_rPr()
    rPr.append(OxmlElement('w:rtl'))
    return run

def add_heading(doc, text, level, rtl=False):
    p = doc.add_heading(text, level=level)
    if rtl:
        set_rtl(p)
        for run in p.runs:
            run._r.get_or_add_rPr().append(OxmlElement('w:rtl'))
    return p

def meta_row(doc, label, value, rtl=False):
    p = doc.add_paragraph()
    if rtl:
        set_rtl(p)
        rtl_run(p, f"{label}: ", bold=True)
        rtl_run(p, value)
    else:
        p.add_run(f"{label}: ").bold = True
        p.add_run(value)

def blockquote(doc, text, rtl=False):
    p = doc.add_paragraph(style='Normal')
    p.paragraph_format.left_indent = Cm(1.2)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '6')
    left.set(qn('w:space'), '4')
    left.set(qn('w:color'), '999999')
    pBdr.append(left)
    pPr.append(pBdr)
    if rtl:
        set_rtl(p)
        rtl_run(p, text, italic=True)
    else:
        p.add_run(text).italic = True

def cls_table(doc, rows, rtl=False):
    tbl = doc.add_table(rows=1 + len(rows), cols=2)
    tbl.style = 'Table Grid'
    hdr = tbl.rows[0].cells
    if rtl:
        hdr[0].text = "נימוק"; hdr[1].text = "סיווג"
    else:
        hdr[0].text = "Classification"; hdr[1].text = "Rationale"
    for cell in hdr:
        for run in cell.paragraphs[0].runs:
            run.bold = True
        if rtl:
            set_rtl(cell.paragraphs[0])
    for i, (label, rationale) in enumerate(rows):
        row = tbl.rows[i + 1].cells
        if rtl:
            row[0].text = rationale; row[1].text = label
            for cell in row: set_rtl(cell.paragraphs[0])
        else:
            row[0].text = label; row[1].text = rationale

# ── English document builder ──────────────────────────────

def build_en(d):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(3); s.right_margin = Cm(2.5)

    add_heading(doc, "Patent Prior Art Analysis Report", 0)
    doc.add_paragraph()
    for label, key in [
        ("Source URL","url"), ("Document Type","doc_type"),
        ("Publication Number / DOI","pub_number"), ("Publication Date","pub_date"),
        ("Authors / Inventors","authors"), ("Analysis Date","analysis_date"),
    ]:
        meta_row(doc, label, d[key])
    meta_row(doc, "Analyzed By", "Claude (patent-source-analyzer skill)")
    doc.add_paragraph()

    add_heading(doc, "1. Title", 1)
    doc.add_paragraph(d["title"])

    add_heading(doc, "2. Abstract", 1)
    doc.add_paragraph(d["abstract"])

    add_heading(doc, "3. Technical Summary", 1)
    for para in d["technical_summary"]:
        doc.add_paragraph(para)

    add_heading(doc, "4. Prior Art Claim Elements and Findings", 1)
    for f in d["findings"]:
        add_heading(doc, f"Finding {f['number']}: {f['title']}", 2)
        p = doc.add_paragraph()
        p.add_run("Disclosure: ").bold = True
        p.add_run(f["disclosure"])
        doc.add_paragraph().add_run(f"Relevant Text ({f['location']}):").bold = True
        blockquote(doc, f["quote"])
        doc.add_paragraph().add_run("Patent Law Significance:").bold = True
        b = doc.add_paragraph(style='List Bullet')
        b.add_run("Anticipation (35 USC §102 / IL Patents Law §4): ").bold = True
        b.add_run(f["anticipation"])
        b = doc.add_paragraph(style='List Bullet')
        b.add_run("Obviousness (35 USC §103 / IL Patents Law §5): ").bold = True
        b.add_run(f["obviousness"])
        b = doc.add_paragraph(style='List Bullet')
        b.add_run("Classification: ").bold = True
        b.add_run(f["classification"])

    add_heading(doc, "5. Key Technical Features Disclosed", 1)
    for i, feat in enumerate(d["key_features"], 1):
        doc.add_paragraph(f"{i}. {feat}")

    add_heading(doc, "6. Limitations and Gaps", 1)
    for gap in d["gaps"]:
        doc.add_paragraph(gap, style='List Bullet')

    add_heading(doc, "7. Recommended Classification", 1)
    cls_table(doc, d["class_table"])
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Recommended: ").bold = True
    p.add_run(d["recommended"])

    add_heading(doc, "8. Full Bibliographic Reference", 1)
    doc.add_paragraph(d["bibliography"])
    return doc

# ── Hebrew document builder ───────────────────────────────

def build_he(d):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(2.5); s.right_margin = Cm(3)

    add_heading(doc, "דוח ניתוח אמנות קודמת", 0, rtl=True)
    doc.add_paragraph()
    for label, key in [
        ("מקור URL","url"), ("סוג מסמך","doc_type_he"),
        ("מספר פטנט / DOI","pub_number"), ("תאריך פרסום","pub_date"),
        ("מחברים / ממציאים","authors"), ("תאריך ניתוח","analysis_date"),
    ]:
        meta_row(doc, label, d[key], rtl=True)
    meta_row(doc, "נותח על ידי", "Claude (patent-source-analyzer)", rtl=True)
    doc.add_paragraph()

    add_heading(doc, "1. כותרת", 1, rtl=True)
    p = doc.add_paragraph(); set_rtl(p); rtl_run(p, d["title_he"])

    add_heading(doc, "2. תקציר", 1, rtl=True)
    p = doc.add_paragraph(); set_rtl(p); rtl_run(p, d["abstract_he"])

    add_heading(doc, "3. סיכום טכני", 1, rtl=True)
    for para in d["technical_summary_he"]:
        p = doc.add_paragraph(); set_rtl(p); rtl_run(p, para)

    add_heading(doc, "4. פריטי אמנות קודמת וממצאים", 1, rtl=True)
    for f in d["findings_he"]:
        add_heading(doc, f"ממצא {f['number']}: {f['title']}", 2, rtl=True)
        p = doc.add_paragraph(); set_rtl(p)
        rtl_run(p, "גילוי: ", bold=True); rtl_run(p, f["disclosure"])
        p2 = doc.add_paragraph(); set_rtl(p2)
        rtl_run(p2, f"טקסט רלוונטי ({f['location']}):", bold=True)
        blockquote(doc, f["quote"], rtl=True)
        if f.get("quote_translation"):
            ptr = doc.add_paragraph(); set_rtl(ptr)
            rtl_run(ptr, f"(תרגום: {f['quote_translation']})", italic=True)
        p3 = doc.add_paragraph(); set_rtl(p3)
        rtl_run(p3, "משמעות משפטית:", bold=True)
        b = doc.add_paragraph(style='List Bullet'); set_rtl(b)
        rtl_run(b, 'פסילה עצמאית (סעיף 4 לחוק הפטנטים, תשכ"ז-1967): ', bold=True)
        rtl_run(b, f["anticipation"])
        b = doc.add_paragraph(style='List Bullet'); set_rtl(b)
        rtl_run(b, "אי-יצירתיות (סעיף 5 לחוק): ", bold=True)
        rtl_run(b, f["obviousness"])
        b = doc.add_paragraph(style='List Bullet'); set_rtl(b)
        rtl_run(b, "סיווג: ", bold=True); rtl_run(b, f["classification"])

    add_heading(doc, "5. מאפיינים טכניים עיקריים שנחשפו", 1, rtl=True)
    for i, feat in enumerate(d["key_features_he"], 1):
        p = doc.add_paragraph(); set_rtl(p); rtl_run(p, f"{i}. {feat}")

    add_heading(doc, "6. פערים וחסרים במסמך", 1, rtl=True)
    for gap in d["gaps_he"]:
        p = doc.add_paragraph(style='List Bullet'); set_rtl(p); rtl_run(p, gap)

    add_heading(doc, "7. המלצת סיווג", 1, rtl=True)
    cls_table(doc, d["class_table_he"], rtl=True)
    doc.add_paragraph()
    p = doc.add_paragraph(); set_rtl(p)
    rtl_run(p, "המלצה: ", bold=True); rtl_run(p, d["recommended_he"])

    add_heading(doc, "8. ציטוט ביבליוגרפי מלא", 1, rtl=True)
    p = doc.add_paragraph(); set_rtl(p); rtl_run(p, d["bibliography"])
    return doc

# ══════════════════════════════════════════════════════════
# DATA — replace every "REPLACE..." value with real content
# ══════════════════════════════════════════════════════════

SLUG      = "REPLACE-WITH-SLUG"      # e.g. "EP1234567-method-for-X"
TIMESTAMP = "REPLACE-TIMESTAMP"      # e.g. "2026-04-27_14-30"

en = {
    "url":               "REPLACE",
    "doc_type":          "REPLACE",   # e.g. "Scientific Article"
    "pub_number":        "REPLACE",
    "pub_date":          "REPLACE",
    "authors":           "REPLACE",
    "analysis_date":     "REPLACE",
    "title":             "REPLACE",
    "abstract":          "REPLACE",
    "technical_summary": [
        "REPLACE paragraph 1",
        "REPLACE paragraph 2",
    ],
    "findings": [
        {
            "number":        1,
            "title":         "REPLACE Finding Title",
            "disclosure":    "REPLACE disclosure text.",
            "location":      "Section X",
            "quote":         "REPLACE exact quote from source.",
            "anticipation":  "REPLACE 35 USC 102 analysis.",
            "obviousness":   "REPLACE 35 USC 103 analysis.",
            "classification":"X — Anticipates alone",
        },
        # add more findings...
    ],
    "key_features": [
        "REPLACE feature 1",
        "REPLACE feature 2",
    ],
    "gaps": [
        "The reference does not disclose REPLACE.",
        "The reference is silent on REPLACE.",
    ],
    "class_table": [
        ("X (anticipates alone)",        "REPLACE rationale"),
        ("Y (anticipates in combination)","REPLACE rationale"),
        ("I (technological interest)",   "REPLACE rationale"),
        ("A (general background)",       "REPLACE rationale"),
    ],
    "recommended":  "X — REPLACE short explanation",
    "bibliography": "REPLACE full APA/IEEE citation",
}

he = {
    "url":                  en["url"],
    "doc_type_he":          "REPLACE",  # e.g. "מאמר מדעי"
    "pub_number":           en["pub_number"],
    "pub_date":             en["pub_date"],
    "authors":              en["authors"],
    "analysis_date":        en["analysis_date"],
    "title_he":             "REPLACE כותרת (Original Title in parentheses)",
    "abstract_he":          "REPLACE תרגום תקציר.",
    "technical_summary_he": [
        "REPLACE פסקה 1",
        "REPLACE פסקה 2",
    ],
    "findings_he": [
        {
            "number":           1,
            "title":            "REPLACE שם ממצא",
            "disclosure":       "REPLACE גילוי.",
            "location":         "סעיף X",
            "quote":            "REPLACE original English quote.",
            "quote_translation":"REPLACE תרגום לעברית.",
            "anticipation":     "REPLACE ניתוח פסילה עצמאית.",
            "obviousness":      "REPLACE ניתוח אי-יצירתיות.",
            "classification":   "X — פוסל עצמאית",
        },
        # add more findings...
    ],
    "key_features_he": [
        "REPLACE מאפיין 1",
        "REPLACE מאפיין 2",
    ],
    "gaps_he": [
        "המסמך אינו מגלה REPLACE.",
        "המסמך שותק לגבי REPLACE.",
    ],
    "class_table_he": [
        ("X (פוסל עצמאית)",    "REPLACE נימוק"),
        ("Y (פוסל בשילוב)",    "REPLACE נימוק"),
        ("I (עניין טכנולוגי)", "REPLACE נימוק"),
        ("A (רקע כללי)",       "REPLACE נימוק"),
    ],
    "recommended_he": "X — REPLACE הסבר קצר",
    "bibliography":   en["bibliography"],
}

# ── Save ───────────────────────────────────────────────────
en_path = os.path.join(OUTPUT_DIR, f"{TIMESTAMP}_{SLUG}_en.docx")
he_path = os.path.join(OUTPUT_DIR, f"{TIMESTAMP}_{SLUG}_he.docx")

build_en(en).save(en_path)
build_he(he).save(he_path)
print(f"Created: {en_path}")
print(f"Created: {he_path}")
```

**הוראות ביצוע:**

1. **מלא** את כל ערכי `"REPLACE..."` בתוכן האמיתי מהניתוח.
2. **הגדר** `SLUG` (עד 40 תווים, מקפים בלבד) ו-`TIMESTAMP` (פורמט `YYYY-MM-DD_HH-MM`).
3. **שמור** כ-`source_analyses/gen_docx_temp.py`.
4. **הרץ:**
   ```bash
   cd /path/to/project && python3 source_analyses/gen_docx_temp.py
   ```
5. **מחק** את הסקריפט הזמני:
   ```bash
   rm source_analyses/gen_docx_temp.py
   ```

---

## שלב 5: דיווח למשתמש

לאחר יצירת הקבצים, דווח על:
- נתיבי קבצי ה-DOCX שנוצרו
- מספר הממצאים שנמצאו
- המלצת הסיווג (X/Y/I/A)
- תאריך פרסום המקור (חשוב לקביעת אמנות קודמת)

---

## הנחיות כלליות

- **דיוק בציטוטים:** אל תמציא ציטוטים. אם אינך יכול לאתר עמוד/שורה מדויקים, ציין "Section [שם סעיף]" במקום.
- **שפה משפטית:** השתמש תמיד במינוח מהמילון. אל תשתמש בביטויים לא-פורמליים.
- **מסמכי פטנט:** אם ה-URL הוא פטנט — חפש במיוחד את ה-Claims section ונתח כל תביעה בנפרד.
- **מאמרים מדעיים:** חפש Abstract, Results, Discussion, ו-Conclusions.
- **כאשר תוכן מוגבל:** אם WebFetch מחזיר תוכן חלקי (paywall, JavaScript rendering), הודע למשתמש ועבוד עם מה שיש, תוך ציון המגבלה במסמך.
- **שפת המקור:** אם המקור בשפה אחרת מאנגלית (גרמנית, יפנית, כד'), תרגם לאנגלית לצורך הניתוח ואז לעברית.
