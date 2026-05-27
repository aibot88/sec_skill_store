---
description: Map all applicable regulations based on jurisdiction, industry, data types, and customer requirements
---

# Regulatory Landscape

Map the full regulatory landscape for "$ARGUMENTS". Identify every applicable regulation based on where the business operates, what data it processes, what industries its customers serve, and what certifications those customers require.

## Prerequisites

None — this is a Phase 0 (Scope) skill.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference

2. **Jurisdiction mapping:**
   - Identify all jurisdictions where the business operates (headquarters, offices, data centers, customers)
   - Map each jurisdiction to its regulatory requirements (EU, US federal, US state, UK, APAC, etc.)
   - Note cross-border data transfer implications

3. **Data classification:**
   - Identify data types processed (PII, PHI, PCI, financial data, children's data, biometric data, etc.)
   - Map each data type to regulations that govern it
   - Note data residency and sovereignty requirements

4. **Industry and customer analysis:**
   - Identify industries the business serves (healthcare, finance, government, education, etc.)
   - Map industry-specific regulations (HIPAA, PCI DSS, FedRAMP, FERPA, etc.)
   - Document certifications customers require or request in sales cycles

5. **Regulation inventory:**
   - Create a comprehensive regulation inventory table with columns: regulation name, jurisdiction, data types covered, industry applicability, mandatory vs. customer-driven, enforcement status
   - Map each regulation to applicability criteria specific to "$ARGUMENTS"
   - Flag regulations with upcoming enforcement dates or recent changes

6. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/00-scope.md` with sections:
   - **Jurisdiction Map** — where the business operates and applicable jurisdictions
   - **Data Type Inventory** — data types processed and governing regulations
   - **Industry Requirements** — sector-specific regulations and customer demands
   - **Regulation Inventory Table** — full list of applicable regulations with applicability criteria
   - **Cross-Border Considerations** — data transfer and sovereignty requirements

## Output

The regulatory landscape analysis written to `.metapowers/compliance/$ARGUMENTS/00-scope.md`. Present a summary to the user highlighting:
- Total number of applicable regulations identified
- Top regulations by business impact
- Any surprising applicability findings
- Recommended next step: run `/compliance:compliance-priorities $ARGUMENTS`
