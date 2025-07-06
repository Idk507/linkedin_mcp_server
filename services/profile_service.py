from typing import Dict, Any
from datetime import datetime
from config.linkedin_config import logger

class ProfileService:
    @staticmethod
    def get_profile(linkedin_client: Any, profile_id: str = None) -> Dict[str, Any]:
        """Get LinkedIn profile information"""
        if not linkedin_client.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            if profile_id:
                profile = linkedin_client.linkedin_client.get_profile(profile_id)
            else:
                profile = linkedin_client.linkedin_client.get_profile()
            
            return {
                "success": True,
                "profile": profile,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error retrieving profile: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
