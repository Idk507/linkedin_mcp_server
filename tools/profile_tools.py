from typing import Dict, Any
from fastmcp import FastMCP
from services.profile_service import ProfileService

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp = None

@mcp.tool()
def get_profile_info(profile_id: str = None) -> Dict[str, Any]:
    """
    Get LinkedIn profile information
    """
    global linkedin_mcp
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return ProfileService.get_profile(linkedin_mcp, profile_id)
