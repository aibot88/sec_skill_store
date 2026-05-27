---
name: adult-payment-processor
description: Guide for adult content payment processor selection, merchant account application, compliance, webhook integration, and fallback strategies (CCBill, SegPay, AllSecure, Epoch, Telegram Stars, crypto)
context: |
  Stack context: Acaption (acaption.com), ATagger (atagger.com), ATagger Video — all blocked on adult payment processor approval. CCBill inquiry sent April 2026. AllSecure inquiry sent April 2026. SegPay/CCBill merchant applications pending. Consumer checkout is live via Telegram Stars. B2B/agency sales use Stripe manual invoicing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
argument-hint: "[product name] [processor name] [stage: research|application|integration|webhook]"
---

# Adult Payment Processor Skill

You are an expert on adult content payment processing. You know every major processor, their requirements, integration patterns, and fallback strategies.

## Processors — Ranked by Approval Ease

### 1. CCBill (most common for SaaS adult tools)
- **Approval**: 3–10 business days. Requires: gov ID, business registration docs, website screenshot, content description
- **Fees**: 10–14% + $0.30 per transaction for consumer; lower for high volume
- **Webhook**: `https://api.acaption.com/ccbill-webhook` — POST with `subscriptionId`, `clientAccnum`, `clientSubacc`, `timestamp`, `transactionId`, `billedAmount`, `billedCurrency`
- **Compliance docs needed**: 2257 statement (US performers), GDPR policy, privacy policy with data retention, explicit content policy
- **Contact**: milit@ccbill.com (technical), merchant-support@ccbill.com (onboarding)
- **Test environment**: sandbox.ccbill.com — test cards available after approval

### 2. SegPay (good for subscriptions)
- **Approval**: 5–14 days. US-based. Similar docs to CCBill
- **Fees**: 12–15% depending on chargeback history
- **Strong for**: recurring subscriptions, upsells, cascade billing
- **Weakness**: less developer-friendly API than CCBill

### 3. AllSecure / AllCard (EU-friendly)
- **Approval**: 7–21 days. EU company — easier for non-US merchants
- **Fees**: negotiated; typically 8–12%
- **Good for**: EU VAT handling, SEPA cards, GDPR compliance
- **Integration**: REST API with tokenisation; supports 3DS2

### 4. Epoch (legacy, still active)
- **Approval**: 5–10 days
- **Use case**: impulse purchases, one-click upsells
- **Weakness**: dated interface, lower conversion on mobile

### 5. Paxum (payouts, not consumer billing)
- **Not for checkout** — used for paying adult performers/affiliates, not for charging customers

---

## Fallback Strategies (while waiting for approval)

### Telegram Stars (ACTIVE — Acaption)
- Already live at acaption.com via Telegram bot
- Bot: immediate licence fulfilment on payment
- Limitation: requires Telegram account; not suitable for mainstream consumers
- Conversion: lower than web checkout but zero processor fees (Telegram takes 30%)

### Stripe B2B/Agency (ACTIVE)
- Manual invoice via Stripe — works for B2B/agency orders
- Stripe ToS prohibits consumer adult content sales but allows B2B software invoicing
- Keep this path active even after CCBill approval — agencies prefer invoices

### Crypto (optional fallback)
- BTCPay Server (self-hosted, no fees) or Coinbase Commerce
- 48h price lock for volatile assets
- Low conversion but zero chargebacks and zero processor dependency
- Add as "Pay with crypto" secondary button — do not make it primary

### Lemon Squeezy / Paddle (NOT viable for adult)
- Both explicitly prohibit adult content in ToS — do not apply

---

## Application Process — Step by Step

### CCBill Application
1. Go to ccbill.com/contact → "Become a Merchant"
2. Documents needed:
   - Valid government-issued photo ID
   - Business registration certificate or Articles of Incorporation
   - Screenshot of website with "Members Area" shown
   - Written description: "Software SaaS tool for adult content creators — captions/tags generation, no hosted media"
   - 2257 compliance statement (for tools that handle user-uploaded content)
3. After approval:
   - Get `clientAccnum` and `clientSubacc` from dashboard
   - Set webhook URL in CCBill Merchant Dashboard → Postback URL
   - Use FlexForms for checkout (hosted) or Direct Post API (integrated)
4. Test with sandbox before going live

### 2257 Statement (required for tools that process adult imagery)
Even for SaaS tools that don't host content, include:
```
This website is not a producer of sexually explicit content. We provide software tools to 
content creators. Records required by 18 U.S.C. §2257 are maintained by the primary producer.
```

---

## Webhook Integration Pattern (CCBill)

```python
# Flask example — adapt to your framework
@app.route('/ccbill-webhook', methods=['POST'])
def ccbill_webhook():
    data = request.form  # CCBill sends form-encoded POST
    
    event_type = data.get('eventType')  # 'NewSaleSuccess', 'Cancellation', 'RenewalSuccess'
    subscription_id = data.get('subscriptionId')
    amount = float(data.get('billedAmount', 0))
    currency = data.get('billedCurrency', 'USD')
    
    # Verify with CCBill's digest
    # md5(clientAccnum + clientSubacc + subscriptionId + transactionId + billedAmount + billedCurrency + salt)
    
    if event_type == 'NewSaleSuccess':
        # provision licence
        pass
    elif event_type == 'Cancellation':
        # revoke licence
        pass
    elif event_type == 'RenewalSuccess':
        # extend expiry
        pass
    
    return 'OK', 200
```

---

## Compliance Checklist (before going live)
- [ ] Age verification page / disclaimer on entry
- [ ] Clear adult content warning in metadata and footer
- [ ] Privacy policy with: data collected, retention period, GDPR rights, xAI/third-party disclosure
- [ ] Refund policy (3–7 day money-back is standard; CCBill requires one)
- [ ] 2257 statement (even for tool SaaS)
- [ ] DMCA takedown contact in footer
- [ ] No minors clause in Terms of Service

---

## Pricing Strategy for Adult SaaS
- **Higher than universal equivalents** — adult buyers expect premium pricing; ~20–30% above comparable universal tool
- **Annual vs monthly**: monthly has higher chargeback rate; push annual with 2-month discount
- **One-time licence**: lower chargeback risk than subscriptions; preferred by adult buyers who distrust recurring billing
- **Refund window**: 3 days visible in checkout reduces chargebacks (buyers who intend to dispute often give up if they see a refund path)
