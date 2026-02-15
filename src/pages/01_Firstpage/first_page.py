from datetime import datetime
import streamlit as st
import os
import sys
import importlib
import pandas as pd

#################[Module PATH 지정]###################
current_dir = os.path.dirname(os.path.realpath(__file__))
tab_logic_path = os.path.join(current_dir, 'tabs', '01_tab')
resource_path = os.path.abspath(os.path.join(current_dir, '../../resource/'))
login_dir = os.path.abspath(os.path.join(current_dir, '../../../login/'))

for p in [tab_logic_path, resource_path, login_dir]:
    if p not in sys.path:
        sys.path.append(p)

login_module = importlib.import_module("lgn")

######################################################

# --- 1. 레이아웃 정렬 CSS ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
            max-width: 95% !important;
        }
        .stHeadingContainer { margin-bottom: -1.5rem !important; }
        hr { margin-top: 0.5rem !important; margin-bottom: 1rem !important; }

        /* 실시간 엔트리와 통계 박스 윗선 일치용 */
        .colored-bg {
            background-color: #f0f0f0;
            border: 1px solid #e0e0e0;
            padding: 10px;
            height: 48px;
            display: flex;
            align-items: center;
            margin-bottom: 0px !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    config = login_module.get_conf()
    login_module.login_check(config)

if st.session_state.get('authentication_status'):
    # [2. 데이터 초기화 및 렌더링 에러 방지]
    # '게임득실' 컬럼이 없으면 세션을 강제 초기화합니다.
    if 'score_data' not in st.session_state or '게임득실' not in st.session_state.score_data.columns:
        teams = [f"팀_{chr(65 + i)}{j}" for i in range(2) for j in range(1, 6)]
        st.session_state.score_data = pd.DataFrame({
            "조": ['A조'] * 5 + ['B조'] * 5,
            "팀명": teams,
            "매치승": [0] * 10,
            "매치패": [0] * 10,
            "게임득실": [0] * 10,  # 컬럼명 통일
            "승점": [0] * 10
        })

    # 50인 예선 엔트리 데이터
    df_raw = pd.DataFrame({
        "No": range(1, 51),
        "성명": [f"CJ_테니스꾼_{i:02d}" for i in range(1, 51)],
        "레벨": ["A", "B", "C"] * 16 + ["A", "B"],
        "조": [f"{(i - 1) // 5 + 1}조" for i in range(1, 51)]
    })

    # [3. Header Section]
    st.header("🎾 3월 8일 장충 테니스 대회 예선 운영")
    st.markdown("<hr style='border-top: 3px solid black; margin-top: 10px; margin-bottom: 20px'/>",
                unsafe_allow_html=True)

    # [4. Upper Layout] 좌우 라인 정렬
    layout1, layout2 = st.columns([10, 3.5])

    with layout1:
        st.subheader('📍 참가자 명단')
        st.divider()
        select_options = ['전체'] + [f'{i}조' for i in range(1, 11)]
        select_value = st.selectbox("Select Group:", select_options, key='filter_select')

        st.markdown('<div class="colored-bg">실시간 엔트리 확인</div>', unsafe_allow_html=True)
        with st.container(height=350, border=None):
            st.write(df_raw[df_raw['조'] == select_value] if select_value != '전체' else df_raw)

    with layout2:
        st.subheader('📊 조별 정보')
        st.divider()
        # [정렬] 76px 공백으로 좌측 Selectbox 높이 상쇄
        st.markdown("<div style='height: 76px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="colored-bg">통계</div>', unsafe_allow_html=True)
        with st.container(height=350, border=None):
            st.info(
                f"**선택된 조**: {select_value}\n\n인원: {len(df_raw[df_raw['조'] == select_value]) if select_value != '전체' else 50}명")
            st.divider()
            st.caption("🏆 1단 2복: 최종 매치 승리 시 승점 3점")

    # [5. Lower Layout] 결과 입력 및 랭킹
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📝 예선 경기 결과 입력 및 실시간 순위")
    st.divider()

    score_col1, score_col2 = st.columns([1, 1])

    with score_col1:
        st.write("### 🅰️ A조 순위")
        # 승점 -> 게임득실 순으로 정렬
        a_rank = st.session_state.score_data[st.session_state.score_data['조'] == 'A조'].sort_values(by=["승점", "게임득실"],
                                                                                                   ascending=False)
        st.table(a_rank)

    with score_col2:
        st.write("### 🅱️ B조 순위")
        b_rank = st.session_state.score_data[st.session_state.score_data['조'] == 'B조'].sort_values(by=["승점", "게임득실"],
                                                                                                   ascending=False)
        st.table(b_rank)

    st.info("💡 각 팀의 매치 결과와 게임 득실을 입력하세요. (1단 2복 단체전)")

    # 데이터 에디터 (에러 방지를 위해 세션 데이터 직접 연결)
    edited_df = st.data_editor(
        st.session_state.score_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "팀명": st.column_config.Column(disabled=True),
            "조": st.column_config.Column(disabled=True),
            "매치승": st.column_config.NumberColumn("매치 승리 (Max 3)", min_value=0, max_value=3),
            "게임득실": st.column_config.NumberColumn("게임 득실차"),
            "승점": st.column_config.NumberColumn("최종 승점", help="승리 팀 3점 부여")
        },
        key="editor"
    )

    if st.button("💾 결과 저장 및 순위 반영"):
        st.session_state.score_data = edited_df
        st.rerun()

else:
    st.header('🔐 로그인이 필요한 서비스입니다.')