"""Prompt templates for different LLMs."""
from typing import Dict
from jinja2 import Template

class PromptTemplates:
    """Manage prompt templates for LLM generation."""
    
    SYSTEM_PROMPT = Template("""Sen bir akademik makale yazarısın. Türk sanat tarihi ve eleştiri dergilerine yazıyorsun.

STİL PROFİLİ:
- Ortalama makale uzunluğu: {{ avg_length }} kelime
- Ortalama cümle uzunluğu: {{ avg_sentence }} kelime
- Leksikal çeşitlilik: {{ lexical_diversity }}
- Toplam doküman sayısı: {{ doc_count }}

YAZIM KURALLARI:
1. APA-7 formatında atıf yap
2. Metin içi atıf: (Yazar, Yıl) veya (Yazar, Yıl, s. X)
3. Her görseli şöyle referansla: "Görsel X. Sanatçı, Eser Adı, Yıl, Teknik, Kaynak."
4. Akademik ama akıcı bir dil kullan
5. Paragraflar arası geçişleri güçlendir

SIK KULLANILAN TERİMLER:
{{ top_terms }}""")
    
    ARTICLE_OUTLINE = Template("""{{ system_prompt }}

GÖREV: Aşağıdaki konu için detaylı bir makale taslağı oluştur.

KONU: {{ topic }}

TASLAK ŞEKLİ:
{
  "title": "Makale başlığı",
  "abstract_tr": "150-200 kelimelik Türkçe özet",
  "abstract_en": "150-200 kelimelik İngilizce özet",
  "keywords_tr": ["anahtar", "kelimeler"],
  "keywords_en": ["key", "words"],
  "sections": [
    {
      "title": "Giriş",
      "subsections": ["Alt başlık 1", "Alt başlık 2"],
      "estimated_words": 800,
      "key_points": ["Nokta 1", "Nokta 2"],
      "required_citations": 3
    }
  ],
  "required_visuals": [
    {
      "number": 1,
      "description": "Görsel açıklaması",
      "suggested_source": "Kaynak önerisi"
    }
  ],
  "min_references": 25
}

SADECE JSON döndür, başka bir şey yazma.""")
    
    SECTION_WRITER = Template("""{{ system_prompt }}

MAKALE BAĞLAMI:
Başlık: {{ article_title }}
Bölüm: {{ section_title }}

BÖLÜM GEREKSİNİMLERİ:
- Tahmini uzunluk: {{ estimated_words }} kelime
- Ana noktalar: {{ key_points }}
- Minimum atıf: {{ min_citations }} adet

GÖREV: Bu bölümü yaz.

KURALLAR:
1. Atıfları eksiksiz yap: (Yazar, Yıl, s. X)
2. Akademik ama sıkıcı olma
3. Her paragraf 4-6 cümle olsun
4. Geçişleri güçlendir ("Bu bağlamda", "Diğer yandan", vb.)

BÖLÜM METNİ:""")
    
    CITATION_GENERATOR = Template("""{{ system_prompt }}

GÖREV: Aşağıdaki konu için akademik kaynakça listesi oluştur (APA-7).

KONU: {{ topic }}
GEREKEN KAYNAK SAYISI: {{ min_references }}

KAYNAK TİPLERİ (dengeli dağılım):
- Kitaplar: %30
- Makale: %40
- Katalog/Sergi: %20
- Web kaynakları: %10

FORMAT:
Her kaynak şu formatta:
{
  "type": "book|article|catalog|web",
  "apa_citation": "Tam APA-7 formatında kaynak",
  "author": "Yazar adı",
  "year": "2020",
  "title": "Eser başlığı",
  "doi": "10.xxxx/xxxxx (varsa)"
}

SADECE JSON array döndür.""")
    
    @classmethod
    def get_outline_prompt(cls, topic: str, profile: Dict) -> str:
        """Generate outline creation prompt."""
        system = cls.SYSTEM_PROMPT.render(
            avg_length=int(profile.get('avg_doc_length', 4000)),
            avg_sentence=profile['sentence_structure']['avg_sentence_length'],
            lexical_diversity=profile['vocabulary']['lexical_diversity'],
            doc_count=profile['document_count'],
            top_terms=", ".join(list(profile['vocabulary']['top_50_words'].keys())[:20])
        )
        
        return cls.ARTICLE_OUTLINE.render(
            system_prompt=system,
            topic=topic
        )
    
    @classmethod
    def get_section_prompt(cls, profile: Dict, article_title: str, 
                          section_title: str, estimated_words: int,
                          key_points: list, min_citations: int) -> str:
        """Generate section writing prompt."""
        system = cls.SYSTEM_PROMPT.render(
            avg_length=int(profile.get('avg_doc_length', 4000)),
            avg_sentence=profile['sentence_structure']['avg_sentence_length'],
            lexical_diversity=profile['vocabulary']['lexical_diversity'],
            doc_count=profile['document_count'],
            top_terms=", ".join(list(profile['vocabulary']['top_50_words'].keys())[:20])
        )
        
        return cls.SECTION_WRITER.render(
            system_prompt=system,
            article_title=article_title,
            section_title=section_title,
            estimated_words=estimated_words,
            key_points=", ".join(key_points),
            min_citations=min_citations
        )
    
    @classmethod
    def get_citation_prompt(cls, profile: Dict, topic: str, min_references: int = 25) -> str:
        """Generate citation list prompt."""
        system = cls.SYSTEM_PROMPT.render(
            avg_length=int(profile.get('avg_doc_length', 4000)),
            avg_sentence=profile['sentence_structure']['avg_sentence_length'],
            lexical_diversity=profile['vocabulary']['lexical_diversity'],
            doc_count=profile['document_count'],
            top_terms=", ".join(list(profile['vocabulary']['top_50_words'].keys())[:20])
        )
        
        return cls.CITATION_GENERATOR.render(
            system_prompt=system,
            topic=topic,
            min_references=min_references
        )
