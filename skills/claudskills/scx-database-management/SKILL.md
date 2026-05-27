---
name: scx-database-management
description: SCX-Studio-Pro projesinin Prisma ORM ve SQLite tabanlı veritabanı şemasını, model ilişkilerini, migrasyon süreçlerini ve veri yönetimini açıklar.
---

# SCX-Studio-Pro Veritabanı Yönetimi

Bu skill, SCX-Studio-Pro projesinin veritabanı yapısını ve yönetimiyle ilgili süreçleri detaylandırır. Proje, **Prisma ORM** ve **SQLite** kullanmaktadır.

## 1. Veritabanı Şeması (`prisma/schema.prisma`)

`prisma/schema.prisma` dosyası, projenin tüm veritabanı modellerini ve ilişkilerini tanımlar. Aşağıda kritik modeller ve ilişkileri özetlenmiştir:

### 1.1. `User` Modeli

Kullanıcı bilgilerini (isim, e-posta, roller, API anahtarları vb.) saklar. Diğer birçok modelle bire-çok veya bire-bir ilişkisi vardır.

| Alan Adı | Tipi | Açıklama |
| :--- | :--- | :--- |
| `id` | `String` | Kullanıcı ID (cuid) |
| `name` | `String?` | Kullanıcı adı |
| `email` | `String?` | Kullanıcı e-postası (unique) |
| `emailVerified` | `DateTime?` | E-posta doğrulama tarihi |
| `image` | `String?` | Profil resmi URL'si |
| `isAdult` | `Boolean` | Yetişkin onayı (varsayılan: `false`) |
| `role` | `String` | Kullanıcı rolü (varsayılan: `"USER"`) |
| `gender` | `String?` | Cinsiyet |
| `apiKeys` | `String?` | Kullanıcının API anahtarlarını JSON olarak saklar |
| `createdAt` | `DateTime` | Oluşturulma tarihi |
| `updatedAt` | `DateTime` | Son güncelleme tarihi |
| `accounts` | `Account[]` | Kullanıcının hesapları (NextAuth) |
| `adminActions` | `AdminAction[]` | Admin eylemleri |
| `albums` | `Album[]` | Kullanıcının albümleri |
| `characters` | `CharacterDNA[]` | Kullanıcının karakter DNA'ları |
| `generatedImages` | `GeneratedImage[]` | Kullanıcının ürettiği görseller |
| `securitySettings` | `UserSecuritySettings?` | Kullanıcının güvenlik ayarları (bire-bir ilişki) |

### 1.2. `CharacterDNA` Modeli

Karakterlerin genetik bilgilerini ve görsel referanslarını saklar. Bir `User`'a aittir.

| Alan Adı | Tipi | Açıklama |
| :--- | :--- | :--- |
| `id` | `String` | Karakter ID (cuid) |
| `userId` | `String` | İlişkili kullanıcı ID'si |
| `name` | `String?` | Karakter adı (varsayılan: `"Ana Karakter"`) |
| `isMainCharacter` | `Boolean` | Ana karakter mi (varsayılan: `false`) |
| `faceImages` | `String?` | Yüz görselleri (JSON string) |
| `poseReference` | `String?` | Poz referans görseli |
| `view360PackJson` | `String?` | 360 derece görünüm paketi (JSON string) |
| `user` | `User` | İlişkili kullanıcı (bire-çok) |

### 1.3. `GeneratedImage` Modeli

Üretilen görsellerin detaylarını, kullanılan prompt'ları ve depolama bilgilerini saklar. Bir `User`'a aittir ve isteğe bağlı olarak bir `Album`'e bağlı olabilir.

| Alan Adı | Tipi | Açıklama |
| :--- | :--- | :--- |
| `id` | `String` | Görsel ID (cuid) |
| `userId` | `String` | İlişkili kullanıcı ID'si |
| `promptUsed` | `String` | Görsel üretiminde kullanılan prompt |
| `imageUrl` | `String` | Görselin URL'si |
| `storageSource` | `String` | Depolama kaynağı (varsayılan: `"external"`) |
| `driveFileId` | `String?` | Google Drive dosya ID'si |
| `albumId` | `String?` | İlişkili albüm ID'si |
| `engineUsed` | `String` | Kullanılan AI motoru (varsayılan: `"fal_ai_flux_pulid"`) |
| `isNsfw` | `Boolean` | NSFW içeriği mi (varsayılan: `false`) |
| `user` | `User` | İlişkili kullanıcı (bire-çok) |
| `album` | `Album?` | İlişkili albüm (bire-çok) |

### 1.4. `Album` Modeli

Kullanıcıların görsellerini organize ettiği albümleri temsil eder. Bir `User`'a aittir.

| Alan Adı | Tipi | Açıklama |
| :--- | :--- | :--- |
| `id` | `String` | Albüm ID (cuid) |
| `userId` | `String` | İlişkili kullanıcı ID'si |
| `name` | `String` | Albüm adı |
| `kind` | `String` | Albüm türü (varsayılan: `"standard"`) |
| `visibilityMode` | `String` | Görünürlük modu (varsayılan: `"normal"`) |
| `requiresPin` | `Boolean` | PIN gerektiriyor mu (varsayılan: `false`) |
| `user` | `User` | İlişkili kullanıcı (bire-çok) |
| `images` | `GeneratedImage[]` | Albümdeki görseller |

### 1.5. `UserSecuritySettings` Modeli

Kullanıcıya özel güvenlik ve sağlayıcı ayarlarını saklar. Bir `User` ile bire-bir ilişkisi vardır.

| Alan Adı | Tipi | Açıklama |
| :--- | :--- | :--- |
| `id` | `String` | Ayar ID (cuid) |
| `userId` | `String` | İlişkili kullanıcı ID'si |
| `providerDefaults` | `String?` | Sağlayıcı varsayılanları (JSON string) |
| `providerPools` | `String?` | Sağlayıcı havuzları (JSON string) |
| `selfHostConfig` | `String?` | Self-host yapılandırması (JSON string) |
| `user` | `User` | İlişkili kullanıcı (bire-bir) |

## 2. Migrasyonlar

Veritabanı şemasında yapılan değişiklikler, Prisma migrasyonları aracılığıyla yönetilir. Yeni bir değişiklik yapıldığında aşağıdaki komutlar kullanılır:

```bash
npx prisma migrate dev --name <migration_name>
```

Bu komut, şema değişikliklerini algılar, yeni bir migrasyon dosyası oluşturur ve veritabanına uygular.

## 3. Veritabanı Erişimi

Prisma Client, `lib/core/prisma.ts` üzerinden projenin geri kalanına sağlanır. Veritabanı işlemleri için doğrudan `prisma` objesi kullanılır.

```typescript
import { prisma } from '@/lib/core/prisma';

// Örnek kullanım
const user = await prisma.user.findUnique({ where: { id: userId } });
```

## 4. Bilinen Sorunlar ve Çözümler

*   **`SecuritySettings` Hatası:** Yeni bir kullanıcı oluşturulduğunda veya mevcut kullanıcıda üretim hatası alındığında, `scripts/fix-user-settings.ts` scriptini çalıştırarak varsayılan sağlayıcı ayarlarını (SecuritySettings) veritabanına ekleyin.

Bu skill, SCX-Studio-Pro veritabanı yapısını ve yönetimini anlamak için kapsamlı bir rehber sunar.
