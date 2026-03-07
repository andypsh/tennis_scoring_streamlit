import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_module

# --- 1. UI 설정 및 커스텀 CSS ---
st.set_page_config(layout="wide", page_title="CJ Tennis Live Board")

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
        "[B] 대통-올영B (남단)", "[B] 대통-올영B (여복)", "[B] ENT-A-제당B (남복)", "[A] 제당A-CM-B (남복)",
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
        "[A] 올네A-ENT-B (여복)", "[B] 대통-올영B (남복)", "[B] CM-A-ENT-A (남복)", "[B]CM-A-올영B(남복)",
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