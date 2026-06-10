@echo off
title Demis Git Backup Only
cd /d "%~dp0"

echo ==========================================
echo   Demis Auto Git Backup Only (No Shutdown)
echo ==========================================
echo.
echo 1. Backing up all changes to Git...
git add .
git commit -m "feat: final auto backup subway shorts & geumdeungjisa"
git push
echo.
echo Git backup completed successfully!
echo.
echo This window will close in 5 seconds.
echo ==========================================
timeout /t 5
