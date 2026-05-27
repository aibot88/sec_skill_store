---
name: Competitor Radar
description: Rakiplerin içeriklerini (Instagram, TikTok) ve reklam stratejilerini (Meta Ads vb.) analiz ederek içerik boşluklarını (content gap) bulmaya yarayan araştırma motoru.
---

## Açıklama

`rakip-analiz` yeteneği, Antigravity'nin istenen rakip veya pazar alanına dair veri toplamasına ve bu veriyi LLM ile "Content Gap (İçerik Boşluğu)" veya strateji raporlarına dönüştürmesine olanak tanır. 

Bu skill *modüler* bir yapıdadır. Hedef platforma göre ilgili *collector (veri toplayıcı)* çağrılır (örn: Apify Actor) ve elde edilen veriler analiz motoruna (`analyzer.py`) gönderilerek anlamlı bir Markdown raporuna çevrilir.

## Gereksinimler

- `python3 -m pip install -r scripts/requirements.txt` ile bağımlılıkların kurulu olması.
- `.env` veya `_knowledge/api-anahtarlari.md` tabanlı Apify ve Gemini/OpenAI API anahtarlarının ("APIFY_API_TOKEN", "GEMINI_API_KEY") ayarlanmış olması.

## Adımlar

1. Rakibin hangi kanalının analiz edileceğine karar ver (ig profil, meta reklamları vb.).
2. Ana router olan `radar_engine.py` scriptini uygun parametrelerle çağır.
3. Script, ilgili collector'ı çalıştırıp datayı çeker, LLM'e özetletir ve belirlenen klasöre (varsayılan: `/tmp/radar_report.md` veya `artifacts`) kaydeder.

## Komut Kullanımı (CLI)

```bash
# Instagram gönderi analizi için (Apify Instagram Scraper kullanarak):
python3 _skills/rakip-analiz/scripts/radar_engine.py \
  --target "example_competitor_ig" \
  --module "apify_ig" \
  --output "/tmp/radar_report_ig.md"

# Meta reklam analizi için:
python3 _skills/rakip-analiz/scripts/radar_engine.py \
  --target "example_competitor_page_name" \
  --module "meta_ads" \
  --output "/tmp/radar_report_ads.md"
```

### Parametreler
- `--target`: Hedef hesap adı, arama terimi veya URL.
- `--module`: Kullanılacak veri toplama modülü. Desteklenenler: `apify_ig`, `meta_ads`
- `--output`: Analiz raporunun kaydedileceği Markdown dosyası yolu.

## Modüller (Collectors)

- **apify_ig:** Apify'daki Instagram scraper actor'lerini kullanarak son postları, likes/comments oranlarını ve metinlerini çeker.
- **meta_ads:** Facebook Ad Library veya Apify Meta Ads scraper kullanarak rakibin anlık aktif reklam içeriklerini çeker.

## Analiz Raporu Çıktısı (`analyzer.py`)
Toplanan veriyi şu başlıklarla sentezler:
- Genel Durum (Ne paylaşıyorlar, sıklık vb.)
- En Çok Etkileşim Alan Konseptler (Winners)
- İçerik Boşlukları (Bizim ne yapmamız lazım?)
- Örnek Post Fikirleri
