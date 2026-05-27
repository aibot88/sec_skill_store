---
name: atlas-state
description: >
  Instant orientation skill for the Atlas 330 / atlas_core project. Use this skill at
  the start of ANY session involving Atlas development, research, scripting, graph work,
  dataset work, visualization, or philosophical/doctrinal writing. Also trigger when the
  user mentions: kernel.py, npu_engine, field_state, nakshatra, tithi, graha, devi,
  raga, corpus, relations, datasets, routes, S-layers, hexfield, toroidal field,
  Bandhu, sound, jyotisha, wave field, chladni, or any Atlas engine by name.
  Read before touching anything.
---

# Atlas State Skill

## What Atlas Is

**Atlas 330** is a Vedic cosmological field computer running as a Flask kernel (`kernel.py`)
on a van-mounted Intel NUC called `kanjira` at `~/atlas_core/`. It integrates jyotish,
biodynamic agriculture, sacred geometry, Ayurveda, Gaudiya Vaishnava knowledge systems,
and NPU-powered relational graph computation into a unified living platform.

The guiding principle: **everything is a projection of the cosmological field state.**
Every API endpoint, every display, every sound event derives from `kernel.field_state()`.
Nothing cosmological is hardcoded.

---

## Repository Structure (as of April 22, 2026)

```
atlas_core/                        Active computation repo
  kernel.py                        Flask entry — 8,404 lines, 147 @app.route
  npu_engine/                      238 Python files across 15+ subdirectories
    jyotisha_engine.py             Swiss Ephemeris chart + wave field (Apr 16)
    jyotish_utils.py               Rashi/graha normalization, CSV loaders
    datasets.py                    Shared CSV/JSON loader, all data access
    build_field_state.py           FieldState construction pipeline
    graph_engine.py                GraphEngine (17,612 entities, 13,304 edges)
    toroidal_field.py              Toroidal θ/φ coordinates (OpenVINO NPU)
    pasaka_engine.py               Pasaka dice oracle
    field/                         34 derive_*() engines (goloka, trajectory, etc.)
    engines/                       9 ZoneEngine subclasses + base
    renderers/                     figure_renderer, species_renderer
    sound/                         22 files — full audio pipeline, OSC bridge
    rhythm/                        13 files — tala, theka, tihai, layakari
    vocal/                         11 files — bhava, gamaka, phoneme, svara
    mix/                           11 files — per-nakshatra/guna/deity mix
    sympathetic/                   4 files — string model
    routes/                        8 blueprints (112 routes total)
      jyotish_bp.py                /jyotish/* (10 routes, Apr 16)
      sound_bp.py                  /sound/* (26 routes)
      plants_bp.py                 /plants/* (17 routes)
      system_bp.py                 /system/* (25 routes)
      corpus_bp.py, reading_bp.py, render_bp.py, symbols_bp.py
    geometry/, core/, zones/, time/, text/, system/, game/, nature/, ui/
  datasets/                        240 CSV + 765 JSON across 42 domains
    astro/                         16 CSV (nakshatra, tithi, graha, rashi)
    cosmology/                     20 CSV (devi, deity, goloka, yantra geometry)
    jyotish/                       5 CSV + 3 YAML (dignity, friendship, aspects, karakas, lords)
    relations/                     27 CSV (canonical graph edges)
    sources/                       140,941 JSONL corpus chunks, 80+ texts
    ayurveda/, plants/, sound/, vastu/, gandharva/, geography/, species/ ...
  static/                          16 HTML pages + 9 widgets
    s0.html–s6.html                S-layer domain pages (self-assembling)
    oracle.html                    I Ching + Pasaka two-instrument oracle
    jyotish_chart.html             Nakshatra mandala + wave field
    shalaka.html                   Sri Rama Shalaka grid oracle
    home.html, dashboard.html, glyphs.html, hexd-portal.html
  sc/                              atlas_synth.scd — 17 SynthDefs, wave field handlers
  research/                        32 markdown papers + 9 JSON artifacts
  docs/audit/                      System audit (April 21, 2026)
  instance/personal/               natal.json (personal chart — NOT for public repo)

atlas_330/                         Archive/presentation repo
  apps/                            27 HTML apps across 11 domains
  wiki/                            219 markdown pages
  static/                          shell.html (original vastu mandala), live.html, etc.
```

---

## Known State as of April 22, 2026

**Source**: `docs/audit/` documents + live measurement.

### Scale
| Metric | Count |
|--------|-------|
| kernel.py routes | 147 |
| Blueprint routes | 112 |
| **Total routes** | **259** |
| Engine files (*_engine.py) | 98 |
| Total Python files (npu_engine/) | 238 |
| CSV datasets | 240 |
| Dataset domains | 42 |
| Graph entities | 17,612 |
| Graph edges | 13,304 |
| Corpus JSONL chunks | 140,941 |
| Research papers (md) | 32 |
| Static HTML pages | 16 |
| Blueprints registered | 8 |

