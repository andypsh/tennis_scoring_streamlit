import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import ast

# --- 1. UI 및 CSS 설정 ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container { padding-top: 1rem !important; margin-top: 0rem !important; max-width: 95% !important; }
        hr { margin-top: 0.5rem !important; margin-bottom: 1rem !important; }
        .group-title { font-size: 1.5rem; font-weight: 800; color: #1E1E1E; margin-bottom: 18px; }
    </style>
""", unsafe_allow_html=True)


# --- 2. 구글 시트 연동 함수 ---
def get_gsheets_conn():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        st.error(f"❌ 구글 시트 연결 설정 오류: {e}")
        st.stop()


# def load_from_gsheets():
#     conn = get_gsheets_conn()
#     # Matches 탭에서 대진표 로드 ㅡㅡ^
#     try:
#         df = conn.read(worksheet="Matches", ttl=0)
#         if not df.empty:
#             for col in ['남단_선수', '남복_선수', '여복_선수']:
#                 if col in df.columns:
#                     df[col] = df[col].apply(
#                         lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else (
#                             x if isinstance(x, list) else [])
#                     )
#         return df
#     except:
#         return pd.DataFrame()
def load_from_gsheets():
    conn = get_gsheets_conn()
    try:
        # [확인용] 시트에서 읽어오자마자 화면에 냅다 찍어봅니다.
        df = conn.read(worksheet="Matches", ttl=0)

        # 디버깅: 운영 서버에서만 잠깐 켜서 데이터 확인 ㅡㅡ^
        # with st.expander("🔍 [디버그] 구글 시트 원본 데이터 확인"):
        #     st.write("현재 연결된 시트에서 가져온 쌩 데이터입니다:")
        #     st.dataframe(df)
        #     st.write(f"최근 로드 시간: {pd.Timestamp.now()}")

        if not df.empty:
            for col in ['남단_선수', '남복_선수', '여복_선수']:
                if col in df.columns:
                    df[col] = df[col].apply(
                        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else (
                            x if isinstance(x, list) else [])
                    )
        return df
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}")
        return pd.DataFrame()
# def load_from_gsheets():
#     conn = get_gsheets_conn()
#     try:
#         # ttl=0을 줘도 운영 서버는 캐시를 잡을 때가 있으니 주의 ㅡㅡ^
#         df = conn.read(worksheet="Matches", ttl=0)
#         if df.empty: return pd.DataFrame()
#
#         for col in ['남단_선수', '남복_선수', '여복_선수']:
#             if col in df.columns:
#                 def safe_eval(x):
#                     if not isinstance(x, str) or not x.strip(): return []
#                     try:
#                         # 시트의 ['A'], ['B'] 같은 비정상 포맷도 처리 시도 ㅡㅡ^
#                         return ast.literal_eval(x)
#                     except:
#                         return []
#                 df[col] = df[col].apply(safe_eval)
#         return df
#     except Exception as e:
#         # ⭕ 운영 서버 화면에 에러를 표시해서 원인을 잡습니다!
#         st.error(f"⚠️ 시트 로드 에러 (URL이나 권한 확인 필요): {e}")
#         return pd.DataFrame()

# Players 탭 로드 헬퍼 ㅡㅡ^
def load_players_from_gsheets():
    conn = get_gsheets_conn()
    try:
        return conn.read(worksheet="Players", ttl=0)
    except:
        return None


def save_matches_to_gsheets(df):
    if df.empty: return
    conn = get_gsheets_conn()
    save_df = df.copy()
    for col in ['남단_선수', '남복_선수', '여복_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    # Matches 워크시트에 업데이트 ㅡㅡ^
    conn.update(worksheet="Matches", data=save_df)


def save_players_to_gsheets(df):
    if df is None or df.empty: return
    conn = get_gsheets_conn()
    # Players 워크시트에 업데이트 ㅡㅡ^
    conn.update(worksheet="Players", data=df)
    st.success("✅ 선수 명단이 'Players' 탭에 저장되었습니다!")


# --- 3. 데이터 초기화 ---
if 'match_data' not in st.session_state:
    st.session_state.match_data = load_from_gsheets()

if 'player_db' not in st.session_state:
    st.session_state.player_db = load_players_from_gsheets()

if 'groups' not in st.session_state: st.session_state.groups = {}

# 시트 기반 조 정보 복구 ㅡㅡ^
if not st.session_state.match_data.empty:
    unique_groups = sorted(st.session_state.match_data['조'].unique())
    for gn in unique_groups:
        teams = sorted(list(set(
            st.session_state.match_data[st.session_state.match_data['조'] == gn]['홈'].tolist() +
            st.session_state.match_data[st.session_state.match_data['조'] == gn]['어웨이'].tolist()
        )))
        st.session_state.groups[gn] = teams

# --- 4. 메인 화면 ---
st.header("🏆 대회 실시간 운영 센터")

current_role = st.session_state.get('role', 'User')

if current_role == "Admin":
    st.markdown("### ⚙️ 대회 관리 설정 (관리자 전용)")

    with st.expander("📂 1단계: 선수 명단 업로드", expanded=(st.session_state.player_db is None)):
        uploaded_file = st.file_uploader("명단 업로드 (Excel)", type=['xlsx', 'xls'])
        if uploaded_file:
            pdf = pd.read_excel(uploaded_file)
            st.session_state.player_db = pdf
            save_players_to_gsheets(pdf)

    if st.session_state.player_db is not None:
        all_teams = sorted(st.session_state.player_db['소속'].unique().tolist())
        with st.expander("⚖️ 2단계: 조 편성 및 대진표 생성", expanded=st.session_state.match_data.empty):
            num_groups = st.selectbox("조 개수:", [2, 3, 4, 5], index=0)
            group_names = [f"{chr(65 + i)}조" for i in range(num_groups)]

            if st.session_state.player_db is not None:
                all_teams = sorted(st.session_state.player_db['소속'].unique().tolist())
                with st.expander("⚖️ 2단계: 조 편성 및 대진표 생성", expanded=st.session_state.match_data.empty):
                    # key 인자를 추가하여 중복 ID 오류를 해결합니다 ㅡㅡ^
                    num_groups = st.selectbox("조 개수:", [2, 3, 4, 5], index=0, key="num_groups_selector")
                    group_names = [f"{chr(65 + i)}조" for i in range(num_groups)]

                    # 실시간 모든 선택 팀 수집 ㅡㅡ^
                    all_selected_teams = []
                    for g_name in group_names:
                        key = f"sel_{g_name}"
                        if key in st.session_state:
                            all_selected_teams.extend(st.session_state[key])

                    temp_groups = {}

                    for g_name in group_names:
                        key = f"sel_{g_name}"
                        current_selected = st.session_state.get(key, st.session_state.groups.get(g_name, []))

                        # 다른 조에서 선택된 팀 제외 로직 ㅡㅡ^
                        others_selected = [t for t in all_selected_teams if t not in current_selected]
                        available_options = sorted([t for t in all_teams if t not in others_selected])

                        # 💡 [핵심 추가] 현재 엑셀(available_options)에 존재하는 팀만 기본값으로 걸러냅니다.
                        # 과거 세션에 남아있는 'ENM-CM-B' 같은 유령 데이터는 여기서 탈락합니다. ㅡㅡ^
                        valid_default = [t for t in current_selected if t in available_options]

                        selected = st.multiselect(
                            f"📍 {g_name} 팀 선택",
                            options=available_options,
                            default=valid_default,  # 필터링된 안전한 리스트만 통과시킵니다
                            key=key
                        )
                        temp_groups[g_name] = selected

                    if st.button("🚀 대진표 생성 및 시트 저장", key="btn_save_matches"):
                        matches = []
                        for gn, gt in temp_groups.items():
                            for i in range(len(gt)):
                                for j in range(i + 1, len(gt)):
                                    matches.append({
                                        "조": gn, "홈": gt[i], "어웨이": gt[j],
                                        "남단_홈": 0, "남단_어웨이": 0, "남복_홈": 0, "남복_어웨이": 0, "여복_홈": 0, "여복_어웨이": 0,
                                        "남단_선수": [], "남복_선수": [], "여복_선수": [], "확정": False
                                    })
                        st.session_state.match_data = pd.DataFrame(matches)
                        st.session_state.groups = temp_groups
                        save_matches_to_gsheets(st.session_state.match_data)
                        st.rerun()



st.divider()

# --- 5. 실시간 순위 현황 (컬러 적용 및 데이터 타입 수정) ---
if not st.session_state.match_data.empty:
    # --- 수정 후 ---
    def calculate_standings(df_matches, target_group):
        group_teams = st.session_state.groups.get(target_group, [])
        standings = []

        # 교류전이므로 선수 구력 데이터(pdb)는 순위 산정에 사용하지 않습니다.

        # 전체 데이터의 '확정' 열을 숫자형으로 미리 변환 ㅡㅡ^
        df_matches['확정_val'] = pd.to_numeric(df_matches['확정'], errors='coerce').fillna(0)

        for team in group_teams:
            team_str = str(team).strip()

            # 1. 확정된 경기 필터링 강화 (숫자 1 혹은 1.0 등 모두 포함) ㅡㅡ^
            m = df_matches[
                ((df_matches['홈'].astype(str).str.strip() == team_str) |
                 (df_matches['어웨이'].astype(str).str.strip() == team_str)) &
                (df_matches['확정_val'] > 0)
                ]

            w, d, l, gd = 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (str(row['홈']).strip() == team_str)

                # 기존의 세부 종목별 승수 비교 로직 유지
                h_wins = (int(row['남단_홈']) > int(row['남단_어웨이'])) + \
                         (int(row['남복_홈']) > int(row['남복_어웨이'])) + \
                         (int(row['여복_홈']) > int(row['여복_어웨이']))

                a_wins = (int(row['남단_어웨이']) > int(row['남단_홈'])) + \
                         (int(row['남복_어웨이']) > int(row['남복_홈'])) + \
                         (int(row['여복_어웨이']) > int(row['여복_홈']))

                c_gd = (int(row['남단_홈']) - int(row['남단_어웨이'])) + \
                       (int(row['남복_홈']) - int(row['남복_어웨이'])) + \
                       (int(row['여복_홈']) - int(row['여복_어웨이']))

                gd += c_gd if is_home else -c_gd

                if h_wins == a_wins:
                    d += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1
                else:
                    l += 1

            standings.append({
                "팀명": team, "경기": int(len(m)), "승": int(w), "무": int(d), "패": int(l),
                "득실": int(gd)
            })

        df_result = pd.DataFrame(standings).sort_values(
            by=["승", "무", "득실"],
            ascending=[False, False, False]
        ).reset_index(drop=True)

        return df_result

    # 🌟 [추가] 개인별 승률 및 득실 계산 함수 ㅡㅡ^
    def calculate_player_standings(df_matches):
        player_stats = {}

        # '확정' 처리된 데이터만 추출
        df_matches['확정_val'] = pd.to_numeric(df_matches['확정'], errors='coerce').fillna(0)
        df_confirmed = df_matches[df_matches['확정_val'] > 0]

        cats = [('남단_홈', '남단_어웨이', '남단_선수'),
                ('남복_홈', '남복_어웨이', '남복_선수'),
                ('여복_홈', '여복_어웨이', '여복_선수')]

        for _, row in df_confirmed.iterrows():
            for h_col, a_col, p_col in cats:
                h_s, a_s = int(row[h_col]), int(row[a_col])

                # 경기를 치르지 않은 세트(점수가 둘 다 0)는 건너뜀
                if h_s == 0 and a_s == 0:
                    continue

                h_gd = h_s - a_s
                a_gd = a_s - h_s

                if h_s > a_s:
                    h_res, a_res = '승', '패'
                elif h_s < a_s:
                    h_res, a_res = '패', '승'
                else:
                    h_res, a_res = '무', '무'

                ps = row[p_col]
                h_players, a_players = [], []
                if isinstance(ps, list):
                    if len(ps) > 0 and isinstance(ps[0], list): h_players = ps[0]
                    if len(ps) > 1 and isinstance(ps[1], list): a_players = ps[1]

                # 홈팀 선수 전적 기록
                for p in h_players:
                    p = str(p).strip()
                    if not p: continue
                    if p not in player_stats: player_stats[p] = {"경기": 0, "승": 0, "무": 0, "패": 0, "득실": 0}
                    player_stats[p]["경기"] += 1
                    player_stats[p][h_res] += 1
                    player_stats[p]["득실"] += h_gd

                # 어웨이팀 선수 전적 기록
                for p in a_players:
                    p = str(p).strip()
                    if not p: continue
                    if p not in player_stats: player_stats[p] = {"경기": 0, "승": 0, "무": 0, "패": 0, "득실": 0}
                    player_stats[p]["경기"] += 1
                    player_stats[p][a_res] += 1
                    player_stats[p]["득실"] += a_gd

        df_players = pd.DataFrame([{"선수명": k, **v} for k, v in player_stats.items()])
        if not df_players.empty:
            df_players = df_players.sort_values(by=["승", "무", "득실"], ascending=[False, False, False]).reset_index(
                drop=True)
            df_players.index = df_players.index + 1  # 1위부터 보기 좋게 인덱스 조정
        return df_players


    # --- 4. 화면 출력 (구력 컬럼 숨기기) ---
    # for gn in sorted(st.session_state.groups.keys()):
    #     st.markdown(f"#### 📍 {gn} 현황")
    #     df_res = calculate_standings(st.session_state.match_data, gn)
    #
    #     if not df_res.empty:
    #         # 화면에서는 구력을 보여주지 않음 ㅡㅡ^
    #         display_df = df_res.drop(columns=['구력합계'])
    #         # display_df = df_res.copy()
    #         st.dataframe(
    #             display_df.style.highlight_max(subset=['승점'], color='#D1E7DD'),
    #             use_container_width=True,
    #             hide_index=True
    #         )
    # 1. 자동 갱신을 위한 '프래그먼트' 함수 생성 ㅡㅡ^
    # --- 수정 후 ---
    # --- 수정 후 ---
    @st.fragment(run_every=30)
    def show_live_rankings_area():
        live_df = load_from_gsheets()

        if not live_df.empty:
            # --- 1. 팀 현황 ---
            for gn in sorted(st.session_state.groups.keys()):
                st.markdown(f"#### 📍 {gn} 현황 (실시간 업데이트 중)")
                df_res = calculate_standings(live_df, gn)
                if not df_res.empty:
                    st.dataframe(
                        df_res.style.highlight_max(subset=['승'], color='#D1E7DD'),
                        use_container_width=True,
                        hide_index=True
                    )

            st.divider()

            # --- 2. 🌟 참가자 개인 순위 ---
            st.markdown("#### 🏅 참가자 개인 다승 순위")
            df_players = calculate_player_standings(live_df)
            if not df_players.empty:
                st.dataframe(
                    df_players.style.highlight_max(subset=['승'], color='#D1E7DD'),
                    use_container_width=True
                )
            else:
                st.info("아직 확정된 개인 경기 결과가 없습니다.")



            st.divider()
            st.subheader("🔍 팀별 상세 매치 리포트")

            all_teams_list = []
            for teams in st.session_state.groups.values():
                all_teams_list.extend(teams)
            all_teams_list = sorted(list(set(all_teams_list)))

            selected_team = st.selectbox("상세 결과를 보고 싶은 팀을 선택하세요:", options=["선택하세요"] + all_teams_list,
                                         key="team_detail_select")

            if selected_team != "선택하세요":
                # 1. '확정' 여부 상관없이 해당 팀의 모든 경기 로드 ㅡㅡ^
                team_matches = live_df[
                    (live_df['홈'] == selected_team) | (live_df['어웨이'] == selected_team)
                    ]

                if not team_matches.empty:
                    for _, row in team_matches.iterrows():
                        is_home = (row['홈'] == selected_team)
                        opp_team = row['어웨이'] if is_home else row['홈']
                        is_confirmed = str(row['확정']).upper() in ['TRUE', '1', '1.0']

                        status_badge = "✅ 종료" if is_confirmed else "🎾 진행 중"
                        with st.expander(f"{status_badge} | {selected_team} vs {opp_team}", expanded=not is_confirmed):
                            cols = st.columns(3)
                            cats = [('남단', '남단_홈', '남단_어웨이', '남단_선수'),
                                    ('남복', '남복_홈', '남복_어웨이', '남복_선수'),
                                    ('여복', '여복_홈', '여복_어웨이', '여복_선수')]

                            for i, (label, h_col, a_col, p_col) in enumerate(cats):
                                with cols[i]:
                                    h_s, a_s = int(row[h_col]), int(row[a_col])

                                    # 2. 점수가 둘 다 0이면 '진행예정' 표시 ㅡㅡ^
                                    if h_s == 0 and a_s == 0:
                                        st.markdown(f"**{label}**")
                                        st.info("진행예정")
                                    else:
                                        if h_s > a_s:
                                            res = "승" if is_home else "패"
                                        elif h_s < a_s:
                                            res = "패" if is_home else "승"
                                        else:
                                            res = "무"
                                        st.markdown(f"**{label} {res}**")
                                        st.markdown(f"### {h_s if is_home else a_s} : {a_s if is_home else h_s}")

                                    # 선수명 표시 로직
                                    ps = row[p_col]
                                    try:
                                        h_names = ", ".join(ps[0]) if len(ps) > 0 and ps[0] else "미정"
                                        a_names = ", ".join(ps[1]) if len(ps) > 1 and ps[1] else "미정"
                                        st.caption(
                                            f"{h_names if is_home else a_names} VS {a_names if is_home else h_names}")
                                    except:
                                        st.caption("선수 정보 미등록")
                else:
                    st.info(f"'{selected_team}' 팀의 매치업 정보가 없습니다.")

            st.caption(f"🕒 마지막 업데이트: {pd.Timestamp.now().strftime('%H:%M:%S')}")
    # @st.fragment(run_every=30)  # 30초마다 이 함수 안의 코드만 다시 실행!
    # def show_live_rankings_area():
    #     # 2. 핵심: 세션 데이터가 아니라 시트에서 "생으로" 새로 읽어옵니다.
    #     live_df = load_from_gsheets()
    #
    #     if not live_df.empty:
    #         for gn in sorted(st.session_state.groups.keys()):
    #             st.markdown(f"#### 📍 {gn} 현황 (실시간 업데이트 중)")
    #
    #             # 3. 방금 읽어온 따끈따끈한 live_df를 계산 함수에 넣습니다.
    #             df_res = calculate_standings(live_df, gn)
    #
    #             if not df_res.empty:
    #                 display_df = df_res.drop(columns=['구력합계'])
    #                 st.dataframe(
    #                     display_df.style.highlight_max(subset=['승점'], color='#D1E7DD'),
    #                     use_container_width=True,
    #                     hide_index=True
    #                 )
    #         # 언제 마지막으로 갱신됐는지 알려주면 사용자들이 안심합니다.
    #         st.caption(f"🕒 마지막 업데이트: {pd.Timestamp.now().strftime('%H:%M:%S')}")


    # 4. 마지막에 이 함수를 호출해서 화면에 그려줍니다.
    show_live_rankings_area()

    # st.subheader("📊 실시간 조별 순위 (Live)")
    # for gn in sorted(st.session_state.groups.keys()):
    #     st.markdown(f"#### 📍 {gn} 현황")
    #     df_res = calculate_standings(st.session_state.match_data, gn)
    #     if not df_res.empty:
    #         # 득실 컬럼이 확실히 int형인지 보장 ㅡㅡ^
    #         df_res['득실'] = df_res['득실'].astype(int)
    #         st.dataframe(
    #             df_res.style.highlight_max(subset=['승점'], color='#D1E7DD').highlight_min(subset=['패'], color='#F8D7DA'),
    #             use_container_width=True, hide_index=True)
else:
    st.info("📢 대진표 데이터가 없습니다.")