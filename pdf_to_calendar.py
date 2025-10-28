#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF에서 정산/환수 일정을 추출하여 .ics 캘린더 파일로 변환하는 스크립트

사용법:
    python pdf_to_calendar.py <PDF파일경로>

    또는 폴더의 모든 PDF 처리:
    python pdf_to_calendar.py
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Dict

try:
    import pdfplumber
except ImportError:
    print("pdfplumber 라이브러리가 필요합니다. 설치: pip install pdfplumber")
    sys.exit(1)

try:
    from icalendar import Calendar, Event
except ImportError:
    print("icalendar 라이브러리가 필요합니다. 설치: pip install icalendar")
    sys.exit(1)


class PDFCalendarExtractor:
    """PDF에서 캘린더 이벤트를 추출하는 클래스"""

    # 날짜 패턴들
    DATE_PATTERNS = [
        # 2026.10, 2025.12 형식
        r'(\d{4})\.(\d{1,2})',
        # 2026.10.15, 2025.12.31 형식
        r'(\d{4})\.(\d{1,2})\.(\d{1,2})',
        # 2026년 10월 형식
        r'(\d{4})년\s*(\d{1,2})월',
        # 2026-10-15 형식
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
    ]

    # 이벤트 키워드
    EVENT_KEYWORDS = {
        '지급': '💰',
        '환수': '⚠️',
        '정산': '📊',
        '행사': '🎉',
        '초대': '✈️',
        '확정': '✅',
        '마감': '⏰',
        '반영': '📝',
        '달성': '🎯',
        '참가': '🎫',
    }

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.events: List[Dict] = []

    def extract_text(self) -> str:
        """PDF에서 텍스트 추출"""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def extract_schedule_table(self) -> List[Dict]:
        """정산/환수 테이블을 직접 파싱하여 이벤트 추출"""
        events = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                # 테이블 추출
                tables = page.extract_tables()

                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    # 헤더 행에서 컬럼 찾기
                    header = [str(cell).strip() if cell else "" for cell in table[0]]

                    # 정산/환수 테이블인지 확인
                    header_text = " ".join(header).lower()
                    if not ("캠페인" in header_text or "산출" in header_text or "환수" in header_text):
                        continue

                    # 컬럼 인덱스 찾기
                    campaign_idx = None
                    calculation_idx = None
                    payment_idx = None
                    recovery_idx = None

                    for idx, h in enumerate(header):
                        h_lower = h.lower()
                        if "캠페인" in h_lower:
                            campaign_idx = idx
                        elif "산출" in h_lower:
                            calculation_idx = idx
                        elif "지급" in h_lower or "행사" in h_lower:
                            payment_idx = idx
                        elif "환수" in h_lower:
                            recovery_idx = idx

                    # 데이터 행 파싱
                    for row in table[1:]:
                        if not row or len(row) == 0:
                            continue

                        # 캠페인명 추출
                        campaign_name = None
                        if campaign_idx is not None and campaign_idx < len(row):
                            campaign_name = str(row[campaign_idx]).strip() if row[campaign_idx] else None

                        if not campaign_name or campaign_name == "":
                            continue

                        # 1. 산출 날짜
                        if calculation_idx is not None and calculation_idx < len(row):
                            calc_cell = str(row[calculation_idx]).strip() if row[calculation_idx] else ""
                            dates = self.parse_dates_from_text(calc_cell)
                            for date_obj in dates:
                                events.append({
                                    'date': date_obj,
                                    'summary': f"[{campaign_name}] 📊 산출",
                                    'description': f"{campaign_name} 캠페인 최종 산출",
                                    'type': '산출'
                                })

                        # 2. 지급/행사 날짜
                        if payment_idx is not None and payment_idx < len(row):
                            pay_cell = str(row[payment_idx]).strip() if row[payment_idx] else ""
                            dates = self.parse_dates_from_text(pay_cell)

                            # 지급인지 행사인지 판단
                            if "행사" in pay_cell or "초대" in pay_cell:
                                emoji = "🎉"
                                type_name = "행사"
                            else:
                                emoji = "💰"
                                type_name = "지급"

                            for date_obj in dates:
                                events.append({
                                    'date': date_obj,
                                    'summary': f"[{campaign_name}] {emoji} {type_name}",
                                    'description': f"{campaign_name} 캠페인 {type_name}",
                                    'type': type_name
                                })

                        # 3. 환수 날짜
                        if recovery_idx is not None and recovery_idx < len(row):
                            recovery_cell = str(row[recovery_idx]).strip() if row[recovery_idx] else ""

                            # "1차", "2차" 구분
                            rounds = re.findall(r'(\d+)차[:\s]*([0-9.년월\s]+)', recovery_cell)
                            if rounds:
                                for round_num, date_text in rounds:
                                    dates = self.parse_dates_from_text(date_text)
                                    for date_obj in dates:
                                        events.append({
                                            'date': date_obj,
                                            'summary': f"[{campaign_name}] ⚠️ {round_num}차 환수",
                                            'description': f"{campaign_name} 캠페인 {round_num}차 환수",
                                            'type': '환수'
                                        })
                            else:
                                # 차수 없는 일반 환수
                                dates = self.parse_dates_from_text(recovery_cell)
                                for date_obj in dates:
                                    events.append({
                                        'date': date_obj,
                                        'summary': f"[{campaign_name}] ⚠️ 환수",
                                        'description': f"{campaign_name} 캠페인 환수",
                                        'type': '환수'
                                    })

        return events

    def parse_dates_from_text(self, text: str) -> List[datetime]:
        """텍스트에서 날짜 파싱"""
        dates = []

        for pattern in self.DATE_PATTERNS:
            for match in re.finditer(pattern, text):
                groups = match.groups()
                year = int(groups[0])
                month = int(groups[1])
                day = int(groups[2]) if len(groups) > 2 else 1

                try:
                    date_obj = datetime(year, month, day)
                    dates.append(date_obj)
                except ValueError:
                    continue

        return dates

    def extract_schedule_section(self, text: str) -> str:
        """정산 및 환수 일정 섹션만 추출"""
        # 섹션 시작 패턴들
        section_start_patterns = [
            r'정산\s*및\s*환수\s*일정',
            r'정산/환수\s*일정',
            r'\[정산/환수\s*기준\]',
            r'정산.*환수.*기준',
        ]

        # 섹션 시작 위치 찾기
        start_pos = None
        for pattern in section_start_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start_pos = match.start()
                break

        if start_pos is None:
            # 섹션을 못 찾았으면 전체 텍스트 반환 (기존 동작 유지)
            return text

        # 섹션 끝 패턴들 (다음 주요 섹션 또는 페이지 구분)
        section_end_patterns = [
            r'\n\s*\[.*?\]\s*\n',  # 다음 대괄호 섹션
            r'\n\s*\d+\.\s+[가-힣A-Za-z]',  # 다음 번호 매겨진 섹션 (예: 1. 캠페인)
            r'\n\s*■\s*',  # 다음 항목 마커
            r'\n\s*※\s*',  # 주의사항
            r'\[업적환수\]',  # 업적환수 섹션
        ]

        # 시작 위치 이후에서 끝 위치 찾기
        end_pos = len(text)
        search_start = start_pos + 100  # 시작점에서 100자 이후부터 끝 찾기

        for pattern in section_end_patterns:
            match = re.search(pattern, text[search_start:])
            if match:
                candidate_end = search_start + match.start()
                if candidate_end < end_pos:
                    end_pos = candidate_end

        # 섹션 텍스트 추출 (최소 200자는 확보)
        if end_pos - start_pos < 200:
            end_pos = min(start_pos + 1000, len(text))

        section_text = text[start_pos:end_pos]
        return section_text

    def find_dates_with_context(self, text: str) -> List[Tuple[datetime, str, int]]:
        """텍스트에서 날짜와 주변 컨텍스트 찾기

        Returns:
            List of (date, context_text, position)
        """
        dates_found = []

        for pattern in self.DATE_PATTERNS:
            for match in re.finditer(pattern, text):
                # 날짜 파싱
                groups = match.groups()
                year = int(groups[0])
                month = int(groups[1])
                day = int(groups[2]) if len(groups) > 2 else 1

                try:
                    date_obj = datetime(year, month, day)
                except ValueError:
                    continue

                # 날짜 주변 100자 추출 (앞 50자, 뒤 50자)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].replace('\n', ' ').strip()

                dates_found.append((date_obj, context, match.start()))

        # 날짜 순으로 정렬
        dates_found.sort(key=lambda x: x[0])
        return dates_found

    def extract_event_name(self, context: str, date_str: str) -> str:
        """컨텍스트에서 이벤트 이름 추출"""
        # 잘 알려진 캠페인명 패턴 (우선순위 순)
        known_campaigns = [
            r'All\s+Round\s+Rival\s+(?:Agent|Match)',
            r'New\s+Frontier\s+\d+',
            r'Champions?\s+League',
            r'MPC\s+Reaction\s+Point',
            r'With\s+U\s+Dollar',
            r'도전!\s*달러벨',
            r'BQR\s*\([^)]+\)',
        ]

        campaign_name = None

        # 1. 잘 알려진 캠페인명 먼저 찾기
        for pattern in known_campaigns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                campaign_name = match.group(0).strip()
                break

        # 2. 일반적인 캠페인명 패턴
        if not campaign_name:
            campaign_patterns = [
                r'([가-힣A-Za-z0-9\s]+)\s*캠페인',
                r'([가-힣A-Za-z0-9\s]+)\s*Campaign',
                # 대문자로 시작하는 연속된 영단어 (최소 2단어)
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+(?:\s+\d+)?)\b',
            ]

            for pattern in campaign_patterns:
                match = re.search(pattern, context)
                if match:
                    candidate = match.group(1).strip()
                    # 너무 짧거나 일반적인 단어는 제외
                    if len(candidate) > 3 and candidate not in ['Business Quality Review']:
                        campaign_name = candidate
                        break

        # 3. 캠페인명을 못 찾았으면 기본값
        if not campaign_name:
            campaign_name = "MetLife 캠페인"

        # 이벤트 타입 추출 (지급, 환수 등)
        event_types = []
        for keyword, emoji in self.EVENT_KEYWORDS.items():
            if keyword in context:
                event_types.append(f"{emoji} {keyword}")

        if event_types:
            event_type = ", ".join(event_types)
        else:
            event_type = "일정"

        # 차수 정보 추출 (1차, 2차 등)
        round_match = re.search(r'(\d+)차', context)
        if round_match:
            event_type = f"{round_match.group(1)}차 {event_type}"

        return f"[{campaign_name}] {event_type}"

    def extract_events(self) -> List[Dict]:
        """PDF에서 모든 이벤트 추출"""
        print(f"📄 PDF 파일 분석 중: {self.pdf_path.name}")

        # 방법 1: 테이블 구조 파싱 (우선)
        print(f"📊 정산/환수 테이블 파싱 시도...")
        table_events = self.extract_schedule_table()

        if table_events:
            print(f"✅ 테이블에서 {len(table_events)}개의 이벤트를 추출했습니다.")

            # 이벤트 출력
            for event in table_events:
                date_str = event['date'].strftime('%Y.%m.%d')
                print(f"  📅 {date_str}: {event['summary']}")

            return table_events

        # 방법 2: 텍스트 기반 파싱 (폴백)
        print(f"⚠️  테이블을 찾을 수 없어 텍스트 기반 파싱으로 전환...")

        # 전체 텍스트 추출
        full_text = self.extract_text()

        # 정산 및 환수 일정 섹션만 추출
        text = self.extract_schedule_section(full_text)
        print(f"📑 정산/환수 일정 섹션 추출 완료 ({len(text)}자)")

        dates_with_context = self.find_dates_with_context(text)

        print(f"✅ {len(dates_with_context)}개의 날짜를 발견했습니다.")

        events = []
        for date_obj, context, pos in dates_with_context:
            # 정산/환수 관련 날짜만 필터링
            if not any(keyword in context for keyword in self.EVENT_KEYWORDS.keys()):
                continue

            date_str = date_obj.strftime('%Y.%m.%d')
            event_name = self.extract_event_name(context, date_str)

            # 중복 제거 (같은 날짜, 같은 이름)
            if any(e['date'] == date_obj and e['summary'] == event_name for e in events):
                continue

            events.append({
                'date': date_obj,
                'summary': event_name,
                'description': context[:200],  # 설명에 컨텍스트 포함
            })

            print(f"  📅 {date_str}: {event_name}")

        return events

    def create_ics_file(self, events: List[Dict], output_path: str = None) -> str:
        """이벤트를 .ics 파일로 저장"""
        if not events:
            print("⚠️  추출된 이벤트가 없습니다.")
            return None

        # 출력 경로 설정
        if output_path is None:
            output_path = self.pdf_path.with_suffix('.ics')

        # 캘린더 생성
        cal = Calendar()
        cal.add('prodid', '-//PDF to Calendar//hwansu//KR')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('x-wr-calname', 'MetLife 정산/환수 일정')
        cal.add('x-wr-timezone', 'Asia/Seoul')

        # 이벤트 추가
        for event_data in events:
            event = Event()
            event.add('summary', event_data['summary'])
            event.add('dtstart', event_data['date'].date())
            event.add('dtend', (event_data['date'] + timedelta(days=1)).date())
            event.add('description', event_data['description'])
            event.add('dtstamp', datetime.now())

            # 알림 설정 (7일 전, 1일 전)
            if '환수' in event_data['summary']:
                # 환수는 14일 전, 7일 전, 1일 전 알림
                from icalendar import Alarm

                for days in [14, 7, 1]:
                    alarm = Alarm()
                    alarm.add('action', 'DISPLAY')
                    alarm.add('trigger', timedelta(days=-days))
                    alarm.add('description', f"{event_data['summary']} - {days}일 전 알림")
                    event.add_component(alarm)
            elif '지급' in event_data['summary']:
                # 지급은 3일 전, 1일 전 알림
                from icalendar import Alarm

                for days in [3, 1]:
                    alarm = Alarm()
                    alarm.add('action', 'DISPLAY')
                    alarm.add('trigger', timedelta(days=-days))
                    alarm.add('description', f"{event_data['summary']} - {days}일 전 알림")
                    event.add_component(alarm)

            cal.add_component(event)

        # 파일 저장
        with open(output_path, 'wb') as f:
            f.write(cal.to_ical())

        print(f"\n✅ 캘린더 파일 생성 완료: {output_path}")
        print(f"📱 이 파일을 더블클릭하면 캘린더 앱에서 자동으로 열립니다.")

        return str(output_path)


