---
name: template-generator
description: Generate standardized document templates (DOCUMENT, TECHNICAL, PROPOSAL, RESEARCH, SECURITY-QA, INDEX) with YAML frontmatter, Quick Reference sections, and consistent structure for professional documentation.
---

# Template Generator - Professional Document Architect

> **Purpose**: Generate standardized, professional document templates with YAML frontmatter, Quick Reference sections, and consistent structure for various document types (general, technical, proposal, research, security Q&A).

## When to Use This Skill

Use this skill when the user's request involves:
- **New documentation** - Starting a new document from scratch
- **Standardization** - Ensuring consistent format across team
- **YAML frontmatter** - Need metadata (tags, audience, reading_time)
- **Quick Reference** - Executive summaries, key information tables
- **Professional formatting** - Proposals, technical specs, research reports
- **Template library** - Building reusable document templates

## Core Identity

You are a **document architect** who provides professional, battle-tested templates that ensure consistency, discoverability (via YAML metadata), and readability (via Quick Reference sections) across all documentation.

---

## Available Templates (6 Types)

| Template | Use Case | Key Features | Reading Time |
|----------|----------|--------------|--------------|
| **DOCUMENT** | General purpose docs | Quick Reference, checklist, tags | 5 min |
| **TECHNICAL** | Architecture, implementation | Tech stack, complexity, code samples | 10-30 min |
| **PROPOSAL** | Client proposals, RFPs | Executive summary, ROI, phases | 15-30 min |
| **RESEARCH** | Market research, analysis | Methodology, findings, recommendations | 20-45 min |
| **SECURITY-QA** | Security Q&A, compliance | Question categorization, evidence, priority | 10-20 min |
| **INDEX.md** | Markdown index | Directory structure, document list, stats | 5 min |

---

## Template 1: DOCUMENT (General Purpose)

### When to Use
- General documentation (not technical, not proposal)
- Process guides, how-to docs, meeting notes
- Internal documentation

### Structure

```yaml
---
title: '[Document Title]'
category: '[business|technical|security|research|proposal]'
priority: '[CRITICAL|HIGH|MEDIUM|LOW]'
reading_time: '[number]'
status: '[draft|review|approved|archived]'
tags:
  - tag1
  - tag2
audience:
  - Audience 1
  - Audience 2
related_docs:
  <!-- Template Example: Replace path/to/doc1.md with your actual related documentation paths -->
  - path/to/doc1.md
created: 'YYYY-MM-DD'
version: '1.0'
---
# [Document Title]

## 🎯 Key Summary (30 seconds)

[Summarize core content in 2-3 sentences]

**Purpose**: [Problem this document addresses]

**Key Messages**:
- [Key point 1]
- [Key point 2]
- [Key point 3]

---

## 📊 Quick Reference

| Item | Details |
|------|---------|
| **Category** | [category] |
| **Priority** | [priority] |
| **Reading Time** | [reading_time] min |
| **Audience** | [audience] |
| **Main Tags** | [Top 3 tags] |

---

## [Section 1 Title]

[Content]

---

## [Section 2 Title]

[Content]

---

## ✅ Checklist

- [ ] [Item 1]
- [ ] [Item 2]
- [ ] [Item 3]

---

## References

### Related Documents
<!-- Template Example: Replace [Document Name] and (path) with your actual document references -->
- [Document Name](path)

### External Links
<!-- Template Example: Replace [Link Name] and (URL) with your actual external links -->
- [Link Name](URL)

---

**Created**: YYYY-MM-DD
**Author**: [Name]
**Version**: 1.0
```

---

## Template 2: TECHNICAL (Technical Documentation)

### When to Use
- Architecture documents, system design
- Implementation guides, API specs
- Technical specifications

### Structure

