# /update-skill - Update Existing Skills from Project Knowledge

Refresh one or more skills by diffing their current content against what the project actually does today. Pulls from `.context/knowledge/`, live source files, and dependency manifests to keep skills accurate and actionable.

## When to Run
- After `/learn` accumulates several entries for a domain a skill covers
- After a library version upgrade that a skill documents
- After conventions drift and the skill no longer reflects reality
- Periodically (e.g., after every few features) to keep skills sharp

## $ARGUMENTS

Parse the invocation:
- `/update-skill [name]` — update a specific skill by directory name (e.g., `testing-conventions`)
- `/update-skill --stale` — scan all skills, identify drift, report, ask which to update
- `/update-skill --all` — run `--stale` check then update every stale skill

## Process

### Single skill: `/update-skill [name]`

1. **Validate** the skill exists at `skills/[name]/SKILL.md`. If not, stop and list available skills.

2. **Measure baseline**: `wc -c skills/[name]/SKILL.md` and record the byte count.

3. **Diff current state** — compare skill content against project reality:

   - **testing-conventions**: Read actual test files. Check framework (jest/pytest/rspec), file naming, describe/it structure, mocking approach, assertion style. Note mismatches with what the skill claims.
   - **api-conventions**: Read actual route/controller files. Check HTTP method conventions, error response shape, auth middleware placement, validation patterns.
   - **Library skills** (postgres, redis, python-backend, etc.): Read `package.json`, `requirements.txt`, `Gemfile`, or equivalent. Compare installed version against the version the skill documents. Flag if major version differs.
   - **Any skill**: Check `.context/knowledge/` for entries that belong in this skill's domain — see step 4.

4. **Gather new content** from knowledge sources:
   - Scan `.context/knowledge/LEARNINGS.md` for entries related to this skill's domain
   - Scan `.context/knowledge/libraries/` for relevant library knowledge files
   - Read `.context/patterns/CODE_PATTERNS.md` and `ANTI_PATTERNS.md` for patterns that fit this skill's scope
   - If this is a library skill and the version changed: use Context7 to check for API changes between the documented version and the installed version

5. **Draft the update**:
   - Merge new content into the existing skill structure — preserve section headings and archetype
   - Remove content that contradicts what the project actually does (document the removal reason in the report)
   - Preserve all existing content that is still accurate
   - If populating a previously empty skeleton: follow the same population approach `/init` uses (read real project files, fill sections with concrete, greppable examples)
   - Token budget: aim for ~40 lines in SKILL.md. If new content would push past that, extract detail to `skills/[name]/REFERENCE.md` and link from SKILL.md

6. **Review pass**: Delegate to `reviewer` agent with:
   - The original skill content
   - The proposed updated content
   - The source evidence gathered in steps 3-4

   Reviewer checks:
   - No valid existing content was lost
   - New content is accurate, concrete, and actionable (not vague)
   - Still within the ~40-line token budget
   - The `description` frontmatter field still accurately describes what the skill covers
   - Structural archetype (sections, frontmatter) is intact

7. **Apply** reviewer-approved changes by writing the updated SKILL.md.

8. **Measure after**: `wc -c skills/[name]/SKILL.md`. Report delta.

9. **Report**:
   ```
   Skill updated: skills/[name]/SKILL.md
   Before: [N] bytes | After: [N] bytes | Delta: [+/-N]

   Changes:
   - Added: [what was added and why]
   - Removed: [what was removed and why]
   - Unchanged: [what was preserved]

   Sources used: [list of .context/ files or source files consulted]
   ```

---

### Stale scan: `/update-skill --stale`

1. **Enumerate** all skills in `skills/*/SKILL.md`.

2. **Classify each skill**:
   - **Framework-level** (auth-security, context-system, sequential-thinking, prompt-efficiency, mcp-tools, context7-docs, git-workflow, deployment-cicd): skip — these document general best practices, not project specifics.
   - **Project-specific** (testing-conventions, api-conventions, and any user-created skills): check for drift.
   - **Library skills** (postgres, redis, python-backend, react-frontend, ruby, database-migrations, knowledge-base, google-workspace, postgres-mcp, puppeteer): check installed version vs documented version.

3. **For each project-specific skill**: run the diff check from step 3 of the single-skill flow (lightweight — just flag mismatches, don't gather full new content yet).

4. **For each library skill**: read the relevant manifest (package.json, requirements.txt, Gemfile, pyproject.toml) and compare the installed version to what the skill documents.

5. **Report staleness**:
   ```
   ## Skill Staleness Report

   | Skill                  | Type            | Status  | Drift Details                          |
   |------------------------|-----------------|---------|----------------------------------------|
   | testing-conventions    | project-specific| STALE   | Skill says jest, project uses vitest   |
   | api-conventions        | project-specific| OK      | No drift detected                      |
   | postgres               | library         | STALE   | Skill: v14, installed: v16             |
   | redis                  | library         | OK      | Version matches                        |
   | auth-security          | framework       | SKIPPED | Framework-level, not project-specific  |
   ```

6. **Ask**: "Which skills would you like to update? List names or say 'all stale'."

7. **Update each confirmed skill** using the single-skill flow above.

---

### Update all: `/update-skill --all`

Run the `--stale` scan, then update every skill flagged as STALE without prompting per-skill. Present a combined report at the end.

---

## Rules
- Never modify framework-level skill content (e.g., auth-security OWASP rules, react-frontend component patterns, git-workflow branching rules). These encode general best practices, not project specifics.
- Only update project-specific content: testing-conventions, api-conventions, and any user-created or empty skills.
- For library skills: update the documented version and any API usage notes that changed — do not rewrite the entire skill.
- Always preserve the skill's structural archetype (frontmatter, section headings). Never remove sections — only clear stale content within them.
- Token budget (~40 lines for SKILL.md) is enforced. Overflow goes to `skills/[name]/REFERENCE.md`.
- Reviewer agent must approve before any changes are written.
- Report before/after byte counts for every updated skill.
- If a skill is an empty skeleton, populating it is the same operation — treat it as a full update from scratch, sourcing content from real project files.
- Do not update skills when the project has no source files in that skill's domain — report "no project content found" instead.

## User Input
$ARGUMENTS
