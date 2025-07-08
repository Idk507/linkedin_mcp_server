import streamlit as st
import os
from git import Repo
import logging
from pathlib import Path
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Git Repository Manager",
    page_icon="🔧",
    layout="wide"
)

def get_default_branch(repo, remote_name="origin"):
    """
    Get the default branch of the remote repository
    
    Args:
        repo: Git repository object
        remote_name: Name of the remote repository
        
    Returns:
        str: Name of the default branch or None if not found
    """
    try:
        remote = repo.remotes[remote_name]
        remote.fetch()
        
        # Try to get the default branch from remote HEAD
        try:
            default_branch = repo.git.symbolic_ref('refs/remotes/origin/HEAD').split('/')[-1]
            logger.info(f"Found default branch: {default_branch}")
            return default_branch
        except:
            # If symbolic-ref fails, try common branch names
            remote_branches = [ref.name.split('/')[-1] for ref in remote.refs]
            logger.info(f"Available remote branches: {remote_branches}")
            
            # Check common branch names in order of preference
            for branch_name in ['main', 'master', 'develop', 'dev']:
                if branch_name in remote_branches:
                    logger.info(f"Using branch: {branch_name}")
                    return branch_name
            
            # If no common branches found, use the first available branch
            if remote_branches:
                branch_name = remote_branches[0]
                logger.info(f"Using first available branch: {branch_name}")
                return branch_name
                
    except Exception as e:
        logger.error(f"Error getting default branch: {str(e)}")
    
    return None

def ensure_local_branch_exists(repo, branch_name, remote_name="origin"):
    """
    Ensure local branch exists and is tracking the remote branch
    
    Args:
        repo: Git repository object
        branch_name: Name of the branch
        remote_name: Name of the remote repository
    """
    try:
        # Check if local branch exists
        if branch_name in repo.branches:
            logger.info(f"Local branch '{branch_name}' already exists")
            repo.git.checkout(branch_name)
        else:
            # Check if remote branch exists
            remote_branch = f"{remote_name}/{branch_name}"
            if remote_branch in [ref.name for ref in repo.remotes[remote_name].refs]:
                # Create local branch tracking remote
                logger.info(f"Creating local branch '{branch_name}' tracking '{remote_branch}'")
                repo.git.checkout('-b', branch_name, remote_branch)
            else:
                # Create new local branch
                logger.info(f"Creating new local branch '{branch_name}'")
                repo.git.checkout('-b', branch_name)
                
    except Exception as e:
        logger.error(f"Error ensuring local branch exists: {str(e)}")
        raise

