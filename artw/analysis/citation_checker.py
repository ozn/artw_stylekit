"""APA-7 citation validation."""
import re
import requests
from typing import List, Dict, Tuple
from ..logger import logger

class APAValidator:
    """Validate APA-7 citations."""
    
    DOI_PATTERN = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
    IN_TEXT_PATTERN = r'\(([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+(?:ve|and|&)\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)?),\s*(\d{4})(?:,\s*s\.\s*(\d+(?:-\d+)?))?\)'
    
    def validate_doi(self, doi: str, timeout: int = 5) -> bool:
        """Check if DOI is valid and accessible."""
        try:
            response = requests.head(f"https://doi.org/{doi}", timeout=timeout, allow_redirects=True)
            return response.status_code == 200
        except:
            return False
    
    def extract_in_text_citations(self, text: str) -> List[Tuple[str, str]]:
        """Extract (Author, Year) from text."""
        matches = re.findall(self.IN_TEXT_PATTERN, text)
        return [(author, year) for author, year, _ in matches]
    
    def check_et_al_usage(self, text: str) -> List[str]:
        """Validate et al. usage (APA-7: 3+ authors)."""
        issues = []
        et_al_citations = re.findall(r'\([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+et\s+al\.,\s*\d{4}\)', text)
        if et_al_citations:
            logger.debug(f"Found {len(et_al_citations)} et al. citations")
        return issues
    
    def validate_visual_captions(self, text: str) -> List[str]:
        """Check visual caption format: Görsel X. Artist, Title, Year, Technique, Source, Date"""
        caption_pattern = r'Görsel\s+\d+\.\s+[A-ZÇĞİÖŞÜ]'
        captions = re.findall(caption_pattern, text)
        
        issues = []
        if len(captions) < 1:
            issues.append("No visual captions found (expected: Görsel 1. ...)")
        
        return issues
