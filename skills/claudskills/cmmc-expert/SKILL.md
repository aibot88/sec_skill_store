---
name: cmmc-expert
description: CMMC v2.0 expert for DoD contractors. Provides deep knowledge of Cybersecurity Maturity Model Certification including 5 levels, 14 domains, 171 practices, NIST 800-171 alignment, and C3PAO assessment preparation.
allowed-tools: Read, Glob, Grep, Write
---

# CMMC Expert

Deep expertise in Cybersecurity Maturity Model Certification (CMMC) v2.0 for Department of Defense contractors.

## Expertise Areas

### CMMC Program Overview

**Purpose**: Standardize cybersecurity across the Defense Industrial Base (DIB)
**Authority**: DFARS 252.204-7012, 7019, 7020, 7021
**Effective**: FY2025 implementation phase

**Key Changes from CMMC 1.0 to 2.0**:

- Streamlined from 5 to 3 levels
- Reduced from 320 to 171 practices (at Level 3)
- Aligned directly with NIST 800-171
- Simplified assessment requirements
- Added self-assessment path (Level 1)

### CMMC Levels

| Level | Name | Practices | Assessment | Frequency | Who Needs It |
|-------|------|-----------|------------|-----------|--------------|
| **Level 1** | Foundational | 17 | Self | Annual | FCI only |
| **Level 2** | Advanced | 110 | C3PAO | Triennial | CUI, most DIB |
| **Level 3** | Expert | 110+ | Government | Triennial | Critical CUI |

### 14 Domains

1. **Access Control (AC)** - 22 practices
   - Least privilege, separation of duties
   - Remote access control, session termination

2. **Asset Management (AM)** - 5 practices
   - Hardware/software inventory
   - Asset accountability and tracking

3. **Audit and Accountability (AU)** - 9 practices
   - Audit record creation and protection
   - Log review and analysis

4. **Awareness and Training (AT)** - 5 practices
   - Security awareness programs
   - Role-based training

5. **Configuration Management (CM)** - 9 practices
   - Baseline configurations
   - Change control processes

6. **Identification and Authentication (IA)** - 11 practices
   - User/device identification
   - Multi-factor authentication (MFA)
   - Password management

7. **Incident Response (IR)** - 8 practices
   - Incident handling capability
   - Tracking and reporting

8. **Maintenance (MA)** - 6 practices
   - Scheduled maintenance
   - Tool control, sanitization

9. **Media Protection (MP)** - 8 practices
   - Media control and sanitization
   - CUI marking and handling

10. **Personnel Security (PS)** - 4 practices
    - Background screening
    - Termination procedures

11. **Physical Protection (PE)** - 6 practices
    - Facility access control
    - Visitor management

12. **Recovery (RE)** - 3 practices
    - Backup and recovery
    - Redundancy planning

13. **Risk Management (RM)** - 7 practices
    - Risk assessments
    - Vulnerability scanning and remediation

14. **Security Assessment (CA)** - 5 practices
    - Assessment planning and execution
    - POA&M tracking

15. **Situational Awareness (SA)** - 4 practices (Level 3)
    - System monitoring
    - Information sharing

16. **System and Communications Protection (SC)** - 12 practices
    - Boundary protection
    - Cryptographic protection
    - Transmission security

17. **System and Information Integrity (SI)** - 9 practices
    - Flaw remediation
    - Malicious code protection

### NIST 800-171 Alignment

CMMC v2.0 is directly based on NIST Special Publication 800-171 "Protecting CUI in Nonfederal Systems"

**Mapping**:

- **Level 1**: 17 basic safeguarding practices (subset of 800-171)
- **Level 2**: All 110 practices from NIST 800-171 Rev 2
- **Level 3**: Level 2 + additional practices for critical programs

### Assessment Process

**C3PAO (Certified Third-Party Assessor Organization)**:

- DoD Accreditation Body oversight
- Independent assessment
- Standardized methodology
- Official CMMC certification

**Assessment Phases**:

1. **Pre-assessment**: Scope determination, SSP review
2. **On-site Assessment**: Evidence review, interviews, testing
3. **Post-assessment**: Report generation, scorecard
4. **Certification**: 3-year validity

**Scoring Criteria**:

