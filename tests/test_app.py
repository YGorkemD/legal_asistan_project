import pytest
import streamlit as st
from src.preprocess import DocumentPreprocessor
from src.vectorizer import DocumentVectorizer
from src.retriever import DocumentRetriever
from src.generator import AnswerGenerator
import os

@pytest.fixture
def sample_text_document(tmpdir):
    """Geçici bir metin dosyası oluşturur ve test klasörüne kaydeder."""
    txt_file = tmpdir.join("test_document.txt")
    txt_file.write("Bu bir test dokümanıdır. Hukuki süreçler burada açıklanır.")
    return str(txt_file)

def test_document_preprocessing(sample_text_document):
    """TXT dosyası işlenmeli ve çıktı klasörüne kaydedilmeli."""
    processor = DocumentPreprocessor(input_folder=os.path.dirname(sample_text_document),
                                     output_folder="data/processed")
    processor.process_documents()
    
    processed_path = "data/processed/test_document.txt.processed.txt"
    assert os.path.exists(processed_path)

def test_document_retrieval():
    """Doğru belgelerin arama ile getirilmesi kontrol edilir."""
    retriever = DocumentRetriever(vector_store='faiss', top_k=3)
    results = retriever.retrieve("hukuki süreç")
    assert len(results) > 0

def test_answer_generation(mocker):
    """Groq LLM yanıt üretimi testi."""
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: {
        "response": "Hukuki süreçler mahkemelerde yürütülür."
    }))
    generator = AnswerGenerator()
    response = generator.generate_answer("Hukuki süreç nedir?", [("doc_1", "İçerik", 0.9)])
    assert response == "Hukuki süreçler mahkemelerde yürütülür."
