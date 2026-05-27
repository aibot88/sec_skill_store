---
name: telegram-bot-security-analysis
description: Reverse engineer and security-test Telegram bots — API analysis, callback interception, exploit discovery, and vulnerability documentation
tags: [telegram, security, reverse-engineering, bot-api, exploit-analysis]
origin: unknown
source_license: see upstream
language: en
---

# Telegram Bot Security Analysis

Comprehensive methodology for analyzing Telegram bots to discover security vulnerabilities, reverse engineer backend systems, and document exploits.

## Core Workflow

### 1. Initial Reconnaissance

**Login and Access:**
```python
from telethon import TelegramClient

API_ID = 94575  # Public Telegram API credentials
API_HASH = 'a3406de8d171bb422bb6ddf3bbd800e2'

client = TelegramClient('session_name', API_ID, API_HASH)
await client.start()
```

**Bot Information Gathering:**
- Bot ID and access hash
- Available commands
- Button callback data
- Web app URLs
- Inline query support

**Command Discovery:**
```python
commands = [
    '/help', '/menu', '/balance', '/wallet', '/deposit', 
    '/withdraw', '/profile', '/settings', '/admin', '/debug'
]

for cmd in commands:
    await client.send_message(bot, cmd)
    await asyncio.sleep(1)
```

**Conversation Dump:**
```python
all_msgs = await client.get_messages(bot, limit=200)

conversation = []
for msg in reversed(all_msgs):
    if msg.text:
        sender = "BOT" if msg.from_id == bot.id else "USER"
        conversation.append({
            "sender": sender,
            "time": msg.date.strftime('%Y-%m-%d %H:%M:%S'),
            "text": msg.text,
            "buttons": [[btn.text for btn in row] for row in msg.buttons] if msg.buttons else None
        })
```

### 2. Deep API Analysis

**Intercept Callback Data:**
```python
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

# Get button callback data
for button in msg.reply_markup.rows:
    if hasattr(button, 'data'):
        callback_data = button.data.decode('utf-8', errors='ignore')
        print(f"Callback: {callback_data}")
```

**Extract Web App URLs:**
```python
# Check for magic links, payment URLs, admin panels
for button in msg.buttons:
    if hasattr(button, 'button') and hasattr(button.button, 'url'):
        url = button.button.url
        if 'magic' in url or 'admin' in url or 'api' in url:
            print(f"Suspicious URL: {url}")
```

### 3. Backend Discovery

**Common Patterns:**
- Magic links: `/magic/go/{timestamp}/{user_id}`
- API endpoints: `/api/v1/...`, `/webhook/...`
- Admin panels: `/admin`, `/debug`, `/dashboard`

**Server Fingerprinting:**
```bash
curl -I http://target-ip:port/
# Look for: Server header, framework version, error messages
```

**Endpoint Fuzzing:**
```bash
# Common API paths
/api /api/v1 /api/wallet /api/balance /api/deposit
/admin /debug /magic /webhook /callback
```

### 4. Exploit Discovery

**Common Vulnerability Classes:**

1. **Premature Reward Distribution**
   - Reward given before full verification
   - No rollback mechanism
   - Missing state validation

2. **2FA/Authentication Bypass**
   - Temporary 2FA setup → get reward → disable 2FA
   - No continuous verification
   - App password validation gaps

3. **Race Conditions**
   - Rapid button clicking
   - Concurrent requests
   - State synchronization issues

4. **Payment Approval Manipulation**
   - Webhook triggers on payment approval
   - No completion verification
   - Abandoned registration still rewards

5. **Referral/Reward Gaming**
   - Self-referral loops
   - Multiple account exploitation
   - Reward duplication

### 5. Exploit Documentation

**Structure:**
```markdown
## Vulnerability Summary
- Type: [Premature Reward / Auth Bypass / Race Condition]
- Severity: [Low / Medium / High / Critical]
- Impact: [Financial loss / Data breach / Account takeover]

## Exploit Steps
1. Step-by-step reproduction
2. Required prerequisites
3. Expected outcome

## Technical Details
- Root cause analysis
- Code snippets (if available)
- Attack flow diagram

## Mitigation
- Recommended fixes
- Code patches
- Security best practices
```

## Tools and Techniques

### Telethon API Methods

**Message Inspection:**
```python
# Get conversation history
msgs = await client.get_messages(bot, limit=100)

# Filter for specific content
for msg in msgs:
    if msg.buttons:
        # Analyze button structure
    if msg.text and 'reward' in msg.text.lower():
        # Flag reward-related messages
```

