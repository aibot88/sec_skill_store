---
name: test-chaos
description: Introduce controlled failures to test system resilience. Kill processes, cut network, fill disk. Use when testing fault tolerance, disaster recovery, or resilience.
license: MIT
metadata:
  author: vant
  version: "1.0"
---

# Test Chaos

> Resilience testing.

## When To Use

- Fault tolerance
- Disaster recovery
- System hardening

## Chaos Experiments

### 1. Kill Process

```bash
kill -9 <pid>
```

### 2. Cut Network

```bash
iptables -A INPUT -j DROP
```

### 3. Fill Disk

```bash
dd if=/dev/zero of=/full
```

### 4. Latency

```bash
tc qdisc add dev eth0 root netem delay 5000ms
```

---

## Tools

| Tool | Use |
|------|-----|
| Chaos Monkey | Netflix chaos |
| Litmus | Kubernetes chaos |
| Pumba | Docker chaos |
| Gremlin | Chaos as service |

---

## Output

```
## Chaos Test

| Experiment | Result | Recovery |
|------------|--------|---------|
| Kill DB | [FAIL→RECOVERED] | 5s |
| Net cut | [FAIL→RECOVERED] | 2s |
| Disk full | [HANDLED] | N/A |
```

**Role**: Chaos Engineer  
**Input**: Experiment  
**Output**: Resilience