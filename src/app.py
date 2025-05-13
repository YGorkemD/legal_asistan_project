import streamlit as st
from preprocess import DocumentPreprocessor
from vectorizer import DocumentVectorizer
from retriever import DocumentRetriever
from generator import AnswerGenerator

# Başlık ve açıklama
st.set_page_config(page_title="Legal Assistant with RAG", layout="wide")
st.title("🗂️ Legal Assistant with RAG")
st.write("Türkçe yasal belgelerden hızlı ve doğru yanıtlar alın.")

# Yüklenen dosyalar
uploaded_files = st.file_uploader(
    "Lütfen yasal belgelerinizi yükleyin (PDF, DOCX, TXT desteklenir):",
    accept_multiple_files=True
)

# Depo Seçimi
vector_store = st.radio(
    "Vektör Deposu Seçin:",
    ('faiss', 'chroma')
)

# Belgeleri kaydetme ve işleme
if st.button("📌 Belgeleri İşle"):
    if uploaded_files:
        processor = DocumentPreprocessor()
        for file in uploaded_files:
            file_path = f"data/raw/{file.name}"
            with open(file_path, "wb") as f:
                f.write(file.read())
            st.success(f"{file.name} yüklendi ve kaydedildi.")

        # İşlenmiş belgeler
        processor.process_documents()
        st.success("Belgeler başarıyla işlendi.")
    else:
        st.error("Lütfen en az bir belge yükleyin.")

# Sorgu girişi
query = st.text_input("Sormak istediğiniz soruyu girin:")

# Arama butonu
if st.button("🔎 Ara"):
    if query:
        retriever = DocumentRetriever(vector_store=vector_store, top_k=3)
        results = retriever.retrieve(query)

        if results:
            st.subheader("📌 İlgili Belgeler:")
            for idx, (doc_id, content, score) in enumerate(results):
                st.write(f"**{idx + 1}. Belge ID:** {doc_id}")
                st.write(f"**Alaka Skoru:** {score:.2f}")
                st.text_area(f"Belge İçeriği - {doc_id}", content, height=150)
            
            # Yanıt üretimi
            generator = AnswerGenerator()
            st.subheader("💡 Üretilen Yanıt:")
            answer = generator.generate_answer(query, results)
            st.write(answer)
        else:
            st.warning("Uygun bir belge bulunamadı.")
    else:
        st.error("Lütfen bir sorgu girin.")

# Özetleme butonu
st.subheader("📄 Belge Özeti:")
if st.button("📝 Seçili Belgeyi Özetle"):
    selected_doc = st.selectbox("Özetlemek istediğiniz belgeyi seçin:", [f.name for f in uploaded_files])
    if selected_doc:
        file_path = f"data/processed/{selected_doc}.processed.txt"
        if not file_path.endswith(".processed.txt"):
            file_path += ".processed.txt"
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            generator = AnswerGenerator()
            summary = generator.summarize_document(content)
            st.write("📌 **Belge Özeti:**")
            st.write(summary)
        else:
            st.error("Seçili belge bulunamadı veya işlenemedi.")
    else:
        st.error("Lütfen bir belge seçin.")
