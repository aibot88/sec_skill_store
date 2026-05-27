---
title: Design Automation
description: Rule-based design systems, constraint satisfaction, space planning algorithms, automated layout generation, drawing automation, code compliance checking, and computational workflows for AEC design automation
version: 1.0.0
tags: [automation, rule-based, constraint-satisfaction, space-planning, layout, compliance, workflow, code-generation]
auto_activate: true
user_invocable: true
invocation: /design-automation
---

# Design Automation for AEC

Design automation is the disciplined application of computational logic to replace, accelerate, or augment repetitive and rule-governed design tasks across architecture, engineering, and construction. This skill covers the full spectrum from simple parametric rules through constraint-satisfaction engines to fully generative layout systems, drawing automation pipelines, and automated code-compliance verification.

---

## 1. Design Automation Spectrum

### 1.1 Levels of Automation in AEC

Design automation exists on a continuum. Understanding where a task falls on this spectrum determines the appropriate technology and the degree of human oversight required.

| Level | Label | Description | Example |
|-------|-------|-------------|---------|
| 0 | Manual | Designer makes every decision, draws every line | Hand-drafted floor plans |
| 1 | Parametric | Geometry driven by explicit parameters; designer controls inputs | Grasshopper slider controlling facade panel width |
| 2 | Rule-Based | IF-THEN logic encodes design knowledge; system applies rules automatically | Auto-sizing exit widths based on occupant load |
| 3 | Constraint-Based | System searches solution space satisfying stated constraints | CSP solver placing rooms to satisfy adjacency + area constraints |
| 4 | Generative | System produces many candidate designs autonomously; human selects | GA-based floor plan generator producing 500 layout options |
| 5 | AI-Assisted | Machine-learned models propose designs or predict performance | GAN generating floor plan from adjacency graph |
| 6 | Autonomous | Fully closed-loop: sense conditions, generate design, validate, output | Automated site grading from survey to construction docs (emerging) |

### 1.2 What Can vs. Should Be Automated

**High automation potential:**
- Code compliance checking (deterministic rules)
- Structural member sizing (engineering formulas)
- Parking layout optimization (geometric + count)
- Sheet creation and annotation (repetitive)
- Clash detection (spatial intersection)
- Area and quantity takeoffs (data extraction)

**Medium automation potential:**
- Space planning and room layout (heuristic + constraint)
- Facade design (performance + aesthetic rules)
- MEP routing (complex constraints, many valid solutions)
- Site grading (optimization with soft constraints)

**Low automation potential (human judgment critical):**
- Architectural concept design (cultural, contextual)
- Urban massing and placemaking (experiential quality)
- Material palette selection (aesthetic, tactile)
- Client presentation and persuasion (social)

### 1.3 Human-in-the-Loop Design Automation

The most effective AEC automation systems keep designers in the loop at critical decision points:

1. **Define** — Human sets objectives, constraints, preferences
2. **Generate** — System produces candidate solutions
3. **Evaluate** — System scores and ranks; human reviews
4. **Select** — Human chooses preferred direction
5. **Refine** — System develops selected option further
6. **Validate** — Automated compliance checking; human sign-off

This cycle can repeat at multiple scales: master plan level, building level, floor level, room level.

### 1.4 The Role of Design Rules and Heuristics

Design rules encode domain expertise in computable form:

- **Hard rules**: Must be satisfied (building code, structural limits). Violation = invalid design.
- **Soft rules**: Should be satisfied (rules of thumb, best practices). Violation = penalty score.
- **Heuristics**: Rules of thumb that usually produce good results but are not guaranteed optimal. Examples:
  - Office floor plate depth should not exceed 15m from core to window
  - Residential corridor length should not exceed 30m without a window
  - Parking bay angle of 90 degrees maximizes density; 60 degrees improves maneuverability
  - Structure grid spacing of 7.5-9.0m suits most office programs

---

## 2. Rule-Based Design Systems

### 2.1 Production Rules (IF-THEN)

The simplest and most widely used automation pattern in AEC:

```
IF occupant_load > 500
THEN required_exits >= 3
     AND exit_width_total >= occupant_load * 5.0mm

IF room_type == "bathroom" AND floor_area < 4.0
THEN min_dimension >= 1.5m
     AND door_swing == "outward"

IF building_height > 23m
THEN fire_resistance_rating >= 120min
     AND sprinkler_system == required
```

Production rules are stored in a rule base and executed by a rule engine that:
1. Matches rules against current facts (pattern matching)
2. Resolves conflicts when multiple rules fire (conflict resolution)
3. Executes the winning rule's action (assertion or modification)
4. Repeats until no more rules fire (quiescence)

### 2.2 Decision Trees

Hierarchical rule structures where each node tests a condition and branches lead to sub-decisions:

```
Building Classification Decision Tree:
├── Occupancy > 300?
│   ├── YES → Assembly (A)
│   │   ├── Fixed seating? → A-1
│   │   ├── No fixed seating? → A-2
│   │   └── Worship? → A-3
│   └── NO → Business (B)
│       ├── Office? → B
│       └── Educational? → E
│           ├── Students > 12 yrs? → E
│           └── Students ≤ 12 yrs? → E (daycare)
```

Decision trees are valuable because they are transparent, auditable, and can be validated against code text.

### 2.3 Rule Engines

Production rule engines for AEC applications:

- **Forward chaining**: Start from known facts, derive conclusions. Used for compliance checking. "Given this building, what rules are violated?"
- **Backward chaining**: Start from goal, find supporting facts. Used for design guidance. "What do I need to achieve fire compliance?"
- **Rete algorithm**: Efficient pattern matching for large rule sets. Maintains a network of partial matches; only re-evaluates affected rules when facts change.

