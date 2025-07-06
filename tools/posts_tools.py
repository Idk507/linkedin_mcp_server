from typing import Dict, Any
from fastmcp import FastMCP
from services.posts_service import PostsService

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp = None

@mcp.tool()
def get_profile_posts(profile_id: str = None, limit: int = 10) -> Dict[str, Any]:
    """
    Get posts from a LinkedIn profile
    """
    global linkedin_mcp
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return PostsService.get_posts(linkedin_mcp, profile_id, limit)

