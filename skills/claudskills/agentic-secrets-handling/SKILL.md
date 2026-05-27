---
name: agentic-secrets-handling
description: API anahtarları, kubeconfig ve Juju credential için saklama sırası ve log maskeleme kurallarını uygularken kullan.
---

## Amaç

Sırlar için öncelik sırası: **secret manager / vault (tercih)** > **ortam değişkeni** > **kısıtlı izinli dosya** (ör. `chmod 600`). `.env` dosyası **asla** commit edilmez; `.env.example` yalnız placeholder içerir. Log ve trajectory çıktılarında **maskeleme** zorunlu. Env isimleri `LLM_PROVIDERS.md` ile uyumlu tutulur (`SENTINEL_API_KEY`, `ANTHROPIC_API_KEY`, `SENTINEL_LOCAL_*`, vb.).

## Kapsam

### Dahil

- LLM API anahtarları, isteğe bağlı OAuth/token (ürün kararı).
- `kubeconfig`, Juju credentials, cloud config dosyaları.

### Hariç

- Vault ürününün kurulum rehberi (harici dokümantasyon).

## Kurallar

- Repo içinde gerçek anahtar tespitinde: rotate + `git history` temizliği (proje prosedürü).
- Debug log seviyesinde bile anahtar ve JWT benzeri stringler **redact**.
- CI’da fork PR’lar için secret yok varsayımı (`agentic-ci-github-actions`).

## Kontrol listesi

- [ ] `.gitignore` `.env` ve yerel credential dosyalarını kapsıyor mu?
- [ ] Uygulama başlangıcında “env’de key var mı” kontrolü kullanıcıya güvenli mesajla mı dönüyor?
- [ ] Trajectory kaydında PII/secret filtreleri tanımlı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Anahtar loga düştü | Log handler | Maskeleme kuralı ekle, anahtarı rotate et |
| Yanlış env okundu | Profil önceliği | `agentic-config-layers` sırasını doğrula |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-cli-logging/SKILL.md`
- `../agentic-config-env-reference/SKILL.md`
- `../agentic-trajectory-recording/SKILL.md`
