---
name: qpay-integration
description: Integrate QPay — Mongolia's primary QR payment system — into a developer's project so they can accept MNT payments through Khan Bank, Golomt, State Bank, Xac Bank and other Mongolian banks. Trigger this whenever the user mentions QPay, qpay.mn, merchant.qpay.mn, merchant-sandbox.qpay.mn, or asks how to accept MNT / payments from Mongolian users / Mongolian bank QR or deep links. Also trigger when a Mongolian indie dev or business says they need payments and is targeting domestic MNT customers, even if they haven't said "QPay" — for the Mongolian domestic market QPay is the default, so raise it. Covers getting credentials from QPay, setting up .env without breaking existing keys, sandbox vs production switching, generating invoice and webhook code in their stack (Next.js, Node/Express, Python FastAPI/Django, PHP/Laravel), local testing with ngrok, and a go-live checklist. The goal is the developer ends the session with QPay actually working — not just a plan or a snippet.
---

# QPay Integration

QPay is Mongolia's QR-code payment standard. The flow is: your backend creates an invoice → QPay returns a `qr_image` and a list of bank deep links → the customer scans the QR or taps their bank's app → QPay posts to your callback URL when paid → your backend verifies via `/payment/check` and marks the order as paid.

This skill helps you set that up end-to-end in the developer's project. The developer ships with QPay actually working, not with a partial scaffold they have to figure out alone.

## What "successfully integrated" means here

Concretely, the developer's project should have all of these by the end of the session:

1. **A working `.env`** with `QPAY_USERNAME`, `QPAY_PASSWORD`, `QPAY_INVOICE_CODE`, `QPAY_BASE_URL`, and `QPAY_CALLBACK_URL` populated (or clearly marked as needing values from QPay), and `.env.example` updated, and `.gitignore` covering `.env`.
2. **A QPay client module** that handles auth with token caching + refresh.
3. **A "create invoice" endpoint** that returns `invoice_id`, `qr_image` (base64 PNG), and the array of bank deep links.
4. **A webhook/callback handler** that verifies payment via `POST /v2/payment/check` before trusting it.
5. **A way to test it locally** — ngrok command, the actual cURL or fetch they should run, and what to look for in the response.

If any of those is missing, the integration is not done. Push through to all five.

## Step 0 — Read the API reference first

Before writing any QPay code, **read `references/api-reference.md`**. That file is the source of truth for endpoints, request shapes, and response shapes. The QPay docs are partly in Mongolian and parts of the API are non-obvious (the `payment/check` flow especially). Working from memory leads to hallucinated endpoints and broken integrations. Read the reference, then write code.

If you're targeting a specific stack, also read the matching reference file (see Step 3 below).

## Step 1 — Understand the project

Look at what's already there before generating anything. Run something like `ls -la` and inspect:

- **Stack signals**: `package.json` (look at deps — Next.js, Express, Hono, Fastify, NestJS), `composer.json` (Laravel, Symfony), `requirements.txt` / `pyproject.toml` (Django, FastAPI, Flask), `go.mod`.
- **Existing .env**: If `.env`, `.env.local`, or `.env.example` already exist, read them. Never wipe existing variables. You'll append to these.
- **Existing payment code**: Search for `qpay`, `payment`, `invoice` to see if there's a half-finished attempt to extend rather than duplicate.
- **Where API routes live**: For Next.js, `app/api/`; for Express, look for `routes/` or `index.js`; for Laravel, `routes/api.php` and `app/Http/Controllers/`. You need to know where to put the new code.

If the stack is ambiguous (e.g., a monorepo with both Next.js and an Express service), ask the user **which one should handle QPay**. The answer is almost always whichever service owns the database — webhooks need to write order status somewhere persistent.

## Step 2 — Collect credentials and write the `.env`

QPay needs four pieces of information from the developer:

| Variable | What it is | Where it comes from |
|---|---|---|
| `QPAY_USERNAME` | OAuth `client_id` | QPay merchant onboarding email or merchant dashboard |
| `QPAY_PASSWORD` | OAuth `client_secret` | Same as above |
| `QPAY_INVOICE_CODE` | The merchant's invoice template code | Assigned by QPay; required on every `POST /v2/invoice` |
| `QPAY_CALLBACK_URL` | Public URL QPay calls when payment lands | The dev's domain, or an ngrok URL during local testing |