Implementation options:
- Python: `durable-rules`, `business-rules`, custom engines
- Java/Kotlin: Drools (most mature open-source rule engine)
- .NET: NRules (for Revit add-in integration)
- Grasshopper: Conditional components, custom C# script nodes

### 2.4 Shape Grammars (Stiny)

Shape grammars define a set of shape rules that transform geometric configurations. Formally:

```
SG = (S, L, R, I)
where:
  S = finite set of shapes
  L = finite set of labels (markers, reference points)
  R = finite set of shape rules: α → β (replace shape α with shape β)
  I = initial shape
```

Shape grammar applications in AEC:
- **Palladian villa grammar** (Stiny & Mitchell, 1978): Generates villa plans following Palladio's compositional logic
- **Prairie house grammar** (Koning & Eizenberg, 1981): Encodes Frank Lloyd Wright's Prairie style
- **Musgum grammar**: Encodes traditional Musgum shell house typology
- **Islamic geometric pattern grammars**: Tile-based generation of complex ornamental patterns
- **Facade grammar**: Generates facade variations from a vocabulary of elements (window, panel, mullion, spandrel)

### 2.5 Graph Grammars

Extend shape grammars to operate on graph structures (nodes + edges) rather than geometric shapes:

- Nodes represent rooms, spaces, or building elements
- Edges represent adjacency, access, containment, or structural relationships
- Rules transform subgraphs: match a pattern, replace with a new pattern

Graph grammars are powerful for:
- Floor plan generation from room adjacency programs
- Building massing from spatial relationship diagrams
- Urban block subdivision from land-use programs

### 2.6 Rule Priority and Conflict Resolution

When multiple rules apply simultaneously, conflict resolution strategies include:

1. **Priority ordering**: Each rule has a numeric priority; highest fires first
2. **Specificity**: More specific rules override general rules (e.g., local code overrides IBC)
3. **Recency**: Rules matching recently modified facts fire first
4. **Refraction**: A rule does not fire twice on the same set of facts
5. **Jurisdictional hierarchy**: Federal > State > Local > Project-specific

### 2.7 Rule Libraries for AEC

| Domain | Rule Source | Key Rules |
|--------|-----------|-----------|
| Egress | IBC Chapter 10 | Occupant load factors, exit width, travel distance, common path |
| Fire safety | IBC Chapter 7 | Fire resistance ratings, compartment sizes, opening protection |
| Accessibility | ADA/ABA, EN 17210 | Clear widths, ramp grades, turning radii, reach ranges |
| Structural | ASCE 7, Eurocode | Load combinations, deflection limits, drift limits |
| Zoning | Local zoning code | Setbacks, height, FAR, lot coverage, parking ratios |
| Energy | ASHRAE 90.1, IECC | Envelope U-values, WWR limits, HVAC efficiency |
| Plumbing | IPC | Fixture counts by occupancy, pipe sizing |

---

## 3. Constraint Satisfaction Problems (CSP)

### 3.1 CSP Formalism

A CSP is defined by the triple (X, D, C):

- **X** = {X1, X2, ..., Xn}: set of variables
- **D** = {D1, D2, ..., Dn}: set of domains (possible values for each variable)
- **C** = {C1, C2, ..., Cm}: set of constraints (relations restricting variable assignments)

A **solution** is an assignment of values to all variables such that every constraint is satisfied.

### 3.2 CSP for Floor Plan Layout

Formulating floor plan layout as a CSP:

**Variables**: Room positions and dimensions
- X_i = (x_i, y_i, w_i, h_i) for each room i

**Domains**:
- Position: within building boundary
- Width/height: within acceptable range for room type

**Constraints**:
- **Non-overlap**: No two rooms share interior area
- **Boundary containment**: All rooms within building envelope
- **Adjacency**: Specified room pairs must share a wall segment of minimum length (door width)
- **Non-adjacency**: Certain rooms must not be adjacent (e.g., bedroom not adjacent to mechanical)
- **Area**: Room area within specified range (e.g., living room 20-35 m2)
- **Aspect ratio**: Room width-to-depth ratio within range (e.g., 1:1 to 1:2)
- **Window access**: Rooms requiring daylight must touch an exterior wall
- **Structural grid alignment**: Room boundaries align with structural grid lines

### 3.3 Arc Consistency

Arc consistency (AC-3) prunes variable domains before search begins:

For every pair of constrained variables (Xi, Xj), remove values from Di that have no supporting value in Dj. Repeat until no more pruning occurs.

This dramatically reduces the search space. For AEC problems with continuous domains, discretize positions to a grid (e.g., 300mm module) to make the domain finite.

### 3.4 Backtracking Search

The standard algorithm for solving CSPs:

```
function BACKTRACK(assignment, csp):
    if assignment is complete: return assignment
    var = SELECT-UNASSIGNED-VARIABLE(csp)
    for value in ORDER-DOMAIN-VALUES(var, assignment, csp):
        if value is consistent with assignment:
            add {var = value} to assignment
            inferences = INFERENCE(csp, var, value)
            if inferences != failure:
                add inferences to assignment
                result = BACKTRACK(assignment, csp)
                if result != failure: return result
            remove inferences and {var = value}
    return failure
```

Key heuristics for AEC CSPs:
- **MRV (Minimum Remaining Values)**: Assign the room with fewest valid placements first (fail-early)
- **Degree heuristic**: Assign the room with most adjacency constraints first
- **Least Constraining Value**: Try placements that leave the most options for unassigned rooms

