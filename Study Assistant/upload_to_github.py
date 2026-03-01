#!/usr/bin/env python3
"""
GitHub Upload Script for Study Assistant
Clean and upload new version to GitHub repository
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_repo():
    """Check if we're in a git repository"""
    success, _, _ = run_command("git status")
    return success

def initialize_git():
    """Initialize new git repository"""
    print("🔧 Initializing new git repository...")
    
    # Initialize git
    success, _, error = run_command("git init")
    if not success:
        print(f"❌ Failed to initialize git: {error}")
        return False
    
    # Add remote
    success, _, error = run_command("git remote add origin https://github.com/MADGE-petter/Study-assistant.git")
    if not success:
        print(f"❌ Failed to add remote: {error}")
        return False
    
    print("✅ Git repository initialized")
    return True

def clean_git_repo():
    """Clean git repository completely"""
    print("🧹 Cleaning git repository...")
    
    # Remove all git history
    commands = [
        "rm -rf .git",
        "git init",
        "git remote add origin https://github.com/MADGE-petter/Study-assistant.git"
    ]
    
    for cmd in commands:
        success, _, error = run_command(cmd)
        if not success and "rm -rf" not in cmd:
            print(f"❌ Failed to run {cmd}: {error}")
            return False
    
    print("✅ Git repository cleaned")
    return True

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
build/
dist/
*.spec

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# Environment
.env
.venv
env/
venv/

# NLTK data
nltk_data/

# Temporary files
*.tmp
*.temp
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore")

def add_files_to_git():
    """Add files to git"""
    print("📁 Adding files to git...")
    
    # Add all files
    success, stdout, error = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {error}")
        return False
    
    print(f"✅ Files added to git")
    return True

def commit_changes():
    """Commit changes"""
    print("📝 Committing changes...")
    
    # Commit
    success, stdout, error = run_command('git commit -m "🚀 Upload Study Assistant v2.0 - Admin Panel with Security"')
    if not success:
        print(f"❌ Failed to commit: {error}")
        return False
    
    print("✅ Changes committed")
    return True

def push_to_github():
    """Push to GitHub"""
    print("📤 Pushing to GitHub...")
    
    # Force push to overwrite everything
    commands = [
        "git branch -M main",
        "git push -f origin main"
    ]
    
    for cmd in commands:
        success, stdout, error = run_command(cmd)
        if not success:
            print(f"❌ Failed to push: {error}")
            print("💡 You may need to authenticate with GitHub first")
            return False
    
    print("✅ Pushed to GitHub successfully")
    return True

def create_github_release():
    """Create GitHub release (optional)"""
    print("📦 Creating GitHub release...")
    
    # This would require GitHub CLI or API
    print("💡 To create a release, visit: https://github.com/MADGE-petter/Study-assistant/releases/new")
    return True

def main():
    """Main upload process"""
    print("🚀 Study Assistant GitHub Upload Script")
    print("=" * 50)
    
    # Change to main app directory
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    print(f"📁 Working directory: {app_dir}")
    
    # Check if we need to clean or initialize
    if os.path.exists('.git'):
        print("🔍 Found existing .git directory")
        response = input("❓ Do you want to clean and reinitialize? (y/n): ")
        if response.lower() == 'y':
            if not clean_git_repo():
                print("❌ Failed to clean git repository")
                return False
        else:
            print("📋 Using existing git repository")
    else:
        if not initialize_git():
            print("❌ Failed to initialize git repository")
            return False
    
    # Create .gitignore
    create_gitignore()
    
    # Add files
    if not add_files_to_git():
        print("❌ Failed to add files")
        return False
    
    # Commit changes
    if not commit_changes():
        print("❌ Failed to commit changes")
        return False
    
    # Push to GitHub
    if not push_to_github():
        print("❌ Failed to push to GitHub")
        return False
    
    # Create release info
    create_github_release()
    
    print("\n🎉 Upload completed successfully!")
    print("📋 Summary:")
    print("✅ Repository cleaned and initialized")
    print("✅ Files added and committed")
    print("✅ Pushed to GitHub")
    print("🌐 Repository: https://github.com/MADGE-petter/Study-assistant")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        # Force clean and reinitialize
        if os.path.exists('.git'):
            shutil.rmtree('.git')
        main()
    else:
        main()
