@echo off
echo === Arc Project GitHub Setup ===

REM Initialize git repository
git init

REM Add all files
git add .

REM Create initial commit
git commit -m "Initial commit: Arc - Image to 3D Model Tool for Hackathon"

echo.
echo Next steps:
echo 1. Create repository on GitHub.com
echo 2. Copy the remote URL
echo 3. Run: git remote add origin YOUR_REPO_URL
echo 4. Run: git push -u origin main
echo.
pause