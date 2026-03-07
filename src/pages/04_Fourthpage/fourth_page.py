import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_module

# --- 1. UI 설정 및 커스텀 CSS ---
st.set_page_config(layout="wide", page_title="CJ Tennis Live Board")
with st.expander("📋 대회 상세 모집 요강 (필독)", expanded=False):





    st.markdown("""
    
    
    ### 1. 대회 개요
    
    
    * **일시:** 2026년 3월 8일 (일요일) 08:00 ~ 15:00
    
    
    * **장소:** 장충 테니스장 (**집결 시간: 오전 07:30**)
    
    
    
    
    ### 2. 경기 운영 및 종료 상세 규칙
    
    
    * **즉시 시작 (No Warm-up):** 코트 입장 즉시 첫 서브로 경기 시작 (몸풀기는 코트 밖 진행)
    
    
    * **노-애드 (No-Ad):** 모든 게임 적용 (40:40 시 리시버 선택)
    
    
    * **코트 체인지:** 예선 X(가위바위보 승자가 위치정함).
    
    본선에선 적용.게임 합이 홀수일 때 휴식 없이 즉시 교대.
    
    
    * **경기 종료 공지:** - **28분 OR 38분 경과:** 마이크로 "라스트 게임" 공지 (해당 게임이 마지막)
    
    
    - **예선 30분 버저:** 종료 전 게임이 안 끝날 경우 **버저 시점 스코어**로 승/무/패 결정 (동점 시 무승부)
    
    
    
    - **본선 40분 버저:** 종료 전 게임이 안 끝날 경우 **버저 시점 스코어**로 승/무/패 결정 (동점 시 무승부)
    
    
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


st.markdown("""
    <style>
        /* 메인 타이틀 스타일 */
        .main-title { font-size: 2.2rem; font-weight: 900; color: #333; margin-bottom: 20px; }

        /* 실시간 강조 애니메이션 */
        .live-text { color: red; font-weight: bold; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* 테이블 폰트 크기 및 스타일 */
        .stDataFrame { font-size: 0.95rem !important; }
    </style>
""", unsafe_allow_html=True)

schedule_data = {
    "시간": ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:40", "14:20"],
    "1코트": [
        "[A]올영A-올네A(남복)", "[A] 제당A-올네A (남복)", "[A] 제당A-CM-B (남단)", "[A]CM-B-올네A(여복)",
        "[B]올영B-CM-A(여복)", "[A] 제당A-올네A (남단)", "[B] 올영B-ENT-A(남단)", "[A] ENT-B- CM-B(여복)",
        "[A]제당A-올영A(남복)", "[A]ENT-B-올영A(남복)", "6강PO1(남단)", "4강 1 (남단)", "결승 (남단)"
    ],
    "2코트": [
        "[B] 대통-올영B (남단)", "[B] 대통-올영B (여복)", "[A] 올네A-ENT-B (여복)", "[A] 제당A-CM-B (남복)",
        "[B]대통-ENT-A(남단)", "[A]올영A-올네A(여복)", "[A]ENT-B - CM-B(남복)", "[B]대통-제당B(여복)",
        "[A]제당A-올영A(여복)", "[A]ENT-B-올영A(여복)", "6강PO1(여복)", "4강 1 (남복)", "결승 (남복)"
    ],
    "3코트": [
        "[B] ENT-A-제당B (여복)", "[B] ENT-A-제당B (남단)", "[A]올영A-ENT-B(남단)", "[B] CM-A-ENT-A (여복)",
        "[B]대통-ENT-A(남복)", "[B]제당B-CM-A(남복)", "[A] 제당A-올네A (여복)", "[B]대통-제당B(남복)",
        "[A] 올네A-ENT-B (남단)", "[A]올영A-CM-B(남단)", "6강PO1(남복)", "4강 1 (여복)", "결승 (여복)"
    ],
    "4코트": [
        "[B] CM-A-ENT-A (남단)", "[A] CM-B-올영A (남복)", "[A] 제당A-CM-B(여복)", "[A] 올네A-ENT-B(남복)",
        "[A] 제당A-ENT-B(남단)", "[A]제당A-ENT-B(여복)", "[B]제당B-CM-A(여복)", "[A] 제당A-올영A(남단)",
        "[B]대통-ENT-A(여복)", "[A] 올네A-CM-B(남복)", "6강PO2(남단)", "4강 2 (남단)", "3,4위전 (남단)"
    ],
    "5코트": [
        "[A] CM-B-올영A (남단)", "[A] CM-B-올영A (여복)", "[B] CM-A -올영B(남단)", "[B] 대통-CM-A(남단)",
        "[B]제당B-CM-A(남단)", "[A]제당A-ENT-B(남복)", "[A] ENT-B - CM-B(남단)", "[B]올영B-ENT-A(남복)",
        "[B]제당B-올영B(남단)", "[B]제당B-올영B(남복)", "6강PO2(남복)", "4강 2 (남복)", "3,4위전 (남복)"
    ],
    "6코트": [
        "[B] ENT-A-제당B (남복)", "[B] 대통-올영B (남복)", "[B] CM-A-ENT-A (남복)", "[B]CM-A-올영B(남복)",
        "[A]올영A-올네A(남단)", "[B] 대통-제당B(남단)", "[B]대통-CM-A(남복)", "[B]올영B-ENT-A(여복)",
        "[B]제당B-올영B(여복)", "[B] 대통-CM-A(여복)", "6강PO2(여복)", "4강 2 (여복)", "3,4위전 (여복)"
    ]
}
df_timetable = pd.DataFrame(schedule_data)


# --- 3. 하이라이트 로직 ---
def highlight_combined(row, teams, events):
    now_t = datetime.now().time()
    start_t = datetime.strptime(row['시간'], "%H:%M").time()

    # 시간대별 종료 시간 계산 (간단히 다음 행 시간 참조)
    try:
        idx = df_timetable[df_timetable['시간'] == row['시간']].index[0]
        if idx < len(df_timetable) - 1:
            end_t = datetime.strptime(df_timetable.iloc[idx + 1]['시간'], "%H:%M").time()
        else:
            end_t = time(23, 59)
    except:
        end_t = time(23, 59)

    styles = [''] * len(row)

    # 1) 현재 시간대 행 전체 강조 (연한 노랑)
    if start_t <= now_t < end_t:
        styles = ['background-color: #FFF9C4; border-left: 6px solid #FBC02D;'] * len(row)

    # 2) 선택된 팀 + 종목 조합 강조 (주황색 테두리 + 볼드)
    for i, val in enumerate(row):
        cell_str = str(val)
        # 팀이 포함되어 있고 AND 종목이 포함되어 있는지 체크
        team_match = any(t in cell_str for t in teams) if teams else False
        event_match = any(f"({e})" in cell_str for e in events) if events else False

        if team_match and event_match:
            styles[
                i] += 'color: #E65100; font-weight: 900; border: 3px solid #FF9800 !important; background-color: #FFF3E0;'

    return styles


# --- 4. 상단 고정 필터 UI ---
st.markdown('<div class="main-title">🎾 CJ TENNIS 대회 실시간 전광판</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    selected_teams = st.multiselect("집중 마킹 팀 선택",
                                    ["제당A", "올영A", "올네A", "CM-B", "ENT-B", "CM-A", "ENT-A", "대통", "올영B", "제당B"],
                                    default=["제당A"])
with c2:
    selected_events = st.multiselect("집중 마킹 종목 선택", ["남단", "남복", "여복"], default=["남단", "남복", "여복"])
with c3:
    st.write("")  # 패딩용
    run_btn = st.button("🚀 실시간 가동 시작", use_container_width=True)

st.divider()

# 세션 상태 관리
if 'is_running' not in st.session_state: st.session_state.is_running = False
if run_btn: st.session_state.is_running = True

placeholder = st.empty()

# --- 5. 출력 루프 ---
while True:
    now_dt = datetime.now()

    with placeholder.container():
        st.markdown(f"#### 🕒 전체 코트 현황 (마킹: {', '.join(selected_teams)} / {', '.join(selected_events)})")

        # 스타일 적용된 데이터프레임
        styled_df = df_timetable.style.apply(lambda r: highlight_combined(r, selected_teams, selected_events), axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True, height=520)

        if st.session_state.is_running:
            st.caption(f"⚡ 실시간 모니터링 중... (현재 시각: {now_dt.strftime('%H:%M:%S')})")
            time_module.sleep(1)
        else:
            st.warning("상단의 '🚀 실시간 가동 시작' 버튼을 누르면 현재 경기 시간대가 강조됩니다.")
            break