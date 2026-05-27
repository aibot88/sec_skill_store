---
name: agentic-cli-logging
description: Yapılandırılmış log alanları, stderr vs dosya ve secret redaction kurallarını uygularken kullan.
---

## Amaç

Log alanları örnekleri: **`session_id`**, **`provider`**, **`turn`**, **`tool_name`**, **`event`**, **`duration_ms`**. Varsayılan **stderr**; dosyaya yazım opsiyonel. **Debug** seviyesinde bile API anahtarları, Authorization, kubeconfig içeriği **maskelenir** (`agentic-secrets-handling`).

## Kapsam

### Dahil

- Log seviyesi: `INFO`, `DEBUG` (proje kararı env veya flag).
- Yapılandırılmış JSON log satırı önerisi (observability uyumu).

### Hariç

- Merkezi log sunucusu zorunluluğu.

## Kurallar

- Kullanıcı mesajı içeriği log’a tam yazılacaksa PII uyarısı ve opt-in (`agentic-trajectory-recording` ile hizala).
- Trace id varsa OpenTelemetry ile korelasyon (`agentic-telemetry-optional`).
- Hata stack trace yalnız verbose modda.

## Kontrol listesi

- [ ] Örnek log satırında secret yok mu?
- [ ] Log döndürme / boyut sınırı tanımlı mı?
- [ ] Windows vs Unix path log’da okunaklı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Disk dolu | log path | Rotasyon veya stderr-only |
| Çok gürültülü DEBUG | Filtre | Alan bazlı flag |

## İlgili belgeler ve skill'ler

- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../agentic-secrets-handling/SKILL.md`
- `../agentic-telemetry-optional/SKILL.md`
- `../agentic-trajectory-recording/SKILL.md`
