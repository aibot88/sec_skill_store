---
name: palo-alto
description: PAN-OS firewall'unda DNAT (port yönlendirme) ve security policy source kısıtlama işlerini doğal dilden uygular. Müşteri tek cümlede ister ("198.51.100.108'in 80 portu 192.168.1.50:90'a yönlendirilsin" / "RULE_108 sadece şu IP'lere açık olsun"); skill firewall'a doğrudan bağlanır, çakışmaları kontrol eder, idempotent şekilde NAT + security policy + service/address objelerini oluşturur ve commit eder. Credential'lar sadece process içinde tutulur, diske yazılmaz. Her çağrı öncesi auto-update yapar (24h cache).
---

# Palo Alto Doğal Dil Skill

PAN-OS firewall'una **doğrudan** Claude Code üzerinden iş yaptırır. Müşteri tek cümle yazar — skill geri kalanını yapar.

## Kullanım Modeli

1. **Müşteri tek cümlede konuyu söyler.**
   > "10.0.0.1, admin/MyPass123. 198.51.100.108'in 80 portu 192.168.1.50:90'a yönlendir."
2. **Claude credential'ları env var olarak set eder, ilgili script'i çağırır.** Credential'lar process içinde yaşar, exit'te kaybolur.
3. **Skill çakışma kontrolü yapar, hata varsa açıklayıcı Türkçe mesaj döner; sorun yoksa uygular ve commit eder.**

## Claude'un Akış Şeması

Claude bu skill'i kullanırken şu adımları takip eder:

### Adım 0 — Auto-update (otomatik)

`dnat.py`, `restrict_source.py` ve `free_ip.py` `main()`'ları başlangıçta `runtime.auto_update()` çağırır; bu da `update.sh`'i best-effort olarak fork eder (24h cache, network hatası silent skip, timeout 15s). Skill her zaman en güncel commit ile çalışır, Claude'un ek bir şey yapması gerekmez.

Devre dışı bırakmak istersen (test ortamı): `export PALO_ALTO_SKIP_AUTO_UPDATE=1`.

### Adım 1 — Firewall bilgilerini topla
Eğer henüz bilinmiyorsa, müşteriden iste:
- `host` (firewall mgmt IP veya FQDN)
- `username` ve `password` (veya doğrudan API key)
- Self-signed cert kullanıyorsa: `insecure=true` (varsayılan)

Müşteri aynı sohbette daha önce verdiyse aynı bilgileri kullan — yeniden sorma.

### Adım 2 — Bağlantı kurulumu (ilk kullanımda)

macOS/Linux:
```bash
bash ~/.claude/skills/palo-alto/scripts/setup.sh
```

Windows (PowerShell):
```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\skills\palo-alto\scripts\setup.ps1"
```

Her iki platformda da sadece Python venv + `pan-os-python` kurar. Credential sormaz, hiçbir şey saklamaz.

### Adım 3 — İsteğe göre script çağrısı

Komutu çalıştırırken sadece **işletim sistemine göre python yolu** ve **env var söz dizimi** değişir; argümanlar ve script aynıdır.

| Platform | Python yolu | Env var söz dizimi (örnek) |
|----------|-------------|---------------------------|
| macOS / Linux | `~/.palo-alto/venv/bin/python` | `KEY=value cmd` (tek satır) |
| Windows (PowerShell) | `$env:USERPROFILE\.palo-alto\venv\Scripts\python.exe` | `$env:KEY='value'` (önceki satırda) |

**DNAT — müşteri spesifik WAN IP söylediyse:**

> "198.51.100.108'in 80 portu 192.168.1.50:90'a yönlendir"

macOS/Linux:
```bash
PANOS_HOST=10.0.0.1 \
PANOS_USERNAME=admin \
PANOS_PASSWORD=MyPass123 \
PANOS_INSECURE=1 \
~/.palo-alto/venv/bin/python ~/.claude/skills/palo-alto/scripts/dnat.py \
  --wan-ip 198.51.100.108 \
  --public-port 80 \
  --target-ip 192.168.1.50 \
  --target-port 90
```

