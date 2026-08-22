<p align="center">
  <img src="assets/brand/mintmark-logo.svg" width="112" height="112" alt="Mintmark">
</p>

<h1 align="center">Mintmark sigorta</h1>

<p align="center"><strong>Sağlık branşı sağlık branşı olarak kalan Türkçe poliçe ve hasar verisi.</strong></p>

<p align="center">
  Bireysel ve kurumsal poliçe sahipleri, ana branşlarda poliçeler, ödeme izini<br>
  ile hasarlar ve kişisel verinin saklandığı serbest metin.
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark-insurance/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lokomotifai/mintmark-insurance/ci.yml?branch=main&amp;style=flat-square&amp;label=CI"></a>
  <img alt="Sıfır motor kodu" src="https://img.shields.io/badge/motor%20kodu-yok-3C873A?style=flat-square">
  <img alt="18 kapsam hedefinin 18'i tutturuldu" src="https://img.shields.io/badge/kapsam%20hedefi-18%2F18-3C873A?style=flat-square">
  <img alt="Yayımlanmış sürüm yok" src="https://img.shields.io/badge/sürüm-yayımlanmadı-3B3F46?style=flat-square">
  <a href="LICENSE"><img alt="Apache-2.0 lisansı" src="https://img.shields.io/badge/lisans-Apache--2.0-3B3F46?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark"><img alt="Mintmark çekirdeğini gerektirir" src="https://img.shields.io/badge/çekirdek-%3E%3D0.1%2C%3C0.2-17191F?style=flat-square"></a>
  <img alt="Altı kayıt tipi" src="https://img.shields.io/badge/kayıt%20tipi-6-17191F?style=flat-square">
  <img alt="Yedi sigorta branşı" src="https://img.shields.io/badge/branş-7-17191F?style=flat-square">
  <img alt="26 kurgusal sigortacı adı" src="https://img.shields.io/badge/kurgusal%20sigortaci-26-D11F26?style=flat-square">
  <img alt="Sağlık kategori granülerliğinde kalır" src="https://img.shields.io/badge/sağlık-kategori%20granülerliği-C98A2B?style=flat-square">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/docs-English-D11F26?style=flat-square"></a>
</p>

<p align="center">
  <a href="#kendiniz-basın"><strong>Kendiniz basın</strong></a>
  ·
  <a href="#sağlık-sınırı"><strong>Sağlık sınırı</strong></a>
  ·
  <a href="#taksonominin-bizim-yerimize-verdiği-iki-karar"><strong>Taksonominin kararları</strong></a>
  ·
  <a href="README.md"><strong>English</strong></a>
</p>

---

