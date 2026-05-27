---
name: vps-security-hardening
description: Audit and harden VPS security — fail2ban, SSH hardening, firewall setup
tags: [security, vps, ssh, fail2ban, linux, ubuntu]
origin: unknown
source_license: see upstream
language: en
---

# VPS Security Hardening

Audit and harden VPS security with fail2ban (brute-force protection), SSH hardening, and optional firewall setup.

## When to Use

- New VPS setup (initial hardening)
- Security audit requested
- SSH brute-force attacks detected
- User wants to "secure VPS" or "protect server"

## Prerequisites: Establishing SSH Access

**Before hardening, ensure you can SSH into the VPS.**

### If Password Auth is Disabled (PublicKey only)

VPS providers often disable password auth by default. You need to add your SSH key first.

#### Option 1: Via VPS Web Console (Recommended)

1. **Generate SSH key locally** (if not exists):
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N '' -C "user@machine"
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Login to VPS via web console** (provider dashboard → Console/Terminal)

3. **Add public key to VPS**:
   ```bash
   mkdir -p ~/.ssh
   echo "ssh-ed25519 AAAA... user@machine" >> ~/.ssh/authorized_keys
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

4. **Test from local machine**:
   ```bash
   ssh root@VPS_IP
   ```

#### Option 2: Via Provider Dashboard

Most providers (DigitalOcean, Vultr, Biznet, etc.) have "Add SSH Key" in dashboard:
- Copy public key (`cat ~/.ssh/id_ed25519.pub`)
- Paste into provider's SSH key management
- Rebuild/restart VPS (some providers require this)

#### Option 3: Enable Password Auth Temporarily

**Only if web console is unavailable:**

1. Login via web console
2. Edit SSH config:
   ```bash
   echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config.d/99-temp-password.conf
   systemctl reload sshd
   ```
3. SSH in with password, add your key
4. Remove temp config:
   ```bash
   rm /etc/ssh/sshd_config.d/99-temp-password.conf
   systemctl reload sshd
   ```

### Common Pitfall: sshpass with PublicKey-Only VPS

**Problem:** `sshpass -p 'password' ssh user@host` fails with "Permission denied (publickey)" even with correct password.

**Why:** VPS has `PasswordAuthentication no` in sshd_config — password auth is disabled at server level.

**Solution:** Use web console to add SSH key first (see Option 1 above).

## Workflow

### Phase 1: Security Audit

1. **Check running processes**
   ```bash
   ps aux --sort=-%mem | head -20
   systemctl list-units --type=service --state=running
   ```

2. **Check listening ports**
   ```bash
   sudo ss -tulpn
   sudo netstat -tulpn
   ```

3. **Check for rootkits/malware**
   ```bash
   # Hidden processes
   ps aux | wc -l
   ls /proc | grep -E '^[0-9]+$' | wc -l
   
   # Recent failed logins
   sudo grep "Failed password" /var/log/auth.log | tail -20
   ```

4. **Check user accounts**
   ```bash
   cat /etc/passwd | grep -E '/bin/(bash|sh)$'
   sudo lastlog
   ```

5. **Resource usage**
   ```bash
   free -h
   df -h
   uptime
   ```

### Phase 2: Install fail2ban

```bash
# Install
sudo apt-get update
sudo apt-get install -y fail2ban

# Enable and start
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Phase 3: Configure fail2ban

Create `/etc/fail2ban/jail.local`:

```ini
[DEFAULT]
bantime  = 3600        # Ban for 1 hour
findtime = 600         # Count failures in last 10 minutes
maxretry = 5           # Ban after 5 failures

[sshd]
enabled = true
port    = 22
logpath = /var/log/auth.log
maxretry = 5
```

Restart:
```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
```

### Phase 4: SSH Hardening

Create `/etc/ssh/sshd_config.d/99-hardening.conf`:

```conf
# Disable root login
PermitRootLogin no

# Enable public key auth
PubkeyAuthentication yes

# Disable empty passwords
PermitEmptyPasswords no

# Limit auth attempts
MaxAuthTries 3

# Disable X11 forwarding
X11Forwarding no

# Disable TCP forwarding
AllowTcpForwarding no

# Disable agent forwarding
AllowAgentForwarding no

# Set login grace time
LoginGraceTime 30

# Limit sessions
MaxSessions 2

# Strong ciphers only
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# Strong MACs only
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Strong key exchange
KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256
```