Windows (PowerShell):
```powershell
$env:PANOS_HOST='10.0.0.1'
$env:PANOS_USERNAME='admin'
$env:PANOS_PASSWORD='MyPass123'
$env:PANOS_INSECURE='1'
& "$env:USERPROFILE\.palo-alto\venv\Scripts\python.exe" `
  "$env:USERPROFILE\.claude\skills\palo-alto\scripts\dnat.py" `
  --wan-ip 198.51.100.108 --public-port 80 `
  --target-ip 192.168.1.50 --target-port 90
```

**DNAT — müşteri "boş bir IP bul" dediyse:**

> "Boş bir IP'nin 80 portu 192.168.1.50:90'a yönlensin"

```bash
PANOS_HOST=... PANOS_USERNAME=... PANOS_PASSWORD=... PANOS_INSECURE=1 \
~/.palo-alto/venv/bin/python ~/.claude/skills/palo-alto/scripts/dnat.py \
  --public-port 80 --target-ip 192.168.1.50 --target-port 90
```

**Source IP kısıtlama:**

> "RULE_108 sadece 203.0.113.46 için açık olsun"

```bash
PANOS_HOST=... ... ~/.palo-alto/venv/bin/python \
  ~/.claude/skills/palo-alto/scripts/restrict_source.py \
  --rule RULE_108 --source-ips 203.0.113.46
```

**Boş IP/port önizleme (read-only):**

```bash
PANOS_HOST=... ... ~/.palo-alto/venv/bin/python \
  ~/.claude/skills/palo-alto/scripts/free_ip.py [--port 80]
