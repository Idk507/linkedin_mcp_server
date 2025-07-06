from typing import Dict, Any
from datetime import datetime
from config.linkedin_config import logger

class ConnectionsService:
    @staticmethod
    def get_connections(linkedin_client: Any, urn_id: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get LinkedIn connections for a profile"""
        if not linkedin_client.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            if urn_id:
                connections = linkedin_client.linkedin_client.get_profile_connections(urn_id=urn_id, limit=limit)
            else:
                own_profile = linkedin_client.linkedin_client.get_profile()
                own_urn = own_profile.get('entityUrn', '').replace('urn:li:fs_profile:', '')
                if own_urn:
                    connections = linkedin_client.linkedin_client.get_profile_connections(urn_id=own_urn, limit=limit)
                else:
                    raise Exception("Could not retrieve own profile URN")
            
            return {
                "success": True,
                "connections": connections,
                "count": len(connections) if connections else 0,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error retrieving connections: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
