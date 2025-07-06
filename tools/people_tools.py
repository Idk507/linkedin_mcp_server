from typing import Dict, Any
from fastmcp import FastMCP
from services.people_service import PeopleService

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp = None

@mcp.tool()
def search_linkedin_people(keywords: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search for people on LinkedIn
    """
    global linkedin_mcp
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return PeopleService.search_people(linkedin_mcp, keywords, limit)
