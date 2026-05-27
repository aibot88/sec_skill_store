---
name: cg-cloud
description: Invoke when the user wants to understand or manage the cloud layer — publishing, governance, adopt/sync/unpublish, account authentication, registry configuration, or whether to use cg vs a self-hosted registry. Covers both conceptual questions ("what does X mean") and operational ones ("how do I log in", "how do I add a registry"). Fires on "how does cloud work", "explain publishing", "what's governance", "open vs protected", "why can't I push this widget", "what does adopt do", "should I use cg or my own registry", "manage my cloud account", "how do I log in to cartograph", "how do I add a registry", "list my registries", "who am I logged in as", "whoami", "how do I connect to a new registry". Does NOT fire on one-off agent MCP calls made as part of a task (e.g. the agent calling checkin_widget with publish=true). Does NOT fire on config/defaults intent — that's cg-config. Does NOT fire on reviewing an incoming proposals queue — that's cg-proposals.
---

# cg-cloud — understand the cloud layer

This skill orients the user to how Cartograph's cloud layer works
and handles the bounded account and registry operations that go with
it: login/logout/whoami, registry add/remove/list, adopt, sync,
publish/unpublish.

It does not own the stable setup preferences (cg-config handles
defaults) or walking the proposals queue (cg-proposals). Hand off
cleanly if the conversation drifts into either.

## Tool boundary

Prefer Cartograph MCP tools when they cover the action. Use
`cartograph_config` for defaults, `checkin_widget` with
`publish=true` for explicit checkin-and-publish flows, and
`registry_widget` for search/install/inspect operations.

Use the `cartograph` CLI for auth, registry listing, proposals,
adopt/sync/unpublish/settings, or other cloud commands that are not
currently exposed as MCP tools.

## Opening reads

In parallel, call:
- `cartograph_config` — for `publish-registry`, `visibility`,
  `governance`, `auto-publish`
- `cartograph whoami` — for auth state on the current registry
- `cartograph registry` — for the list of configured registries

## Start with where the user stands

Before explaining anything, ground the conversation in the user's
current situation. One sentence, concrete:

- *"You're authenticated as `<user>`, publishing to `cg` (public
  community registry), governance default is `open`."*
- *"You're not authenticated on `cg`. Reads work fine, but publishing
  or managing widgets needs `cartograph login` first."*
- *"You're set up to publish to `acme` (self-hosted), visibility
  default is `private`, governance default is `protected`."*

This single sentence decides which parts of the explanation matter
most to the user. Don't skip it.

## What this means in practice

Before jumping into abstract concepts, spell out how the user's
current settings actually behave. One short paragraph synthesizing
`auto-publish` + `publish-registry` + `governance` + auth state into
an operational narrative.

Common shapes:

- **auto-publish on, registry=cg, governance=open, logged in:** every
  successful checkin pushes a new public version to `cg`. Community
  members can propose updates; minor edits flow through
  automatically, significant changes (widget.json or substantial
  code) queue up for your review.
- **auto-publish off, registry=cg, logged in:** checkin stays local.
  When you explicitly run `cloud publish`, the widget goes public.
  Governance applies only to widgets you've actually published.
- **auto-publish on, registry=<org>, visibility=private, logged in:**
  every checkin pushes privately to the org registry. Only invited
  collaborators see it. Governance determines whether those
  collaborators can edit without your approval.
- **not logged in:** reads still work — you can search and install —
  but any publish or governance action fails until `cartograph
  login`. If `auto-publish=true`, checkin will succeed locally and
  the publish step will fail loudly.

Write this as a single paragraph, not a bulleted list. Match the
user's actual config.

## The layer, in one paragraph

Cloud registries host widgets so other people — or other machines —
can install them. `cg` is the public community registry that ships
with Cartograph. Self-hosted registries exist for orgs that want their
own namespace (identified by a custom prefix). Auth is per-registry;
being logged into one doesn't log you into another.

## The two choices that actually matter