```yaml
---
title: '[Technical Document Title]'
category: technical
priority: '[CRITICAL|HIGH|MEDIUM|LOW]'
reading_time: '[number]'
status: '[draft|review|approved|archived]'
tags:
  - tech1
  - tech2
audience:
  - Developers
  - Architects
  - DevOps
tech_stack:
  - Technology 1
  - Technology 2
complexity: '[low|medium|high|expert]'
implementation_time: '[Estimated implementation time]'
prerequisites:
  - Prerequisite 1
  - Prerequisite 2
related_docs: []
created: 'YYYY-MM-DD'
version: '1.0'
---
# [Technical Document Title]

## 🎯 Key Summary (30 seconds)

[Summarize core technical content in 2-3 sentences]

**Purpose**: [Purpose of this technical document]

**Key Content**:
- [Key point 1]
- [Key point 2]
- [Key point 3]

**Use Cases**: [When to use this technology?]

---

## 📊 Quick Reference

| Item | Details |
|------|---------|
| **Tech Stack** | [tech_stack] |
| **Complexity** | [complexity] |
| **Implementation Time** | [implementation_time] |
| **Prerequisites** | [prerequisites] |
| **Audience** | [audience] |

---

## 🏗️ Architecture

### System Structure

```
[Architecture diagram or text description]
```

### Key Components

- **[Component 1]**: [Description]
- **[Component 2]**: [Description]
- **[Component 3]**: [Description]

---

## ⚙️ Technical Specifications

| Item | Specification |
|------|---------------|
| **Language/Framework** | [Details] |
| **Database** | [Details] |
| **Performance Goals** | [Details] |
| **Requirements** | [Details] |

---

## 🛠️ Implementation Guide

### Environment Setup

\`\`\`bash
# Install dependencies
[Setup commands]

# Environment variables
[Environment variable configuration]
\`\`\`

### Code Examples

\`\`\`python
# Example code
[Code]
\`\`\`

---

## ✅ Checklist

- [ ] Environment setup complete
- [ ] Dependencies installed
- [ ] Tests passed
- [ ] Documentation updated

---

## References

### Internal Documents
<!-- Template Example: Replace [Related Technical Doc] and (path) with your actual technical document references -->
- [Related Technical Doc](path)

### External References
<!-- Template Example: Replace [Official Docs], [Example Code] and (URL) with your actual external references -->
- [Official Docs](URL)
- [Example Code](URL)

---

**Created**: YYYY-MM-DD
**Author**: [Name]
**Version**: 1.0
**Complexity**: [complexity]
```

---

## Template 3: PROPOSAL (Proposal/RFP)

### When to Use
- Client proposals, RFPs
- Project proposals, investment pitches
- Executive presentations

### Structure

```yaml
---
title: '[Proposal Title]'
category: proposal
priority: '[CRITICAL|HIGH|MEDIUM|LOW]'
reading_time: '[number]'
status: '[draft|submitted|approved|rejected]'
tags:
  - proposal
  - client
  - project
audience:
  - Client
  - Executive Team
client: '[Client Name]'
project_name: '[Project Name]'
estimated_cost: '[Total Budget]'
estimated_duration: '[Estimated Duration]'
proposal_date: 'YYYY-MM-DD'
valid_until: 'YYYY-MM-DD'
phases: []
related_docs: []
created: 'YYYY-MM-DD'
version: '1.0'
---
# [Proposal Title]

## 🎯 Executive Summary (30 seconds)

[Summarize proposal core content in 2-3 sentences]

**Purpose**: [Purpose of this proposal]

**Key Value**:
- [Value proposition 1]
- [Value proposition 2]
- [Value proposition 3]

**Expected ROI**: [ROI figure or description]

---

## 📊 Quick Reference

| Item | Details |
|------|---------|
| **Client** | [client] |
| **Project Name** | [project_name] |
| **Total Budget** | [estimated_cost] |
| **Estimated Duration** | [estimated_duration] |
| **Proposal Valid Until** | [valid_until] |
| **Number of Phases** | [number] |

---

## 💼 Client Pain Points

### Current Problems

1. **[Problem 1]**
   - Situation: [Specific description]
   - Impact: [Business impact]

2. **[Problem 2]**
   - Situation: [Specific description]
   - Impact: [Business impact]

### Business Impact Analysis

| Problem Area | Annual Loss | Priority |
|--------------|-------------|----------|
| [Area 1] | [Amount] | HIGH |
| [Area 2] | [Amount] | MEDIUM |

---

## ✨ Proposed Solution

### Solution Overview

[Overall solution overview in 3-5 sentences]

### Key Features

1. **[Feature 1]**
   - Description: [Detailed description]
   - Effect: [Expected effect]

2. **[Feature 2]**
   - Description: [Detailed description]
   - Effect: [Expected effect]

---

## 📈 ROI Analysis

### Cost Structure

| Phase | Budget | Duration | Key Deliverables |
|-------|--------|----------|------------------|
| Phase 0 | [Amount] | [Duration] | [Deliverables] |
| Phase 1 | [Amount] | [Duration] | [Deliverables] |

### Expected Benefits

| Metric | Current | After Improvement | Improvement Rate |
|--------|---------|-------------------|------------------|
| [Metric 1] | [Current value] | [Improved value] | [%] |
| [Metric 2] | [Current value] | [Improved value] | [%] |

### ROI Calculation

- **Total Investment**: [Amount]
- **Annual Savings**: [Amount]
- **ROI**: [%]
- **Payback Period**: [Months]

---

## 🗓️ Schedule and Milestones

| Phase | Duration | Key Milestones |
|-------|----------|----------------|
| Phase 0 | [Duration] | [Milestone] |
| Phase 1 | [Duration] | [Milestone] |

---

## 📋 Next Steps

1. **[Step 1]**: [Description] (Deadline: [Date])
2. **[Step 2]**: [Description] (Deadline: [Date])
3. **[Step 3]**: [Description] (Deadline: [Date])

---

## Appendix

### Our Team Introduction
[Team introduction]

### Similar Project Case Studies
[1-3 case studies]

---

**Proposal Date**: [proposal_date]
**Valid Until**: [valid_until]
**Contact**: [Name/Contact]
```

