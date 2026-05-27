---
name: author-skill
description: Author a new Cody skill and ship it end-to-end. Writes skills/<name>/SKILL.md, commits on the secret-agent-skills-bank branch (Cody's own branch), and fast-forwards main to the same commit so the existing publish-gateway-bundle workflow rebundles skills/** and pulls them onto the gateway. No human review step. Use when the user asks Cody to create a new skill. Do NOT use to edit an existing skill.
metadata: {"openclaw":{"emoji":"🧩","os":["linux"],"requires":{"bins":["git"]}}}
---

# author-skill

Create a new skill and ship it to the gateway without human review. Cody owns this flow end-to-end.

## Inputs you need before running

- `SKILL_NAME` — kebab-case folder name, e.g. `outlook-search-folders`. Must be unique under `skills/`.
- `SKILL_DESCRIPTION` — one sentence, present tense, starting with a verb. Goes into frontmatter `description`.
- `SKILL_BODY` — Markdown body. Mirror the shape of `skills/cody-admin/SKILL.md` or `skills/memory-read/SKILL.md`: what it does, when to use, when NOT to use, commands, notes.
- `REQUIRED_BINS_JSON` — JSON array of binaries the skill shells out to, e.g. `["memory-read"]`. Use `[]` for pure-prose skills.
- `EMOJI` — one glyph for the operator-studio sidebar.

If any are missing, ask the user. Do not invent names or descriptions.

## Preconditions

- Working tree is `/opt/openclaw/repo/Agent-Cody` (the clone bootstrapped by `openclaw-init.sh`).
- SSH deploy key from secret `agent-cody/github-deploy-key` is already installed. No GitHub PAT needed — deploy key is write-enabled for this repo.
- `git status` is clean before starting. If dirty, abort and report — do not stash, reset, or improvise.

## Flow

```bash
set -euo pipefail

REPO=/opt/openclaw/repo/Agent-Cody
BRANCH=secret-agent-skills-bank

cd "$REPO"

# Refuse to run on a dirty tree so we never entangle unrelated work.
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERROR: working tree is dirty; aborting to avoid mixing changes" >&2
  git status --short >&2
  exit 1
fi

# Always start from a fresh main so the FF push to main below is valid.
git fetch origin main
git checkout -B "$BRANCH" origin/main

# Create the skill. $SKILL_NAME must be kebab-case.
mkdir -p "skills/$SKILL_NAME"
cat > "skills/$SKILL_NAME/SKILL.md" <<SKILL_EOF
---
name: $SKILL_NAME
description: $SKILL_DESCRIPTION
metadata: {"openclaw":{"emoji":"$EMOJI","os":["linux"],"requires":{"bins":$REQUIRED_BINS_JSON}}}
---

$SKILL_BODY
SKILL_EOF

# Structural checks — every skill in this repo has a '---' fence on line 1
# and a name: field matching the folder.
head -1 "skills/$SKILL_NAME/SKILL.md" | grep -qx '---' \
  || { echo "ERROR: frontmatter fence missing" >&2; exit 1; }
grep -qE "^name: $SKILL_NAME\$" "skills/$SKILL_NAME/SKILL.md" \
  || { echo "ERROR: name field missing or wrong" >&2; exit 1; }

git add "skills/$SKILL_NAME/SKILL.md"
git commit -m "feat(skills): add $SKILL_NAME"
SHA=$(git rev-parse HEAD)

# Push to Cody's branch first. --force-with-lease is safe here — this is
# Cody's own namespace branch, and we only overwrite our own prior staging.
git push --force-with-lease -u origin "$BRANCH"

# Fast-forward main to the same commit so publish-gateway-bundle.yml fires.
# NO --force here: if main has moved since the fetch above, this push fails
# with non-fast-forward. That is the correct behavior — bail and let the
# operator sort out the conflict rather than clobbering main.
if ! git push origin "HEAD:refs/heads/main"; then
  echo "ERROR: main moved under us; the skill is on $BRANCH at $SHA but main was not advanced" >&2
  echo "Report the branch + SHA to the user and stop. Do NOT force-push main." >&2
  exit 2
fi

echo "shipped $SKILL_NAME at $SHA"
echo "branch: https://github.com/TechniBears/Agent-Cody/tree/$BRANCH"
echo "CI:     https://github.com/TechniBears/Agent-Cody/actions/workflows/publish-gateway-bundle.yml"
```

## After the push

Report back to the user with:

- skill name
- one-line description
- commit SHA
- link to the CI workflow run (the `publish-gateway-bundle` workflow will auto-trigger on the main push and handle bundle upload + SSM pull-latest)

Expect the gateway to be running the new skill within ~3–5 minutes of the push (CI build + bundle upload + SSM pull). If the workflow run goes red, report the failure URL verbatim.

## When NOT to use

- Editing an existing skill — open a normal topic branch and commit there. This skill only creates new additions so the diff stays trivial.
- Shipping a skill that depends on a binary not yet on the gateway. First ship the binary via `scripts/` + a bundle, then add the skill in a follow-up.
- Dirty working tree — abort, do not improvise cleanup.

## Notes

- `secret-agent-skills-bank` is intentionally a long-lived branch, reused every time Cody authors a skill. It accumulates an attribution log of everything Cody has authored. `--force-with-lease` keeps concurrent-push safety.
- The FF push to main is what actually ships. CI is gated on `push: branches: [main]` with `skills/**` in the path filter (`.github/workflows/publish-gateway-bundle.yml`).
- To OPT OUT of this auto-ship for a single skill, the operator pushes their own commit on top of main before Cody's FF push lands — the non-FF check will refuse and Cody will stop with a clear error, leaving the commit on `secret-agent-skills-bank` for manual review.
- Failure to push is almost always an SSH key or known_hosts issue — re-run the SSH setup in `scripts/openclaw-init.sh`, do not substitute HTTPS.
