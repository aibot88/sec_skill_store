---
name: validate-contribution
description: >
  Validate geographic data contributions against the CSC database schema.
  Use this skill whenever you encounter a PR that adds, modifies, or deletes
  data in the contributions/ directory. Trigger on: validate, check, review,
  verify, audit, inspect, or assess any data contribution, PR review requests,
  schema compliance checks, field validation, or when someone says "is this
  correct", "check my data", "validate this", or "review my PR". Also use
  when asked about required fields, allowed values, or data format rules.
  Read schema-rules.md in this directory for the complete field specification.
---

## Validation Process

When validating a contribution, follow these steps in order:

### Step 1: Identify the Entity Type

Determine whether the contribution is for cities, states, or countries based on the file path or content structure.

### Step 2: Check for Auto-Managed Fields

The following fields must NOT be present in contributions (they are auto-managed):
- `id`
- `created_at`
- `updated_at`
- `flag`

If any are present, flag as an error and instruct the contributor to remove them.

### Step 3: Validate Required Fields

Read the `schema-rules.md` file in this skill's directory for the complete field specifications, constraints, and example records per entity type. Use it as the authoritative reference for all field validation.

**Cities require:** `name`, `state_id`, `state_code`, `country_id`, `country_code`, `latitude`, `longitude`
**States require:** `name`, `country_id`, `country_code`
**Countries require:** `name`

### Step 4: Validate Field Formats

- `country_code`: must be exactly 2 uppercase letters (ISO 3166-1 alpha-2)
- `latitude`: must be a decimal number between -90 and 90
- `longitude`: must be a decimal number between -180 and 180
- `name`: must be non-empty, max 255 characters (100 for countries)
- `wikiDataId`: must match pattern Q followed by digits (e.g., Q65)
- `state_id`, `country_id`: must be positive integers

### Step 5: Cross-Reference Validation

- Load the existing `countries.json` and `states.json` files
- Verify `country_id` exists in the countries data
- Verify `country_code` matches the ISO2 code of the referenced country
- For cities: verify `state_id` exists in states data AND belongs to the specified country
- For cities: verify `state_code` matches the code of the referenced state

### Step 6: Coordinate Plausibility

- Check that coordinates are within the geographic bounds of the specified country
- Flag coordinates that fall outside the country (may be valid for border cities)

### Step 7: Duplicate Detection

- Check for existing entries with the same name in the same state/country
- Check for entries within 5km of the new coordinates
- Report potential duplicates as warnings (they may be legitimate)

## Output Format

Present results as a clear validation checklist:

```
### Validation Results for [filename]

**Schema Compliance:**
- [PASS/FAIL] Required fields present
- [PASS/FAIL] No auto-managed fields included
- [PASS/FAIL] Field formats valid

**Cross-References:**
- [PASS/FAIL] country_id [X] exists ([country name])
- [PASS/FAIL] country_code "[XX]" matches country_id
- [PASS/FAIL] state_id [X] exists ([state name])
- [PASS/FAIL] state_code "[XX]" matches state_id

**Data Quality:**
- [PASS/WARN] Coordinates within country bounds
- [PASS/WARN] No duplicates detected

**Overall: [PASS / NEEDS CHANGES]**
```
