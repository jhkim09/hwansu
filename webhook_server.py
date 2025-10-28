#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make.com용 웹훅 API 서버
PDF에서 정산/환수 일정을 추출하여 JSON으로 반환

사용법:
    python webhook_server.py

    또는 배포:
    uvicorn webhook_server:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import tempfile
import base64
import requests
from pathlib import Path
from datetime import datetime
import io

# PDF 처리를 위한 기존 클래스 임포트
import sys
sys.path.append(str(Path(__file__).parent))
from pdf_to_calendar import PDFCalendarExtractor

app = FastAPI(
    title="PDF to Calendar API",
    description="PDF에서 정산/환수 일정을 추출하여 Google Calendar용 이벤트로 변환",
    version="1.0.0"
)

# CORS 설정 (Make.com에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 모델
class PDFUrlRequest(BaseModel):
    """PDF URL로 처리하는 요청"""
    url: HttpUrl
    filename: Optional[str] = None


class PDFBase64Request(BaseModel):
    """Base64 인코딩된 PDF로 처리하는 요청"""
    data: str
    filename: Optional[str] = "document.pdf"


# 응답 모델
class CalendarEvent(BaseModel):
    """캘린더 이벤트"""
    date: str  # YYYY-MM-DD 형식
    summary: str
    description: str
    category: str  # "지급", "환수", "정산" 등
    alerts: List[int]  # 알림 일수 (예: [14, 7, 1])


class PDFProcessResponse(BaseModel):
    """PDF 처리 응답"""
    success: bool
    events: List[CalendarEvent]
    total_events: int
    message: str


@app.get("/")
async def root():
    """API 루트"""
    return {
        "service": "PDF to Calendar API",
        "version": "1.0.0",
        "endpoints": {
            "POST /webhook/pdf-url": "PDF URL로 이벤트 추출",
            "POST /webhook/pdf-base64": "Base64 PDF로 이벤트 추출",
            "POST /webhook/pdf-upload": "PDF 파일 업로드로 이벤트 추출",
            "GET /health": "헬스 체크"
        }
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


def determine_event_category(summary: str) -> str:
    """이벤트 제목에서 카테고리 추출"""
    if "환수" in summary:
        return "환수"
    elif "지급" in summary:
        return "지급"
    elif "정산" in summary:
        return "정산"
    elif "행사" in summary or "초대" in summary:
        return "행사"
    elif "마감" in summary or "반영" in summary:
        return "마감"
    else:
        return "일정"


def determine_alerts(category: str) -> List[int]:
    """카테고리에 따른 알림 일수 결정"""
    if category == "환수":
        return [14, 7, 1]  # 14일 전, 7일 전, 1일 전
    elif category == "지급":
        return [3, 1]  # 3일 전, 1일 전
    elif category == "행사":
        return [7, 1]  # 7일 전, 1일 전
    elif category == "산출":
        return [7, 3, 1]  # 7일 전, 3일 전, 1일 전
    else:
        return [1]  # 1일 전


def merge_events_by_date(events: List[CalendarEvent]) -> List[CalendarEvent]:
    """같은 날짜의 이벤트들을 하나로 병합"""
    from collections import defaultdict

    # 날짜별로 이벤트 그룹화
    events_by_date = defaultdict(list)
    for event in events:
        events_by_date[event.date].append(event)

    # 카테고리 우선순위 (높을수록 우선)
    category_priority = {
        "환수": 5,
        "지급": 4,
        "정산": 3,
        "행사": 2,
        "마감": 1,
        "일정": 0
    }

    merged_events = []
    for date, date_events in sorted(events_by_date.items()):
        if len(date_events) == 1:
            # 하나만 있으면 그대로 사용
            merged_events.append(date_events[0])
        else:
            # 여러 개 있으면 병합
            # 모든 고유한 캠페인명 추출
            campaign_names = set()
            for event in date_events:
                if ']' in event.summary:
                    campaign = event.summary.split(']')[0] + ']'
                    campaign_names.add(campaign)

            # 캠페인명이 여러 개면 모두 표시, 하나면 그것 사용
            if len(campaign_names) > 1:
                base_title = " & ".join(sorted(campaign_names))
            elif campaign_names:
                base_title = list(campaign_names)[0]
            else:
                base_title = "[MetLife 캠페인]"

            # 모든 고유한 이모지와 키워드 추출
            unique_parts = set()
            for event in date_events:
                # 대괄호 이후 부분을 쉼표로 분리
                if ']' in event.summary:
                    parts = event.summary.split(']', 1)[1].strip().split(',')
                    for part in parts:
                        unique_parts.add(part.strip())

            # 정렬하여 일관된 순서로 표시
            sorted_parts = sorted(unique_parts, key=lambda x: (
                # "1차", "2차" 등이 있으면 맨 앞으로
                not any(c in x for c in ['1차', '2차', '3차']),
                x
            ))

            merged_summary = f"{base_title} {', '.join(sorted_parts)}"

            # 가장 긴 설명 선택
            merged_description = max(date_events, key=lambda e: len(e.description)).description

            # 가장 우선순위 높은 카테고리 선택
            merged_category = max(date_events, key=lambda e: category_priority.get(e.category, 0)).category

            # 가장 긴 알림 목록 선택
            merged_alerts = max(date_events, key=lambda e: len(e.alerts)).alerts

            merged_events.append(CalendarEvent(
                date=date,
                summary=merged_summary,
                description=merged_description,
                category=merged_category,
                alerts=merged_alerts
            ))

    return merged_events


def process_pdf_bytes(pdf_bytes: bytes, filename: str) -> PDFProcessResponse:
    """PDF 바이트를 처리하여 이벤트 추출"""
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name

        # PDF 처리
        extractor = PDFCalendarExtractor(tmp_path)
        raw_events = extractor.extract_events()

        # 이벤트를 API 응답 형식으로 변환
        events = []
        for event in raw_events:
            summary = event['summary']

            # PDF에서 추출된 타입 정보 사용 (있으면)
            if 'type' in event:
                category = event['type']
            else:
                category = determine_event_category(summary)

            alerts = determine_alerts(category)

            events.append(CalendarEvent(
                date=event['date'].strftime('%Y-%m-%d'),
                summary=summary,
                description=event['description'],
                category=category,
                alerts=alerts
            ))

        # 병합하지 않음 - 각 타입(산출/지급/환수)을 명확하게 구분
        # events = merge_events_by_date(events)

        # 임시 파일 삭제
        Path(tmp_path).unlink()

        return PDFProcessResponse(
            success=True,
            events=events,
            total_events=len(events),
            message=f"✅ {filename}에서 {len(events)}개의 이벤트를 추출했습니다."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF 처리 중 오류 발생: {str(e)}"
        )


@app.post("/webhook/pdf-url", response_model=PDFProcessResponse)
async def process_pdf_from_url(request: PDFUrlRequest):
    """
    PDF URL로부터 이벤트 추출

    Make.com 시나리오에서 Google Drive 파일 URL을 전달받아 처리
    """
    try:
        # URL에서 PDF 다운로드
        response = requests.get(str(request.url), timeout=30)
        response.raise_for_status()

        filename = request.filename or "document.pdf"
        return process_pdf_bytes(response.content, filename)

    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"PDF 다운로드 실패: {str(e)}"
        )


