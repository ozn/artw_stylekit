"""Generate comprehensive style profile from corpus."""
from pathlib import Path
from typing import Dict, List
import json
import jsonlines
from collections import Counter
import re
from ..logger import logger

class StyleProfiler:
    """Analyze writing style from corpus."""
    
    def __init__(self):
        self.texts: List[str] = []
        
    def load_corpus(self, corpus_file: Path):
        """Load corpus from JSONL."""
        logger.info(f"Loading corpus from {corpus_file}")
        with jsonlines.open(corpus_file) as reader:
            for obj in reader:
                self.texts.append(obj['text'])
        logger.info(f"Loaded {len(self.texts)} documents")
    
    def analyze(self) -> Dict:
        """Generate style profile."""
        profile = {
            "document_count": len(self.texts),
            "avg_doc_length": sum(len(t.split()) for t in self.texts) / len(self.texts) if self.texts else 0,
            "vocabulary": self._analyze_vocabulary(),
            "sentence_structure": self._analyze_sentences(),
            "citations": self._analyze_citations(),
            "terminology": self._extract_terminology(),
        }
        return profile
    
    def _analyze_vocabulary(self) -> Dict:
        """Analyze vocabulary patterns."""
        all_words = []
        for text in self.texts:
            words = re.findall(r'\b\w+\b', text.lower())
            all_words.extend(words)
        
        word_freq = Counter(all_words)
        
        return {
            "total_tokens": len(all_words),
            "unique_tokens": len(word_freq),
            "top_50_words": dict(word_freq.most_common(50)),
            "lexical_diversity": len(word_freq) / len(all_words) if all_words else 0
        }
    
    def _analyze_sentences(self) -> Dict:
        """Analyze sentence structure."""
        all_sentences = []
        for text in self.texts:
            sentences = re.split(r'[.!?]+', text)
            all_sentences.extend([s.strip() for s in sentences if s.strip()])
        
        lengths = [len(s.split()) for s in all_sentences]
        
        return {
            "avg_sentence_length": sum(lengths) / len(lengths) if lengths else 0,
            "median_sentence_length": sorted(lengths)[len(lengths)//2] if lengths else 0,
            "total_sentences": len(all_sentences)
        }
    
    def _analyze_citations(self) -> Dict:
        """Analyze citation patterns."""
        citation_patterns = {
            "in_text": r'\([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+(?:ve|and|&)\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)?,\s*\d{4}\)',
            "et_al": r'\bet\s+al\.\B',
            "page_ref": r's\.\s*\d+',
        }
        
        counts = {}
        for pattern_name, pattern in citation_patterns.items():
            total = sum(len(re.findall(pattern, text)) for text in self.texts)
            counts[pattern_name] = total
        
        return counts
    
    def _extract_terminology(self) -> List[str]:
        """Extract domain-specific terms."""
        all_text = " ".join(self.texts)
        terms = re.findall(r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]{3,}\b', all_text)
        term_freq = Counter(terms)
        return [term for term, count in term_freq.most_common(100) if count > 3]
