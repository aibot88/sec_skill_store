---
name: npm-package-audit
description: Audit npm packages for publishing quality, cross-OS compatibility, type declarations, build config, security, and CI/CD — produces a scored report with actionable fixes
argument-hint: [package-path-or-name]
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(npm:*), Bash(node:*), Bash(jq:*), Bash(git:*), Bash(./scripts/*:*),
effort: high
paths: "**/package.json"
---

# npm Package Audit

ultrathink

<!-- anthril-output-directive -->
> **Output path directive (canonical — overrides in-body references).**
> All file outputs from this skill MUST be written under `.anthril/audits/`.
> Run `mkdir -p .anthril/audits` before the first `Write` call.
> Primary artefact: `.anthril/audits/npm-package-audit.md`.
> Do NOT write to the project root or to bare filenames at cwd.
> Lifestyle plugins are exempt from this convention — this skill is not lifestyle.

## Dependencies

External tools required at runtime:

- **`node`** (>= 18) — runs `package.json` introspection one-liners
- **`npm`** — executes `npm run build`, `npm pack --dry-run`, audit commands
- **`jq`** — parses JSON in scripts under `scripts/`
- **`git`** (optional) — used for repository metadata checks

Scripts under `scripts/` assume a POSIX shell (`bash`). All run from the package root.

## Before You Start

1. **Locate the package.** Find `package.json` in the target directory. If a path was not provided, look in the current working directory. If no `package.json` is found, ask the user for the package path.
2. **Run the build.** Execute `npm run build` (or the project's build command) so `dist/` artefacts are available for inspection. If the build fails, report it as a Phase 4 critical finding but continue with remaining phases.
3. **Map the project structure.** Run a directory listing excluding `node_modules/`, `.git/`, and `dist/` to understand the codebase layout.

## User Context

$ARGUMENTS

Package state:
- Version: !`node -p "require('./package.json').version" 2>/dev/null || echo "No package.json found"`
- Build output: !`ls dist/ 2>/dev/null | head -10 || echo "No dist/ directory"`

---

## Audit Phases

Execute every phase in order. For each phase, score using the rubric in `reference.md` and report findings with file paths and line numbers. Do not skip phases — mark as N/A if genuinely not applicable.

---

### Phase 1: Package Discovery & Context

**Objective:** Identify the package, tech stack, and configuration.

1. Read `package.json` — extract: name, version, description, type, main, module, types, exports, files, bin, engines, scripts, publishConfig, repository, homepage, bugs, license, keywords, author
2. Detect build tool: look for `tsup.config.ts`, `rollup.config.js`, `rollup.config.mjs`, `esbuild` references in scripts, `vite.config.ts`
3. Detect test framework: `vitest.config.ts`, `jest.config.js`, `jest.config.ts`, `.mocharc.yml`, `package.json` jest config
4. Detect CI/CD: `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`
5. Read `tsconfig.json` if present
6. Read `.npmrc`, `.npmignore` if present
7. Run `npm pack --dry-run 2>&1` to see what would be published
8. Establish project structure with a directory listing

This phase is context-only — no score.

---

### Phase 2: package.json Quality (15 points)

**Objective:** Verify all critical package.json fields are present, correct, and complete.

Refer to the field reference in `${CLAUDE_PLUGIN_ROOT}/skills/npm-package-audit/reference.md` for validation rules.

Run the automated check:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/npm-package-audit/scripts/validate-package-json.sh" .
```

Check three tiers:

**Required** (fail if missing):
- `name` — follows npm naming rules (lowercase, no spaces, valid scope)
- `version` — valid semver
- `description` — present and under 280 chars, not default npm init text
- `main` or `exports` — at least one entry point defined
- `license` — valid SPDX identifier
- `files` — array set (not relying on .npmignore alone), includes dist/

**Recommended** (warning if missing):
- `types` — points to `.d.ts` file
- `module` — points to ESM entry
- `engines` — specifies minimum Node version
- `repository`, `homepage`, `bugs` — URLs present
- `keywords` — 3+ relevant terms
- `author` — name and optionally email/url

**Optional** (suggestion if missing):
- `publishConfig` — access and registry set for scoped packages
- `bin` — entries point to files with proper shebangs
- `sideEffects` — set for library packages to enable tree-shaking
- `funding` — for open-source packages

---

### Phase 3: Exports Map & Entry Points (15 points)

**Objective:** Verify the exports map is correct and all entry points resolve.

Run the automated check:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/npm-package-audit/scripts/check-exports.sh" .
```

1. If `"exports"` is defined, for every path entry verify:
   - `"types"` condition comes **first** (TypeScript resolution order)
   - `"import"` points to `.js` or `.mjs` file
   - `"require"` points to `.cjs` file
   - All referenced files exist in the build output
2. If subpath exports exist (e.g., `"./hooks/runner"`), verify each resolves to a real file
3. Check `"main"`, `"module"`, `"types"` are consistent with `"exports"` (no conflicts)
4. Verify `"type": "module"` is set if ESM is the primary format
5. Check for `"sideEffects"` field if the package is a library

---

### Phase 4: Build Configuration (15 points)

**Objective:** Verify build tooling produces correct dual CJS/ESM output with types and source maps.

1. **Build tool config** — read tsup/rollup/esbuild config and verify:
   - Both `esm` and `cjs` formats configured
   - `dts` (type declaration generation) enabled
   - `sourcemap` enabled
   - `target` matches `engines.node`
   - `clean` set to avoid stale artefacts
2. **TypeScript config** — verify `tsconfig.json`:
   - `"declaration": true` (if types not handled by build tool)
   - `"strict": true`
   - `"moduleResolution"` matches the package's module system
3. **Build output** — run `npm run build` then verify:
   - ESM entry exists (`.js` or `.mjs`)
   - CJS entry exists (`.cjs`)
   - Type declarations exist (`.d.ts`)
   - Source maps exist (`.js.map`, `.cjs.map`)
   - No unexpected files in dist/
4. **Build script hygiene** — flag overly long shell one-liners in `"build"` script

---

### Phase 5: Type Declarations (10 points)

**Objective:** Verify type declarations are correct, complete, and usable.

1. Run `npx tsc --noEmit` — zero errors required
2. Verify every exported function/class/type from the entry point has a corresponding declaration in the `.d.ts` output
3. Check for `any` types in the public API surface: `grep ": any" dist/*.d.ts`
4. Verify declaration maps (`.d.ts.map`) exist if `declarationMap: true` in tsconfig
5. Verify subpath export declarations resolve (e.g., `dist/hooks/runner.d.ts` exists if `"./hooks/runner"` is exported)
6. Check for excessive `// @ts-ignore` or `// @ts-expect-error` in source

---

### Phase 6: Testing & Coverage (10 points)

**Objective:** Verify tests exist, pass, and meet coverage thresholds.

1. Test framework configured (vitest, jest, mocha, etc.)
2. Run `npm test` — all tests must pass
3. Run coverage: `npm run test:coverage` or equivalent
4. Check coverage thresholds (recommended minimums):
   - Lines: >= 80%
   - Branches: >= 70%
   - Functions: >= 75%
   - Statements: >= 80%
5. Coverage thresholds enforced in config (not just CLI flags)
6. Critical paths have test coverage: main exports, CLI entry point, error handling
7. Coverage excludes configured: `node_modules/`, `dist/`, `tests/`, config files
8. Test commands present in `package.json` scripts

---

### Phase 7: Cross-OS Compatibility (10 points)

**Objective:** Verify the package works on Linux, macOS, and Windows.

Run the automated check:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/npm-package-audit/scripts/cross-os-lint.sh" .
```

1. **Path separators** — grep for hardcoded `/` or `\\` in path construction; must use `path.join()`, `path.resolve()`, or `path.sep`
2. **Line endings** — `.gitattributes` exists with `* text=auto` or similar
3. **Shell scripts** — any `.sh` files have `#!/usr/bin/env bash` shebang, not `#!/bin/bash`
4. **Bin shebangs** — `bin` entries use `#!/usr/bin/env node`
5. **Environment variables** — `process.env` access accounts for cross-OS differences (`HOME` vs `USERPROFILE`)
6. **File system case sensitivity** — no two files in same directory differ only by case
7. **npm scripts** — use cross-platform syntax:
   - `&&` not `;` for chaining
   - Avoid `rm -rf` (use `rimraf` or `del-cli`)
   - Use `cross-env` for env var setting if needed
8. **CI matrix** — tests run on ubuntu, macos, and windows
9. **Node version matrix** — CI tests on minimum `engines.node` version and latest LTS

---

### Phase 8: Security & Supply Chain (10 points)

**Objective:** Identify security vulnerabilities and supply chain risks.

1. Run `npm audit 2>&1` — report critical/high/moderate/low counts
2. `.npmrc` does not contain tokens or credentials
3. `npm pack --dry-run` output reviewed — no unexpected files published:
   - `.env`, `.env.*` must be excluded
   - `tests/`, `coverage/`, `.github/` excluded
   - Source files excluded if only distributing compiled output
4. No `postinstall` scripts that download binaries or run arbitrary code
5. Dependencies pinned or range-locked appropriately (no `"*"` ranges)
6. `package-lock.json` is committed for reproducible installs
7. No dependency confusion risk: scoped package name, `publishConfig.registry` set
8. If using GitHub Actions for publish: `NPM_TOKEN` in secrets, `--provenance` flag used

---

### Phase 9: Publishing Configuration & CI/CD (10 points)

**Objective:** Verify the publish pipeline is correct and automated.

1. `"publishConfig.access"` set (`"public"` for scoped packages)
2. `"prepublishOnly"` or `"prepack"` script runs build + test
3. GitHub Actions publish workflow (if present):
   - Triggers on correct event (tag push, release, or merge to main)
   - Runs install, build, test before publish
   - Uses `npm publish --provenance` for supply chain security
   - Creates git tag and GitHub Release
   - Handles prerelease dist-tags correctly
4. Package follows semver; prerelease tags (alpha, beta, rc) handled
5. CHANGELOG exists and follows Keep a Changelog or Conventional Changelog format
6. README exists with: description, install instructions, basic usage, license
7. LICENSE file exists and matches `"license"` field

---

### Phase 10: Documentation & Conventions (5 points)

**Objective:** Verify community conventions and documentation quality.

1. **README.md** — has title, install instructions, usage example (code block), API docs or link, license section, badges (npm version, CI, coverage, license)
2. **CONTRIBUTING.md** — setup, development, and PR instructions
3. **LICENSE** — matches package.json, recognised SPDX identifier
4. **CHANGELOG.md** — follows semver, latest version documented
5. **.editorconfig** — present for consistent formatting
6. **Husky + commitlint** (if configured) — hooks installed, config valid
7. **Prettier + ESLint** — both configured, `format:check` and `lint` scripts exist
8. **SECURITY.md** — vulnerability reporting instructions (recommended for public packages)

---

## Scoring

Calculate scores per phase using the rubric in `${CLAUDE_PLUGIN_ROOT}/skills/npm-package-audit/reference.md`.

**Verdict thresholds:**
- **90-100**: PASS — production-ready
- **70-89**: PASS WITH WARNINGS — publishable but improvements needed
- **50-69**: CONDITIONAL — significant issues to address before publishing
- **0-49**: FAIL — not ready for publishing

---

## Reporting

After all phases, produce a structured report. Use the template from `${CLAUDE_PLUGIN_ROOT}/skills/npm-package-audit/templates/output-template.md`.

The report must include:
- A clear PASS / FAIL / PASS WITH WARNINGS verdict per phase
- Every finding must include a **file path and line number** (or config field name)
- Severity ratings: **CRITICAL** (must fix before publish), **WARNING** (should fix), **SUGGESTION** (nice to have)
- A prioritised action list at the end
- Mermaid charts for visual summary

---

## Important Principles

- **Be thorough.** Read actual config files and run actual commands. Don't guess from file names.
- **Be specific.** Every finding needs a file path + line number or config field reference. "Consider improving exports" is useless — say exactly what's wrong and where.
- **Don't fix during the audit.** This is a report. List findings and let the user decide.
- **Run commands when possible.** `npm pack --dry-run`, `npm audit`, `tsc --noEmit`, `npm test` — real output beats eyeballing.
- **Test the consumer experience.** Think about what happens when someone `npm install`s the package — do types resolve? Do imports work? Does the CLI start?

## Edge Cases

1. **No build step** — package publishes source directly (e.g., pure JS). Skip Phase 4 build verification but still check entry points.
2. **Monorepo package** — the package may be nested inside a workspace. Adjust paths to find the correct package.json and build output.
3. **CJS-only package** — no ESM output. Flag as a warning but don't fail — some packages legitimately target CJS only.
4. **Private package** — `"private": true` in package.json. Skip publishing checks (Phase 9) but still audit quality.
5. **CLI-only package** — no library exports, only `bin`. Adjust Phase 3 to focus on bin entry rather than exports map.
6. **Pre-1.0 package** — semver allows breaking changes in 0.x. Note this but don't penalise.
