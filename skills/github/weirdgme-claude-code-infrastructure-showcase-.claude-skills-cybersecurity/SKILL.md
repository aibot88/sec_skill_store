# Cybersecurity Skill

## Overview

Comprehensive cybersecurity guidance covering security architecture, threat modeling, security operations, incident response, application security, network security, cloud security, identity and access management, cryptography, security testing, and compliance.

## When to Use This Skill

This skill should be activated when:
- Designing security architectures
- Implementing security controls
- Conducting threat modeling
- Setting up security operations
- Responding to security incidents
- Securing applications and APIs
- Implementing network security
- Securing cloud environments
- Managing identity and access
- Implementing cryptographic solutions
- Performing security testing
- Achieving security compliance

## Core Security Domains

### 1. Security Architecture & Design

**Principles:**
- Zero Trust Architecture
- Defense in Depth
- Least Privilege
- Separation of Duties
- Fail Secure
- Security by Design

**Architecture Patterns:**
- Segmented network architecture
- Micro-segmentation
- Perimeter security
- Defense in depth layering
- Security zones and enclaves
- DMZ architecture
- Bastion host patterns

### 2. Threat Modeling & Risk Management

**Frameworks:**
- STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
- PASTA (Process for Attack Simulation and Threat Analysis)
- DREAD (Damage, Reproducibility, Exploitability, Affected Users, Discoverability)
- OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation)

**Process:**
1. Identify assets
2. Identify threats
3. Assess vulnerabilities
4. Determine risk
5. Implement mitigations
6. Validate and monitor

### 3. Security Operations (SecOps)

**Key Components:**
- Security Operations Center (SOC)
- Security Information and Event Management (SIEM)
- Security Orchestration, Automation, and Response (SOAR)
- Intrusion Detection/Prevention Systems (IDS/IPS)
- Endpoint Detection and Response (EDR)
- Extended Detection and Response (XDR)

**Processes:**
- Continuous monitoring
- Log aggregation and analysis
- Threat intelligence integration
- Alert triage and investigation
- Incident escalation
- Threat hunting
- Vulnerability management
- Patch management

### 4. Incident Response

**Phases:**
1. **Preparation:** IR plan, team, tools, training
2. **Identification:** Detect and determine scope
3. **Containment:** Short-term and long-term containment
4. **Eradication:** Remove threat and vulnerabilities
5. **Recovery:** Restore systems to normal
6. **Lessons Learned:** Post-incident review

**Key Artifacts:**
- Incident Response Plan
- Playbooks/Runbooks
- Communication plan
- Evidence handling procedures
- Chain of custody documentation
- Post-incident reports

### 5. Application Security (AppSec)

**Secure Development:**
- Secure SDLC (SSDLC)
- Security requirements
- Threat modeling in design
- Secure coding practices
- Code review
- Security testing

**Security Testing:**
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Interactive Application Security Testing (IAST)
- Software Composition Analysis (SCA)
- Penetration testing
- Bug bounty programs

**Common Vulnerabilities:**
- OWASP Top 10
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Insecure deserialization
- Security misconfiguration
- Broken authentication
- Sensitive data exposure

### 6. Network Security

**Controls:**
- Firewalls (next-gen, web application)
- Network segmentation
- VLANs and VXLANs
- VPN (IPSec, SSL/TLS)
- Network Access Control (NAC)
- Intrusion Detection/Prevention
- DDoS protection
- DNS security (DNSSEC)

**Monitoring:**
- Network traffic analysis
- NetFlow/sFlow analysis
- Packet capture and analysis
- Anomaly detection
- Threat intelligence feeds

### 7. Cloud Security

**Shared Responsibility Model:**
- Cloud provider responsibilities
- Customer responsibilities
- Different models: IaaS, PaaS, SaaS

**Cloud Security Controls:**
- Cloud Security Posture Management (CSPM)
- Cloud Workload Protection Platform (CWPP)
- Cloud Access Security Broker (CASB)
- Secure configuration
- Identity and access management
- Encryption (at-rest, in-transit)
- Key management
- Logging and monitoring
- Compliance validation

**Cloud-Specific Threats:**
- Misconfigured storage buckets
- Excessive IAM permissions
- Unencrypted data
- Exposed secrets
- Vulnerable container images
- Supply chain attacks

### 8. Identity & Access Management (IAM)

**Core Concepts:**
- Authentication vs Authorization
- Single Sign-On (SSO)
- Multi-Factor Authentication (MFA)
- Privileged Access Management (PAM)
- Identity Federation
- Just-In-Time (JIT) access
- Zero Trust Network Access (ZTNA)

**Technologies:**
- Active Directory / Azure AD
- LDAP
- SAML 2.0
- OAuth 2.0 / OpenID Connect
- Kerberos
- RADIUS
- TACACS+

**Best Practices:**
- Principle of least privilege
- Regular access reviews
- Strong password policies
- MFA enforcement
- Service account management
- Privileged account monitoring
- Identity lifecycle management

### 9. Cryptography

**Fundamentals:**
- Symmetric encryption (AES, ChaCha20)
- Asymmetric encryption (RSA, ECC)
- Hash functions (SHA-256, SHA-3)
- Digital signatures
- Message Authentication Codes (MAC)
- Key derivation functions (KDF)

**Implementations:**
- TLS/SSL configuration
- Certificate management
- Public Key Infrastructure (PKI)
- Hardware Security Modules (HSM)
- Key Management Systems (KMS)
- Encryption key rotation
- Perfect Forward Secrecy (PFS)

