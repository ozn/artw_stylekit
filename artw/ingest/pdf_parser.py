"""PDF text extraction."""
from pathlib import Path
import fitz  # PyMuPDF
from typing import Dict, Optional
from ..logger import logger

def extract_text_from_pdf(pdf_path: Path) -> Optional[Dict]:
    """
    Extract text from PDF with metadata.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dict with text, metadata, or None if failed
    """
    try:
        doc = fitz.open(pdf_path)
        
        text = ""
        for page in doc:
            text += page.get_text()
        
        metadata = {
            "filename": pdf_path.name,
            "pages": doc.page_count,
            "author": doc.metadata.get("author", ""),
            "title": doc.metadata.get("title", ""),
        }
        
        doc.close()
        
        return {
            "text": text.strip(),
            "metadata": metadata,
            "path": str(pdf_path)
        }
    except Exception as e:
        logger.error(f"Failed to process {pdf_path.name}: {e}")
        return None
