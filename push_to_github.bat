@echo off
REM COVID-19 Data Tracker - Git Push Script
REM This script initializes git and pushes to GitHub

echo.
echo ====================================
echo COVID-19 Data Tracker - Git Setup
echo ====================================
echo.

REM Initialize git repository
echo [1/5] Initializing git repository...
git init
if errorlevel 1 goto error

REM Add all files
echo [2/5] Adding files...
git add .
if errorlevel 1 goto error

REM Create initial commit
echo [3/5] Creating commit...
git commit -m "Initial commit: COVID-19 Data Tracker with interactive dashboard"
if errorlevel 1 goto error

REM Add remote
echo [4/5] Adding GitHub remote...
git remote add origin https://github.com/25sh0363-code/Corona-virus-updates.git
if errorlevel 1 goto error

REM Rename branch to main
echo [5/5] Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 goto error

echo.
echo ====================================
echo SUCCESS! Code pushed to GitHub
echo ====================================
echo.
echo View your repository at:
echo https://github.com/25sh0363-code/Corona-virus-updates
echo.
pause
exit /b 0

:error
echo.
echo ERROR! Something went wrong.
echo Make sure Git is installed and you have internet connection.
echo.
pause
exit /b 1
