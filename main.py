from fastmcp import FastMCP
from tools.auth_tools import authenticate_linkedin
from tools.profile_tools import get_profile_info
from tools.posts_tools import get_profile_posts
from tools.jobs_tools import search_linkedin_jobs, get_job_details
from tools.people_tools import search_linkedin_people
from tools.connections_tools import get_linkedin_connections
from tools.status_tools import get_authentication_status

def main():
    mcp = FastMCP("LinkedIn MCP Server")
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("LinkedIn MCP Server - Test Mode")
        print("Available tools:")
        
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
        print("\nTo run as MCP server: python main.py")
        print("To run this test: python main.py test")
        
    else:
        print("LinkedIn MCP Server starting...")
        print("Server is ready and listening for MCP client connections")
        print("Connect your MCP client to use the LinkedIn tools")
        mcp.run()

if __name__ == "__main__":
    main()
