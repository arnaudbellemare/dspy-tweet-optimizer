# Publishing to GitHub - Step-by-Step Guide

This guide will help you publish your DSPy Tweet Optimizer project to GitHub.

## Prerequisites

- A GitHub account ([Sign up here](https://github.com/join))
- Git installed on your local machine
- Access to the Replit workspace shell

## Step 1: Create a New GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Fill in the details:
   - **Repository name**: `dspy-tweet-optimizer` (or your preferred name)
   - **Description**: "AI-powered tweet optimization tool using DSPy and Claude 3.5 Sonnet"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

## Step 2: Export Dependencies

Since Replit manages dependencies, you'll need to create a `requirements.txt` file manually:

1. In the Replit shell, run:
```bash
pip freeze > requirements.txt
```

2. Edit `requirements.txt` to keep only the essential packages:
```
streamlit>=1.28.0
dspy-ai>=2.0.0
pydantic>=2.0.0
pandas>=2.0.0
openai>=1.0.0
pytest>=7.4.0
pytest-mock>=3.11.0
```

## Step 3: Review Files Before Publishing

Make sure these files are ready:
- ✅ `README.md` - Project documentation
- ✅ `.gitignore` - Excludes unnecessary files
- ✅ `LICENSE` - MIT license
- ✅ All `.py` files - Your application code
- ✅ `tests/` directory - Unit tests
- ✅ `.streamlit/config.toml` - Streamlit configuration

Optional files (you may want to exclude these):
- `categories.json` - User's custom categories
- `settings.json` - User preferences
- `input_history.json` - User's input history

## Step 4: Connect to GitHub

In the Replit shell, run these commands (replace `YOUR_USERNAME` with your GitHub username):

```bash
# Remove the current backup remote
git remote remove gitsafe-backup

# Add your GitHub repository as the origin
git remote add origin https://github.com/YOUR_USERNAME/dspy-tweet-optimizer.git

# Verify the remote was added
git remote -v
```

## Step 5: Commit Your Changes

```bash
# Check what files will be committed
git status

# Add all files
git add .

# Create a commit
git commit -m "Initial commit: DSPy Tweet Optimizer with tests and documentation"
```

## Step 6: Push to GitHub

```bash
# Push to GitHub (you'll be prompted for your GitHub credentials)
git push -u origin main

# If your default branch is 'master' instead of 'main', use:
git push -u origin master
```

**Note**: You may need to authenticate. GitHub no longer accepts passwords for git operations. You'll need to:
- Use a [Personal Access Token](https://github.com/settings/tokens) instead of your password
- Or set up [SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

## Step 7: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/dspy-tweet-optimizer`
2. Verify all files are there
3. Check that the README displays correctly
4. Browse through the code to ensure everything looks good

## Step 8: Update README (Optional)

Update the clone URL in `README.md`:

```markdown
git clone https://github.com/YOUR_USERNAME/dspy-tweet-optimizer.git
```

Commit and push the change:
```bash
git add README.md
git commit -m "Update clone URL in README"
git push
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:
1. Create a Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token"
   - Give it repo access
   - Use the token as your password when pushing

2. Or set up SSH keys for easier authentication

### Branch Name Mismatch

If GitHub shows a different default branch:
```bash
# Rename your branch to match GitHub's default
git branch -M main
git push -u origin main
```

### Large Files

If you have files over 100MB, they'll be rejected. Check `.gitignore` to exclude them.

## Next Steps

After publishing:
- Add a repository description and topics on GitHub
- Enable GitHub Actions for CI/CD (optional)
- Add contributors (if working with a team)
- Star your own repository
- Share it with others!

## Keeping it Updated

Whenever you make changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

---

Congratulations! Your project is now on GitHub. 🎉