```

### Adım 4 — JSON sonucunu yorumla

Tüm script'ler stdout'a JSON döner. Hata yoksa `"status": "applied"`, hata varsa `"status": "error"` + `"kind"` + `"error"`.

#### Hata türleri ve Claude'un müşteriye söyleyeceği şey

| `kind` | Anlam | Claude → müşteri (Türkçe) |
|--------|-------|---------------------------|
| `config` | Env var eksik | "Firewall bilgilerini tekrar verir misin? (host, kullanıcı, şifre)" |
| `wan_subnet_mismatch` | Müşteri WAN subnet'i dışı IP verdi | JSON'daki `wan_subnet` field'ını kullan: "Verdiğin IP firewall'unun WAN subnet'i (X) içinde değil. Lütfen o aralıktan bir IP seç." |
| `port_conflict` | İstenen port o IP'de zaten kullanımda | JSON'daki `conflicting_rules` listesini göster: "Bu port o IP'de zaten kullanılıyor (kural: ...). Farklı bir IP veya port seç." |
| `object_conflict` | Aynı isimde farklı parametreli kural mevcut | Farkı göster, manuel rename öner |
| `not_owned` | Skill, operatörün yarattığı bir kuralı/objeyi silmeye veya source'unu değiştirmeye çalıştı | JSON'daki `object_kind` + `object_name` + `action` field'larını kullan: "Bu kural senin firewall'unda zaten var ve skill tarafından yaratılmadığı için silinemez/değiştirilemez. Sadece destination'unu güncellemek istersen `--update` ile yapabilirim." |
| `auth_expired` | API key süresi dolmuş veya PA kimliği reddetti | "PA kimlik bilgisini reddetti — büyük olasılıkla API key'in süresi dolmuş. `auth.py` çalıştırıp host/kullanıcı/şifreyi tekrar gir, skill yeni key alacak." |
| `commit` | Commit hatası | Firewall'un dönen mesajını göster (validation hatası vb.) |
| `panos` | Genel PAN-OS API hatası | Hata mesajını ham hâliyle göster |

## Çakışma Kontrol Mantığı (Müşterinin Beklediği Davranış)

Müşteri "198.51.100.99'un 80 portu ..." dediğinde skill ŞU sırayla kontrol eder:

1. **IP formatı geçerli mi?** Değilse → reddedilir.
2. **IP firewall'un WAN subnet'inde mi?** `198.51.100.96/28` dışında bir IP verdiyse (örnek: 1.2.3.4) → `wan_subnet_mismatch` hatası.
3. **Bu IP'de istenen port/range zaten başka NAT rule'da kullanılıyor mu?** Evet ise → `port_conflict` hatası + çakışan rule isimleri.
   - Service-group'ları açar; `PORT_7081_TCP` veya `7000-7010` range'i de tetikler.
   - `service=any` kuralı varsa o IP'nin TÜM portları tutuluyor sayılır.
   - Firewall'un kendi WAN IP'si de DNAT için geçerli hedef sayılır (tek-public-IP'li kurumlar için yaygın). Sadece port çakışması varsa engellenir.
4. **Aynı isimde NAT/security rule farklı parametre ile var mı?** Evet ise → `object_conflict` (üzerine YAZILMAZ).
5. **Aynı isimde, aynı parametre ile var mı?** → No-op (idempotent, tekrar çalıştırma güvenli).

## Hard Isolation — Skill Yalnızca Kendi Yarattığı Kurallara Müdahale Eder

Skill'in **yazma yetkisi** kasten dar:

| İşlem | Kim üzerinde? |
|-------|---------------|
| Yeni NAT/security/address/service yaratma | Sadece kendi (her yarattığına `[skill-managed]` marker ekler) |
| `--remove` (NAT + security + orphan address/service) | **YALNIZCA skill-managed kurallar.** Operatör kuralları `not_owned` ile reddedilir. |
| `restrict_source.py` (security policy source güncelleme) | **YALNIZCA skill-managed kurallar.** |
| `--update` (NAT rule destination IP/port değişimi) | **Skill-managed + operatör kuralları** — TEK istisna. |
| Diğer her şey (zone, interface, VPN, audit log, vs.) | Yetki yok. |

Marker kontrolü `description.startswith("[skill-managed]")` ile yapılır. Operatörün manuel yarattığı her şey skill'in dokunamayacağı alandadır. Discovery (`free_ip.py`, conflict scan) **read-only** olduğu için operatör config'ini okuyabilir, sadece yazma kapsamı kısıtlıdır.

### `--remove` ve Otomatik GC

Bir kuralı sildiğinde (`dnat.py --remove RULExxx` veya doğal dil "RULExxx'i sil"):

1. NAT rule skill-managed mi? Değilse `not_owned` ile reddedilir.
2. Naming convention'la eşleşen security rule (`RULE_xxx`) bulunur — skill-managed ise silinir; operatör'ünki ise dokunulmaz.
3. **Otomatik orphan cleanup:** İki kuralın referans verdiği address/service objeleri taranır. Bir obje SİLİNİR ancak şu şartlarda:
   - Description'ında `[skill-managed]` marker'ı taşıyor, VE
   - Hiçbir başka NAT/security rule veya group bu objeyi kullanmıyor.
4. Address-group içindeki üyeler recursive olarak temizlenir.
5. Tüm değişiklikler tek commit ile uygulanır.

JSON sonucu `deleted_orphans` ve `kept_objects` (`name`, `reason`) listelerini içerir. `reason` örnekleri: `not-skill-managed`, `used-by-N-other-refs`.

### `--update` — Mevcut Kuralın İç Hedefini Değiştir

```
dnat.py --update RULE100 --target-ip 10.0.10.222 --target-port 9090
```

`destination_translated_address` + `destination_translated_port` güncellenir. **Kuralın adı, WAN tarafı, zone'lar, source filter, service object, eşli security policy — hepsi olduğu gibi kalır.** Tek değişen iç hedef.

Operatör kuralında çalıştığında skill yeni target address objesini `[skill-managed]` marker ile yaratır (gelecekteki GC için). Eski destination address skill-managed ve sıfır referans ise GC'ye girer; operatör objesi ise korunur. Yanıttaki `rule_owned_by: "skill"|"operator"` hangi yolu izlediğini gösterir.

## Mimari Kararlar

1. **Credential persistence YOK** — env var üzerinden geçer, process exit'te kaybolur. Şifre asla diske yazılmaz.
2. **pan-os-python SDK** — direkt Python kütüphanesi. Idempotency, conflict detection ve transaction kontrolü güvenilir.
3. **TLS** — `PANOS_INSECURE=1` ile self-signed cert kabul edilir (firewall mgmt cert'leri genelde self-signed olduğu için müşteri-dostu). `PANOS_CA_BUNDLE` ile pinned cert mümkün. Default behavior PAN-OS gerçekliğine uygundur.
4. **Tek müşteri tek firewall** — `customer_id` veya profile dosyası yok. Müşteri kendi Claude'unu kurar, kendi firewall'una bağlanır.
5. **Direct apply + commit** — başarısızlıkta PAN-OS candidate'ı otomatik geri alır.
6. **Naming convention** — WAN_IF108, SERVER_50, SVC_80_TCP, RULE108, RULE_108. Standart PA naming pattern. Override `PANOS_*` env var'ları ile mümkün (zone/interface).
7. **Default security profile** — yeni security rule'a `virus=default, spyware=strict, vulnerability=strict, wildfire-analysis=default` uygulanır (yaygın güvenlik baseline).
8. **`[skill-managed]` marker'ı** — yaratılan her address/service/group/NAT/security objesinin `description` alanına eklenir. `--remove`'un otomatik orphan cleanup'ı sadece bu marker'ı taşıyan + zero-reference objeleri siler; operatörün elle yarattığı her şey korunur.

## Dosya İndeksi

| Dosya | Amaç |
|-------|------|
| `scripts/setup.sh` | Tek seferlik: venv + pan-os-python kurulumu |
| `scripts/config.py` | Env var → Config (creds dahil, sadece bellek) |
| `scripts/panos_client.py` | Idempotent CRUD wrapper |
| `scripts/discovery.py` | Boş IP/port keşfi + çakışma tespiti |
| `scripts/dnat.py` | DNAT entry point |
| `scripts/restrict_source.py` | Source IP kısıtlama entry point |
| `scripts/free_ip.py` | Boş IP/port önizleme (read-only) |
| `scripts/update.sh` | Auto-update — her çağrı öncesi 24h cache'li git pull |
| `references/xml-api-cheatsheet.md` | XML API debug komutları (manuel teşhis) |
| `references/troubleshooting.md` | Sık karşılaşılan sorunlar |

## Env Var Referansı

| Var | Zorunlu | Açıklama |
|-----|---------|----------|
| `PANOS_HOST` | ✓ | Firewall mgmt IP veya FQDN |
| `PANOS_API_KEY` | (api_key veya user/pass) | API key — varsa öncelikli |
| `PANOS_USERNAME` | (api_key yoksa) | Admin kullanıcı |
| `PANOS_PASSWORD` | (api_key yoksa) | Admin şifresi (process içinde, diske yazılmaz) |
| `PANOS_INSECURE` | opsiyonel | `1` → TLS verify skip (self-signed için) |
| `PANOS_CA_BUNDLE` | opsiyonel | CA PEM path (TLS verify yapılacaksa) |
| `PANOS_WAN_ZONE` | opsiyonel | default: `WAN` |
| `PANOS_LAN_ZONE` | opsiyonel | default: `LAN` |
| `PANOS_WAN_INTERFACE` | opsiyonel | default: `ethernet1/2` |
| `PANOS_LAN_INTERFACE` | opsiyonel | default: `ethernet1/1` |
| `PANOS_VSYS` | opsiyonel | default: `vsys1` |
| `PANOS_WAN_SUBNET` | opsiyonel | CIDR override; yoksa interface'den okunur |
