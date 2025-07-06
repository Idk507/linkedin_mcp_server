from typing import Dict, Any
from fastmcp import FastMCP

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp = None

@mcp.tool()
def get_authentication_status() -> Dict[str, Any]:
    """
    Check current authentication status
    """
    global linkedin_mcp
    if linkedin_mcp and linkedin_mcp.authenticated:
        return {
            "success": True,
            "authenticated": True,
            "message": "Successfully authenticated with LinkedIn"
        }
    else:
        return {
            "success": False,
            "authenticated": False,
            "message": "Not authenticated with LinkedIn"
        }
