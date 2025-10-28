# 🔌 API 사용 예제

webhook_server.py API 서버의 사용 예제입니다.

## 📡 서버 실행

```bash
python webhook_server.py
```

서버 주소: `http://localhost:8000`

API 문서: `http://localhost:8000/docs` (Swagger UI)

---

## 🧪 테스트 방법

### 1. 웹 브라우저에서 테스트 (가장 쉬움!)

```
http://localhost:8000/docs 접속
→ POST /webhook/pdf-upload 선택
→ Try it out 클릭
→ 파일 선택
→ Execute 클릭
```

### 2. curl 명령어 (터미널)

Windows PowerShell에서:

```powershell
# 파일 업로드
curl -X POST "http://localhost:8000/webhook/pdf-upload" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.pdf"
```

Mac/Linux에서:

```bash
# 파일 업로드
curl -X POST "http://localhost:8000/webhook/pdf-upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.pdf"
```

### 3. Python requests

```python
import requests

url = "http://localhost:8000/webhook/pdf-upload"
files = {'file': open('CA채널_2025년_Classic_CA.pdf', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

### 4. Make.com HTTP 모듈

```json
{
  "url": "https://your-server.com/webhook/pdf-base64",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "data": "{{base64(previousModule.data)}}",
    "filename": "document.pdf"
  }
}
```

---

## 📥 예제 응답

### 성공 응답

```json
{
  "success": true,
  "events": [
    {
      "date": "2025-10-01",
      "summary": "[All Round Rival Match] ⚠️ 환수",
      "description": "...2025. 9-10월 (각 월) Summer 기간 동안의 CMIP를 업적순으로 등위를 매겨 1:1 Match...",
      "category": "환수",
      "alerts": [14, 7, 1]
    },
    {
      "date": "2025-11-07",
      "summary": "[MPC Reaction Point] 📝 반영, ⏰ 마감",
      "description": "...2025. 10월 EP로 청약 시 CMIP X 200%를 MPC Point에 가산...",
      "category": "마감",
      "alerts": [1]
    },
    {
      "date": "2025-12-31",
      "summary": "[With U Dollar] 💰 지급",
      "description": "...MIP X 100% 현금시상 (간편포함) 단, 13차월 지급...",
      "category": "지급",
      "alerts": [3, 1]
    },
    {
      "date": "2026-10-15",
      "summary": "[New Frontier 3300] 💰 지급",
      "description": "...Recruiting 인원에 따른 현금 시상 정산 시점 (2026.10) 잔존 위촉 인원 기준 시상금 확정...",
      "category": "지급",
      "alerts": [3, 1]
    },
    {
      "date": "2026-12-15",
      "summary": "[New Frontier 3300] 1차 ⚠️ 환수",
      "description": "...환수 발생 시 수당공제로 우선 충당하며, 부족 시 별도 청구...",
      "category": "환수",
      "alerts": [14, 7, 1]
    },
    {
      "date": "2027-03-31",
      "summary": "[Champions League] ✅ 확정, 🎫 참가",
      "description": "...2025년 달성인원을 대상으로 2027년 3월 유지율 재 평가하여 80% 이상 시 참가 확정...",
      "category": "행사",
      "alerts": [7, 1]
    }
  ],
  "total_events": 9,
  "message": "✅ CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.pdf에서 9개의 이벤트를 추출했습니다."
}
```

### 오류 응답

```json
{
  "detail": "PDF 처리 중 오류 발생: Invalid PDF file"
}
```

---

## 🔍 응답 필드 설명

### CalendarEvent 객체

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `date` | string | 이벤트 날짜 (YYYY-MM-DD) | "2025-10-01" |
| `summary` | string | 이벤트 제목 | "[All Round Rival Match] ⚠️ 환수" |
| `description` | string | 이벤트 설명 (PDF에서 추출한 컨텍스트) | "...업적순으로 등위를 매겨..." |
| `category` | string | 이벤트 카테고리 | "환수", "지급", "정산", "행사" 등 |
| `alerts` | array | 알림 일수 배열 (일 단위) | [14, 7, 1] = 14일 전, 7일 전, 1일 전 |

### PDFProcessResponse 객체

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | boolean | 처리 성공 여부 |
| `events` | array | CalendarEvent 객체 배열 |
| `total_events` | integer | 추출된 이벤트 개수 |
| `message` | string | 처리 결과 메시지 |

---

## 🎯 엔드포인트 별 사용 시나리오

### 1. `/webhook/pdf-upload` - 직접 업로드

**사용 시나리오**: 테스트, 간단한 통합

```bash
# Postman, Swagger UI, curl 등으로 파일 직접 업로드
```

**장점**: 간단함
**단점**: Make.com에서 사용 어려움

---

### 2. `/webhook/pdf-url` - URL로 다운로드

**사용 시나리오**: Google Drive 공유 링크 사용

```json
{
  "url": "https://drive.google.com/uc?id=FILE_ID&export=download",
  "filename": "campaign.pdf"
}
```

**장점**: URL만 전달하면 됨
**단점**: 공개 URL 필요

---

### 3. `/webhook/pdf-base64` - Base64 인코딩

**사용 시나리오**: Make.com, Zapier 등 자동화 플랫폼 (추천!)

```json
{
  "data": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PAovQ3...",
  "filename": "campaign.pdf"
}
```

**장점**: 파일 내용을 직접 전송, 공유 링크 불필요
**단점**: Base64 인코딩 필요 (Make.com은 자동)

---

## 🔐 보안 고려사항

### 1. API 키 인증 추가 (선택)

현재는 누구나 접근 가능합니다. 프로덕션 환경에서는 인증 추가를 권장:

```python
# webhook_server.py에 추가
from fastapi import Header, HTTPException

@app.post("/webhook/pdf-upload")
async def process_pdf_from_upload(
    file: UploadFile = File(...),
    x_api_key: str = Header(...)
):
    if x_api_key != "your-secret-key":
        raise HTTPException(401, "Unauthorized")
    # ...
```

### 2. Rate Limiting

많은 요청을 방지:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/webhook/pdf-upload")
@limiter.limit("5/minute")
async def process_pdf_from_upload(...):
    # ...
```

### 3. 파일 크기 제한

```python
from fastapi import UploadFile, File, HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/webhook/pdf-upload")
async def process_pdf_from_upload(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")
    # ...
```

---

## 📊 모니터링

### 로그 확인

서버 실행 시 자동으로 로그가 출력됩니다:

```
INFO:     127.0.0.1:50234 - "POST /webhook/pdf-upload HTTP/1.1" 200 OK
```

### 헬스 체크

```bash
curl http://localhost:8000/health
```

응답:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-28T15:30:00.123456"
}
```

---

## 🚀 배포 후 URL

배포 후에는 ngrok URL 대신 실제 URL을 사용:

```
# Render.com
https://your-app.onrender.com/webhook/pdf-base64

# Railway
https://your-app.up.railway.app/webhook/pdf-base64

# Fly.io
https://your-app.fly.dev/webhook/pdf-base64
```

---

**더 자세한 내용은 API 문서를 참고하세요:** http://localhost:8000/docs
