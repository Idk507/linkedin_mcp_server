#!/usr/bin/env python3
"""
LinkedIn MCP Server
Provides LinkedIn functionality through MCP protocol including:
- Post checking and retrieval
- Job post crawling  
- Profile information retrieval
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from fastmcp import FastMCP
from linkedin_api import Linkedin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    """Configuration for LinkedIn credentials"""
    email: str
    password: str

class LinkedInMCP:
    def __init__(self, config: LinkedInConfig):
        self.config = config
        self.linkedin_client = None
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """Authenticate with LinkedIn using provided credentials"""
        try:
            self.linkedin_client = Linkedin(
                self.config.email, 
                self.config.password
            )
            self.authenticated = True
            logger.info("Successfully authenticated with LinkedIn")
            return True
        except Exception as e:
            logger.error(f"LinkedIn authentication failed: {str(e)}")
            self.authenticated = False
            return False
    
    def get_profile(self, profile_id: str = None) -> Dict[str, Any]:
        """Get LinkedIn profile information"""
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            if profile_id:
                # Get specific profile by ID or username
                profile = self.linkedin_client.get_profile(profile_id)
            else:
                # Get own profile
                profile = self.linkedin_client.get_profile()
            
            return {
                "success": True,
                "profile": profile,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error retrieving profile: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_posts(self, profile_id: str = None, limit: int = 10) -> Dict[str, Any]:
        """Get posts from a LinkedIn profile"""
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            if profile_id:
                posts = self.linkedin_client.get_profile_posts(profile_id, post_count=limit)
            else:
                # Get own posts
                posts = self.linkedin_client.get_profile_posts(post_count=limit)
            
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
    
    def search_jobs(self, keywords: str, location: str = None, limit: int = 25) -> Dict[str, Any]:
        """Search for job postings on LinkedIn"""
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            search_params = {
                "keywords": keywords,
                "limit": limit
            }
            
            if location:
                search_params["location_name"] = location
            
            jobs = self.linkedin_client.search_jobs(**search_params)
            
            return {
                "success": True,
                "jobs": jobs,
                "count": len(jobs) if jobs else 0,
                "search_params": search_params,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_job_details(self, job_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific job posting"""
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            job_details = self.linkedin_client.get_job(job_id)
            
            return {
                "success": True,
                "job": job_details,
                "retrieved_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error retrieving job details: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_people(self, keywords: str, limit: int = 10) -> Dict[str, Any]:
        """Search for people on LinkedIn"""
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            people = self.linkedin_client.search_people(
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
    
    def get_connections(self, urn_id: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get LinkedIn connections for a profile"""
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            if urn_id:
                connections = self.linkedin_client.get_profile_connections(urn_id=urn_id, limit=limit)
            else:
                # Get own profile URN first
                own_profile = self.linkedin_client.get_profile()
                own_urn = own_profile.get('entityUrn', '').replace('urn:li:fs_profile:', '')
                if own_urn:
                    connections = self.linkedin_client.get_profile_connections(urn_id=own_urn, limit=limit)
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

# Initialize MCP server
mcp = FastMCP("LinkedIn MCP Server")

# Global LinkedIn client instance
linkedin_mcp: Optional[LinkedInMCP] = None

@mcp.tool()
def authenticate_linkedin(email: str, password: str) -> Dict[str, Any]:
    """
    Authenticate with LinkedIn using email and password
    
    Args:
        email: LinkedIn email address
        password: LinkedIn password
    
    Returns:
        Authentication status and result
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

@mcp.tool()
def get_profile_info(profile_id: str = None) -> Dict[str, Any]:
    """
    Get LinkedIn profile information
    
    Args:
        profile_id: LinkedIn profile ID or username (optional, defaults to own profile)
    
    Returns:
        Profile information
    """
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return linkedin_mcp.get_profile(profile_id)

@mcp.tool()
def get_profile_posts(profile_id: str = None, limit: int = 10) -> Dict[str, Any]:
    """
    Get posts from a LinkedIn profile
    
    Args:
        profile_id: LinkedIn profile ID or username (optional, defaults to own profile)
        limit: Maximum number of posts to retrieve (default: 10)
    
    Returns:
        List of posts
    """
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return linkedin_mcp.get_posts(profile_id, limit)

@mcp.tool()
def search_linkedin_jobs(keywords: str, location: str = None, limit: int = 25) -> Dict[str, Any]:
    """
    Search for job postings on LinkedIn
    
    Args:
        keywords: Job search keywords
        location: Job location (optional)
        limit: Maximum number of jobs to retrieve (default: 25)
    
    Returns:
        List of job postings
    """
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return linkedin_mcp.search_jobs(keywords, location, limit)

@mcp.tool()
def get_job_details(job_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific job posting
    
    Args:
        job_id: LinkedIn job ID
    
    Returns:
        Detailed job information
    """
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return linkedin_mcp.get_job_details(job_id)

@mcp.tool()
def search_linkedin_people(keywords: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search for people on LinkedIn
    
    Args:
        keywords: Search keywords for people
        limit: Maximum number of people to retrieve (default: 10)
    
    Returns:
        List of people profiles
    """
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return linkedin_mcp.search_people(keywords, limit)

@mcp.tool()
def get_linkedin_connections(urn_id: str = None, limit: int = 50) -> Dict[str, Any]:
    """
    Get LinkedIn connections for a profile
    
    Args:
        urn_id: LinkedIn profile URN ID (optional, defaults to own profile)
        limit: Maximum number of connections to retrieve (default: 50)
    
    Returns:
        List of connections
    """
    if not linkedin_mcp or not linkedin_mcp.authenticated:
        return {
            "success": False,
            "message": "Not authenticated. Please authenticate first."
        }
    
    return linkedin_mcp.get_connections(urn_id, limit)

@mcp.tool()
def get_authentication_status() -> Dict[str, Any]:
    """
    Check current authentication status
    
    Returns:
        Authentication status information
    """
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
if __name__ == "__main__":
    import sys
    
    # Check if we should run in test mode
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode - run some sample operations
        print("LinkedIn MCP Server - Test Mode")
        print("Available tools:")
        
        # List all available tools
        tools = [
            "authenticate_linkedin",
            "get_profile_info", 
            "get_profile_posts",
            "search_linkedin_jobs",
            "get_job_details",
            "search_linkedin_people",
            "get_linkedin_connections",
            "get_authentication_status"
        ]
        
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool}")
        
        print("\nExample usage:")
        print("1. First authenticate:")
        print("   authenticate_linkedin('your_email@example.com', 'your_password')")
        print("\n2. Then use other tools:")
        print("   search_linkedin_jobs('python developer', 'San Francisco')")
        print("   get_profile_info()")
        print("\nTo run as MCP server: python linkedin_demo.py")
        print("To run this test: python linkedin_demo.py test")
        
    else:
        # Normal MCP server mode
        print("LinkedIn MCP Server starting...")
        print("Server is ready and listening for MCP client connections")
        print("Connect your MCP client to use the LinkedIn tools")
        mcp.run()