---
name: atlas-tx-regional-water-authority-ingestion
description: Add new Texas regional water-authority data slices to Atlas TX using ArcGIS/Hub-first discovery, strict TDD, and fail-soft handling for flaky upstreams.
version: 1.0.0
metadata:
  hermes:
    tags: [atlas-tx, water, texas, arcgis, ingest, hydrology, county-join, tdd]
---

# Atlas TX regional water-authority ingestion

Use this when extending `~/Projects/atlas-tx` with new basin/authority-backed water layers like LCRA, GBRA, SARA, TRA, SJRA, or similar regional sources.

## When to use
- User asks to ingest a new Texas river authority / regional water authority source into Atlas TX.
- You need to turn ArcGIS Hub / FeatureServer / app-backed monitoring data into typed adapters and API routes.
- You need county joins for basin features, especially lakes or monitoring sites.

## Core approach
1. Read repo ground state first:
   - `docs/STATE.md`
   - current plan under `docs/plans/`
   - `skills/atlas-tx/SKILL.md`
2. Prefer machine-readable surfaces in this order:
   - ArcGIS Hub DCAT feed
   - Hub `/api/v3/datasets`
   - direct FeatureServer / MapServer layer URLs
   - app-backed JSON endpoints
   - browser/manual discovery only last
3. Use strict TDD:
   - write failing tests first
   - run the targeted tests and observe RED
   - implement the minimum to pass
   - run targeted tests again, then full suite, then lint/build

## Proven discovery workflow
### For ArcGIS Hub-backed authorities
Use terminal HTTP first. These endpoints worked well for GBRA:
- Hub home: `https://<hub>.hub.arcgis.com/`
- dataset API: `https://<hub>.hub.arcgis.com/api/v3/datasets`
- DCAT feed: `https://<hub>.hub.arcgis.com/api/feed/dcat-us/1.1.json`

The DCAT feed is especially useful because it reveals:
- human dataset title
- item identifier
- direct `FeatureServer/<layer>` URLs
- download links

For GBRA this surfaced the first high-value layers quickly:
- major rivers = layer 1
- GVHS lakes = layer 2
- subwatersheds = layer 3
- watersheds = layer 4

### For site pages / experiences
Use browser only when the direct API path is unclear. Do not scrape page text if the same source has ArcGIS endpoints.

## Implementation pattern
### 1. Add typed records in `src/lib/water/types.ts`
Create narrow normalized types with:
- `sourceId`
- stable ID / name
- only high-value numeric fields
- `raw`

### 2. Build a focused adapter in `src/lib/water/<authority>-<slice>.ts`
Patterns that worked:
- central `buildQueryUrl(layerId, returnGeometry=false)`
- small per-layer attribute types
- `normalizeString()` + `normalizeNumber()` helpers
- `fetchJson()` that throws on non-OK status
- cache via `getGlobalWaterDataCache().getOrLoad(...)`
- lightweight name filters for routes

### 3. Add routes under `src/app/api/water/...`
Route pattern:
- read optional query params like `?name=`
- fetch source rows
- apply local filter helper
- return `{ sourceId, featureCount, <rows>, freshness }`

### 4. Register source + freshness
Update:
- `src/lib/water/water-source-registry.ts`
- `src/lib/water/freshness.ts`

### 5. Wire minimal UI exposure only after route stability
For early slices, it is enough to add API links on `/water` before deeper summary integration.

## County-join pattern that worked
For GBRA GVHS lakes, a reusable approach was:
1. Fetch the authority polygon layer with `returnGeometry=true`.
2. Query Census TIGERweb county overlay via POST, not GET, because polygon geometry URLs can get huge.
3. Use:
   - URL: `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1/query`
   - `geometryType=esriGeometryPolygon`
   - `spatialRel=esriSpatialRelIntersects`
   - `where=STATE='48'`
   - `outFields=NAME,GEOID`
   - `returnGeometry=false`
   - `f=json`
4. Pass `inSR` using the authority layer SR, not guessed WGS84/WebMercator.
5. For GBRA hydrology, the correct SR was `26914` (UTM zone 14N). This mattered. Using the wrong SR caused empty county matches.
6. Normalize returned counties through `getCountyByFips()` / `getCountyBySlugOrName()` from `county-lookup.ts`.
7. Deduplicate counties by slug.

### Important pitfall
Do not send large polygons to TIGERweb as GET query params. That caused transport / SSL / EOF failures. Use POST with `application/x-www-form-urlencoded`.

## Handling flaky upstreams
Two live-source issues showed up and should be preserved:
1. `waterquality.lcra.org` TLS verification is flaky from Node in this environment.
   - Summary services should fail soft when optional LCRA quality fetches fail.
   - Use safe fallbacks for overview paths so unrelated tests/pages do not fail.
2. TIGERweb can be sensitive to large geometry requests.
   - POST helps materially.
   - Keep county-overlay work isolated to dedicated routes/slices when possible.

## Test strategy that worked
For each new authority slice, add:
1. Adapter unit test
   - normalization
   - filter helpers
   - fetch path with mocked `globalThis.fetch`