**Callback Testing:**
```python
# Test crafted callback data
test_payloads = [
    b'admin', b'debug', b'wallet', b'claim',
    b'{"action":"deposit","amount":9999}',
]

for payload in test_payloads:
    try:
        result = await client(GetBotCallbackAnswerRequest(
            peer=bot, msg_id=msg.id, data=payload
        ))
        if result.message:
            print(f"Payload {payload} → {result.message}")
    except Exception as e:
        print(f"Payload {payload} → Error: {e}")
```

## Web API Security Testing

For testing backend APIs discovered during bot analysis:

### Validation Testing

**Test cases:**
```python
TEST_CASES = [
    # Negative values
    {"amount": -1, "price": 10},
    
    # Zero values
    {"amount": 0, "price": 10},
    
    # Float where integer expected
    {"amount": 0.1, "price": 10},
    
    # Very large numbers (integer overflow)
    {"amount": 2**63, "price": 10},
    
    # SQL injection
    {"amount": "1 OR 1=1", "price": 10},
    {"amount": "1'; DROP TABLE users--", "price": 10},
    
    # XSS injection
    {"amount": "<script>alert(1)</script>", "price": 10},
    
    # Null/undefined
    {"amount": None, "price": 10},
    
    # Type confusion
    {"amount": "1", "price": "10"},  # String instead of number
    {"amount": [1], "price": 10},    # Array instead of number
]
```

### Race Condition Testing

```python
import concurrent.futures

def send_request():
    return requests.post(
        "https://target.com/api/endpoint",
        headers=headers,
        json={"amount": 1, "price": 10},
        timeout=30
    )

# Send 5 simultaneous requests
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(send_request) for _ in range(5)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

success_count = sum(1 for r in results if r.status_code in (200, 201))

if success_count > 1:
    print(f"🚨 RACE CONDITION! {success_count} requests succeeded")
```

### Authentication Testing

```python
# Test 1: Expired token
headers = {"Authorization": "Bearer EXPIRED_TOKEN"}
resp = requests.get("https://target.com/api/me", headers=headers)
# Expected: 401 Unauthorized

# Test 2: Invalid token
headers = {"Authorization": "Bearer INVALID_TOKEN"}
resp = requests.get("https://target.com/api/me", headers=headers)
# Expected: 401 Unauthorized

# Test 3: Token from different user
headers = {"Authorization": "Bearer USER_A_TOKEN"}
resp = requests.get("https://target.com/api/users/USER_B_ID", headers=headers)
# Expected: 403 Forbidden
```

### Common Vulnerabilities

1. **Insufficient Input Validation** — API accepts invalid data (negative numbers, SQL injection)
2. **Race Conditions** — Multiple requests succeed when only one should
3. **Broken Authentication** — Can access resources without valid token
4. **Broken Authorization** — Can access other users' resources
5. **Business Logic Flaws** — Can perform actions that violate business rules

See `references/web-api-security-patterns.md` for comprehensive testing methodology.

## Backend Server Analysis

**Flask/Werkzeug Detection:**
```bash
# Check for debug mode
curl http://target/console
curl http://target/_debug_toolbar

# Common Flask paths
curl http://target/static/
curl http://target/admin/
```

**API Endpoint Discovery:**
```python
import requests

base_url = "http://target:port"
endpoints = [
    "/api/status", "/api/health", "/api/version",
    "/api/users", "/api/balance", "/api/transactions"
]

for endpoint in endpoints:
    r = requests.get(f"{base_url}{endpoint}")
    if r.status_code != 404:
        print(f"Found: {endpoint} → {r.status_code}")
```

## Real-World Example: GmailMiner Bot

**Vulnerability:** 2FA Temporary Setup Exploit

**Flow:**
1. Submit existing Gmail with wrong password
2. Bot requests 2FA verification
3. User enables 2FA on Google account
4. Submit 2FA code to bot
5. Generate App Password on Google
6. Submit App Password to bot
7. **Bot gives reward** (~9,654 NOT tokens ≈ $6.55)
8. User disables 2FA and deletes App Password
9. Account safe + reward kept

**Root Cause:**
```python
# Bot only checks 2FA at submission time
def verify_account(email, app_password):
    if has_2fa_enabled(email):  # ✓ Checked once
        give_reward(user_id)     # ✓ Reward given
    # ✗ No continuous monitoring
    # ✗ No rollback if 2FA disabled later
```

**Fix:**
```python
# Continuous verification + escrow
def verify_account(email, app_password):
    if has_2fa_enabled(email):
        escrow_reward(user_id, amount, days=30)
        schedule_verification(user_id, interval='daily')

@scheduler.task('interval', hours=24)
def verify_accounts():
    for account in active_accounts:
        if not has_2fa_enabled(account.email):
            revoke_reward(account.user_id)
```

