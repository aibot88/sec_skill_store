---
name: network-intelligence-ops
description: "Operational safety rules untuk Network Intelligence — RTBH, DDoS, dan IBN."
version: "1.0.0"
---

> Melengkapi Domain 13 di SKILL.md.

================================================================
## DDOS ESCALATION MATRIX (L1-L5)
================================================================
Penanganan serangan tidak boleh langsung memutus traffic tanpa tahapan yang jelas.

| Level | Kondisi | Aksi (Remediasi) | Notifikasi |
|-------|---------|------------------|------------|
| L1 | Anomali traffic < 2x baseline | Observasi, tambah logging | Slack P4 |
| L2 | Spesifik flow > batas aman | BGP Flowspec (Rate limit flow) | Slack P3 |
| L3 | Serangan memengaruhi service lain | RTBH spesifik /32 IP victim | PagerDuty P2 |
| L4 | Link uplink saturate > 90% | BGP BGP Flowspec redirect ke scrubbing | PagerDuty P1 |
| L5 | Volumetric ekstrim > Kapasitas ISP | Koordinasi ISP upstream blackhole | Call NOC MGR |

================================================================
## RTBH (REMOTELY TRIGGERED BLACK HOLE) SAFETY RULES
================================================================
RTBH sangat berbahaya jika salah target. Patuhi aturan ini:

1. **Auto-Withdraw Timer:** Semua RTBH injeksi WAJIB memiliki batas waktu (misal: 1 jam). Script harus otomatis mencabut rute setelah waktu habis.
2. **Whitelist Critical IPs:** IP infrastruktur inti (DNS, Gateway, Management) TIDAK BOLEH bisa di-RTBH. Implementasikan cek regex/subnet sebelum `announce`.
3. **Prefix Limit:** DILARANG melakukan RTBH untuk subnet lebih besar dari `/24`. Jika terdeteksi, gagalkan dan minta manual approval.
4. **Audit Log:** Setiap eksekusi RTBH wajib masuk ke syslog/Loki dengan ID alert pemantiknya.

================================================================
## CORRELATION ENGINE ENFORCEMENT
================================================================
1. **Time Window:** Korelasi hanya valid jika event terjadi dalam window waktu yang sempit (contoh: 30 detik untuk BGP Flap + Interface Down).
2. **Topology-Aware:** Mesin harus tahu topologi. BGP flap di Router A akibat link mati di Router B adalah satu insiden, BUKAN dua.
3. **Deduplication:** Alarm yang sama dalam 5 menit hanya di-trigger sekali.

================================================================
## IBN (INTENT-BASED NETWORKING) COMPILATION RULES
================================================================
1. **Dry-Run Validation:** Intent compiler WAJIB melakukan validasi sintaks sebelum di-push (contoh: `commit check` di Juniper).
2. **Compile-Before-Push:** Template Jinja2/YANG harus di-render dan disimpan ke file sementara untuk keperluan audit sebelum push eksekusi.
3. **Rollback Timeout:** Gunakan mekanisme commit confirmed (`commit confirmed 10` di JunOS) agar jika management plane putus, konfigurasi otomatis rollback.
