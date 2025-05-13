import os
import fitz  # PyMuPDF
import docx
from concurrent.futures import ThreadPoolExecutor

class DocumentPreprocessor:
    """
    Belge ön işleme sınıfı.
    - PDF, DOCX, TXT dosyalarını okur ve temizlenmiş metin döndürür.
    """

    SUPPORTED_FORMATS = ('.pdf', '.txt', '.docx')

    def __init__(self, input_folder='data/raw', output_folder='data/processed'):
        self.input_folder = input_folder
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def _read_pdf(self, file_path):
        """PDF belgesini okur ve metni çıkarır."""
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            print(f"❌ PDF okunurken hata oluştu: {file_path} - Hata: {e}")
        return text

    def _read_txt(self, file_path):
        """TXT belgesini okur ve metni çıkarır."""
        text = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ TXT okunurken hata oluştu: {file_path} - Hata: {e}")
        return text

    def _read_docx(self, file_path):
        """DOCX belgesini okur ve metni çıkarır."""
        text = ""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"❌ DOCX okunurken hata oluştu: {file_path} - Hata: {e}")
        return text

    def _save_processed_text(self, filename, content):
        """İşlenmiş metni çıktılar klasörüne kaydeder."""
        output_path = os.path.join(self.output_folder, filename)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ İşlenmiş belge kaydedildi: {output_path}")
        except Exception as e:
            print(f"❌ Metin kaydedilemedi: {output_path} - Hata: {e}")

    def process_documents(self):
        """Belgeleri işler ve çıktı klasörüne kaydeder."""
        files = [f for f in os.listdir(self.input_folder) if f.endswith(self.SUPPORTED_FORMATS)]
        if not files:
            print("⚠️ İşlenecek belge bulunamadı.")
            return

        with ThreadPoolExecutor(max_workers=5) as executor:
            for file in files:
                file_path = os.path.join(self.input_folder, file)
                if file.endswith('.pdf'):
                    content = executor.submit(self._read_pdf, file_path).result()
                elif file.endswith('.txt'):
                    content = executor.submit(self._read_txt, file_path).result()
                elif file.endswith('.docx'):
                    content = executor.submit(self._read_docx, file_path).result()
                
                if content:
                    self._save_processed_text(f"{file}.processed.txt", content)

# Kullanım
if __name__ == "__main__":
    processor = DocumentPreprocessor()
    processor.process_documents()
