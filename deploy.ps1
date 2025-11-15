# COVID-19 Data Tracker - GitHub Deploy Script
# Run this script to commit and push all files to GitHub

Write-Host "`n====================================`n" -ForegroundColor Cyan
Write-Host "COVID-19 Data Tracker - GitHub Deploy" -ForegroundColor Green
Write-Host "`n====================================`n" -ForegroundColor Cyan

# Change to project directory
Set-Location "c:\Users\Student 1\Desktop\corona virus"
Write-Host "[1/6] Working directory: $(Get-Location)" -ForegroundColor Yellow

# Initialize git repository
Write-Host "[2/6] Initializing git repository..." -ForegroundColor Yellow
git init
if ($LASTEXITCODE -ne 0) { Write-Host "Error initializing git!" -ForegroundColor Red; exit 1 }

# Add all files
Write-Host "[3/6] Adding all files..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) { Write-Host "Error adding files!" -ForegroundColor Red; exit 1 }

# Create initial commit
Write-Host "[4/6] Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: COVID-19 Data Tracker with interactive dashboard"
if ($LASTEXITCODE -ne 0) { Write-Host "Warning: Commit may have already been made" -ForegroundColor Yellow }

# Add remote (check if already exists)
Write-Host "[5/6] Adding GitHub remote..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote already exists, updating..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/25sh0363-code/Corona-virus-updates.git
} else {
    git remote add origin https://github.com/25sh0363-code/Corona-virus-updates.git
}
if ($LASTEXITCODE -ne 0) { Write-Host "Error adding remote!" -ForegroundColor Red; exit 1 }

# Rename branch and push
Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n====================================`n" -ForegroundColor Green
    Write-Host "SUCCESS! Code pushed to GitHub" -ForegroundColor Green
    Write-Host "`n====================================`n" -ForegroundColor Green
    Write-Host "View your repository at:" -ForegroundColor Cyan
    Write-Host "https://github.com/25sh0363-code/Corona-virus-updates" -ForegroundColor Blue
    Write-Host "`n"
} else {
    Write-Host "`nERROR! Something went wrong during push." -ForegroundColor Red
    Write-Host "Make sure you have internet connection and Git is configured correctly.`n" -ForegroundColor Red
    exit 1
}
