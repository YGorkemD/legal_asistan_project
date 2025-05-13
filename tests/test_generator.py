import pytest
from src.generator import AnswerGenerator

@pytest.fixture
def sample_documents():
    return [
        ("document_1", "Hukuki süreçler mahkemelerde yürütülür.", 0.85),
        ("document_2", "Dava süreçleri kanunlarla belirlenmiştir.", 0.78)
    ]

def test_generate_answer(sample_documents, mocker):
    """Groq LLM yanıt üretimi testi."""
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: {
        "response": "Hukuki süreçler mahkemelerde yürütülür."
    }))

    generator = AnswerGenerator()
    answer = generator.generate_answer("Hukuki süreçler nedir?", sample_documents)
    assert answer == "Hukuki süreçler mahkemelerde yürütülür."