Test and reload:
```bash
sudo sshd -t
sudo systemctl reload sshd
```

### Phase 5: Verify

```bash
# fail2ban status
sudo fail2ban-client status sshd

# SSH config
sudo sshd -T | grep -E '(permitrootlogin|maxauthtries|x11forwarding)'

# Check banned IPs
sudo fail2ban-client get sshd banip
```

## Important: Password vs SSH Key Decision

**DO NOT automatically disable password authentication!**

### Check First

```bash
# Check if user has SSH keys
cat ~/.ssh/authorized_keys

# Check how user is currently connected
sudo grep "Accepted" /var/log/auth.log | tail -5
```

### Decision Logic

**If user logs in with PASSWORD:**
- ✅ Keep `PasswordAuthentication yes`
- ✅ fail2ban provides brute-force protection
- ⚠️ Disabling password = user gets locked out

**If user logs in with SSH KEY:**
- ✅ Can disable `PasswordAuthentication no`
- ✅ Maximum security (impossible to brute-force)

### User Preference Handling

**CRITICAL:** If user says "keep password" or "tanpa ssh key" or similar:
- ✅ Accept their decision
- ✅ Explain security is already good with fail2ban
- ❌ DO NOT keep suggesting SSH keys
- ❌ DO NOT say "but SSH keys are better"
- ❌ DO NOT make them feel their choice is wrong

**User knows their use case better than you:**
- They might need portability (login from anywhere)
- They might not want key file management
- They might prefer convenience over maximum security
- **Respect their decision and move on**

## Pitfalls

### 1. Disabling Password Auth Too Early

**Problem:** User currently uses password, you disable it, user gets locked out.

**Solution:**
- Always check current connection method first
- If password login, keep it enabled
- Only disable if user has working SSH keys AND explicitly requests it

### 2. Not Testing SSH Config

**Problem:** Invalid SSH config breaks SSH service, user locked out.

**Solution:**
- Always run `sudo sshd -t` before reload
- Use `reload` not `restart` (preserves current connections)

### 3. fail2ban Banning User's Own IP

**Problem:** User makes typo 5 times, gets banned.

**Solution:**
- Explain how to unban via VPS console: `sudo fail2ban-client unban --all`
- Consider whitelist for user's known IPs (optional)

### 4. Over-Suggesting Security Improvements

**Problem:** User made decision (e.g., keep password), you keep suggesting alternatives.

**Solution:**
- Present options ONCE with pros/cons
- User decides
- Accept decision and move on
- Don't revisit unless user asks

### 5. Cloud Provider Default Users

**Problem:** Deleting cloud provider system users (e.g., `lighthouse` on Tencent Cloud).

**Solution:**
- Check if user has sudo privileges: `sudo grep lighthouse /etc/sudoers.d/*`
- If yes, it's emergency access mechanism
- DO NOT delete (user might need it for recovery)

## Monitoring Commands

```bash
# Check fail2ban status
sudo fail2ban-client status sshd

# Check banned IPs
sudo fail2ban-client get sshd banip

# Unban IP
sudo fail2ban-client set sshd unbanip 1.2.3.4

# Watch SSH attacks live
sudo journalctl -u ssh -f

# Recent failed attempts
sudo grep "Failed password" /var/log/auth.log | tail -20
```

## Optional: UFW Firewall

Only enable if user requests or if no cloud-level firewall exists.

```bash
# Allow SSH first (CRITICAL!)
sudo ufw allow 22/tcp

# Allow other services
sudo ufw allow 1430/tcp  # Example: API port

# Enable
sudo ufw enable

# Check status
sudo ufw status
```

## Success Criteria

- ✅ fail2ban running and banning attackers
- ✅ SSH hardened (root disabled, limited attempts)
- ✅ User can still login (not locked out)
- ✅ Auto-updates enabled
- ✅ User satisfied with security level

## References

- `references/ssh-key-vs-password.md` — Detailed comparison and decision framework
- fail2ban docs: https://www.fail2ban.org/
- SSH hardening guide: https://www.ssh.com/academy/ssh/sshd_config
- Ubuntu security: https://ubuntu.com/security