> **Bu depo hiç motor kodu içermez.** Bildirim ve veridir. Bunları okuyan motor
> [mintmark](https://github.com/lokomotifai/mintmark) deposunda yaşar ve burada
> kapalı üst sınırlı bir sürüm aralığıyla sabitlenmiştir.

Türk sigortacıları, acenteleri ve insurtech ekipleri finansal, davranışsal ve
sağlığa komşu kişisel veriyi bir arada tutan poliçe ve hasar verisi taşır.
Hiçbiri KVKK riski alınmadan test ortamına taşınamaz. Bu paket o veriyi beyan
eder, motor da basar: deterministik, span düzeyinde etiketli ve bir manifestoyla
mühürlenmiş.

**Sürüm 0.1, ön yayın. Hiçbir sürüm yayımlanmadı ve indirilecek bir referans veri
kümesi henüz yok.** Bugün doğru olan: `packcheck` sabitlenmiş çekirdeğe karşı
geçiyor, test paketi geçiyor ve değerlendirme tarifi on sekiz kapsam hedefinin
hepsini tutturuyor.

> [!IMPORTANT]
> **Bu paket ne değildir.** Poliçe verinizin anonimleştirilmesi değildir; hiç veri
> almaz. Uyumluluk garantisi değildir, hukuki güvenli liman değildir. **Klinik veri
> değildir ve onun yerine geçmez**: sağlık branşı tasarım gereği kategori
> granülerliğinde kalır. Anomali tarifi dedektör tarafı test verisidir ve bu depo
> hiçbir atlatma rehberliği içermez. Üretilen telefon numaraları atanmış
> numaralarla çakışabilir, çünkü Türkiye numara planı kurgusal bir aralık ayırmaz.
> Bu veri sistemleri test etmek içindir. Hiçbir zaman kimseye ulaşmak için
> değildir.

## Burada ne var, ne yok

![Sigorta paketinin kayıt tiplerinin diyagramı: bireysel ve kurumsal olarak ayrılan poliçe sahibi, yedi branşta poliçe (etiketsiz plaka ve marka/model alanı olmadan), talep edilen ve ödenen tutarlar ile anomali türü taşıyan hasar, ve kartla veya havaleyle ödeme. Altta kırmızıyla iki belge tipi, hasar notu ve çağrı dökümü, her biri etiket dosyası üretiyor. Altta bir şerit sağlık sınırını belirtiyor](assets/readme/record-map.png)

<p align="center"><sub><a href="assets/readme/record-map.svg">Erişilebilir SVG kaynağını görüntüleyin</a></sub></p>

| Var | Yok |
| --- | --- |
| Altı kayıt tipi, ikisi serbest metin | Motor kodu. Tek Python `tests/` altında |
| Kurumsal poliçe sahipleri; vergi numaralarının alanda yaşadığı yer | Araç marka veya model alanı. Marka yasağı araç markalarını da kapsar |
| Poliçelerin yüzde onunda sağlık branşı | Her türlü klinik ayrıntı. Aşağıdaki sınıra bakın |
| Gerçek kurum listesine karşı taranan 26 uydurma sigortacı adı | Gerçek sigortacı. Geliştirme sırasında biri girdi ve şöyle yakalandı |

## Sağlık sınırı

Bu paket poliçe ve hasar düzeyinde bir `saglik` branşı içerir; çünkü sigorta
verisinde vardır ve aksini varsayan bir test ortamı temsili değildir.

Sağlık ifadeleri **kategori granülerliğinde** kalır: bir durum sınıfı ve fazlası
değil. Teşhis yok, klinik bulgu yok, tedavi yok, ilaç yok, prognoz yok. Bir
şablon, doğal okunmasını sağlayacak ayrıntı yasak olduğu için cılız hissettiriyorsa
o şablon cılızdır. Doğru sonuç budur.

Bu çizgiyi bir değil iki kontrol tutar:

- Her sağlık span'i çekirdeğin elle derlenmiş durum sınıfı betimleyicilerinden
  çekilir; bunlar o granülerlikte yazılmış ve elden geçirilmiştir.
- `lexicons/clinical_denied_tr.txt` bu paketin reddettiği kelime dağarcığını
  listeler ve bir test her işlenmiş belgeyi buna karşı tarar. İnceleme yorulur,
  liste yorulmaz; ve buradaki hata sessizdir, çünkü klinik ayrıntıya kayan bir
  şablon yine render olur, yine etiketler ve diğer her kontrolü yine geçer.

Sağlık sektör paketinin kendisi aile yol haritasında ertelenmiş durumdadır. Özel
nitelikli veri yoğunluğu, brief yazılmadan önce daha sıkı bir yönetişim incelemesi
ister. Bu paket o paket değildir ve her iki README de bunu söyler.

## Taksonominin bizim yerimize verdiği iki karar

İkisi de gözden kaçırma değil ve ikisi de okurun aksi hâlde hata sanacağı türden.

**Araç plakaları etiketsiz üretilir.** Sabitlenmiş taksonomide PLATE etiketi yok.
Bir plakayı ADDRESS diye etiketlemek bu paketin veri kümesinin kullanıldığı her
değerlendirmeyi bozardı; kapalı kümenin dışında bir etiket uydurmak ise tasarım
gereği kapalı biçimde reddedilir. Alan bu yüzden hiçbir etiket taşımaz ve bir test
hiçbir etiket dosyasındaki hiçbir span'in plakayı kapsamadığını doğrular. Sonraki
bir taksonomi sürümü etiketi eklerse bu paket onu majör bir yükseltmeyle alır.

**Araç markası veya modeli yoktur.** Ailenin marka yasağı araç markalarını kapsar,
dolayısıyla bir araç yalnızca yıl ve kasa tipiyle anlatılır. Markaya göre çalışan
bir fiyatlandırma motorunu test edecek biri için bu gerçek bir modelleme kaybıdır
ve veri alındıktan sonra keşfedilmek yerine burada söylenir.

## Kendiniz basın

```bash
uv tool install mintmark
git clone https://github.com/lokomotifai/mintmark-insurance
cd mintmark-insurance

mintmark packcheck .
mintmark mint --pack . --recipe portfolio-baseline --seed 20261001 --out ./run
mintmark verify ./run
```

Üretildiği hâliyle bir hasar notu:

```
Hasar dosyasi notu. Olay yeri Çınar Sokak olarak tespit edildi. Karsi
taraf Kemal Kılıç, iletisim +90 504 822 44 34. Sigortali 32493027203
numarali kisi, odeme icin TR919999905512934097477394 hesabini bildirdi.
Arac plakasi.
```

Bu, [`samples/claim_note.jsonl`](samples/claim_note.jsonl) içindeki ilk kayıttır;
README için yazılmış bir örnek değil. Bir test ikisini karşılaştırır.

## Değerlendirme kümesi

`pii-eval` her etiket için bir kapsam hedefi beyan eder ve on sekizini de
tutturur. Vergi numarası yükünü taşıyan şey kurumsal poliçe sahibi payıdır; bu,
bankacılık paketinden temel yapısal farktır: orada her kayıt tipi bireyseldir,
dolayısıyla VKN veriye belge şablonları üzerinden girmek zorundadır.

| Etiket grubu | Hedef | Ulaşılan |
| --- | --- | --- |
| PERSON, ADDRESS, ORG, DOB | her biri 300 | her biri 2000 |
| Sekiz özel nitelik | her biri 300 | 474 ilâ 519 |
| TCKN, VKN, IBAN, PAN, PHONE, EMAIL | her biri 500 | her biri 2000 |

Sekiz özel nitelikli etiketin her birinden 300 span, 2000 belgede 2400 enjeksiyon
demek; üstelik bu pakette bunları yayacak iki belge tipi var, bankacılıkta üç.
Değerlendirme şablonları bu yüzden bir oranıyla ayrı bir aile: belge başına iki
özel slot, etiketler eşit dağıtılmış.

## Üç tarif

| Tarif | Şekil | Ne için |
| --- | --- | --- |
| **portfolio-baseline** | 8 000 poliçe sahibi, yaklaşık 16 000 poliçe, 2 700 hasar, 40 000 ödeme ve 2 900 belge | Bir test ortamını portföy gibi davranan bir şeyle doldurmak |
| **pii-eval** | 2 000 belge, her etiket hedefinin üzerinde | Bir dedektörü Türkçe sigorta metninde ölçmek |
| **anomaly-mix** | Taban artı her hasarda etiketli bir anomali alanı | Bir izleme sistemini gerçek referansa karşı puanlamak |

### anomaly-mix'in açıkça belirtilen bir sınırı

Her hasar `anomaly_kind` ve `is_anomaly` taşır ve ikisi hiç çelişmez. Ancak dört
tür, **beyan edilen oranlarda çekilmiş satır bazlı etiketlerdir; gerçek zamansal
veya kayıtlar arası yapılar değil**. Gerçek bir mükerrer talep örüntüsü tek bir
poliçedeki birkaç hasara yayılır; burada bir etikettir.

Bu bir gözden kaçırma değil, paket sözleşmesinin sınırıdır: her alan bağımsız bir
akıştan çekilir, dolayısıyla bir paket satırları ilişkilendiren bir örüntü beyan
edemez. Bu tarifi hattınızın etiketleri doğru taşıdığını denetlemek için kullanın.
Bir dedektörün gerçek örüntüleri bulup bulmadığını ölçmek için kullanmayın.

## Kurgusal listeye giren gerçek bir sigortacı

Anlatmaya değer, çünkü denylist'in gerekçesi bu; onun hakkında bir varsayım değil.

Çekirdeğin denylist'i ödeme sistemleri katılımcı sicilinden kurulur ve orada
bankalar vardır. Bir sigortacıyla çakışmayı yakalayamaz ve bu paketin kurgusal
sözlüğünde biri duruyordu: **Bereket Sigorta, 1995 kuruluşlu gerçek bir şirket**.
Oraya "bereket" sıradan bir Türkçe kelime olduğu için girdi.

Kök, iki pakette üç sözlükte ve çekirdeğin kendi kurum betimleyicilerinde çıktı.
Hepsi düzeltildi, bu paket artık bankaları ve sigortacıları kapsayan 110 girişlik
bir denylist uzantısı taşıyor ve tüm aile buna karşı yeniden tarandı.

O doğrulamanın bir sınırı da söylenmeye değer: Türkiye Sigorta Birliği
otoritatif üye listesini yayımlar ve sayfası istemci tarafında render edildiği
için burada kullanılan liste 40 şirketlik kamusal bir derlemedir. Bu, gerçek bir
çakışmayı yakalamaya yetti. Hiç olmadığını kanıtlamaya yetmez ve birliğin kendi
sayfasının elle okunması sürüm kontrol listesine aittir. Tam kayıt
[docs/normative-verification.md](docs/normative-verification.md) içinde.

## Depo haritası

```
pack.yaml           kimlik, çekirdek pini, izin verilen tanımlayıcı politikaları
fields/             üretim sırasına göre kayıt tipi başına bir dosya
recipes/            portfolio-baseline, pii-eval, anomaly-mix
templates/          taban setleri ve ayrı değerlendirme setleri
lexicons/           uydurma sigortacılar ve acenteler, denylist, bu paketin
                    reddettiği klinik kelime dağarcığı
samples/            tip başına elli kayıt, sabit tohumdan yeniden üretilir
vendor/             zorunlu CI'ın karşı koştuğu çekirdek wheel, özetiyle kayıtlı
tests/              uygunluk paketi, sağlık sınırı kontrolü dahil
docs/               referans veri kümesi kaydı ve doğrulama kaydı
```

## Depoyu geliştirin

```bash
uv sync
uv run mintmark packcheck .
uv run pytest
uv run python tools/mdlint.py .
```

Hepsi vendor'lanmış çekirdek wheel'ine karşı çevrimdışı çalışır.

## Proje durumu

Sürüm 0.1, ön yayın. Sürüm yok, yayımlanmış veri kümesi yok. Referans veri
kümeleri yerleşik tohumlarıyla
[docs/reference-datasets.json](docs/reference-datasets.json) içinde beyan
edilmiştir; bunları yayımlamak, veri seti lisansını teyit etmekle birlikte bir dış
yetki kapısıdır.

## Topluluk sözleşmesi

Katkılar, katkı lisans sözleşmesi olmaksızın Developer Certificate of Origin 1.1
kapsamında. Bakınız [CONTRIBUTING.md](CONTRIBUTING.md),
[GOVERNANCE.md](GOVERNANCE.md) ve [SECURITY.md](SECURITY.md).

[README.md](README.md) kanoniktir ve bu belge tam bir aynadır.

## Lisans ve marka

Apache-2.0. Bakınız [LICENSE](LICENSE) ve [NOTICE](NOTICE). Lisans, Mintmark adı
veya logosu üzerinde hiçbir hak vermez; bakınız [TRADEMARKS.md](TRADEMARKS.md).

Yayımlanan referans veri kümeleri için veri seti lisansı CC0-1.0 olarak
önerilmiştir ve hukuk teyidi beklemektedir.

<p align="center"><sub>Mintmark ailesinin parçası: <a href="https://github.com/lokomotifai/mintmark">çekirdek</a> · <a href="https://github.com/lokomotifai/mintmark-banking">bankacılık</a> · <a href="https://github.com/lokomotifai/mintmark-hr">insan kaynakları</a></sub></p>
