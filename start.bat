@echo off
chcp 65001 >nul
:: Đổi bảng mã sang UTF-8 để hiển thị tiếng Việt

echo ========================================================
echo        🚀 KHOI DONG WIKI-AI (LOCAL MULTI-AGENT) 🚀
echo ========================================================

cd /d "%~dp0"

echo.
echo [1/3] Kiem tra Backend (Cong 8000)...
netstat -ano | findstr :8000 >nul 2>nul
if %ERRORLEVEL%==0 (
    echo  -^> Backend FastApi da hoat dong san.
) else (
    echo  -^> Dang bat Backend trong cua so moi...
    :: Goi activate venv neu can, roi mo run.py
    start "WIKI-AI Backend" cmd /k "cd backend && if exist venv\Scripts\activate (call venv\Scripts\activate) && python run.py"
)

echo.
echo [2/3] Kiem tra Frontend (Cong 5173)...
netstat -ano | findstr :5173 >nul 2>nul
if %ERRORLEVEL%==0 (
    echo  -^> Frontend React da hoat dong san.
) else (
    echo  -^> Dang bat Frontend trong cua so moi...
    start "WIKI-AI Frontend" cmd /k "cd frontend && npm run dev"
)

echo.
echo [3/3] Cho he thong san sang va mo trinh duyet...
:: Doi khoang 5 giay de chac chan frontend da len
timeout /t 5 >nul
start http://localhost:5173

echo.
echo ========================================================
echo ✅ HOAN TAT! Ban co the bat dau chat voi WIKI-AI.
echo Chu y: Dong cua so nay khong lam tat cac server. 
echo De tat server, hay tat 2 cua so den (Backend ^& Frontend) biet lap.
echo ========================================================
pause