### Live Systems
| System | Status |
|--------|--------|
| Kernel (Flask, port 5000) | Running |
| Swiss Ephemeris (panchanga + jyotisha) | Active |
| Sound field loop (60s tick, 15 OSC msgs) | Running |
| SuperCollider (17 SynthDefs + wave handlers) | Available |
| Graph engine (17.6K entities) | Active |
| Toroidal field (OpenVINO NPU) | Active |
| Vector store (140K chunks) | Active |
| iGPU render (4 projections) | Active |
| Geosolar logger (600s tick) | Running |

### Sound Architecture — LIVE
Sound pipeline is fully operational as of April 18, 2026:
- `derive_sound_spec()` → 15 OSC messages per tick (5 standard + 10 wave field)
- Tanpura drone: breathing (4s prana LFO), dynamic partials (Sa/Pa/Ma/ga), drift
- Wave field → gamak intensity, tempo from tithi phase (60-120 bpm), dominant k → partial
- Rhythm task: prime-grouped percussive pulse (3/5/7-fold from wave field)
- Raga from Moon nakshatra (27 NAK_RAGA mappings)
- Natal tonal filter (home raga, crossover at activation 0.5)
- Blocker: PipeWire JACK shim to MOTU M2 for SC. pw-cat path works.

### Jyotisha Layer (April 16-18, 2026)
- `jyotisha_engine.py`: Swiss Ephemeris, compute_chart, dignity, combustion, aspects, Tara Bala, tithi, two-source wave field (compute_wave_field, compute_nakshatra_field)
- `jyotish_utils.py`: normalization (3-way rashi, 3-way graha), DMS parser, CSV loaders
- `jyotish_bp.py`: /jyotish/chart, /compute, /natal, /transits, /tara, /wave_field, /calendar, /sound_state, /compatibility
- `jyotish_chart.html`: nakshatra mandala, wave opacity overlay, pada ring, graha placement, SI overlay
- Naming: simplified IAST for rashi (Mesha), English for graha (Sun), matching graha_master.csv
- Ayanamsha: swe Lahiri default, custom_ayanamsha_deg param for calibration

---

## S-Stack Framing

The S0–S6 stack is sabda descending — the same present-moment field state
re-expressed at increasing density of manifestation, not seven functional surfaces:

