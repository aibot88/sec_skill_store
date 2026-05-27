---
name: agentic-mcp-client-config
description: MCP sunucu listesinin config şekli, stdio vs HTTP ve env injection kurallarını tanımlarken kullan.
---

## Amaç

Yapılandırma: örn. **`mcp_servers`** YAML dizisi — `name`, `command`+`args` (stdio) veya `url` (HTTP/SSE, proje kararı). **Env injection**: sunucuya hangi env geçirilir; secret’lar dikkatli. **Güvenilir kaynak**: yalnız kullanıcı eklediği sunucular; rastgele URL kabul etme. `agentic-feature-flags` ile varsayılan kapalı olabilir.

## Kapsam

### Dahil

- Başlangıç timeout ve sağlık kontrolü.
- Sunucu çöküşünde yeniden bağlanma (proje kararı).

### Hariç

- MCP sunucu implementasyon rehberi.

## Kurallar

- Her sunucu için çalışma dizini ve PATH dokümante.
- Ağ tabanlı MCP için TLS ve allowlist (`agentic-threat-model`).
- `agentic-mcp-tool-mapping` ile isim çakışması önlemi.

## Kontrol listesi

- [ ] Örnek config repoda secret içermiyor mu?
- [ ] Bilinmeyen sunucu eklerken onay var mı?
- [ ] stdio buffer deadlock senaryosu ele alındı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Server start fail | command path | `which` / absolute path |
| Protocol uyumsuzluğu | SDK sürümü | Pin version |

## İlgili belgeler ve skill'ler

- `../agentic-mcp-tool-mapping/SKILL.md`
- `../agentic-feature-flags/SKILL.md`
- `../agentic-offline-airgap-notes/SKILL.md`
- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
