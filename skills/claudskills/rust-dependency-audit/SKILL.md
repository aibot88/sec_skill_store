---
name: rust-dependency-audit
description: "Audit Rust dependencies for vulnerabilities, license compliance, supply chain integrity, and freshness using cargo-audit, cargo-deny, cargo-vet, and cargo-outdated. Use whenever the user asks about dependency auditing, vulnerability scanning, license checks, supply chain verification, crate freshness, or says 'cargo outdated' or 'cargo update'. Also use before any Rust crate release. Do NOT use for Rust tooling guidance on refactoring, profiling, or benchmarking (use rust-sota-arsenal instead)."
allowed-tools: Read, Grep, Bash, WebSearch, WebFetch
---

# Rust Dependency Audit

Comprehensive dependency audit workflow using four complementary tools: freshness checking, vulnerability scanning, license/advisory compliance, and supply chain verification.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## CRITICAL: Web-Verify Before Upgrade Decisions

**Always check crates.io for latest versions before recommending upgrades.** Static docs go stale; the crates.io API is ground truth.

1. **Before upgrading a crate**: Check what version is current and what it depends on

   ```
   WebFetch: https://crates.io/api/v1/crates/{crate_name}
   Prompt: "What is the latest version? List recent versions and their dependencies."
   ```

2. **Before ignoring a vulnerability**: Verify whether a patched version exists

   ```
   WebSearch: "{advisory_id} {crate_name} fix patch"
   ```

3. **Check compatibility chains**: When crate A depends on crate B, verify both latest versions are compatible

   ```
   WebFetch: https://crates.io/api/v1/crates/{crate_name}/{version}/dependencies
   Prompt: "What version of {dependency} does this require?"
   ```

4. **Fallback: Firecrawl scrape** (if WebFetch fails — JS-heavy pages, rate limits, incomplete data):

   ```bash
   curl -s -X POST http://littleblack:3002/v1/scrape \
     -H "Content-Type: application/json" \
     -d '{"url": "https://crates.io/crates/{crate_name}", "formats": ["markdown"], "waitFor": 0}' \
     | jq -r '.data.markdown'
   ```

   Requires Tailscale connectivity. See `/devops-tools:firecrawl-research-patterns` for full API reference.

## When to Use

- Before a release (full audit pipeline)
- After `cargo update` (verify no new vulnerabilities)
- CI pipeline setup (automated dependency checks)
- License compliance review (open source projects)
- Supply chain security assessment

## Four-Tool Audit Workflow

Run in this order — each tool catches different issues:

```bash
# 1. Freshness — what's outdated?
cargo outdated

# 2. Vulnerabilities — any known CVEs?
cargo audit

# 3. Licenses + Advisories — compliance check
cargo deny check

# 4. Supply Chain — who audited these crates?
cargo vet
```

### Quick Assessment

```bash
# One-liner: run all four (stop on first failure)
cargo outdated && cargo audit && cargo deny check && cargo vet
```

## Freshness: Finding Outdated Dependencies

Three tools for different needs:

| Tool                         | Install                        | Purpose                                                  | Best For            |
| ---------------------------- | ------------------------------ | -------------------------------------------------------- | ------------------- |
| `cargo-outdated`             | `cargo install cargo-outdated` | Full outdated report with compatible/latest versions     | Comprehensive audit |
| `cargo-upgrades`             | `cargo install cargo-upgrades` | Lightweight — only shows incompatible (breaking) updates | Quick check         |
| `cargo upgrade` (cargo-edit) | `cargo install cargo-edit`     | Actually updates `Cargo.toml` versions                   | Performing updates  |

```bash
# Show all outdated deps (compatible + incompatible)
cargo outdated --root-deps-only

# Show only breaking updates needed
cargo upgrades

# Actually update Cargo.toml (dry run first)
cargo upgrade --dry-run
cargo upgrade --incompatible

# Nightly: native cargo support (experimental)
cargo +nightly update --breaking
```

**Recommendation**: Use `cargo-upgrades` for quick checks, `cargo-outdated` for full audits, `cargo upgrade` (cargo-edit) when ready to actually update.

See [cargo-outdated reference](./references/cargo-outdated-guide.md).

## Security: Vulnerability Scanning

### cargo-audit (RUSTSEC Database)

```bash
# Scan for known vulnerabilities
cargo audit

# Auto-fix where possible (updates Cargo.lock)
cargo audit fix

# Binary scanning (audit compiled binaries)
cargo audit bin ./target/release/my-binary

# Custom config (ignore specific advisories)
# Create audit.toml:
```

