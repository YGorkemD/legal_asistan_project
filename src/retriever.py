import os
from vectorizer import DocumentVectorizer

class DocumentRetriever:
    """
    Belge getirici sınıf.
    - FAISS veya Chroma'dan en yakın belgeleri getirir.
    - İşlenmiş metinleri okur ve yanıt üretimi için hazır hale getirir.
    """
    
    def __init__(self, vector_store='faiss', top_k=5, processed_folder='data/processed'):
        """
        :param vector_store: "faiss" veya "chroma"
        :param top_k: En yakın kaç sonuç getirileceği
        :param processed_folder: İşlenmiş belgelerin tutulduğu klasör
        """
        self.vectorizer = DocumentVectorizer(vector_store=vector_store)
        self.top_k = top_k
        self.processed_folder = processed_folder

    def _load_document_content(self, doc_id):
        """İşlenmiş belgeyi dosyadan okur."""
        file_path = os.path.join(self.processed_folder, f"{doc_id}.processed.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"❌ Belge bulunamadı: {file_path}")
            return None

    def retrieve(self, query):
        """
        Kullanıcı sorgusuna en yakın belgeleri getirir.
        :param query: Kullanıcının sorgusu
        :return: [(doc_id, content, score), ...]
        """
        results = self.vectorizer.search(query, top_k=self.top_k)
        retrieved_docs = []

        for doc_id, score in results:
            content = self._load_document_content(doc_id)
            if content:
                retrieved_docs.append((doc_id, content, score))

        print(f"🔍 {len(retrieved_docs)} belge bulundu.")
        return retrieved_docs


# Kullanım
if __name__ == "__main__":
    retriever = DocumentRetriever(vector_store='faiss', top_k=3)
    results = retriever.retrieve("hukuki süreç nedir?")
    
    for doc_id, content, score in results:
        print(f"\n📄 Belge ID: {doc_id}")
        print(f"🔍 Alaka Skoru: {score}")
        print(f"📝 İçerik (Özet): {content[:200]}...\n")