---

## Template 4: RESEARCH (Research/Analysis)

### When to Use
- Market research, competitive analysis
- User research, data analysis
- Literature reviews, case studies

### Structure

```yaml
---
title: '[리서치 제목]'
category: research
priority: '[CRITICAL|HIGH|MEDIUM|LOW]'
reading_time: '[숫자]'
status: '[draft|review|approved]'
tags:
  - research
  - analysis
  - data
audience:
  - 경영진
  - 제품팀
research_type: '[market|competitive|user|technical]'
methodology:
  - 방법론1
  - 방법론2
data_sources:
  - 출처1
  - 출처2
research_period: '[시작일 ~ 종료일]'
related_docs: []
created: 'YYYY-MM-DD'
version: '1.0'
---
# [리서치 제목]

## 🎯 핵심 요약 (60초)

[리서치 핵심 내용을 3-5문장으로 요약]

**리서치 목적**: [목적]

**주요 발견**:
- [발견 1]
- [발견 2]
- [발견 3]

**권장 사항**: [핵심 권장 사항]

---

## 📊 Quick Reference

| 항목 | 내용 |
|------|------|
| **리서치 유형** | [research_type] |
| **방법론** | [methodology] |
| **조사 기간** | [research_period] |
| **데이터 출처** | [주요 출처 3개] |
| **신뢰도** | [HIGH|MEDIUM|LOW] |

---

## 🔍 리서치 방법론

### 조사 방법

1. **[방법 1]**
   - 설명: [상세 설명]
   - 샘플 크기: [N]

2. **[방법 2]**
   - 설명: [상세 설명]
   - 샘플 크기: [N]

### 데이터 출처

<!-- Template Example: Replace [출처1], [출처2], [유형], and [링크] with your actual research sources and URLs -->
| 출처 | 유형 | 신뢰도 | URL/레퍼런스 |
|------|------|--------|------------|
| [출처1] | [유형] | HIGH | [링크] |
| [출처2] | [유형] | MEDIUM | [링크] |

---

## 📈 주요 발견 (Key Findings)

### 발견 1: [제목]

**데이터**:
- [통계/수치]
- [증거]

**분석**:
[해석 및 의미]

**영향**:
[비즈니스 영향]

---

### 발견 2: [제목]

[위와 동일 구조]

---

## 💡 인사이트 (Insights)

### 패턴 및 트렌드

- **패턴 1**: [설명]
- **패턴 2**: [설명]
- **패턴 3**: [설명]

### 시사점

| 인사이트 | 실행 가능성 | 우선순위 |
|---------|------------|----------|
| [인사이트1] | HIGH | CRITICAL |
| [인사이트2] | MEDIUM | HIGH |

---

## 🎯 권장 사항 (Recommendations)

### 즉시 실행 (High Priority)

1. **[권장사항 1]**
   - 근거: [발견/데이터]
   - 기대 효과: [효과]
   - 예상 비용: [비용]
   - 실행 기간: [기간]

### 중기 실행 (Medium Priority)

1. **[권장사항 2]**
   - [위와 동일 구조]

---

## 📊 데이터 및 차트

[차트, 그래프, 표 등]

---

## ⚠️ 제약사항 (Limitations)

- **제약 1**: [설명]
- **제약 2**: [설명]

**향후 리서치**: [추가 조사가 필요한 영역]

---

## 참고 자료

### 1차 자료 (Primary Sources)
<!-- Template Example: Replace [출처1], [출처2] and (URL) with your actual primary source references -->
- [출처1](URL)
- [출처2](URL)

### 2차 자료 (Secondary Sources)
<!-- Template Example: Replace [출처1], [출처2] and (URL) with your actual secondary source references -->
- [출처1](URL)
- [출처2](URL)

---

**리서치 기간**: [research_period]
**작성자**: [이름/팀]
**리뷰어**: [리뷰어 이름]
```

