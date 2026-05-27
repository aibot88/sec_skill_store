---
name: remove-claude-commits
description: Remove Co-Authored-By lines from git history. Use when cleaning Claude Code co-author signatures from commits.
---

# Remove Co-Authored-By

Strip `Co-Authored-By` trailers from git commit messages using `git-filter-repo`.

## Tool

Location: `~/.local/bin/remove-claude-commits`

Dependencies: `bun`, `git-filter-repo`

## Usage

```bash
remove-claude-commits --dry-run   # preview affected commits
remove-claude-commits             # rewrite history
```

## Flags

- `--dry-run` / `-n` — list affected commits without modifying anything

## Preconditions

- Must be inside a git repository
- Working tree must be clean (no staged or unstaged changes)

## Behavior

1. Scans all branches for commits containing `Co-Authored-By`
2. In dry-run mode, lists affected commits and exits
3. In normal mode, uses `git-filter-repo --message-callback` to strip the lines
4. Reports how many lines were removed

## Side Effects

- `git-filter-repo` removes the `origin` remote after rewriting (safety measure)
- All commit hashes from the first affected commit onward will change
- Rewriting invalidates existing commit signatures
- Requires `git remote add`, re-signing, and `git push --force` after running

## Workflow

1. Ensure working tree is clean
2. Run `remove-claude-commits --dry-run` to preview
3. Note existing tags and their commit messages: `git tag -l | xargs -I{} git log --format="{} %s" -1 {}`
4. Push current state to a backup remote if needed
5. Run `remove-claude-commits`
6. Re-sign all commits: `git rebase --root --exec 'git commit --amend --no-edit -S'`
7. Re-tag: for each tag, find the new commit by message and `git tag -f -s <tag> <new-hash>`
8. Re-add remote: `git remote add origin <url>`
9. Fetch remote: `git fetch origin`
10. Diff local against remote: `git diff origin/main..HEAD --stat` to verify only commit messages changed (no file diffs)
11. If branch is protected, temporarily remove protection: `codeberg-settings unprotect <branch>`
12. Propose force push to the user: `git push --force`
13. Force push tags: `git push --force --tags`
14. Re-apply branch protection: `codeberg-settings apply`
