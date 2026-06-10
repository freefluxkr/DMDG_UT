@echo off
title Demis Force Git Backup
cd /d "%~dp0"

echo ==========================================
echo   Demis Force Git Backup (Overwrite Remote)
echo ==========================================
echo.
echo 1. Aborting any pending rebase/merge...
git rebase --abort 2>nul
git merge --abort 2>nul

echo.
echo 2. Force pushing to GitHub to overwrite conflicts...
git push origin main --force
echo.
echo Force Git backup completed successfully!
echo This window will close in 5 seconds.
echo ==========================================
timeout /t 5
