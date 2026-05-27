---
name: govconnect-api-testing
description: >
  Referensi lengkap semua API endpoint GovConnect untuk testing: auth, laporan/complaint,
  layanan/service request, kategori, nomor penting, AI webhook, knowledge base, superadmin,
  dan public forms. Termasuk contoh request PowerShell dan curl untuk setiap endpoint.
  Gunakan skill ini saat melakukan API testing GovConnect.
---

# GovConnect API Testing Reference

## Auth

```powershell
# Login superadmin
$r = Invoke-RestMethod -Uri "http://127.0.0.1:3010/api/auth/login" `
  -Method POST -ContentType "application/json" `
  -Body '{"username":"superadmin","password":"GovConnect2026!"}'
$SA_TOKEN = $r.token

# Login village admin
$r2 = Invoke-RestMethod -Uri "http://127.0.0.1:3010/api/auth/login" `
  -Method POST -ContentType "application/json" `
  -Body '{"username":"admin_sangreseng","password":"SangresengAde2026!"}'
$VA_TOKEN = $r2.token

# Get current user
Invoke-RestMethod -Uri "http://127.0.0.1:3010/api/auth/me" `
  -Headers @{ Authorization = "Bearer $VA_TOKEN" }
```

## Headers Helper

```powershell
$SA_H = @{ Authorization = "Bearer $SA_TOKEN" }
$VA_H = @{ Authorization = "Bearer $VA_TOKEN" }
$INT_H = @{ "x-api-key" = "govconnect-internal-api-key-2025" }
```

## Laporan / Complaint (via Dashboard Proxy)

```powershell
# List laporan (village admin)
Invoke-RestMethod "http://127.0.0.1:3010/api/laporan" -Headers $VA_H

# List laporan dengan filter
Invoke-RestMethod "http://127.0.0.1:3010/api/laporan?status=OPEN&limit=10" -Headers $VA_H

# Detail laporan
Invoke-RestMethod "http://127.0.0.1:3010/api/laporan/LAP-20260101-001" -Headers $VA_H

# Update status laporan
Invoke-RestMethod "http://127.0.0.1:3010/api/laporan/LAP-20260101-001/status" `
  -Method PATCH -ContentType "application/json" -Headers $VA_H `
  -Body '{"status":"PROCESS","admin_notes":"Sedang ditindaklanjuti"}'

# Tambah update/catatan laporan
Invoke-RestMethod "http://127.0.0.1:3010/api/laporan/LAP-20260101-001/updates" `
  -Method POST -ContentType "application/json" -Headers $VA_H `
  -Body '{"note_text":"Tim sudah turun ke lapangan"}'
```

## Kategori dan Jenis Pengaduan

```powershell
# List kategori pengaduan (village admin)
Invoke-RestMethod "http://127.0.0.1:3010/api/complaints/categories" -Headers $VA_H

# Buat kategori baru
Invoke-RestMethod "http://127.0.0.1:3010/api/complaints/categories" `
  -Method POST -ContentType "application/json" -Headers $VA_H `
  -Body '{"name":"Infrastruktur","description":"Pengaduan infrastruktur desa"}'

# List jenis pengaduan
Invoke-RestMethod "http://127.0.0.1:3010/api/complaints/types" -Headers $VA_H

# Buat jenis pengaduan
Invoke-RestMethod "http://127.0.0.1:3010/api/complaints/types" `
  -Method POST -ContentType "application/json" -Headers $VA_H `
  -Body '{"category_id":"<cat-id>","name":"Jalan Rusak","is_urgent":false,"require_address":true}'
```

## Layanan / Service Request (via Dashboard Proxy)

```powershell
# List layanan
Invoke-RestMethod "http://127.0.0.1:3010/api/layanan" -Headers $VA_H

# Detail layanan
Invoke-RestMethod "http://127.0.0.1:3010/api/layanan/<service-id>" -Headers $VA_H

# List service requests
Invoke-RestMethod "http://127.0.0.1:3010/api/service-requests" -Headers $VA_H

