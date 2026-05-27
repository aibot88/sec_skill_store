---
name: tailscale-k8s
description: "Run Tailscale inside a Kubernetes pod reliably — persistent identity, SSH host keys, RBAC, stop/start without re-registration, and API-based device cleanup. Use when: configuring tailscaled in a pod or StatefulSet, debugging Tailscale device getting a -1 suffix on pod restart, setting up Tailscale SSH in a container, storing Tailscale state in a K8s secret, managing Tailscale devices via API from a CLI or script, or asking why SSH fingerprints change after pod restart. Trigger on phrases like 'tailscale in kubernetes', 'tailscale pod keeps getting -1', 'tailscale ssh in container', 'TS_KUBE_SECRET', 'tailscale state kube', 'tailscale device cleanup', 'ssh host key changes on pod restart'."
argument-hint: "state | ssh | rbac | cleanup | identity | troubleshoot"
---

# Tailscale in Kubernetes

Patterns for running `tailscaled` inside a Kubernetes pod with persistent identity, stable SSH host keys, and reliable device lifecycle management.

---

## Quick-Reference: Required Setup

| Concern | Solution |
|---|---|
| Node identity persists across pod restart | `--state=kube:<secret-name>` |
| SSH host keys persist (no fingerprint churn) | `--statedir=<pvc-backed-path>` |
| Tailscale can write its K8s secret | ServiceAccount with `get/create/update/patch` on secrets |
| No `-1` suffix on pod restart | Idempotent `tailscale up` — skip authkey if already authenticated |
| Clean device removal | Scale pod to 0, wait for termination, **then** call API |
| `stop` preserves identity; `delete` removes from tailnet | Never call API on stop — only on delete |

---

## tailscaled Startup Command

```bash
# Create dirs — statedir on the PVC so SSH host keys survive pod restarts
mkdir -p /var/run/tailscale
mkdir -p "/home/${USER}/.tailscale-state"
chown root:root "/home/${USER}/.tailscale-state"
chmod 700 "/home/${USER}/.tailscale-state"

tailscaled \
  --tun=userspace-networking \        # no /dev/net/tun needed in most k8s setups
  --state=kube:${TS_KUBE_SECRET} \   # auth state → K8s secret (persists across restarts)
  --statedir="/home/${USER}/.tailscale-state" \  # SSH host keys → PVC (persists)
  --socket=/var/run/tailscale/tailscaled.sock \
  &
TAILSCALED_PID=$!

# Wait for socket
for i in $(seq 1 30); do
  [ -S /var/run/tailscale/tailscaled.sock ] && break
  sleep 1
done
```

**Why both `--state` and `--statedir`?**

- `--state=kube:<name>` stores the Tailscale node key and auth credentials in a K8s Secret. Without this, the pod re-registers as a brand new device on every restart and gets a `-1`, `-2`, ... suffix.
- `--statedir` stores SSH host keys (and other local files). If this points to an `emptyDir`, the SSH host keys are regenerated on every restart, causing `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED` for every client. Point it to a PVC-backed path.

Without `--statedir`, tailscaled logs:
```
warning: unable to get SSH host keys, SSH will appear as disabled for this node: no var root for ssh keys
```

---

## Idempotent `tailscale up`

Never unconditionally pass `--authkey` on every pod start. If the pod already has valid state in the K8s secret, passing an authkey registers a **new** device instead of resuming, resulting in a `-1` suffix.

```bash
# Check if already authenticated before deciding whether to pass authkey
if tailscale status --peers=false &>/dev/null; then
  # Resuming — auth state loaded from K8s secret
  tailscale up \
    --hostname="${TS_HOSTNAME}" \
    --ssh \
    --accept-routes
else
  # First boot — register with authkey
  tailscale up \
    --authkey="${TS_AUTHKEY}" \
    --hostname="${TS_HOSTNAME}" \
    --ssh \
    --accept-routes
fi
```

---

## Required RBAC

`tailscaled` with `--state=kube:` needs to read and write a K8s Secret in its own namespace. Without this it crashes or falls back to file state.

```go
// ServiceAccount
&corev1.ServiceAccount{
    ObjectMeta: metav1.ObjectMeta{Name: "myapp-tailscale", Namespace: ns},
}

// Role
&rbacv1.Role{
    ObjectMeta: metav1.ObjectMeta{Name: "myapp-tailscale", Namespace: ns},
    Rules: []rbacv1.PolicyRule{
        {
            APIGroups: []string{""},
            Resources: []string{"secrets"},
            Verbs:     []string{"get", "create", "update", "patch"},
        },
        {
            APIGroups: []string{""},
            Resources: []string{"events"},
            Verbs:     []string{"get", "create", "patch"},
        },
    },
}

// RoleBinding — bind the Role to the ServiceAccount
```

Set `spec.serviceAccountName` on the PodSpec to the ServiceAccount name.

**Required env vars** on the container:

```yaml
- name: TS_KUBE_SECRET
  value: "tailscale-state-<instance-name>"   # unique per pod/StatefulSet
- name: TS_AUTHKEY
  valueFrom:
    secretKeyRef:
      name: myapp-ts-<instance-name>
      key: authkey
- name: TS_HOSTNAME
  value: "myapp-<instance-name>"
```

---

## Volume Setup

Only one emptyDir is needed — for the Tailscale socket. SSH host keys and auth state both go to persistent storage:

