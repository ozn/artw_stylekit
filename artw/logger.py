"""Logging setup."""
from loguru import logger
import sys
from .config import Config

logger.remove()
logger.add(
    sys.stderr,
    level=Config.LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>"
)
logger.add(
    "data/artw.log",
    rotation="10 MB",
    retention="1 week",
    level="DEBUG"
)
