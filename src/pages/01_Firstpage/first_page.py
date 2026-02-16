import streamlit as st
import pandas as pd

# --- 1. UI 및 상단 밀착 CSS ---
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

        .group-card {
            background-color: #ffffff;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            border-top: 6px solid #FF4B4B; 
            padding: 24px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .group-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #1E1E1E;
            margin-bottom: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. 세션 상태 초기화 ---
if 'player_db' not in st.session_state: st.session_state.player_db = None
if 'groups' not in st.session_state: st.session_state.groups = {}
if 'match_data' not in st.session_state: st.session_state.match_data = pd.DataFrame()
if 'mode' not in st.session_state: st.session_state.mode = "토너먼트 (조별 예선)"
if 'role' not in st.session_state: st.session_state.role = "Public"  # 기본 권한은 공개(Public)

# --- 3. 사이드바 로그인 시스템 (다중 계정 대응) ㅡㅡ^ ---
with st.sidebar:
    st.title("🔐 사용자 인증")
    if st.session_state.role == "Public":
        input_user = st.text_input("아이디")
        input_pw = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            # 1. 관리자 체크
            if input_user == st.secrets["auth"]["admin_user"] and \
                    input_pw == st.secrets["auth"]["admin_password"]:
                st.session_state.role = "Admin"
                st.rerun()
            # 2. 일반인 계정 체크
            elif input_user == st.secrets["auth"]["general_user"] and \
                    input_pw == st.secrets["auth"]["general_password"]:
                st.session_state.role = "User"
                st.rerun()
            else:
                st.error("계정 정보가 일치하지 않습니다.")
    else:
        st.write(f"✅ **{st.session_state.role}** 권한으로 접속 중")
        if st.button("로그아웃"):
            st.session_state.role = "Public"
            st.rerun()

# --- 4. 메인 화면: 관리자(Admin) 전용 설정 구역 ---
st.header("🏆 대회 실시간 운영 센터")

if st.session_state.role == "Admin":
    st.markdown("### ⚙️ 대회 관리 설정 (andy 전용)")
    st.session_state.mode = st.radio("대회 유형 설정:", ["토너먼트 (조별 예선)", "교류전 (2개 팀 맞대결)"],
                                     index=0 if "토너먼트" in st.session_state.mode else 1, horizontal=True)

    with st.expander("📂 1단계: 선수 명단 엑셀 업로드", expanded=(st.session_state.player_db is None)):
        uploaded_file = st.file_uploader("명단 업로드", type=['xlsx', 'xls'])
        if uploaded_file is not None:
            df_p = pd.read_excel(uploaded_file)
            st.session_state.player_db = df_p
            st.success("✅ 명단 로드 완료")

    if st.session_state.player_db is not None:
        all_teams = sorted(st.session_state.player_db['소속'].unique().tolist())

        if "토너먼트" in st.session_state.mode:
            with st.expander("⚖️ 2단계: 조 편성 (중복 차단)", expanded=st.session_state.match_data.empty):
                num_groups = st.selectbox("조 개수:", [2, 3, 4, 5])
                group_names = [f"{chr(65 + i)}조" for i in range(num_groups)]
                temp_groups = {}
                already_selected = []

                for g_name in group_names:
                    available = [t for t in all_teams if t not in already_selected]
                    prev = st.session_state.groups.get(g_name, [])
                    options_show = sorted(list(set(available + prev)))

                    selected = st.multiselect(f"📍 {g_name} 팀 선택", options=options_show, default=prev,
                                              key=f"sel_{g_name}")
                    temp_groups[g_name] = selected
                    already_selected.extend(selected)

                if st.button("🚀 대진표 생성 및 대회 시작"):
                    matches = []
                    for gn, gt in temp_groups.items():
                        for i in range(len(gt)):
                            for j in range(i + 1, len(gt)):
                                matches.append(
                                    {"조": gn, "홈": gt[i], "어웨이": gt[j], "남단_홈": 0, "남단_어웨이": 0, "남복_홈": 0, "남복_어웨이": 0,
                                     "여복_홈": 0, "여복_어웨이": 0, "남단_선수": [], "남복_선수": [], "여복_선수": [], "확정": False})
                    st.session_state.match_data = pd.DataFrame(matches)
                    st.session_state.groups = temp_groups
                    st.rerun()
elif st.session_state.role == "User":
    st.info("👋 **cheiljedang_a**님 환영합니다. 현재 순위표 조회 권한이 활성화되었습니다.")
else:
    st.info("ℹ️ 현재 실시간 순위 조회 모드입니다. 관리 정보 수정은 로그인 후 가능합니다.")

st.divider()

# --- 5. 실시간 순위 현황 (누구나 볼 수 있음) ---
if not st.session_state.match_data.empty:
    def calculate_standings(df_matches, target_group):
        if target_group not in st.session_state.groups: return pd.DataFrame()
        group_teams = st.session_state.groups[target_group]
        standings = []
        for team in group_teams:
            m = df_matches[((df_matches['홈'] == team) | (df_matches['어웨이'] == team)) & (df_matches['확정'])]
            w, d, l, pts, gd = 0, 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (row['홈'] == team)
                h_wins = (row['남단_홈'] > row['남단_어웨이']) + (row['남복_홈'] > row['남복_어웨이']) + (row['여복_홈'] > row['여복_어웨이'])
                a_wins = (row['남단_어웨이'] > row['남단_홈']) + (row['남복_어웨이'] > row['남복_홈']) + (row['여복_어웨이'] > row['여복_홈'])
                c_gd = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
                gd += c_gd if is_home else -c_gd
                if h_wins == a_wins:
                    d += 1; pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1; pts += 3
                else:
                    l += 1
            standings.append({"팀명": team, "경기": len(m), "승": w, "무": d, "패": l, "승점": pts, "득실": gd})
        return pd.DataFrame(standings).sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)


    st.subheader("📊 실시간 조별 순위 (Live)")
    for gn in st.session_state.groups.keys():
        with st.container():
            st.markdown(f'<div class="group-card"><div class="group-title">📍 {gn} 현황</div></div>',
                        unsafe_allow_html=True)
            df_res = calculate_standings(st.session_state.match_data, gn)
            if not df_res.empty:
                # 색깔 강조 유지 ㅡㅡ^
                st.dataframe(df_res.style.highlight_max(subset=['승점'], color='#D1E7DD').highlight_min(subset=['패'],
                                                                                                      color='#F8D7DA'),
                             use_container_width=True, hide_index=True)