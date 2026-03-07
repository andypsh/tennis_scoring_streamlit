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

                        selected = st.multiselect(
                            f"📍 {g_name} 팀 선택",
                            options=available_options,
                            default=current_selected,
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
        pdb = st.session_state.player_db

        # 전체 데이터의 '확정' 열을 숫자형으로 미리 변환 ㅡㅡ^
        df_matches['확정_val'] = pd.to_numeric(df_matches['확정'], errors='coerce').fillna(0)

        for team in group_teams:
            team_str = str(team).strip()

            # 1. 확정된 경기 필터링 강화 (숫자 1 혹은 1.0 등 모두 포함) ㅡㅡ^
            # 홈/어웨이 팀 이름도 공백 제거 후 비교하도록 수정
            m = df_matches[
                ((df_matches['홈'].astype(str).str.strip() == team_str) |
                 (df_matches['어웨이'].astype(str).str.strip() == team_str)) &
                (df_matches['확정_val'] > 0)
                ]

            team_total_career = 0
            # ... (구력 계산 로직은 동일) ...

            w, d, l, pts, gd = 0, 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (str(row['홈']).strip() == team_str)

                # 점수 데이터 형변환 에러 방지 ㅡㅡ^
                h_score = int(row['남단_홈']) + int(row['남복_홈']) + int(row['여복_홈'])  # 단순 합계 예시 (세부 승수 로직 적용 가능)

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
                    d += 1;
                    pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1;
                    pts += 3
                else:
                    l += 1

            standings.append({
                "팀명": team, "경기": int(len(m)), "승": int(w), "무": int(d), "패": int(l),
                "승점": int(pts), "득실": int(gd), "구력합계": float(team_total_career)
            })

        # 정렬 및 결과 반환
        df_result = pd.DataFrame(standings).sort_values(
            by=["승점", "득실", "구력합계"],
            ascending=[False, False, True]
        ).reset_index(drop=True)

        return df_result
    # def calculate_standings(df_matches, target_group):
    #     group_teams = st.session_state.groups.get(target_group, [])
    #     standings = []
    #     pdb = st.session_state.player_db
    #
    #     for team in group_teams:
    #         # 1. 확정된 경기만 필터링 ㅡㅡ^
    #         m = df_matches[((df_matches['홈'] == team) | (df_matches['어웨이'] == team)) &
    #                        (df_matches['확정'].astype(str).str.upper().isin(['TRUE', '1']))]
    #
    #         # 2. 구력 합산 (텍스트에서 숫자만 추출) ㅡㅡ^
    #         team_total_career = 0
    #         if pdb is not None and '구력' in pdb.columns:
    #             team_mask = pdb['소속'].astype(str).str.strip() == str(team).strip()
    #             # '7년', '0.5년'에서 숫자(정수/소수점)만 추출하는 마법 ㅡㅡ^
    #             career_values = pdb[team_mask]['구력'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
    #             team_career_numeric = pd.to_numeric(career_values, errors='coerce').fillna(0)
    #             team_total_career = team_career_numeric.sum()
    #
    #         w, d, l, pts, gd = 0, 0, 0, 0, 0
    #         for _, row in m.iterrows():
    #             is_home = (row['홈'] == team)
    #             h_wins = (int(row['남단_홈']) > int(row['남단_어웨이'])) + (int(row['남복_홈']) > int(row['남복_어웨이'])) + (
    #                         int(row['여복_홈']) > int(row['여복_어웨이']))
    #             a_wins = (int(row['남단_어웨이']) > int(row['남단_홈'])) + (int(row['남복_어웨이']) > int(row['남복_홈'])) + (
    #                         int(row['여복_어웨이']) > int(row['여복_홈']))
    #             c_gd = (int(row['남단_홈']) - int(row['남단_어웨이'])) + (int(row['남복_홈']) - int(row['남복_어웨이'])) + (
    #                         int(row['여복_홈']) - int(row['여복_어웨이']))
    #             gd += c_gd if is_home else -c_gd
    #
    #             if h_wins == a_wins:
    #                 d += 1; pts += 1
    #             elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
    #                 w += 1; pts += 3
    #             else:
    #                 l += 1
    #
    #         standings.append({
    #             "팀명": team, "경기": int(len(m)), "승": int(w), "무": int(d), "패": int(l),
    #             "승점": int(pts), "득실": int(gd), "구력합계": float(team_total_career)
    #         })
    #
    #     # 3. 정렬 (승점 내림 -> 득실 내림 -> 구력합계 오름차순) ㅡㅡ^
    #     df_result = pd.DataFrame(standings).sort_values(
    #         by=["승점", "득실", "구력합계"],
    #         ascending=[False, False, True]
    #     ).reset_index(drop=True)
    #
    #     return df_result


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
    @st.fragment(run_every=30)  # 30초마다 이 함수 안의 코드만 다시 실행!
    def show_live_rankings_area():
        # 2. 핵심: 세션 데이터가 아니라 시트에서 "생으로" 새로 읽어옵니다.
        live_df = load_from_gsheets()

        if not live_df.empty:
            for gn in sorted(st.session_state.groups.keys()):
                st.markdown(f"#### 📍 {gn} 현황 (실시간 업데이트 중)")

                # 3. 방금 읽어온 따끈따끈한 live_df를 계산 함수에 넣습니다.
                df_res = calculate_standings(live_df, gn)

                if not df_res.empty:
                    display_df = df_res.drop(columns=['구력합계'])
                    st.dataframe(
                        display_df.style.highlight_max(subset=['승점'], color='#D1E7DD'),
                        use_container_width=True,
                        hide_index=True
                    )
            # 언제 마지막으로 갱신됐는지 알려주면 사용자들이 안심합니다.
            st.caption(f"🕒 마지막 업데이트: {pd.Timestamp.now().strftime('%H:%M:%S')}")


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