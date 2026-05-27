---
name: ai4scholar-mcp
description: All-in-one academic research với 28 tools. Kết nối arXiv, PubMed, Semantic Scholar, bioRxiv, medRxiv, Google Scholar. Hỗ trợ auto-cite và AI scientific figure generation.
version: 1.0.0
author: Hermes Agent Community
metadata:
  hermes:
    requires:
      env:
        - AI4SCHOLAR_API_KEY
      bins:
        - python
    primaryEnv: AI4SCHOLAR_API_KEY
    emoji: "🎓"
    homepage: https://pypi.org/project/ai4scholar-mcp/
---

# ai4scholar MCP Skill — All-in-One Academic Research

Skill này cho phép Hermes Agent tìm kiếm, download và phân tích academic papers từ 6 nguồn cùng lúc.

## Khi Nào Sử Dụng

Sử dụng skill này khi người dùng:
- Tìm kiếm papers trên nhiều databases cùng lúc
- Cần tìm papers của một tác giả cụ thể
- Muốn download PDF và đọc nội dung
- Cần auto-cite cho bài viết
- Muốn tạo scientific figures bằng AI

## 28 Tools Theo Platform

| Platform | Tools |
|----------|-------|
| arXiv | search_arxiv, download_arxiv, read_arxiv_paper |
| PubMed | search_pubmed, get_pubmed_paper_detail, get_pubmed_citations, get_pubmed_related |
| Semantic Scholar | search_semantic, download_semantic, read_semantic_paper, get_semantic_citations, get_semantic_references, search_semantic_authors, get_semantic_author_papers, get_semantic_recommendations, search_semantic_snippets |
| Google Scholar | search_google_scholar |
| bioRxiv | search_biorxiv, download_biorxiv, read_biorxiv_paper |
| medRxiv | search_medrxiv, download_medrxiv, read_medrxiv_paper |
| General | download_pdf_by_doi |
| Auto-Cite | auto_cite |
| Nano Draw | nano_generate, nano_edit |

## Ví Dụ Sử Dụng

**Tìm papers của tác giả:**
"Tìm tất cả papers của tác giả Luong Pham Hanh Nguyen"
→ Dùng search_semantic_authors, get_semantic_author_papers

**Tìm papers theo topic:**
"Tìm papers về RAG trên tất cả databases"
→ Dùng search_arxiv + search_pubmed + search_semantic + search_biorxiv

**Download và đọc paper:**
"Download paper 2401.12345 và tóm tắt"
→ Dùng download_arxiv → read_arxiv_paper

## Cài Đặt

```bash
pip install ai4scholar-mcp
```

## Cấu Hình Hermes Agent

```json
{
  "mcpServers": {
    "ai4scholar": {
      "command": "python",
      "args": ["-m", "ai4scholar_mcp.server"],
      "env": {
        "AI4SCHOLAR_API_KEY": "<your-ai4scholar-api-key>"
      }
    }
  }
}
```

> **Lưu ý:** Nếu muốn dùng SSE remote thay vì local Python, thay bằng:
> ```json
> "url": "https://mcp.ai4scholar.net/sse",
> "headers": { "Authorization": "Bearer <key>" }
> ```
> Tuy nhiên mcp.json hiện tại đang dùng local Python.

