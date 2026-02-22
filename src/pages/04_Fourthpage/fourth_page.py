import streamlit as st
import pandas as pd

# --- 1. UI 및 상단 밀착 CSS ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container {
            padding-top: 1rem !important;
            margin-top: 0rem !important;
            max-width: 98% !important;
        }
        /* 테이블 폰트 및 가독성 최적화 */
        .stTable { font-size: 0.82rem !important; }
        .match-type { font-weight: normal; color: #666; }
        .rule-box {
            background-color: #f8f9fa;
            border-left: 5px solid #ff4b4b;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. 대회 요강 섹션 (상단 배치) ---
st.title("🎾 제1회 CJ 계열사 대항 테니스 대회")

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

    ### 3. 대회 방식 및 심판 규정
    * **예선:** 2개 조 풀리그 (승점제: 승 3, 무 1, 패 0)
    * **결선:** 6강 PO → 4강 → 결승 (순위: 승점 > 득실차 > 다득점 순)
    * **심판:** 4강전부터 **대진과 관련 없는 타 계열사 인원**이 심판 진행

    ### 4. 출전 명단 및 중복 출전 규정
    * **매치 구성:** 1번 남복 / 2번 단식 / 3번 여복
    * **중복 규정:** **한 경기(Match) 내 중복 불가, 다음 경기(타 팀전) 출전 허용**
        - 💡 예: [제당 vs 올네] 단식 출전 선수 → [제당 vs 올영] 복식 출전 (**가능**)
    * **여복 특례:** 여성 부족 시 **구력 1.5년 이하 남성**에 한해 출전 가능

    ### 5. 결과 입력 및 ID (PW: 팀장님들께 공유)
    * 제일제당: `cheiljedang_a` / 올리브영: `oliveyoung` / 올리브네트웍스: `ons`
    * ENM 엔터: `enment` / ENM 커머스: `enmcms` / 대한통운: `daetong`

    ### 6. 식사 및 주차
    * **식사:** 클럽별 개별 해결
    * **주차:** **코트 내 불가** (동국대 앞 유소년 야구장 골목 또는 국립극장 공영주차장)
    """)

st.divider()

# --- 3. 타임테이블 데이터 생성 ---
st.header("📅 공식 타임테이블")
schedule_data = {
    "시간": ["08:00", "08:40", "09:20", "10:00", "10:40", "11:20", "12:00", "12:40 (6강)", "13:25 (4강)", "14:10 (결승)"],
    "1코트": ["제당A-B (남단)", "CM A-B (남단)", "ENT A-제당A (남단)", "제당B-CM A (남단)", "CM B-ENT A (남단)", "제당A-CM B (남복)", "CM B-제당B (남단)", "6강 PO1 (남단)", "4강 1 (남단)", "결승 (남단)"],
    "2코트": ["CM A-B (남복)", "ENT A-제당A (남복)", "제당A-B (남복)", "CM B-ENT A (남복)", "제당B-CM A (남복)", "제당B-ENT A (여복)", "ENT A-CM A (남복)", "6강 PO1 (남복)", "4강 1 (남복)", "결승 (남복)"],
    "3코트": ["ENT A-제당A (여복)", "제당A-B (여복)", "CM A-B (여복)", "제당B-CM A (여복)", "CM B-ENT A (여복)", "제당A-CM B (남단)", "CM B-제당B (여복)", "6강 PO1 (여복)", "4강 1 (여복)", "결승 (여복)"],
    "4코트": ["ENT B-올네 (남단)", "올영A-B (남단)", "CJ-ENT B (남단)", "올네-올영A (남단)", "올영B-CJ (남단)", "ENT B-올영A (남복)", "올영B-올네 (남단)", "6강 PO2 (남단)", "4강 2 (남단)", "3,4위전 (남단)"],
    "5코트": ["올영A-B (남복)", "CJ-ENT B (남복)", "ENT B-올네 (남복)", "올영B-CJ (남복)", "올네-올영A (남복)", "올네-올영B (여복)", "CJ-올영A (남복)", "6강 PO2 (남복)", "4강 2 (남복)", "3,4위전 (남복)"],
    "6코트": ["CJ-ENT B (여복)", "ENT B-올네 (여복)", "올영A-B (여복)", "올네-올영A (여복)", "올영B-CJ (여복)", "ENT B-올영A (남단)", "올영B-올네 (여복)", "6강 PO2 (여복)", "4강 2 (여복)", "3,4위전 (여복)"]
}

df_timetable = pd.DataFrame(schedule_data)
st.table(df_timetable)

st.info("💡 12:40분부터는 본선 토너먼트가 시작됩니다. 예선 결과에 따라 대진이 자동 배정됩니다.")

# --- 4. 선수 등록 ---
st.divider()
st.subheader("📥 선수 명단 일괄 등록")
uploaded_file = st.file_uploader("명단 엑셀 업로드 (이름, 소속, 구력, 성별)", type=['xlsx', 'xls'])
if uploaded_file:
    df_players = pd.read_excel(uploaded_file)
    st.session_state.player_db = df_players
    st.success("선수 명단 배포 완료!")