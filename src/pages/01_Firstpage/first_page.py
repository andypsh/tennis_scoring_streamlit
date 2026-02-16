import streamlit as st
import pandas as pd
import sqlite3
import ast

# --- DB Helper ---
DB_FILE = "tennis_data.db"
def save_to_db(df):
    conn = sqlite3.connect(DB_FILE)
    save_df = df.copy()
    for col in ['남단_선수', '남복_선수', '여복_선수']:
        save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    save_df.to_sql('matches', conn, if_exists='replace', index=True, index_label='idx')
    conn.commit()
    conn.close()

def load_from_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql('SELECT * FROM matches', conn).set_index('idx')
        conn.close()
        for col in ['남단_선수', '남복_선수', '여복_선수']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x)
        return df
    except: return pd.DataFrame()

# --- 1. UI 및 CSS ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container { padding-top: 0rem !important; margin-top: 0rem !important; max-width: 95% !important; }
        .stHeadingContainer { margin-bottom: -1.5rem !important; }
        hr { margin-top: 0.5rem !important; margin-bottom: 1rem !important; }
        .group-card { background-color: #ffffff; border-radius: 12px; border: 1px solid #e0e0e0; border-top: 6px solid #FF4B4B; padding: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .group-title { font-size: 1.5rem; font-weight: 800; color: #1E1E1E; margin-bottom: 18px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 세션 및 물리 데이터 동기화 ㅡㅡ^ ---
if 'player_db' not in st.session_state: st.session_state.player_db = None
if 'groups' not in st.session_state: st.session_state.groups = {}
# 물리 DB에서 데이터 로드
db_data = load_from_db()
st.session_state.match_data = db_data if not db_data.empty else pd.DataFrame()

if 'mode' not in st.session_state: st.session_state.mode = "토너먼트 (조별 예선)"
if 'role' not in st.session_state: st.session_state.role = "Public"
if 'num_groups' not in st.session_state: st.session_state.num_groups = 2

# --- 3. 사이드바 ---
with st.sidebar:
    st.title("🔐 사용자 인증")
    if st.session_state.role == "Public":
        input_user = st.text_input("아이디")
        input_pw = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            if input_user == st.secrets["auth"]["admin_user"] and input_pw == st.secrets["auth"]["admin_password"]:
                st.session_state.role = "Admin"; st.rerun()
            elif input_user == st.secrets["auth"]["general_user"] and input_pw == st.secrets["auth"]["general_password"]:
                st.session_state.role = "User"; st.rerun()
            else: st.error("정보 불일치")
    else:
        st.write(f"✅ **{st.session_state.role}** 접속 중")
        if st.button("로그아웃"): st.session_state.role = "Public"; st.rerun()

# --- 4. 메인 화면 ---
st.header("🏆 대회 실시간 운영 센터")

if st.session_state.role == "Admin":
    st.markdown("### ⚙️ 대회 관리 설정")
    st.session_state.mode = st.radio("대회 유형 설정:", ["토너먼트 (조별 예선)", "교류전 (2개 팀 맞대결)"], index=0 if "토너먼트" in st.session_state.mode else 1, horizontal=True)

    with st.expander("📂 1단계: 선수 명단 업로드", expanded=(st.session_state.player_db is None)):
        uploaded_file = st.file_uploader("명단 업로드", type=['xlsx', 'xls'])
        if uploaded_file:
            st.session_state.player_db = pd.read_excel(uploaded_file); st.success("✅ 로드 완료")

    if st.session_state.player_db is not None:
        all_teams = sorted(st.session_state.player_db['소속'].unique().tolist())
        if "토너먼트" in st.session_state.mode:
            with st.expander("⚖️ 2단계: 조 편성", expanded=st.session_state.match_data.empty):
                group_opts = [2, 3, 4, 5]
                num_groups = st.selectbox("조 개수:", group_opts, index=group_opts.index(st.session_state.num_groups))
                st.session_state.num_groups = num_groups
                group_names = [f"{chr(65 + i)}조" for i in range(num_groups)]
                temp_groups = {}
                already_selected = []
                for g_name in group_names:
                    avail = [t for t in all_teams if t not in already_selected]
                    prev = st.session_state.groups.get(g_name, [])
                    selected = st.multiselect(f"📍 {g_name} 선택", options=sorted(list(set(avail + prev))), default=prev, key=f"sel_{g_name}")
                    temp_groups[g_name] = selected; already_selected.extend(selected)

                if st.button("🚀 대진표 생성 및 물리 DB 초기화"):
                    matches = []
                    for gn, gt in temp_groups.items():
                        for i in range(len(gt)):
                            for j in range(i + 1, len(gt)):
                                matches.append({"조": gn, "홈": gt[i], "어웨이": gt[j], "남단_홈": 0, "남단_어웨이": 0, "남복_홈": 0, "남복_어웨이": 0, "여복_홈": 0, "여복_어웨이": 0, "남단_선수": [], "남복_선수": [], "여복_선수": [], "확정": False})
                    st.session_state.match_data = pd.DataFrame(matches)
                    st.session_state.groups = temp_groups
                    save_to_db(st.session_state.match_data) # 초기화 시 DB 저장 ㅡㅡ^
                    st.rerun()

st.divider()

# --- 5. 실시간 순위 현황 ---
if not st.session_state.match_data.empty:
    def calculate_standings(df_matches, target_group):
        if target_group not in st.session_state.groups: return pd.DataFrame()
        group_teams = st.session_state.groups[target_group]
        standings = []
        for team in group_teams:
            m = df_matches[((df_matches['홈'] == team) | (df_matches['어웨이'] == team)) & (df_matches['확정'] == 1)]
            w, d, l, pts, gd = 0, 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (row['홈'] == team)
                h_wins = (row['남단_홈'] > row['남단_어웨이']) + (row['남복_홈'] > row['남복_어웨이']) + (row['여복_홈'] > row['여복_어웨이'])
                a_wins = (row['남단_어웨이'] > row['남단_홈']) + (row['남복_어웨이'] > row['남복_홈']) + (row['여복_어웨이'] > row['여복_홈'])
                c_gd = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
                gd += c_gd if is_home else -c_gd
                if h_wins == a_wins: d += 1; pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home): w += 1; pts += 3
                else: l += 1
            standings.append({"팀명": team, "경기": len(m), "승": w, "무": d, "패": l, "승점": pts, "득실": gd})
        return pd.DataFrame(standings).sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)

    st.subheader("📊 실시간 조별 순위 (Live)")
    for gn in st.session_state.groups.keys():
        with st.container():
            st.markdown(f'<div class="group-card"><div class="group-title">📍 {gn} 현황</div></div>', unsafe_allow_html=True)
            df_res = calculate_standings(st.session_state.match_data, gn)
            if not df_res.empty:
                st.dataframe(df_res.style.highlight_max(subset=['승점'], color='#D1E7DD').highlight_min(subset=['패'], color='#F8D7DA'), use_container_width=True, hide_index=True)