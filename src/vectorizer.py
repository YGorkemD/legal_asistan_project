import os
import faiss
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

class DocumentVectorizer:
    """
    Belge vektörleştirme sınıfı.
    - FAISS ve Chroma desteği içerir.
    - İlgili yapılandırmalara göre doğru depolama mekanizmasını seçer.
    """

    def __init__(self, vector_store='faiss', model_name='all-mpnet-base-v2'):
        """
        :param vector_store: "faiss" veya "chroma" seçeneği (default: faiss)
        :param model_name: SentenceTransformer model ismi
        """
        self.vector_store = vector_store
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        if vector_store == 'faiss':
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.doc_map = {}  # Vektör ID -> Doküman Adı Eşleşmesi
            print("✅ FAISS vektör deposu başlatıldı.")
        
        elif vector_store == 'chroma':
            self.client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                                   persist_directory="models/embeddings"))
            self.collection = self.client.get_or_create_collection(name="documents")
            print("✅ ChromaDB vektör deposu başlatıldı.")

        else:
            raise ValueError("❌ Geçersiz vector_store seçimi. Sadece 'faiss' veya 'chroma' kullanılabilir.")

    def _embed_text(self, text):
        """Metni vektör haline getirir."""
        return self.model.encode(text)

    def add_document(self, doc_id, content):
        """Belgeyi vektörleştirip seçilen depoya ekler."""
        vector = self._embed_text(content)

        if self.vector_store == 'faiss':
            self.index.add(np.array([vector]))
            self.doc_map[len(self.doc_map)] = doc_id
            print(f"✅ Belge FAISS deposuna eklendi: {doc_id}")

        elif self.vector_store == 'chroma':
            self.collection.add(
                embeddings=[vector.tolist()],
                ids=[doc_id],
                documents=[content]
            )
            print(f"✅ Belge ChromaDB deposuna eklendi: {doc_id}")

    def search(self, query, top_k=5):
        """Sorgu vektörünü arar ve en yakın `top_k` sonuçları döndürür."""
        query_vector = self._embed_text(query)

        if self.vector_store == 'faiss':
            distances, indices = self.index.search(np.array([query_vector]), top_k)
            results = [(self.doc_map[i], d) for i, d in zip(indices[0], distances[0])]
            print(f"🔍 FAISS sonuçları: {results}")
            return results

        elif self.vector_store == 'chroma':
            results = self.collection.query(
                query_embeddings=[query_vector.tolist()],
                n_results=top_k
            )
            matches = list(zip(results["ids"], results["distances"]))
            print(f"🔍 ChromaDB sonuçları: {matches}")
            return matches

    def persist(self):
        """FAISS veya Chroma deposunu kaydeder."""
        if self.vector_store == 'faiss':
            faiss.write_index(self.index, "models/embeddings/faiss_index.bin")
            with open("models/embeddings/faiss_map.txt", 'w') as f:
                for idx, doc_id in self.doc_map.items():
                    f.write(f"{idx},{doc_id}\n")
            print("💾 FAISS deposu kaydedildi.")

        elif self.vector_store == 'chroma':
            print("💾 ChromaDB deposu zaten anlık olarak kaydediliyor.")

    def load(self):
        """FAISS veya Chroma deposunu yükler."""
        if self.vector_store == 'faiss':
            self.index = faiss.read_index("models/embeddings/faiss_index.bin")
            with open("models/embeddings/faiss_map.txt", 'r') as f:
                for line in f:
                    idx, doc_id = line.strip().split(',')
                    self.doc_map[int(idx)] = doc_id
            print("✅ FAISS deposu yüklendi.")

        elif self.vector_store == 'chroma':
            print("✅ ChromaDB deposu anlık yükleniyor, manuel yükleme gerekmez.")

# Kullanım
if __name__ == "__main__":
    # FAISS kullanalım
    vectorizer = DocumentVectorizer(vector_store='faiss')
    vectorizer.add_document("document_1", "Bu bir test dokümanıdır.")
    vectorizer.add_document("document_2", "Yapay zeka ve hukuk alanında yenilikler.")
    vectorizer.search("hukuk yenilikleri")
    vectorizer.persist()
