# 📅 PDF → Calendar 자동 변환기

MetLife 캠페인 시행문 PDF에서 정산/환수 일정을 자동으로 추출하여 캘린더 파일(.ics)로 변환합니다.

## ✨ 특징

- 🎯 **유연한 날짜 인식**: PDF 구조가 바뀌어도 날짜 패턴으로 자동 인식
- 📊 **지능적 분류**: "지급", "환수", "정산" 등 키워드로 이벤트 분류
- 🔔 **알림 자동 설정**:
  - 환수: 14일 전, 7일 전, 1일 전 알림
  - 지급: 3일 전, 1일 전 알림
- 📱 **범용 포맷**: Google Calendar, Outlook, Apple Calendar 등 모든 캘린더 앱 지원

## 🚀 설치 방법

### 1. Python 설치 확인

```bash
python --version
```

Python이 없다면 [Python 공식 사이트](https://www.python.org/downloads/)에서 설치하세요.

### 2. 필요한 라이브러리 설치

**방법 A: 배치 파일 사용 (Windows, 가장 쉬움!)**
```bash
setup.bat 더블클릭
```

**방법 B: make 사용 (make가 설치되어 있다면)**
```bash
make install
```

**방법 C: 직접 설치**
```bash
pip install -r requirements.txt
```

또는 개별 설치:
```bash
pip install pdfplumber icalendar
```

> 💡 **Windows에서 make 사용하기**: `SETUP.md` 파일을 참고하세요!

## 📖 사용 방법

### 🥇 추천: 배치 파일 사용 (Windows)

**모든 PDF 변환**
```bash
run.bat 더블클릭
```
또는
```bash
convert_pdfs.bat 더블클릭
```

**특정 PDF 변환 (드래그앤드롭)**
```bash
PDF 파일을 convert_pdf_drag.bat 위에 드래그앤드롭
```

**환경 체크**
```bash
check.bat 더블클릭
```

**생성된 .ics 파일 삭제**
```bash
clean.bat 더블클릭
```

---

### 🥈 make 사용 (make가 설치되어 있다면)

```bash
make install   # 라이브러리 설치
make run       # PDF 변환 실행
make check     # 환경 체크
make clean     # .ics 파일 삭제
make help      # 도움말
```

---

### 🥉 Python 직접 실행

**방법 1: 폴더의 모든 PDF 처리**

PDF 파일과 같은 폴더에서 실행:

```bash
python pdf_to_calendar.py
```

**방법 2: 특정 PDF 파일 처리**

```bash
python pdf_to_calendar.py "CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.pdf"
```

## 📝 실행 예시

```bash
C:\Users\newsh\test-project\hwansu> python pdf_to_calendar.py

============================================================
📅 PDF → Calendar 변환기
============================================================

📄 PDF 파일 분석 중: CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.pdf
✅ 45개의 날짜를 발견했습니다.
  📅 2025.10.01: [All Round Rival Match] ⚠️ 환수
  📅 2025.11.07: [MPC Reaction Point] 📝 반영, ⏰ 마감
  📅 2025.12.31: [With U Dollar] 💰 지급
  📅 2026.10.15: [New Frontier 3300] 💰 지급
  📅 2026.12.15: [New Frontier 3300] ⚠️ 환수, 1차 ⚠️ 환수
  📅 2027.03.31: [Champions League] ✅ 확정, 🎫 참가

✅ 캘린더 파일 생성 완료: CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.ics
📱 이 파일을 더블클릭하면 캘린더 앱에서 자동으로 열립니다.

============================================================
🎉 완료! 1개의 캘린더 파일이 생성되었습니다.
============================================================

📱 다음 파일들을 캘린더에 추가하세요:
  • CA채널_2025년_Classic_CA_7_ways_2MSR_캠페인_시행문_20251001.ics

💡 Tip: 파일을 더블클릭하면 Google Calendar, Outlook 등에서 자동으로 열립니다!
```

## 📥 캘린더에 추가하기

### Google Calendar

1. 생성된 `.ics` 파일을 더블클릭
2. 또는 Google Calendar 웹사이트 → 설정 → 가져오기 및 내보내기 → 파일 선택

### Outlook

1. `.ics` 파일을 더블클릭
2. 또는 Outlook → 파일 → 열기 및 내보내기 → 가져오기/내보내기

### Apple Calendar (macOS/iOS)

1. `.ics` 파일을 더블클릭
2. "캘린더에 추가" 선택

## 🔍 인식되는 이벤트 유형

스크립트는 다음 키워드를 자동으로 인식합니다:

| 키워드 | 아이콘 | 알림 설정 |
|--------|--------|-----------|
| 지급 | 💰 | 3일 전, 1일 전 |
| 환수 | ⚠️ | 14일 전, 7일 전, 1일 전 |
| 정산 | 📊 | 7일 전, 1일 전 |
| 행사 | 🎉 | 7일 전, 1일 전 |
| 초대 | ✈️ | 7일 전, 1일 전 |
| 확정 | ✅ | 1일 전 |
| 마감 | ⏰ | 3일 전, 1일 전 |
| 반영 | 📝 | 1일 전 |
| 달성 | 🎯 | 1일 전 |
| 참가 | 🎫 | 7일 전, 1일 전 |

## 🛠️ 문제 해결

### Q: "pdfplumber 라이브러리가 필요합니다" 오류

```bash
pip install pdfplumber
```

### Q: "icalendar 라이브러리가 필요합니다" 오류

```bash
pip install icalendar
```

### Q: 날짜가 제대로 추출되지 않아요

- PDF 파일을 직접 열어서 "정산 및 환수 일정" 표가 있는지 확인
- 날짜 형식이 `YYYY.MM` 또는 `YYYY.MM.DD` 형식인지 확인
- 이슈가 있다면 PDF 파일과 함께 제보해주세요

### Q: 중복된 이벤트가 생성돼요

스크립트는 자동으로 중복을 제거하지만, 만약 여러 PDF를 처리했다면 각 PDF마다 별도의 .ics 파일이 생성됩니다. 필요없는 파일은 삭제하세요.

## 💡 팁

### 1. 자동 실행 배치 파일 만들기

`convert_pdfs.bat` 파일 생성:

```batch
@echo off
echo PDF 변환 시작...
python pdf_to_calendar.py
echo.
echo 완료! 아무 키나 누르면 종료됩니다.
pause
```

이제 PDF를 받으면 `convert_pdfs.bat`를 더블클릭만 하면 됩니다!

### 2. 폴더 드래그앤드롭

`convert_pdf_drag.bat` 파일 생성:

```batch
@echo off
python pdf_to_calendar.py %1
pause
```

이제 PDF 파일을 배치 파일 위에 드래그앤드롭하면 변환됩니다!

### 3. 월별로 정리하기

```bash
mkdir calendar_files
move *.ics calendar_files/
```

## 📁 파일 구조

```
hwansu/
├── pdf_to_calendar.py          # 메인 Python 스크립트
├── requirements.txt             # 필요한 라이브러리 목록
├── README.md                    # 📖 사용 가이드 (이 파일)
├── SETUP.md                     # 🛠️ Windows에서 make 사용하기
├── Makefile                     # make 명령어 정의
│
├── 🚀 실행 파일 (배치 파일)
├── setup.bat                    # 라이브러리 설치
├── run.bat                      # PDF 변환 실행
├── check.bat                    # 환경 체크
├── clean.bat                    # .ics 파일 삭제
├── convert_pdfs.bat             # 모든 PDF 변환 (run.bat과 동일)
├── convert_pdf_drag.bat         # 드래그앤드롭 변환
│
├── 📄 입력/출력 파일
├── CA채널_2025년_*.pdf         # 입력 PDF 파일
└── CA채널_2025년_*.ics         # 출력 캘린더 파일
```

## 🎯 어떤 파일을 실행해야 하나요?

| 목적 | 배치 파일 | make 명령 |
|------|-----------|-----------|
| 처음 설치 | `setup.bat` | `make install` |
| PDF 변환 | `run.bat` 또는 `convert_pdfs.bat` | `make run` |
| 환경 확인 | `check.bat` | `make check` |
| 파일 삭제 | `clean.bat` | `make clean` |
| 드래그앤드롭 | `convert_pdf_drag.bat` | - |

## 🔄 업데이트 내역

### v1.0.0 (2025-10-28)
- 초기 버전 릴리스
- PDF에서 날짜 자동 추출
- .ics 캘린더 파일 생성
- 키워드 기반 이벤트 분류
- 자동 알림 설정

## 📞 문의

문제가 있거나 개선 사항이 있다면 이슈를 남겨주세요!

---

**만든이**: Claude Code
**라이선스**: MIT
