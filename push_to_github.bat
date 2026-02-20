@echo off
echo ========================================
echo GitHub Push Setup
echo ========================================
echo.

REM Check if git is configured
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Git user not configured. Let's set it up!
    echo.
    set /p USERNAME="Enter your GitHub username: "
    set /p EMAIL="Enter your GitHub email: "
    
    git config --global user.name "%USERNAME%"
    git config --global user.email "%EMAIL%"
    
    echo.
    echo Git configured successfully!
    echo.
)

echo Current git configuration:
git config user.name
git config user.email
echo.

echo ========================================
echo Step 1: Commit your changes
echo ========================================
git add .
git commit -m "Initial commit: Production-grade AI translation system with NLLB-200 support"
echo.

echo ========================================
echo Step 2: Create GitHub Repository
echo ========================================
echo.
echo Please do the following:
echo 1. Go to https://github.com/new
echo 2. Repository name: AI-Translation-Hub
echo 3. Description: Production-grade multilingual AI translation system for Indian languages
echo 4. Make it Public
echo 5. DO NOT initialize with README (we already have one)
echo 6. Click "Create repository"
echo.
echo After creating the repository, copy the URL (it will look like):
echo https://github.com/YOUR_USERNAME/AI-Translation-Hub.git
echo.
set /p REPO_URL="Paste your repository URL here: "

echo.
echo ========================================
echo Step 3: Push to GitHub
echo ========================================
git branch -M main
git remote add origin %REPO_URL%
git push -u origin main

echo.
echo ========================================
echo Done! Your code is now on GitHub!
echo ========================================
echo.
echo Your repository: %REPO_URL%
echo.
echo Next steps:
echo 1. Deploy API to Render: See DEPLOYMENT_GUIDE.md
echo 2. Deploy UI to Streamlit: See DEPLOY_CHECKLIST.md
echo.
pause
