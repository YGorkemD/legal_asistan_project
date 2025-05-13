### 📌 **README.md - Legal Assistant with RAG**

---

# 🗂️ Legal Assistant with RAG (Retrieval-Augmented Generation)

Türkçe yasal belgeler üzerinden soru-cevap işlemi yapan, Groq-hosted LLM destekli bir "Legal Assistant" uygulaması. Uygulama, yüklenen PDF, DOCX ve TXT formatındaki yasal belgeleri vektörleştirip, doğal dil sorgularına doğru yanıtlar üretebilir.

---

## 📌 **Proje Mimarisi**

```
legal_assistant_project/
│
├── data/                          # Yüklenen yasal belgeler
│   ├── raw/                       # Ham belgeler
│   └── processed/                 # İşlenmiş ve tokenize edilmiş belgeler
│
├── models/                        # LLM ve FAISS/Chroma modelleri
│   ├── embeddings/                # Vektör dosyaları
│   └── checkpoints/               # LLM kontrol noktaları
│
├── src/                           # Ana kaynak kodları
│   ├── preprocess.py              # Veri ön işleme (PDF, DOCX, TXT okuma ve temizleme)
│   ├── vectorizer.py              # FAISS veya Chroma ile vektörleştirme
│   ├── retriever.py               # İlgili dokümanları getiren sorgu işlemi
│   ├── generator.py               # Groq-hosted LLM ile yanıt üretme
│   ├── app.py                     # Streamlit arayüzü
│   └── utils.py                   # Yardımcı fonksiyonlar
│
├── configs/                       # Konfigürasyon dosyaları
│   ├── app_config.yaml            # Uygulama genel ayarları
│   └── model_config.yaml          # Model ve vektör ayarları
│
├── logs/                          # Uygulama log dosyaları
│   └── app.log                    # Ana log kaydı
│
├── tests/                         # Birim testler ve entegrasyon testleri
│   ├── test_preprocess.py
│   ├── test_vectorizer.py
│   ├── test_retriever.py
│   ├── test_generator.py
│   ├── test_app.py
│   └── test_end_to_end.py
│
├── Dockerfile                     # Docker yapılandırması
├── requirements.txt               # Gerekli Python paketleri
├── README.md                      # Proje açıklamaları ve kullanım kılavuzu
├── .env                           # Ortam değişkenleri (API anahtarları vb.)
└── .dockerignore                  # Docker'da kopyalanmayacak dosyalar
```

---

## 🚀 **Kurulum Adımları**

### 1️⃣ Gerekli Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

### 2️⃣ `.env` Dosyası Oluşturma

`.env` dosyası ana dizinde bulunmalı ve içeriği şu şekilde olmalı:

```env
GROQ_API_URL=https://console.groq.com/api/v1/generate
GROQ_API_KEY=your_api_key_here
```

### 3️⃣ Docker Build ve Run

```bash
# Docker image oluştur
docker build -t legal-assistant-rag .

# Docker container başlat
docker run -d -p 8501:8501 --name legal-assistant legal-assistant-rag
```

### 4️⃣ Uygulamayı Aç

[http://localhost:8501](http://localhost:8501) adresine giderek arayüzü görebilirsiniz.

---

## 🔎 **Uygulama Özellikleri**

* **Belge Yükleme:** PDF, DOCX, TXT formatındaki yasal belgeler yüklenebilir.
* **Vektörleştirme:** FAISS veya Chroma tabanlı arama desteği.
* **Sorgu Cevaplama:** Doğal dilde sorulan sorulara yanıt üretir.
* **Özetleme:** Seçilen belge, Groq-hosted LLM ile özetlenir.
* **Kaynak Belge Gösterimi:** Yanıt üretilirken kullanılan belgeler referans olarak gösterilir.

---

## 🧪 **Testler**

Tüm testleri çalıştırmak için:

```bash
pytest tests/ --disable-warnings
```

**Testler:**

* `test_preprocess.py`: PDF, DOCX, TXT dosyalarının doğru şekilde işlenmesi.
* `test_vectorizer.py`: FAISS ve Chroma üzerinden doğru vektörleştirme.
* `test_retriever.py`: Doğru belgelerin getirilmesi.
* `test_generator.py`: Groq-hosted LLM'den yanıt üretilmesi.
* `test_app.py`: Arayüz işlemlerinin testi.
* `test_end_to_end.py`: Uçtan uca tam entegrasyon testi.

---

## 📌 **API Bağlantısı**

Groq-hosted LLM, doğal dil işlemlerini yapmak için kullanılır. İstekler, `generator.py` dosyası aracılığıyla yapılır. Yanıtlar doğrudan arayüze yansıtılır.

---

## 📄 **Yapılandırma Dosyaları**

1. **app\_config.yaml**: Uygulama genel ayarları (Başlık, açıklama, vektör depolama seçimi, top\_k ayarı).
2. **model\_config.yaml**: Model konfigürasyonları (Embedding modeli, FAISS yolu, Chroma dizini).

---

## 🚀 **Konteyner Yönetimi**

* **Container Durdur:**

  ```bash
  docker stop legal-assistant
  ```
* **Container Başlat:**

  ```bash
  docker start legal-assistant
  ```
* **Logları İncele:**

  ```bash
  docker logs legal-assistant
  ```

---

## 💡 **Geliştirici Notları**

* Groq-hosted API anahtarı geçersizse, yanıt alınamayacaktır.
* FAISS ve Chroma bağımsız çalışabilir, tercihe göre değiştirebilirsiniz.
* İşlenmiş belgeler `data/processed` altında `.processed.txt` formatında tutulur.

---

## 📌 **Katkıda Bulunma**

Her türlü katkıya açığız. Lütfen bir **pull request** açın veya bir **issue** oluşturun.

---

## 📄 **Lisans**

MIT Lisansı altında lisanslanmıştır.