Frame the user's decisions as two axes:

**1. Where should widgets live?**
- `cg` — public community registry. Free, shared, discoverable. All
  widgets on `cg` are public; `visibility` is a no-op here.
- Self-hosted (`acme`, `myorg`, etc.) — org's own namespace. Private
  visibility is load-bearing. Useful for proprietary widgets.

**2. How much control do you want over your widgets?**
- `open` — the community can push updates. Proposals fire back to you
  only for *significant* changes (widget.json edits, or substantive
  code changes). Minor edits flow through without approval. Best when
  you want the wheel to turn and don't mind others polishing your
  work.
- `protected` — every proposed update requires your manual
  accept/reject. Best when you spent a lot of time on a widget and
  don't want anyone breaking it.

Governance is set per-widget, but defaults to the config's
`governance` value at publish time.

## The operations, each in a sentence or two

**publish** — shares the widget with the configured registry so others
can install it. Either manual (`cartograph cloud publish`) or
automatic on every checkin (`auto-publish=true`).

**unpublish** — removes the widget from the registry. Users who
already installed still have the code on their machine, but future
searches won't find it. Republishable later with the same widget_id.

**adopt** — links a local widget to its cloud counterpart by writing
a `.cartograph_source` sidecar. Use this when you have a local widget
that's really the cloud version but Cartograph doesn't know that — so
`checkin --publish` fails because the link is missing. `cartograph
cloud adopt <local-id> <@owner/prefix-widget-id>` fixes it.

**sync** — pulls lesser versions up to speed. Compares local library
against cloud; higher version wins in either direction. Useful after
long offline stretches or a fresh clone.

**settings** — per-widget tweaks you own (its specific visibility,
governance). Overrides the config defaults for that one widget.

**proposals** — incoming queue of changes others submitted to your
widgets. Mention it in passing; the cg-proposals skill walks the
actual review workflow.

## Help the user decide

Close with a short, direct recommendation shaped by what you read:

- *"If you mostly want to consume widgets, `cg` with no login is
  fine."*
- *"If you want to contribute back, login to `cg` and pick
  `governance=open` if you're comfortable with community edits, or
  `protected` if you want to gatekeep."*
- *"If you're at an org, add your org's registry with `cartograph
  registry add <url>`, set `publish-registry=<org>`, and
  `visibility=private` if that's the org's norm."*

Hand-off line if they want to change defaults:
*"If you want to change any of this, cg-config can walk the setup."*

## Common gotchas (when publishing fails)

If the user's publish isn't working, check in this order:

1. **Not logged in.** `cartograph whoami` returns unauthenticated on
   the target registry. Fix: `cartograph login`.
2. **Wrong `publish-registry`.** Config points to a registry the user
   doesn't have configured, or the widget_id prefix doesn't match.
3. **Sidecar missing on a cloud widget.** Local widget exists but has
   no `.cartograph_source` — checkin refuses to push. Fix: `cartograph
   cloud adopt`.
4. **Visibility misconfigured for target.** On a self-hosted registry,
   `visibility=public` may be rejected by the registry's policy.
5. **Unstamped widget.** Validation stamp missing or stale — widget
   gets filtered from search post-publish. Fix: re-validate before
   checkin.

State the observed cause, don't guess. If multiple could apply, ask.

## Scope

This skill explains the cloud layer. It does not change config
(cg-config does), does not review proposals (cg-proposals does), and
does not plan widget work (cg-plan does). If the conversation drifts
into those, hand off cleanly.

## What not to do

- Don't launch into mechanics before grounding the user in their
  current auth + registry state.
- Don't explain every CLI flag. The MCP surface handles mechanics;
  this skill is about the mental model.
- Don't recommend flipping a widget to public without the user saying
  they want that — publishing is meaningful.
- Don't walk the proposals queue here. Mention it, then stop.
- Don't editorialize governance choices. `open` and `protected` are
  both legitimate; the right one depends on the widget.