**Post-Quantum Cryptography:**
- NIST PQC candidates
- Hybrid approaches
- Migration planning

### 10. Security Testing & Assessment

**Types:**
- Vulnerability Assessment
- Penetration Testing (black box, white box, gray box)
- Red Team Exercises
- Purple Team Exercises
- Bug Bounty Programs
- Security Audits
- Compliance Assessments

**Methodologies:**
- OWASP Testing Guide
- PTES (Penetration Testing Execution Standard)
- OSSTMM (Open Source Security Testing Methodology Manual)
- NIST SP 800-115

**Tools:**
- Vulnerability scanners (Nessus, Qualys, OpenVAS)
- Web app scanners (Burp Suite, OWASP ZAP)
- Network scanners (Nmap, Masscan)
- Exploitation frameworks (Metasploit)
- Password crackers (John, Hashcat)
- Social engineering (GoPhish)

### 11. Compliance & Governance

**Frameworks:**
- NIST Cybersecurity Framework (CSF)
- ISO/IEC 27001/27002
- CIS Controls
- COBIT
- NIST SP 800-53
- PCI DSS
- HIPAA Security Rule
- GDPR
- SOC 2
- FedRAMP
- CMMC

**Key Activities:**
- Policy development
- Standards documentation
- Control implementation
- Compliance monitoring
- Audit preparation
- Evidence collection
- Risk assessments
- Gap analysis

## Security by Domain

### Commercial/Enterprise Security
- Corporate network security
- Endpoint protection
- Email security
- Data loss prevention (DLP)
- Insider threat programs
- Security awareness training
- Third-party risk management
- Supply chain security

### Government/Cleared Security
- Classified information handling
- SCIF security requirements
- TEMPEST protection
- Cross-domain solutions
- Secure communications (HAIPE, COMSEC)
- Personnel security (clearances)
- Physical security integration
- Continuous monitoring programs

### Cloud-Native Security
- Container security
- Kubernetes security
- Serverless security
- API security
- DevSecOps integration
- Secrets management
- Service mesh security
- Infrastructure as Code security

## Common Security Patterns

### 1. Zero Trust Implementation
```
┌─────────────────────────────────────────┐
│         Zero Trust Architecture         │
├─────────────────────────────────────────┤
│ • Verify explicitly (every access)      │
│ • Least privilege access                │
│ • Assume breach                         │
│                                         │
│ Components:                             │
│ ├─ Identity Provider (IdP)             │
│ ├─ Policy Decision Point (PDP)         │
│ ├─ Policy Enforcement Point (PEP)      │
│ ├─ Continuous monitoring               │
│ └─ Analytics and threat intelligence   │
└─────────────────────────────────────────┘
```

### 2. Defense in Depth Layers
```
┌─────────────────────────────────────────┐
│ Layer 1: Physical Security             │
├─────────────────────────────────────────┤
│ Layer 2: Network Perimeter             │
├─────────────────────────────────────────┤
│ Layer 3: Network Segmentation          │
├─────────────────────────────────────────┤
│ Layer 4: Endpoint Security             │
├─────────────────────────────────────────┤
│ Layer 5: Application Security          │
├─────────────────────────────────────────┤
│ Layer 6: Data Security                 │
├─────────────────────────────────────────┤
│ Layer 7: Security Monitoring           │
└─────────────────────────────────────────┘
```

### 3. Incident Response Workflow
```
Detection → Triage → Investigation → Containment →
Eradication → Recovery → Lessons Learned →
Update Defenses → Monitor
```

## Integration with Other Skills

- **devsecops**: Security in CI/CD pipelines, compliance automation
- **cloud-engineering**: Cloud security architecture, CSPM
- **infrastructure-architecture**: Secure architecture design, threat modeling
- **network-engineering**: Network security controls, segmentation
- **platform-engineering**: Container/K8s security, secrets management
- **observability-engineering**: Security monitoring, SIEM integration
- **sre**: Incident response, security monitoring

## Resources

See the `resources/` directory for detailed guides on:
- Security architecture patterns
- Threat modeling guides
- Incident response playbooks
- Security testing methodologies
- Cryptography implementation guides
- Compliance frameworks
- Security tools and technologies

## Quick Reference

### Security Assessment Questions
1. What assets are we protecting?
2. What are the threats?
3. What are the vulnerabilities?
4. What is the risk level?
5. What controls are in place?
6. What is the residual risk?
7. Are we compliant with requirements?
8. How do we detect incidents?
9. How do we respond?
10. How do we improve?

### Common Security Acronyms
- CIA: Confidentiality, Integrity, Availability
- AAA: Authentication, Authorization, Accounting
- IDS/IPS: Intrusion Detection/Prevention System
- SIEM: Security Information and Event Management
- SOAR: Security Orchestration, Automation, and Response
- EDR: Endpoint Detection and Response
- XDR: Extended Detection and Response
- CASB: Cloud Access Security Broker
- CSPM: Cloud Security Posture Management
- CWPP: Cloud Workload Protection Platform
- PAM: Privileged Access Management
- ZTNA: Zero Trust Network Access
- MFA: Multi-Factor Authentication
- SSO: Single Sign-On

---
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATED: cybersecurity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


**Remember:** Security is not a product, it's a process. Continuous improvement and adaptation are essential.
