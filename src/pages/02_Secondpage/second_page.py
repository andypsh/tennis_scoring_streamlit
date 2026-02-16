import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import ast

# --- 1. 구글 시트 연동 헬퍼 (SQLite 대체) --- ㅡㅡ^
def get_gsheets_conn():
    return st.connection("gsheets", type=GSheetsConnection)

def load_from_gsheets():
    conn = get_gsheets_conn()
    try:
        df = conn.read(ttl="5s")
        for col in ['남단_선수', '남복_선수', '여복_선수']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x)
        return df
    except: return pd.DataFrame()

def save_to_gsheets(df):
    if df.empty: return
    conn = get_gsheets_conn()
    save_df = df.copy()
    for col in ['남단_선수', '남복_선수', '여복_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    conn.update(data=save_df)
    st.success("✅ 구글 시트에 실시간 저장되었습니다!")

# --- 2. 저장 확인 팝업창 (구글 시트 저장 로직으로 교체) ---
@st.dialog("📝 경기 결과 최종 확인")
def confirm_save_dialog(idx, m_type, v_h, v_a, l_h, l_a, finalized):
    curr = st.session_state.match_data.loc[idx]
    st.write(f"### ⚔️ {m_type} 결과 확인")
    st.write(f"**{curr['홈']}**: {', '.join(l_h)} ({v_h}점)")
    st.write(f"**{curr['어웨이']}**: {', '.join(l_a)} ({v_a}점)")
    st.divider()

    c1, c2 = st.columns(2)
    if c1.button("✅ 구글 시트 저장", use_container_width=True):
        # 1. 세션 업데이트
        st.session_state.match_data.at[idx, f"{m_type}_홈"] = v_h
        st.session_state.match_data.at[idx, f"{m_type}_어웨이"] = v_a
        st.session_state.match_data.at[idx, f"{m_type}_선수"] = [l_h, l_a]
        st.session_state.match_data.at[idx, '확정'] = finalized
        # 2. 구글 시트 동기화 ㅡㅡ^
        save_to_gsheets(st.session_state.match_data)
        st.rerun()
    if c2.button("❌ 취소", use_container_width=True): st.rerun()

# --- 3. UI 및 데이터 로드 ---
st.header("📝 실시간 경기 스코어보드 입력")
st.markdown("<hr style='border-top: 3px solid black; margin-top: 10px; margin-bottom: 20px'/>", unsafe_allow_html=True)

# 최신 구글 시트 데이터 로드
st.session_state.match_data = load_from_gsheets()

# 🚨 [에러 방어] 데이터 존재 여부 체크 (Specialist님을 위한 핵심 로직 ㅡㅡ^)
if 'match_data' not in st.session_state or st.session_state.player_db is None:
    st.error("❌ 명단 데이터가 없습니다! FIRST_PAGE에서 엑셀 업로드를 먼저 해주세요.")
    st.stop()

# --- 4. 필터 및 대진 선택 ---
available_groups = ["전체"] + list(st.session_state.groups.keys()) if st.session_state.groups else ["전체"]
f_group = st.radio("조 필터:", available_groups, horizontal=True)
m_df = st.session_state.match_data
if f_group != "전체": m_df = m_df[m_df['조'] == f_group]

if m_df.empty:
    st.warning("선택한 조에 경기 데이터가 없습니다.")
    st.stop()

opts = [f"[{r['조']}] {r['홈']} vs {r['어웨이']}" for _, r in m_df.iterrows()]
sel_raw = st.selectbox("대진 선택:", range(len(opts)), format_func=lambda x: opts[x])
real_idx = m_df.index[sel_raw]
curr_match = st.session_state.match_data.loc[real_idx]

st.markdown("---")
m_type = st.radio("🔢 종목 선택:", ["남단", "남복", "여복"], horizontal=True)

# --- 5. 선수 필터링 및 입력 ---
used_h, used_a = [], []
for mt in ["남단", "남복", "여복"]:
    if mt != m_type:
        lineup = curr_match.get(f"{mt}_선수")
        if isinstance(lineup, list) and len(lineup) == 2:
            used_h.extend(lineup[0]); used_a.extend(lineup[1])

# 여기서 copy() 에러 방어가 완료되었습니다 ㅡㅡ^
pdb = st.session_state.player_db.copy()
pdb['소속'] = pdb['소속'].astype(str).str.strip()
pdb['성별'] = pdb['성별'].astype(str).str.strip()
gender_query = "남" if m_type in ["남단", "남복"] else "여"
p_count = 1 if m_type == "남단" else 2

h_filtered = pdb[(pdb['소속'] == curr_match['홈'].strip()) & (pdb['성별'].str.contains(gender_query))]['이름'].tolist()
a_filtered = pdb[(pdb['소속'] == curr_match['어웨이'].strip()) & (pdb['성별'].str.contains(gender_query))]['이름'].tolist()
h_pool = [p for p in h_filtered if p not in used_h]
a_pool = [p for p in a_filtered if p not in used_a]

l_col, r_col = st.columns(2)
with l_col:
    st.markdown(f"**🏠 {curr_match['홈']}**")
    sel_h = st.multiselect(f"선수 (총 {len(h_pool)}명)", h_pool, max_selections=p_count, key=f"h_{real_idx}_{m_type}")
    sc_h = st.number_input("세트 스코어", 0, 6, key=f"sh_{real_idx}_{m_type}")
with r_col:
    st.markdown(f"**🚀 {curr_match['어웨이']}**")
    sel_a = st.multiselect(f"선수 (총 {len(a_pool)}명)", a_pool, max_selections=p_count, key=f"a_{real_idx}_{m_type}")
    sc_a = st.number_input("세트 스코어 ", 0, 6, key=f"sa_{real_idx}_{m_type}")

if st.button("💾 경기 데이터 저장하기", use_container_width=True):
    if len(sel_h) == p_count and len(sel_a) == p_count:
        confirm_save_dialog(real_idx, m_type, sc_h, sc_a, sel_h, sel_a, True)
    else: st.error(f"❌ {p_count}명을 선택하세요.")