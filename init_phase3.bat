@echo off
echo =======================================================
echo Phase 3: React + Firebase 프로젝트 초기화 스크립트
echo =======================================================
echo.
echo 1. Vite React 프로젝트 생성 중 (museum-react)...
call npx -y create-vite@latest museum-react --template react
if %ERRORLEVEL% neq 0 (
    echo [에러] Vite 프로젝트 생성 실패!
    pause
    exit /b %ERRORLEVEL%
)

cd museum-react

echo 2. 기본 패키지 설치 중...
call npm install
if %ERRORLEVEL% neq 0 (
    echo [에러] npm install 실패!
    pause
    exit /b %ERRORLEVEL%
)

echo 3. Phase 3 핵심 라이브러리 설치 중 (Firebase, Router, Framer Motion, Tailwind)...
call npm install firebase react-router-dom framer-motion tailwindcss @tailwindcss/vite
if %ERRORLEVEL% neq 0 (
    echo [에러] 추가 라이브러리 설치 실패!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =======================================================
echo 프로젝트 초기화가 완벽하게 완료되었습니다!
echo 이제 당목담글 AI 팀(제이)에게 완료되었다고 알려주세요!
echo =======================================================
pause
