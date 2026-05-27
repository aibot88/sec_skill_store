---
name: windows-local-ai-services
description: Run local AI services on Windows — port binding, firewall, WSL2 networking, and common pitfalls.
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [Windows, WSL2, networking, ports, firewall, AI proxy, local services]
    related_skills: [llama-cpp, serving-llms-vllm]
origin: original
source_repo: kevinnft/ai-agent-skills
source_url: https://github.com/kevinnft/ai-agent-skills
source_license: MIT
language: en
---

# Windows Local AI Services

Running local AI services (enowxai, Ollama, LM Studio, vLLM, llama.cpp servers) on Windows has specific networking and port binding pitfalls. This skill covers setup, troubleshooting, and WSL2 cross-OS access.

## References

- `references/windows-port-restrictions.md` — Windows reserved port ranges and binding errors
- `references/headless-gui-apps.md` — Running GUI apps in headless WSL2 with Xvfb

## Common Pitfalls

### 1. **Port Binding Failures**

**Symptom**: Service crashes immediately with:
```
ERROR failed to start error="listen tcp4 127.0.0.1:1430: bind: An attempt was made to access a socket in a way forbidden by its access permissions."
```

**Root Cause**: Windows reserves certain port ranges for system services (Hyper-V, WinNAT, dynamic port allocation). Ports in these ranges cannot be bound by user applications.

**Fix**:
1. **Change the port** (easiest):
   ```powershell
   # Use a port outside reserved ranges (8000-9000 is usually safe)
   service start --port 8430
   ```

2. **Check reserved ranges**:
   ```powershell
   netsh int ipv4 show dynamicport tcp
   netsh int ipv4 show excludedportrange protocol=tcp
   ```

3. **Exclude a specific port** (risky, can conflict with system services):
   ```powershell
   netsh int ipv4 add excludedportrange protocol=tcp startport=1430 numberofports=1
   ```

**Never kill `svchost.exe`** — it's a Windows system service host. If `netstat` shows `svchost` using your target port, the port is reserved by Windows.

### 2. **WSL2 Cross-OS Networking**

**Symptom**: Service runs on Windows but WSL2 cannot connect via `localhost`.

**Root Cause**: WSL2 uses a virtualized network. `localhost` in WSL2 points to the WSL2 VM, not the Windows host.

**Fix**:
1. **Use Windows host gateway IP** from WSL2:
   ```bash
   # Get Windows host IP (usually 172.17.16.1, but can change on reboot)
   ip route show default | awk '{print $3}'
   
   # Test connection
   curl http://172.17.16.1:8430/v1/models
   ```

2. **Ensure Windows service listens on 0.0.0.0** (not 127.0.0.1):
   ```powershell
   # Check listening address
   netstat -ano | findstr :8430
   
   # Should show 0.0.0.0:8430, not 127.0.0.1:8430
   ```

3. **Configure Windows Firewall**:
   ```powershell
   # Allow inbound on the service port
   New-NetFirewallRule -DisplayName "AI Service Port 8430" -Direction Inbound -LocalPort 8430 -Protocol TCP -Action Allow
   ```

### 3. **Process Already Running**

**Symptom**: Service says "port already in use" but `Get-Process` shows nothing.

**Diagnosis**:
```powershell
# Find what's using the port
netstat -ano | findstr :8430

# Get process details (replace 1234 with PID from netstat)
Get-Process -Id 1234 | Select-Object Name, Id, Path
```

**Fix**:
- If it's your service from a previous run: kill it and restart
- If it's `svchost` or another system service: change your service's port

### 4. **Service Crashes Silently**

**Always check logs first**:
```powershell
# Common log locations
Get-Content ~\.service-name\service.log -Tail 50
Get-Content $env:APPDATA\service-name\logs\latest.log -Tail 50
```

**Common causes**:
- Missing dependencies (Python, CUDA/ROCm, Visual C++ Redistributable)
- Config file syntax errors
- Permission issues (try running PowerShell as Administrator)

## Setup Checklist

When setting up a new local AI service on Windows:

1. **Choose a safe port** (8000-9000 range recommended)
2. **Configure to listen on 0.0.0.0** (not 127.0.0.1) if WSL2 access needed
3. **Add Windows Firewall rule** for the port
4. **Test from Windows** first: `curl http://localhost:PORT/health`
5. **Test from WSL2**: `curl http://$(ip route show default | awk '{print $3}'):PORT/health`
6. **Save the gateway IP** or add to WSL2 `~/.bashrc`:
   ```bash
   export WINDOWS_HOST=$(ip route show default | awk '{print $3}')
   export AI_SERVICE_URL="http://$WINDOWS_HOST:8430/v1"
   ```

## Verification

After setup, verify cross-OS connectivity:

```bash
# From WSL2
GATEWAY_IP=$(ip route show default | awk '{print $3}')
echo "Windows host IP: $GATEWAY_IP"

# Test connection
curl -s http://$GATEWAY_IP:8430/v1/models | jq .

# If it works, save to config
echo "export AI_SERVICE_URL=http://$GATEWAY_IP:8430/v1" >> ~/.bashrc
```

## Rules

1. **Always check logs before guessing** — most errors are explicit
2. **Never kill system processes** (svchost, System, services.exe)
3. **Use gateway IP for WSL2 → Windows** — never `localhost`
4. **Verify firewall rules** before blaming the service
5. **Document the port** — save it in config files, not just command-line flags