# Detail service request
Invoke-RestMethod "http://127.0.0.1:3010/api/service-requests/<id>" -Headers $VA_H

# Update status service request
Invoke-RestMethod "http://127.0.0.1:3010/api/service-requests/<id>/status" `
  -Method PATCH -ContentType "application/json" -Headers $VA_H `
  -Body '{"status":"PROCESS","admin_notes":"Sedang diproses"}'
```

## Nomor Penting / Important Contacts

```powershell
# List kategori kontak penting
Invoke-RestMethod "http://127.0.0.1:3010/api/important-contacts/categories" -Headers $VA_H

# Buat kategori kontak
Invoke-RestMethod "http://127.0.0.1:3010/api/important-contacts/categories" `
  -Method POST -ContentType "application/json" -Headers $VA_H `
  -Body '{"name":"Darurat","description":"Nomor darurat desa"}'

# List kontak penting
Invoke-RestMethod "http://127.0.0.1:3010/api/important-contacts" -Headers $VA_H

# Buat kontak penting
Invoke-RestMethod "http://127.0.0.1:3010/api/important-contacts" `
  -Method POST -ContentType "application/json" -Headers $VA_H `
  -Body '{"category_id":"<cat-id>","name":"Kepala Desa","phone":"081234567890","description":"Nomor HP Kepala Desa"}'
```

## Knowledge Base

```powershell
# List knowledge
Invoke-RestMethod "http://127.0.0.1:3010/api/knowledge" -Headers $VA_H

# Buat knowledge
Invoke-RestMethod "http://127.0.0.1:3010/api/knowledge" `
  -Method POST -ContentType "application/json" -Headers $VA_H `
  -Body '{"title":"Syarat KTP","content":"Syarat membuat KTP: ...","category":"Layanan"}'

# Cek konsistensi knowledge
Invoke-RestMethod "http://127.0.0.1:3010/api/knowledge-consistency/scan" `
  -Method POST -Headers $VA_H
```

## AI Service - Simulasi Pesan WhatsApp

```powershell
# Dapatkan village_id dulu
$village = Invoke-RestMethod "http://127.0.0.1:3010/api/villages/me" -Headers $VA_H
$VILLAGE_ID = $village.data.id

# Simulasi webhook WhatsApp masuk ke channel-service
$waBody = @{
  type = "message"
  village_id = $VILLAGE_ID
  from = "6281234567890@s.whatsapp.net"
  messageId = "test-msg-$(Get-Date -Format 'yyyyMMddHHmmss')"
  timestamp = [int][double]::Parse((Get-Date -UFormat %s))
  message = @{
    conversation = "halo, mau tanya syarat buat KTP"
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://127.0.0.1:3001/webhook/whatsapp" `
  -Method POST -ContentType "application/json" `
  -Headers $INT_H -Body $waBody

# Simulasi laporan darurat
$urgentBody = @{
  type = "message"
  village_id = $VILLAGE_ID
  from = "6281234567890@s.whatsapp.net"
  messageId = "test-urgent-$(Get-Date -Format 'yyyyMMddHHmmss')"
  timestamp = [int][double]::Parse((Get-Date -UFormat %s))
  message = @{
    conversation = "tolong ada kebakaran di RT 03!"
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://127.0.0.1:3001/webhook/whatsapp" `
  -Method POST -ContentType "application/json" `
  -Headers $INT_H -Body $urgentBody
```

## AI Service - Direct API

```powershell
# Health check AI service
Invoke-RestMethod "http://127.0.0.1:3002/health"

# Cek AI usage
Invoke-RestMethod "http://127.0.0.1:3010/api/ai-usage/messages" -Headers $VA_H

# Cek AI balance
Invoke-RestMethod "http://127.0.0.1:3010/api/ai-balance" -Headers $VA_H
```

## Webchat Testing