```yaml
# StatefulSet volumes
volumes:
- name: tailscale-run
  emptyDir: {}           # /var/run/tailscale — socket only, safe as emptyDir

# No tailscale-state emptyDir needed — statedir goes on the home PVC

volumeMounts:
- name: tailscale-run
  mountPath: /var/run/tailscale
- name: home                       # PVC
  mountPath: /home/<user>
  # ~/.tailscale-state/ lives here — created by init script
```

---

## Device Lifecycle: Stop vs Delete

### Stop (scale to 0, resume later)

Do **not** call the Tailscale API on stop. The device stays registered as offline. When the pod restarts:
- Auth state is loaded from the K8s secret → same node key → same device
- SSH host keys are loaded from the PVC → same fingerprint
- The pod rejoins the tailnet as the same device, no `-1` suffix

```bash
# Correct stop sequence
kubectl scale statefulset myapp-<name> --replicas=0 -n <ns>
# Wait for pod to terminate
# DO NOT call DELETE /api/v2/device/{id}
```

### Delete (permanent removal)

Must call the API **after** the pod is fully terminated. If you call it while `tailscaled` is still running, it immediately re-registers with the same hostname — the deletion has no effect.

```bash
# Correct delete sequence
kubectl scale statefulset myapp-<name> --replicas=0 -n <ns>
# Wait for pod to fully terminate — THEN call API
curl -s -u "${TS_API_KEY}:" \
  -X DELETE "https://api.tailscale.com/api/v2/device/${DEVICE_ID}"
# Now safe to delete the StatefulSet, Service, Secrets, etc.
```

### Go implementation

```go
// WRONG — calling API on stop breaks identity on resume
func runStop(...) {
    ScaleStatefulSet(ctx, cs, ns, name, 0)
    WaitForStopped(ctx, cs, ns, name)
    tsapi.DeleteDevice(apiKey, hostname)  // ← removes device; next start gets -1 suffix
}

// CORRECT — stop just scales down
func runStop(...) {
    ScaleStatefulSet(ctx, cs, ns, name, 0)
    WaitForStopped(ctx, cs, ns, name)
    // identity preserved in K8s secret + PVC
}

// CORRECT — delete: stop first, then API, then k8s cleanup
func runDelete(...) {
    ScaleStatefulSet(ctx, cs, ns, name, 0)
    WaitForStopped(ctx, cs, ns, name)   // MUST wait — pod gone before API call
    tsapi.DeleteDevice(apiKey, hostname)
    DeleteStatefulSet(...)
    DeleteSecrets(...)
}
```

---

## Tailscale API — Find and Delete Device by Hostname

```go
// GET /api/v2/tailnet/-/devices — find by hostname prefix, then DELETE
func DeleteDevice(apiKey, hostname string) (bool, error) {
    req, _ := http.NewRequest("GET",
        "https://api.tailscale.com/api/v2/tailnet/-/devices?fields=all", nil)
    req.SetBasicAuth(apiKey, "")

    resp, err := http.DefaultClient.Do(req)
    // ... parse JSON, find device where d.Hostname == hostname or HasPrefix
    // DELETE https://api.tailscale.com/api/v2/device/{id}
    // Returns (true, nil) on success, (false, nil) if not found, (false, err) on error
}
```

Use a prefix match (`strings.HasPrefix(d.Hostname, hostname)`) rather than exact match — Tailscale may register the device as `myapp-pi` or `myapp-pi-<suffix>` depending on history.

---

## Userspace Networking Notes

`--tun=userspace-networking` avoids the need for `/dev/net/tun` and `NET_ADMIN` capability, which makes it safe for unprivileged pods. Tradeoff: the pod **cannot establish direct WireGuard connections** and always relays through Tailscale DERP servers. This adds ~15–30ms latency vs direct connections.

If low latency matters (e.g. VS Code Remote SSH), use kernel-mode Tailscale with:
```yaml
securityContext:
  capabilities:
    add: ["NET_ADMIN"]
# and mount /dev/net/tun as a hostPath or use a device plugin
```

---

## Tailscale SSH ACL

To allow SSH without interactive browser auth prompts, add to your tailnet ACL:

```json
"ssh": [
  {
    "action": "accept",
    "src":    ["autogroup:member"],
    "dst":    ["tag:devpod"],           // or autogroup:self for personal tailnets
    "users":  ["autogroup:nonroot", "root"]
  }
]
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Device gets `-1` suffix on pod restart | Using file-based `--state` on emptyDir — use `--state=kube:<secret>` |
| SSH disabled: `no var root for ssh keys` | Missing `--statedir` or `--statedir` on emptyDir — point to PVC path |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED` | SSH host keys on emptyDir — move `--statedir` to PVC |
| API delete has no effect (device re-registers instantly) | Pod still running — scale to 0 and wait for termination first |
| Stop breaks Tailscale identity on resume | Calling `DELETE /api/v2/device/{id}` on stop — only call on delete |
| Always registers as new device even with kube state | Passing `--authkey` unconditionally — check `tailscale status` first |
| `tailscaled` CrashLoopBackOff: missing permissions | No RBAC for `TS_KUBE_SECRET` — add ServiceAccount/Role/RoleBinding |
| DERP relay, high latency (15–30ms) | Userspace networking can't do direct WireGuard — use kernel mode if latency matters |
