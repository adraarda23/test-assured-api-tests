---
marp: true
theme: default
paginate: true
size: 16:9
---

# Yapay Zeka Destekli Yazılım Test Mühendisliği

**Ödev:** REST Assured ile servis regresyon testi otomasyonu
**Demo proje:** Tasks API + REST Assured test paketi
**Sunan:** Arda Aydın Kılınç

---

## Gündem

1. Yazılım test mühendisliği — neden var, ne işe yarar
2. Test otomasyonu ve test piramidi
3. REST Assured'un yeri
4. Yapay zeka destekli test mühendisliği
5. Bu projeyi yapay zeka ile nasıl geliştirdim
6. Demo
7. Avantajlar, riskler ve pratik öneriler

---

## Yazılım test mühendisliği nedir?

Bir yazılımın **doğru çalıştığını** ve **çalışmaya devam ettiğini** sistematik olarak kanıtlama disiplini.

Üç temel sorunun cevabını arar:

- **Doğruluk:** Beklenen davranışı yapıyor mu?
- **Sağlamlık:** Hatalı veri veya yük altında nasıl davranıyor?
- **Regresyon:** Yeni bir değişiklik eski özellikleri bozdu mu?

Manuel test ölçeklenmez — her commit'te tüm senaryoyu insanın tekrar koşmasını isteyemeyiz. Bu nedenle **otomatik regresyon testleri** üretiriz.

---

## Test piramidi

```
              /\
             /E2E\           az sayıda, yavaş, kırılgan
            /------\
           / Integ. \        orta sayıda, orta hızda
          /----------\
         /   Unit     \      çok sayıda, hızlı, ucuz
        /--------------\
```

Pratik kural: **çok unit, makul integration, az E2E**.

Bu projede:
- **24 unit test** (Mockito + saf JUnit) — milisaniye seviyesinde
- **12 integration test** (REST Assured + Spring Boot embedded server) — gerçek HTTP çağrıları

---

## REST Assured neden?

Java tarafında HTTP API'leri test etmek için en yaygın kütüphane.

```java
given()
    .body(Map.of("title", "Buy milk", "completed", false))
.when()
    .post("/tasks")
.then()
    .statusCode(201)
    .body("title", equalTo("Buy milk"))
    .time(lessThan(2000L));
```

Üç şeyi tek bir akıcı zincirde söyletir:

- **Status code** — `.statusCode(201)`
- **Response body** — `.body("title", equalTo(...))`
- **Süre** — `.time(lessThan(2000L))`

Ödevin gerektirdiği üç kontrol de buraya sığıyor.

---

## Yapay zeka destekli test mühendisliği — manzara

LLM tabanlı asistanlar (Claude, Copilot, Cursor vb.) ile test mühendisliği artık iki yönlü:

| Klasik test mühendisliği | + AI desteği |
|---|---|
| İnsan testi yazar | İnsan + asistan birlikte yazar |
| Senaryo aklına gelen | LLM "kenar durumu unuttun mu?" diye sorar |
| Stack trace okunur | LLM hatayı özetler ve düzeltme önerir |
| Test dokümanı manuel | Asistan dokümantasyon ve raporu üretir |

Önemli: **AI, test mühendisini değiştirmiyor; karar merci hâlâ insan.** Düşünmeyi outsource edersen yanlış güvene düşersin.

---

## AI'nın test yaşam döngüsündeki tipik rolleri

1. **Test üretimi** — Belirtilen bir API/sınıf için temel pozitif ve negatif senaryoları otomatik üretmek
2. **Test oracle** — "Bu çıktı doğru mu?" kararını bilgi tabanından çıkarmak (özellikle ML/üretken sistemlerde)
3. **Test bakımı** — Üretim kodu değişince bozulan testleri otomatik güncellemek, flakiness analizi
4. **Hata triyajı** — Stack trace'ten kök neden hipotezi üretmek, log korelasyonu
5. **Doğal dilden senaryoya** — "Kullanıcı sepete ürün eklerse stok azalmalı" → çalıştırılabilir test