### 3.5 Constraint Propagation

Beyond arc consistency, stronger propagation techniques:
- **Path consistency**: Ensures consistency for triples of variables
- **MAC (Maintaining Arc Consistency)**: Run AC-3 after each assignment
- **Forward checking**: Remove inconsistent values from neighbors of just-assigned variable

### 3.6 Soft vs. Hard Constraints

In real AEC problems, not all constraints are absolute:

**Hard constraints** (must satisfy):
- Building code requirements
- Structural limits
- Site boundary
- Non-overlap of rooms

**Soft constraints** (prefer to satisfy, with penalty for violation):
- Preferred adjacency (e.g., kitchen near dining)
- View orientation (e.g., living room faces south)
- Preferred aspect ratio
- Acoustic separation preferences

Soft constraints are handled by:
1. **Weighted CSP**: Each soft constraint has a weight; minimize total penalty
2. **Optimization over feasible set**: Find all hard-constraint-satisfying solutions, then rank by soft constraint satisfaction
3. **Pareto frontier**: When soft constraints conflict, find non-dominated solutions

### 3.7 CSP for Structural Grid

Variables: Grid line positions along X and Y axes
Domains: Continuous within building boundary, discretized to module (e.g., 100mm)
Constraints:
- Minimum span: 5.0m (functional space between columns)
- Maximum span: 12.0m (without transfer structures for typical concrete)
- Column-free zones: No columns in specified areas (auditorium, lobby)
- Edge alignment: Grid aligns with building perimeter
- Core alignment: Grid lines pass through core walls
- Regularity: Prefer uniform bay sizes (soft constraint)

---

## 4. Space Planning Algorithms

### 4.1 Adjacency-Based Layout

The classic space planning approach:

1. **Adjacency matrix**: Define required and desired adjacencies between rooms

```
         LIV  DIN  KIT  BED1 BED2 BATH ENT
Living    -    2    1    0    0    0    2
Dining    2    -    2    0    0    0    0
Kitchen   1    2    -    0    0    0    0
Bed 1     0    0    0    -    0    2    0
Bed 2     0    0    0    0    -    1    0
Bath      0    0    0    2    1    -    0
Entry     2    0    0    0    0    0    -

(0 = no relation, 1 = preferred, 2 = required)
```

2. **Bubble diagram generation**: Place rooms as circles/rectangles; connect required adjacencies with springs; use force-directed layout to minimize spring energy

3. **Graph-based placement**: Represent adjacency as a planar graph; find a planar embedding; assign rooms to faces of the graph

### 4.2 Grid-Based Placement

Discretize the floor plate into a grid and assign rooms to grid cells:

- **Grid resolution**: Typically 300mm, 600mm, or 1200mm module
- **Bin packing**: Treat rooms as rectangles, floor plate as a bin; use heuristics (bottom-left, best-fit, shelf algorithms)
- **Integer programming**: Assign binary variables x_{i,j,k} = 1 if room i occupies grid cell (j,k); add constraints for contiguity, adjacency, area
- **Advantages**: Naturally handles structural grid alignment
- **Disadvantages**: Grid resolution limits design freedom; large grids = many variables

### 4.3 Force-Directed Layout

Model rooms as particles in a physics simulation:

- **Attractive forces**: Between rooms that should be adjacent (spring force, F = k * delta)
- **Repulsive forces**: Between all room pairs to prevent overlap (Coulomb-like, F = q / r^2)
- **Boundary forces**: Repel rooms from floor plate boundary (containment)
- **Gravity**: Pull rooms toward building center (compactness)
- **Damping**: Reduce velocity each step to reach equilibrium (damping factor 0.8-0.95)

Algorithm:
```
1. Initialize room positions randomly within boundary
2. For each timestep:
   a. Calculate all forces on each room
   b. Update velocities: v += F * dt / mass
   c. Apply damping: v *= damping_factor
   d. Update positions: p += v * dt
   e. Resolve overlaps (push apart along shortest separating axis)
   f. Enforce boundary containment
3. Stop when total kinetic energy < threshold
```

Force-directed layout produces organic, relationship-driven arrangements but rarely produces rectangular room boundaries without post-processing.

### 4.4 Evolutionary Layout (GA-Based Floor Plan Generation)

Genetic algorithm approach:

**Genome encoding**:
- Sequence of room placements: [(room_id, x, y, w, h, rotation), ...]
- Or: slicing floorplan tree (horizontal/vertical cuts + room assignment)
- Or: adjacency graph + relative positioning flags (left-of, above, ...)

**Fitness function** (multi-objective):
- Adjacency satisfaction score (weighted)
- Area utilization (minimize wasted space)
- Aspect ratio quality (penalize extreme ratios)
- Circulation efficiency (total corridor area)
- Daylight access (perimeter contact for daylight-required rooms)
- Code compliance (exit distance, egress width)

**Operators**:
- **Selection**: Tournament selection (size 3-5)
- **Crossover**: Swap room subtrees between two parent slicing trees; or swap room positions
- **Mutation**: Shift room position, resize room, swap two rooms, change cut direction
- **Repair**: Fix overlaps, enforce boundary, adjust areas to program

**Parameters**:
- Population: 200-1000
- Generations: 500-5000
- Crossover rate: 0.7-0.9
- Mutation rate: 0.05-0.20
- Elitism: preserve top 5-10%

### 4.5 Recursive Subdivision

Top-down partitioning of a floor plate:

