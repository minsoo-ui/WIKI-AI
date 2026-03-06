@echo off
chcp 65001 >nul

echo ========================================================
echo        🔍 DEBUG BACKEND WIKI-AI 🔍
echo ========================================================
echo.

cd /d "D:\Google Antigravity\WIKI-AI\backend"

echo Kiem tra moi truong VENV...
if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo -^> Da kich hoat venv
) else (
    echo -^> Khong tim thay venv, dung Python he thong.
)

echo.
echo Khoi dong server: python run.py
echo --------------------------------------------------------
python run.py

echo.
echo --------------------------------------------------------
echo 🛑 BACKEND DA DUNG LAI (Có thể do lỗi Code / Thiếu thư viện)
echo Vui long chup hoac copy dong chu bao loi (neu co) len chat.
pause
