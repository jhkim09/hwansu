# 🛠️ Windows에서 make 사용하기

Windows에서는 기본적으로 `make`가 설치되어 있지 않습니다. 여러 방법이 있습니다:

## 방법 1: Chocolatey 사용 (추천)

### 1. Chocolatey 설치 (관리자 권한 PowerShell)
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### 2. make 설치
```powershell
choco install make
```

### 3. 사용
```bash
make install
make run
```

---

## 방법 2: Git Bash 사용 (Git이 이미 설치되어 있다면)

Git Bash에는 make가 포함되어 있습니다.

### 1. Git Bash 열기
- 폴더에서 우클릭 → "Git Bash Here"

### 2. 사용
```bash
make install
make run
```

---

## 방법 3: WSL (Windows Subsystem for Linux) 사용

### 1. WSL 설치 (관리자 권한 PowerShell)
```powershell
wsl --install
```

### 2. Ubuntu에서 make 사용
```bash
make install
make run
```

---

## 방법 4: make 없이 사용 (가장 간단!)

### Windows 배치 파일 사용

`make`가 없어도 동일한 기능을 하는 배치 파일을 만들었습니다:

#### setup.bat (라이브러리 설치)
```batch
@echo off
echo 📦 라이브러리 설치 중...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo ✅ 설치 완료!
pause
```

#### run.bat (PDF 변환 실행)
```batch
@echo off
echo 🚀 PDF 변환 시작...
python pdf_to_calendar.py
echo ✅ 완료!
pause
```

#### clean.bat (.ics 파일 삭제)
```batch
@echo off
echo 🧹 .ics 파일 삭제 중...
del /Q *.ics 2>nul
echo ✅ 삭제 완료!
pause
```

그냥 배치 파일을 더블클릭하면 됩니다!

---

## 권장 사항

### 🥇 처음 사용하시는 경우
→ **방법 4: 배치 파일 사용** (별도 설치 불필요)

### 🥈 Git을 사용하시는 경우
→ **방법 2: Git Bash 사용** (이미 make가 포함되어 있음)

### 🥉 개발 환경을 자주 사용하시는 경우
→ **방법 1: Chocolatey 사용** (다른 도구도 쉽게 설치 가능)

---

## 빠른 비교표

| 방법 | 설치 필요 | 난이도 | 추천 대상 |
|------|-----------|--------|-----------|
| 배치 파일 | ❌ 없음 | ⭐ 쉬움 | 처음 사용자 |
| Git Bash | ✅ Git만 | ⭐⭐ 보통 | Git 사용자 |
| Chocolatey | ✅ Chocolatey | ⭐⭐ 보통 | 개발자 |
| WSL | ✅ WSL | ⭐⭐⭐ 어려움 | Linux 선호자 |

---

## make 명령어 vs 배치 파일

| make 명령어 | 배치 파일 | 설명 |
|-------------|-----------|------|
| `make install` | `setup.bat` | 라이브러리 설치 |
| `make run` | `run.bat` | PDF 변환 실행 |
| `make clean` | `clean.bat` | .ics 파일 삭제 |
| `make check` | `check.bat` | 환경 체크 |

---

## 💡 결론

**make가 없어도 괜찮습니다!**

이미 제공된 파일들로 충분히 사용 가능합니다:
- `convert_pdfs.bat` - PDF 변환
- `convert_pdf_drag.bat` - 드래그앤드롭 변환

이 파일들을 더블클릭하기만 하면 됩니다!
