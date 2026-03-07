import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. UI 설정 및 강제 리프레시 스타일 ---
st.set_page_config(layout="wide")  # 화면 넓게 쓰기

if 'first_run' not in st.session_state:
    st.cache_data.clear()
    st.session_state['first_run'] = True
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container {
            padding-top: 1rem !important;
            max-width: 98% !important;
        }
        .live-indicator {
            color: #FF0000;
            font-weight: bold;
            animation: blinker 1.2s linear infinite;
        }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# --- 2. 최신 조 편성 데이터 (A/B조 완벽 분리) ---
# A조: 제당A, 올네A, ENM-CM-B, 올영A, ENM-ENT-B
# B조: ENM-CM-A, ENM-ENT-A, 대통-푸드빌A, 올영B, 제당B

schedule_data = {
    "시간": ["08:00", "08:40", "09:20", "10:00", "10:40", "11:20", "12:00", "12:40 (6강)", "13:25 (4강)", "14:10 (결승)"],
    "1코트 (A조 남단)": [
        "제당A-올네A", "CM-B-ENT-B", "올네A-올영A", "제당A-ENT-B", "제당A-CM-B", "올네A-ENT-B", "제당A-올네A",
        "6강 PO1 (남단)", "4강 1 (남단)", "결승 (남단)"
    ],
    "2코트 (A조 남복/여복)": [
        "CM-B-올영A", "제당A-올영A", "CM-B-ENT-B", "올네A-CM-B", "올영A-ENT-B", "제당A-올영A", "CM-B-올영A",
        "6강 PO1 (남복)", "4강 1 (남복)", "결승 (남복)"
    ],
    "3코트 (A조 대기)": [
        "ENT-B 휴식", "올네A 휴식", "제당A 휴식", "올영A 휴식", "올네A 휴식", "CM-B 휴식", "ENT-B 휴식",
        "6강 PO1 (여복)", "4강 1 (여복)", "결승 (여복)"
    ],
    "4코트 (B조 남단)": [
        "CM-A-ENT-A", "대통-제당B", "ENT-A-올영B", "CM-A-제당B", "CM-A-대통", "ENT-A-제당B", "CM-A-ENT-A",
        "6강 PO2 (남단)", "4강 2 (남단)", "3,4위전 (남단)"
    ],
    "5코트 (B조 남복/여복)": [
        "대통-올영B", "CM-A-올영B", "대통-제당B", "ENT-A-대통", "올영B-제당B", "CM-A-올영B", "대통-올영B",
        "6강 PO2 (남복)", "4강 2 (남복)", "3,4위전 (남복)"
    ],
    "6코트 (B조 대기)": [
        "제당B 휴식", "ENT-A 휴식", "CM-A 휴식", "올영B 휴식", "ENT-A 휴식", "대통 휴식", "제당B 휴식",
        "6강 PO2 (여복)", "4강 2 (여복)", "3,4위전 (여복)"
    ]
}

df_timetable = pd.DataFrame(schedule_data)

# --- 3. 실시간 시간 처리 로직 ---
now = datetime.now()
current_time_str = now.strftime("%H:%M")

st.header(f"📅 3월 8일 대회 공식 타임테이블")
st.subheader(f"현재 시각: {current_time_str}")


def apply_highlight(row):
    # 시간 문자열에서 비교용 시간만 추출 (예: "12:40 (6강)" -> "12:40")
    row_start_time = row['시간'].split(' ')[0]

    # 현재 행의 인덱스를 찾아 다음 행의 시간을 가져옴 (종료 시간 판정용)
    idx = df_timetable.index[df_timetable['시간'] == row['시간']][0]
    if idx < len(df_timetable) - 1:
        next_time = df_timetable.iloc[idx + 1]['시간'].split(' ')[0]
    else:
        next_time = "23:59"

    # 현재 시간이 경기 시작과 다음 경기 시작 사이에 있으면 하이라이트
    if row_start_time <= current_time_str < next_time:
        return ['background-color: #FFF9C4; color: black; font-weight: bold; border: 2px solid #FFD600'] * len(row)
    return [''] * len(row)


# 스타일 적용된 테이블 출력
styled_df = df_timetable.style.apply(apply_highlight, axis=1)
st.table(styled_df)

st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px;">
        <span class="live-indicator">● LIVE</span> 
        현재 <b>{current_time_str}</b> 기준 진행 중인 경기는 노란색으로 강조됩니다.
    </div>
""", unsafe_allow_html=True)