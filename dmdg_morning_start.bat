@echo off
chcp 65001 > nul
title [당목담글] 아벤져스 팀원 전체 활성화 스크립트

echo ========================================================
echo   🌅 [당목담글] 아침 출근 에이전트 자동 기동 서비스
echo ========================================================
echo.

:: 1. Ollama 서버 확인 및 자동 실행
echo [1/3] 로컬 Ollama AI 서버 상태 체크 중...
netstat -ano | findstr 11434 > nul
if %errorlevel% equ 0 (
    echo    => ✅ Ollama 서버가 이미 실행 중입니다.
) else (
    echo    => ⚠️ Ollama 서버가 꺼져 있습니다. 백그라운드로 실행합니다...
    start /min "" ollama serve
    timeout /t 3 > nul
)

:: 2. 텔레그램 에이전트 봇 기동
echo [2/3] 텔레그램 에이전트 봇 (@aiffall_bot) 기동 중...
set PYTHONIOENCODING=utf-8
start /min "당목담글 텔레그램 봇" python "c:\Users\tuesv\Documents\DMDG_UT\.agent\telegram\bot.py"
echo    => ✅ 텔레그램 봇이 백그라운드에서 실행되었습니다.

:: 3. 리액트 로컬 개발 웹앱 서버 기동
echo [3/3] 리액트 웹앱 로컬 개발 서버 기동 중...
cd /d "c:\Users\tuesv\Documents\DMDG_UT\museum-react"
start /min "당목담글 리액트 웹앱" npm run dev
echo    => ✅ 리액트 웹앱 서버가 백그라운드에서 실행되었습니다 (http://localhost:5173).

echo.
echo ========================================================
echo   🎉 모든 팀원(에이전트) 및 서버 활성화 완료!
echo   (백그라운드에서 조용히 대기 중이니 바로 작업하시면 됩니다.)
echo ========================================================
echo.
timeout /t 5
