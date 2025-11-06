@echo off
REM GitHub Deployment Setup Script
REM This script helps you prepare and push your code to GitHub

echo ========================================
echo Patrol Shapefile Downloader
echo GitHub Deployment Setup
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Checking repository status...
echo.

REM Check if already a git repository
if exist ".git" (
    echo This directory is already a Git repository.
    echo Current remote:
    git remote -v
    echo.
    set /p REINIT="Do you want to reinitialize? (y/n): "
    if /i not "%REINIT%"=="y" (
        echo Keeping existing repository.
        goto :COMMIT
    )
    echo Removing existing .git directory...
    rmdir /s /q .git
)

echo [2/5] Initializing Git repository...
git init
echo.

echo [3/5] Please enter your GitHub repository URL
echo Example: https://github.com/yourusername/streamlit_patrol.git
set /p REPO_URL="Repository URL: "
echo.

echo Adding remote origin...
git remote add origin %REPO_URL%
echo.

:COMMIT
echo [4/5] Staging all files...
git add .
echo.

echo Files to be committed:
git status --short
echo.

set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Initial commit: Patrol Shapefile Downloader v1.0

echo Committing files...
git commit -m "%COMMIT_MSG%"
echo.

echo [5/5] Ready to push to GitHub!
echo.
set /p DO_PUSH="Push to GitHub now? (y/n): "
if /i "%DO_PUSH%"=="y" (
    echo Pushing to main branch...
    git branch -M main
    git push -u origin main
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Go to https://share.streamlit.io
    echo 2. Sign in with GitHub
    echo 3. Click 'New app'
    echo 4. Select your repository
    echo 5. Set main file to: app.py
    echo 6. Click Deploy!
    echo.
) else (
    echo.
    echo Push skipped. To push later, run:
    echo   git branch -M main
    echo   git push -u origin main
    echo.
)

echo ========================================
echo Setup complete!
echo ========================================
pause
