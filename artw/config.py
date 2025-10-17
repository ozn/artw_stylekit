"""Configuration management."""
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Global configuration."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Paths
    CORPUS_DIR = Path(os.getenv("CORPUS_DIR", "C:/Korpus"))
    DATA_DIR = Path("data")
    OUT_DIR = Path("out")
    
    # Processing
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "6"))
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def ensure_dirs(cls):
        """Create necessary directories."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.OUT_DIR.mkdir(exist_ok=True)
        (cls.OUT_DIR / "prompts").mkdir(exist_ok=True)
