from typing import Dict, Any
from datetime import datetime
from config.linkedin_config import logger

class JobsService:
    @staticmethod
    def search_jobs(linkedin_client: Any, keywords: str, location: str = None, limit: int = 25) -> Dict[str, Any]:
        """Search for job postings on LinkedIn"""
        if not linkedin_client.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            search_params = {
                "keywords": keywords,
                "limit": limit
            }
            
            if location:
                search_params["location_name"] = location
            
            jobs = linkedin_client.linkedin_client.search_jobs(**search_params)
            
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
    
    @staticmethod
    def get_job_details(linkedin_client: Any, job_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific job posting"""
        if not linkedin_client.authenticated:
            raise Exception("Not authenticated with LinkedIn")
        
        try:
            job_details = linkedin_client.linkedin_client.get_job(job_id)
            
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