- All practices must be implemented
- Must meet maturity level requirements
- Compensating controls evaluated case-by-case
- POA&M for minor gaps (limited)

### Data Types

**FCI (Federal Contract Information)**:

- Not classified, not CUI
- Provided by/generated for the government
- Under contract performance
- Example: Pricing, delivery schedules

**CUI (Controlled Unclassified Information)**:

- 125 CUI categories
- Export control (ITAR, EAR)
- Critical infrastructure
- Privacy information
- Example: Technical data, engineering drawings

**CUI Marking Requirements**:

- Banner markings required
- Category identification
- Dissemination controls

### Common Implementation Gaps

1. **MFA (IA.L2-3.5.7/.8)**:
   - Not implemented for all accounts
   - SMS-based MFA (inadequate)
   - Lack of phishing-resistant MFA

2. **Asset Inventory (AM.L2-3.4.1/.2)**:
   - Incomplete hardware/software inventory
   - No network diagram
   - Shadow IT not tracked

3. **Audit Logging (AU domain)**:
   - Insufficient log retention
   - No log review process
   - Missing audit events

4. **Incident Response (IR.L2-3.6.1)**:
   - No written IR plan
   - Plan not tested
   - No 72-hour DoD reporting process

5. **Configuration Management (CM domain)**:
   - No baseline configurations
   - Change control informal
   - Security settings not enforced

### System Security Plan (SSP)

**Required Documentation**:

- System description and boundaries
- Data flow diagrams
- Network architecture
- Practice implementation statements
- Policies and procedures
- POA&M for deficiencies

**NIST 800-171A Assessment Objectives**:

- Each practice has assessment objectives
- Determine, Examine, Interview, Test (DEIT)
- Evidence artifacts required

### Critical Success Factors

1. **Executive Support**: C-suite commitment and resources
2. **Scope Definition**: Clear CUI boundaries and enclaves
3. **Documentation**: Policies, procedures, diagrams current
4. **Technical Controls**: MFA, encryption, logging, monitoring
5. **Training**: All personnel aware of responsibilities
6. **Continuous Monitoring**: Ongoing compliance, not point-in-time

### POA&M (Plan of Action & Milestones)

**Acceptable for**:

- Minor gaps with clear remediation plan
- Resource constraints with executive approval
- Technology limitations with compensating controls

**Not Acceptable for**:

- Fundamental practice failures
- Multiple related gaps
- Level 2+ critical practices

**POA&M Requirements**:

- Specific remediation steps
- Resource allocation
- Milestone dates (typically <6 months)
- Compensating controls if applicable

### Cost Considerations

**Level 1 (Self-Assessment)**:

- $0 - $50K (consulting/tools)
- Annual submission to DoD

**Level 2 (C3PAO Assessment)**:

- Assessment: $50K - $200K+ (based on scope)
- Remediation: $100K - $500K+ (tooling, consulting)
- Triennial recertification

**Level 3 (Government Assessment)**:

- Similar to Level 2 but government-led
- Additional scrutiny and requirements

### Timeline

**Typical CMMC Journey**:

1. **Gap Assessment**: 2-4 weeks
2. **Remediation**: 6-18 months (varies widely)
3. **Pre-assessment Prep**: 1-2 months
4. **C3PAO Assessment**: 1-4 weeks
5. **Certification**: Immediate upon passing

### Resources

**Official Sources**:

- CMMC Accreditation Body (Cyber AB)
- DoD CMMC website
- NIST 800-171 Rev 2
- NIST 800-171A (Assessment Procedures)
- DFARS clauses 252.204-7012, 7019, 7020, 7021

**Key Publications**:

- CMMC Model v2.0
- CMMC Assessment Guide v2.0
- CMMC Scoping Guide
- NIST 800-171 Rev 2
- NIST 800-171A

## Capabilities

- CMMC level selection and scoping
- Practice-by-practice implementation guidance
- SSP development and review
- Gap assessment and remediation planning
- C3PAO assessment preparation
- POA&M development
- Evidence artifact collection
- NIST 800-171 mapping and compliance
- OSC (Office of the Under Secretary of Defense for Acquisition & Sustainment) platform guidance
- DIBCAC (Defense Industrial Base Collaborative Information Sharing Environment) integration
