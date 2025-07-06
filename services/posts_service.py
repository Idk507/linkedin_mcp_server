from typing import Dict, Any
from datetime import datetime
from config.linkedin_config import logger

class PostsService:
    @staticmethod
    def get_posts(linkedin_client: Any, profile_id: str = None, limit: int = 10) -> Dict[str, Any]:
        """Get posts from a LinkedIn profile"""
        if not linkedin_client.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            if profile_id:
                posts = linkedin_client.linkedin_client.get_profile_posts(profile_id, post_count=limit)
            else:
                posts = linkedin_client.linkedin_client.get_profile_posts(post_count=limit)
            
            return {
                "success": True,
                "posts": posts,
                "count": len(posts) if posts else 0,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error retrieving posts: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