---

## Template 5: SECURITY-QA (Security Q&A)

### When to Use
- Security compliance documentation
- FAQ for security reviews
- Regulatory Q&A (ISMS-P, SOC 2, ISO 27001)

### Structure

```yaml
---
title: '[보안 Q&A 제목]'
category: security
priority: CRITICAL
reading_time: '[숫자]'
status: '[draft|review|approved]'
tags:
  - security
  - compliance
  - qa
audience:
  - 보안팀
  - CISO
  - 감사팀
compliance_frameworks:
  - ISMS-P
  - SOC 2
  - ISO 27001
total_questions: '[숫자]'
review_date: 'YYYY-MM-DD'
related_docs: []
created: 'YYYY-MM-DD'
version: '1.0'
---
# [보안 Q&A 제목]

## 🎯 핵심 요약 (30초)

[보안 Q&A 개요를 2-3문장으로]

**목적**: [이 Q&A의 목적]

**적용 프레임워크**:
- [프레임워크 1]
- [프레임워크 2]

**총 질문 수**: [total_questions]개

---

## 📊 Quick Reference

| 항목 | 내용 |
|------|------|
| **프레임워크** | [compliance_frameworks] |
| **총 질문** | [total_questions]개 |
| **최종 검토일** | [review_date] |
| **대상 독자** | [audience] |

---

## 📋 질문 카테고리

| 카테고리 | 질문 수 | 우선순위 |
|---------|--------|---------|
| 물리적 보안 | [N]개 | CRITICAL |
| 네트워크 보안 | [N]개 | HIGH |
| 데이터 보안 | [N]개 | CRITICAL |
| 접근 제어 | [N]개 | HIGH |
| 감사 & 모니터링 | [N]개 | MEDIUM |

---

## 1️⃣ 물리적 보안 (Physical Security)

### Q1. [질문]

**우려 사항**: [보안팀의 우려]

**답변**:
[상세 답변]

**증거/증명 자료**:
- [증거 1] (문서/링크)
- [증거 2] (문서/링크)

**관련 규정**:
- ISMS-P: [조항 번호]
- SOC 2: [관련 통제]

**우선순위**: ⭐⭐⭐⭐⭐ (CRITICAL)

---

### Q2. [질문]

[위와 동일 구조]

---

## 2️⃣ 네트워크 보안 (Network Security)

### Q3. [질문]

[위와 동일 구조]

---

## 3️⃣ 데이터 보안 (Data Security)

### Q4. [질문]

[위와 동일 구조]

---

## 🔗 관련 문서

### 내부 정책 문서
<!-- Template Example: Replace [정책 문서 1], [정책 문서 2] and (경로) with your actual internal policy document references -->
- [정책 문서 1](경로)
- [정책 문서 2](경로)

### 외부 인증/감사
<!-- Template Example: Replace [인증서 1], [감사 보고서] and (경로/URL) with your actual certification and audit references -->
- [인증서 1](경로/URL)
- [감사 보고서](경로/URL)

---

## 📝 검토 이력

| 날짜 | 검토자 | 변경 사항 |
|------|--------|---------|
| [날짜] | [이름] | [변경 내용] |

---

**작성일**: [created]
**최종 검토**: [review_date]
**담당자**: [이름/부서]
**승인자**: [CISO 이름]
```

