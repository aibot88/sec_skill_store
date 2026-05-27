---
name: codexini-openclaw
description: Start privacy-preserving Codexini voice calls from OpenClaw.
metadata:
  {
    "openclaw":
      {
        "skillKey": "codexini-openclaw",
        "requires": { "config": ["plugins.entries.codexini.enabled"] },
      },
  }
---

# Codexini for OpenClaw

Use `codexini_bootstrap_call` when the user asks for a one-command install,
enable, consent, and call flow, for example "install Codexini and call me" or
"set up Codexini and start a voice call." Pass only the current OpenClaw
account id, agent id, session key, channel, reply target, optional call id,
and `userInitiated: true`; do not include the user's message text,
topic, reason, memory text, transcript, or tool payload. If the tool returns
`bootstrap_setup_required`, fill missing fields from the current OpenClaw
session if the host exposes them. Do not ask the user whether Aura is installed,
whether a runtime token is present, or which chat should receive the link.

When `codexini_bootstrap_call` succeeds, reply with the returned `join_url` as
the invite link. Include the daily beta minutes remaining when the tool returns
them. That link already carries the browser-only onboarding key; do not add
context, topics, transcripts, memory text, or tool payloads to the message.

Use `codexini_start_call` when the user asks OpenClaw to move the current conversation into a Codexini voice call, for example "call me", "let's talk this through", or "start a Codexini call".

Use `codexini_record_enablement` when the user explicitly asks to install,
enable, or turn on Codexini from an OpenClaw-supported channel. Pass only the
current OpenClaw account id, agent id, session key, channel, reply target, and
`userInitiated: true`; do not include the user's message text or reason.

Use `codexini_record_dispatch_delivery` after OpenClaw delivers a Codexini
call task result back to the original session/channel. Pass only call id,
account id, session key, channel, reply target, dispatch run id, and the two
delivery booleans; do not include the task question, answer, result text, or
tool payload.

Use `codexini_record_scheduler_boundary` after OpenClaw accepts or defers any
future-call or callback work for the current session. Pass only account id,
agent id, session key, channel, reply target, `scheduledCallPath`,
`callbackPath`, `openclawStatusChecked: true`, and
`fallbackWordingPresent: true`; do not include reminder text, callback topics,
transcripts, memory text, or tool payloads.

Prefer `codexini_bootstrap_call` over `codexini_start_call` for normal users.
The user's explicit install-and-call request is the consent action for the
current disclosure version, and the plugin stores that acknowledgement as
metadata only. Do not ask a separate yes/no disclosure question unless the host
cannot persist plugin settings.

When calling `codexini_start_call`, pass the current OpenClaw account id, session key, channel, and reply target. The call-control Worker uses session/channel/reply metadata plus the authenticated account to return any later status to the original OpenClaw place. The account id is also used locally, when `CODEXINI_CONTEXT_EVENTS_JSONL` is configured, to write a metadata-only call-request proof event without message text.

Use Codexini for immediate calls only.

Keep the boundary clear:

- OpenClaw remains the assistant that owns memory, tools, approvals, and final delivery.
- Aura is the voice steering layer the browser opens from the invite link.
- For the beta OpenClaw flow, Codexini manages the browser Aura call link. The
  user should only need to ask OpenClaw and click the returned invite.
- The join link starts onboarding from an encrypted OpenClaw brief, so the
  browser knows the room, host skill names, and safe dispatch boundary after the
  user joins.
- Beta use is capped at one hour per day.
- Codexini call-control should only receive metadata needed to create a single-use invite.
- Do not send transcripts, memory text, tool payloads, prep notes, or summaries to Codexini servers.
- Voice cannot approve destructive operations. Ask for typed or clicked confirmation through OpenClaw.
- During the call, Aura may ask OpenClaw to handle real work through `openclaw_agent_consult`; do not bypass OpenClaw's approval flow with direct tool or confirmation overrides.
- For exact future calls or reminders, use OpenClaw scheduled tasks/cron. Do not store the call topic in Codexini call-control.
- For inferred "check back later" callbacks, use OpenClaw commitments/heartbeat when enabled. If no OpenClaw scheduler accepted the job, say: "I can start a Codexini call now. For later, I need OpenClaw to create the reminder first; I won't store that call topic in Codexini."

Do not use this skill for PSTN phone calls. If the user asks for a normal phone call through OpenClaw's built-in voice-call plugin, use that plugin's `voice_call` tool instead.
