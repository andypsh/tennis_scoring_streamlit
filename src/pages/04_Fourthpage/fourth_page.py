import streamlit as st
import pandas as pd
from datetime import datetime, time

# --- 1. UI 설정 및 커스텀 CSS ---
st.set_page_config(layout="wide", page_title="CJ Tennis Live Board")
with st.expander("📋 대회 상세 모집 요강 (필독)", expanded=False):
    st.markdown("""
    ### 1. 대회 개요
* **일시:** 2026년 3월 21일 (토요일) 18:00 ~ 22:00
* **장소:** 항공대 테니스장 (**집결 시간: 17:45**)

### 2. 경기 운영 및 종료 상세 규칙
* **즉시 시작 (No Warm-up):** 코트 입장 즉시 첫 서브로 경기 시작 (1경기,2경기만 10분간 몸풀기)
* **경기 방식:** 매치당 30분, 6게임 진행
* **노-애드 (No-Ad):** 모든 게임 적용 (40:40 시 리시버 선택)
* **무승부 규정:** 게임 스코어 5:5 도달 시 무승부 처리 (타이브레이크 없음)

### 3. 식사 및 주차
* **식사:** 클럽별 개별 해결
* **주차:** **항공대 교내 주차 (클럽하우스 내 주차권 수령)**
    """)

st.markdown("""
    <style>
        .main-title { font-size: 2.2rem; font-weight: 900; color: #333; margin-bottom: 20px; }
        .stDataFrame { font-size: 0.95rem !important; }
    </style>
""", unsafe_allow_html=True)

schedule_data = {
    "시간": ["18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30"],
    "1코트": [
        "[남복] 예준/소휘 (3.5) vs 병호/동희 (2.5)",
        "[혼복] 성혁/민영 (3.6) vs 익성/성희 (3.0)",
        "[남복] 성혁/소휘 (5.5) vs 경랑/병호 (4.0)",
        "[혼복] 소휘/문정 (4.0) vs 동희/새롬 (2.5)",
        "[남복] 성혁/두영 (4.5) vs 익성/재환 (5.5)",
        "[혼복] 예준/민영 (1.1) vs 경랑/은채 (4.0)",
        "[남복] 성혁/현준 (5.5) vs 재환/경랑 (5.5)",
        "[혼복] 규찬/문정 (3.0) vs 태훈/은채 (4.0)"
    ],
    "2코트": [
        "[남복] 현준/규찬 (3.5) vs 태훈/재환 (5.5)",
        "[여복] 혜린/유진 (1.5) vs 은채/새롬 (2.5)",
        "[남복] 현준/두영 (3.5) vs 태훈/익성(5.5)",
        "[혼복] 현준/유진 (3.0) vs 경랑/승은 (4.5)",
        "[혼복] 소휘/혜린 (4.5) vs 태훈/승은 (3.0)",
        "[혼복] 규찬/문정 (3.0) vs 태훈/새롬 (4.0)",
        "[남복] 예준/두영 (2.0) vs 동희/익성 (3.0)",
        "[여복] 유진/혜린 (1.5) vs 새롬/성희 (2.5)"
    ],
    "3코트": [
        "[여복] 문정/유진 (2.5) vs 승은/은채 (3.0)",
        "[남복] 예준/두영 (2.0) vs 경랑/동희 (4.0)",
        "[여복] 민영/혜린 (0.6) vs 승은/성희 (3.0)",
        "[남복] 규찬/예준 (2.5) vs 재환/병호 (4.0)",
        "[여복] 민영/문정 (1.5) vs 은채/성희 (3.0)",
        "[남복] 성혁/현준 (6.0) vs 재환/동희 (4.0)",
        "[여복] 민영/유진 (1.1) vs 승은/성희 (3.0)",
        "[남복] 소휘/두영 (3.5) vs 익성/병호 (3.0)"
    ]
}
df_timetable = pd.DataFrame(schedule_data)


# --- 2. 하이라이트 로직 (현재 시간대만 강조) ---
def highlight_time_only(row):
    now_t = datetime.now().time()
    start_t = datetime.strptime(row['시간'], "%H:%M").time()

    # 시간대별 종료 시간 계산
    try:
        idx = df_timetable[df_timetable['시간'] == row['시간']].index[0]
        if idx < len(df_timetable) - 1:
            end_t = datetime.strptime(df_timetable.iloc[idx + 1]['시간'], "%H:%M").time()
        else:
            end_t = time(23, 59)
    except:
        end_t = time(23, 59)

    styles = [''] * len(row)

    # 현재 시간대 행 전체 강조 (연한 노랑)
    if start_t <= now_t < end_t:
        styles = ['background-color: #FFF9C4; border-left: 6px solid #FBC02D;'] * len(row)

    return styles


# --- 3. 타이틀 및 출력 ---
st.markdown('<div class="main-title">🎾 CJ TENNIS 대회 전광판</div>', unsafe_allow_html=True)
st.divider()

now_dt = datetime.now()

st.markdown("#### 🕒 전체 코트 현황")

# 스타일 적용된 데이터프레임 (시간만 하이라이트)
styled_df = df_timetable.style.apply(highlight_time_only, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True, height=520)

st.caption(f"⚡ 마지막 새로고침 시각: {now_dt.strftime('%H:%M:%S')} (페이지를 새로고침하면 현재 시간이 반영됩니다.)")