def process_pdf(pdf_path: str) -> str:
    """PDF 파일 하나를 처리"""
    extractor = PDFCalendarExtractor(pdf_path)
    events = extractor.extract_events()

    if events:
        return extractor.create_ics_file(events)
    return None


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("📅 PDF → Calendar 변환기")
    print("=" * 60)
    print()

    # 명령행 인자 처리
    if len(sys.argv) > 1:
        pdf_files = [Path(sys.argv[1])]
    else:
        # 현재 폴더의 모든 PDF 파일 처리
        current_dir = Path.cwd()
        pdf_files = list(current_dir.glob("*.pdf"))

        if not pdf_files:
            print("❌ PDF 파일을 찾을 수 없습니다.")
            print("\n사용법:")
            print("  1. 이 스크립트를 PDF 파일이 있는 폴더에 넣고 실행")
            print("  2. 또는: python pdf_to_calendar.py <PDF파일경로>")
            return

    # PDF 파일 처리
    ics_files = []
    for pdf_file in pdf_files:
        if not pdf_file.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {pdf_file}")
            continue

        print()
        ics_file = process_pdf(str(pdf_file))
        if ics_file:
            ics_files.append(ics_file)

    # 결과 요약
    print("\n" + "=" * 60)
    print(f"🎉 완료! {len(ics_files)}개의 캘린더 파일이 생성되었습니다.")
    print("=" * 60)

    if ics_files:
        print("\n📱 다음 파일들을 캘린더에 추가하세요:")
        for ics_file in ics_files:
            print(f"  • {ics_file}")
        print("\n💡 Tip: 파일을 더블클릭하면 Google Calendar, Outlook 등에서 자동으로 열립니다!")


if __name__ == "__main__":
    main()
