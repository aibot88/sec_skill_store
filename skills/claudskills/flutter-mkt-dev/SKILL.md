---
name: flutter-mkt-dev
description: "Flutter development skill for Miqotul Khoir TV (MKT) project. Use for: implementing new Flutter features, fixing UI bugs, modifying widgets, creating Cubit state management, working with Android TV D-Pad navigation, debugging widget issues, adding touch/gesture support, editing DPadStepper or GlassmorphismCard, working in Clean Architecture layers (domain/data/presentation), writing dart widget or unit tests. Knows: ScreenUtil, Cubit/BLoC, Islamic Glassmorphism theme, SQLite offline-first, prayer time calculation."
argument-hint: "Describe the feature or bug you want to work on"
---

# Flutter MKT Development

## Project Summary

**Miqotul Khoir TV (MKT)** — Aplikasi jam masjid digital dan jadwal sholat untuk Android TV.

- **Platform**: Android TV (API 24+), landscape 1920×1080, D-Pad navigation
- **State Management**: Cubit (flutter_bloc)
- **Architecture**: Clean Architecture (domain → data → presentation)
- **Theme**: Islamic Glassmorphism (emerald `#004D40` + gold `#FFD700`)
- **Data**: SQLite offline-first (sqflite), no network calls
- **Responsive**: `flutter_screenutil` — gunakan `.sp`, `.w`, `.h`, `.r` untuk semua sizing

For complete conventions, see [AGENTS.md](../../../AGENTS.md).

---

## Architecture Layer Rules

```
lib/
├── domain/         ← Entities, Use Cases, Repository Interfaces (ZERO framework imports)
├── data/           ← Models, DataSources, Repository Implementations (SQLite)
└── presentation/
    ├── cubits/     ← State management (Cubit + State classes)
    ├── pages/      ← Page widgets (section-based layout)
    └── widgets/    ← Reusable widgets (DPadStepper, GlassmorphismCard, etc.)
```

**Dependency Rule**: Hanya outer layer yang boleh import inner layer. Domain tidak boleh import Flutter framework.

---

## Workflow: Bug Fix UI

### 1. Analyze (Read First, Code Second)

Sebelum menyentuh kode apapun:

1. Baca file yang relevan dengan `read_file`
2. Identifikasi **root cause** — jangan langsung fix tanpa memahami penyebab
3. Presentasikan analisis kepada user dengan format:
   - **Root Cause** — apa yang menyebabkan masalah
   - **Ringkasan Temuan** — tabel komponen yang bermasalah vs yang perlu diubah
   - **Strategi Perbaikan** — perubahan minimal yang cukup
4. Tunggu konfirmasi user sebelum implementasi

### 2. Implement (Surgical Changes)

- Gunakan `manage_todo_list` untuk task multi-step
- Buat perubahan **seminimal mungkin** — jangan refactor kode yang tidak diminta
- Gunakan `multi_replace_string_in_file` untuk perubahan yang sudah pasti
- Untuk perubahan di widget: sertakan 3–5 baris konteks sebelum dan sesudah

### 3. Validate

```bash
# Setelah edit, selalu jalankan:
dart analyze lib/path/to/file.dart
```

Atau gunakan `get_errors` pada file yang diedit. Pastikan zero errors sebelum selesai.

---

## Workflow: Implementasi Fitur Baru

Ikuti urutan fase SDLC:

| Fase              | Agent                          | Output                   |
| ----------------- | ------------------------------ | ------------------------ |
| 1. Requirements   | `@ProductManagerPRD`           | PRD document             |
| 2. Specification  | `@SpecificationArchitect`      | Spec document di `spec/` |
| 3. Planning       | `@PlannerArchitect`            | Plan document di `plan/` |
| 4. Implementation | `@BeastModeDev` / `@MiniBeast` | Code + tests             |
| 5. Testing        | `@QATestArchitect`             | Test verification        |

**Jangan skip fase.** Setiap fase harus selesai sebelum lanjut.

---

## Workflow: Membuat / Mengedit Widget

### Checklist Widget Android TV

- [ ] Icon/button size minimal `44.sp` (touch target)
- [ ] Padding minimal `8.r` di sekeliling interactive elements
- [ ] Semua interactive element dibungkus `Focus` atau `FocusableWidget`
- [ ] `GestureDetector` untuk touch, `onKeyEvent` untuk D-Pad — keduanya harus ada
- [ ] Long press support: `onLongPressStart` / `onLongPressEnd` untuk stepper/spinner
- [ ] Dispose timer di `dispose()` jika ada `Timer` atau `AnimationController`
- [ ] Gunakan `const` constructor bila memungkinkan
- [ ] Sizing via `flutter_screenutil`: `.sp` font, `.w/.h` box, `.r` radius/padding