**BSP-Tree (Binary Space Partitioning)**:
1. Start with the entire floor plate as a single region
2. Choose a cutting line (horizontal or vertical)
3. Split the region into two sub-regions
4. Assign rooms to sub-regions based on program
5. Recursively subdivide each sub-region
6. Stop when each region contains exactly one room

**K-D Tree variant**: Alternate between horizontal and vertical cuts at each level.

**Squarified treemap**: Choose cut direction and position to minimize aspect ratio deviation from 1:1. Produces compact, well-proportioned rooms.

Decision: Where to cut?
- Proportional to area: Cut position based on area ratio of rooms assigned to each side
- Adjacency-driven: Keep adjacent rooms on the same side of the cut
- Structural grid-aligned: Snap cuts to structural grid lines

### 4.6 Stacking Algorithms (Multi-Story)

For multi-story buildings, stacking determines which rooms/units go on which floors:

1. **Core alignment**: Vertical circulation (stairs, elevators) must align across all floors
2. **Structural continuity**: Load-bearing walls and columns must stack vertically
3. **Program zoning**: Public/commercial on lower floors, private/residential above
4. **MEP continuity**: Wet rooms (kitchens, bathrooms) should stack for efficient plumbing risers
5. **Unit type assignment**: Assign unit types to floor plates considering:
   - Typical floor repetition (efficiency)
   - Setback floors (larger/different units)
   - Ground floor special conditions (retail, lobby)
   - Penthouse floor special conditions

### 4.7 Corridor and Circulation Routing

After rooms are placed, corridors must connect them:

- **Shortest path**: A* or Dijkstra on grid graph connecting room doors to building exits
- **Minimum spanning tree**: Connect all rooms with minimum total corridor length
- **Dead-end elimination**: Ensure corridors form loops or connect to multiple exits
- **Width compliance**: Corridors must meet minimum width (typically 1200mm residential, 1500mm commercial, 2400mm hospital)
- **Travel distance**: Maximum travel distance from any point to an exit (IBC: 60m sprinklered, 45m unsprinklered for most occupancies)

### 4.8 Room Sizing Rules by Program Type

| Room Type | Area Range (m2) | Min Dimension | Notes |
|-----------|----------------|---------------|-------|
| Studio apartment | 28-40 | 3.6m | Combined living/sleeping |
| 1-bed apartment | 45-65 | - | Separate bedroom |
| 2-bed apartment | 65-90 | - | - |
| 3-bed apartment | 85-120 | - | - |
| Living room | 18-35 | 3.3m | Daylight required |
| Master bedroom | 12-20 | 3.0m | Daylight, closet |
| Secondary bedroom | 9-14 | 2.7m | Daylight, closet |
| Kitchen | 7-15 | 2.4m | Ventilation required |
| Bathroom | 3.5-8 | 1.5m | Wet area |
| Powder room | 1.5-3 | 0.9m width | No shower/tub |
| Office (private) | 9-15 | 2.7m | Daylight preferred |
| Office (open plan) | 6-10 per person | - | 8-12m max depth from window |
| Meeting room (small) | 12-20 | 3.0m | 4-8 persons |
| Meeting room (large) | 30-60 | 5.0m | 12-20 persons |
| Hotel guest room | 22-35 | 3.6m | Standard; 40-65 for suite |
| Hospital patient room | 14-22 (single) | 3.6m | With en-suite |
| Classroom | 50-75 | 6.0m | 25-30 students |
| Restaurant dining | 1.2-1.8 per seat | - | Varies by service style |
| Retail | varies | 6.0m frontage min | Varies widely |

---

## 5. Automated Layout Generation

### 5.1 Residential Unit Layout Generation

Automated residential layout follows a hierarchical process:

1. **Unit boundary definition**: From structural grid and building envelope
2. **Zone identification**: Public zone (living, dining, kitchen), private zone (bedrooms, bathrooms), service zone (laundry, storage), circulation (entry, corridors)
3. **Room placement priority order**:
   - Entry (fixed by corridor access point)
   - Kitchen (plumbing riser location)
   - Bathrooms (plumbing riser location)
   - Living room (largest contiguous window wall)
   - Bedrooms (remaining window walls)
   - Storage/utility (interior, no window needed)
4. **Circulation routing**: Entry to all rooms with minimum corridor
5. **Window assignment**: Each habitable room gets exterior wall contact
6. **Validation**: Check minimum areas, dimensions, ventilation, egress

Key constraints:
- Every habitable room must have natural light (window access)
- Kitchen requires exhaust ventilation path
- Bathroom requires mechanical or natural ventilation
- Entry should not open directly into bedroom
- No room should be a pass-through (except living to dining)

### 5.2 Office Floor Plate Optimization

Office layout automation considers:

- **Core-to-window depth**: 8-12m for open plan, 6-8m for cellular offices
- **Core placement**: Central core maximizes usable perimeter; side core maximizes contiguous floor area
- **Planning grid**: 1.35m or 1.50m module (furniture coordination)
- **Cellular office sizing**: 1-module (2.7m) small, 2-module (4.05m) standard, 3-module (5.4m) large
- **Open plan zones**: 6-8 workstations per cluster, team neighborhoods
- **Support spaces**: Meeting rooms at core adjacency, break rooms at perimeter
- **Circulation**: Primary corridor (1.8m), secondary aisles (1.2m)
- **Efficiency target**: 80-85% net-to-gross ratio

### 5.3 Hospital Department Layout

Hospital layout automation is among the most constrained:

