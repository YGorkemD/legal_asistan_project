import pytest
from src.vectorizer import DocumentVectorizer

@pytest.fixture
def sample_document():
    return "Bu bir test belgesidir. Hukuki süreçler hakkında bilgiler içerir."

def test_faiss_vectorizer(sample_document):
    """FAISS vektörleştirici doğru şekilde çalışmalı."""
    vectorizer = DocumentVectorizer(vector_store='faiss')
    vectorizer.add_document("test_doc", sample_document)
    
    results = vectorizer.search("hukuki süreçler")
    assert len(results) > 0
    assert results[0][0] == "test_doc"

def test_chroma_vectorizer(sample_document):
    """ChromaDB vektörleştirici doğru şekilde çalışmalı."""
    vectorizer = DocumentVectorizer(vector_store='chroma')
    vectorizer.add_document("test_doc", sample_document)
    
    results = vectorizer.search("hukuki süreçler")
    assert len(results) > 0
    assert results[0][0] == "test_doc"