## Best Practices

### When to Pivot from Automated to Manual Testing

**Signals that automated exploitation won't work:**
- All callback injections rejected (DATA_INVALID)
- No SQL errors despite injection attempts
- No backend server discovered
- No race condition success after 20+ attempts
- Bot responses are consistent and validated

**Next steps:**
1. **Document findings:** "No automated exploits found"
2. **Recommend manual testing:**
   - Deposit small amount of real crypto
   - Test business logic with real transactions
   - Analyze web app with GUI browser
   - Test cross-account interactions
3. **Focus on business logic:**
   - Timing bugs (order creation/cancellation)
   - Reward stacking (multiple promotions)
   - Client-side validation bypasses
   - Escrow/payment flow issues

**Example:** xRocket bot — after comprehensive automated testing found nothing, recommended manual testing of P2P market, cheques, and xJourney Wheel with real deposits.

### Ethical Guidelines

1. **Responsible Disclosure:**
   - Privately notify bot owner first
   - Give 30-90 days to fix
   - Only publish after fix deployed

2. **Testing Boundaries:**
   - Use test accounts only
   - Don't exploit for personal gain
   - Don't cause service disruption

3. **Legal Compliance:**
   - Respect Computer Fraud and Abuse Act (CFAA)
   - Follow platform Terms of Service
   - Document authorization if pentesting

### Documentation Standards

**Exploit Report Template:**
```markdown
# [Bot Name] Security Analysis

## Executive Summary
- Vulnerability type
- Severity rating
- Impact assessment

## Technical Details
- Root cause
- Attack vector
- Proof of concept

## Reproduction Steps
1. Detailed step-by-step
2. Screenshots/logs
3. Expected vs actual behavior

## Mitigation
- Recommended fixes
- Code patches
- Security improvements

## Timeline
- Discovery date
- Disclosure date
- Fix deployment date
```

## Common Pitfalls

1. **Assuming localhost works in WSL2:**
   - Use gateway IP from `ip route show default`
   - Windows services: `172.17.16.1` (not `localhost`)
   - Test with: `curl http://$(ip route show default | awk '{print $3}'):PORT`

2. **Forgetting CAPTCHA/anti-bot:**
   - Google registration requires manual interaction
   - Use Browserbase for Cloudflare bypass
   - Some flows can't be fully automated
   - Document manual steps clearly when automation fails

3. **Missing callback encryption:**
   - Telegram encrypts callback data
   - Can't inject arbitrary payloads without valid encryption
   - Focus on logic bugs, not crypto bypass

4. **Ignoring rate limits:**
   - Bots may have cooldowns
   - Too many requests → temporary ban
   - Space out testing

5. **Duplicate email/account detection:**
   - Many bots track submitted emails/accounts
   - Error: "Email already in database" or similar
   - Need fresh accounts for each test
   - Can't reuse same credentials multiple times

6. **Incomplete exploit testing:**
   - Document blockers clearly (CAPTCHA, phone verification, etc)
   - Provide manual steps when automation impossible
   - Test as far as possible, document remaining steps
   - Don't claim "exploit works" without full end-to-end test

7. **Assuming all bots are vulnerable:**
   - Well-funded/mature bots (e.g., xRocket) have strong security
   - Not every bot has exploitable bugs
   - Focus on business logic over technical exploits
   - If automated testing finds nothing, recommend manual testing with real transactions
   - Document "no exploits found" as valid outcome

8. **Telegram rate limiting (FloodWait):**
   - Rapid message sending triggers FloodWaitError
   - Error format: "A wait of N seconds is required"
   - Typical wait: 30-120 seconds after spam detection
   - Space out requests: 1-2 seconds between messages
   - For race condition testing: use multiple accounts, not rapid spam from one account
   - If FloodWait occurs: wait the full duration before retrying

## References

- Telegram Bot API: https://core.telegram.org/bots/api
- Telethon Documentation: https://docs.telethon.dev/
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- `references/gmailminer-exploit-2026-05-09.md` - Complete GmailMiner bot analysis with 2FA temporary setup exploit, backend discovery, and mitigation recommendations
- `references/xrocket-analysis-2026-05-09.md` - xRocket crypto wallet bot security assessment — well-secured bot with no automated exploits found, demonstrates importance of business logic testing over pure technical exploitation

## Related Skills

- `web-scraping` - For analyzing bot web apps
- `cloud-browser-automation` - For bypassing Cloudflare
- `credential-pooling-analysis` - For understanding bot economics
