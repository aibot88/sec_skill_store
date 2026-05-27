---
name: rn-firebase-entegrasyonu
description: React Native uygulamada Firebase modüllerinin (Auth/Firestore/Storage/Crashlytics vb.) entegrasyonunu projeye uygun standartta uygulat; config, environment ve güvenli kullanım kurallarını uygula.
tags: [react-native, firebase, auth, firestore, storage]
---

## Amaç
Mobilde Firebase’i “tek yerden” yönetmek; config ve env hatalarını azaltmak.

## Ne zaman kullanılır?
- Yeni Firebase modülü eklerken
- Android/iOS config güncellenirken
- Prod/test ortamları karıştığında

## Kurallar
- Firebase init/config tek bir modülde yapılır ve uygulama geneline buradan servis edilir.
- UI katmanı Firebase SDK API’lerini doğrudan çağırmaz.
- Hata kodları tek tip `AppError` modeline map edilir.

## Kontrol listesi
- Ortamlar: dev/staging/prod Firebase project ayrımı net mi?
- Auth: token/oturum yenileme davranışı ve logout temizliği doğru mu?
- Firestore: query’ler index ihtiyacı için notlanıyor mu?
- Loglama: PII yazılmıyor mu?

## Çıktı formatı
- Kurulum adımları (repo dosya yolları ile)
- Servis katmanı örnekleri (AuthService, LessonsService)
- Riskler
