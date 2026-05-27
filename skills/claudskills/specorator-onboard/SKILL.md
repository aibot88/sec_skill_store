---
name: specorator-onboard
description: Create the guided 5-step onboarding series. Always writes local markdown files with frontmatter in docs/onboarding/. Optionally creates GitHub issues when gh auth and a remote are available. Idempotent — skips if series exists.
argument-hint: "[--force]"
---

# Specorator Onboarding

Create five onboarding task files that walk a new Specorator user through the core workflow using real practice — not documentation.

**Local files are always created.** GitHub issues are created only when a GitHub remote and `gh` authentication are both available — they are a bonus, not a requirement. The files in `docs/onboarding/` are sufficient on their own.

## Primary deliverable — local files

Five Markdown files with frontmatter are written to `docs/onboarding/` in the repository root:

| # | File | Title |
|---|---|---|
| 1 | `docs/onboarding/01-create-your-first-issue.md` | `Create your first issue` |
| 2 | `docs/onboarding/02-triage-classify-and-prioritise.md` | `Triage: classify and prioritise` |
| 3 | `docs/onboarding/03-break-the-issue-down.md` | `Break the issue down` |
| 4 | `docs/onboarding/04-open-a-pr-and-enter-the-feedback-loop.md` | `Open a PR and enter the feedback loop` |
| 5 | `docs/onboarding/05-accept-and-merge-the-pr.md` | `Accept and merge the PR` |
The skill creates these files at runtime; they are not committed to the repository.

## Idempotency guard

Check for an existing series:

```bash
ls docs/onboarding/01-create-your-first-issue.md 2>/dev/null
```

If the file exists and `--force` was **not** passed, stop and print:
> Onboarding series already exists (`docs/onboarding/01-create-your-first-issue.md`). Pass `--force` to re-create it.

If `--force` is passed:
1. Remove existing local files:
   ```bash
   rm -f docs/onboarding/0[1-5]-*.md
   ```
2. If GitHub is available, close existing series issues (see Force-close section in Step 3).

## Step 1 — Create local files

Create the directory if it does not exist:

```bash
mkdir -p docs/onboarding
```

For each step, write a file with generated frontmatter followed by the template body:

```bash
TODAY=$(date -I)

{
  echo "---"
  echo "title: \"Create your first issue\""
  echo "status: todo"
  echo "series: onboarding"
  echo "step: 1"
  echo "created: $TODAY"
  echo "---"
  echo ""
  cat templates/onboarding/01-create-your-first-issue.md
} > docs/onboarding/01-create-your-first-issue.md
```

Repeat for steps 2–5, substituting the title, step number, and template filename for each.

## Step 2 — Resolve local next-step links

Replace the placeholder `[Title]()` links with relative paths to the next local file. Also strip the stale auto-update note from file 1.

```bash
sed -i "s|\[Issue 2 — Triage: classify and prioritise\]()|[Issue 2 — Triage: classify and prioritise](./02-triage-classify-and-prioritise.md)|" \
  docs/onboarding/01-create-your-first-issue.md
sed -i '/> \*\*Note:\*\* The link above will be updated automatically/d' \
  docs/onboarding/01-create-your-first-issue.md

sed -i "s|\[Issue 3 — Break the issue down\]()|[Issue 3 — Break the issue down](./03-break-the-issue-down.md)|" \
  docs/onboarding/02-triage-classify-and-prioritise.md

sed -i "s|\[Issue 4 — Open a PR and enter the feedback loop\]()|[Issue 4 — Open a PR and enter the feedback loop](./04-open-a-pr-and-enter-the-feedback-loop.md)|" \
  docs/onboarding/03-break-the-issue-down.md

sed -i "s|\[Issue 5 — Accept and merge the PR\]()|[Issue 5 — Accept and merge the PR](./05-accept-and-merge-the-pr.md)|" \
  docs/onboarding/04-open-a-pr-and-enter-the-feedback-loop.md
```

## Step 3 — GitHub issues (optional)

Check whether GitHub issues can be created. The remote must exist, the origin's **host** must be exactly `github.com` (substring matching would let `notgithub.com` through), and `gh` must be authenticated:

```bash
ORIGIN_URL=$(git remote get-url origin 2>/dev/null) || ORIGIN_URL=""
case "$ORIGIN_URL" in
  git@*:*)
    ORIGIN_HOST="${ORIGIN_URL#git@}"
    ORIGIN_HOST="${ORIGIN_HOST%%:*}"
    ;;
  *://*)
    ORIGIN_HOST="${ORIGIN_URL#*://}"
    ORIGIN_HOST="${ORIGIN_HOST#*@}"
    ORIGIN_HOST="${ORIGIN_HOST%%[/:]*}"
    ;;
  *)
    ORIGIN_HOST=""
    ;;
esac
case "$ORIGIN_HOST" in
  github.com) IS_GITHUB=1 ;;
  *) IS_GITHUB=0 ;;
esac
if [ "$IS_GITHUB" = "1" ] && gh auth status >/dev/null 2>&1; then
  GITHUB_OK=1
else
  GITHUB_OK=0
fi
```

If `GITHUB_OK=0`, skip to **Output** and note:
> GitHub issues skipped — origin is not a GitHub remote or `gh` is not authenticated. Local files in `docs/onboarding/` are the deliverable.

