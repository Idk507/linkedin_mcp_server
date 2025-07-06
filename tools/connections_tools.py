from typing import Dict, Any
from fastmcp import FastMCP
from services.connections_service import ConnectionsService

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp = None

@mcp.tool()
def get_linkedin_connections(urn_id: str = None, limit: int = 50) -> Dict[str, Any]:
    """
    Get LinkedIn connections for a profile
    """
    global linkedin_mcp
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return ConnectionsService.get_connections(linkedin_mcp, urn_id, limit)