def commit_and_push_files(repo_path: str, remote_name: str = "origin", branch: str = None, 
                         progress_callback=None, log_callback=None):
    """
    Commit and push each file in the repository separately
    
    Args:
        repo_path: Path to the local Git repository
        remote_name: Name of the remote repository (default: origin)
        branch: Branch to push to (default: auto-detect)
        progress_callback: Function to update progress
        log_callback: Function to log messages
    """
    def log_message(message, level="info"):
        if log_callback:
            log_callback(message, level)
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
    
    try:
        # Initialize the repository
        repo = Repo(repo_path)
        
        # Ensure the repository is not bare and has a valid remote
        if repo.bare:
            log_message("Repository is bare, cannot proceed", "error")
            return False
        
        if remote_name not in repo.remotes:
            log_message(f"Remote '{remote_name}' not found", "error")
            return False
        
        # Auto-detect branch if not specified
        if branch is None:
            branch = get_default_branch(repo, remote_name)
            if branch is None:
                log_message("Could not determine default branch", "error")
                return False
        
        # Define the project structure
        project_structure = [
            "config/linkedin_config.py",
            "services/__init__.py",
            "services/linkedin_client.py",
            "services/profile_service.py",
            "services/posts_service.py",
            "services/jobs_service.py",
            "services/people_service.py",
            "services/connections_service.py",
            "tools/__init__.py",
            "tools/auth_tools.py",
            "tools/profile_tools.py",
            "tools/posts_tools.py",
            "tools/jobs_tools.py",
            "tools/people_tools.py",
            "tools/connections_tools.py",
            "tools/status_tools.py",
            "main.py",
            "requirements.txt"
        ]
        
        # Ensure local branch exists and switch to it
        ensure_local_branch_exists(repo, branch, remote_name)
        
        # Get the remote
        remote = repo.remotes[remote_name]
        
        # Pull latest changes to avoid push conflicts (only if remote branch exists)
        try:
            remote_branch = f"{remote_name}/{branch}"
            if remote_branch in [ref.name for ref in remote.refs]:
                log_message(f"Pulling latest changes from {remote_name}/{branch}")
                repo.git.pull(remote_name, branch)
            else:
                log_message(f"Remote branch {remote_name}/{branch} doesn't exist, skipping pull")
        except Exception as e:
            log_message(f"Failed to pull from {remote_name}/{branch}: {str(e)}", "warning")
            log_message("Continuing with commits, but push may fail if there are conflicts", "warning")
        
        # Track files that were successfully committed
        committed_files = []
        
        total_files = len(project_structure)
        
        for i, file_path in enumerate(project_structure):
            full_path = os.path.join(repo_path, file_path)
            
            if progress_callback:
                progress_callback(i + 1, total_files, file_path)
            
            if not os.path.exists(full_path):
                log_message(f"File not found: {file_path}", "warning")
                continue
                
            try:
                # Stage the file
                repo.git.add(file_path)
                
                # Check if there are changes to commit
                if repo.is_dirty(path=file_path) or file_path not in [item.a_path for item in repo.index.diff("HEAD")]:
                    # Commit the file
                    commit_message = f"Add/update {file_path}"
                    repo.index.commit(commit_message)
                    log_message(f"Committed: {file_path}")
                    committed_files.append(file_path)
                else:
                    log_message(f"No changes in {file_path}, skipping commit")
                    
            except Exception as e:
                log_message(f"Error processing {file_path}: {str(e)}", "error")
                continue
        
        # Push all commits at once if there were any commits
        if committed_files:
            try:
                log_message(f"Pushing {len(committed_files)} commits to {remote_name}/{branch}")
                remote.push(refspec=f"{branch}:{branch}")
                log_message(f"Successfully pushed all commits to {remote_name}/{branch}")
                log_message(f"Pushed files: {', '.join(committed_files)}")
            except Exception as e:
                log_message(f"Failed to push commits: {str(e)}", "error")
                log_message("You may need to resolve conflicts manually", "error")
                return False
        else:
            log_message("No files were committed, nothing to push")
                
        log_message("All files processed successfully")
        return True
        
    except Exception as e:
        log_message(f"Failed to process repository: {str(e)}", "error")
        return False

