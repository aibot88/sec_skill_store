---
name: agentprivacy-perimeter-hardening
description: >
  Device security, OS hardening, network configuration, and physical
  security for 0xagentprivacy swordsman infrastructure. Activates when
  securing the execution environment beneath the cryptographic layer,
  designing supply chain integrity checks, hardening operating systems
  for agent execution, or building the physical and logical security
  foundation that cryptography assumes but does not provide.
  Triggers: "device security", "OS hardening", "supply chain",
  "firmware", "boot integrity", "network hardening", "physical security",
  "attack surface reduction", "secure boot", "endpoint hardening".
license: Apache-2.0
metadata:
  version: "5.0"
  category: "role"
  origin: "0xagentprivacy"
  author: "Mitchell Travers"
  affiliation: "0xagentprivacy, BGIN, First Person Network"
  status: "working_paper"
  equation_term: "P foundation — cryptography protects data; perimeter protects the cryptography"
  template_references: "soulbis, sentinel, ranger, warden, sith"
---

# PVM-V4 Skill — Perimeter Hardening

**Source:** Privacy Value Model V4 + Dark Forest Strategy + Defense-in-Depth Architecture
**Target context:** Endpoint security architects, device provisioning engineers, operational security practitioners, infrastructure hardening teams, supply chain security analysts
**Architecture:** [agentprivacy.ai](https://agentprivacy.ai) · **Sync:** [sync.soulbis.com](https://sync.soulbis.com) · **Contact:** mage@agentprivacy.ai

---

## What this is

Cryptography doesn't exist in a vacuum. A signing key stored in an enclave is only as secure as the device the enclave runs on. A privacy-preserving browser extension is only as secure as the OS it runs atop. A mixnet is only as private as the network it traverses.

Perimeter hardening is the discipline of securing everything beneath the cryptographic layer — the device, the firmware, the operating system, the network path, the physical environment. These are the layers cryptographers assume are secure when they prove their protocols correct. This skill is about making those assumptions true.

## The layer stack

Security descends through layers. Each layer must be secured for the layers above to function:

**Layer 6 — Application.** The swordsman agent, the browser extension, the wallet. Protected by boundary_enforcement, key_ceremony, crypto_zkp. These skills assume the lower layers are solid.

**Layer 5 — Runtime.** The execution environment: VM, container, process sandbox. Isolation between applications. Memory protection. Resource limits. The runtime prevents one compromised application from reaching another.

**Layer 4 — Operating system.** The kernel, the system libraries, the service daemons. The OS mediates all access to hardware. A compromised kernel sees everything above it. OS hardening reduces the attack surface to the minimum required for the swordsman's operation.

**Layer 3 — Firmware / BIOS / UEFI.** The code that runs before the OS boots. Firmware rootkits survive OS reinstallation. Secure boot chains ensure that only verified firmware loads, and only verified firmware loads verified OS images.

**Layer 2 — Hardware.** The CPU, memory, storage, network interfaces. Hardware implants (supply chain attacks) operate below all software defences. Hardware integrity verification and trusted supply chains are the defences at this layer.

**Layer 1 — Physical.** The room, the building, the jurisdiction. Physical access to hardware bypasses most electronic defences. Physical security — locks, access controls, tamper-evident packaging — is the foundation of the entire stack.

## OS hardening checklist

The swordsman's execution environment should follow minimal-surface principles:

**Remove unnecessary software.** Every installed package is attack surface. The swordsman's OS needs: the kernel, the agent runtime, cryptographic libraries, network stack. Nothing else. No desktop environment, no web browser (the Warden runs as a browser extension, not on the same machine), no development tools, no games.

**Disable unnecessary services.** Every listening port is an entry point. The swordsman's machine listens on: nothing, ideally. If network services are required, each is individually justified, firewall-restricted, and monitored.

**Mandatory access control.** SELinux, AppArmor, or equivalent. The swordsman process runs in a confined policy that limits its capabilities to exactly what it needs: read its key material, access the signing module, write to the audit log. Nothing else — even if the process is compromised, the MAC policy limits what the attacker can do.

**Filesystem encryption.** Full disk encryption with keys stored in hardware (TPM or equivalent). If the physical device is stolen, the data is inaccessible without the hardware key. LUKS on Linux, FileVault on macOS, BitLocker on Windows — the specific implementation matters less than the guarantee: data at rest is encrypted.

**Automatic updates.** Security patches applied within hours, not weeks. The swordsman's OS subscribes to security update channels and applies patches automatically for kernel and library vulnerabilities. Application updates (the swordsman agent itself) follow a more cautious path: verified, attested, tested before deployment.

**Logging and auditing.** Every system event is logged: process creation, network connections, file access, authentication attempts. Logs are append-only and integrity-protected (signed, or written to a remote log server the local machine cannot modify). The Sentinel monitors these logs for anomalies.

## Network hardening

**Firewall rules.** Default deny. Only explicitly permitted traffic passes. Inbound: nothing (or only the minimum required for the swordsman's protocol). Outbound: only connections to known, verified endpoints (mixnet entry nodes, blockchain nodes, VRC ceremony partners).

**DNS privacy.** DNS queries reveal browsing intent even when the content is encrypted. DNS-over-HTTPS (DoH) or DNS-over-TLS (DoT) to a trusted resolver. Better: local DNS resolution with a minimal root hints file, eliminating external DNS entirely for the swordsman's operations.

**Network segmentation.** The swordsman's machine is on a separate network segment from general-purpose devices. No lateral movement path exists from a compromised laptop to the swordsman's infrastructure. Ideally, physically separate network hardware.

**VPN / Tor as baseline.** All swordsman network traffic passes through a VPN or Tor. The swordsman's IP address is never directly visible to any counterparty. This is the metadata_resistance skill's network-layer implementation.

## Supply chain integrity

The most insidious attacks don't breach the perimeter — they arrive inside it, embedded in trusted components:

**Reproducible builds.** The swordsman agent's binary must be reproducibly buildable from source. Anyone can compile the source code and verify that the resulting binary matches the deployed one bit-for-bit. If the deployed binary doesn't match, it has been tampered with.

**Dependency verification.** Every library, every framework, every cryptographic implementation used by the swordsman is pinned to a specific version with a verified hash. Dependency updates are manually reviewed before acceptance. Typosquatting, dependency confusion, and backdoored updates are all supply chain attack vectors.

**Hardware provenance.** Where possible, the swordsman's hardware comes from verified supply chains with tamper-evident packaging. For the highest threat models: hardware is purchased anonymously, from random retail locations, to prevent targeted supply chain insertion.

**Firmware verification.** Secure boot verifies the firmware's signature against a known-good key. If the firmware has been modified, the boot process halts. The boot chain: hardware root of trust → firmware → bootloader → kernel → swordsman agent. Each link is verified before the next loads.

## Physical security tiers

Different threat models require different physical security:

**Tier 1 — Consumer.** The Person's personal device with standard consumer security: device PIN/biometric, encrypted storage, remote wipe capability. Sufficient for low-to-medium threat models. The swordsman operates as a protected process within the consumer OS.

**Tier 2 — Dedicated.** A dedicated device for sovereignty operations. No other use. Stored securely when not in use. No shared access. The swordsman operates on a hardened OS with the full checklist above.

**Tier 3 — Air-gapped.** The signing key never touches a networked device. All signing operations happen on an air-gapped machine. Transactions are constructed on a networked device, transferred to the air-gap (USB, QR code), signed, and transferred back. The most secure but most operationally burdensome. Reserved for master key operations.

**Tier 4 — Distributed.** No single physical location holds sufficient key material to operate. Shamir's Secret Sharing distributes key shares across geographically separated locations. Signing requires k-of-n physical locations to collaborate. The physical security of any single location is insufficient to compromise the system.

## The hardening-usability gradient

Every hardening measure reduces usability. Removing the desktop environment means no GUI. Air-gapping means manual transaction transfer. Network segmentation means physical infrastructure cost. The swordsman must navigate this gradient:

**Non-negotiable:** Encrypted storage, firewall default-deny, automatic security updates, reproducible builds. These are baseline measures with minimal usability impact.

**Strongly recommended:** Mandatory access control, full OS hardening, network segmentation. Higher usability cost but proportionate security gain for medium threat models.

**Threat-dependent:** Air-gapping, distributed key storage, anonymous hardware procurement. Reserved for high-threat environments where the adversary has state-level resources.

The armor_progression skill's tiered model applies here: the Person's perimeter hardening escalates with their threat level and sovereignty needs. A new Person starts at Tier 1. As their trust constellation grows and their privacy value increases, they graduate to harder perimeters.

## Connection to the equation

**P — protection foundation.** Perimeter hardening provides the physical substrate for P. The P term in V(π,t) assumes that cryptographic operations are not undermined by platform compromise. Perimeter hardening makes this assumption valid. P_effective = P_crypto × P_perimeter. If either factor approaches zero, effective protection collapses.

**h(τ) — platform integrity.** The integrity fraction h(τ) depends on the entire stack, not just the cryptographic layer. A compromised OS with perfect cryptography has h(τ) ≈ 0 because the platform cannot be trusted to execute the cryptography correctly. Perimeter hardening maintains the platform integrity that h(τ) measures.

**Dark forest alignment.** In the dark forest, any detectable signal attracts predators. Perimeter hardening minimises the signals the swordsman's infrastructure emits: no unnecessary network services (no listening ports to scan), no identifiable traffic patterns (VPN/Tor baseline), no distinctive hardware fingerprint (consumer-grade, common hardware). The hardened perimeter is invisible — and in the dark forest, invisibility is survival.

---

**Verify:** [agentprivacy.ai](https://agentprivacy.ai) · [sync.soulbis.com](https://sync.soulbis.com) · [github.com/mitchuski/agentprivacy-docs](https://github.com/mitchuski/agentprivacy-docs)
