---
name: project-readme-generator
description: 'Generates professional project README files (project statements) for 4Geeks Academy bootcamp modules. Use this skill whenever a user asks to create, write, or generate a project README, project statement, or module instructions for 4Geeks Academy — including any course track (Full-Stack, Data Science, Cybersecurity, AI Engineering). Trigger even if the user says things like "write a new project for the syllabus", "create a module statement", "generate README for this topic", or "I need a bootcamp project about X". Always use this skill when 4Geeks Academy context is present and a project document is needed.'
---

# 4Geeks Academy — Project Statement Generator

This skill generates bilingual project READMEs (`README.md` + `README.es.md`) for any 4Geeks Academy bootcamp module, following the academy's pedagogical principles and formatting standards.

---

## Step 1 — Collect Required Inputs

Before generating anything, scan the conversation for every input below. For each one **not** already provided, add it to your "missing" list. Then ask for **all missing items in a single message** — never spread across multiple rounds.

| Input              | Description                                                                                                                                                       | Default                                       |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `module_topic`     | Core concept(s) this module teaches                                                                                                                               | — Must ask —                                  |
| `module_class`     | Syllabus classification: a **skill** name (e.g. "CSS Flexbox"), a **week/day** slot (e.g. "Week 3 / Day 2"), or a **subject** area (e.g. "Frontend Fundamentals") | — Must ask —                                  |
| `module_position`  | Position in syllabus: `early`, `mid`, or `late`                                                                                                                   | — Must ask —                                  |
| `prior_concepts`   | Skills from previous modules available for reinforcement                                                                                                          | — Must ask —                                  |
| `project_context`  | Professional scenario, industry, or client type                                                                                                                   | — Must ask —                                  |
| `template_repo`    | Starter repo URL students will fork                                                                                                                               | `https://github.com/4GeeksAcademy/html-hello` |
| `authors`          | GitHub username(s) — one or two authors                                                                                                                           | — Must ask —                                  |
| `team_type`        | `individual`, `pair`, or `team of N`                                                                                                                              | `individual`                                  |
| `primary_language` | Language for the main README                                                                                                                                      | `English`                                     |

> **Missing-fields rule:** Never proceed to generation with unknown required fields. If `module_topic`, `module_class`, `authors`, `module_position`, `prior_concepts`, or `project_context` are missing, list them clearly and wait for the user's reply before continuing.

> **Note on template repos:** The default is `html-hello`. For TypeScript, Next.js, FastAPI, or other stacks, confirm the correct boilerplate with the author before generating.

---

## Step 2 — Apply Pedagogical Principles

Before writing, internalize these rules:

- **Learning by doing**: The README does not re-teach lesson content. Theory is assumed to be covered.
- **Complementary knowledge exception**: If the project requires operational context _not_ in the lessons (e.g., what makes a good dashboard), add a brief, practical subsection in the challenge. Keep it concise.
- **Progressive difficulty**: Early = more guided. Late = more open. Never assume mastery of newly introduced concepts.
- **Prior module reinforcement**: Include prior skills in the checklist _only_ when the project naturally accommodates them. Do not force them in.
- **Professional framing**: Frame everything as a real work scenario (client request, team assignment, business problem). Never use academic framing ("in this exercise you will…").
- **Active reading**: Embed some requirements in the narrative — not everything in bullet lists. Students should practice extracting specs from text like a real brief.

---

## Step 3 — Write the README

### Required Structure (exact order)

```
1. Project Title
2. Hidden metadata block
3. --- separator
4. 🎯 Challenge
   └── [optional] complementary knowledge subsection
   └── [optional] client spec in blockquotes
5. 🌱 How to Start the Project
6. 💻 What You Need to Do  (checklist)
7. ✅ What We Will Evaluate  (checklist)
8. 📦 How to Submit
9. --- separator + Footer
```

**Mandatory section emojis:**

- `🎯` Challenge / Tu reto
- `🌱` How to start / Cómo iniciar el proyecto
- `💻` What to do / Qué debes hacer
- `✅` Evaluation / Qué vamos a evaluar
- `📦` Submission / Cómo entregar

---

### Hidden Metadata Block

Place this immediately after the title, before the first `---`.

**One author:**

```markdown
<!-- hide -->

By [@username](https://github.com/username) and [other contributors](https://github.com/4GeeksAcademy/repo-name/graphs/contributors) at [4Geeks Academy](https://4geeksacademy.com/)

[![build by developers](https://img.shields.io/badge/build_by-Developers-blue)](https://4geeks.com)
[![4Geeks Academy](https://img.shields.io/twitter/follow/4geeksacademy?style=social&logo=x)](https://x.com/4geeksacademy)

_Estas instrucciones están [disponibles en español](./README.es.md)._

**Before you start**: 📗 [Read the instructions](https://4geeks.com/lesson/how-to-start-a-project) on how to start a coding project.

<!-- endhide -->
```

**Two authors:** Replace the first line with:

```markdown
By [@firstusername](https://github.com/firstusername) and [@secondusername](https://github.com/secondusername) and [other contributors](https://github.com/4GeeksAcademy/repo-name/graphs/contributors) at [4Geeks Academy](https://4geeksacademy.com/)
```

