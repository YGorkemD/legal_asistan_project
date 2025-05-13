import pytest
from src.preprocess import DocumentPreprocessor
from src.vectorizer import DocumentVectorizer
from src.retriever import DocumentRetriever
from src.generator import AnswerGenerator

def test_end_to_end_workflow(tmpdir):
    """
    Uçtan uca:
    1. Belge İşleme
    2. Vektörleştirme
    3. Arama
    4. Yanıt Üretme
    """
    # 1️⃣ Preprocess
    txt_file = tmpdir.join("test_document.txt")
    txt_file.write("Bu belge, hukuki süreçleri açıklamaktadır.")
    
    processor = DocumentPreprocessor(input_folder=tmpdir, output_folder="data/processed")
    processor.process_documents()
    
    processed_path = "data/processed/test_document.txt.processed.txt"
    assert os.path.exists(processed_path)

    # 2️⃣ Vectorize
    vectorizer = DocumentVectorizer(vector_store='faiss')
    vectorizer.add_document("test_document", "Bu belge, hukuki süreçleri açıklamaktadır.")

    # 3️⃣ Retrieve
    retriever = DocumentRetriever(vector_store='faiss')
    results = retriever.retrieve("hukuki süreç")
    assert len(results) > 0
    assert results[0][0] == "test_document"

    # 4️⃣ Generate Answer
    mocker = pytest.importorskip("pytest_mock")
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: {
        "response": "Hukuki süreçler mahkemelerde yürütülür."
    }))
    
    generator = AnswerGenerator()
    response = generator.generate_answer("Hukuki süreç nedir?", results)
    assert response == "Hukuki süreçler mahkemelerde yürütülür."
