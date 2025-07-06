from typing import Dict, Any
from fastmcp import FastMCP
from services.jobs_service import JobsService

mcp = FastMCP("LinkedIn MCP Server")
linkedin_mcp = None

@mcp.tool()
def search_linkedin_jobs(keywords: str, location: str = None, limit: int = 25) -> Dict[str, Any]:
    """
    Search for job postings on LinkedIn
    """
    global linkedin_mcp
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return JobsService.search_jobs(linkedin_mcp, keywords, location, limit)

@mcp.tool()
def get_job_details(job_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific job posting
    """
    global linkedin_mcp
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return JobsService.get_job_details(linkedin_mcp, job_id)
