@echo off
chcp 65001 > nul
echo ============================================================
echo 🔍 환경 체크
echo ============================================================
echo.

echo [1] Python 버전:
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되어 있지 않습니다!
    echo    https://www.python.org/downloads/ 에서 설치하세요.
) else (
    echo ✅ Python 설치됨
)
echo.

echo [2] 필요한 라이브러리:
python -m pip list 2>nul | findstr "pdfplumber" >nul
if %errorlevel% equ 0 (
    echo ✅ pdfplumber 설치됨
) else (
    echo ❌ pdfplumber 미설치
    echo    setup.bat을 실행하세요!
)

python -m pip list 2>nul | findstr "icalendar" >nul
if %errorlevel% equ 0 (
    echo ✅ icalendar 설치됨
) else (
    echo ❌ icalendar 미설치
    echo    setup.bat을 실행하세요!
)
echo.

echo [3] PDF 파일 목록:
dir /B *.pdf 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  PDF 파일이 없습니다.
) else (
    echo ✅ PDF 파일 발견
)
echo.

echo [4] 생성된 .ics 파일:
dir /B *.ics 2>nul
if %errorlevel% neq 0 (
    echo ℹ️  아직 생성된 .ics 파일이 없습니다.
) else (
    echo ✅ .ics 파일 발견
)
echo.

echo ============================================================
echo ✅ 체크 완료!
echo ============================================================
echo.
pause
