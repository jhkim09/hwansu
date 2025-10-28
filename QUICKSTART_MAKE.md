# ⚡ 빠른 시작 가이드 (Make.com)

5분 안에 자동화 설정 완료하기!

## 🎯 목표

PDF 업로드 → 자동으로 Google Calendar에 일정 추가

## 📋 체크리스트

- [ ] Python 설치됨
- [ ] Google Drive 계정 있음
- [ ] Google Calendar 사용 중
- [ ] Make.com 계정 있음 (없으면 [무료 가입](https://www.make.com/en/register))

---

## Step 1: 라이브러리 설치 (1분)

```bash
pip install -r requirements.txt
```

또는 배치 파일:
```bash
setup.bat 더블클릭
```

---

## Step 2: API 서버 실행 (1분)

### 터미널 1: API 서버

```bash
python webhook_server.py
```

또는 배치 파일:
```bash
start_server.bat 더블클릭
```

서버가 실행되면:
```
🚀 PDF to Calendar API 서버 시작
📡 서버 주소: http://localhost:8000
```

### 터미널 2: ngrok (외부 접근용)

**1. ngrok 다운로드**
- https://ngrok.com/download

**2. 실행**
```bash
ngrok http 8000
```

**3. URL 복사**
```
Forwarding: https://abc123.ngrok.io -> http://localhost:8000
           ^^^^^^^^^^^^^^^^^^^^
           이 URL 복사!
```

---

## Step 3: Make.com 설정 (3분)

### 1. 새 시나리오 생성

https://www.make.com/en/scenarios 접속

→ **Create a new scenario** 클릭

### 2. 모듈 추가

#### Module 1: Google Drive - Watch Files
```
Folder: PDF를 업로드할 폴더 선택
File extension filter: pdf
Limit: 1
```

#### Module 2: Google Drive - Download a File
```
File ID: {{1.id}}
```

#### Module 3: HTTP - Make a Request
```
URL: https://YOUR-NGROK-URL.ngrok.io/webhook/pdf-base64
Method: POST
Headers:
  Content-Type: application/json
Body type: Raw
Request content:
  {
    "data": "{{base64(2.data)}}",
    "filename": "{{1.name}}"
  }
Parse response: ✓
```

#### Module 4: Iterator
```
Array: {{3.events}}
```

#### Module 5: Google Calendar - Create an Event
```
Calendar ID: primary
Event name: {{4.summary}}
All day event: ✓
Start date: {{4.date}}
End date: {{4.date}}
Description: {{4.description}}
```

### 3. 시나리오 저장 및 활성화

우측 상단 → **Save** → **ON**

---

## Step 4: 테스트 (30초)

1. Google Drive의 설정한 폴더에 PDF 업로드
2. Make.com → History에서 실행 확인
3. Google Calendar 확인!

---

## ✅ 완료!

이제 PDF를 업로드하기만 하면 자동으로 캘린더에 추가됩니다!

---

## 🐛 문제 해결

### "Connection refused"
→ API 서버와 ngrok이 모두 실행 중인지 확인

### "Invalid PDF"
→ PDF 파일이 정상인지 확인

### 이벤트가 생성되지 않음
→ Make.com History에서 오류 확인
→ http://localhost:8000/docs 에서 API 직접 테스트

---

## 📚 더 알아보기

- 상세 가이드: `MAKE_SCENARIO_GUIDE.md`
- 배포 방법: `DEPLOYMENT.md` (곧 추가 예정)
- API 문서: http://localhost:8000/docs

---

## 💡 팁

### 1. ngrok 없이 사용하기

Render.com, Railway 등에 배포하면 ngrok 없이 사용 가능!

### 2. 테스트용 엔드포인트

http://localhost:8000/docs 에서:
- `POST /webhook/pdf-upload` - 직접 PDF 업로드
- 파일 선택 → Execute → 결과 확인

### 3. 알림 설정

Google Calendar 모듈의 Reminders 설정:
```
Use default reminders: No
Overrides:
  - Method: popup
    Minutes before: {{first(4.alerts) * 24 * 60}}
```

---

**문제가 있나요?** Issues에 문의하세요!