```powershell
# Kirim pesan via webchat
$webchatBody = @{
  village_slug = "desa-sanreseng-ade"
  session_id = "web_test_$(Get-Date -Format 'yyyyMMddHHmmss')"
  message = "halo, mau tanya layanan apa saja yang tersedia?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:3010/api/webchat" `
  -Method POST -ContentType "application/json" -Body $webchatBody

# Poll webchat response
Invoke-RestMethod -Uri "http://127.0.0.1:3010/api/webchat/poll?session_id=web_test_xxx" `
  -Method GET
```

## Public Forms

```powershell
# Cek layanan by slug (public)
Invoke-RestMethod "http://127.0.0.1:3010/api/public/services/by-slug?village_slug=desa-sanreseng-ade&service_slug=<slug>"

# Submit pengaduan publik
$complaintBody = @{
  village_id = $VILLAGE_ID
  kategori = "Jalan Rusak"
  deskripsi = "Jalan di RT 03 berlubang besar"
  alamat = "Jl. Desa RT 03"
  channel = "WEBCHAT"
  session_id = "web_test_001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:3010/api/public/complaints" `
  -Method POST -ContentType "application/json" -Body $complaintBody

# Cek status pengaduan publik
Invoke-RestMethod "http://127.0.0.1:3010/api/public/complaints/LAP-xxx/check" `
  -Method POST -ContentType "application/json" `
  -Body '{"session_id":"web_test_001","channel":"WEBCHAT"}'
```

## Superadmin Endpoints

```powershell
# List villages
Invoke-RestMethod "http://127.0.0.1:3010/api/superadmin/villages" -Headers $SA_H

# List village admins
Invoke-RestMethod "http://127.0.0.1:3010/api/superadmin/village-admins" -Headers $SA_H

# System health
Invoke-RestMethod "http://127.0.0.1:3010/api/superadmin/system-health" -Headers $SA_H

# AI wallets
Invoke-RestMethod "http://127.0.0.1:3010/api/superadmin/ai-wallets" -Headers $SA_H

# LLM check
Invoke-RestMethod "http://127.0.0.1:3010/api/superadmin/llm-check" -Headers $SA_H
```

## Statistics

```powershell
# Overview statistik
Invoke-RestMethod "http://127.0.0.1:3010/api/statistics/overview" -Headers $VA_H

# Realtime summary dashboard
Invoke-RestMethod "http://127.0.0.1:3010/api/dashboard/realtime-summary" -Headers $VA_H

# AI usage stats
Invoke-RestMethod "http://127.0.0.1:3010/api/statistics/ai-usage" -Headers $VA_H
```

## Cek Database Langsung

```powershell
$env:PGPASSWORD = "dbgovconnect2026"

# Laporan terbaru
psql -h 127.0.0.1 -U govconnect -d govconnect -c `
  "SELECT complaint_id, status, kategori, is_urgent, village_id FROM cases.complaints ORDER BY created_at DESC LIMIT 10;"

# Service requests terbaru
psql -h 127.0.0.1 -U govconnect -d govconnect -c `
  "SELECT request_number, status, village_id FROM cases.service_requests ORDER BY created_at DESC LIMIT 10;"

# Notification logs
psql -h 127.0.0.1 -U govconnect -d govconnect -c `
  "SELECT notification_type, status, channel, created_at FROM notification.notification_logs ORDER BY created_at DESC LIMIT 10;"

# AI grounding mismatches
psql -h 127.0.0.1 -U govconnect -d govconnect -c `
  "SELECT mismatch_kind, status, village_id, detected_at FROM ai.ai_runtime_grounding_mismatches ORDER BY detected_at DESC LIMIT 10;"

# Outbox events pending
psql -h 127.0.0.1 -U govconnect -d govconnect -c `
  "SELECT routing_key, status, attempt_count, created_at FROM cases.event_outbox WHERE status != 'sent' ORDER BY created_at DESC LIMIT 10;"
```

## Cek RabbitMQ

```powershell
# Cek queues via management API
Invoke-RestMethod "http://127.0.0.1:15672/api/queues/govconnect" `
  -Headers @{ Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:genfityrabbitmq")) }
```
