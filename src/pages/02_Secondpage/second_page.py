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
        /* 블러 처리를 위한 스타일 ㅡㅡ^ */
        .blur-container { filter: blur(4px); pointer-events: none; opacity: 0.6; }
        .entered-msg { background-color: #ff4b4b; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)


# --- 2. 구글 시트 연동 헬퍼 ---
def get_gsheets_conn():
    return st.connection("gsheets", type=GSheetsConnection)


def load_data():
    conn = get_gsheets_conn()
    try:
        m_df = conn.read(worksheet="Matches", ttl=0)
        if not m_df.empty:
            for col in ['남단_선수', '남복_선수', '여복_선수']:
                if col in m_df.columns:
                    m_df[col] = m_df[col].apply(
                        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else (
                            x if isinstance(x, list) else [])
                    )
    except:
        m_df = pd.DataFrame()

    try:
        p_df = conn.read(worksheet="Players", ttl=0)
    except:
        p_df = None

    return m_df, p_df


def save_to_gsheets(df):
    if df.empty: return
    conn = get_gsheets_conn()
    save_df = df.copy()
    for col in ['남단_선수', '남복_선수', '여복_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    conn.update(worksheet="Matches", data=save_df)
    st.success("✅ 경기 결과가 구글 시트에 저장되었습니다!")


# --- 3. 데이터 동기화 ---
if 'match_data' not in st.session_state or 'player_db' not in st.session_state:
    st.session_state.match_data, st.session_state.player_db = load_data()

if not st.session_state.match_data.empty:
    unique_groups = sorted(st.session_state.match_data['조'].unique())
    st.session_state.groups = {gn: sorted(list(set(
        st.session_state.match_data[st.session_state.match_data['조'] == gn]['홈'].tolist() +
        st.session_state.match_data[st.session_state.match_data['조'] == gn]['어웨이'].tolist()
    ))) for gn in unique_groups}
else:
    st.session_state.groups = {}

# --- 4. 화면 구성 ---
st.header("📝 실시간 경기 스코어보드 입력")

if st.sidebar.button("🔄 데이터 새로고침"):
    st.session_state.match_data, st.session_state.player_db = load_data()
    st.rerun()

if st.session_state.player_db is None or st.session_state.match_data.empty:
    st.error("❌ 데이터를 불러올 수 없습니다. FIRST_PAGE 설정을 확인하세요.")
    st.stop()


# --- 5. 입력 및 저장 로직 ---
@st.dialog("📝 경기 결과 최종 확인")
def confirm_save_dialog(idx, m_type, v_h, v_a, l_h, l_a, finalized):
    curr = st.session_state.match_data.loc[idx]
    st.write(f"### ⚔️ {m_type} 결과 확인")
    st.write(f"**{curr['홈']}**: {', '.join(l_h)} ({v_h}점)")
    st.write(f"**{curr['어웨이']}**: {', '.join(l_a)} ({v_a}점)")
    st.divider()

    c1, c2 = st.columns(2)
    if c1.button("✅ 저장", use_container_width=True):
        st.session_state.match_data.at[idx, f"{m_type}_홈"] = int(v_h)
        st.session_state.match_data.at[idx, f"{m_type}_어웨이"] = int(v_a)
        st.session_state.match_data.at[idx, f"{m_type}_선수"] = [l_h, l_a]
        save_to_gsheets(st.session_state.match_data)
        st.rerun()
    if c2.button("❌ 취소", use_container_width=True): st.rerun()


f_group = st.radio("조 필터:", ["전체"] + list(st.session_state.groups.keys()), horizontal=True)
m_df = st.session_state.match_data.copy()
if f_group != "전체": m_df = m_df[m_df['조'] == f_group]

if not m_df.empty:
    opts = [f"[{r['조']}] {r['홈']} vs {r['어웨이']}" for _, r in m_df.iterrows()]
    sel_raw = st.selectbox("대진 선택:", range(len(opts)), format_func=lambda x: opts[x])
    real_idx = m_df.index[sel_raw]
    curr_match = st.session_state.match_data.loc[real_idx]

    st.markdown("---")
    m_type = st.radio("🔢 종목 선택:", ["남단", "남복", "여복"], horizontal=True)

    # --- [데이터 검증 및 에러 방지 안전장치] ㅡㅡ^ ---
    raw_saved = curr_match.get(f"{m_type}_선수", [[], []])
    # 만약 데이터가 [ [], [] ] 형식이 아니면(빈 리스트 등) 초기화해줌 ㅡㅡ^
    if not isinstance(raw_saved, list) or len(raw_saved) < 2:
        saved_lineup = [[], []]
    else:
        saved_lineup = raw_saved

    # 이미 입력된 데이터인지 확인 ㅡㅡ^
    is_already_entered = len(saved_lineup[0]) > 0 and len(saved_lineup[1]) > 0

    if is_already_entered:
        st.markdown('<div class="entered-msg">⚠️ 이 경기는 이미 입력되었습니다! 수정을 원하시면 관리자에게 문의하세요.</div>', unsafe_allow_html=True)

    # 블러 처리를 위한 컨테이너 시작 ㅡㅡ^
    input_container = st.container()
    if is_already_entered:
        st.markdown('<div class="blur-container">', unsafe_allow_html=True)

    with input_container:
        pdb = st.session_state.player_db.copy()
        gender_query = "남" if m_type in ["남단", "남복"] else "여"
        p_count = 1 if m_type == "남단" else 2


        # 중복 출전 방지 로직 ㅡㅡ^
        def get_already_played(side_idx):
            played = []
            for t in ["남단", "남복", "여복"]:
                if t != m_type:
                    lineup = curr_match.get(f"{t}_선수", [])
                    if isinstance(lineup, list) and len(lineup) > side_idx:
                        p_list = lineup[side_idx]
                        played.extend(p_list if isinstance(p_list, list) else [p_list])
            return [p for p in played if p]


        h_played = get_already_played(0)
        a_played = get_already_played(1)

        # 기존 값 불러오기 ㅡㅡ^
        def_h_players = saved_lineup[0]
        def_a_players = saved_lineup[1]
        def_h_score = int(curr_match.get(f"{m_type}_홈", 0))
        def_a_score = int(curr_match.get(f"{m_type}_어웨이", 0))

        # 필터링 및 옵션 구성 ㅡㅡ^
        h_options = sorted(list(set(pdb[(pdb['소속'].astype(str).str.strip() == str(curr_match['홈']).strip()) &
                                        (pdb['성별'].astype(str).str.contains(gender_query)) &
                                        (~pdb['이름'].isin(h_played))]['이름'].tolist() + def_h_players)))

        a_options = sorted(list(set(pdb[(pdb['소속'].astype(str).str.strip() == str(curr_match['어웨이']).strip()) &
                                        (pdb['성별'].astype(str).str.contains(gender_query)) &
                                        (~pdb['이름'].isin(a_played))]['이름'].tolist() + def_a_players)))

        l_col, r_col = st.columns(2)
        with l_col:
            st.markdown(f"**🏠 {curr_match['홈']}**")
            sel_h = st.multiselect(f"선수", h_options, default=def_h_players, max_selections=p_count,
                                   key=f"h_{real_idx}_{m_type}", disabled=is_already_entered)
            sc_h = st.number_input("점수", 0, 6, value=def_h_score, key=f"sh_{real_idx}_{m_type}",
                                   disabled=is_already_entered)
        with r_col:
            st.markdown(f"**🚀 {curr_match['어웨이']}**")
            sel_a = st.multiselect(f"선수 ", a_options, default=def_a_players, max_selections=p_count,
                                   key=f"a_{real_idx}_{m_type}", disabled=is_already_entered)
            sc_a = st.number_input("점수 ", 0, 6, value=def_a_score, key=f"sa_{real_idx}_{m_type}",
                                   disabled=is_already_entered)

        if st.button("💾 데이터 저장 (구글 시트 동기화)", use_container_width=True, disabled=is_already_entered):
            if len(sel_h) == p_count and len(sel_a) == p_count:
                confirm_save_dialog(real_idx, m_type, sc_h, sc_a, sel_h, sel_a, True)
            else:
                st.error(f"❌ {p_count}명의 선수를 선택해 주세요.")

    if is_already_entered:
        st.markdown('</div>', unsafe_allow_html=True)