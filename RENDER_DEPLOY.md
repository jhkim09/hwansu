# 🚀 Render.com 배포 가이드

ngrok 없이 Render.com에 배포하여 고정 URL 사용하기!

## ✨ Render.com의 장점

- ✅ **완전 무료** (월 750시간)
- ✅ **고정 URL** (예: `https://your-app.onrender.com`)
- ✅ **HTTPS 자동** (보안 인증서 자동)
- ✅ **자동 배포** (GitHub 푸시하면 자동 배포)
- ✅ **쉬운 설정** (클릭 몇 번이면 끝)

### 무료 플랜 제한사항

- ⚠️ **15분 미사용 시 Sleep** (다음 요청 시 ~30초 걸림)
- ⚠️ **월 750시간 제한** (하루 24시간 × 31일 = 충분함!)
- ⚠️ **매월 15일 서비스 일시 정지** (1분 정도)

**Make.com 자동화엔 완벽합니다!** (PDF 업로드 빈도가 낮으니까)

---

## 📋 준비사항

- [x] GitHub 계정 (없으면 [가입](https://github.com/join))
- [x] Render.com 계정 (없으면 [가입](https://dashboard.render.com/register))
- [x] 이 프로젝트 파일들

---

## 🎯 배포 방법 (2가지 중 선택)

### 방법 1: GitHub 연동 (추천, 자동 배포!)

Git 사용 경험이 있다면 이 방법 추천!

### 방법 2: 수동 배포

Git 모르면 이 방법도 가능!

---

## 방법 1: GitHub 연동 배포 (추천)

### Step 1: GitHub 저장소 생성

**1-1. GitHub에서 새 저장소 생성**

https://github.com/new 접속

```
Repository name: pdf-to-calendar
Description: PDF에서 정산/환수 일정을 추출하여 Google Calendar로 변환
Public 또는 Private 선택
```

**Create repository** 클릭

**1-2. 로컬 Git 초기화 및 푸시**

```bash
# hwansu 폴더에서
cd C:\Users\newsh\test-project\hwansu

# Git 초기화 (처음 한 번만)
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: PDF to Calendar API"

# GitHub 저장소 연결 (YOUR-USERNAME을 본인 계정으로 변경)
git remote add origin https://github.com/YOUR-USERNAME/pdf-to-calendar.git

# 푸시
git branch -M main
git push -u origin main
```

---

### Step 2: Render.com에서 배포

**2-1. Render 대시보드 접속**

https://dashboard.render.com

**2-2. New Web Service 생성**

1. 우측 상단 **"New +"** 클릭
2. **"Web Service"** 선택

**2-3. GitHub 저장소 연결**

- **"Connect a repository"** 클릭
- GitHub 계정 인증 (처음 한 번만)
- 방금 만든 저장소 선택: `pdf-to-calendar`
- **"Connect"** 클릭

**2-4. 설정 입력**

자동으로 `render.yaml`을 감지하여 설정이 채워집니다!

확인 및 수정:

```
Name: pdf-to-calendar-api (원하는 이름)
Region: Singapore (한국과 가까움)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn webhook_server:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

**2-5. 배포 시작**

**"Create Web Service"** 클릭

배포 시작! (약 2-3분 소요)

**2-6. 배포 완료 확인**

로그에서 다음 메시지가 보이면 성공:

```
==> Your service is live 🎉
https://pdf-to-calendar-api.onrender.com
```

---

### Step 3: API 테스트

**3-1. 헬스 체크**

브라우저에서 접속:
```
https://your-app-name.onrender.com/health
```

응답:
```json
{"status": "healthy", "timestamp": "..."}
```

**3-2. API 문서 확인**

```
https://your-app-name.onrender.com/docs
```

Swagger UI가 열리면 성공!

**3-3. PDF 업로드 테스트**

Swagger UI에서:
1. `POST /webhook/pdf-upload` 선택
2. **Try it out** 클릭
3. PDF 파일 선택
4. **Execute** 클릭
5. 응답 확인!

---

### Step 4: Make.com에서 사용

Make.com HTTP 모듈 설정:

```
URL: https://your-app-name.onrender.com/webhook/pdf-base64
Method: POST
Headers:
  Content-Type: application/json
Body:
  {
    "data": "{{base64(2.data)}}",
    "filename": "{{1.name}}"
  }
```

**ngrok URL 대신 이 고정 URL을 사용하세요!**

---

## 방법 2: 수동 배포 (GitHub 없이)

Git을 사용하지 않는 경우:

### Step 1: Render CLI 설치

```bash
# Windows (PowerShell)
iwr https://render.com/cli/install.ps1 -useb | iex

# Mac/Linux
curl -fsSL https://render.com/install.sh | sh
```

### Step 2: Render CLI로 배포

```bash
cd C:\Users\newsh\test-project\hwansu

# Render 로그인
render login

# 배포
render deploy
```

---

## 🔄 자동 배포 설정 (GitHub 연동 시)

GitHub에 푸시하면 자동으로 Render에 배포됩니다!

```bash
# 코드 수정 후
git add .
git commit -m "Update: ..."
git push

# Render가 자동으로 감지하고 재배포!
```

Render 대시보드에서 배포 진행 상황 확인 가능!

---

## ⚙️ 환경 변수 설정 (선택)

Render 대시보드 → 서비스 선택 → **Environment**

필요한 경우 추가:

```
API_KEY=your-secret-key
MAX_FILE_SIZE=10485760
```

webhook_server.py에서 사용:

```python
import os
API_KEY = os.getenv('API_KEY')
```

---

## 📊 모니터링

### 로그 확인

Render 대시보드 → 서비스 선택 → **Logs**

실시간 로그 확인 가능!

### 사용량 확인

Render 대시보드 → 서비스 선택 → **Metrics**

- CPU 사용량
- 메모리 사용량
- 요청 수

### Sleep 방지 (선택)

무료 플랜은 15분 미사용 시 Sleep됩니다.

**방법 1: UptimeRobot 사용**

1. https://uptimerobot.com 가입 (무료)
2. Add New Monitor
3. Monitor Type: HTTP(s)
4. URL: `https://your-app.onrender.com/health`
5. Monitoring Interval: 5분

→ 5분마다 자동으로 요청하여 Sleep 방지!

**방법 2: Make.com으로 Ping**

Make.com에서 5분마다 `/health` 엔드포인트 호출하는 시나리오 생성

---

## 🔧 문제 해결

### Q: "Build failed" 오류

**원인**: requirements.txt 문제

**해결**:
```bash
# 로컬에서 테스트
pip install -r requirements.txt

# 문제 없으면 다시 푸시
git add requirements.txt
git commit -m "Fix requirements"
git push
```

### Q: "Application failed to respond" 오류

**원인**: PORT 환경변수 사용 안 함

**해결**: webhook_server.py 마지막 부분 확인
```python
# ❌ 잘못된 예
uvicorn.run(app, host="0.0.0.0", port=8000)

# ✅ 올바른 예
import os
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Q: Cold start가 너무 느려요

**원인**: 무료 플랜의 Sleep 기능

**해결**:
1. UptimeRobot으로 Sleep 방지 (위 참고)
2. 또는 Starter 플랜 사용 ($7/월, Sleep 없음)

### Q: "Out of hours" 오류

**원인**: 월 750시간 초과 (거의 불가능)

**해결**: 다음 달까지 대기 또는 Starter 플랜 업그레이드

---

## 💰 비용

### Free 플랜
- **가격**: $0
- **시간**: 750시간/월
- **메모리**: 512MB
- **Sleep**: 15분 후 자동
- **추천**: 테스트 및 저빈도 사용

### Starter 플랜
- **가격**: $7/월
- **시간**: 무제한
- **메모리**: 512MB
- **Sleep**: 없음
- **추천**: 실제 사용 (항상 켜져 있어야 할 때)

**Make.com 자동화는 Free 플랜으로 충분합니다!**

---

## 🎉 배포 완료 체크리스트

- [ ] Render.com 배포 성공
- [ ] `/health` 엔드포인트 작동 확인
- [ ] `/docs` API 문서 접속 확인
- [ ] Swagger UI에서 PDF 업로드 테스트 성공
- [ ] Make.com에서 Render URL 업데이트
- [ ] Make.com 시나리오 테스트 성공
- [ ] (선택) UptimeRobot 설정으로 Sleep 방지

---

## 🚀 다음 단계

1. ✅ Render 배포 완료
2. ✅ Make.com 시나리오에서 URL 변경
3. ✅ Google Drive에 PDF 업로드 테스트
4. ✅ Google Calendar 확인
5. ✅ 자동화 완성! 🎊

---

## 🔗 유용한 링크

- Render 대시보드: https://dashboard.render.com
- Render 문서: https://render.com/docs
- Render 상태: https://status.render.com
- UptimeRobot: https://uptimerobot.com

---

**배포 성공하셨나요? 축하합니다! 🎉**

이제 PDF를 Google Drive에 업로드하기만 하면 자동으로 캘린더에 추가됩니다!
