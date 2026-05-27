---
name: watch-marketplace
description: Poll the Anthropic plugin marketplace manifest until "channelhub" appears, then notify the user. Use when waiting for the security review to land — the submission portal shows "Published" before the public manifest is updated.
---

# Watch the official marketplace for channelhub

The plugin submission shows "Published" in the Anthropic submissions portal,
but the install command keeps failing because Anthropic must add `channelhub`
to the public manifest at
`anthropics/claude-plugins-official/.claude-plugin/marketplace.json`.

This skill is the polling loop that catches the moment that lands.

## Run

The user invokes:

```
/loop 30m channelhub:watch-marketplace
```

(`/loop` is the built-in superpowers skill. `30m` is plenty — manifest deploys
are infrequent.)

## What this skill does each tick

```bash
gh api repos/anthropics/claude-plugins-official/contents/.claude-plugin/marketplace.json --jq '.content' \
  | base64 -d \
  | python3 -c "
import json, sys, datetime
m = json.load(sys.stdin)
plugins = m.get('plugins', [])
hit = next((p for p in plugins if p.get('name') == 'channelhub'), None)
print('CHECKED', datetime.datetime.now().isoformat(timespec='seconds'),
      'plugins:', len(plugins), 'channelhub:', 'YES' if hit else 'NO')
if hit: print(json.dumps(hit, indent=2))
"
```

Branch on the result:

- **Plugin not yet listed** — print one line: `still waiting (N plugins, no channelhub yet)`. Reschedule.
- **Plugin listed!** — STOP the loop. Tell the user clearly:
  - The exact entry from the manifest (source path, category)
  - The install command they can now run: `/plugin install channelhub@claude-plugins-official`
  - That `README.md` and `install.sh` should now be reverted from the
    `--dangerously-load-development-channels` workaround back to the proper
    install path (a follow-up commit for them).
- **API call fails** (rate-limited, network blip) — print the error and
  reschedule. Don't escalate unless 3+ consecutive failures.

## Stop conditions

- Plugin appears in manifest → success, stop.
- User cancels.
- 30+ days elapsed (something's very wrong, escalate to the user).

## Don't

- Don't check more often than 30 minutes — Anthropic is not deploying every
  5 minutes; faster polling is just noise.
- Don't try to "force" the listing by re-submitting — submission already
  passed; the gate is security review on Anthropic's side.
- Don't forget to update memory once it lands. The
  `project_plugin_published.md` memory says "not live yet" — flip it.
