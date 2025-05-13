import os
import requests
import yaml
from dotenv import load_dotenv

load_dotenv()

class AnswerGenerator:
    """
    Soru-cevap üreticisi.
    - Groq-hosted LLM ile yanıt üretir.
    - İlgili belgelerden alınan içeriklerle birlikte daha anlamlı sonuçlar sağlar.
    """

    def __init__(self):
        self.api_url = os.getenv("GROQ_API_URL")
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_url or not self.api_key:
            raise ValueError("❌ API ayarları bulunamadı. Lütfen .env dosyasını kontrol edin.")

        print("✅ Groq-hosted LLM bağlantısı sağlandı.")

    def _prepare_prompt(self, query, documents):
        """
        LLM'ye gönderilecek prompt'u hazırlar.
        :param query: Kullanıcı sorgusu
        :param documents: [(doc_id, content, score), ...]
        :return: Hazırlanmış prompt
        """
        document_contexts = "\n\n".join([f"Kaynak: {doc_id}\n\n{content[:500]}..." for doc_id, content, _ in documents])
        prompt = f"""
        Soru: {query}
        Aşağıda ilgili belgelerden alınmış içerikler bulunmaktadır:
        
        {document_contexts}
        
        Lütfen yukarıdaki bilgiler ışığında, soruya net, doğru ve Türkçe bir yanıt ver.
        Eğer cevap belgelerde açıkça yer almıyorsa, tahmin yürütmeden "Belge içerisinde bu bilgiye ulaşılamadı." de.
        """

        return prompt

    def generate_answer(self, query, documents):
        """
        LLM'den yanıt üretir.
        :param query: Kullanıcı sorgusu
        :param documents: İlgili belgeler
        :return: Yanıt metni
        """
        prompt = self._prepare_prompt(query, documents)
        
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt, "max_tokens": 300}
            )
            response.raise_for_status()
            result = response.json()
            print("✅ Yanıt başarıyla alındı.")
            return result.get("response", "Yanıt alınamadı.")
        
        except requests.RequestException as e:
            print(f"❌ API isteği sırasında hata oluştu: {e}")
            return "API isteği sırasında bir hata oluştu."

    def summarize_document(self, content):
        """
        Belgeyi özetler.
        :param content: Özetlenecek belge içeriği
        :return: Özet metni
        """
        prompt = f"""
        Aşağıda verilen belgeyi özetle:
        
        {content[:1000]}...
        
        Özet:
        """

        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt, "max_tokens": 200}
            )
            response.raise_for_status()
            result = response.json()
            print("✅ Özet başarıyla alındı.")
            return result.get("response", "Özet alınamadı.")
        
        except requests.RequestException as e:
            print(f"❌ API isteği sırasında hata oluştu: {e}")
            return "API isteği sırasında bir hata oluştu."
    

# Kullanım
if __name__ == "__main__":
    generator = AnswerGenerator()
    documents = [
        ("document_1", "Hukuki süreç, mahkeme aşamalarını ve dava sürecini kapsar.", 0.8),
        ("document_2", "Adalet sistemi, toplumun güvenini sağlamak amacıyla oluşturulmuştur.", 0.7)
    ]

    yanit = generator.generate_answer("Hukuki süreç nedir?", documents)
    print("\n📝 Üretilen Yanıt:\n", yanit)
    
    ozet = generator.summarize_document("Adalet sistemi, toplumun güvenini sağlamak amacıyla oluşturulmuştur.")
    print("\n📌 Belge Özeti:\n", ozet)