2. Route test
   - mock adapter module
   - verify optional query param behavior
   - verify freshness envelope
3. Registry test update
4. If `/water` surface changes, add or patch the page test for the new API link

Then run:
- targeted `npm test -- --run ...`
- full `npm test`
- `npm run lint`
- `npm run build`

## Best-first source selection heuristic
When choosing the first slice for a new authority:
- prefer low-cardinality, clearly-named ArcGIS layers with obvious user value
- examples: major rivers, lakes, watersheds, subwatersheds
- defer complex monitoring dashboards until you verify stable JSON / ArcGIS endpoints

## Good next steps after first authority slice
1. county join / overlay for key basin assets
2. watershed / subwatershed polygons
3. monitoring or water-quality layer only if machine-readable and stable

## GBRA water-quality discovery findings worth preserving
After the first GBRA hydrology slices, the most reusable lesson was that the obvious ArcGIS water-quality service is not the right primary truth source for current monitoring.

### What looked promising first, but should be treated as secondary
Public ArcGIS service:
- `https://services7.arcgis.com/Q6vsXnxTnYcWB7qg/ArcGIS/rest/services/Water_Quality_Sample_Stations/FeatureServer`
- item id: `d27bbbc66f8e448e8505ac14742c83fa`

Useful facts discovered:
- service description says it is a TCEQ-derived inventory of surface-water monitoring stations with monitoring entity tags
- layer `0` = `CRP Water Quality Monitoring Sites (2019)`
- layer `1` = `Surface Water Quality Monitoring Stations (TCEQ)`
- ArcGIS item metadata and layer edit dates point back to 2020-era content
- counts observed live:
  - layer 0 total: `120`
  - layer 0 `Entity='GBRA'`: `82`
  - layer 0 `ACTIVE_IND='Y' AND Entity='GBRA'`: `70`
  - layer 1 total: `224`
  - layer 1 `Monitoring='GBRA'`: `78`

Conclusion:
- this service is still useful for geometry, station metadata, county tags, and legacy inventory context
- do **not** treat it as the primary current monitoring source for GBRA program truth

### Better primary source for current GBRA monitoring
Use GBRA’s county monitoring pages plus the linked `waterservices.gbra.org` files.

Verified county-page pattern:
- `https://www.gbra.org/environmental/water-quality/sites/<county>/`
- examples: `hays`, `caldwell`, `victoria`

These pages expose, per station:
- TCEQ station id
- description
- latitude / longitude
- parameters / frequency
- monitoring type / by
- historical Excel link
- current CSV link

Verified live current-data host:
- `https://waterservices.gbra.org/crp/<station-or-file>.csv`
- example: `https://waterservices.gbra.org/crp/12672.csv`

Important live behavior discovered:
- current CSV files can be materially fresher than the ArcGIS inventory
- example: station `12672.csv` returned `Last-Modified: Mon, 04 May 2026 ...`
- CSV schema observed live:
  - `Collect Date`
  - `Collect Time`
  - `Parameter`
  - `Reported Result`
  - `Units`
  - `Parameter Code`

### Critical implementation lesson
Do **not** assume every current CSV is at `/<stationId>.csv` by pattern alone.

Observed behavior:
- some station-id CSVs returned `200`
- some active ArcGIS stations returned `404` at the guessed station-id CSV URL
- therefore the authoritative current CSV URL must come from the GBRA county page table itself, not from string interpolation

### Best implementation choice for a GBRA monitoring slice
Prefer this source priority:
1. GBRA county monitoring pages for station metadata and authoritative download links
2. `waterservices.gbra.org` current CSV files for observation rows
3. ArcGIS `Water_Quality_Sample_Stations` only as a fallback geometry/inventory supplement

Recommended normalized site fields:
- `stationId`
- `county`
- `description`
- `latitude`
- `longitude`
- `parameterFrequency`
- `monitoringType`
- `currentCsvUrl`
- `historicalXlsUrl`
- `sourcePageUrl`

Recommended normalized observation fields:
- `collectedAt`
- `parameter`
- `reportedResult`
- `units`
- `parameterCode`

### Practical GBRA water-quality routes to build next
- `/api/water/gbra/quality/sites`
- `/api/water/gbra/quality/sites/[stationId]`
- `/api/water/gbra/quality/sites/[stationId]/observations`
- optional county helper route:
  - `/api/water/gbra/quality/counties/[countySlug]/sites`

### Discovery pitfall to remember
GBRA has multiple overlapping public surfaces:
- ArcGIS inventory
- county HTML pages
- `waterservices.gbra.org` file downloads
- TCEQ references

The right move was to change course after seeing the ArcGIS service was stale. For GBRA monitoring, current county pages + linked CSVs beat ArcGIS purity.

## Deliverable checklist
- typed adapter
- routes
- registry entry
- freshness entry
- RED→GREEN tests
- full test/lint/build pass
- `docs/STATE.md` updated

## Atlas TX-specific notes
- Keep demo paths cached or fail-soft when upstreams are brittle.
- Prefer authoritative geometry / monitoring layers over dashboard scraping.
- Add UI links early; deeper county-summary integration can follow once data shape stabilizes.
