---
name: op-secret-template
description: Generate `op://` secret references for every field on a 1Password item. Output is ready to paste into a `.env` template.
argument-hint: "<item-name-or-id> [--vault <vault>]"
allowed-tools: Bash(op item get:*), Bash(op vault list:*)
---

# /op-secret-template

Given an item identifier, print every field on the item as a `KEY=op://...` line, suitable for a `.env` template used with `op run --env-file=.env -- ...`.

## Inputs

`$ARGUMENTS` — first arg is the item name or ID. Optionally `--vault <vault>` to scope the lookup.

## Steps

1. Fetch the item as JSON:
   ```bash
   op item get $ARGUMENTS --format=json
   ```

2. From the JSON, extract:
   - `vault.name` (call this `VAULT`)
   - `title` (call this `ITEM`)
   - For each entry in `fields[]`:
     - `label` (or `id` if no label)
     - `section.label` if `section` is present
     - `purpose` (`PASSWORD`, `USERNAME`, `NOTES`, etc.) if no label
     - `type` (`STRING`, `CONCEALED`, `URL`, `EMAIL`, `OTP`, `DATE`, `MONTH_YEAR`, `PHONE`)

3. Emit `KEY=op://VAULT/ITEM[/SECTION]/FIELD_LABEL` lines:
   - Skip fields with no value AND no label (CLI metadata).
   - Use the human-readable label for the secret reference.
   - Convert each label to a SCREAMING_SNAKE env var name on the left side.
   - For OTP fields, append `?attribute=otp` so it returns the current code.
   - For SSH private-key fields, append `?ssh-format=openssh`.

4. Wrap output in a fenced block with a header explaining usage:
   ```
   # Generated for item "ITEM" in vault "VAULT"
   # Use with: op run --env-file=.env -- <command>
   USERNAME=op://VAULT/ITEM/username
   PASSWORD=op://VAULT/ITEM/password
   API_KEY=op://VAULT/ITEM/Credentials/api_key
   TOTP=op://VAULT/ITEM/totp?attribute=otp
   ```

5. Note any field type that needs special handling (file attachments → `op read --out-file ...` not env, document attachments not supported).

## Edge cases

- **Multiple sections with same field name** → include the section name in the reference so the URI is unambiguous.
- **Whitespace in vault/item/field names** → wrap the whole reference value in single quotes in the output: `KEY='op://Acme Prod/My Item/api key'`.
- **Special characters that secret refs don't allow** → use the field's `id` instead of `label`, and note "(using ID instead of name due to special characters)".
- **Item is a Document or has file attachments** → emit a comment line explaining `op read --out-file` is needed instead of env loading.

## On failure

- Item not found → suggest `/op-find <query>` to locate it.
- Multiple matches (interactive only error) → tell the user to disambiguate by ID or `--vault`.
