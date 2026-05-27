---
name: sports-tracker
description: Sport- und Fitness-Tracking mit P90X, Fahrrad, Wandern, Laufen. SQLite-basiert mit automatischem Komoot-Import, Berichten (Woche, Monat), Emoji-Visualisierung, Kalorien-Berechnung und Workout-Tracking.
---

# Sports Tracker v2.0

Track P90X workouts, cycling, hiking, running with SQLite, CLI reports, automatic calorie calculation, and automated Komoot tour import.

## Features

- **Manual Logging** - Log activities via CLI with automatic calorie calculation
- **Automated Komoot Import** - Fetches and imports tours automatically (every 4h)
- **Auto-Calorie Calculation** - Based on MET × weight × duration
- **Workout Tracking** - Training day management (Mon/Wed/Fri)
- **GPX Export** - Download GPX data from Komoot tours
- **Multi-format Reports** - Weekly, monthly, detailed stats
- **Dedup** - Prevents duplicate imports via Komoot tour ID

## CLI Usage

```bash
# Initialize / migrate database (safe to run on existing DB)
python3 skills/sports-tracker/scripts/sports_tracker.py --init

# ─── Add activities (auto-calculates calories) ───
python3 skills/sports-tracker/scripts/sports_tracker.py --add "5 km Wandern"
python3 skills/sports-tracker/scripts/sports_tracker.py --add "P90X"
python3 skills/sports-tracker/scripts/sports_tracker.py --add "P90X 45 min"
python3 skills/sports-tracker/scripts/sports_tracker.py --add "17.7 km Fahrrad"
python3 skills/sports-tracker/scripts/sports_tracker.py --add "5 km Wandern gestern"

# ─── Weight management ───
python3 skills/sports-tracker/scripts/sports_tracker.py --weight 115

# ─── Reports ───
python3 skills/sports-tracker/scripts/sports_tracker.py --week
python3 skills/sports-tracker/scripts/sports_tracker.py --month
python3 skills/sports-tracker/scripts/sports_tracker.py --month-full
python3 skills/sports-tracker/scripts/sports_tracker.py --list
python3 skills/sports-tracker/scripts/sports_tracker.py --stats

# ─── Workout Tracking (P90X) ───
python3 skills/sports-tracker/scripts/sports_tracker.py --done
python3 skills/sports-tracker/scripts/sports_tracker.py --done P90X3
python3 skills/sports-tracker/scripts/sports_tracker.py --missed
python3 skills/sports-tracker/scripts/sports_tracker.py --workout-status
python3 skills/sports-tracker/scripts/sports_tracker.py --workout-check
python3 skills/sports-tracker/scripts/sports_tracker.py --workout-stats

# ─── Komoot Import ───
python3 skills/sports-tracker/scripts/komoot_import.py
python3 skills/sports-tracker/scripts/komoot_import.py --full
python3 skills/sports-tracker/scripts/komoot_import.py --dry-run
python3 skills/sports-tracker/scripts/komoot_import.py --export-gpx
```

## Categories

| Category | Value type | Type | Emoji |
|----------|-----------|------|-------|
| P90X     | done (session count) | strength | 💪 |
| Fahrrad  | km        | cardio | 🚴 |
| Spazieren | km        | cardio | 🥾 |
| Laufen   | km        | cardio | 🏃 |

## Calorie Calculation (Automatic)

Formula: `Kcal = MET × weight_kg × duration_hours`

| Activity | MET | Speed | Duration Calculation |
|----------|-----|-------|---------------------|
| Fahrrad  | 8.0 | 18 km/h | `km / 18` hours |
| Wandern  | 3.5 | 4.5 km/h | `km / 4.5` hours |
| P90X     | 6.0 | — | 60 min (default) or specified |

**Default weight:** 120 kg (configurable via `--weight`)

## Komoot Import Details

The `komoot_import.py` script connects to the Komoot API and imports tours into the sports tracker database.

### What gets imported

- Distance in km
- Duration in minutes
- Calories via MET formula
- Elevation gain/loss in meters
- Average and max speed
- Sport type mapped to tracker categories

### Komoot Sport-Type Mapping

| Komoot Type | Sports Tracker |
|------------|---------------|
| touring_cycling, cycling, mtb, race_cycling | Fahrrad |
| hiking, hike | Spazieren |
| walking, walk, nordic_walking | Wandern |
| running, run, trail_running | Laufen |
| skiing, ski_touring, snowboard | Skifahren |

### Setup

Add to `.env`:
```bash
KOMOOT_EMAIL=your@email.com
KOMOOT_PASSWORD=your_password
KOMOOT_USER_ID=your_user_id
```

## Database

Path: `data/sports_tracker.db`

### Tables

**activities** (main tracking)

| Column      | Type    | Description |
|-------------|---------|-------------|
| id          | INTEGER | Primary key |
| date        | TEXT    | Activity date |
| category    | TEXT    | Activity category |
| value       | TEXT    | km or "done" |
| description | TEXT    | Activity description |
| created_at  | TEXT    | Timestamp |
| type        | TEXT    | 'cardio' or 'strength' |
| duration_min| INTEGER | Duration in minutes |
| calories    | INTEGER | Calculated calories |
| speed_kmh   | REAL    | Average speed |
| weight_kg   | REAL    | Weight at time of activity |

**workout_status** (P90X tracking)

| Column | Type | Description |
|--------|------|-------------|
| date    | TEXT | Unique date |
| is_training_day | BOOLEAN | Mo/We/Fr = true |
| status  | TEXT | done, missed, rest, pending |
| type    | TEXT | P90X, P90X2, P90X3 |
| notes   | TEXT | Notes |

**user_settings** (key/value store)

| Key | Default | Description |
|-----|---------|-------------|
| weight_kg | 120 | Current weight |

## Workout Rules

- **Training days:** Monday, Wednesday, Friday
- **Rest days:** Tuesday, Thursday, Saturday, Sunday
- "done" on training day or next day = counted as trained
- **Sarcasm trigger:** 2+ missed training days in last 14 days

## Date Parsing

Recognizes German phrases:
- `heute` → today
- `gestern` → yesterday
- `vorgestern` → day before yesterday
- `DD.MM.YYYY` → explicit date

## Migration

`--init` safely migrates existing v1 databases to v2 without data loss:
- Adds new columns (`type`, `duration_min`, `calories`, `speed_kmh`, `weight_kg`)
- Creates `workout_status`, `workout_rules`, and `user_settings` tables
- Preserves all existing activity data
