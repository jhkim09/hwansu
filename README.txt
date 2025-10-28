📅 PDF to Google Calendar - 자동화 프로젝트
================================================

이 프로젝트는 MetLife 캠페인 시행문 PDF에서 정산/환수 일정을 자동으로 추출하여
Google Calendar에 추가하는 도구입니다.

🚀 빠른 시작 가이드
================================================

[옵션 1] 로컬에서 사용 (수동)
   1. setup.bat 실행 (처음 한 번)
   2. run.bat 실행 (PDF 변환)
   3. 생성된 .ics 파일을 Google Calendar에 임포트

   👉 상세 가이드: README.md

[옵션 2] Make.com 자동화 (추천!)
   1. DEPLOY_NOW.md 따라하기 (Render 배포)
   2. QUICKSTART_MAKE.md 따라하기 (Make.com 설정)
   3. PDF 업로드만 하면 자동으로 캘린더에 추가!

   👉 배포 가이드: DEPLOY_NOW.md
   👉 Make.com 가이드: QUICKSTART_MAKE.md

📁 주요 파일
================================================

[실행 파일]
- setup.bat              → 라이브러리 설치
- run.bat                → PDF 변환 실행
- start_server.bat       → API 서버 실행

[가이드 문서]
- README.md              → 로컬 사용 상세 가이드
- DEPLOY_NOW.md          → Render 배포 빠른 가이드 ⭐
- QUICKSTART_MAKE.md     → Make.com 5분 시작 가이드 ⭐
- MAKE_SCENARIO_GUIDE.md → Make.com 상세 가이드
- RENDER_DEPLOY.md       → Render 배포 상세 가이드

[핵심 코드]
- pdf_to_calendar.py     → PDF → .ics 변환
- webhook_server.py      → Make.com용 API 서버

💡 시작하기
================================================

[처음 사용하시나요?]
→ DEPLOY_NOW.md 파일을 열어보세요! (Render 배포 + Make.com 설정)

[로컬만 사용하시나요?]
→ README.md 파일을 열어보세요! (배치 파일 사용)

🔗 GitHub 레포지토리
================================================
https://github.com/jhkim09/hwansu

📞 문의
================================================
Issues: https://github.com/jhkim09/hwansu/issues

🎉 즐거운 자동화 되세요!
