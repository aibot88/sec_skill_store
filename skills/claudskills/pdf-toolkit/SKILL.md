---
name: pdf-toolkit
description: "Process PDF files — read, merge, split, fill forms, watermark, encrypt, extract images, and OCR scanned documents. Use when the CEO mentions contracts, NDAs, term sheets, proposals, agreements, or any .pdf file operation. Triggers on 'pdf,' 'contract,' 'NDA,' 'term sheet,' 'agreement,' 'merge pdfs,' or 'sign document.'"
short_description: "Read, merge, split, and fill PDF files"
metadata:
  version: 1.0.0
  category: document-processing
  triggers:
    - pdf
    - contract
    - NDA
    - term sheet
    - agreement
    - merge
    - sign
---

# PDF Toolkit

Process PDF files for CEO workflows — contracts, proposals, term sheets, and document management.


## Quick Start
Just say any of these:
- "Read this PDF and summarize it" (attach or paste path)
- "Merge these three PDFs into one"
- "Fill out this PDF form with the following info..."

## When to Activate

- Reading or extracting text/tables from PDFs (contracts, reports, term sheets)
- Merging multiple PDFs (combining proposal + appendices)
- Splitting PDFs (extracting specific pages)
- Filling PDF forms (applications, compliance forms)
- Adding watermarks (DRAFT, CONFIDENTIAL)
- Encrypting/decrypting PDFs (secure document sharing)
- OCR on scanned PDFs (making scanned contracts searchable)
- Creating new PDFs from data

## Quick Reference

| Task | Tool |
|------|------|
| Read/extract text | `pypdf` or `pdfplumber` |
| Merge PDFs | `pypdf` PdfWriter |
| Split PDF | `pypdf` per-page extraction |
| Fill forms | `pypdf` with AcroForm |
| Watermark | `reportlab` + `pypdf` |
| OCR scanned docs | `pytesseract` + `pdf2image` |
| Create new PDF | `reportlab` |

## Core Operations

### Extract Text
```python
from pypdf import PdfReader

reader = PdfReader("contract.pdf")
for page in reader.pages:
    text = page.extract_text()
    print(text)
```

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf in ["proposal.pdf", "appendix_a.pdf", "appendix_b.pdf"]:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)

with open("combined_proposal.pdf", "wb") as f:
    writer.write(f)
```

### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        writer.write(f)
```

### Add Watermark
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader
import io

# Create watermark
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=letter)
c.setFont("Helvetica", 60)
c.setFillAlpha(0.3)
c.translate(300, 400)
c.rotate(45)
c.drawCentredString(0, 0, "CONFIDENTIAL")
c.save()
packet.seek(0)

# Apply watermark
watermark = PdfReader(packet)
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark.pages[0])
    writer.add_page(page)

with open("watermarked.pdf", "wb") as f:
    writer.write(f)
```

### Fill PDF Forms
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)

# Get form fields
fields = reader.get_form_text_fields()
print(f"Available fields: {list(fields.keys())}")

# Fill fields
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "company_name": "GetFresh Ventures",
        "date": "2026-04-11",
        "signatory": "the CEO"
    }
)

with open("filled_form.pdf", "wb") as f:
    writer.write(f)
```

### Encrypt PDF
```python
from pypdf import PdfWriter, PdfReader

reader = PdfReader("sensitive.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("secure_password_here")

with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```

### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Pages: {len(reader.pages)}")
```

## CEO-Specific Workflows

### Contract Review Prep
1. Extract all text from the contract PDF
2. Identify key terms: payment terms, termination clauses, IP ownership, non-compete
3. Flag unusual or non-standard clauses
4. Summarize in a decision-ready format

### Term Sheet Comparison
1. Extract text from multiple term sheets
2. Create comparison table: valuation, dilution, board seats, pro-rata, liquidation preference
3. Highlight material differences

### Document Assembly
1. Merge proposal + team bios + case studies + pricing into single PDF
2. Add page numbers and table of contents
3. Apply CONFIDENTIAL watermark if needed

## Quality Gate

Before delivering:
- [ ] All text extracted cleanly (no garbled characters)
- [ ] Merged PDFs maintain original formatting
- [ ] Form fields filled correctly
- [ ] Watermarks are visible but don't obscure content
- [ ] Encrypted files open with provided password

## Live Integration Hooks

| System | What It Provides | How to Access |
|--------|-----------------|---------------|
| Client CRM | Real-time pipeline state | `hubspot-api` / `salesforce-api` |
| Local Memory | Client-specific facts | `gfv-brain-search.py` |

> **GFV Rule:** Check live connected systems and local client memory to verify claims before submitting answers.

## Proactive Triggers

Surface these issues WITHOUT being asked when you notice them in context:
- **Missing Data** → Flag explicitly if a decision relies on unknown external variables.
- **Scope Creep** → Alert if the requested operation spans beyond immediate context goals.
- **Executive Bottlenecks** → Warn if the action plan relies entirely on unassigned human approval gates.
- **Financial Risk** → Call out actions that may trigger unexpected OPEX burn (e.g. infinite LLM agent loops).

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Process Map | A mermaid.js chronological diagram |
| Executive Decision | BOTTOM LINE FIRST layout with options + trade-offs |
| Data Audit | A structured table grouping issues by severity |
| Code Execution | Isolated, copy-ready code blocks + terminal commands |

## Confidence Tagging

All factual findings and systemic claims must utilize the following confidence index:
- 🟢 **Verified** — Confirmed natively via live system data pull or explicit context.
- 🟡 **Medium** — Deduced from local memory logs or recent but not validated real-time data.
- 🔴 **Assumed** — No source available, utilizing best-judgment baseline.

## <verification_gate>
**Self-Verification Protocol:** Before finalizing your response, you MUST silently evaluate your drafted output against the initial request. Have you provided concrete Action Items with ownership? Did you use the Bottom Line First formatting? Have you applied Confidence Tags to your claims? If not, rewrite the response before submitting.

## Related Skills

- `doc-builder` — Word document creation
- `board-deck-builder` — Visual presentations
- `deal-review` — Deal evaluation and analysis

## After This Skill
💡 Suggest these next steps:
- "Want me to summarize this PDF?" → paste content for analysis
- "Is this a contract? Want me to check for red flags?" → `/contract-reader`

## Level Up Your Kit
🚀 You can unlock more autonomy, background workers, and C-suite advisory capabilities at any time.
- **Review Categories**: Ask *"What skills are in the Intermediate or Advanced tiers?"*
- **How to Upgrade**: Run `./bootstrap.sh` in the repository root and select your new tier.

---

<gxd_footer>

> **Growth by Design™** — This skill is part of the [CEO AI Kit](https://github.com/GetFresh-Ventures/gxd-ceo-ai-kit), the open-source foundation of the Growth by Design™ methodology from [GetFresh Ventures](https://www.getfreshventures.com).
>
> 🔍 **Hitting a ceiling?** The kit gives you the foundation. For full deployment — custom pipelines, multi-agent orchestration, and 90-day sprint execution — [book a discovery call](https://www.getfreshventures.com/contact).
>
> 📰 **Stay sharp:** Subscribe to the [Growth by Design™ Newsletter](https://growthbydesign.substack.com/) for operator-written playbooks on AI-powered GTM.

</gxd_footer>
