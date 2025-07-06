#!/usr/bin/env python3
"""
Interactive test interface for LinkedIn MCP Server
"""

import json
import sys
import os
import getpass

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linkedin_demo import (
    authenticate_linkedin, 
    get_profile_info, 
    get_profile_posts,
    search_linkedin_jobs,
    get_job_details,
    search_linkedin_people,
    get_linkedin_connections,
    get_authentication_status,
)

def print_result(data, title="Result"):
    """Pretty print results with all data"""
    print(f"\n{'='*60}")
    print(f"[{title}]")
    print(f"{'='*60}")
    
    if isinstance(data, dict):
        if data.get('success'):
            print("Status: SUCCESS")
            if 'message' in data:
                print(f"Message: {data['message']}")
            if 'count' in data:
                print(f"Count: {data['count']}")
            if 'retrieved_at' in data:
                print(f"Retrieved at: {data['retrieved_at']}")
            if 'authenticated_at' in data:
                print(f"Authenticated at: {data['authenticated_at']}")
            
            # Print all data based on type
            if 'profile' in data:
                print("\nProfile Data:")
                print(json.dumps(data['profile'], indent=2, default=str))
            
            if 'posts' in data:
                print("\nPosts Data:")
                print(json.dumps(data['posts'], indent=2, default=str))
            
            if 'jobs' in data:
                print("\nJobs Data:")
                print(json.dumps(data['jobs'], indent=2, default=str))
                if 'search_params' in data:
                    print(f"\nSearch Parameters: {data['search_params']}")
            
            if 'job' in data:
                print("\nJob Details:")
                print(json.dumps(data['job'], indent=2, default=str))
            
            if 'people' in data:
                print("\nPeople Data:")
                print(json.dumps(data['people'], indent=2, default=str))
            
            if 'connections' in data:
                print("\nConnections Data:")
                print(json.dumps(data['connections'], indent=2, default=str))
                
        else:
            print("Status: FAILED")
            if 'message' in data:
                print(f"Message: {data['message']}")
            if 'error' in data:
                print(f"Error: {data['error']}")
    else:
        print("Raw Data:")
        print(json.dumps(data, indent=2, default=str))
    
    print(f"{'='*60}\n")

def main():
    print("LinkedIn MCP Server - Interactive Test")
    print("=" * 60)
    
    authenticated = False
    
    while True:
        print("\nAvailable Options:")
        print("1. Authenticate with LinkedIn")
        print("2. Get profile info")
        print("3. Get profile posts")
        print("4. Search jobs")
        print("5. Search people")
        print("6. Get connections")
        print("7. Test all functions (demo mode)")
        print("8. Exit")
        
        choice = input("\nChoose an option (1-8): ").strip()
        
        if choice == '1':
            # Authenticate
            print("\nLinkedIn Authentication")
            email = input("Enter your LinkedIn email: ").strip()
            password = getpass.getpass("Enter your LinkedIn password: ")
            
            if email and password:
                print("Authenticating...")
                result = authenticate_linkedin(email, password)
                print_result(result, "Authentication Result")
                authenticated = result.get('success', False)
                
                # Check authentication status after login
                if authenticated:
                    status_result = get_authentication_status()
                    print_result(status_result, "Authentication Status")
            else:
                print("Email and password are required!")
                
        elif choice == '2':
            # Get profile info
            if not authenticated:
                print("Please authenticate first!")
                continue
            
            profile_id = input("Enter profile ID (or press Enter for your profile): ").strip()
            profile_id = profile_id if profile_id else None
            
            print("Getting profile info...")
            result = get_profile_info(profile_id)
            print_result(result, "Profile Information")
            
        elif choice == '3':
            # Get profile posts
            if not authenticated:
                print("Please authenticate first!")
                continue
            
            profile_id = input("Enter profile ID (or press Enter for your profile): ").strip()
            profile_id = profile_id if profile_id else None
            
            try:
                limit = int(input("Number of posts to retrieve (default 10): ").strip() or "10")
            except ValueError:
                limit = 10
            
            print("Getting posts...")
            result = get_profile_posts(profile_id, limit)
            print_result(result, "Profile Posts")
            
        elif choice == '4':
            # Search jobs
            if not authenticated:
                print("Please authenticate first!")
                continue
            
            keywords = input("Enter job search keywords: ").strip()
            if not keywords:
                print("Keywords are required!")
                continue
            
            location = input("Enter location (optional): ").strip()
            location = location if location else None
            
            try:
                limit = int(input("Number of jobs to retrieve (default 25): ").strip() or "25")
            except ValueError:
                limit = 25
            
            print("Searching jobs...")
            result = search_linkedin_jobs(keywords, location, limit)
            print_result(result, "Job Search Results")
            
        elif choice == '5':
            # Search people
            if not authenticated:
                print("Please authenticate first!")
                continue
            
            keywords = input("Enter people search keywords: ").strip()
            if not keywords:
                print("Keywords are required!")
                continue
            
            try:
                limit = int(input("Number of people to retrieve (default 10): ").strip() or "10")
            except ValueError:
                limit = 10
            
            print("Searching people...")
            result = search_linkedin_people(keywords, limit)
            print_result(result, "People Search Results")
            
        elif choice == '6':
            # Get connections
            if not authenticated:
                print("Please authenticate first!")
                continue
            
            urn_id = input("Enter profile URN ID (or press Enter for your connections): ").strip()
            urn_id = urn_id if urn_id else None
            
            try:
                limit = int(input("Number of connections to retrieve (default 50): ").strip() or "50")
            except ValueError:
                limit = 50
            
            print("Getting connections...")
            result = get_linkedin_connections(urn_id, limit)
            print_result(result, "Connections")
            
        elif choice == '7':
            # Test all functions in demo mode
            print("\nDemo Mode - Testing all functions...")
            
            # Test authentication status
            result = get_authentication_status()
            print_result(result, "Authentication Status")
            
            # Test other functions (will show "not authenticated" messages)
            print("Testing other functions...")
            
            job_result = search_linkedin_jobs("python developer", "San Francisco", 5)
            print_result(job_result, "Job Search (Demo)")
            
            profile_result = get_profile_info()
            print_result(profile_result, "Profile Info (Demo)")
            
            people_result = search_linkedin_people("data scientist", 3)
            print_result(people_result, "People Search (Demo)")
            
            connections_result = get_linkedin_connections(None, 10)
            print_result(connections_result, "Connections (Demo)")
            
            print("Demo completed!")
            
        elif choice == '8':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please choose 1-8.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()