### Pattern: Touch + D-Pad Stepper

```dart
// ✅ Pattern yang benar untuk icon yang bisa touch DAN D-Pad
GestureDetector(
  onTap: _decrement,
  onLongPressStart: (_) => _startTimer(false),
  onLongPressEnd: (_) => _cancelTimer(),
  child: Padding(
    padding: EdgeInsets.all(8.r),  // tap target lebih besar
    child: Icon(Icons.remove_circle_outline, size: 44.sp),
  ),
),
```

### Pattern: GlassmorphismCard

```dart
GlassmorphismCard(
  isFocused: isFocused,
  padding: EdgeInsets.symmetric(horizontal: 24.w, vertical: 16.h),
  child: ...,
)
```

### Pattern: IslamicTypography

```dart
IslamicTypography.heading()      // Title besar (section header)
IslamicTypography.title()        // Bold medium (value display)
IslamicTypography.body()         // Body text
IslamicTypography.subtitle()     // Keterangan/deskripsi kecil
```

---

## Workflow: Cubit Baru

1. **State file** (`feature_state.dart`): extend `Equatable`, define states
2. **Cubit file** (`feature_cubit.dart`): extend `Cubit<FeatureState>`, inject repository
3. **Barrel file** (`feature.dart`): export keduanya
4. **Test file** (`test/presentation/cubits/feature/feature_cubit_test.dart`): gunakan `bloc_test` + `mocktail`

```
lib/presentation/cubits/feature_name/
├── feature_state.dart
├── feature_cubit.dart
└── feature.dart          ← barrel export
```

---

## Testing

### Menjalankan Tests

```bash
# Semua tests (required format)
flutter test --reporter=expanded

# File tertentu
flutter test test/presentation/widgets/dpad_stepper_test.dart --reporter=expanded

# Satu directory
flutter test test/presentation/ --reporter=expanded
```

### Checklist Sebelum Commit

```bash
dart format .            # Format kode
dart analyze             # Zero warnings/errors
flutter test             # Semua tests pass
```

### SQLite Test Pattern

Gunakan `sqflite_common_ffi` dengan `inMemoryDatabasePath` — jangan gunakan database file asli di tests.

```dart
setUp(() async {
  sqfliteFfiInit();
  databaseFactory = databaseFactoryFfi;
  await DatabaseHelper.instance.initForTesting();
});
```

---

## Common Pitfalls

### Timer Memory Leak

```dart
// ✅ Selalu cancel timer di dispose()
@override
void dispose() {
  _timer?.cancel();
  super.dispose();
}
```

### setState pada Unmounted Widget

```dart
// ✅ Cek mounted sebelum setState
if (mounted) setState(() {});
```

### SQLite Transaction

```dart
// ✅ Selalu wrap multiple writes dalam transaction
await db.transaction((txn) async {
  await txn.update('settings', data, where: 'id = ?', whereArgs: [1]);
});
```

---

## Key Files

| File                                                   | Keterangan                   |
| ------------------------------------------------------ | ---------------------------- |
| `lib/presentation/widgets/dpad_stepper.dart`           | Stepper widget (nilai + / −) |
| `lib/presentation/widgets/focusable_widget.dart`       | D-Pad focus wrapper          |
| `lib/presentation/widgets/glassmorphism_card.dart`     | Glassmorphism card container |
| `lib/core/theme/islamic_colors.dart`                   | Color constants              |
| `lib/core/theme/islamic_typography.dart`               | Text style factory           |
| `lib/data/datasources/database_helper.dart`            | SQLite singleton             |
| `lib/domain/entities/settings.dart`                    | Settings entity              |
| `lib/presentation/cubits/settings/settings_cubit.dart` | Settings state management    |

---

## Git Policy

**DILARANG** commit/push otomatis. Selalu jelaskan perubahan dan minta konfirmasi eksplisit dari user sebelum `git commit`.

Format commit:

```
feat(widget): add touch support to DPadStepper buttons

- Wrap - and + icons with GestureDetector
- Support onTap (single) and onLongPress (hold-to-repeat)
- Increase icon size from 32.sp to 44.sp for better tap target
```
