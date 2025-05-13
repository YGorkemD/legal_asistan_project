import pytest
from src.retriever import DocumentRetriever

@pytest.fixture
def sample_documents():
    return [
        ("document_1", "Hukuki süreçler mahkemelerde yürütülür.", 0.85),
        ("document_2", "Dava süreçleri kanunlarla belirlenmiştir.", 0.78)
    ]

def test_document_retrieval(sample_documents):
    """Belge getirici doğru şekilde sonuç döndürmeli."""
    retriever = DocumentRetriever(vector_store='faiss')
    results = retriever.retrieve("hukuki süreçler")
    
    assert len(results) > 0
    assert "document_1" in [doc[0] for doc in results]