@app.post("/webhook/pdf-base64", response_model=PDFProcessResponse)
async def process_pdf_from_base64(request: PDFBase64Request):
    """
    Base64 인코딩된 PDF로부터 이벤트 추출

    Make.com에서 파일을 Base64로 인코딩하여 전달받아 처리
    """
    try:
        # Base64 디코딩
        pdf_bytes = base64.b64decode(request.data)
        return process_pdf_bytes(pdf_bytes, request.filename)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Base64 디코딩 실패: {str(e)}"
        )


@app.post("/webhook/pdf-upload", response_model=PDFProcessResponse)
async def process_pdf_from_upload(file: UploadFile = File(...)):
    """
    PDF 파일 업로드로부터 이벤트 추출

    직접 파일을 업로드하여 처리
    """
    try:
        # 파일 확장자 체크
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="PDF 파일만 업로드 가능합니다."
            )

        # 파일 읽기
        pdf_bytes = await file.read()
        return process_pdf_bytes(pdf_bytes, file.filename)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"파일 처리 실패: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    import os

    # Render.com에서는 PORT 환경변수 사용
    port = int(os.getenv("PORT", 8000))

    print("=" * 60)
    print("🚀 PDF to Calendar API 서버 시작")
    print("=" * 60)
    print()
    print(f"📡 서버 주소: http://0.0.0.0:{port}")
    print(f"📚 API 문서: http://localhost:{port}/docs")
    print()
    print("💡 Make.com에서 사용할 웹훅 URL:")
    print(f"   - PDF URL: POST http://localhost:{port}/webhook/pdf-url")
    print(f"   - Base64:  POST http://localhost:{port}/webhook/pdf-base64")
    print(f"   - Upload:  POST http://localhost:{port}/webhook/pdf-upload")
    print()
    print("=" * 60)
    print()

    uvicorn.run(app, host="0.0.0.0", port=port)