---

## Template 6: INDEX.md (Markdown Index)

### When to Use
- README files for directories
- Human-readable documentation indexes
- Navigation hubs

### Structure

```markdown
# [Directory Name] Documentation Index

[1-2문장 설명]

---

## 📁 Directory Structure

\`\`\`
directory/
├── README.md
├── subdirectory1/
│   ├── README.md
│   └── doc1.md
├── subdirectory2/
│   ├── README.md
│   └── doc2.md
└── doc3.md
\`\`\`

---

## 📋 Document List

<!-- Template Example: Replace [file1.md], [file2.md], and ./file paths with your actual documentation files -->
| 파일 | 주제 | 주요 내용 | 읽기 시간 |
|-----|------|----------|----------|
| [file1.md](./file1.md) | 제목 | • 내용 1<br>• 내용 2 | 10분 |
| [file2.md](./file2.md) | 제목 | • 내용 1<br>• 내용 2 | 15분 |

**총 N개 문서**

---

## 🎯 역할별 추천

### 개발자
- [문서1](./path/doc1.md) - 기술 가이드
- [문서2](./path/doc2.md) - API 레퍼런스

### 경영진
- [문서3](./path/doc3.md) - Executive Summary
- [문서4](./path/doc4.md) - ROI 분석

### 보안팀
- [문서5](./path/doc5.md) - 보안 아키텍처
- [문서6](./path/doc6.md) - 규정 준수

---

## 📚 관련 문서

- **상위 INDEX**: [../README.md](../README.md)
- **기술 문서**: [../technical/README.md](../technical/README.md)
- **제안 문서**: [../proposals/README.md](../proposals/README.md)

---

## 📊 통계

- **총 문서 수**: N개
- **총 읽기 시간**: N분
- **최근 업데이트**: YYYY-MM-DD

---

**작성일**: YYYY-MM-DD
**버전**: 1.0
**관리자**: [이름]
```

---

## YAML Frontmatter Best Practices

### Required Fields (All Templates)

```yaml
title: 'Document Title'
category: '[business|technical|security|research|proposal]'
priority: '[CRITICAL|HIGH|MEDIUM|LOW]'
reading_time: '[숫자]'
status: '[draft|review|approved|archived]'
tags:
  - tag1
  - tag2
  - tag3
created: 'YYYY-MM-DD'
version: '1.0'
```

---

### Optional Fields (Template-Specific)

**Technical**:
```yaml
tech_stack: [list]
complexity: '[low|medium|high|expert]'
prerequisites: [list]
```

**Proposal**:
```yaml
client: 'Client Name'
estimated_cost: 'Amount'
estimated_duration: 'Period'
phases: [list]
```

**Research**:
```yaml
research_type: 'Type'
methodology: [list]
data_sources: [list]
```

**Security**:
```yaml
compliance_frameworks: [list]
total_questions: [number]
review_date: 'YYYY-MM-DD'
```

---

## Quick Reference Section Standards

### Purpose
- Provide at-a-glance information
- Enable quick decision-making
- Improve discoverability

### Structure

```markdown
## 📊 Quick Reference

| 항목 | 내용 |
|------|------|
| **Key Field 1** | Value |
| **Key Field 2** | Value |
| **Key Field 3** | Value |
```

### What to Include

- **Category/Type**
- **Priority/Urgency**
- **Reading Time**
- **Target Audience**
- **Key Metrics** (cost, duration, complexity)

---

## Workflow: Creating a New Document

### Step 1: Select Template

**Question**: "What type of document are you creating?"

| Answer | Template |
|--------|----------|
| General doc | DOCUMENT |
| Technical spec | TECHNICAL |
| Client proposal | PROPOSAL |
| Research report | RESEARCH |
| Security Q&A | SECURITY-QA |
| Directory index | INDEX.md |

---

### Step 2: Fill YAML Frontmatter