- **S0** = cosmological frame (Gaudiya + Vedic substrate, static, read-only)
- **S1** = devi (today's Nitya + her yantra + her retinue)
- **S2** = nada (para → pasyanti → madhyama → vaikhari as nested rings)
- **S3** = kala (panchanga, counted time)
- **S4** = yantra (geometry, chladni interference, today's field's geometric face)
- **S5** = bhumi (land/direction/season)
- **S6** = lila (prescribed action, human experience interface)

Each layer analyzes the same moment in its own medium. Not "seven apps" —
one descent re-read at seven densities.

---

## Portal Aesthetic Rule

Register belongs to the layer, not the system:
- S0/S1 → temple register (gold on plum, Cormorant Garamond, devotional)
- S3/S4 → cartographer register (navy/orange, JetBrains Mono)
- S2 → hybrid (temple shell with cartographer readouts)

Unified portal is polyvocal, not consistent-chrome. The bindu/ego-point is
invariant: current field state + natal imprint + resonance score.

---

## Research Paper Inventory

`~/atlas_core/research/` contains active research papers. Read the relevant
paper before working in its domain:

- **yantra_eigenvalue_exploration.md** — Lo Shu ±2√6 invariant, Kronecker scaling, Brahmasthana Theorem, Lo Shu breaks I Ching Q6 degeneracy 7→27 eigenvalues
- **two-source-interference-v3.md** — Findings 7-14: N-source boundary silence, two-source = classical aspects (k=1 conjunction, k=3 trine, k=4 square, k=6 sextile, k=12 rashi; BPHS Ch. 28), 180° parity rule, wave matrix rank 15 = Nitya count, gandanta p<0.0001, Kp null, planetary retrograde primes {3,5,7,11}, tidal-weighted → 44 regions (Sri Yantra 43+bindu)
- **planetary-primes-v1.md** — Mercury=3, Venus=5, Mars=7, Jupiter=11 retrograde symmetries (ephemeris-verified); tidal-weighted cos(nθ) → 44 regions
- **vertebral-primes-v1.md** — Cross-species vertebral analysis; C7+T12+L5=24=Sri Yantra crossings; hand 27=nakshatras; 44 upper-limb marma = wave field regions. PENDING: bat T=12 primary-literature verification.

---

## BIHS Institutional Context

The Bhaktivedanta Institute for Higher Studies (BIHS) is headquartered in
Gainesville, FL — the same city as kanjira. Designated home of the Richard
L. Thompson Archives (Sadaputa Dasa). Runs hybrid Thompson reading groups
alternate Saturdays.

Atlas is a contemporary computational extension of the Bhaktisiddhanta →
Thompson methodological lineage — same lineage-act (keeping Bhagavata
cosmography coherent with present-day instrumental resolution), different
era's tools.

---

## Confessional-Methodology Stance

The Gaudiya astronomical lineage is characterized academically as "confessional
methodology, not history of science." Atlas accepts this honestly. The lineage
is specific and short: Bhaskara (12c) → Bhaktisiddhanta (19c) → Thompson (20c)
→ Atlas (21c), each re-expressing the same Bhagavata cosmography at its era's
instrumental resolution. This is lineage-continuation-through-re-expression,
not orthodoxy-inheritance. Do not over-claim continuity with classical acharyas
who did not themselves write ganita-sastras.

---

## Architecture Decisions (Permanent)

- **Gamak ARE the notes** (Pearson 2016) — SC uses continuous pitch, not quantized
- **Bhedabheda filter**: harinama / japa / smarana NEVER appear in avoid lists (BRS 1.2)
- **Screen IS Vastu Purusha Mandala** (8 zones, content by zone deity)
- **Animal → Graha → Mood → Music**: `blend_toward_graha()` is gradual
- **Atlas functions as an OS**: toroidal field = scheduler, corpus = filesystem, panchanga = clock
- **`_OV_DEVICE="AUTO"`** is verified correct (do not override)
- **Naming**: simplified IAST for rashi (Mesha not Mesa), English for graha keys (Sun not Surya)
- **Ayanamsha**: Lahiri (swe default). Custom param available for calibration.
- **House system**: whole-sign implemented, others accept parameter + raise NotImplementedError

---

## Compute Routing (verified April 2026)

- **CPU** wins all element-wise math (field query, yantra to 81×81)
- **NPU** wins transformer inference (MiniLM 2.43ms)
- **GPU** wins 729×729+ matmul, Chladni 1024×1024 (2.1× faster), gamak DSP at 16+ notes

---

## Key APIs

```
GET  /field              → current field state
GET  /spine              → full FieldState from 10 engines
GET  /jyotish/natal      → natal chart (Swiss Ephemeris, real positions)
GET  /jyotish/transits   → current sky chart (real ephemeris)
GET  /jyotish/wave_field → two-source wave interference analysis
GET  /jyotish/calendar   → per-day ephemeris for date range
GET  /jyotish/sound_state→ wave-derived sound parameters
GET  /goloka             → ashtakala + Vraja forest + Nitya Devi
GET  /trajectory         → temporal arc projection
GET  /sound/state        → current sound spec
GET  /corpus/search      → JSONL passage search (140K chunks)
GET  /layers/<layer>     → S-layer composed content
GET  /oracle             → I Ching + Pasaka oracle page
GET  /lila/augury/*      → hexagram, omen, cast, pasaka routes
```

---

## Session Startup Protocol

1. Read this skill file
2. Read `~/atlas_core/CLAUDE.md` for repo-specific instructions
3. Identify session type: engine / dataset / route / frontend / sound / research / jyotish
4. Check `docs/audit/OPEN_QUESTIONS.md` for pending decisions
5. If touching S-layers: check `docs/audit/S_LAYER_CURRENT_STATE.md`
6. If touching research: read the relevant paper in `research/` first
7. If touching sound: know that the pipeline is LIVE and producing audio

## What Claude Should Never Do

- Hardcode cosmological values — always derive from /field
- Modify `datasets/relations/relations_resolved_canon.csv` without confirmation
- Assume natal.json can be public (contains personal birth data)
- Re-derive findings already captured in research/ papers
- Override user-set raga/mode with wave field suggestions
- Count stub directories as missing engines (they're planned refactors)
- Fabricate attestation for data that doesn't have it

---

## Current Known Gaps / Blockers

- `natal.json` contains personal birth data — must be .gitignored before public push
- Bat T=12 in vertebral paper: genus-level verification needed before distribution
- 6/15 Nitya yantra geometry rows are SPECULATIVE (no canonical source text)
- PipeWire JACK shim for SC→MOTU: pw-cat workaround works
- Krishna paksha Devi ordering (reverse vs forward) unresolved
- Lagna differs from natal.json by 4.46° (ASC computation method, not ayanamsha)
- 3 S-layers (S0, S2, S6) have no layer_composer content
- s4-bloom.html (54K Chladni variant) is unrouted
- HTML-in-core boundary: stated rule is "JSON only" but 16 HTML pages exist in static/
