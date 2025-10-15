#!/bin/bash
# Script to push code to GitHub repository

echo "================================================"
echo "Pushing to GitHub: dspy-tweet-optimizer"
echo "================================================"
echo ""

# Get GitHub token
TOKEN=$(python get_github_token.py 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "Error: Could not get GitHub token"
    exit 1
fi

# Repository details
REPO_URL="https://tom-doerr:${TOKEN}@github.com/tom-doerr/dspy-tweet-optimizer.git"

# Add remote if it doesn't exist
if ! git remote | grep -q "^origin$"; then
    echo "Adding GitHub remote..."
    git remote add origin "$REPO_URL"
else
    echo "Updating GitHub remote..."
    git remote set-url origin "$REPO_URL"
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)

if [ -z "$CURRENT_BRANCH" ]; then
    echo "No commits yet, creating initial commit..."
    git add .
    git commit -m "Initial commit: DSPy Tweet Optimizer with comprehensive tests"
    CURRENT_BRANCH="main"
    git branch -M main
else
    echo "Current branch: $CURRENT_BRANCH"
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "Committing changes..."
        git add .
        git commit -m "Update: Add GitHub integration and scripts"
    fi
fi

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin "$CURRENT_BRANCH"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Successfully pushed to GitHub!"
    echo "================================================"
    echo "Repository: https://github.com/tom-doerr/dspy-tweet-optimizer"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check the error above."
    exit 1
fi
