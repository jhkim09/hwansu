@echo off
chcp 65001 > nul
echo ============================================================
echo 🚀 PDF to Calendar API 서버 시작
echo ============================================================
echo.
echo 필요한 라이브러리 확인 중...
python -m pip list | findstr "fastapi" >nul
if %errorlevel% neq 0 (
    echo ⚠️  fastapi가 설치되어 있지 않습니다.
    echo.
    echo 설치하시겠습니까? (Y/N)
    set /p install=">> "
    if /i "%install%"=="Y" (
        echo.
        echo 📦 라이브러리 설치 중...
        python -m pip install -r requirements.txt
    ) else (
        echo.
        echo ❌ 설치를 취소했습니다.
        pause
        exit /b
    )
)
echo.
echo ============================================================
echo 🌐 서버를 시작합니다...
echo ============================================================
echo.
echo 📡 서버 주소: http://localhost:8000
echo 📚 API 문서: http://localhost:8000/docs
echo.
echo 💡 Tip: Make.com에서 사용하려면 ngrok이 필요합니다!
echo     새 터미널에서 'ngrok http 8000' 실행
echo.
echo ============================================================
echo.
python webhook_server.py
pause
