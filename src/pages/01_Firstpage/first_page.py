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
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. 세션 상태 초기화 ---
if 'groups' not in st.session_state: st.session_state.groups = {}
if 'match_data' not in st.session_state: st.session_state.match_data = pd.DataFrame()
if 'mode' not in st.session_state: st.session_state.mode = "토너먼트"

# --- 3. 대회 모드 및 선수 등록 ---
st.header("🏆 대회/교류전 운영 본부")

st.session_state.mode = st.radio("대회 유형을 선택하세요:", ["토너먼트 (조별 예선)", "교류전 (2개 팀 맞대결)"], horizontal=True)

with st.expander("📂 1단계: 선수 명단 엑셀 업로드", expanded=True):
    uploaded_file = st.file_uploader("필수 컬럼: 이름, 소속, 성별, 구력", type=['xlsx', 'xls'])
    if uploaded_file is not None:
        df_players = pd.read_excel(uploaded_file)
        if all(col in df_players.columns for col in ['이름', '소속', '성별', '구력']):
            st.session_state.player_db = df_players
            st.success(f"✅ {len(df_players)}명의 선수가 등록되었습니다.")
        else:
            st.error("❌ 엑셀 컬럼 확인 필요: 이름, 소속, 성별, 구력")

# --- 4. 모드별 조 편성 및 대진 생성 ---
if 'player_db' in st.session_state:
    all_teams = sorted(st.session_state.player_db['소속'].unique().tolist())

    if st.session_state.mode == "토너먼트 (조별 예선)":
        with st.expander("⚖️ 2단계: 조 편성 (중복 선택 방지)", expanded=True):
            num_groups = st.selectbox("조 개수 선택:", [2, 3, 4, 5], index=0)
            group_names = [f"{chr(65 + i)}조" for i in range(num_groups)]

            temp_groups = {}
            already_selected = []

            # 세로로 주르륵 배치하며 필터링 적용
            for g_name in group_names:
                # 이미 선택된 팀을 제외한 옵션 생성
                available_options = [t for t in all_teams if t not in already_selected]

                selected = st.multiselect(
                    f"📍 {g_name} 팀 선택 (남은 팀: {len(available_options)}개)",
                    options=available_options,
                    key=f"select_{g_name}"
                )
                temp_groups[g_name] = selected
                already_selected.extend(selected)  # 선택된 팀 목록 업데이트
                st.markdown("---")

            if st.button("🚀 토너먼트 대진표 생성"):
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

    else:
        with st.expander("🤝 2단계: 교류전 팀 및 경기 수 설정", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                team_h = st.selectbox("홈 팀 선택:", all_teams, key="h_team")
            with c2:
                team_a = st.selectbox("어웨이 팀 선택:", [t for t in all_teams if t != team_h], key="a_team")
            with c3:
                match_count = st.number_input("총 대결 횟수(단체전 수):", 1, 10, 1)

            if st.button("🚀 교류전 대진표 생성"):
                matches = []
                for i in range(1, match_count + 1):
                    matches.append(
                        {"조": f"{i}회차", "홈": team_h, "어웨이": team_a, "남단_홈": 0, "남단_어웨이": 0, "남복_홈": 0, "남복_어웨이": 0,
                         "여복_홈": 0, "여복_어웨이": 0, "남단_선수": [], "남복_선수": [], "여복_선수": [], "확정": False})
                st.session_state.match_data = pd.DataFrame(matches)
                st.session_state.groups = {"교류전": [team_h, team_a]}
                st.rerun()

st.divider()

# --- 5. 결과 입력 및 순위표 섹션 ---
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
                current_gd = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (
                            row['여복_홈'] - row['여복_어웨이'])
                gd += current_gd if is_home else -current_gd
                if h_wins == a_wins:
                    d += 1;
                    pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1;
                    pts += 3
                else:
                    l += 1
            standings.append({"팀명": team, "경기": len(m), "승": w, "무": d, "패": l, "승점": pts, "득실": gd})
        return pd.DataFrame(standings).sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)


    st.subheader("📊 실시간 순위 현황")
    g_names = list(st.session_state.groups.keys())

    for gn in g_names:
        with st.container():
            st.markdown(f"""
                <div class="group-card">
                    <div class="group-title">
                        <span>📍 {gn} 순위 상황</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            df_res = calculate_standings(st.session_state.match_data, gn)
            if not df_res.empty:
                st.dataframe(
                    df_res.style.highlight_max(subset=['승점'], color='#D1E7DD')
                    .highlight_min(subset=['패'], color='#F8D7DA'),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "팀명": st.column_config.TextColumn("팀명", width="medium"),
                        "승점": st.column_config.NumberColumn("승점 🔥"),
                        "득실": st.column_config.NumberColumn("득실(GD)")
                    }
                )
            else:
                st.info(f"{gn}의 진행 중인 경기가 없습니다.")
            st.write("")
