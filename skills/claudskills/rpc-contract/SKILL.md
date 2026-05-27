---
name: rpc-contract
description: RPC contract validation — Contract-first development, direkt REST bypass yasak
version: 1.0.0
session: dev
---

# RPC Contract Skill

## 🗣️ Dil Kuralı

**ANADİL: TÜRKÇE**

- ✅ Tüm yorumlar, commit mesajları **Türkçe**
- ✅ Toast/error mesajları **Türkçe**
- ❌ Kullanıcı istemedikçe İngilizce kullanma

---

## 🎯 Ne Zaman Kullanılır

**Bu skill SADECE `dev` session'da aktif olur.**

- RPC çağrısı yapmadan önce
- Yeni RPC fonksiyonu yazarken
- Mevcut REST bypass kodunu RPC'ye çevirirken
- RPC contract validation gerektiğinde

---

## 📚 RPC Kuralı (KRİTİK)

### ⛔ YASAK

```javascript
// ❌ Direkt INSERT/UPDATE/DELETE/PATCH — YASAK!
await supabase.from('tohumlama').insert({...})
await supabase.from('hayvanlar').update({...}).eq('id', id)
await supabase.from('dogum').delete().eq('id', id)
await supabase.from('hastalik').update({...}).eq('id', id)

// ❌ Direkt REST bypass — YASAK!
write('tohumlama', {...})  // write() fonksiyonu yasak
```

### ✅ DOĞRU

```javascript
// ✅ SADECE RPC kullan
await rpcOptimistic('tohumlama_kaydet', { 
  p_hayvan_id: hayvanId, 
  p_tarih: tarih 
})

await rpcOptimistic('dogum_kaydet', {
  p_anne_id: anneId,
  p_tarih: tarih
})

await rpcOptimistic('hayvan_guncelle', {
  p_id: id,
  p_alan: 'grup_id',
  p_deger: yeniGrupId
})
```

---

## 📋 Kullanım Öncesi Kontrol Listesi

Her RPC çağrısı öncesi:

```
[ ] RPC adı `.claude/rpc-reference.md`'de var mı?
[ ] Parametreler imzayla eşleşiyor mu? (p_ prefix kontrolü)
[ ] Return type `{ ok: boolean, ... }` formatında mı?
[ ] `rpcOptimistic(name, params, opts)` — 1. parametre string RPC adı
[ ] Türkçe toast/error mesajları var mı?
```

---

## 🔍 RPC İmza Doğrulama

### Örnek: tohumlama_kaydet

**rpc-reference.md'den kontrol:**
```sql
CREATE OR REPLACE FUNCTION tohumlama_kaydet(
  p_hayvan_id UUID,
  p_tarih DATE,
  p_sperma_kodu TEXT DEFAULT NULL,
  p_teknisyen TEXT DEFAULT NULL
) RETURNS JSONB
```

**Doğru kullanım:**
```javascript
const result = await rpcOptimistic('tohumlama_kaydet', {
  p_hayvan_id: hayvanId,      // UUID
  p_tarih: tarih,              // DATE
  p_sperma_kodu: spermaKodu,   // TEXT (opsiyonel)
  p_teknisyen: teknisyen       // TEXT (opsiyonel)
})

// Return: { ok: true, tohumlama_id: '...' }
```

**Yanlış kullanım:**
```javascript
// ❌ Parametre adı yanlış (p_ prefix yok)
await rpcOptimistic('tohumlama_kaydet', {
  hayvan_id: id,  // YANLIŞ → p_hayvan_id olmalı
  tarih: tarih
})

// ❌ Return type yanlış
const result = await rpcOptimistic(...)
console.log(result.data)  // YANLIŞ → result.ok kontrol et
```

---

## 🚨 Sık Yapılan Hatalar

| Hata | Çözüm |
|------|-------|
| **Direkt INSERT** | `rpcOptimistic()` kullan |
| **p_ prefix eksik** | Parametre adlarını rpc-reference.md'den kontrol et |
| **Return type yanlış** | `{ ok: boolean, ... }` formatı kullan |
| **RPC adı yanlış** | `.claude/rpc-reference.md` kontrol et |
| **Yasak fonksiyon** | `write()` yerine `rpcOptimistic()` |

---

## 📖 RPC Hızlı Referans

### Tohumlama
```javascript
rpcOptimistic('tohumlama_kaydet', { p_hayvan_id, p_tarih, p_sperma_kodu, p_teknisyen })
rpcOptimistic('tohumlama_sonuc_gebe', { p_tohumlama_id })
rpcOptimistic('tohumlama_sonuc_bos', { p_tohumlama_id })
```

### Doğum
```javascript
rpcOptimistic('dogum_kaydet', { p_anne_id, p_tarih, p_buzagi_cinsiyet, p_buzagi_kupe })
```

### Hayvan
```javascript
rpcOptimistic('hayvan_ekle', { p_kupe_no, p_grup_id, p_dogum_tarihi, p_cinsiyet })
rpcOptimistic('hayvan_guncelle', { p_id, p_alan, p_deger })
```

### Hastalık
```javascript
rpcOptimistic('hastalik_kaydet', { p_hayvan_id, p_tanis, p_tarih })
rpcOptimistic('hastalik_kapat', { p_id, p_kapanis_tarihi })
rpcOptimistic('hastalik_sil', { p_id })
```

### Tedavi
```javascript
rpcOptimistic('tedavi_ekle', { p_hastalik_id, p_ilac_id, p_doza, p_sure })
rpcOptimistic('tedavi_sil', { p_id })
rpcOptimistic('tedavi_guncelle', { p_id, p_alan, p_deger })
```

---

## 🛡️ Güvenlik Kuralı

**SQL Injection Önleme:**

```javascript
// ❌ YANLIŞ — String concat ile SQL injection riski
const query = `SELECT * FROM hayvanlar WHERE kupe_no = '${kupeNo}'`

// ✅ DOĞRU — RPC parametre binding kullanır
await rpcOptimistic('hayvan_bul', { p_kupe_no: kupeNo })
```

**RPC otomatik parametre binding yapar — SQL injection güvenli!**

---

## 📋 Checklist (Her RPC Çağrısı)

```
[ ] RPC adı `.claude/rpc-reference.md`'de doğrulandı
[ ] Parametreler p_ prefix ile doğru
[ ] Return type { ok: boolean, ... } kontrol edildi
[ ] rpcOptimistic() kullanıldı (direkt REST yok)
[ ] Türkçe toast/error mesajları var
[ ] node --check geçti
```

---

## 📖 Referanslar

- **RPC İmzaları:** `.claude/rpc-reference.md`
- **Domain Kuralları:** `.claude/domain-rules.md`
- **UI Haritası:** `.claude/ui-map.md`

---

**Bu skill yüklendiğinde:** RPC contract-first development mode aktif olur.

🔒 RPC Contract hazır!
