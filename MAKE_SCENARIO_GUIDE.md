# 🤖 Make.com 자동화 시나리오 가이드

Google Drive에 PDF 업로드 → 자동으로 날짜 추출 → Google Calendar에 이벤트 추가

## 📋 목차

1. [준비사항](#준비사항)
2. [API 서버 실행](#api-서버-실행)
3. [Make.com 시나리오 구성](#makecom-시나리오-구성)
4. [테스트](#테스트)
5. [배포 옵션](#배포-옵션)

---

## 준비사항

### 1. 필요한 계정

- ✅ **Google 계정** (Drive, Calendar 사용)
- ✅ **Make.com 계정** (무료 플랜 가능)
- ✅ **Python 3.8+** (로컬 또는 서버)

### 2. 라이브러리 설치

```bash
pip install -r requirements.txt
```

설치되는 것:
- `fastapi` - API 서버
- `uvicorn` - ASGI 서버
- `pdfplumber` - PDF 파싱
- `icalendar` - 캘린더 처리
- `requests` - HTTP 요청

---

## API 서버 실행

### 방법 1: 로컬에서 실행 (테스트용)

```bash
python webhook_server.py
```

실행되면:
```
🚀 PDF to Calendar API 서버 시작
📡 서버 주소: http://localhost:8000
📚 API 문서: http://localhost:8000/docs
```

**중요**: 로컬에서 실행 시 Make.com이 접근할 수 없습니다!
→ ngrok 또는 배포 필요 (아래 참고)

### 방법 2: ngrok으로 외부 접근 가능하게 만들기

**1. ngrok 설치**
- https://ngrok.com/download 에서 다운로드
- 또는 `choco install ngrok` (Chocolatey)

**2. 서버 실행**
```bash
# 터미널 1
python webhook_server.py
```

**3. ngrok 실행**
```bash
# 터미널 2
ngrok http 8000
```

**4. ngrok URL 복사**
```
Forwarding: https://abc123.ngrok.io -> http://localhost:8000
```

→ 이 URL(`https://abc123.ngrok.io`)을 Make.com에서 사용!

---

## Make.com 시나리오 구성

### 전체 흐름

```
1. Google Drive: Watch Files (PDF 업로드 감지)
2. Google Drive: Download a File (PDF 다운로드)
3. HTTP: Make a Request (API 서버로 PDF 전송)
4. Iterator (이벤트 목록 순회)
5. Google Calendar: Create an Event (각 이벤트 생성)
```

---

### Step 1: Google Drive - Watch Files

**목적**: 특정 폴더에 PDF가 업로드되면 자동 감지

**설정**:
1. Make.com에서 새 시나리오 생성
2. Google Drive 모듈 선택 → "Watch Files"
3. Google 계정 연결
4. **Folder**: PDF를 업로드할 폴더 선택 (예: `/MetLife 캠페인/`)
5. **File extension filter**: `pdf` 입력
6. **Limit**: 1 (한 번에 하나씩 처리)

---

### Step 2: Google Drive - Download a File

**목적**: 감지된 PDF 파일 다운로드

**설정**:
1. 모듈 추가 → Google Drive → "Download a File"
2. **File ID**: `{{1.id}}` (이전 모듈에서 받은 파일 ID)

---

### Step 3: HTTP - Make a Request

**목적**: API 서버로 PDF 전송하여 이벤트 추출

**설정**:
1. 모듈 추가 → HTTP → "Make a Request"

**URL**:
```
https://your-ngrok-url.ngrok.io/webhook/pdf-base64
```
또는 배포한 서버 URL

**Method**: `POST`

**Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Body type**: `Raw`

**Request content**:
```json
{
  "data": "{{base64(2.data)}}",
  "filename": "{{1.name}}"
}
```

**Parse response**: ✅ Yes

---

### Step 4: Iterator

**목적**: API에서 받은 이벤트 목록을 하나씩 순회

**설정**:
1. 모듈 추가 → Flow Control → "Iterator"
2. **Array**: `{{3.events}}` (HTTP 응답의 events 배열)

---

### Step 5: Google Calendar - Create an Event

**목적**: 각 이벤트를 Google Calendar에 추가

**설정**:
1. 모듈 추가 → Google Calendar → "Create an Event"
2. Google 계정 연결

**Calendar ID**: 본인의 캘린더 ID (기본: `primary`)

**Event name**: `{{4.summary}}`

**Start date**: `{{4.date}}`

**End date**: `{{4.date}}`

**All day event**: ✅ Yes

**Description**:
```
{{4.description}}

카테고리: {{4.category}}
```

**Reminders** (선택사항):
- 이벤트 알림을 수동으로 설정하거나
- Advanced Settings → Reminders 에서 설정

---

### Step 6: 오류 처리 (선택사항)

**오류 핸들러 추가**:

1. HTTP 모듈 우클릭 → "Add error handler"
2. Error handler 선택 → "Break"
3. 또는 Slack/이메일 알림 모듈 추가

---

## 테스트

### 1. 시나리오 활성화

Make.com에서 시나리오를 "ON"으로 전환

### 2. PDF 업로드

설정한 Google Drive 폴더에 PDF 업로드:
```
/MetLife 캠페인/CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문.pdf
```

### 3. 실행 확인

- Make.com → History에서 실행 기록 확인
- Google Calendar에서 이벤트 추가 확인

### 4. 예상 결과

```
✅ 9개의 이벤트가 Google Calendar에 추가됨:
  📅 2025-10-01: [All Round Rival Match] ⚠️ 환수
  📅 2025-12-31: [With U Dollar] 💰 지급
  📅 2026-10-15: [New Frontier 3300] 💰 지급
  ...
```

---

## 배포 옵션

로컬 실행은 테스트용입니다. 실제 사용을 위해서는 배포가 필요합니다.

### 옵션 1: Render.com (무료, 추천)

**장점**: 무료 플랜, 자동 배포, HTTPS 제공

**단계**:
1. https://render.com 가입
2. New → Web Service
3. GitHub 연결 또는 Docker 배포
4. Environment: Python
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn webhook_server:app --host 0.0.0.0 --port $PORT`
7. 배포 완료 후 URL 복사 (예: `https://your-app.onrender.com`)

### 옵션 2: Railway.app (무료)

**장점**: 간단한 배포, 무료 $5 크레딧

**단계**:
1. https://railway.app 가입
2. New Project → Deploy from GitHub
3. 자동으로 Python 감지 및 배포

### 옵션 3: Fly.io (무료)

**장점**: 글로벌 엣지 배포

**단계**:
1. https://fly.io 가입
2. `flyctl launch` 명령어로 배포

### 옵션 4: Vercel (Serverless)

**장점**: Serverless, 자동 스케일링

**주의**: Serverless 환경에서는 PDF 처리가 무거울 수 있음

---

## 시나리오 JSON 템플릿

Make.com에서 직접 import 가능한 JSON 템플릿은 `make-scenario-template.json` 파일을 참고하세요.

**Import 방법**:
1. Make.com → Scenarios
2. 우측 상단 ... → Import Blueprint
3. `make-scenario-template.json` 파일 선택
4. 연결 재설정 (Google Drive, Calendar)
5. HTTP 모듈의 URL을 본인의 API 서버 URL로 변경

---

## 고급 설정

### 1. 필터 추가

특정 파일명 패턴만 처리:
- Google Drive 모듈 뒤에 Filter 추가
- Condition: `{{1.name}}` contains `시행문`

### 2. 중복 방지

같은 파일을 여러 번 처리하지 않도록:
- Data Store 모듈 사용
- 처리한 파일 ID 저장 후 체크

### 3. 알림 추가

처리 완료 시 Slack/이메일 알림:
- 마지막에 Slack 또는 Email 모듈 추가

### 4. 오류 로깅

오류 발생 시 Google Sheets에 기록:
- Error Handler → Google Sheets → Add a Row

---

## 문제 해결

### Q: "Connection refused" 오류

→ API 서버가 실행 중인지 확인
→ ngrok이 실행 중인지 확인

### Q: "Invalid PDF" 오류

→ PDF 파일이 정상인지 확인
→ 파일 크기 제한 확인 (Make.com 무료: 5MB)

### Q: 이벤트가 생성되지 않음

→ Make.com History에서 오류 메시지 확인
→ API 서버 로그 확인
→ Google Calendar 권한 확인

### Q: 날짜가 잘못 추출됨

→ PDF 형식 확인
→ "정산 및 환수 일정" 표가 있는지 확인
→ API 응답 확인 (`/docs`에서 테스트)

---

## 비용

### Make.com
- **Free**: 1,000 operations/month
- **Core**: $9/month, 10,000 operations
- **Pro**: $16/month, 10,000 operations + 고급 기능

### API 서버 호스팅
- **Render.com Free**: 무료 (sleep after 15min idle)
- **Render.com Starter**: $7/month (항상 실행)
- **Railway**: $5 무료 크레딧
- **Fly.io**: 무료 플랜

**권장**: Make.com Free + Render.com Free = $0/month

---

## 다음 단계

1. ✅ API 서버 실행 확인
2. ✅ ngrok 또는 배포
3. ✅ Make.com 시나리오 구성
4. ✅ 테스트 PDF 업로드
5. ✅ Google Calendar 확인
6. ✅ 실제 사용 시작!

---

**도움이 필요하면 Issues에 문의하세요!** 🚀
