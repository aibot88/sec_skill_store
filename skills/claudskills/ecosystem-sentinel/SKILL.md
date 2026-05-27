---
name: Ecosystem Sentinel & Automation Auditor
description: >
  - **Nexus Orchestration**: Ability to lead the **Nexus War Room** and delegate sub-tasks to OpenClaw, Qwen, or DeepSeek via the `agents_vault`. Maintains a high-level architectural view while using **Nexus Monitor** for passive ecosystem oversight.
  - **Anti-Hallucination Mandate (v3.43.0)**: Mandatory **Pre-Flight Env Audit** before ANY task using `node scripts/audits/check_sync_status.cjs`. Agents MUST follow the **Clean-Pipe Sync Protocol** via `robust_sync.cjs`.
  - **Master Architect Alignment**: Primary enforcer of the `DISCO_DAILY_MASTER_PRD.md` as the absolute source of truth.
  - **LLM Evolution Auditor**: Periodically audits model performance and recommends switching to newer, smarter LLMs if available. Protokol untuk audit kode otomatis, manajemen versi (upgrading), pemeriksaan fitur live (Vercel), sinkronisasi total antara Contract-Database-UX/UI (Senior Web3 UI/UX Staff Engineer Standards), Build Pipeline Guard, dan **Nexus Monitor Privacy Lockdown**.
---

### 🛡️ LOCAL HARDWARE OPTIMIZATION (Mandatory)
Target System: Intel(R) Core(TM) i5-4210U CPU @ 1.70GHz (Dual-Core) / 16GB RAM.

**Rules for Local Development (Environment-Aware):**
> [!IMPORTANT]
> Aturan ini **HANYA** berlaku saat running secara lokal (laptop user). Pengecekan dilakukan via `isLocalDev` (NODE_ENV=development && !VERCEL). Cloud Hosting (Vercel/VPS) akan tetap mendapatkan full performance standar.

1.  **Lightweight Vite**: Optimasi `vite.config.js` dengan `ignored` monitoring hanya aktif di lokal.
2.  **Reduced Polling**: Interval polling worker script lokal diset ke **>= 30 detik**. Di VPS/Cloud, interval bisa lebih cepat (5-10 detik).
3.  **Clean Shutdown**: Handler `SIGINT`/`SIGTERM` tetap dipertahankan di semua env karena ini best practice Node.js.
4.  **Build Guards**: Plugin berat otomatis didisable di lokal kecuali dibutuhkan.
5.  **Local Server Resource Hygiene**: SELALU matikan (terminate) server lokal (Express, Vite, etc.) sesaat setelah verifikasi manual selesai. Jangan biarkan proses Node.js menggantung di background untuk menghemat resource CPU/RAM (i5-4210U).

5.  **Vercel Hobby Plan Guard (Profit-First Strategy)**:
    - **API Consolidation Mandate**: Seluruh fitur API baru **WAJIB** masuk ke dalam bundle yang sudah ada (`admin-bundle.js`, `user-bundle.js`, `tasks-bundle.js`, `audit-bundle.js`).
    - **Limit 12 Fungsi**: Jumlah Serverless Functions di Vercel **TIDAK BOLEH** melebihi 12 fungsi untuk menghindari biaya sebelum project mencapai PnL positif (Profit). Jika fitur baru membutuhkan endpoint baru, konsolidasi fungsionalitas ke dalam bundle yang relevan.
    - **Folder API Root-Only**: Hindari pembuatan sub-folder dalam `api/`. Gunakan flat structure dan bundle logic di level root `api/`.

6.  **Activity Log & UGC Standard (Profit-First History)**:
    - **user_activity_logs**: Seluruh riwayat aksi user (XP, Purchase, Reward) **WAJIB** dicatat di tabel `user_activity_logs`.
- [ ] Verify `user_activity_logs` population for UGC.
- [ ] Verify UGC Moderation Parity (`is_active: false` for Raffles/Missions by default) (v3.39.1).
- [ ] Verify Hardened `get_auth_wallet()` pattern to prevent RLS spoofing (v3.39.1).
- [ ] Verify `Point-Sync` for all rewards (dynamic fetch vs hardcode).
    - [ ] Verify `Zero-Hardcode` compliance across the entire feature set.
    - [ ] Check Vercel Function Count (Stay < 12).
    - [ ] **✨ ADMIN SYSTEM HARDENING & ABI SYNC AUDIT (v3.42.8)**:
        - [ ] Verify `TaskList.jsx` uses `String()` for all ID comparisons.
        - [ ] Verify primary action buttons use Indigo transparent/border and NO icons.
        - [ ] Verify layout uses `overflow-x-hidden` and `max-w-[100vw]` for mobile.
        - [ ] Verify `handleClaim` forces `fetchData()` on "already completed" errors.
    - **UGC Tracking**: Aksi User Generated Content (Mission Creation, Raffle Launch, Sponsorship Renewal) **WAJIB** memicu log dengan kategori `PURCHASE` dan menyertakan `tx_hash` serta metadata lengkap.
    - **Frontend Reporting**: Gunakan `ActivityLogSection.jsx` untuk menampilkan riwayat ini di profil user secara real-time.

# Ecosystem Sentinel & Master Architect Enforcer

---

## 📄 PRD LIVING DOCUMENT MANDATE (TASK UTAMA)

> [!IMPORTANT]
> **PRD adalah dokumen hidup (living document) yang merupakan task utama selama seluruh siklus pengembangan aplikasi.** Setiap agent WAJIB merujuk, memverifikasi, dan memperbarui PRD secara konsisten.

### 📍 Lokasi Kanonik PRD
**File:** `e:\Disco Gacha\Disco_DailyApp\PRD\DISCO_DAILY_MASTER_PRD.md`
(Versi lama diarsipkan di `PRD/_archive/`)

### ⚠️ Aturan Wajib PRD (PRD Enforcement Protocol)

1.  **Baca PRD Sebelum Fitur Baru**: Setiap kali memulai fitur atau modul baru, Agent **WAJIB** membaca seksi PRD yang relevan terlebih dahulu untuk memastikan implementasi sesuai spesifikasi.

2.  **Update PRD Setelah Perubahan Fitur**: Setiap perubahan signifikan pada fitur (new page, baru contract, endpoint baru, perubahan ekonomi) **WAJIB** diikuti update pada PRD di seksi yang relevan. Tidak boleh ada fitur yang berjalan di production tetapi tidak terdokumentasi di PRD.