- **Clinical adjacencies**: ED adjacent to imaging and lab; OR suite adjacent to ICU; CSSD below OR suite
- **Clean/dirty flows**: Separate clean and dirty corridors in surgical suites; soiled utility rooms with pass-through
- **Patient flow**: Intake → triage → treatment → discharge (linear, no backtracking)
- **Staff flow**: Separate from patient and visitor flows
- **Infection control zones**: Negative pressure rooms, anteroom airlocks
- **Department sizing**: By bed count, procedure volume, and throughput models
- **Wayfinding**: Clear circulation hierarchy; minimize decision points

### 5.4 Hotel Floor Plate

Hotel floor plate automation:

- **Room arrangement**: Double-loaded corridor (rooms on both sides) is most efficient
- **Room width**: Structural bay width (typically 3.6-4.2m standard, 7.2-8.4m for suite)
- **Room depth**: 6.0-8.0m for standard rooms
- **Service core placement**: Centralized or dual cores; housekeeping rooms per floor
- **Corner rooms**: Premium rooms, typically suites, require special planning
- **Corridor length**: Maximum ~60m between elevator lobby and last room (guest experience)
- **Back-of-house**: Service elevator, linen chute, housekeeping station, trash room

### 5.5 Parking Layout Optimization

Parking is highly amenable to automation:

- **Bay angle options**: 90 degrees (most dense), 60 degrees (easier maneuver), 45 degrees (one-way aisles), 0 degrees (parallel, least dense)
- **Stall dimensions**: 2.4m x 5.4m standard, 2.6m x 5.4m accessible
- **Aisle width**: 7.2m for 90-degree two-way, 5.5m for 60-degree one-way, 3.6m for parallel
- **Ramp placement**: Typically at perimeter; 12% max slope, 6% transition at top/bottom; 3.6m clear width per lane
- **Optimization objective**: Maximize stall count within site boundary
- **Algorithm**: Grid search over bay angle and aisle direction; evaluate count for each configuration
- **Structural grid**: 5.0m x 5.0m bays typical for parking; 8.1m x 5.0m for column-free spans
- **Accessible stalls**: 1 per 25 stalls minimum; van-accessible 1 per 6 accessible

### 5.6 Classroom/School Layout

School layout automation:

- **Classroom clusters**: Groups of 4-6 classrooms sharing a breakout space
- **Adjacency**: Classrooms near related labs; art/music with acoustic separation
- **Outdoor access**: Ground-floor classrooms with direct outdoor access (primary school)
- **Acoustic separation**: Music rooms and gymnasia separated from quiet classrooms (STC 55+ walls)
- **Supervision lines**: Staff offices with sightlines to corridors and play areas
- **Safe access**: Single controlled entry point; perimeter security
- **Hall/gymnasium**: Central location accessible from all classroom wings

---

## 6. Drawing Automation

### 6.1 Automated Floor Plan Generation from Spatial Data

Given a spatial model (rooms with geometry), automated floor plan production:

1. **Wall line generation**: Extract room boundaries, merge shared walls, assign wall types (exterior, interior, fire-rated)
2. **Door and window placement**: From openings in spatial model; apply standard sizes
3. **Fixture placement**: Bathroom fixtures, kitchen counters by room type templates
4. **Hatch/fill patterns**: Apply by material (concrete, tile, carpet) or by room type
5. **Line weight assignment**: By element type (heavy for cut walls, medium for furniture, light for ceiling grid)
6. **Annotation layer**: Room names, numbers, areas, door/window tags

### 6.2 Section and Elevation Generation

Automated sections and elevations:

- **Section cut placement**: At key locations (through stairs, through atrium, through typical bay)
- **Depth limiting**: Clip section depth to show relevant information only
- **Material hatching**: Auto-apply section hatches by material
- **Annotation**: Floor-to-floor heights, slab thicknesses, structural member sizes
- **Elevation generation**: Project facade elements; apply material annotations; dimension window/door openings

### 6.3 Detail Library Management and Auto-Placement

- **Standard detail library**: Organized by CSI division (02-Sitework, 03-Concrete, 04-Masonry, etc.)
- **Detail keying**: Each detail has a unique key (type + condition + material)
- **Auto-placement**: System identifies conditions in the model (e.g., wall-to-slab junction) and places the appropriate standard detail
- **Detail adaptation**: Parametric details adjust dimensions to match model conditions
- **Version control**: Detail library versioned; updates propagate to all projects

### 6.4 Annotation Automation

- **Dimension strings**: Auto-dimension structural grids, wall-to-wall, opening positions
- **Room tags**: Auto-place with room name, number, area, finish floor elevation
- **Door/window tags**: Auto-tag with mark number, type, size
- **Keynoting**: Auto-keynote materials by element type; generate keynote legend
- **Leader and callout placement**: Avoid overlaps using collision detection; route leaders to clear space
- **Coordination**: Ensure annotation does not overlap with drawing content

### 6.5 Sheet Layout Optimization

- **View-to-sheet assignment**: Assign views to sheets based on drawing set organization (plans on A-series, sections on A-series, details on A-series sub-sheets)
- **View placement**: Optimize view positions on sheets to minimize white space
- **Title block**: Auto-populate project info, sheet number, revision history
- **Sheet numbering**: Follow standard conventions (A1.01, A2.01, S1.01, etc.)
- **Cross-referencing**: Auto-update section markers, detail callouts, drawing references

### 6.6 Export Automation

