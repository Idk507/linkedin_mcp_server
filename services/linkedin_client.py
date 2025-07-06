from typing import Optional
from linkedin_api import Linkedin
from config.linkedin_config import LinkedInConfig, logger

class LinkedInMCP:
    def __init__(self, config: LinkedInConfig):
        self.config = config
        self.linkedin_client = None
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """Authenticate with LinkedIn using provided credentials"""
        try:
            self.linkedin_client = Linkedin(
                self.config.email, 
                self.config.password
            )
            self.authenticated = True
            logger.info("Successfully authenticated with LinkedIn")
            return True
        except Exception as e:
            logger.error(f"LinkedIn authentication failed: {str(e)}")
            self.authenticated = False
            return False
