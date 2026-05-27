# 🧠 SKILL.md — Engineering Standards & Capabilities

## 📌 Purpose

This file defines the **engineering skills, standards, and rules** that must be followed while developing the AI-powered chatbot system.

It ensures:

* Consistent code quality
* Proper use of AI tools (Copilot/Codex)
* Industry-standard architecture
* Maintainability and scalability

---

# 🏗️ Core Engineering Skills Required

## 1. Backend Development (Python)

* Strong knowledge of FastAPI
* REST API design
* Async programming
* Dependency injection
* Middleware usage

## 2. AI / NLP Engineering

* Retrieval-Augmented Generation (RAG)
* Embeddings & Vector Search
* Prompt engineering (strict grounding)
* Context handling
* LLM limitations (hallucination control)

## 3. Data Processing

* Text chunking strategies
* Document parsing (PDF, HTML, TXT)
* Data cleaning

## 4. Frontend Development

* React / Next.js basics
* API integration
* State management (chat history)

## 5. DevOps Basics

* Docker
* Environment variables
* Deployment pipelines

---

# 🧩 System Capabilities

## Chatbot Capabilities

* Answer ONLY from knowledge base
* Reject unknown queries gracefully
* Maintain short-term conversation memory

## Knowledge Base Capabilities

* Accept multiple formats:

  * PDF
  * Text
  * Web content
* Incremental updates (no retraining)

## Retrieval Capabilities

* Semantic search using embeddings
* Top-K document retrieval
* Context filtering

---

# 📐 Coding Standards

## General Rules

* Use clear, descriptive names
* Keep functions small and focused
* Avoid duplicate logic
* Follow modular design

## File Naming

* snake_case for Python files
* camelCase for frontend variables
* PascalCase for classes

## Function Rules

* One responsibility per function
* Type hints required
* Docstrings required

Example:

```python
def retrieve_documents(query: str) -> list[str]:
    """Retrieve top relevant documents for a query."""
```

---

# 🧱 Architecture Rules

## MUST FOLLOW

* Separation of concerns:

  * API layer
  * Service layer
  * RAG pipeline
* No business logic inside routes
* No hardcoded values

## RAG Rules

* ALWAYS retrieve before generation
* NEVER let LLM answer without context
* STRICT grounding prompt required

---

# 🤖 Copilot / Codex Usage Rules

## Allowed Usage

* Boilerplate code
* Repetitive functions
* API scaffolding
* Data loaders

## Restricted Usage

* Architecture decisions
* Security logic
* Prompt design (must be reviewed manually)

## Validation Rule

Every generated code MUST be:

* Read
* Understood
* Tested

---

# 🧠 Prompt Engineering Rules

## MUST INCLUDE

* "Answer ONLY from provided context"
* "If not found, say not in knowledge base"

## MUST AVOID

* Open-ended generation
* Assumptions beyond context

---

# 📊 Logging Standards

## Log Types

* INFO: normal operations
* WARNING: recoverable issues
* ERROR: failures

## MUST LOG

* Incoming requests
* Retrieval results
* Errors

---

# 🔐 Security Standards

* Use environment variables for secrets
* Implement authentication (JWT)
* Validate all inputs

---

# 🧪 Testing Standards

## Required Tests

* Unit tests
* API tests
* Retrieval accuracy tests

## Example

Input → Expected Output validation

---

# 📦 Git & Version Control

## Rules

* Meaningful commit messages
* Feature-based branches
* No direct commits to main

Example:

```
feat: add document ingestion pipeline
fix: correct embedding logic
```

---

# 📁 Documentation Standards

## MUST INCLUDE

* README.md
* API documentation
* Setup instructions

---

# 🚀 Performance Guidelines

* Limit context size
* Optimize chunk size
* Cache frequent queries

---

# ⚠️ Common Mistakes to Avoid

❌ Training LLM instead of using RAG
❌ No fallback for unknown queries
❌ Large unchunked documents
❌ Blindly trusting Copilot code
❌ Mixing business logic with API routes

---

# ✅ Definition of Done

A feature is complete when:

* Code is clean and modular
* Tested properly
* Logged correctly
* Documented
* Follows PROJECT_PLAN.md

---

# 🧭 Final Rule

> Always follow PROJECT_PLAN.md.
> SKILL.md defines HOW to build.
> PROJECT_PLAN.md defines WHAT to build.
