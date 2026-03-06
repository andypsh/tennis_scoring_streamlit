import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_module

# --- 1. UI 설정 및 커스텀 CSS (정적) --- ㅡㅡ^
st.markdown("""
    <style>
        /* 스티커 메모 컨테이너 */
        .sticky-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        /* 개별 스티커 메모 스타일 */
        .sticky-note {
            background-color: #FFFD75;
            width: 130px;
            height: 130px;
            padding: 15px;
            box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-bottom-right-radius: 40px 5px;
            position: relative;
        }

        .sticky-note::before {
            content: "";
            position: absolute;
            top: 8px;
            width: 12px;
            height: 12px;
            background-color: rgba(255,0,0,0.4);
            border-radius: 50%;
        }

        .note-1 { transform: rotate(-2deg); }
        .note-2 { transform: rotate(3deg); background-color: #FFFA9E; }
        .note-3 { transform: rotate(-1deg); background-color: #FFF9C4; }
        .note-4 { transform: rotate(2deg); }
        .note-5 { transform: rotate(-3deg); background-color: #FEFF9C; }

        .sticky-label { font-size: 0.8rem; color: #555; font-weight: bold; margin-bottom: 2px; }
        .sticky-value { font-size: 1.5rem; color: #000; font-weight: 900; font-family: 'Courier New', monospace; }

        .live-text { color: red; font-weight: bold; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# --- 2. 대회 요강 (정적 섹션) --- ㅡㅡ^
st.title("🎾 제1회 CJ 계열사 대항 테니스 대회")

with st.expander("📋 대회 상세 모집 요강 (필독)", expanded=False):
    with st.expander("📋 대회 상세 모집 요강 (필독)", expanded=True):

        st.markdown("""
    
        ### 1. 대회 개요
    
        * **일시:** 2026년 3월 8일 (일요일) 08:00 ~ 15:00
    
        * **장소:** 장충 테니스장 (**집결 시간: 오전 07:30**)
    
    
    
        ### 2. 경기 운영 및 종료 상세 규칙
    
        * **즉시 시작 (No Warm-up):** 코트 입장 즉시 첫 서브로 경기 시작 (몸풀기는 코트 밖 진행)
    
        * **노-애드 (No-Ad):** 모든 게임 적용 (40:40 시 리시버 선택)
    
        * **코트 체인지:** 게임 합이 홀수일 때 휴식 없이 즉시 교대
    
        * **경기 종료 공지:** - **38분 경과:** 마이크로 "라스트 게임" 공지 (해당 게임이 마지막)
    
        - **40분 버저:** 종료 전 게임이 안 끝날 경우 **버저 시점 스코어**로 승/무/패 결정 (동점 시 무승부)
    
        * **타이(TIE)브레이크 :** 없음(5대5 일시 무승부 처리)
    
        * **상금 :** 없음. 다만, 트로피 및 메달 부여(3등까지)
    
    
    
    
    
    
    
        ### 3. 대회 방식 및 심판 규정
    
        * **예선:** 2개 조 풀리그 (승점제: 승 3, 무 1, 패 0)
    
        * **결선:** 6강 PO → 4강 → 결승 (순위: 승점 > 득실차 > 다득점>합산 구력>합산 나이 순)
    
        * **3.4 위전 진행:** 4강 패배 팀끼리 3위 결정전 시행
    
        * **심판:** 4강전부터 **대진과 관련 없는 타 계열사 인원**이 심판 진행
    
    
    
        ### 4. 출전 명단 및 중복 출전 규정
    
        * **매치 구성:** 1번 남복 / 2번 단식 / 3번 여복
    
        * **중복 규정:** **한 경기(Match) 내 중복 불가, 다음 경기(타 팀전) 출전 허용**
    
        - 💡 예: [제당 vs 올네] 단식 출전 선수 → [제당 vs 올영] 복식 출전 (**가능**)
    
        * **여복 특례:** 여성 부족 시 **구력 1.5년 이하 남성**에 한해 출전 가능
    
        * **용병:** 사내 인원 부족으로 참가가 어려울시 외부 용병 팀당 1명 승인 가능(사전 CJ테니스클럽 임원진 승인 필요)
    
        ### 5. 결과 입력 및 ID (PW: 팀장님들께 공유)
    
        * 제일제당: `cheiljedang_a` / 올리브영: `oliveyoung` / 올리브네트웍스: `ons`
    
        * ENM 엔터: `enment` / ENM 커머스: `enmcms` / 대한통운: `daetong_food
    
    
    
        ### 6. 식사 및 주차
    
        * **식사:** 클럽별 개별 해결
    
        * **주차:** **코트 내 불가** (동국대 앞 유소년 야구장 골목 또는 국립극장 공영주차장)
    
        """)

st.divider()

# --- 3. 타임테이블 데이터 (정적 데이터) --- ㅡㅡ^
schedule_data = {
    "시간": ["08:00", "08:40", "09:20", "10:00", "10:40", "11:20", "12:00", "12:40", "13:25", "14:10"],
    "비고": ["예선", "예선", "예선", "예선", "예선", "예선", "예선", "6강 PO", "4강", "결승"],
    "1코트": ["제당A-B", "CM A-B", "ENT A-제당A", "제당B-CM A", "CM B-ENT A", "제당A-CM B", "CM B-제당B", "6강 PO1", "4강 1", "결승"],
    "2코트": ["CM A-B", "ENT A-제당A", "제당A-B", "CM B-ENT A", "제당B-CM A", "제당B-ENT A", "ENT A-CM A", "6강 PO1", "4강 1",
            "결승"],
    "3코트": ["ENT A-제당A", "제당A-B", "CM A-B", "제당B-CM A", "CM B-ENT A", "제당A-CM B", "CM B-제당B", "6강 PO1", "4강 1", "결승"],
    "4코트": ["ENT B-올네", "올영A-B", "CJ-ENT B", "올네-올영A", "올영B-CJ", "ENT B-올영A", "올영B-올네", "6강 PO2", "4강 2", "3,4위전"],
    "5코트": ["올영A-B", "CJ-ENT B", "ENT B-올네", "올영B-CJ", "올네-올영A", "올네-올영B", "CJ-올영A", "6강 PO2", "4강 2", "3,4위전"],
    "6코트": ["CJ-ENT B", "ENT B-올네", "올영A-B", "올네-올영A", "올영B-CJ", "ENT B-올영A", "올영B-올네", "6강 PO2", "4강 2", "3,4위전"]
}
df_timetable = pd.DataFrame(schedule_data)


# 하이라이트 함수 ㅡㅡ^
def highlight_row(row):
    now_t = datetime.now().time()
    start = datetime.strptime(row['시간'], "%H:%M").time()
    try:
        idx = df_timetable[df_timetable['시간'] == row['시간']].index[0]
        if idx < len(df_timetable) - 1:
            end = datetime.strptime(df_timetable.iloc[idx + 1]['시간'], "%H:%M").time()
        else:
            end = time(23, 59)
    except:
        end = time(23, 59)

    if start <= now_t < end:
        return ['background-color: #FFF9C4; border-left: 5px solid #FBC02D; font-weight: bold; color: #7F6000;'] * len(
            row)
    return [''] * len(row)


# --- 4. 실시간 업데이트 로직 (루프 섹션) --- ㅡㅡ^
target_datetime = datetime(2026, 3, 8, 8, 0, 0)
placeholder = st.empty()  # 이 placeholder 하나만 계속 갱신합니다.

while True:
    now = datetime.now()
    diff = target_datetime - now

    # 시간 데이터 계산
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    with placeholder.container():
        # 1) D-Day 스티커 메모 ㅡㅡ^
        st.markdown("### 🏟️ CJ Tournament Live Dashboard")
        if diff.total_seconds() > 0:
            st.markdown(f"""
                <div class="sticky-container">
                    <div class="sticky-note note-1"><div class="sticky-label">TODAY</div><div class="sticky-value" style="font-size:1.1rem;">{now.strftime('%m/%d')}</div></div>
                    <div class="sticky-note note-2"><div class="sticky-label">DAYS</div><div class="sticky-value">{days}</div></div>
                    <div class="sticky-note note-3"><div class="sticky-label">HOURS</div><div class="sticky-value">{hours:02d}</div></div>
                    <div class="sticky-note note-4"><div class="sticky-label">MINS</div><div class="sticky-value">{minutes:02d}</div></div>
                    <div class="sticky-note note-5"><div class="sticky-label">SECS</div><div class="sticky-value">{seconds:02d}</div></div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="sticky-container">
                    <div class="sticky-note note-1"><div class="live-text" style="font-size:1.5rem;">LIVE NOW!</div></div>
                </div>
            """, unsafe_allow_html=True)

        # 2) 실시간 타임테이블 ㅡㅡ^
        st.markdown("#### 🕒 코트별 실시간 타임테이블")
        styled_df = df_timetable.style.apply(highlight_row, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True, height=390)

        st.caption(f"⚡ 실시간 갱신 중... (현재 시각: {now.strftime('%H:%M:%S')})")
        st.info("💡 노란색으로 표시된 행이 현재 진행 중인 시간대입니다.")

    time_module.sleep(1)  # 1초 대기 후 placeholder 내용만 교체