3.  **PRD sebagai Source of Truth**: Jika ada konflik antara kode dan PRD, **PRD yang harus diperbarui** (jika kode memang sudah diubah secara sengaja) atau **kode yang harus diperbaiki** (jika kode menyimpang dari spesifikasi tanpa alasan). Agent harus mengklarifikasi ke user sebelum memutuskan.

4.  **Sinkronisasi PRD dengan .cursorrules**: Setiap update kontrak, alamat, atau protokol di `.cursorrules` **WAJIB** tercermin juga di seksi "Arsitektur Sistem" dalam PRD.

5.  **Checklist PRD per Sesi**: Dalam setiap sesi kerja, Agent wajib menjalankan mini-audit PRD:
    - [ ] Apakah ada fitur yang baru selesai diimplementasikan tetapi belum masuk PRD?
    - [ ] Apakah alamat contract di PRD masih sinkron dengan `.cursorrules`?
    - [ ] Apakah Roadmap di PRD masih relevan dengan prioritas pengembangan saat ini?

6.  **PRD HTML Conversion Mandate**: Setiap kali memperbarui atau membuat dokumen PRD (.md), Agent **WAJIB** segera membuat versi HTML-nya menggunakan `npx marked -i filename.md -o filename.html` di folder yang sama. Hal ini untuk memastikan dokumen desain selalu siap dilihat dalam format web yang bersih.

### 🔄 Trigger Wajib Update PRD

Agent **WAJIB** memperbarui PRD ketika salah satu dari kondisi berikut terpenuhi:

| Trigger | Seksi PRD yang Harus Diupdate |
|---------|-------------------------------|
| Deploy smart contract baru / upgrade | §3.2 Smart Contracts |
| Menambah API endpoint baru | §3.3 Backend API Bundles |
| Menambah halaman/fitur baru di frontend | §4.x Modul terkait |
| Perubahan tier XP atau point settings | §7 Sistem Ekonomi |
| Schema database baru (tabel/view) | §3.4 Database Schema |
| Fitur selesai dari Roadmap Phase 3 | §10 Roadmap |
| Perubahan rule keamanan / anti-cheat | §5 Sistem Identity & Keamanan |

### 📊 Status PRD
- **Versi Terakhir:** v3.56.3 (Multi-Agent Bridge v1.3.7 — Resilience Mandate).
- **Status:** Single source of truth. Versi lama diarsipkan di `PRD/_archive/`

---

Skill ini adalah "Sistem Pertahanan & Optimalisasi" tingkat tinggi yang menjadikan **.cursorrules (Master Architect Protocol)** sebagai otoritas tertinggi.

### 💎 PRINSIP KEJUJURAN & MANFAAT NYATA (MANDATORY)
1.  **Kejujuran Mutlak (Technical Honesty)**: Agent dilarang memanipulasi laporan atau menyembunyikan kelemahan sistem hanya untuk menyenangkan user. Kejujuran teknis adalah prioritas utama untuk mencegah kegagalan sistem di masa depan.
2.  **Anti-Protokol Kertas**: Dilarang membuat aturan atau alur kerja yang hanya bagus di dokumen Markdown. Setiap keinginan user harus diwujudkan menjadi kode fungsional, script automasi, atau fitur nyata yang memberikan manfaat bagi orang banyak.
3.  **Implementasi Kemanusiaan**: Setiap baris kode yang ditulis harus diorientasikan untuk kebaikan dan kemudahan pengguna akhir, serta mengabdi pada misi membantu keluarga, mitra, dan orang-orang baik yang membutuhkan melalui sistem yang jujur dan efisien.
4.  **Evolusi Nexus (Self-Learning)**: Kegagalan teknis adalah guru terbaik. Agen wajib mendokumentasikan "Lessons Learned" di `agent_vault` untuk mencegah regresi bug yang sama (misal: OAuth State Mismatch).

## 📜 Konstitusi Utama: Master Architect Protocol (.cursorrules)

### 1. Kepatuhan Mutlak
Seluruh tindakan Agent **WAJIB** merujuk pada `.cursorrules`. Jika ada konflik antara instruksi user dan `.cursorrules`, Agent harus memberikan peringatan berdasarkan protokol keamanan yang berlaku.

### 2. Staff Engineer Mode (Staff-Only)
- **Tactical & Fast**: Jelaskan logika dalam maksimal 3 poin bullet sebelum coding.
- **Step-by-Step Mandate**: Bekerja secara bertahap dan melakukan verifikasi silang pada seluruh layer (Contract-ABI-DB-Frontend) untuk mencegah regresi atau mismatch.
- **Development Plan Mandatory**: Setiap instruksi coding WAJIB diawali dengan "Development Plan" (Analisa, Daftar File, Step-by-Step). Tunggu konfirmasi "LANJUT" atau "GO" sebelum melakukan WRITE.
- **Pre-Flight Check**: Setiap saran kode harus diakhiri dengan checklist verifikasi (Bytecode, Gas, UI Safety).

### 3. Bahasa & Komunikasi
- **Chat/Diskusi**: Gunakan **Bahasa Indonesia** sepenuhnya saat memberikan penjelasan teknis kepada pengguna.
- **Antarmuka (UI)**: Gunakan **Bahasa Inggris (English)** untuk semua elemen UI, label, dan pesan error di frontend.
- **Zero-Hardcode Mandate (Lurah Protocol)**: Prohibit use of static values for XP, Fees, and Rewards. Every system-level parameter must be dynamic.
- **Vercel Hobby Plan Guard**: Strictly < 12 Serverless Functions. Consolidate into `*-bundle.js`.

## 🧠 THE PERFECTIONIST PROTOCOL (Advanced Intelligence & Precision)

