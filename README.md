
# LinkedIn MCP Server

A Python-based server that provides LinkedIn functionality through the MCP (Message Control Protocol) using the `linkedin-api` and `fastmcp` libraries.

This project allows users to:
- Authenticate with LinkedIn
- Retrieve profile information
- Fetch posts
- Search for jobs and get job details
- Search for people
- Retrieve connections

---

## 📁 Project Structure

```

linkedin\_mcp/
├── config/
│   └── linkedin\_config.py
├── services/
│   ├── **init**.py
│   ├── linkedin\_client.py
│   ├── profile\_service.py
│   ├── posts\_service.py
│   ├── jobs\_service.py
│   ├── people\_service.py
│   └── connections\_service.py
├── tools/
│   ├── **init**.py
│   ├── auth\_tools.py
│   ├── profile\_tools.py
│   ├── posts\_tools.py
│   ├── jobs\_tools.py
│   ├── people\_tools.py
│   ├── connections\_tools.py
│   └── status\_tools.py
├── main.py
├── requirements.txt
└── README.md

````

### Folder Descriptions

- **`config/`**: Contains configuration and logging setup.
- **`services/`**: Core LinkedIn functionality split into logical service classes.
- **`tools/`**: MCP tool definitions that interface with services.
- **`main.py`**: Entry point for running the server or test mode.
- **`requirements.txt`**: Lists required Python packages.

---

## 🚀 Features

- **Authentication**: Authenticate with LinkedIn using email and password.
- **Profile Retrieval**: Fetch profile info for a specific or authenticated user.
- **Post Retrieval**: Get posts from a LinkedIn profile.
- **Job Search**: Search for job postings (optional location filter).
- **Job Details**: Retrieve detailed info about specific jobs.
- **People Search**: Search for people on LinkedIn using keywords.
- **Connections**: Retrieve connections for a profile.
- **Status Check**: Check the current authentication status.

---

## 📦 Installation

1. Clone the repository or extract the project files.
2. Ensure Python 3.6+ is installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
````

### (Optional) Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

## ⚙️ Usage

### Running the Server

```bash
python main.py
```

This starts the MCP server to listen for client connections.

### Test Mode

```bash
python main.py test
```

This will display available tools and sample usage like:

```python
authenticate_linkedin('your_email@example.com', 'your_password')
search_linkedin_jobs('python developer', 'San Francisco')
get_profile_info()
```

---

## 🛠️ Available Tools

```python
authenticate_linkedin(email, password)               # Authenticate with LinkedIn
get_profile_info(profile_id=None)                    # Get profile information
get_profile_posts(profile_id=None, limit=10)         # Retrieve posts from a profile
search_linkedin_jobs(keywords, location=None, limit=25)  # Search for jobs
get_job_details(job_id)                              # Get job details
search_linkedin_people(keywords, limit=10)           # Search for people
get_linkedin_connections(urn_id=None, limit=50)      # Retrieve connections
get_authentication_status()                          # Check auth status
```

---

## 📋 Requirements

* Python 3.6+
* Packages listed in `requirements.txt`:

  * `fastmcp`
  * `linkedin-api`

---

## 🔐 Notes

* Ensure you have valid LinkedIn credentials for authentication.
* The `linkedin-api` library may enforce rate limits or permissions.
* All operations require prior authentication via `authenticate_linkedin`.
* Project is modular: services handle core logic, tools expose MCP interfaces.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).


```
