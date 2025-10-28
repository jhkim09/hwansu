# 📅 PDF to Google Calendar - Make.com 자동화

MetLife 캠페인 시행문 PDF를 Google Drive에 업로드하면 자동으로 Google Calendar에 일정이 추가됩니다!

## ⚡ 빠른 시작

### 1️⃣ 로컬 사용 (배치 파일)

월에 한두 번 수동으로 실행:

```bash
setup.bat         # 처음 한 번만
run.bat           # PDF 변환
```

생성된 `.ics` 파일을 Google Calendar에 임포트

**👉 가이드**: `README.md` 참고

---

### 2️⃣ Make.com 자동화 (추천!)

PDF 업로드하면 자동으로 캘린더에 추가:

```
Google Drive 업로드 → Make.com → Google Calendar
```

**👉 가이드**: `QUICKSTART_MAKE.md` 참고 (5분 설정)

---

## 🎯 어떤 방식이 좋을까요?

| 기준 | 로컬 사용 | Make.com 자동화 |
|------|-----------|-----------------|
| 설정 시간 | 1분 | 5분 |
| 사용 방법 | 배치 파일 실행 | 자동 (PDF 업로드만) |
| 비용 | 무료 | 무료 (월 1,000회) |
| 추천 대상 | 가끔 사용 | 자주 사용 |

---

## 📁 프로젝트 구조

```
hwansu/
├── 📖 로컬 사용 (배치 파일)
│   ├── pdf_to_calendar.py       # PDF → .ics 변환
│   ├── setup.bat                 # 설치
│   ├── run.bat                   # 실행
│   └── README.md                 # 상세 가이드
│
├── 🤖 Make.com 자동화
│   ├── webhook_server.py         # API 서버
│   ├── start_server.bat          # 서버 실행
│   ├── QUICKSTART_MAKE.md        # 5분 시작 가이드
│   ├── MAKE_SCENARIO_GUIDE.md    # 상세 가이드
│   └── make-scenario-template.json  # 시나리오 템플릿
│
└── 📄 공통
    ├── requirements.txt          # 라이브러리
    └── SETUP.md                  # Windows make 설치
```

---

## 🚀 시작하기

### 옵션 A: 로컬 사용 (간단!)

```bash
# 1. 설치
setup.bat

# 2. PDF 변환
run.bat

# 3. .ics 파일 더블클릭 → 캘린더에 추가
```

### 옵션 B: Make.com 자동화 (자동!)

```bash
# 1. 라이브러리 설치
pip install -r requirements.txt

# 2. API 서버 실행
python webhook_server.py

# 3. ngrok 실행 (새 터미널)
ngrok http 8000

# 4. Make.com 설정
QUICKSTART_MAKE.md 참고
```

---

## 📚 문서

### 로컬 사용
- 📖 **README.md** - 배치 파일 사용 가이드
- 🛠️ **SETUP.md** - Windows make 설치

### Make.com 자동화
- ⚡ **QUICKSTART_MAKE.md** - 5분 빠른 시작
- 📘 **MAKE_SCENARIO_GUIDE.md** - 상세 설정 가이드
- 🔧 **API 문서** - http://localhost:8000/docs

---

## ✨ 주요 기능

### 공통
- 🎯 유연한 날짜 인식 (PDF 구조 변경에 강함)
- 📊 키워드 기반 이벤트 분류
- 🔔 자동 알림 설정
  - 환수: 14일, 7일, 1일 전
  - 지급: 3일, 1일 전

### 로컬 전용
- 💾 .ics 파일 생성
- 📱 모든 캘린더 앱 호환

### Make.com 전용
- 🤖 완전 자동화
- 🔄 Google Drive 감시
- ☁️ 클라우드 실행

---

## 🎬 데모

### 로컬 사용

```bash
C:\hwansu> run.bat

📄 PDF 파일 분석 중: CA채널_2025년_Classic_CA.pdf
✅ 9개의 날짜를 발견했습니다.
  📅 2025.10.01: [All Round Rival Match] ⚠️ 환수
  📅 2025.12.31: [With U Dollar] 💰 지급

✅ 캘린더 파일 생성 완료: CA채널_2025년_Classic_CA.ics
```

### Make.com 자동화

```
1. PDF 업로드 → Google Drive
2. Make.com 자동 실행
3. 9개 이벤트 → Google Calendar 추가 완료!
```

---

## 💰 비용

### 로컬 사용
- **무료** (Python만 있으면 OK)

### Make.com 자동화
- **무료 플랜**: 월 1,000회 실행 (충분!)
- **서버 호스팅**:
  - Render.com 무료 플랜 사용 가능
  - 또는 로컬에서 ngrok 사용 (무료)

---

## 🤔 FAQ

### Q: 둘 다 사용 가능한가요?
A: 네! 로컬로 테스트하고 Make.com으로 자동화 가능합니다.

### Q: Make.com 없이 자동화 가능한가요?
A: Zapier, n8n 등 다른 플랫폼도 가능합니다. (API 서버 동일)

### Q: PDF 구조가 바뀌면?
A: 유연한 패턴 인식으로 대부분 작동합니다. 안 되면 이슈 남겨주세요!

### Q: Google Drive 대신 다른 저장소?
A: Make.com에서 Dropbox, OneDrive 등으로 변경 가능!

---

## 🔐 보안

- PDF는 처리 후 즉시 삭제
- 외부 전송 없음 (Make.com 경유만)
- Google OAuth로 안전한 인증

---

## 🛠️ 기술 스택

- **Python 3.8+**
- **FastAPI** - API 서버
- **pdfplumber** - PDF 파싱
- **Make.com** - 워크플로우 자동화
- **Google APIs** - Drive, Calendar

---

## 📞 문의

- 🐛 버그 리포트: Issues
- 💡 기능 제안: Issues
- ❓ 사용 질문: Discussions

---

## 📄 라이선스

MIT License

---

**⭐ 도움이 되셨다면 Star 부탁드립니다!**
