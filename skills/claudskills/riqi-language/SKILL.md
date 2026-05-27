---
name: RiQi Language Development
description: Panduan pengembangan bahasa pemrograman RiQi — smart contract language yang dirancang security-first untuk blockchain Skylum, mencakup compiler, VM, static analyzer, dan optimization engine.
---

# 🔤 RiQi Language Development Skill

## Tujuan
Skill ini memberikan panduan lengkap untuk pengembangan **bahasa pemrograman RiQi** — bahasa smart contract kustom yang dirancang dengan prinsip keamanan-pertama (*security-first*) untuk blockchain Skylum.

## Scope
- `riqi_compiler/` — Compiler utama (lexer, parser, codegen)
- `riqi_code/` — Runtime & opcode definitions
- `riqi-lang/compiler/` — Compiler frontend
- `riqi-lang/vm/` — Virtual Machine
- `riqi-lang/static-analyzer/` — Static analysis tools
- `riqi-lang/optimization-engine/` — Bytecode optimization
- `riqi-lang/vscode-extension/` — VS Code language support
- `riqi-lang/examples/` — Contoh kode RiQi

---

## 📐 Filosofi Desain Bahasa

### Prinsip Utama
1. **Aman Secara Default** — Variabel immutable by default, checked arithmetic bawaan
2. **Eksplisit dan Jelas** — Tidak ada konversi tipe tersembunyi
3. **Manajemen State Ketat** — Ownership & borrowing (terinspirasi Rust)
4. **Integrasi Protokol** — Sintaksis native untuk fitur blockchain Skylum

### Fitur Keamanan Kunci
| Fitur | Detail |
|-------|--------|
| Immutability Default | `let x = 5;` → immutable. `let mut x = 5;` → mutable |
| View/Exec Separation | `fn get() view { }` vs `fn set() exec { }` |
| No While Loops | Hanya `for item in collection` — mencegah infinite loop |
| Checked Arithmetic | Integer overflow/underflow detection bawaan |
| Re-entrancy Guard | Ownership model mencegah re-entrancy attack |

---

## 🏗️ Arsitektur Compiler Pipeline

```
Source Code (.rq)
    │
    ▼
┌──────────┐
│  Lexer   │ → Token stream
└──────────┘
    │
    ▼
┌──────────┐
│  Parser  │ → AST (Abstract Syntax Tree)
└──────────┘
    │
    ▼
┌────────────────┐
│ Static Analyzer│ → Warnings, errors, security checks
└────────────────┘
    │
    ▼
┌──────────────────┐
│ Optimization     │ → Optimized AST
│ Engine           │
└──────────────────┘
    │
    ▼
┌──────────────┐
│ Code Generator│ → Bytecode for Skylum VM
└──────────────┘
    │
    ▼
┌──────────────┐
│  Skylum VM   │ → Execution on-chain
└──────────────┘
```

---

## 📝 Sintaksis RiQi (Referensi Cepat)

### Deklarasi Variabel
```riqi
// Immutable (default, aman)
let nama_proyek: string = "Proyek Skylum";
let versi: uint = 1;

// Mutable (harus eksplisit)
let mut counter: uint = 0;
counter = counter + 1; // Valid
```

### Struct
```riqi
struct InfoRoyalti {
    penerima: Alamat,
    persentase: uint16
}

struct AsetUnik {
    id: uint,
    pemilik: Alamat,
    royalti: InfoRoyalti
}
```

### Fungsi (View vs Exec)
```riqi
// Read-only function (tidak bisa mengubah state)
fn dapatkan_info(id: uint) -> AsetUnik view {
    // ... hanya baca state ...
}

// State-changing function
fn transfer_aset(id: uint, pemilik_baru: Alamat) -> bool exec {
    // ... bisa mengubah state ...
}
```

### Control Flow
```riqi
// If/Else
if (kondisi) {
    // ...
} else {
    // ...
}

// For loop (SATU-SATUNYA jenis loop yang diizinkan)
for item in koleksi {
    // ...
}
```

---

## 🔧 Aturan Pengembangan

### 1. Compiler Development
- Setiap fase compiler harus punya **comprehensive error messages** (bukan generic errors)
- Error harus menunjuk lokasi pasti di source code (line + column)
- Setiap token/AST node harus menyimpan informasi `Span` (posisi dalam source)

### 2. VM Development
- Setiap opcode harus punya **gas cost** yang terdefinisi
- Stack-based VM (mirip EVM, bukan register-based)
- Opcode yang wajib ada:
  - `OP_PUSH`, `OP_POP` — Stack manipulation
  - `OP_ADD`, `OP_SUB`, `OP_MUL`, `OP_DIV` — Arithmetic
  - `OP_SSTORE`, `OP_SLOAD` — State storage (PRIORITAS FASE 8)
  - `OP_JUMP`, `OP_JUMPI` — Control flow
  - `OP_CALL` — External contract call
  - `OP_RETURN` — Return value
  - `OP_REVERT` — Revert transaction
  - `OP_MINT_ASSET` — Native asset minting (protocol integration)

### 3. Static Analyzer
- Detect unused variables
- Detect potential overflow conditions
- Detect state modification in `view` functions
- Detect missing error handling
- Enforce naming conventions

### 4. Testing
- Setiap contoh di `riqi-lang/examples/` harus bisa dikompilasi dan dijalankan
- Test error cases (invalid syntax, type mismatch, dll.)
- Benchmark gas consumption untuk operasi umum

---

## 📋 Status Pengerjaan (Fase 8 Roadmap)
- [ ] `OP_SSTORE` / `OP_SLOAD` — State storage opcodes
- [ ] `if/else` logic di VM level
- [ ] Fitur keamanan: aturan `mut` dan `view/exec` di level compiler
- [ ] Inter-contract calls (`OP_CALL`)
- [ ] Standar `ASSET_SALE_TRANSFER` di level bahasa
