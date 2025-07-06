from typing import Dict, Any
from datetime import datetime
from config.linkedin_config import logger

class PeopleService:
    @staticmethod
    def search_people(linkedin_client: Any, keywords: str, limit: int = 10) -> Dict[str, Any]:
        """Search for people on LinkedIn"""
        if not linkedin_client.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            people = linkedin_client.linkedin_client.search_people(
                keywords=keywords,
                limit=limit
            )
            
            return {
                "success": True,
                "people": people,
                "count": len(people) if people else 0,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error searching people: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
