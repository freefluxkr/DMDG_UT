@echo off
title Demis Git Backup and Shutdown
cd /d "%~dp0"

:: .git 폴더가 있는지 확인하고, 없으면 명시적인 프로젝트 폴더로 이동 시도
if not exist ".git" (
    if exist "c:\Users\tuesv\Documents\DMDG_UT\.git" (
        cd /d "c:\Users\tuesv\Documents\DMDG_UT"
    ) else (
        echo ==========================================
        echo   [ERROR] Git 저장소를 찾을 수 없습니다!
        echo   현재 위치: %CD%
        echo   프로젝트 폴더가 올바른지 확인해주세요.
        echo ==========================================
        pause
        exit /b
    )
)

echo ==========================================
echo   Demis Auto Git Backup ^& Computer Shutdown
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
echo 2. System shutdown options:
echo [1] Shutdown in 120 seconds (2 minutes) - Default
echo [2] Shutdown in 10 seconds (Quick)
echo [3] Backup only (Do not shutdown)
echo.
set "choice="
set /p choice="Select option (1-3, default is 1): "
if "%choice%"=="" set choice=1

if "%choice%"=="2" (
    echo.
    echo Turning off the computer in 10 seconds...
    shutdown /s /t 10
) else if "%choice%"=="3" (
    echo.
    echo Shutdown canceled. Git backup is complete!
    pause
    exit /b
) else (
    echo.
    echo Turning off the computer in 120 seconds...
    echo.
    shutdown /s /t 120
)

echo ==========================================
echo * If you want to CANCEL the shutdown, 
echo   press any key in this window now!
echo ==========================================
echo.
pause
shutdown /a
echo.
echo [INFO] Shutdown has been canceled successfully!
echo.
pause
