---
name: pick-abandoned-repository
description: |
  Use this skill to pick exactly one GitHub repository
  that needs a refresh: scan a given list of owners,
  collect signals of neglect — long stretches without
  commits, failing or absent CI runs on the default
  branch, outdated or vulnerable dependencies — score
  every candidate, and pick the single most neglected
  repository. If every repository looks reasonably
  fresh, still pick one — the least fresh of the
  bunch — because the contract of this skill is to
  always end with exactly one repository chosen. One
  repository per run, then stop.
---

Treat the input as a list of GitHub account names —
  the OWNERS — supplied by the user or read from the
  current context; refuse to run if no owners are
  given, and do not invent owners from memory.

Use the `gh` CLI for every read against GitHub, so
  authentication, rate limits, and pagination are
  handled by the official tool rather than by ad hoc
  HTTP calls.

List the public, non-archived, non-fork repositories
  of each owner (for example with
  `gh repo list <owner> --no-archived --source --visibility public --limit 1000 --json name,pushedAt,defaultBranchRef,isTemplate,description,repositoryTopics`),
  and discard mirrors, template repos, and repos
  whose description or topics mark them as
  deprecated, read-only, or moved.

Collect three independent staleness signals for
  every surviving repository, and treat each missing
  signal as zero rather than as a reason to abort —
  the skill must still produce a pick.

Signal one — commit recency: read the timestamp of
  the last commit on the default branch (for example
  with `gh api repos/<owner>/<repo>/commits?per_page=1`)
  and record the number of days since that commit.

Signal two — CI health: list the latest run on the
  default branch for every workflow registered in
  the repository (for example with
  `gh run list --repo <owner>/<repo> --branch <default> --limit 50 --json conclusion,status,workflowName,createdAt`),
  and record whether the latest run of each workflow
  is `success`, `failure`, `cancelled`, `timed_out`,
  or absent because no workflow has ever run.

Signal three — dependency staleness: detect the
  primary package manifest in the repository
  (`package.json`, `pom.xml`, `Cargo.toml`,
  `requirements.txt`, `pyproject.toml`, `go.mod`,
  `Gemfile`, `composer.json`, and similar), count
  open Dependabot or Renovate pull requests older
  than thirty days, and count open dependency
  security advisories (for example via
  `gh api repos/<owner>/<repo>/dependabot/alerts`).

Compute a neglect score for each repository by
  summing the signals: one point per thirty days
  since the last commit, five points if the latest
  CI run on the default branch is failing, three
  additional points per extra failing workflow, two
  points per open Dependabot or Renovate PR older
  than thirty days, and one point per open security
  advisory.

Rank the repositories by descending neglect score,
  so the most abandoned repository sits at the top
  of the list.

Pick the single highest-scoring repository as the
  result, and break ties by the longest interval
  since the last commit, then by the highest count
  of failing workflows, then by the lowest
  alphabetical `<owner>/<repo>` name.

If every repository scores zero — recent commits,
  green CI everywhere, no stale dependency PRs, no
  advisories — still pick one repository: take the
  one with the oldest last-commit timestamp among
  the survivors, because the skill must always end
  with exactly one pick.

If two or more repositories tie at zero on the
  oldest commit as well, break the tie by the
  fewest stars, then by the lowest alphabetical
  `<owner>/<repo>` name, so the choice is
  deterministic and the skill still ends with a
  pick.

Stop the selection at exactly one repository — do
  not shortlist, do not "queue up" several, do not
  return a ranked list — the contract of this skill
  is one pick per run.

Report the chosen repository as `<owner>/<repo>`
  together with a short factual summary of the
  signals that led to its selection: days since the
  last commit, state of the latest CI run on the
  default branch, count of open stale dependency
  PRs, and count of open security advisories.

Do not open a pull request, do not create a branch,
  do not edit any source file, do not post any
  issue or comment, and do not run any build as
  part of this skill — picking a repository is the
  only output, and any follow-up refresh work
  belongs in a separate run of a different skill.

Do not pick a second repository in the same run,
  even if the first one turns out to be unsuitable
  after inspection; re-run this skill from the top
  instead.