def main():
    st.title("🔧 Git Repository Manager")
    st.markdown("A user-friendly interface for managing your Git repository commits and pushes")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Repository path input
    default_path = r"c:\Users\dhanu\Downloads\mcp_linked"
    repo_path = st.sidebar.text_input(
        "Repository Path",
        value=default_path,
        help="Enter the full path to your Git repository"
    )
    
    # Remote name input
    remote_name = st.sidebar.text_input(
        "Remote Name",
        value="origin",
        help="Name of the remote repository (usually 'origin')"
    )
    
    # Branch selection
    branch_option = st.sidebar.selectbox(
        "Branch Selection",
        ["Auto-detect", "Custom"],
        help="Choose how to select the branch"
    )
    
    custom_branch = None
    if branch_option == "Custom":
        custom_branch = st.sidebar.text_input(
            "Branch Name",
            value="main",
            help="Enter the branch name to push to"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Repository Status")
        
        # Check if repository path exists
        if not os.path.exists(repo_path):
            st.error(f"❌ Repository path does not exist: {repo_path}")
            st.stop()
        
        # Try to load repository info
        try:
            repo = Repo(repo_path)
            st.success(f"✅ Repository loaded successfully")
            
            # Display repository info
            st.subheader("Repository Information")
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.metric("Current Branch", repo.active_branch.name)
                st.metric("Total Commits", len(list(repo.iter_commits())))
            
            with info_col2:
                remotes = [remote.name for remote in repo.remotes]
                st.metric("Remotes", ", ".join(remotes))
                
                # Check if there are uncommitted changes
                if repo.is_dirty():
                    st.warning("⚠️ Repository has uncommitted changes")
                else:
                    st.success("✅ Repository is clean")
            
        except Exception as e:
            st.error(f"❌ Error loading repository: {str(e)}")
            st.stop()
    
    with col2:
        st.header("Project Structure")
        st.markdown("Files to be processed:")
        
        project_files = [
            "config/linkedin_config.py",
            "services/__init__.py",
            "services/linkedin_client.py",
            "services/profile_service.py",
            "services/posts_service.py",
            "services/jobs_service.py",
            "services/people_service.py",
            "services/connections_service.py",
            "tools/__init__.py",
            "tools/auth_tools.py",
            "tools/profile_tools.py",
            "tools/posts_tools.py",
            "tools/jobs_tools.py",
            "tools/people_tools.py",
            "tools/connections_tools.py",
            "tools/status_tools.py",
            "main.py",
            "requirements.txt"
        ]
        
        # Check which files exist
        existing_files = []
        missing_files = []
        
        for file_path in project_files:
            full_path = os.path.join(repo_path, file_path)
            if os.path.exists(full_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        st.metric("Existing Files", len(existing_files))
        st.metric("Missing Files", len(missing_files))
        
        if missing_files:
            with st.expander("Missing Files"):
                for file in missing_files:
                    st.text(f"❌ {file}")
    
    # Action section
    st.header("Actions")
    
    # Commit and Push button
    if st.button("🚀 Commit and Push Files", type="primary", use_container_width=True):
        
        # Determine branch to use
        target_branch = custom_branch if branch_option == "Custom" else None
        
        # Create containers for progress and logs
        progress_container = st.container()
        log_container = st.container()
        
        # Progress tracking
        progress_bar = progress_container.progress(0)
        progress_text = progress_container.empty()
        
        # Log container
        log_placeholder = log_container.empty()
        log_messages = []
        
        def update_progress(current, total, current_file):
            progress = current / total
            progress_bar.progress(progress)
            progress_text.text(f"Processing {current}/{total}: {current_file}")
        
        def log_message(message, level="info"):
            timestamp = datetime.now().strftime("%H:%M:%S")
            emoji = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}
            formatted_message = f"{emoji.get(level, 'ℹ️')} [{timestamp}] {message}"
            log_messages.append(formatted_message)
            
            # Keep only last 20 messages
            if len(log_messages) > 20:
                log_messages.pop(0)
            
            log_placeholder.text_area(
                "Process Log",
                "\n".join(log_messages),
                height=200,
                key=f"log_{len(log_messages)}"
            )
        
        # Execute the commit and push process
        try:
            success = commit_and_push_files(
                repo_path=repo_path,
                remote_name=remote_name,
                branch=target_branch,
                progress_callback=update_progress,
                log_callback=log_message
            )
            
            if success:
                st.success("✅ Repository processing completed successfully!")
                st.balloons()
            else:
                st.error("❌ Repository processing failed. Check the logs for details.")
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.code(traceback.format_exc())
    
    # Additional actions
    st.subheader("Additional Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Check Repository Status"):
            try:
                repo = Repo(repo_path)
                
                # Get status
                status = repo.git.status()
                st.text_area("Repository Status", status, height=200)
                
                # Show recent commits
                st.subheader("Recent Commits")
                commits = list(repo.iter_commits(max_count=5))
                for commit in commits:
                    st.write(f"**{commit.hexsha[:7]}** - {commit.message.strip()} ({commit.author.name})")
                    
            except Exception as e:
                st.error(f"Error checking status: {str(e)}")
    
    with col2:
        if st.button("🌿 List Branches"):
            try:
                repo = Repo(repo_path)
                
                # Local branches
                st.subheader("Local Branches")
                for branch in repo.branches:
                    if branch == repo.active_branch:
                        st.write(f"**{branch.name}** ← current")
                    else:
                        st.write(f"{branch.name}")
                
                # Remote branches
                st.subheader("Remote Branches")
                for remote in repo.remotes:
                    st.write(f"**{remote.name}:**")
                    for ref in remote.refs:
                        branch_name = ref.name.split('/')[-1]
                        st.write(f"  - {branch_name}")
                        
            except Exception as e:
                st.error(f"Error listing branches: {str(e)}")
    
    with col3:
        if st.button("🔄 Pull Latest Changes"):
            try:
                repo = Repo(repo_path)
                current_branch = repo.active_branch.name
                
                # Pull changes
                origin = repo.remotes.origin
                origin.pull(current_branch)
                
                st.success(f"✅ Successfully pulled latest changes from {current_branch}")
                
            except Exception as e:
                st.error(f"Error pulling changes: {str(e)}")
    
    # File explorer section
    st.header("File Explorer")
    
    if st.checkbox("Show file contents"):
        selected_file = st.selectbox(
            "Select a file to view",
            existing_files,
            help="Choose a file to view its contents"
        )
        
        if selected_file:
            try:
                file_path = os.path.join(repo_path, selected_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                st.subheader(f"Contents of {selected_file}")
                st.code(content, language='python' if selected_file.endswith('.py') else 'text')
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This Git Repository Manager helps you commit and push files from your LinkedIn MCP project structure.
    
    **Features:**
    - Automatic branch detection
    - File-by-file commit process
    - Real-time progress tracking
    - Comprehensive logging
    - Repository status checking
    - File content viewing
    
    **Project Structure:**
    The app processes a predefined set of files related to a LinkedIn MCP (Model Context Protocol) project,
    including configuration files, services, tools, and requirements.
    """)

if __name__ == "__main__":
    main()