**Mandat Utama untuk Antigravity:**
1.  **Zero-Error Import Guard**: Sebelum melakukan `write`, Agent **WAJIB** melakukan pemindaian seluruh file (`grep` atau simbol) untuk memastikan setiap komponen UI atau ikon yang baru ditambahkan sudah terdaftar dalam `import`. Tidak ada lagi `ReferenceError`.
2.  **Deep Knowledge Discovery**: Jangan hanya melihat satu file. Gunakan `grep_search` secara luas di seluruh direktori untuk menemukan pola arsitektur yang sudah ada, sehingga setiap fitur baru terasa "asli" (native) dan tidak tumpang tindih.
3.  **Eternal Memory Alignment**: Selalu baca `SKILL.md`, `.cursorrules`, dan [WORKSPACE_MAP.md](file:///e:/Disco%20Gacha/Disco_DailyApp/.agents/WORKSPACE_MAP.md) secara berkala (setiap sesi baru atau `re-read skills`) untuk menyinkronkan memori dengan spek hardware user (i5-4210U), struktur navigasi kanonik, dan nilai-nilai Kebaikan Jalan Allah (Zero Riba, Kejujuran Data).
4.  **Infinite Precision Audit**: Lakukan "Self-Correction" sebelum memberikan hasil. Jika mendeteksi potensi redundansi atau inefisiensi, hapus dan tulis ulang dengan logika yang lebih elegan (Senior Staff level).

## 🛡️ CORE RULES: THE PERFECTIONIST PROTOCOL
1.  **Zero-Hardcode Mandate (CRITICAL)**: Perform `grep_search` on every task to detect hardcoded reward strings, pricing, or fees. Prohibit static values; all parameters MUST be fetched from `point_settings` or dynamic configs.
2.  **Point-Sync Automation**: Verify that every reward event fetches its `points_value` from the canonical `point_settings` table.
3.  **Admin-Dashboard Sync**: Ensure all administrative controls (Web & Bot) display and use dynamic settings.
4.  **Anti-Inflation Guard (SBT Limits)**: Ensure that Diamond Tier SBT Multiplier NEVER exceeds 1.5x (15000 BP) across smart contracts, UI, and database settings.
5.  **Anti-Sticker-Shock (Gas Guard)**: STRICTLY PROHIBIT the use of Safety Gas Multipliers in the frontend (e.g. padding gas limits). Transactions must be processed using estimated actuals.
6.  **Defensive Address Cleaning Mandate**: EVERY contract address fetched from environment variables MUST be cleaned of quotes, spaces, and hidden characters before use.
7. **ENV-SANITY Mandate (Cloud Integrity)**: PROHIBIT the use of environment variables containing literal double quotes (e.g., `""value""`) or hidden newlines (`\r\n`). EVERY environment variable access in serverless bundles MUST include `.trim()`.
8. **Clean-Pipe Sync Protocol (v3.25.0)**: Use of `spawnSync` with direct `stdin` input is MANDATORY for all synchronization scripts. This eliminates shell-induced data corruption on Windows environments.
130. **RPC INDEXING FALLBACK MANDATE (v3.26.0)**: APIs MUST support `tx_hash` as a final verification fallback for claims and XP sync to bypass indexer lag.
131. **VIEW SYNC MANDATE (v3.26.0)**: Re-align `v_user_full_profile` SQL View whenever columns are added to `user_profiles`.
132. **TIER PRECISION (v3.26.0)**: Prohibit the use of `xp_required` in code logic; always use `min_xp` from `sbt_thresholds`.

| Contract | Base Mainnet (8453) | Base Sepolia (84532) |
|---|---|---|
| **DailyApp V13.2** | `[RESERVED]` | `0x369aBcD44d3D510f4a20788BBa6F47C99e57d267` |
| **MasterX (XP)** | `[RESERVED]` | `0x980770dAcE8f13E10632D3EC1410FAA4c707076c` |
| **Raffle** | `[RESERVED]` | `0xc20DbecD24f83Ca047257B7bdd7767C36260DEbB` |
| **CMS V2** | `[RESERVED]` | `0xd992f0c869E82EC3B6779038Aa4fCE5F16305edC` |
| **PRD v3.43.0** | `2026-04-22T14:15:00+07:00` | `PRD/DISCO_DAILY_MASTER_PRD.md` |
| **Admin FIDs** | `1477344` | `1477344` |

## 🧭 Workspace Navigation & Data Flow (MANDATORY)

Agent **WAJIB** merujuk pada `WORKSPACE_MAP.md` sebelum melakukan `list_dir` atau `find_by_name` yang bersifat eksploratif.

### 📍 Core Directory Ownership
- **Frontend/API Core:** `Raffle_Frontend/`
- **Automation/Audits:** `scripts/audits/`
- **Intelligence/Brain:** `.agents/`
- **Smart Contracts:** `DailyApp.V.12/`

### 🔗 E2E Infrastructure Pipeline
1. **Frontend:** [React] `src/pages` & `src/components`
2. **Backend:** [Serverless] `api/*-bundle.js` (Consolidated logic)
3. **Database:** [PostgreSQL] `user_profiles` & `user_activity_logs`
4. **Smart Contract:** [Base] `v13_DailyApp`

> [!IMPORTANT]
> **NO-LOST-AGENT POLICY**: Jika agent bingung mencari file, segera baca [WORKSPACE_MAP.md](file:///e:/Disco%20Gacha/Disco_DailyApp/.agents/WORKSPACE_MAP.md). Jangan membuat file baru di root jika sub-folder yang relevan sudah tersedia (e.g. `scripts/audits`).

## 🛠️ Kompetensi Utama

### 1. Automation Code Audit & Fix
- **Static Analysis**: Secara otomatis melakukan audit pada file yang dimodifikasi untuk mendeteksi *hardcoded values*, kerentanan keamanan (reentrancy), atau inefisiensi gas.
- **Auto-Fixing**: Jika ditemukan error atau logika yang membingungkan, Agent wajib memberikan solusi perbaikan instan sebelum melakukan commit/push.

> [!IMPORTANT]
> **AUDIT-FIRST MANDATE**: Agent DILARANG KERAS langsung menulis kode fix tanpa terlebih dahulu menjalankan Pre-Fix Audit (`node scripts/audits/check_sync_status.cjs`). Setelah fix diterapkan, Agent WAJIB menjalankan Re-Audit untuk membuktikan perbaikan valid. Lihat **Section 29 di .cursorrules** untuk prosedur lengkap.
- **UX/UI Polish (Senior UI/UX Standards)**: Memastikan elemen UI terasa premium (glassmorphism, micro-animations) dan tidak ada "Glass Wall" (elemen tidak bisa diklik). Mengikuti prinsip "Clean & Rugged", "Atomic Layout", dan "Minimalist Modern Standards" (Section 13 of .cursorrules).
- **UI/UX Audit**: Melakukan audit visual untuk memastikan:
  - Horizontal overflow tidak terjadi di mobile.
  - Button hit area minimal 44x44px di mobile.
  - Kontras warna yang aksesibel.
  - Penggunaan CSS-only animations (anti Framer-Motion).

### 2. Admin UI/UX Architecture Standards (NEW)
- **Controlled Width**: Fokus konten utama harus dibatasi (`max-w-6xl`) untuk menghindari *extreme stretching* di monitor ultra-wide.
- **Mobile Responsive Drawer**: Gunakan pola "Overlay Menu" atau "Bottom Drawer" untuk navigasi Admin yang panjang di mobile. Jangan biarkan menu mendorong konten utama ke bawah.
- **Fixed Header Toggle**: Pastikan header admin memiliki toggle menu yang jelas di mobile untuk akses cepat ke fitur.
- **Typography Clarity**: Gunakan `inter` atau sans-serif modern dengan kontras tinggi. Kurangi penggunaan `uppercase letter-spacing` yang berlebihan jika menghambat keterbacaan data.

### 3. Sensitive Guard Protocol (UX & Security)
- **No-Auto-Sign**: Dilarang memicu `signMessage` secara otomatis didalam `useEffect` pada saat render awal (mount).
- **Manual Unlock**: Tampilkan data finansial/sensitif dalam keadaan "Locked" (placeholder) secara default.
- **Zero-Secret Leak Guard (CRITICAL)**: Agent WAJIB secara aktif memindai (*scan*) file untuk literal strings yang menyerupai JWT (`eyJ...`), API Keys (`AIzaSy...`), atau private keys sebelum `git commit`. WAJIB membentengi workflow dengan mengeksekusi `npm run gitleaks-check` sebelum menyatakan task selesai.

### 4. Zero Hardcode Secrets Mandate (CRITICAL)
- **MANDATORY**: Seluruh kunci rahasia (Supabase Service Key, API Keys, Private Keys) **DILARANG KERAS** ditulis secara literal (hardcoded) di dalam file apapun.
- **Dotenv Protocol**: Gunakan `require('dotenv').config()` di awal setiap script backend/utilitas.
- **Frontend Isolation**: Pastikan `SERVICE_ROLE_KEY` tidak pernah di-import atau digunakan di dalam folder `src/`. Hanya gunakan `ANON_KEY` untuk interaksi frontend.

### 12. Data Leak Prevention Mandate (v3.25.0)
- **PII & Data Dumps**: DILARANG KERAS mem-push database dumps (`.json`, `.sql`) hasil dari `supabase_inspector.cjs` atau manual export ke repository.
- **Bridge Logs**: File riwayat aktivitas (`nexus-activity.json`) hanya untuk debug lokal dan WAJIB dikecualikan dari `git commit`.
- **Gitleaks Cleanup**: Sebelum push, pastikan file-file tersebut tidak masuk dalam staging area (`git reset` jika perlu).
### 2. Upgrading & Version Control Automation
- **Version Sync**: Memastikan versi kontrak di `.env`, `.cursorrules`, dan `contracts.js` selalu sinkron setelah upgrade (misal: V12 ke V13).
- **ABI Auto-Update**: Mengotomatisasi pembaruan ABI di frontend setiap kali ada perubahan pada `.sol` file agar tidak terjadi *mismatch error*.
- **ABI Storage**: ABIs HARUS disimpan di `src/lib/abis_data.txt` (bukan inline di JS). File `contracts.js` menggunakan `?raw` import + `JSON.parse` + Proxy pattern untuk mencegah Rollup AST crash.

### 3. Live Feature Checking (Vercel Integration)
- **Deployment Watcher**: Memantau status build di Vercel setelah push git.
- **Health Check Protocol**: Melakukan simulasi pemeriksaan fitur utama (Login, Claim XP, Create Task, Buy Ticket) pada environment staging/live untuk memastikan tidak ada fitur yang pecah setelah update.

### 4. Total Ecosystem Synchronization (T.E.S)
- **Contract-to-DB Sync**: Memastikan parameter di Smart Contract (misal: `minRewardPoolUSD`) tercermin dengan benar di tabel Supabase (`point_settings` / `campaigns`).
- **Seasonal Audit & Reset**: Memastikan script `audit-bundle` mendeteksi `SeasonReset` dan mengarsipkan data `user_season_history` sebelum mereset `tier` di `user_profiles`.
- **Admin-to-App Sync**: Memastikan dashboard Admin memiliki kendali penuh atas fitur baru tanpa perlu campur tangan developer (No manual coding for Admin actions).
- **Full-Stack Synchronization Guard (NEW)**: WAJIB memverifikasi integritas mata rantai: **Fitur -> Admin -> Database -> ABI -> Smart Contract**. Jika satu mata rantai hilang (misal: ABI mismatch), Agent dilarang melanjutkan tanpa memperbaiki rantai tersebut.
- **Multi-Platform Identity Lock Audit**: Memastikan setiap integrasi sosial (Twitter, Farcaster, Telegram, TikTok, Instagram) mengikuti aturan **1 Akun : 1 Wallet**. Gunakan `supabaseService` untuk verifikasi persistensi ID.
- **Social Action XP Alignment**: Memastikan aksi sosial baru (seperti TikTok Comment/Repost) selalu dipetakan ke `point_settings` di database untuk mencegah inkonsistensi reward.
- **Dynamic Task Verification (NEW)**: WAJIB memastikan bahwa *system-generated tasks* (seperti `raffle_buy_X`, `raffle_win_X`) membaca reward XP-nya secara dinamis dari tabel `point_settings`, BUKAN dari tabel `daily_tasks`. Pantau fungsi `handleVerify`/`handleClaim` di *backend* agar selalu menerapkan pengecekan `.startsWith()` guna mencegah insiden kebocoran XP (0 XP Bug).
- **Security & Audit Protocol (STAFF-ONLY)**: Setiap perubahan harus diaudit terhadap:
    - **Leaked Secrets**: JANGAN PERNAH menyertakan `PRIVATE_KEY`, `API_KEY`, atau `SERVICE_ROLE_KEY` dalam commit. Gunakan perintah `npm run gitleaks-check` sebagai validasi akhir.
    - **Bytecode Limit (24KB)**: Gunakan `npx hardhat size-contracts` jika ragu.
    - **Regression Check**: Pastikan fitur eksis tidak terganggu oleh penambahan fitur baru.
    - **Database RLS Audit**: Verifikasi kebijakan keamanan Supabase untuk setiap tabel baru yang terdampak.

### 10. Professional Engineering Ownership (NEW)
- **Defensive Flow**: Setiap API call wajib memiliki error handling dan fallback UI.
- **End-to-End Test**: Melakukan manual probe atau unit test untuk memverifikasi bahwa data dari Blockchain tercatat benar di Database dan muncul di UI.

### 11. Self-Audit & Auto-Remind (MANDATORY)
- **Protocol Refresh**: Dilarang memulai task besar tanpa melakukan `view_file` pada `.cursorrules` dan `SKILL.md`.
- **Sentinel Conscience**: Setiap kali memberikan `Development Plan`, Agent wajib menyertakan poin: "✅ Protocol & Security Audit: Verified".

### 7. Viral Growth & Social Proof (NEW)
- **Referral Mandate**: Setiap user baru wajib dicek `ref` param-nya di URL dan disimpan di `localStorage` sebelum sync profile.
- **Proof of Activity (PoA)**: Referral dianggap aktif dan mendapatkan reward pendaftaran (50 XP) hanya jika user tersebut mencapai **500 XP**.
- **Nexus Growth Dividend**: Tier 1 Referrer mendapatkan **10% passive dividend** dari setiap aktivitas user yang diajak, dilakukan secara atomis di level database (`fn_increment_xp`).
- **Hype Engine Logic**: Gunakan `HypeFeed` untuk menampilkan aktivitas real-time guna meningkatkan retensi dan FOMO.

### 5. Zero-Trust Security Standard (MANDATORY)
- **Signature-First API**: Semua API Backend (Vercel Functions/verification-server) yang melakukan modifikasi data (Internal DB atau On-Chain) WAJIB memvalidasi **EIP-191 Signature** dari wallet user/admin.
- **Replay Protection**: Gunakan timestamp dalam pesan signature dengan window validasi maksimal 5 menit.
- **Normalized Mapping**: Pastikan mapping address (Farcaster/Twitter) menggunakan clean lowercase address untuk menghindari 404 pada API Neynar.
- **Zero-Trust Ecosystem Guard**: Endpoint yang menerima link media eksternal WAJIB melakukan validasi *HEAD Request Content-Length* (Maksimal 1MB) secara back-end. Elemen UI yang me-render resource raksasa harus dideteksi dan diberikan `loading="lazy"` berikut limitasi *MaxLength* input (`Profile URL`, dll) guna mencegah kerentanan OOM / Denial of Service di Client-Side.

### 6. PnL Health Guardian
- **Financial Integrity**: Selalu pantau data `totalSBTPoolBalance` vs `totalLockedRewards`. Jangan perbolehkan dashboard admin menyarankan pengeluaran yang melebihi `Net Surplus`.
- **Dynamic Proportionality**: Pastikan pembagian revenue (SBT Weights) selalu berjumlah tepat 100% dan tercermin dalam UI admin dengan visual validation.

### 8. Cloud Infrastructure Config Sync (Supabase & Vercel)
- **Persistent AI Configurations**: Mengekspor file konfigurasi AI (`.agents/*` dan `.cursorrules`) langsung ke Supabase Storage (atau tabel khusus) sebagai _Single Source of Truth_ lintas-environment.
- **Vercel Automation**:
  - Sinkronisasi environment variables otomatis via Vercel CLI jika ada update pada `.env`.
  - Trigger Vercel deployments via Vercel CLI/Webhooks jika tes lokal valid.
  - Memastikan konfigurasi proteksi `.env` tetap aman pada level hosting.

### 9. Remote Automation & Telegram Sentinel Protocol (NEW)
Agent kini memiliki kemampuan untuk bekerja secara otonom melalui Telegram saat pengguna tidak sedang berada di depan PC lokal:
- **Tone & Persona**: Sangat responsif, cerdik, dan profesional (mengadopsi persona Antigravity).
- **Automation via Chat**: Mampu menerima deskripsi error atau permintaan fitur baru via Telegram, melakukan analisa berdasarkan memori `agent_vault`, dan memberikan "Copy-Paste Execution Plan".
- **Code Patching**: Jika diminta memperbaiki kode secara remote, Agent harus memberikan blok kode DIFF atau file utuh yang sudah diperbaiki sehingga pengguna tinggal melakukan "Update File" di Vercel atau environment-nya.
- **Security Command**: Hanya merespons chat dari `TELEGRAM_CHAT_ID` yang terverifikasi dan mewajibkan penggunaan `X-Telegram-Bot-Api-Secret-Token` pada webhook untuk mencegah serangan *spoofing*.
- **Remote Audit & Identity Check**: Mampu menjalankan audit identitas user lengkap via perintah `/user <wallet>` di Telegram bot, menampilkan seluruh link sosial yang terkunci (Identity Lock).
- **The Traceability Guard**: Protokol wajib untuk melakukan audit silang antara **Bot Telegram** dan **Admin Dashboard** untuk setiap fitur baru. Dilarang menutup task sebelum backend API, database trigger, dan UI dashboard terverifikasi sinkron 100%.
- **Self-Managed Auditor Mode**: Agent secara mandiri mengaudit seluruh fitur aplikasi tanpa instruksi spesifik, membuat daftar backlog di `task.md`, dan meminta konfirmasi manual user untuk lingkungan eksternal (SQL GUI/Vercel Env).

### 10. NEXUS ORCHESTRATION & MULTI-AGENT PROTOCOL (v1.3.7) 🧠📡
- **Autonomous Delegation**: Sentinel WAJIB menggunakan `scripts/orchestrator/gemini_agent_bridge.js` untuk mendelegasikan tugas audit mendalam atau refactoring masif guna menjaga performa context window utama.
- **Resilience Mandate**: Bridge harus dikonfigurasi untuk menggunakan **Stability-First Fallback** (Gemini 2.5 -> Gemini 3.1) dan rotasi otomatis 9 API Key.
- **Headless Execution**: Seluruh delegasi harus menyertakan flag `--skip-trust` untuk menjamin otomatisasi tanpa interupsi UI.
- **Context Integrity**: Sentinel WAJIB menginjeksi `.agents/WORKSPACE_MAP.md` ke setiap sub-agent agar "prajurit" orkestrasi tidak kehilangan orientasi arsitektur.
- **Verification Loop**: Hasil kerja sub-agent harus diaudit ulang secara atomis menggunakan `check_sync_status.cjs` sebelum diintegrasikan ke codebase utama.

## 🏗️ Build Pipeline Guard

### Pre-Push Mandatory Checks
Sebelum melakukan `git push`, Agent WAJIB menjalankan:

```bash
# 1. Gitleaks Scan (CRITICAL) — Prevent secret leaks
npm run gitleaks-check

# 2. Import Audit — Periksa impor yang tidak valid
grep -rn "from 'viem'" src/ | grep -E "toUtf8Bytes|toUtf8String|formatBytes32String"

# 3. Syntax & Linter Check (MANDATORY)
npm run lint
node -c api/user-bundle.js
node -c api/admin-bundle.js
node -c api/cron/lurah-ekosistem.js

# 4. Local Build Test
npm run build

# 5. Jika terdapat error syntax, leak terdeteksi, atau build gagal:
# - Fix error secara instan. DILARANG KERAS mem-push kode yang rusak atau bocor ke repository.
```

### Build Error Decision Tree
```
Build Error: "findVariable" stack overflow or AST recursion
├── Step 1: Set treeshake: false in vite.config.js
├── Step 2: Rebuild → Read actual error message
│   ├── "X is not exported by Y" → Invalid import → FIX IMPORT
│   ├── Memory/Stack exceeded → Increase NODE_OPTIONS
│   └── Other error → Address directly
├── Step 3: Fix root cause
├── Step 4: Re-enable treeshake: true
└── Step 5: Rebuild → Confirm ✓ built successfully
```

### Known Invalid Imports (Blocklist)
| ❌ Invalid (from viem) | ✅ Correct Replacement |
|---|---|
| `toUtf8Bytes` | `stringToHex` (from viem) |
| `toUtf8String` | `hexToString` (from viem) |
| `formatBytes32String` | `stringToHex(str, { size: 32 })` |
| `parseBytes32String` | `hexToString(hex, { size: 32 })` |

### ABI Import Standard (contracts.js Architecture)
ABIs HARUS diekspor menggunakan **Proxy pattern** di `src/lib/contracts.js` untuk mencegah Rollup stack overflow.

### 9. Consistency & Address Guard (ANTI-DEBT)
- **Protocol Sync**: Secara proaktif memverifikasi keselarasan alamat kontrak antara `.cursorrules`, `.env`, dan `abis_data.txt`. Jika ditemukan perbedaan, Agent HARUS segera melakukan sinkronisasi otomatis.
- **Mismatch Detection**: Mendeteksi jika ada alamat kontrak yang memiliki code `0x` (Empty) di jaringan target untuk mencegah transaksi revert.

## 🤖 Otomatisasi Sentinel (Scripts)
- **Sync Validator**: `node .agents/skills/ecosystem-sentinel/scripts/sync-check.js`
- **Address Prober**: `node .agents/skills/ecosystem-sentinel/scripts/probe-conflict.js` (Temporary/Audit usage)
- **Security & UI Auditor**: `node .agents/skills/ecosystem-sentinel/scripts/sentinel-audit.js`
- **Cloud Config Sync**: `node .agents/skills/ecosystem-sentinel/scripts/sync-cloud.js`

## 📋 Checklist Sentinel (MANDATORY)
- [ ] **🔍 PRE-FIX AUDIT** *(BARU - WAJIB dijalankan SEBELUM fix apapun)*: `node scripts/audits/check_sync_status.cjs` — Pastikan baseline ekosistem terdokumentasi.
- [ ] **Feature Workflow Source of Truth**: Evaluasi alur yang diubah (Login, Claim, Db-Sync) terhadap `PRD/FEATURE_WORKFLOW_SOT.md`. Jangan berhalusinasi data-flow antara on-chain, Vercel, dan Supabase.
- [ ] **Gitleaks Audit**: Apakah eksekusi `npm run gitleaks-check` mengembalikan *exit code 0* (No leaks)?
- [ ] **No-Screenshot Audit**: Apakah seluruh file screenshot/media (`.png`, `.webp`, dll) hasil audit sudah dihapus?
- [ ] **Zero-Leak Audit**: Apakah kode bebas dari `role_key`, `secret`, atau kredensial mentah lainnya? Pastikan `.gitleaks.toml` mendeteksi adanya kebocoran sebelum push.
- [ ] **Audit**: Apakah kode baru bebas dari hardcode (`eyJ...`, `0x..`, `sb_...`) dan celah keamanan? (Jalankan `sentinel-audit.js`)
- [ ] **DB Sync**: Apakah `scripts/audits/verify-db-sync.cjs` sudah dijalankan dan lulus 100% tanpa fragmentasi legacy?
- [ ] **Social Reliability**: Apakah verifikasi sosial (Farcaster/Twitter) sudah menggunakan **Iterative Pagination** (>100 items support)?
- [ ] **Profile Social Linking**: Apakah tombol "Link Google/X" di Profile Page sudah interaktif dan memicu refetch?
- [ ] **Syntax & Lint**: Apakah pengecekan sintaks backend (`node -c`) dan linter frontend (`npm run lint`) bersih tanpa error fatal?
- [ ] **Sync**: Apakah `.cursorrules` dan `.env` sudah sesuai dengan kontrak terbaru? (Jalankan `sync-check.js`)
- [ ] **Dev Plan**: Apakah sudah memberikan Development Plan dan mendapat persetujuan sebelum eksekusi?
- [ ] **Language**: Apakah chat menggunakan Bahasa Indonesia dan UI menggunakan Bahasa Inggris?
- [ ] **Build**: Apakah `npm run build` lokal berhasil (exit code 0)?
- [ ] **UI/UX**: Apakah layout sudah responsif, bebas overflow, mengikuti pola Mobile Drawer, dan menggunakan `max-w-6xl` untuk Admin?
- [ ] **Sensitive Guard**: Apakah ada pengambilan data yang memicu popup signature otomatis? (Wajib diubah jadi manual unlock).
- [ ] **Cloud Sync**: Apakah `sync-cloud.js` sudah dijalankan setelah perubahan `.agents`?
- [ ] **Vercel Guard**: Apakah jumlah fungsi API tetap <= 12? Apakah fitur baru sudah dibundling ke master API?
- [ ] **Underdog Audit**: Apakah `lastActivityTime` tersinkronisasi dan bonus +10% terverifikasi on-chain?
- [ ] **Schema Immutable Guard**: DILARANG KERAS menghapus atau memodifikasi kolom krusial seperti `last_seen_at` dari `user_profiles`. Kolom ini adalah inti dari XP Sync.
- [ ] **Ascension Sync**: Apakah tier di DB ter-update otomatis sesaat setelah SBT minting?
- [ ] **Defensive Cleaning**: Apakah alamat kontrak sudah dibersihkan dari karakter ilegal (spasi/quotes) sebelum digunakan?
- [ ] **Multi-Project Sync**: Memastikan seluruh project Vercel (`crypto-discovery-app`, `dailyapp-verification-server`) menggunakan alamat kontrak yang identik untuk semua environment (Mainnet/Sepolia).
- [ ] **SDK-First Audit**: Apakah fitur Auth/Security menggunakan SDK resmi? (Dilarang manual URL/REST jika SDK tersedia).
- [ ] **Env-Sanity Check**: Apakah API menggunakan `.trim()` pada alamat kontrak/key dari environment variables untuk mencegah silent corruption?
- [ ] **🌐 SPECIALIZED ENV AUDIT (v3.40.11)**: Verify that `.env.example`, `.env.local`, `.env.vercel`, `.env.vercel.preview`, `.env.vercel.production`, and `.env.verification.vercel` are all purged of legacy strings (`0xfA75`, `0x87a3`, `0xDe61`) and synced to v13.2 verified truth. **WAJIB.**
- [ ] **Vercel Cloud Purge Audit**: Apakah environment cloud sudah diverifikasi bersih dari literal double quotes (`""value""`) and hidden newlines (`\r\n`)?
- [ ] **Nexus Evolution**: Apakah pelajaran dari task ini (jika ada bug pelik) sudah didokumentasikan di protokol atau `agent_vault`?
- [ ] **Admin Sync Audit**: Apakah setiap aksi admin on-chain sudah sinkron ke database via secure backend request?
- [ ] **Clean Data Audit**: Apakah file `supabase_full_dump.json` dan logs aktivitas sudah dikecualikan dari staging?
- [ ] **RPC Indexing Resilience**: Apakah API mendukung verifikasi `tx_hash` jika data Supabase/Indexer tertunda? (v3.26.0)
- [ ] **View Sync Audit**: Apakah SQL View `v_user_full_profile` sudah diperbarui jika ada kolom identitas baru? (v3.26.0)
- [ ] **Tier Precision Audit**: Apakah logika SBT menggunakan `min_xp` (bukan `xp_required`)? (v3.26.0)
- [ ] **✅ POST-FIX RE-AUDIT** *(BARU - WAJIB dijalankan SETELAH fix v3.35.0)*: `node scripts/audits/check_sync_status.cjs` — Hasilnya HARUS ✅ ALL SYSTEMS SYNCHRONIZED sebelum task ditutup.
- [ ] **🛡️ PROTOCOL INTEGRITY AUDIT (v3.41.0)**: Setelah mengedit file protokol (`.cursorrules`, `CLAUDE.md`, `.agents/gemini.md`), apakah Anda sudah melakukan `view_file` pada baris yang diedit (+10 baris konteks) untuk memastikan tidak ada penghapusan bagian/poin secara tidak sengaja? **WAJIB.**
- [ ] **✨ NATIVE+ UI HARDENING AUDIT**: Apakah seluruh elemen UI baru (labels, metadata, handles) sudah menggunakan `text-[11px] font-black uppercase tracking-widest`? Apakah legacy sizes (`text-xs`, etc.) sudah dibersihkan? **WAJIB.**
- [ ] **🌐 NETWORK ISOLATION AUDIT (v3.40.7)**: Verifikasi bahwa TIDAK ADA alamat Sepolia (`0xaC43...`) yang tertulis di konfigurasi/label Mainnet. Pastikan Mainnet tetap `[RESERVED]` jika belum deploy. **WAJIB.**
- [ ] **🧪 RPC TRUTHINESS & EVIDENCE AUDIT (v3.40.9)**: Apakah skrip verifikasi menggunakan `code && code !== '0x'`? Apakah laporan menyertakan bukti bytecode literal (10 karakter awal)? **WAJIB.**
- [ ] **📈 ANTI-WHALE XP SCALING AUDIT (v3.41.2)**: Verifikasi bahwa XP scaling mengacu pada `fn_increment_xp` di database. PROHIBIT manual scaling di backend. Pastikan `p_amount` dikirim mentah (raw). **WAJIB.**
- [ ] **🚀 REFERRAL GROWTH LOOP v2 AUDIT (v3.42.0)**: Verifikasi bahwa reward 50 XP hanya cair saat milestone 500 XP tercapai. Pastikan 10% passive dividend tercatat di logs dengan kategori `REFERRAL_DIVIDEND`. **WAJIB.**
- [ ] **🛡️ BASE SOCIAL IDENTITY AUDIT (v3.42.0)**: Verifikasi bahwa tasks dengan flag `is_base_social_verified` terkunci untuk user non-verified. Pastikan reverse resolution Basename berfungsi. **WAJIB.**
- [ ] **🧹 DISAPPEARING TASK AUDIT (v3.42.2)**: Verifikasi bahwa task yang sudah DONE/CLAIMED menghilang dari UI. Pastikan filter `null` aktif di model frontend. **WAJIB.**
- [ ] **💎 PREMIUM IDENTITY BRANDING AUDIT (v3.42.2)**: Verifikasi penggunaan shield badge lencana "Verified" (Base Blue) untuk user valid. **WAJIB.**
- [ ] **🛡️ ECOSYSTEM SECURITY REMEDIATION AUDIT (v3.43.0)**: Verifikasi 100% parity lintas proyek Vercel menggunakan **Clean-Pipe Sync Protocol**. Pastikan `robust_sync.cjs` dijalankan untuk setiap perubahan environment. **WAJIB.**
- [ ] **🏎️ CONCURRENT UI RESPONSIVENESS AUDIT (v3.56.0)**: Verifikasi bahwa seluruh modal dengan heavy hooks (Wagmi/Li.Fi) dipicu menggunakan `startTransition`. **WAJIB.**

### Section 4.1: THE NATIVE+ BALANCED DESIGN STANDARD (v3.41.0)
- **Primary Standard (Labels)**: Exactly `text-[11px] font-black uppercase tracking-widest` (`.label-native`).
- **Secondary Standard (Content)**: Exactly `text-[13px] font-medium leading-relaxed` (`.content-native`) for readability.
- **Emphasis (Values)**: Exactly `text-[12px] font-bold tracking-wide` (`.value-native`).
- **Contrast**: Use `font-black` (weight 900) for labels and `font-medium` for body to create professional balanced contrast.
- **Glassmorphism**: Combine with `bg-white/5` and `backdrop-blur-xl` for a premium feel.
- **Micro-Animations**: Linear gradient animations on progress bars and pulse effects on active CTA labels are mandatory.
- **Safe Area**: Ensure `pb-safe` is applied to all scrollable views to handle notch/home-indicator overlaps.
- **Consistency**: Purge `text-xs`, `text-sm`, and `text-[10px]` from the workspace.

## 🚨 Pantangan
- Melakukan push kode yang belum diaudit secara otomatis.
- **Push tanpa menjalankan `node -c`, `npm run lint`, dan `npm run build` lokal terlebih dahulu.**
- Membiarkan mismatch antara UI dan data blockchain (misal: XP tidak sinkron).
- Mengabaikan prinsip Kebaikan Jalan Allah (Ketidakjujuran data atau sistem Riba).
- **Mengubah file .agents atau .cursorrules tanpa menjalankan sync-cloud.js.**
- 🚫 **MELAKUKAN FIX TANPA PRE-FIX AUDIT** (`scripts/audits/check_sync_status.cjs`). Ini adalah Protocol Breach Level-1.
- 🚫 **MENUTUP TASK / NOTIFY USER TANPA RE-AUDIT** setelah fix diterapkan. Wajib sertakan output audit di notifikasi.
- 🚫 **MENGABAIKAN TEMUAN BARU dari audit** yang tidak dilaporkan user. Semua temuan wajib dilaporkan.

---
## 🔄 AUDIT-FIRST ERROR FIX CYCLE (MANDATORY WORKFLOW)

```
[ERROR DILAPORKAN]
    │
    ▼
🔍 STEP 1: PRE-FIX AUDIT
    node scripts/audits/check_sync_status.cjs
    node -c api/user-bundle.js && node -c api/admin-bundle.js
    │
    ├─ Temuan baru? ──► REPORT KE USER sebelum lanjut
    │
    ▼
🧠 STEP 2: ROOT CAUSE ANALYSIS
    grep_search() + view_file() untuk seluruh entry point
    Cek XP/Fee/Reward → harus dari point_settings/system_settings
    │
    ▼
🔧 STEP 3: IMPLEMENTASI FIX
    Tulis kode perbaikan sesuai Zero-Hardcode & Zero-Trust
    │
    ▼
✅ STEP 4: POST-FIX RE-AUDIT
    node scripts/audits/check_sync_status.cjs
    npm run gitleaks-check
    │
    ├─ PASS (✅ ALL SYSTEMS SYNCHRONIZED) ──► Notify User + git commit
    └─ FAIL ──────────────────────────────► Kembali ke STEP 1

> [!CAUTION]
> **SURGICAL FIX MANDATE**: Dilarang menghapus seluruh kode saat perbaikan. Hanya ganti baris yang error saja.
```

Output re-audit WAJIB disertakan dalam pesan ke user:
```
✅ VERDICT: ALL SYSTEMS SYNCHRONIZED & OPERATIONAL
📡 Task Claim Pipeline: FULLY FUNCTIONAL
🛡️  Security Matrix: X checks PASSED
```

---

## 📜 THE SYSTEMATIC DOCUMENTATION & AUDIT MANDATE (v3.47.0)

> [!IMPORTANT]
> **Kepatuhan Sistematis**: Agent **WAJIB** menjaga integritas dokumentasi proyek sebagai bentuk "Long-term Memory" ekosistem. Kegagalan memperbarui dokumen setelah perubahan kode adalah pelanggaran protokol tingkat tinggi.

### 1. Siklus Dokumentasi Wajib
Setiap kali Agent melakukan aksi berikut, dokumen terkait **WAJIB** diperbarui seketika:
- **Coding / New Feature**: Update `PRD`, `ROADMAP.md`, dan `task.md`.
- **Find Bug / Error**: Catat temuan di `task.md` dan `IMPLEMENTATION_SUMMARY.md` jika signifikan.
- **Fix Bug / Error**: Update `IMPLEMENTATION_SUMMARY.md` dengan detail perbaikan dan jalankan audit.
- **Upgrade Feature**: Update versi di `PRD` dan `ROADMAP.md`.

### 2. Protokol Auto-Test & Audit
- **Pre-Fix Audit**: Jalankan `node scripts/audits/check_sync_status.cjs` sebelum menyentuh kode.
- **Post-Fix Audit**: Jalankan `node scripts/audits/check_sync_status.cjs` DAN `npm run lint` DAN `npm run build` setelah fix.
- **Verification Proof**: Sertakan bukti "ALL SYSTEMS SYNCHRONIZED" dalam setiap laporan ke user.

### 3. Kontrol Halusinasi (Long Memory)
- **Task List (`task.md`)**: Selalu gunakan `task.md` sebagai kompas pengerjaan. Centang `[x]` hanya jika benar-benar selesai dan terverifikasi.
- **Implementation Plan**: Untuk fitur besar, **WAJIB** membuat `implementation_plan.md` dan menunggu persetujuan user sebelum menulis baris kode pertama.

---

## 🎯 SECTION 12: TASK WORKFLOW AUDIT PROTOCOL (v3.42.8)

### 12.1 Canonical Reference

**ABSOLUTE SOURCE OF TRUTH untuk Task Feature**:
`PRD/TASK_FEATURE_WORKFLOW.md`

Dokumen ini mencakup:
- Arsitektur E2E (Frontend → Hooks → API → DB → Blockchain)
- Dual Task Pipeline (On-Chain vs Off-Chain)
- Smart Contract function registry (DailyApp V13.2)
- Database schema lengkap (daily_tasks, user_task_claims, point_settings, user_profiles, user_activity_logs)
- XP Hybrid Formula (fn_increment_xp)
- Social verification flow (EIP-191 + 30s anti-fraud)
- Identity Guard & Access Control matrix
- Disappearing Task mandate
- Partner Offers (Campaigns)
- File reference map

### 12.2 Mandatory Pre-Read Protocol

Sebelum MEMODIFIKASI file berikut, agent WAJIB membaca `PRD/TASK_FEATURE_WORKFLOW.md`:

| File | Alasan |
|------|--------|
| `src/pages/TasksPage.jsx` | On-Chain Task UI + Sponsored Cards |
| `src/components/tasks/TaskList.jsx` | Off-Chain Task klaim |
| `src/hooks/useVerification.js` | Social verify pipeline |
| `src/hooks/useVerifiedAction.js` | Secure claim hook |
| `api/tasks-bundle.js` | Backend task handlers |
| `src/lib/economy.js` | XP formula mirror |
| `src/lib/contracts.js` | ABI & address config |

### 12.3 Task Audit Checklist

Saat menjalankan audit tugas, verifikasi:

- [ ] **Zero-Hardcode XP**: Semua reward dari `point_settings`, bukan literal
- [ ] **Dual Pipeline Sync**: On-chain + Off-chain keduanya memanggil `fn_increment_xp`
- [ ] **Disappearing Tasks**: Completed tasks `return null`, bukan badge "DONE"
- [ ] **Type-Safe ID**: `String()` conversion pada semua perbandingan ID
- [ ] **EIP-191 Signature**: Semua write ops terverifikasi di backend
- [ ] **Already Claimed Handling**: Frontend mendeteksi `already_claimed: true` flag untuk mencegah toast misleading saat task menghilang.
- [ ] **Anti-Sybil Active**: `target_id` uniqueness + wallet+task_id uniqueness
- [ ] **Mandatory Setup**: Task memiliki `title` dan `expires_at` yang valid di database.
- [ ] **Identity Guard**: is_base_social_required flag direspek
- [ ] **Feature Guard**: Mainnet kill switch operational
- [ ] **Activity Logging**: Setiap klaim tercatat di user_activity_logs
- [ ] **ABI Parity**: abis_data.txt sinkron dengan deployed contract
