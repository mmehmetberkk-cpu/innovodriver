# Araç Kontrol Formu - Bulut Versiyonu

Streamlit tabanlı araç kontrol formu uygulaması. Bulut ortamında çalışacak şekilde optimize edilmiştir.

## 🚀 Özellikler

- ✅ **Bulut Uyumlu**: Streamlit Cloud, Heroku, Docker ve diğer bulut platformlarında çalışır
- ✅ **Google Sheets Entegrasyonu**: Kalıcı veri depolama için Google Sheets desteği
- ✅ **Kullanıcı Yönetimi**: Kullanıcı girişi ve admin paneli
- ✅ **Form Yönetimi**: Araç kontrol formları oluşturma ve görüntüleme
- ✅ **Excel Fallback**: Google Sheets kullanılamazsa Excel dosyalarına fallback

## 📋 Gereksinimler

- Python 3.9+
- Streamlit
- Google Sheets API (opsiyonel, kalıcı veri için önerilir)

## 🛠️ Kurulum

### Yerel Geliştirme

1. Repository'yi klonlayın:
```bash
git clone <repository-url>
cd driver_v1.1.0
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Secrets yapılandırması:
   - `.streamlit/secrets.toml.example` dosyasını `.streamlit/secrets.toml` olarak kopyalayın
   - Google Sheets bilgilerinizi ekleyin (opsiyonel)

4. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

### Bulut Deployment

Detaylı deployment rehberi için `DEPLOYMENT.md` dosyasına bakın.

**Hızlı Başlangıç (Streamlit Cloud):**

1. GitHub'a push edin
2. [Streamlit Cloud](https://share.streamlit.io/)'a gidin
3. Repository'nizi seçin ve deploy edin
4. Settings > Secrets'tan Google Sheets bilgilerinizi ekleyin
5. `GOOGLE_SHEETS_SETUP.md` dosyasındaki adımları takip edin

## 📁 Proje Yapısı

```
driver_v1.1.0/
├── app.py                      # Ana Streamlit uygulaması
├── excel_handler.py            # Veri işleme modülü (Google Sheets + Excel)
├── requirements.txt            # Python bağımlılıkları
├── .streamlit/
│   ├── config.toml             # Streamlit yapılandırması
│   └── secrets.toml.example     # Secrets örneği
├── DEPLOYMENT.md               # Deployment rehberi
├── GOOGLE_SHEETS_SETUP.md      # Google Sheets kurulum rehberi
└── README.md                   # Bu dosya
```

## 🔐 Secrets Yapılandırması

### Streamlit Cloud Secrets Formatı

```toml
USE_GOOGLE_SHEETS = "true"
GOOGLE_SHEET_ID = "your_sheet_id_here"
GOOGLE_CREDENTIALS_JSON = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
'''
```

### Alternatif: Nested Format

```toml
[google_sheets]
enabled = "true"
sheet_id = "your_sheet_id_here"
credentials_json = '''
{
  "type": "service_account",
  ...
}
'''
```

## 📊 Google Sheets Yapısı

Uygulama aşağıdaki sheet'leri bekler:

- **Vehicles**: Araç listesi
- **FuelLevels**: Yakıt seviyeleri
- **ExteriorChecks**: Dış kontroller
- **EngineChecks**: Motor kontrolleri
- **SafetyEquipment**: Güvenlik ekipmanları
- **InteriorChecks**: İç kontroller
- **Items**: Araç içi eşyalar
- **Users**: Kullanıcı bilgileri
- **Submissions**: Form gönderimleri

Detaylı kurulum için `GOOGLE_SHEETS_SETUP.md` dosyasına bakın.

## 🔄 Veri Depolama

### Google Sheets (Önerilen)

- ✅ Kalıcı veri depolama
- ✅ Bulut ortamında çalışır
- ✅ Gerçek zamanlı senkronizasyon
- ✅ Kolay veri yönetimi

### Excel Fallback

- ⚠️ Geçici dosya sistemi kullanır
- ⚠️ Bulut ortamında veriler kaybolabilir
- ✅ Yerel geliştirme için uygun

## 🐛 Sorun Giderme

### Google Sheets Bağlantı Hatası

1. Service account email'ine Google Sheets'te erişim verdiğinizden emin olun
2. `GOOGLE_SHEET_ID`'nin doğru olduğundan emin olun
3. `GOOGLE_CREDENTIALS_JSON` formatının doğru olduğundan emin olun (\\n karakterleri önemli)

### Veri Kaybolması

- Google Sheets kullanıyorsanız veriler kalıcıdır
- Excel fallback kullanıyorsanız, bulut ortamında dosyalar geçicidir
- Her zaman Google Sheets kullanmanız önerilir

### Login Sorunları

- `Users` sheet'inin Google Sheets'te mevcut olduğundan emin olun
- Kullanıcı bilgilerinin doğru formatta olduğundan emin olun

## 📝 Lisans

Bu proje özel kullanım içindir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add some amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu uygulama bulut ortamında çalışacak şekilde optimize edilmiştir. Yerel dosya yolları kaldırılmış ve Google Sheets entegrasyonu eklenmiştir.

