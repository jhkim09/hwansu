# 🚀 지금 바로 Render 배포하기!

레포지토리가 준비되었으니 바로 배포해봅시다!

## Step 1: Git에 코드 푸시 (5분)

현재 폴더: `C:\Users\newsh\test-project\hwansu`

### 1-1. Git 초기화

```bash
cd C:\Users\newsh\test-project\hwansu

# Git 초기화
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: PDF to Calendar API for Make.com"
```

### 1-2. GitHub에 푸시

```bash
# 레포지토리 연결
git remote add origin https://github.com/jhkim09/hwansu.git

# 브랜치 이름을 main으로 변경
git branch -M main

# 푸시!
git push -u origin main
```

**GitHub 로그인**이 필요할 수 있습니다:
- Username: `jhkim09`
- Password: Personal Access Token (GitHub Settings → Developer settings → Personal access tokens)

---

## Step 2: Render.com 배포 (3분)

### 2-1. Render 가입/로그인

https://dashboard.render.com 접속

- GitHub 계정으로 가입하면 더 편합니다!

### 2-2. New Web Service 생성

1. 우측 상단 **"New +"** 버튼 클릭
2. **"Web Service"** 선택

### 2-3. GitHub 저장소 연결

1. **"Connect a repository"** 섹션에서
2. GitHub 계정 인증 (처음 한 번만)
3. `jhkim09/hwansu` 저장소 찾기
4. **"Connect"** 클릭

### 2-4. 설정 확인

Render가 `render.yaml`을 자동으로 감지합니다!

다음 내용이 자동으로 채워져 있는지 확인:

```
Name: pdf-to-calendar-api (원하는 이름으로 변경 가능)
Region: Singapore
Branch: main
Runtime: Python 3

Build Command: pip install -r requirements.txt
Start Command: uvicorn webhook_server:app --host 0.0.0.0 --port $PORT

Instance Type: Free
```

### 2-5. 배포 시작!

**"Create Web Service"** 클릭

배포 시작! (약 2-3분 소요)

---

## Step 3: 배포 완료 확인

### 3-1. 배포 로그 확인

Render 대시보드에서 로그를 볼 수 있습니다:

```
==> Installing dependencies
==> Running 'pip install -r requirements.txt'
Successfully installed fastapi uvicorn pdfplumber...
==> Build successful!
==> Starting service...
🚀 PDF to Calendar API 서버 시작
==> Your service is live 🎉
```

### 3-2. URL 확인

배포가 완료되면 URL이 표시됩니다:

```
https://pdf-to-calendar-api.onrender.com
```

또는 설정한 이름에 따라:
```
https://your-service-name.onrender.com
```

**이 URL을 복사하세요!** Make.com에서 사용할 거예요.

---

## Step 4: API 테스트

### 4-1. 헬스 체크

브라우저에서 접속:
```
https://your-service-name.onrender.com/health
```

응답이 나오면 성공:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-28T..."
}
```

### 4-2. API 문서 확인

```
https://your-service-name.onrender.com/docs
```

Swagger UI가 열리면 완벽! 🎉

### 4-3. PDF 업로드 테스트

Swagger UI에서:

1. **POST /webhook/pdf-upload** 클릭
2. **Try it out** 클릭
3. **Choose File** → PDF 파일 선택
4. **Execute** 클릭

응답에서 이벤트 목록이 나오면 성공!

```json
{
  "success": true,
  "events": [
    {
      "date": "2025-10-01",
      "summary": "[All Round Rival Match] ⚠️ 환수",
      ...
    }
  ],
  "total_events": 9,
  "message": "✅ ...에서 9개의 이벤트를 추출했습니다."
}
```

---

## Step 5: Make.com에서 사용

### 5-1. Make.com 시나리오 열기

기존에 만든 시나리오 또는 새 시나리오

### 5-2. HTTP 모듈 URL 업데이트

**기존 (ngrok)**:
```
https://abc123.ngrok.io/webhook/pdf-base64
```

**변경 후 (Render)**:
```
https://your-service-name.onrender.com/webhook/pdf-base64
```

### 5-3. 시나리오 저장 및 활성화

**Save** → **ON**

---

## Step 6: 최종 테스트! 🎉

1. Google Drive의 지정된 폴더에 PDF 업로드
2. Make.com History 확인
3. Google Calendar 확인

**자동으로 일정이 추가되었나요? 성공! 🎊**

---

## ⚠️ 중요: 첫 요청은 느릴 수 있어요

Render 무료 플랜은 15분 미사용 시 Sleep 모드로 들어갑니다.

**첫 요청 시**:
- Cold start로 30초~1분 정도 걸릴 수 있음
- 이후 요청은 빠름!

**해결 방법**:
- `RENDER_DEPLOY.md`의 "Sleep 방지" 섹션 참고
- UptimeRobot으로 5분마다 Ping 설정

---

## 🔄 코드 업데이트 시

코드를 수정한 후:

```bash
git add .
git commit -m "Update: 기능 추가"
git push
```

Render가 자동으로 감지하고 재배포합니다!

---

## 📋 체크리스트

- [ ] Git 초기화 및 푸시 완료
- [ ] Render.com 가입 완료
- [ ] Web Service 생성 완료
- [ ] 배포 성공 (로그 확인)
- [ ] `/health` 접속 성공
- [ ] `/docs` 접속 성공
- [ ] Swagger UI에서 PDF 테스트 성공
- [ ] Make.com URL 업데이트 완료
- [ ] Google Drive PDF 업로드 테스트 성공
- [ ] Google Calendar에 이벤트 추가 확인

**모두 체크되었나요? 축하합니다! 완전 자동화 완성! 🚀**

---

## 🆘 문제 발생 시

### Git 푸시 실패
```bash
# GitHub Personal Access Token 필요
# GitHub → Settings → Developer settings → Personal access tokens → Generate
# repo 권한 체크
# Token을 비밀번호로 사용
```

### Render 빌드 실패
- **RENDER_DEPLOY.md**의 "문제 해결" 섹션 참고
- Render 대시보드의 로그 확인

### Make.com 연결 실패
- URL 확인 (`https://`로 시작하는지)
- `/webhook/pdf-base64` 경로 확인
- Render 서비스가 실행 중인지 확인

---

## 🎉 다음 단계

배포가 완료되었다면:

1. ✅ `MAKE_SCENARIO_GUIDE.md` 읽어보기
2. ✅ UptimeRobot 설정 (Sleep 방지)
3. ✅ 실제 PDF 업로드 시작!

---

**배포 성공을 축하합니다! 🎊**

이제 PDF 업로드만 하면 자동으로 캘린더에 추가됩니다!
