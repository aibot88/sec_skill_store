---
name: rag-ai-app-security-audit
description: Use this skill to audit RAG and AI application security, including retrieval boundaries, prompt injection, citations, memory, and data exposure. Do not use it as a scanner or exploit runner.
---

# rag-ai-app-security-audit

## English

### Purpose

Audit RAG and AI application security in audit-only mode.

Use this skill when a review involves retrieval pipelines, document ingestion, embeddings, vector
stores, citations, prompt construction, tool use, memory, tenant filters, or user-visible AI output.

### Workflow

1. Identify trusted and untrusted document sources.
2. Map retrieval filters, metadata boundaries, and tenant scopes.
3. Check whether retrieved text is treated as data rather than instruction.
4. Review citation requirements and output handling.
5. Check memory writes, retention, redaction, and cross-session reuse.
6. Report only evidence-backed findings and regression-test ideas.

### Safety rules

Default to audit-only. Do not execute exploits, do not scan unrelated repositories, do not upload
private source code or secrets, and Do not auto-merge. Ask for human approval before any patch that
changes retrieval policy, tool permissions, memory, privacy, or authorization behavior.

## 中文

### 目的

以 audit-only 模式审计 RAG 和 AI application security。

当 review 涉及 retrieval pipelines、document ingestion、embeddings、vector stores、citations、prompt
construction、tool use、memory、tenant filters 或用户可见 AI output 时，使用这个 skill。

### Workflow

1. 识别 trusted 和 untrusted document sources。
2. 映射 retrieval filters、metadata boundaries 和 tenant scopes。
3. 检查 retrieved text 是否被当作 data，而不是 instruction。
4. 审查 citation requirements 和 output handling。
5. 检查 memory writes、retention、redaction 和 cross-session reuse。
6. 只报告 evidence-backed findings 和 regression-test ideas。

### Safety rules

默认 audit-only。不要执行 exploits，不要扫描无关仓库，不要上传私有源码或 secrets。Do not auto-merge。任何修改 retrieval
policy、tool permissions、memory、privacy 或 authorization behavior 的 patch，都需要 human approval。
