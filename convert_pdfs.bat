@echo off
chcp 65001 > nul
echo ============================================================
echo 📅 PDF → Calendar 변환기
echo ============================================================
echo.
python pdf_to_calendar.py
echo.
echo 완료! 아무 키나 누르면 종료됩니다.
pause