- **Batch PDF export**: Export all sheets to PDF with naming convention
- **DWG export**: Export to DWG with layer mapping table (Revit layers → CAD layers)
- **Transmittal generation**: Auto-generate drawing list, revision log, transmittal cover sheet
- **Naming convention**: Project#-Discipline-SheetType-Number-Revision (e.g., 2024001-A-FP-101-R03.pdf)
- **Quality checks**: Verify all views are placed, all tags are filled, no empty sheets

### 6.7 Revit API for Drawing Automation

Key Revit API classes for drawing automation (C# / pyRevit / RevitPythonShell):

```python
# pyRevit example: Create sheets from Excel schedule
from Autodesk.Revit.DB import (
    FilteredElementCollector, ViewSheet,
    ViewFamilyType, Viewport
)

doc = __revit__.ActiveUIDocument.Document

# Get title block family type
title_blocks = FilteredElementCollector(doc) \
    .OfClass(FamilySymbol) \
    .OfCategory(BuiltInCategory.OST_TitleBlocks) \
    .ToElements()

# Create new sheet
with Transaction(doc, "Create Sheet") as t:
    t.Start()
    new_sheet = ViewSheet.Create(doc, title_blocks[0].Id)
    new_sheet.SheetNumber = "A1.01"
    new_sheet.Name = "FLOOR PLAN - LEVEL 1"

    # Place view on sheet
    view = get_view_by_name("Level 1 Floor Plan")
    viewport = Viewport.Create(doc, new_sheet.Id, view.Id, XYZ(0.4, 0.3, 0))
    t.Commit()
```

### 6.8 Dynamo for View/Sheet Management

Dynamo workflows for drawing automation:
- **Sheets.CreateByNumber**: Create sheets from list of numbers and names
- **Views.SetCropBox**: Auto-set crop regions based on room/level boundaries
- **Viewport.SetLocation**: Position viewports on sheets by coordinates
- **Element.SetParameterByName**: Batch-update parameters (scale, detail level, view template)
- **Data.ImportExcel**: Read sheet lists, room schedules, or parameter data from Excel

---

## 7. Code Compliance Checking

### 7.1 Building Code Automation: Egress

Automated egress checking is the most mature area of code compliance:

**Occupant load calculation**:
```
Occupant_Load = Floor_Area / Load_Factor

Load factors (IBC Table 1004.5):
- Assembly (chairs) = 0.65 m2/person
- Business = 9.3 m2/person
- Residential = 18.6 m2/person
- Educational = 1.9 m2/person
- Mercantile (ground floor) = 2.8 m2/person
```

**Exit requirements**:
- 1-500 occupants: minimum 2 exits
- 501-1000: minimum 3 exits
- 1001+: minimum 4 exits

**Exit width**:
```
Total_exit_width = Occupant_load * width_factor
  Stairways: 7.6 mm/person (sprinklered), 5.1 mm/person (unsprinklered) [IBC]
  Other egress: 5.0 mm/person (sprinklered), 3.8 mm/person (unsprinklered) [IBC]
Minimum single exit width: 810 mm (door), 1120 mm (corridor)
```

**Travel distance** (IBC Table 1017.2):
- Business, sprinklered: 90m (300 ft)
- Residential, sprinklered: 75m (250 ft)
- Assembly, sprinklered: 75m (250 ft)
- High hazard: 23m (75 ft)

**Common path of egress travel**: Maximum distance before two separate paths to exits are available. Typically 23m (75 ft).

### 7.2 Fire Safety Automation

- **Compartmentation**: Maximum compartment area by construction type (IBC Table 506.2). Auto-check that fire walls divide building into compliant compartments.
- **Fire resistance rating**: By construction type and element (IBC Table 601). Auto-assign to wall, floor, and roof assemblies.
- **Sprinkler coverage**: Maximum coverage area per sprinkler head (standard 12.1 m2, light hazard). Auto-generate sprinkler layout.
- **Fire separation distance**: Distance from building face to property line or adjacent building. Determines allowable opening percentage.
- **Smoke control**: Atrium smoke management, stair pressurization requirements.

### 7.3 Accessibility Automation

Key accessibility rules for automated checking:

- **Door clear width**: Minimum 815mm clear (ADA), 900mm (EN); auto-check all doors
- **Ramp grades**: Maximum 1:12 (8.3%); preferred 1:20 (5%); maximum rise 760mm per run; landings at top, bottom, and every 9m
- **Turning circles**: 1500mm diameter (ADA 1525mm) at all turns, at ends of corridors, in accessible rooms
- **Reach ranges**: Forward reach 380-1220mm; side reach 230-1370mm (ADA)
- **Accessible route**: Continuous accessible path from site entrance to all building functions; auto-trace and verify
- **Elevator requirements**: Buildings 3+ stories or 3000+ sq ft per floor require elevator
- **Accessible fixtures**: Toilet centerline 450-460mm from side wall; grab bars at 840-920mm; lavatory knee clearance 685mm

### 7.4 Zoning Compliance

Automated zoning checks:

- **Setback verification**: Measure from building face to property line; compare to required front, side, rear setbacks
- **Height limit**: Building height (grade to highest point) vs. zoning maximum; also story count limits
- **FAR calculation**: Floor Area Ratio = Gross Floor Area / Lot Area; compare to zoning maximum
- **Lot coverage**: Building footprint area / Lot area; compare to maximum
- **Parking requirements**: Required spaces by use type and area/unit count; compare to provided
- **Open space**: Required open space calculation; verify provided open space meets minimum

### 7.5 Daylight Compliance

- **Right to light**: Check that new construction does not reduce daylight to neighboring buildings below acceptable levels (BRE 209 method: VSC, NSL)
- **Daylight factor**: Minimum 2% average daylight factor for habitable rooms (UK standard); 1% minimum at any point
- **Window-to-floor ratio**: Minimum glazing area as percentage of floor area (varies by code; often 10-12.5%)
- **Automated checking**: From model geometry, calculate sky view factor at window; compare to threshold

### 7.6 Automated Compliance Report Generation

Generate structured compliance reports:

```
BUILDING CODE COMPLIANCE REPORT
Project: [Auto-fill from model]
Code: IBC 2021 / Local amendments
Date: [Auto-generate]

1. BUILDING CLASSIFICATION
   Occupancy: B (Business)
   Construction Type: IIA
   Height: 23.5m (< 55m allowed) ✓
   Stories: 6 (< 12 allowed) ✓
   Area per floor: 1,850 m2 (< 3,700 m2 allowed) ✓

2. EGRESS
   Floor 1: Occupant load 199, Required exits 2, Provided 3 ✓
   Floor 2: Occupant load 199, Required exits 2, Provided 2 ✓
   ...
   Max travel distance: 42.3m (< 90m) ✓
   Common path: 18.7m (< 23m) ✓

3. ACCESSIBILITY
   Accessible route: Continuous ✓
   Door clearances: All doors ≥ 815mm ✓
   Elevator provided: Yes ✓
   Accessible toilet: 1 per floor ✓
   ...

RESULT: 47/47 checks PASS, 0 FAIL, 3 ADVISORY
```

---

## 8. Computational Workflow Design

### 8.1 Workflow Orchestration Patterns

**Sequential**: Step A → Step B → Step C. Each step requires output of previous step.
Example: Site analysis → massing generation → energy simulation → report.

**Parallel**: Steps A, B, C run simultaneously; results merged at sync point.
Example: Structural analysis, energy analysis, daylight analysis run in parallel; results combined in dashboard.

**Conditional branching**: IF condition THEN path A ELSE path B.
Example: IF building height > 23m THEN high-rise structural system ELSE conventional framing.

**Iterative loop**: Repeat steps until convergence or max iterations.
Example: Adjust facade WWR → run energy simulation → check EUI target → if not met, adjust again.

**Fan-out/fan-in**: Generate N variants (fan-out) → evaluate all → select best (fan-in).
Example: Generate 100 floor plan options → score each → present top 10.

### 8.2 Workflow Engines for AEC

| Engine | Language | Strengths | AEC Use |
|--------|----------|-----------|---------|
| Grasshopper | Visual/C# | Visual, real-time preview, huge plugin ecosystem | Parametric geometry, environmental analysis, optimization |
| Dynamo | Visual/Python | Revit integration, BIM automation | Drawing automation, model checking, data management |
| Speckle Automate | Python/C# | Cloud-native, event-driven, BIM data | Automated model checks, data transformations |
| n8n | Node.js | API integration, webhook triggers | Multi-tool orchestration, notification pipelines |
| Apache Airflow | Python | DAG-based, scalable, monitoring | Large-scale batch processing, simulation farms |
| Prefect | Python | Modern Airflow alternative, easy debugging | ML pipeline orchestration |
| Custom Python | Python | Full control, any library | Complex multi-step automation |

### 8.3 Error Handling in Automated Workflows

Robust automation requires comprehensive error handling:

1. **Input validation**: Check all inputs before processing (file existence, data types, value ranges)
2. **Graceful degradation**: If optional step fails, continue with defaults
3. **Retry logic**: Transient failures (network, license server) retry with exponential backoff
4. **Fallback strategies**: If primary method fails, use alternative method
5. **Error logging**: Record all errors with context (timestamp, inputs, stack trace)
6. **User notification**: Alert user to failures requiring human intervention
7. **Checkpoint/restart**: Save intermediate results; resume from last checkpoint after failure

### 8.4 Logging and Audit Trails

Design automation must maintain audit trails for:
- Professional liability (documenting design decisions)
- Quality assurance (tracing errors to source)
- Regulatory compliance (demonstrating code compliance process)
- Knowledge management (understanding why decisions were made)

Log levels: DEBUG (detailed computation), INFO (workflow steps), WARNING (non-critical issues), ERROR (failures), CRITICAL (system failures).

### 8.5 Version Control for Workflows

- Store Grasshopper definitions in Git (`.gh` files are binary; use `.ghx` XML format for diffing)
- Dynamo graphs: `.dyn` files are JSON; store in Git with meaningful commit messages
- Python scripts: Standard Git workflow with branching, code review
- Rule libraries: Version rule sets independently from code; track code edition and amendment dates
- Template libraries: Version parametric detail templates with semantic versioning

---

## 9. Design Automation Case Studies

### 9.1 Automated Facade Design

**Pipeline**: Solar analysis → shading device sizing → panel generation → fabrication data

1. **Solar analysis**: Run annual solar radiation simulation on facade surfaces (Ladybug/Honeybee or custom raytracing). Output: radiation map (kWh/m2/yr) per facade cell.
2. **Shading device sizing**: For each cell, calculate required shading depth based on radiation and orientation:
   ```
   shade_depth = window_height * tan(critical_sun_angle) * shading_factor
   critical_sun_angle = solar altitude at cooling design day peak
   ```
3. **Panel generation**: Generate facade panel geometry with sized shading devices. Apply panel types from a limited palette (e.g., 4-5 fin depths) for constructability.
4. **Structural check**: Verify fin depth/projection within structural capacity of facade framing.
5. **Fabrication data**: Export panel schedule with dimensions, material, finish. Generate CNC cutting files for custom panels. Output IFC model for coordination.

**Result**: 3000 unique panels documented in 2 hours instead of 2 weeks.

### 9.2 Automated Parking Garage

**Pipeline**: Site boundary → ramp placement → bay layout → structural grid → count verification

1. **Input**: Site boundary polygon, required stall count, entry/exit locations, floor-to-floor height
2. **Ramp placement**: Test ramp locations at site perimeter and interior; evaluate traffic flow for each
3. **Bay layout**: For each ramp configuration, run parking layout algorithm:
   - Try 90-degree bays along long axis, then short axis
   - Try 60-degree bays if count is not met
   - Evaluate: stall count, aisle efficiency, dead-end length
4. **Structural grid**: Overlay structural grid aligned with parking bays (typically 5.0 x 8.1m or 5.0 x 16.2m for long-span)
5. **Count verification**: Total stalls per level x number of levels; check against requirement
6. **Accessible stalls**: Place required accessible stalls near elevators
7. **Output**: Floor plans, sections, stall count schedule, structural grid drawing

### 9.3 Automated Residential Tower

**Pipeline**: Unit type library → floor plate stacking → core placement → code checking

1. **Unit type library**: Pre-designed unit types with variants:
   - Studio (28-35 m2): 3 variants
   - 1-bed (45-60 m2): 4 variants
   - 2-bed (70-90 m2): 5 variants
   - 3-bed (95-120 m2): 3 variants
   - Penthouse (150-250 m2): 2 variants
2. **Floor plate definition**: Building footprint from massing model; structural grid
3. **Core placement**: Position cores (elevator, stairs, shafts) considering structural, egress, and efficiency requirements
4. **Unit arrangement**: Pack unit types into floor plate around core; maximize units per floor; ensure all units have exterior windows; check corridor length
5. **Stacking**: Assign unit types to floors; align wet walls vertically; vary unit mix by floor level
6. **Code checking**: Run automated egress, fire safety, accessibility, and daylight compliance checks
7. **Output**: Typical floor plans, unit mix schedule, area tabulation, compliance report

### 9.4 Automated Site Grading

**Pipeline**: Topography → cut/fill optimization → drainage design → retaining wall placement

1. **Topographic input**: Point cloud or contour data → TIN surface
2. **Design constraints**: Building pad elevation, access road grades (max 8%), parking areas (max 5%), ADA paths (max 5%), minimum drainage slope (1%)
3. **Cut/fill optimization**: Linear programming to balance cut and fill volumes (minimize import/export). Variables: finished grade elevations at grid points. Constraints: max/min grades, building pad, road connections.
4. **Drainage design**: Identify watersheds on finished grade; route overland flow to retention areas; size drainage infrastructure
5. **Retaining walls**: Where grade change between adjacent areas exceeds safe slope (typically 1:3 or 1:2), insert retaining wall. Size wall by height and soil conditions.
6. **Output**: Grading plan with spot elevations, cut/fill quantity table, drainage plan, retaining wall schedule

### 9.5 Automated MEP Routing

**Pipeline**: Room requirements → duct/pipe sizing → route generation → clash detection

1. **Room requirements**: From room program, determine:
   - Airflow (CFM/L/s) based on occupancy and use
   - Heating/cooling loads (kW)
   - Plumbing fixture count
   - Electrical load (kW)
2. **Duct sizing**: Calculate duct dimensions from airflow using equal friction method:
   ```
   duct_area = airflow / velocity
   velocity: main duct 6-10 m/s, branch 3-6 m/s
   friction_rate: 0.8-1.2 Pa/m (low velocity), 1.5-2.5 Pa/m (high velocity)
   ```
3. **Route generation**: A* pathfinding on 3D grid from AHU to terminal units. Cost function includes: path length, number of bends (fittings), vertical elevation changes, proximity to structure (hanger points).
4. **Collision avoidance**: Route ducts to avoid structural members, other services. Priority: gravity drains > pressurized pipes > supply ducts > return ducts > cable trays.
5. **Clash detection**: Check all service routes against structure and each other. Report clashes with location and clearance required.
6. **Output**: 3D duct/pipe model, routing diagrams, duct/pipe schedules, clash report

---

## Key Design Automation Principles

1. **Automate the boring, not the creative**: Focus automation on repetitive, rule-based tasks. Leave conceptual design to humans.
2. **Start with the constraint, not the solution**: Model the problem as constraints first; let the solver find solutions.
3. **Validate early and often**: Check outputs against requirements at every step; do not accumulate errors.
4. **Design for maintenance**: Rules change (code updates, new standards). Build rule systems that are easy to update.
5. **Transparency over black boxes**: Designers must understand and trust the automation. Show reasoning, not just results.
6. **Graceful degradation**: When automation fails or produces poor results, fall back to manual workflow without data loss.
7. **Measure what matters**: Track automation ROI: time saved, error reduction, design quality improvement.

---

## Tools and Technologies

| Category | Tools |
|----------|-------|
| Rule engines | Drools, NRules, durable-rules, custom Python |
| CSP solvers | Google OR-Tools, python-constraint, MiniZinc |
| Optimization | Galapagos (GH), Optimus (GH), scipy.optimize, pymoo |
| Workflow | Grasshopper, Dynamo, Speckle Automate, Airflow, n8n |
| Drawing automation | Revit API, pyRevit, Dynamo, OpenBIM (IFC) |
| Compliance checking | Solibri, SMC, custom rule engines, BIM Checker |
| Space planning | Archilogic, Finch, depthmapX, custom solvers |
| Version control | Git, GitHub/GitLab, Speckle (model versioning) |
