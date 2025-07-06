LinkedIn MCP Server
A Python-based server that provides LinkedIn functionality through the MCP (Message Control Protocol) using the linkedin-api and fastmcp libraries. This project allows users to authenticate with LinkedIn, retrieve profile information, fetch posts, search for jobs, get job details, search for people, and retrieve connections.
Project Structure
linkedin_mcp/
├── config/
│   └── linkedin_config.py
├── services/
│   ├── __init__.py
│   ├── linkedin_client.py
│   ├── profile_service.py
│   ├── posts_service.py
│   ├── jobs_service.py
│   ├── people_service.py
│   └── connections_service.py
├── tools/
│   ├── __init__.py
│   ├── auth_tools.py
│   ├── profile_tools.py
│   ├── posts_tools.py
│   ├── jobs_tools.py
│   ├── people_tools.py
│   ├── connections_tools.py
│   └── status_tools.py
├── main.py
├── requirements.txt
└── README.md


config/: Contains configuration and logging setup.
services/: Core LinkedIn functionality split into logical service classes.
tools/: MCP tool definitions that interface with services.
main.py: Entry point for running the server or test mode.
requirements.txt: Lists required Python packages.

Features

Authentication: Authenticate with LinkedIn using email and password.
Profile Retrieval: Fetch profile information for a specific user or the authenticated user.
Post Retrieval: Get posts from a LinkedIn profile.
Job Search: Search for job postings with optional location filtering.
Job Details: Retrieve detailed information about specific job postings.
People Search: Search for people on LinkedIn based on keywords.
Connections: Retrieve connections for a profile.
Status Check: Check the current authentication status.

Installation

Clone the repository or extract the project files.
Ensure Python 3.6+ is installed.
Install dependencies:pip install -r requirements.txt


(Optional) Set up a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



Usage
Running the Server
To start the MCP server:
python main.py

This will start the server, which listens for MCP client connections. You can then connect an MCP client to use the LinkedIn tools.
Test Mode
To run in test mode and see available tools:
python main.py test

This displays a list of available tools and example usage, such as:
authenticate_linkedin('your_email@example.com', 'your_password')
search_linkedin_jobs('python developer', 'San Francisco')
get_profile_info()

Available Tools

authenticate_linkedin(email, password): Authenticate with LinkedIn.
get_profile_info(profile_id=None): Get profile information.
get_profile_posts(profile_id=None, limit=10): Retrieve posts from a profile.
search_linkedin_jobs(keywords, location=None, limit=25): Search for jobs.
get_job_details(job_id): Get details for a specific job.
search_linkedin_people(keywords, limit=10): Search for people.
get_linkedin_connections(urn_id=None, limit=50): Retrieve connections.
get_authentication_status(): Check authentication status.

Requirements

Python 3.6+
Packages listed in requirements.txt:
fastmcp
linkedin-api



Notes

Ensure you have valid LinkedIn credentials for authentication.
The linkedin-api library may have rate limits or require specific permissions.
All operations require authentication first via authenticate_linkedin.
The project is modular, with services handling core functionality and tools providing MCP interfaces.

License
This project is licensed under the MIT License.
