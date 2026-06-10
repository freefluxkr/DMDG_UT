@echo off
chcp 65001 > nul
echo ========================================================
echo       Connect AI Agents (어벤져스 팀) 텔레그램 봇
echo ========================================================
echo.
echo 봇을 시작합니다. 중지하려면 이 창에서 Ctrl+C를 누르세요.
echo.

set PYTHONIOENCODING=utf-8
python .agent/telegram/bot.py

pause