```toml
# audit.toml
[advisories]
ignore = [
    "RUSTSEC-YYYY-NNNN",  # Reason for ignoring
]
```

See [cargo-audit reference](./references/cargo-audit-guide.md).

### cargo-deny (Advisories + More)

cargo-deny's advisory check complements cargo-audit with additional sources:

```bash
# Check advisories only
cargo deny check advisories

# All checks (advisories + licenses + bans + sources)
cargo deny check
```

See the License section below for full cargo-deny configuration.

## License: Compliance Checking

### cargo-deny License Check

```toml
# deny.toml
[licenses]
allow = [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-3.0",
]
confidence-threshold = 0.8

[[licenses.clarify]]
name = "ring"
expression = "MIT AND ISC AND OpenSSL"
license-files = [{ path = "LICENSE", hash = 0xbd0eed23 }]
```

```bash
# Check licenses
cargo deny check licenses

# Generate deny.toml template
cargo deny init
```

See [cargo-deny reference](./references/cargo-deny-guide.md).

## Supply Chain: Audit Verification

### cargo-vet (Mozilla)

cargo-vet tracks which crates have been audited and by whom:

```bash
# Check supply chain status
cargo vet

# Audit a specific crate (certify you've reviewed it)
cargo vet certify <crate> <version>

# Import audits from trusted organizations
cargo vet trust --all mozilla
cargo vet trust --all google

# See what needs auditing
cargo vet suggest
```

Key files:

- `supply-chain/audits.toml` — Your audits
- `supply-chain/imports.lock` — Imported audits
- `supply-chain/config.toml` — Trusted sources

See [cargo-vet reference](./references/cargo-vet-guide.md).

## Unsafe Code: Dependency Safety Audit

### cargo-geiger

cargo-geiger quantifies unsafe code usage across your entire dependency tree:

```bash
# Quick check: which deps forbid unsafe? (fast, no compilation)
cargo geiger --forbid-only

# Full audit: count unsafe blocks per crate
cargo geiger

# Output as ratio (for CI/scripting)
cargo geiger --forbid-only --output-format ratio

# Markdown report
cargo geiger --output-format markdown > unsafe-report.md
```

Key flags:

- `--forbid-only`: Fast mode — only checks `#![forbid(unsafe_code)]` (no compilation)
- `--output-format`: `ratio`, `markdown`, `ascii`, `json`
- `--all-features`: Check with all features enabled

See [cargo-geiger reference](./references/cargo-geiger-guide.md).

## Combined CI Workflow (GitHub Actions)

```yaml
name: Dependency Audit
on:
  pull_request:
  schedule:
    - cron: "0 6 * * 1" # Weekly Monday 6am

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: cargo-audit
        run: |
          cargo install cargo-audit
          cargo audit

      - name: cargo-deny
        uses: EmbarkStudios/cargo-deny-action@v2

      - name: cargo-vet
        run: |
          cargo install cargo-vet
          cargo vet

      - name: cargo-geiger
        run: |
          cargo install cargo-geiger
          cargo geiger --forbid-only

      - name: cargo-outdated
        run: |
          cargo install cargo-outdated
          cargo outdated --root-deps-only --exit-code 1
```

## Reference Documents

- [cargo-audit-guide.md](./references/cargo-audit-guide.md) — Vulnerability scanning
- [cargo-deny-guide.md](./references/cargo-deny-guide.md) — License + advisory compliance
- [cargo-outdated-guide.md](./references/cargo-outdated-guide.md) — Freshness + alternatives
- [cargo-vet-guide.md](./references/cargo-vet-guide.md) — Supply chain audit
- [cargo-geiger-guide.md](./references/cargo-geiger-guide.md) — Unsafe code quantification

## Troubleshooting

| Problem                             | Solution                                                    |
| ----------------------------------- | ----------------------------------------------------------- |
| `cargo audit` stale database        | Run `cargo audit fetch` to update RUSTSEC DB                |
| `cargo deny` false positive license | Add `[[licenses.clarify]]` entry in `deny.toml`             |
| `cargo vet` too many unaudited      | Import trusted org audits: `cargo vet trust --all mozilla`  |
| `cargo outdated` shows yanked       | Run `cargo update` first to refresh `Cargo.lock`            |
| Private registry crates             | Configure `[sources]` in `deny.toml` for private registries |
| Workspace vs single crate           | Most tools support `--workspace` flag                       |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