**Required fields**:
- title, category, priority, reading_time, status, tags, created, version

**Ask user**:
- "What's the document title?"
- "Who is the audience?"
- "What's the priority?" (CRITICAL/HIGH/MEDIUM/LOW)
- "Estimated reading time?" (in minutes)

---

### Step 3: Generate Quick Reference

**Extract from YAML**:
- Category
- Priority
- Reading time
- Audience
- Tags (top 3)

**Template-specific additions**:
- TECHNICAL: tech_stack, complexity, prerequisites
- PROPOSAL: client, cost, duration
- RESEARCH: methodology, data sources
- SECURITY-QA: frameworks, total questions

---

### Step 4: Structure Content Sections

**Use template structure**:
- DOCUMENT: General sections + checklist
- TECHNICAL: Architecture + specs + implementation
- PROPOSAL: Pain points + solution + ROI + timeline
- RESEARCH: Methodology + findings + recommendations
- SECURITY-QA: Category-based Q&A

---

### Step 5: Add References

**Always include**:
- Related docs (internal)
- External links (if applicable)
- Author/date/version

---

## Example: Generate TECHNICAL Doc

**User Request**: "Create a technical doc for Zero Trust Architecture"

**Step 1: Select Template**
→ TECHNICAL

**Step 2: Fill YAML**
```yaml
---
title: 'Zero Trust Architecture Design'
category: technical
priority: CRITICAL
reading_time: 25
status: draft
tags:
  - security
  - architecture
  - zero-trust
audience:
  - 개발자
  - 보안팀
  - 아키텍트
tech_stack:
  - AWS
  - Nitro Enclave
  - CloudWatch
complexity: high
implementation_time: '3 months'
prerequisites:
  - AWS 기본 지식
  - 보안 아키텍처 이해
created: '2025-10-27'
version: '1.0'
---
```

**Step 3: Quick Reference**
```markdown
## 📊 Quick Reference

| 항목 | 내용 |
|------|------|
| **기술 스택** | AWS, Nitro Enclave, CloudWatch |
| **복잡도** | High |
| **구현 시간** | 3 months |
| **선행 지식** | AWS 기본, 보안 아키텍처 |
| **대상 독자** | 개발자, 보안팀, 아키텍트 |
```

**Step 4: Structure**
- 🏗️ 아키텍처
- ⚙️ 기술 스펙
- 🛠️ 구현 가이드
- ✅ 체크리스트

**Step 5: References**
- Related: `docs/security-guidelines.md`
- External: Official security standards documentation

---

## Quality Checklist

### YAML Frontmatter

- [ ] All required fields present
- [ ] Tags relevant (3-5 tags)
- [ ] Reading time accurate
- [ ] Audience specified
- [ ] Created date = today

### Quick Reference

- [ ] Key information at-a-glance
- [ ] Table format (항목 | 내용)
- [ ] 5-7 rows max
- [ ] Matches YAML data

### Content Structure

- [ ] Sections logically organized
- [ ] Headers use emoji (🎯, 📊, 🏗️)
- [ ] Bullet points for lists
- [ ] Code blocks for technical content
- [ ] Tables for comparisons

### References

- [ ] Related docs linked
- [ ] External sources cited
- [ ] Author/date/version at end

---

## Common Mistakes to Avoid

### ❌ Missing YAML Frontmatter
**Wrong**:
```markdown
# My Document

Content here...
```

**Right**:
```markdown
---
title: 'My Document'
category: technical
...
---
# My Document

Content here...
```

---

### ❌ No Quick Reference
**Wrong**:
```markdown
---
...
---
# Document

## Section 1
Content...
```

**Right**:
```markdown
---
...
---
# Document

## 🎯 핵심 요약 (30초)
...

## 📊 Quick Reference
...

## Section 1
Content...
```

---

### ❌ Inconsistent Structure
**Wrong**: Each document has different section order

**Right**: Follow template structure consistently

---

## References

### External Standards
- [YAML Frontmatter](https://jekyllrb.com/docs/front-matter/) - YAML standard
- [GitHub Flavored Markdown](https://github.github.com/gfm/) - Markdown spec

---

For detailed usage and examples, see related documentation files.