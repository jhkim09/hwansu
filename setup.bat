@echo off
chcp 65001 > nul
echo ============================================================
echo 📦 라이브러리 설치
echo ============================================================
echo.
echo Python 버전 확인 중...
python --version
echo.
echo pip 업그레이드 중...
python -m pip install --upgrade pip
echo.
echo 필요한 라이브러리 설치 중...
python -m pip install -r requirements.txt
echo.
echo ============================================================
echo ✅ 설치 완료!
echo ============================================================
echo.
echo 이제 'run.bat' 또는 'convert_pdfs.bat'를 실행하세요!
echo.
pause
