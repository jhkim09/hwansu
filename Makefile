.PHONY: help install run clean test

# 기본 타겟
.DEFAULT_GOAL := help

# Python 명령어 (Windows 호환)
PYTHON := python
PIP := $(PYTHON) -m pip

# 색상 코드 (Windows에서는 작동 안할 수 있음)
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m

help: ## 도움말 표시
	@echo "======================================================"
	@echo "  📅 PDF to Calendar - Makefile 명령어"
	@echo "======================================================"
	@echo ""
	@echo "사용 가능한 명령어:"
	@echo ""
	@echo "  make install    - 필요한 라이브러리 설치"
	@echo "  make run        - PDF 변환 실행 (모든 PDF)"
	@echo "  make test       - 테스트 실행"
	@echo "  make clean      - 생성된 .ics 파일 삭제"
	@echo "  make clean-all  - .ics 파일 + Python 캐시 삭제"
	@echo "  make check      - 환경 체크 (Python, 라이브러리)"
	@echo ""
	@echo "======================================================"

install: ## 필요한 라이브러리 설치
	@echo "📦 라이브러리 설치 중..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✅ 설치 완료!"

run: ## PDF 변환 실행
	@echo "🚀 PDF 변환 시작..."
	@$(PYTHON) pdf_to_calendar.py
	@echo ""
	@echo "✅ 완료!"

test: ## 현재 폴더의 첫 번째 PDF로 테스트
	@echo "🧪 테스트 실행 중..."
	@$(PYTHON) pdf_to_calendar.py

clean: ## 생성된 .ics 파일 삭제
	@echo "🧹 .ics 파일 삭제 중..."
	@if exist *.ics del /Q *.ics 2>nul || true
	@echo "✅ 삭제 완료!"

clean-all: clean ## .ics 파일 + Python 캐시 삭제
	@echo "🧹 Python 캐시 삭제 중..."
	@if exist __pycache__ rmdir /S /Q __pycache__ 2>nul || true
	@if exist *.pyc del /Q *.pyc 2>nul || true
	@echo "✅ 전체 삭제 완료!"

check: ## 환경 체크 (Python 버전, 라이브러리)
	@echo "🔍 환경 체크 중..."
	@echo ""
	@echo "Python 버전:"
	@$(PYTHON) --version
	@echo ""
	@echo "설치된 라이브러리:"
	@$(PIP) list | findstr "pdfplumber icalendar" || echo "  ⚠️  pdfplumber 또는 icalendar가 설치되지 않았습니다."
	@echo ""
	@echo "PDF 파일 목록:"
	@if exist *.pdf (dir /B *.pdf) else (echo "  ⚠️  PDF 파일이 없습니다.")
	@echo ""
	@echo "✅ 체크 완료!"

# 파일 이름으로 직접 실행
convert: run ## run의 별칭

setup: install ## install의 별칭
	@echo "💡 설치가 완료되었습니다. 'make run'으로 실행하세요!"
