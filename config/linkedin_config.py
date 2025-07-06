import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    """Configuration for LinkedIn credentials"""
    email: str
    password: str