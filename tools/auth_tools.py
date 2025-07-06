from typing import Dict, Any
from datetime import datetime
from fastmcp import FastMCP
from config.linkedin_config import LinkedInConfig
from services.linkedin_client import LinkedInMCP

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp: LinkedInMCP = None

@mcp.tool()
def authenticate_linkedin(email: str, password: str) -> Dict[str, Any]:
    """
    Authenticate with LinkedIn using email and password
    """
    global linkedin_mcp
    
    try:
        config = LinkedInConfig(email=email, password=password)
        linkedin_mcp = LinkedInMCP(config)
        
        if linkedin_mcp.authenticate():
            return {
                "success": True,
                "message": "Successfully authenticated with LinkedIn",
                "authenticated_at": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "message": "Authentication failed"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Authentication error: {str(e)}"
        }