If `GITHUB_OK=1`, proceed with the sub-steps below.

### Force-close existing GitHub issues (`--force` only)

When `--force` is passed, close existing series issues **before** creating replacements. Running this after creation would match the freshly-created issues by exact title and close them too. Skip this block on a non-`--force` run.

Scope the match to issues that carry **all three** onboarding labels (`good first issue`, `status:draft`, `P2`) **and** the exact title — title alone would also match unrelated issues that happen to use a generic phrase like "Break the issue down":

```bash
for TITLE in \
  "Create your first issue" \
  "Triage: classify and prioritise" \
  "Break the issue down" \
  "Open a PR and enter the feedback loop" \
  "Accept and merge the PR"; do
  NUMBER=$(gh issue list --state open --limit 200 \
    --label "good first issue" --label "status:draft" --label "P2" \
    --json number,title \
    --jq ".[] | select(.title == \"$TITLE\") | .number")
  echo "$NUMBER" | grep -v '^$' | while read -r N; do gh issue close "$N"; done
done
```

### Required labels

Create any missing labels before creating issues:

```bash
gh label create "good first issue" --color "7057ff" --description "Good for newcomers" 2>/dev/null || true
gh label create "status:draft" --color "C5DEF5" --description "Issue still being iterated on; not yet ready for /spec:start" 2>/dev/null || true
gh label create "P2" --color "fbca04" --description "Important for next release" 2>/dev/null || true
```

### Create one issue per step

Extract the body of each local file (strip the YAML frontmatter block) and create the issue. `gh issue create` does not support `--json/--jq`; it prints the issue URL to stdout. Capture the URL and derive the number with `basename`:

```bash
BODY=$(awk '/^---/{c++;next} c>=2{print}' docs/onboarding/01-create-your-first-issue.md)
URL1=$(gh issue create \
  --title "Create your first issue" \
  --body "$BODY" \
  --label "good first issue" \
  --label "status:draft" \
  --label "P2")
N1=$(basename "$URL1")
```

Repeat for steps 2–5, recording URLs `URL1`–`URL5` and numbers `N1`–`N5`.

### Update local file frontmatter with issue URL

Record each issue's URL in the local file's frontmatter:

```bash
sed -i "s|^created:.*|&\ngithub_issue: $URL1|" docs/onboarding/01-create-your-first-issue.md
```

Repeat for steps 2–5.

### Resolve GitHub issue next-step links

Update each GitHub issue body to replace the local relative link with the real GitHub issue URL for the next step:

```bash
# Issue 1 → 2
BODY=$(gh issue view "$N1" --json body --jq '.body')
UPDATED=$(echo "$BODY" | sed "s|\[Issue 2 — Triage: classify and prioritise\](./02-triage-classify-and-prioritise.md)|[Issue 2 — Triage: classify and prioritise]($URL2)|")
gh issue edit "$N1" --body "$UPDATED"

# Issue 2 → 3
BODY=$(gh issue view "$N2" --json body --jq '.body')
UPDATED=$(echo "$BODY" | sed "s|\[Issue 3 — Break the issue down\](./03-break-the-issue-down.md)|[Issue 3 — Break the issue down]($URL3)|")
gh issue edit "$N2" --body "$UPDATED"

# Issue 3 → 4
BODY=$(gh issue view "$N3" --json body --jq '.body')
UPDATED=$(echo "$BODY" | sed "s|\[Issue 4 — Open a PR and enter the feedback loop\](./04-open-a-pr-and-enter-the-feedback-loop.md)|[Issue 4 — Open a PR and enter the feedback loop]($URL4)|")
gh issue edit "$N3" --body "$UPDATED"

# Issue 4 → 5
BODY=$(gh issue view "$N4" --json body --jq '.body')
UPDATED=$(echo "$BODY" | sed "s|\[Issue 5 — Accept and merge the PR\](./05-accept-and-merge-the-pr.md)|[Issue 5 — Accept and merge the PR]($URL5)|")
gh issue edit "$N4" --body "$UPDATED"
```

## Output

Always print:

```
Specorator onboarding series created.

Local files:
  docs/onboarding/01-create-your-first-issue.md
  docs/onboarding/02-triage-classify-and-prioritise.md
  docs/onboarding/03-break-the-issue-down.md
  docs/onboarding/04-open-a-pr-and-enter-the-feedback-loop.md
  docs/onboarding/05-accept-and-merge-the-pr.md

Start at: docs/onboarding/01-create-your-first-issue.md
```

If GitHub issues were also created, append:

```
GitHub issues (linked from local file frontmatter):
  #N1 Create your first issue — <URL1>
  #N2 Triage: classify and prioritise — <URL2>
  #N3 Break the issue down — <URL3>
  #N4 Open a PR and enter the feedback loop — <URL4>
  #N5 Accept and merge the PR — <URL5>
```

## Do not

- Do not skip local file creation — they are always the primary deliverable.
- Do not fail when GitHub is unavailable — skip Step 3 and continue to Output.
- Do not delete or overwrite existing files unless `--force` is passed.
- Do not modify the template files in `templates/onboarding/`.
- Do not push commits or open PRs as part of this skill.
