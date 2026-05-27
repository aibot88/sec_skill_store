---
name: airc:repair
description: Full re-pair of a stale airc mesh — `teardown --flush` + reconnect using the saved invite string. Use when your sends silently fail or `resume` reports stale auth.
user-invocable: true
allowed-tools: Bash, Monitor
argument-hint: "[invite-string]"
---

# airc repair

The one-command recovery for the most common airc failure: your saved pairing is stale (SSH key rotated, host regenerated identity, reinstall broke things, you accidentally paired with the wrong host because of a port collision). Runs the full nuclear repair sequence so you don't have to remember the flag names or hunt for the invite string.

## Execute

If `$ARGUMENTS` contains an invite string (looks like `name@user@host[:port]#<base64>`), use it directly. Otherwise reconstruct from the saved config before wiping.

### Step 1 — extract the saved invite before wiping

```bash
# Grab the pieces the host wrote into config during the last pair.
HOST_NAME=$(python3 -c "import json; print(json.load(open('$(airc debug-scope)/config.json')).get('host_name',''))" 2>/dev/null)
HOST_TARGET=$(python3 -c "import json; print(json.load(open('$(airc debug-scope)/config.json')).get('host_target',''))" 2>/dev/null)
HOST_PORT=$(python3 -c "import json; print(json.load(open('$(airc debug-scope)/config.json')).get('host_port',7547))" 2>/dev/null)
HOST_PUB=$(python3 -c "import json; print(json.load(open('$(airc debug-scope)/config.json')).get('host_ssh_pub',''))" 2>/dev/null)
PUB_B64=$(printf '%s\n' "$HOST_PUB" | base64 | tr -d '\n')

if [ -n "$HOST_NAME" ] && [ -n "$HOST_TARGET" ] && [ -n "$HOST_PUB" ]; then
  SUFFIX=""
  [ "$HOST_PORT" != "7547" ] && SUFFIX=":$HOST_PORT"
  INVITE="${HOST_NAME}@${HOST_TARGET}${SUFFIX}#${PUB_B64}"
fi
```

If `$ARGUMENTS` was passed, override `$INVITE` with it — the user may be repairing to a new host.

### Step 2 — teardown --flush

```bash
airc teardown --flush
```

Wipes identity, peer records, saved pairing, messages. State is gone.

### Step 3 — reconnect with the invite

```
Monitor(persistent=true, command="airc connect $INVITE")
```

Fresh handshake, fresh identity keys get pushed to the host's authorized_keys, clean pair.

## When to use

- `airc join` (resume) exited with `Resume aborted — re-pair required`.
- `airc send` exited with `Authentication failure — re-pair required`.
- You re-installed airc and your mesh stopped working.
- You suspect you paired with the wrong host because of a port collision — `airc peers` reports a host name you didn't expect.
- "Nothing works and I don't know why" — repair is the cheap nuclear option.

## Failure modes

- No invite reconstructable + none passed — config is too stale (missing `host_ssh_pub` or `host_target`). User needs a fresh invite from the host. Ask them to get `/invite` output from the host and pass it as the argument.
- Repair succeeds but still no messages — you may genuinely be on the wrong host. Run `airc peers` and confirm the host name matches who you meant to pair with. If not, ask the host to paste their `/invite` output and try `/repair <that-invite>`.

## Notes

- This is intentionally destructive. Identity keys, peer records, message mirror — all gone. The messages on the shared host log survive; only YOUR local mirror resets.
- Safer than guessing which flag to `airc teardown` with. Pre-repair-skill, users reliably typed `airc teardown` (no flush) + `airc join` (resume) and silently stayed broken. Using this skill removes the footgun.