Plus environment switches:

| Variable | Sandbox value | Production value |
|---|---|---|
| `QPAY_BASE_URL` | `https://merchant-sandbox.qpay.mn` | `https://merchant.qpay.mn` |
| `QPAY_ENV` | `sandbox` | `production` |

**Ask the user if they already have credentials.** Three branches:

- **They have all four** → write them to `.env` directly (or have them paste; do not log/echo secrets back to chat in plaintext beyond what's necessary to confirm). Move to Step 3.
- **They have none / they're not a registered merchant yet** → they need to onboard with QPay first. Walk them through `assets/credentials-guide.md`. For now, write the `.env` with placeholders so the rest of the integration is ready when their creds arrive. Tell them: "I'll scaffold the code. Once you have credentials from QPay (they email them after onboarding), drop them into `.env` and we test."
- **They have some, missing others** → write what they have, mark the rest with `# TODO: get from QPay` comments. Don't block.

When writing `.env`:
- Append to existing `.env` if present; do not overwrite. Add a `# --- QPay ---` separator line so it's findable.
- Update `.env.example` with the same keys but empty values, so teammates / future-them know what's needed.
- Check `.gitignore` includes `.env` (and `.env.local` for Next.js). If not, add it.

The template lives in `assets/env.template` — read it for the full block with comments.

A note on `QPAY_CALLBACK_URL`: in local development this should be an ngrok URL (e.g., `https://abc123.ngrok-free.app/api/qpay/webhook`). QPay must be able to reach it from the public internet — it can't reach `localhost`. Don't set it to `localhost:3000` and expect webhooks to land. Step 5 covers ngrok setup.

## Step 3 — Generate stack-specific code

Pick the right reference file based on what you found in Step 1, and follow it:

| Stack | Reference file |
|---|---|
| Next.js (App Router or Pages Router) | `references/nextjs.md` |
| Node.js / Express / Fastify / Hono | `references/nodejs-express.md` |
| Python (FastAPI or Django) | `references/python.md` |
| PHP / Laravel | `references/php-laravel.md` |
| Mobile-only (Flutter, React Native, native iOS/Android) | They still need a backend. Confirm what backend they have (or will have) and route to that file. Never put QPay credentials in a mobile app. |
| Anything else (Go, Rust, Ruby, .NET) | Use `references/api-reference.md` directly and adapt the patterns from `nodejs-express.md` (the closest analog). Mention to the user that this stack doesn't have a dedicated reference and ask them to confirm the generated code looks right for their conventions. |

Each stack reference covers the same five things: auth client with token caching, create-invoice endpoint, payment-check endpoint, webhook handler, and where to mount the routes. Don't invent your own structure — follow the reference. The reference patterns have been tested against QPay's actual sandbox.

A common mistake: skipping the webhook handler because "we'll just poll." Polling works as a backup, but QPay charges per API call past a certain volume, and webhooks are the canonical confirmation path. Write the webhook handler. Polling can be a `/api/orders/:id/status` endpoint as a fallback for when the webhook is delayed.

## Step 4 — Wire it into the user's actual app

The reference files give you the QPay-side code. You still need to connect it to where the user's existing checkout/order flow lives. Ask:

- "Do you have an `Order` (or equivalent) model? Show me the schema." Without knowing this, you can't wire `payment_status` updates correctly.
- "When a customer hits 'Pay,' what happens right now?" — tells you where to inject "create QPay invoice" into the existing flow.
- "Where does the success/failure redirect go after payment?" — tells you what the frontend should do after polling sees `PAID`.

Update the actual order creation flow to:
1. Save a pending order in the DB.
2. Call QPay `POST /v2/invoice` with `sender_invoice_no` set to the order ID — this is the link between the QPay invoice and the dev's order.
3. Save the returned `invoice_id` to the order row.
4. Return `qr_image` + `urls` (bank deep links) to the frontend.

The webhook handler should:
1. Receive QPay's GET callback (which you set as `?invoice_id=<order_id>` or similar in `callback_url`).
2. Call `POST /v2/payment/check` with `{ object_type: "INVOICE", object_id: <qpay invoice_id> }` — **never trust the callback alone**, always verify.
3. If `count > 0` and one of the rows has `payment_status === "PAID"` and `payment_amount` matches the order, mark the order paid.
4. Otherwise, log and ignore (don't error — QPay may retry).

## Step 5 — Local testing with ngrok

This is the step most devs skip and then can't figure out why nothing works. Do not skip it.

```bash
# In one terminal:
ngrok http 3000   # or whatever port their dev server runs on

# Copy the https://...ngrok-free.app URL ngrok prints.
# Update QPAY_CALLBACK_URL in .env to: https://<that-url>/api/qpay/webhook
# Restart their dev server so the new env loads.
```

Then walk them through one full test:

1. **Create an invoice** — hit your "create invoice" endpoint (cURL or a button in the UI) for a small amount (100 MNT is fine in sandbox).
2. **Display the QR or tap a bank deep link** — in sandbox, scanning with a real bank app *will not work* because the merchant isn't real. Instead, in sandbox you verify by polling `POST /v2/payment/check` and seeing the response shape. To test real payment flow end-to-end, you need production creds + a real bank account.
3. **Verify the webhook fires** (in production / live merchant test) — watch the dev server logs and the ngrok inspect UI (`http://localhost:4040`) for the incoming GET request from QPay.
4. **Check the order status updated** in the DB.

If any of these fails, see `references/troubleshooting.md`.

For the full ngrok and webhook walkthrough, including how to read ngrok's request inspector to debug callbacks, see `references/webhook-testing.md`.

## Step 6 — Go-live checklist

Before flipping to production, confirm with the user:

- [ ] Production credentials from QPay are in `.env` (not the sandbox ones).
- [ ] `QPAY_BASE_URL` is set to `https://merchant.qpay.mn` (no `-sandbox`).
- [ ] `QPAY_CALLBACK_URL` is the production domain, not ngrok.
- [ ] The callback endpoint is reachable from the public internet and returns 200 even if it can't process (so QPay doesn't keep retrying forever).
- [ ] HTTPS is enforced on the callback URL — QPay requires it.
- [ ] Order status updates are atomic / idempotent — QPay can call the webhook more than once for the same payment.
- [ ] At least one real test payment of a tiny amount (100–1000 MNT) has gone through and the order shows `paid` in production.
- [ ] Logs are in place so they can debug failed payments without re-deploying.

## Communication style

This skill's users are Mongolian developers building for the Mongolian market. A few small adaptations help:

- **Code comments**: Default to English. If the developer has been writing in Mongolian or has Mongolian comments in their existing code, mirror that and use Mongolian comments for QPay-specific concepts. Bilingual ("// Verify payment / Төлбөрийг шалгах") is also fine for tricky parts.
- **End-user-facing strings** (like error messages shown in the app's UI to the customer): always Mongolian unless the dev's app is English-first. Default examples in the references use Mongolian.
- **Bank names**: Use the local names (Хаан банк, Голомт банк, Төрийн банк, Хас банк, ХХБ/TDB) in user-facing strings; English equivalents are fine in code.
- **Currency**: Always MNT. Always integer values in the API (QPay does not use cents/sub-units — `1000` means ₮1,000). Display with the `₮` symbol or the suffix `MNT` in the UI.

## What this skill does not do

- **Open a QPay merchant account for them.** That requires an `ААН` (registered Mongolian business entity) or individual merchant registration with QPay. If they're not registered, point them to `assets/credentials-guide.md` and the QPay onboarding process. The skill helps once credentials exist or are imminent.
- **Handle subscriptions / recurring billing.** QPay has a recurring product but it's not in this skill's scope yet. If asked, mention that recurring requires separate QPay onboarding and a different API surface.
- **Replace international payment options.** If the dev wants to charge international customers in USD, QPay is the wrong tool — Lemon Squeezy, Paddle, or a Wyoming LLC + Stripe is the move. Surface this if they mention international customers, but stay focused on QPay for the MNT side.
