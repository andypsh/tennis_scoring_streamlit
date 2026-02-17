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


def load_from_gsheets():
    conn = get_gsheets_conn()
    # Matches 탭에서 대진표 로드 ㅡㅡ^
    try:
        df = conn.read(worksheet="Matches", ttl=0)
        if not df.empty:
            for col in ['남단_선수', '남복_선수', '여복_선수']:
                if col in df.columns:
                    df[col] = df[col].apply(
                        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else (
                            x if isinstance(x, list) else [])
                    )
        return df
    except:
        return pd.DataFrame()


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

            temp_groups = {}
            already_selected = []  # 다른 조에서 선택된 팀 추적 ㅡㅡ^

            for g_name in group_names:
                # 이전에 이 조에 할당되었던 팀 ㅡㅡ^
                prev_selected = st.session_state.groups.get(g_name, [])
                # 다른 조에서 선택되지 않은 팀 + 현재 이 조에 선택되어 있는 팀 ㅡㅡ^
                available_options = sorted(
                    list(set([t for t in all_teams if t not in already_selected] + prev_selected)))

                selected = st.multiselect(f"📍 {g_name} 팀 선택", options=available_options, default=prev_selected,
                                          key=f"sel_{g_name}")
                temp_groups[g_name] = selected
                already_selected.extend(selected)  # 선택된 팀 리스트 업데이트 ㅡㅡ^

            if st.button("🚀 대진표 생성 및 시트 저장"):
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
    def calculate_standings(df_matches, target_group):
        group_teams = st.session_state.groups.get(target_group, [])
        standings = []
        for team in group_teams:
            m = df_matches[((df_matches['홈'] == team) | (df_matches['어웨이'] == team)) & (df_matches['확정'] == True)]
            w, d, l, pts, gd = 0, 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (row['홈'] == team)
                h_wins = (row['남단_홈'] > row['남단_어웨이']) + (row['남복_홈'] > row['남복_어웨이']) + (row['여복_홈'] > row['여복_어웨이'])
                a_wins = (row['남단_어웨이'] > row['남단_홈']) + (row['남복_어웨이'] > row['남복_홈']) + (row['여복_어웨이'] > row['여복_홈'])
                c_gd = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
                gd += c_gd if is_home else -c_gd
                if h_wins == a_wins:
                    d += 1;
                    pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1;
                    pts += 3
                else:
                    l += 1
            # 득실(gd)을 int형으로 강제 변환하여 저장 ㅡㅡ^
            standings.append(
                {"팀명": team, "경기": int(len(m)), "승": int(w), "무": int(d), "패": int(l), "승점": int(pts), "득실": int(gd)})
        return pd.DataFrame(standings).sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)


    st.subheader("📊 실시간 조별 순위 (Live)")
    for gn in sorted(st.session_state.groups.keys()):
        st.markdown(f"#### 📍 {gn} 현황")
        df_res = calculate_standings(st.session_state.match_data, gn)
        if not df_res.empty:
            # 득실 컬럼이 확실히 int형인지 보장 ㅡㅡ^
            df_res['득실'] = df_res['득실'].astype(int)
            st.dataframe(
                df_res.style.highlight_max(subset=['승점'], color='#D1E7DD').highlight_min(subset=['패'], color='#F8D7DA'),
                use_container_width=True, hide_index=True)
else:
    st.info("📢 대진표 데이터가 없습니다.")