@echo off
chcp 65001 > nul
echo ============================================================
echo 🧹 .ics 파일 삭제
echo ============================================================
echo.
echo 생성된 캘린더 파일(.ics) 삭제 중...
del /Q *.ics 2>nul
if %errorlevel% equ 0 (
    echo ✅ 삭제 완료!
) else (
    echo ℹ️  삭제할 .ics 파일이 없습니다.
)
echo.
pause