Her biri **insan denetiminde** kullanıldığında değer üretir.

---

## Bu projeyi yapay zeka ile nasıl geliştirdim

Süreç tamamen **insan + asistan eş geliştirme**:

1. PDF gereksinimi yapay zekaya verildi → 4 aşamalı plan üretildi
2. Her aşama **mikro commit**'lere bölündü (toplam 35+ commit)
3. Asistan kod önerdi, ben okudum, gerektiğinde itiraz ettim:
   - Tek modül vs çok modül kararı tartışıldı
   - Unit testlerin nereye konulacağı düzeltildi
   - Boilerplate kod (POJO) record'a refactor edildi
4. Her adımda `mvn verify` çalıştırılıp **regresyonun korunduğu** doğrulandı

Sonuç: **24 unit + 12 integration test, hepsi yeşil, multi-module Maven projesi.**

---

## Demo akışı

Canlı gösterim sırası:

1. `git log --oneline` — küçük ve okunabilir commit geçmişi
2. `mvn -pl api spring-boot:run` — Spring Boot Tasks API'yi ayağa kaldır
3. `curl http://localhost:8080/api/tasks` — endpoint'lerin çalıştığını göster
4. Bir REST Assured test sınıfını aç — örn. `CreateTaskIT`
5. `mvn verify` — tüm test paketini koştur, yeşili göster
6. IntelliJ test ağacında pas/fail/süre dağılımı
7. CI yeşil rozeti (GitHub Actions)

---

## Avantajlar

- **Hız:** Boilerplate testler dakikalar içinde
- **Kapsam:** "Negatif senaryoyu unutma" hatırlatması sayesinde 400/404 senaryoları doğal olarak eklendi
- **Öğretici:** Asistan açıklarken neden öyle yaptığını anlatıyor — yeni bir kütüphaneyi öğrenmek hızlanıyor
- **Tutarlılık:** Tüm testlerde aynı patern (status + body + time) korunuyor
- **Geri besleme:** Hata mesajından kök nedeni bulmak saatler yerine dakikalar sürüyor

---

## Riskler ve dikkat edilmesi gerekenler

- **Halüsinasyon:** Asistan var olmayan bir metot/parametre uydurabilir — derleyici ve testler bu yüzden değerli
- **Yanlış güven:** "AI yazdı, doğrudur" tuzağı. Her testin **ne kanıtladığını** insan bilmeli
- **Üretim kodu mu, test kodu mu test ediliyor?** AI hem üretim hem test yazıyorsa ikisinin aynı yanlışı paylaşma riski var
- **Gizlilik:** Şirket içi koda LLM erişimi politikaya tabi
- **Yetkinlik kaybı:** Asistan olmadan stack trace okuyabilen mühendis hâlâ gerekli

---

## Pratik öneriler

1. **Asistanı code reviewer gibi düşün** — kabul/ret kararı sende
2. **Mikro adımlar** — büyük tek seferlik üretim yerine küçük commit'ler, her birinde test koş
3. **Test isimlerini insan yaz** — "ne kanıtladığımı" en iyi sen bilirsin
4. **Negatif senaryoları açıkça iste** — "404, 400, boş input için de test ekle" demeyi unutma
5. **Refactor'ı asistana yaptır, kararı sen ver** — boilerplate temizliği AI'ın en iyi olduğu yerdir
6. **CI'a güven, lokal başarıya değil** — temiz makine + farklı JDK = farklı sonuç olabilir

---

## Sonuç

- Yazılım test mühendisliği, yazılımı **güvenle değiştirebilmenin** disiplini
- REST Assured + JUnit + Maven, JVM dünyasında bu işin defacto stack'i
- Yapay zeka, mühendisin **hızını ve kapsamını** büyütüyor — yargısını değil
- Bu projede 4 aşamada, mikro commit'lerle, AI eş geliştirmeyle üretildi
- Repo: `github.com/adraarda23/test-assured-api-tests`

**Sorular?**
