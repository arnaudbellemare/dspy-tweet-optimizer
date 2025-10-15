#!/usr/bin/env python3
"""Script to create a GitHub repository and push code to it."""

import os
import sys
import subprocess
from github import Github, GithubException

def get_github_token():
    """Get GitHub token from environment or connection."""
    # Check if PyGithub integration token is available
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        # Try alternative env var names
        token = os.getenv("GH_TOKEN")
    
    if not token:
        print("Error: GitHub token not found in environment variables")
        print("Please set GITHUB_TOKEN environment variable")
        sys.exit(1)
    
    return token

def run_command(cmd, check=True):
    """Run a shell command and return output."""
    print(f"Running: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=check
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
    return result

def create_github_repo(token, repo_name, description, private=False):
    """Create a new GitHub repository."""
    try:
        g = Github(token)
        user = g.get_user()
        
        print(f"Authenticated as: {user.login}")
        
        # Create repository
        print(f"Creating repository: {repo_name}")
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private,
            auto_init=False  # Don't initialize with README
        )
        
        print(f"✅ Repository created successfully!")
        print(f"   URL: {repo.html_url}")
        print(f"   Clone URL: {repo.clone_url}")
        
        return repo
        
    except GithubException as e:
        if e.status == 422:
            print(f"Error: Repository '{repo_name}' already exists")
            print("Please delete it first or choose a different name")
        else:
            print(f"GitHub API Error: {e.data.get('message', str(e))}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def setup_git_and_push(repo):
    """Initialize git, commit, and push to GitHub."""
    # Check if .git exists
    if os.path.exists('.git'):
        print("Git repository already initialized")
        
        # Check current remote
        result = run_command("git remote -v", check=False)
        
        # Remove existing origin if it's the backup remote
        if "gitsafe-backup" in result.stdout:
            print("Removing backup remote...")
            run_command("git remote remove gitsafe-backup", check=False)
        
        # Check if origin exists
        if "origin" in result.stdout:
            print("Updating origin remote...")
            run_command(f"git remote set-url origin {repo.clone_url}")
        else:
            print("Adding origin remote...")
            run_command(f"git remote add origin {repo.clone_url}")
    else:
        print("Initializing git repository...")
        run_command("git init")
        run_command(f"git remote add origin {repo.clone_url}")
    
    # Configure git user if not set
    result = run_command("git config user.name", check=False)
    if not result.stdout.strip():
        run_command('git config user.name "Replit Agent"')
    
    result = run_command("git config user.email", check=False)
    if not result.stdout.strip():
        run_command('git config user.email "agent@replit.com"')
    
    # Get current branch
    result = run_command("git branch --show-current", check=False)
    current_branch = result.stdout.strip()
    
    if not current_branch:
        # No commits yet, create initial commit
        print("Creating initial commit...")
        run_command("git add .")
        run_command('git commit -m "Initial commit: DSPy Tweet Optimizer"')
        current_branch = "main"
        run_command(f"git branch -M {current_branch}")
    else:
        print(f"Current branch: {current_branch}")
        
        # Check if there are uncommitted changes
        result = run_command("git status --porcelain", check=False)
        if result.stdout.strip():
            print("Committing changes...")
            run_command("git add .")
            run_command('git commit -m "Update: Add GitHub publishing files and integration tests"')
    
    # Push to GitHub
    print(f"Pushing to GitHub ({current_branch})...")
    run_command(f"git push -u origin {current_branch}")
    
    print(f"\n✅ Successfully pushed to GitHub!")
    print(f"   Repository: {repo.html_url}")

def main():
    """Main function."""
    # Configuration
    repo_name = "dspy-tweet-optimizer"
    description = "AI-powered tweet optimization tool using DSPy and Claude 3.5 Sonnet with hill-climbing algorithm"
    private = False  # Make it public
    
    print("=" * 60)
    print("GitHub Repository Creation Script")
    print("=" * 60)
    print()
    
    # Get GitHub token
    token = get_github_token()
    
    # Create repository
    repo = create_github_repo(token, repo_name, description, private)
    
    # Setup git and push
    setup_git_and_push(repo)
    
    print()
    print("=" * 60)
    print("🎉 Success! Your code is now on GitHub!")
    print("=" * 60)
    print(f"Repository URL: {repo.html_url}")
    print()

if __name__ == "__main__":
    main()
