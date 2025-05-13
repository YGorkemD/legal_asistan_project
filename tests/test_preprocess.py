import os
import pytest
from src.preprocess import DocumentPreprocessor

@pytest.fixture
def setup_files(tmpdir):
    """Geçici dosyalar oluşturur."""
    pdf_path = tmpdir.join("test_document.pdf")
    txt_path = tmpdir.join("test_document.txt")
    docx_path = tmpdir.join("test_document.docx")

    with open(txt_path, "w") as f:
        f.write("Bu bir test dökümanıdır.")

    return str(txt_path)

def test_txt_preprocessing(setup_files):
    """TXT dosyası işlenmeli ve çıktı klasörüne kaydedilmeli."""
    processor = DocumentPreprocessor(input_folder=os.path.dirname(setup_files),
                                     output_folder="data/processed")
    processor.process_documents()

    processed_path = os.path.join("data/processed", "test_document.txt.processed.txt")
    assert os.path.exists(processed_path)
    with open(processed_path, "r", encoding='utf-8') as f:
        content = f.read()
    assert "Bu bir test dökümanıdır." in content