> The contributors list link must always be present, regardless of the number of named authors.

---

### 🎯 Challenge Section

1. Open with a **realistic professional scenario**: a client, a startup, a consulting engagement, an internal team need. Be specific enough to feel real.
2. **Describe the problem**, not just the solution. What situation does the client face? What do they need?
3. **Embed some requirements in the narrative** — not every spec is a bullet. Students should practice reading carefully.
4. If needed, add a **complementary knowledge subsection** for context not covered in lessons.
5. For requirements from a PM, email, or spec sheet: use **nested blockquotes** attributed to the source:

```markdown
> Your project manager has shared the following spec:
>
> #### Home page
>
> - Navbar with logo and search bar
> - Hero section
> - Footer with links
```

6. Close with a short **motivating call to action**.

**Avoid:**

- Re-explaining technologies from lessons
- Over-specifying implementation details
- Academic framing ("in this exercise you will practice…")

---

### 🌱 How to Start Section

- Include the template repo link (default or confirmed)
- Reference both Codespaces and local clone
- Remind the student to create their own GitHub repo and update the remote URL
- Link to: [how to start a coding project](https://4geeks.com/lesson/how-to-start-a-project)

---

### 💻 What You Need to Do Section

- Use `- [ ]` for every deliverable
- Group items logically (by view, feature, component, or milestone)
- Include prior module skills only if the project context naturally supports them
- Add `⚠️ **IMPORTANT:**` for technology restrictions
- This section **confirms** what was introduced in the challenge — do not introduce new requirements here

---

### ✅ What We Will Evaluate Section

- Map criteria to the **current module's learning objectives**
- Include prior module criteria only if those skills appear in the task checklist
- Write **observable, measurable outcomes** — not vague qualities
  - ✅ `Correct use of semantic HTML tags`
  - ❌ `Good code quality`
- Use `- [ ]` format
- Add `> Note:` for anything explicitly excluded from evaluation

---

### 📦 How to Submit Section

- Keep brief and consistent
- Standard: push repo to GitHub and share according to the instructor's instructions
- Add track-specific details when relevant (deployed URL, notebook export, specific branch name)

---

### Standard Footer

**English (README.md):**

```markdown
---

This and many other projects are built by students as part of the [Career Programs](https://4geeksacademy.com/compare-programs) at [4Geeks Academy](https://4geeksacademy.com). By [@username](https://github.com/username) and [other contributors](https://github.com/4GeeksAcademy/repo-name/graphs/contributors). Find out more about [AI Engineering](https://4geeksacademy.com/en/coding-bootcamps/ai-engineering), [Data Science & Machine Learning](https://4geeksacademy.com/en/coding-bootcamps/data-science-ml), [Cybersecurity](https://4geeksacademy.com/en/coding-bootcamps/cybersecurity) and [Full-Stack Software Developer with AI](https://4geeksacademy.com/en/coding-bootcamps/full-stack-developer).
```

**Spanish (README.es.md):**

```markdown
---

Este y muchos otros proyectos son construidos por estudiantes como parte de los [Coding Bootcamps](https://4geeksacademy.com/) de 4Geeks Academy. Encuentra más acerca de los [cursos](https://4geeksacademy.com/es/comparar-programas) de [Ingeniería de IA](https://4geeksacademy.com/es/coding-bootcamps/ingenieria-ia), [Data Science & Machine Learning](https://4geeksacademy.com/es/coding-bootcamps/curso-datascience-machine-learning), [Ciberseguridad](https://4geeksacademy.com/es/coding-bootcamps/curso-ciberseguridad) y [Full-Stack Software Developer con IA](https://4geeksacademy.com/es/coding-bootcamps/programador-full-stack).
```

---

## Step 4 — Output

Always generate **both files**:

- `README.md` — English version (primary)
- `README.es.md` — Spanish translation (consistent with English, same structure)

Each file must include a link to its counterpart, **written in the target language** (i.e. the language the reader would switch _to_):

- English README → link is in Spanish: `_Estas instrucciones están [disponibles en español](./README.es.md)._`
- Spanish README → link is in English: `_These instructions are [available in English](./README.md)._`

---

## Quality Self-Check Before Delivering

- [ ] All required inputs were collected before generation (topic, class, position, prior concepts, context, authors, template)
- [ ] Challenge opens with a realistic professional scenario (not academic framing)
- [ ] Some requirements are embedded in the narrative, not only in bullet lists
- [ ] Complementary knowledge included only where lessons don't cover it, and it's concise
- [ ] Prior module skills appear only where the project naturally supports them
- [ ] Technology constraints marked with ⚠️ IMPORTANT
- [ ] Difficulty matches the module's position in the syllabus
- [ ] All required sections present and in correct order
- [ ] Section emojis consistent: 🎯 🌱 💻 ✅ 📦
- [ ] All checklists use `- [ ]` format
- [ ] Nested blockquotes used only for client-sourced or attributed requirements
- [ ] Hidden metadata block present and correctly formatted
- [ ] Footer present in both languages with correct links
- [ ] Both README.md and README.es.md generated and consistent
- [ ] Alternate language link included in both files
