@echo off
title Demis Git Backup and Shutdown
cd /d "c:\Users\user\Documents\DMDG_UT"

echo ==========================================
echo   Demis Auto Git Backup & Computer Shutdown
echo ==========================================
echo.
echo 1. Backing up all changes to Git...
git add .
git commit -m "feat: final auto backup before shutdown"
git push
echo.
echo Git backup completed successfully!
echo ==========================================
echo.
echo 2. Turning off the computer in 10 seconds...
echo (To cancel shutdown, close this window or type: shutdown /a)
shutdown /s /t 10
pause
