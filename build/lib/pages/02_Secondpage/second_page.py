import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import ast


# --- 1. 구글 시트 연동 헬퍼 ---
def get_gsheets_conn():
    return st.connection("gsheets", type=GSheetsConnection)


def load_data():
    conn = get_gsheets_conn()
    # 1. 대진표 로드 (기본 탭)
    try:
        m_df = conn.read(ttl="5s")
        for col in ['남단_선수', '남복_선수', '여복_선수']:
            if col in m_df.columns:
                m_df[col] = m_df[col].apply(
                    lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x)
    except:
        m_df = pd.DataFrame()

    # 2. 명단 로드 (PlayerList 탭) ㅡㅡ^
    try:
        p_df = conn.read(worksheet="PlayerList", ttl="60s")
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
    conn.update(data=save_df)
    st.success("✅ 저장 완료!")


# --- 2. 앱 실행 시 자동 데이터 복구 --- ㅡㅡ^
st.session_state.match_data, st.session_state.player_db = load_data()

# 조(Groups) 정보가 세션에서 사라졌을 경우 대진표에서 역추적 ㅡㅡ^
if not st.session_state.match_data.empty:
    unique_groups = sorted(st.session_state.match_data['조'].unique())
    st.session_state.groups = {gn: [] for gn in unique_groups}

# --- 3. 에러 체크 및 화면 구성 ---
st.header("📝 실시간 경기 스코어보드 입력")

if st.session_state.player_db is None or st.session_state.match_data.empty:
    st.error("❌ 명단 또는 대진표가 없습니다.")
    st.info("💡 해결방법: FIRST_PAGE에서 명단을 올리고 [대진표 생성] 버튼을 꼭 눌러주세요!")
    st.stop()


# --- 이하 로직 (동일) ---
@st.dialog("📝 경기 결과 최종 확인")
def confirm_save_dialog(idx, m_type, v_h, v_a, l_h, l_a, finalized):
    curr = st.session_state.match_data.loc[idx]
    st.write(f"### ⚔️ {m_type} 결과 확인")
    st.write(f"**{curr['홈']}**: {', '.join(l_h)} ({v_h}점)")
    st.write(f"**{curr['어웨이']}**: {', '.join(l_a)} ({v_a}점)")
    st.divider()

    c1, c2 = st.columns(2)
    if c1.button("✅ 저장", use_container_width=True):
        st.session_state.match_data.at[idx, f"{m_type}_홈"] = v_h
        st.session_state.match_data.at[idx, f"{m_type}_어웨이"] = v_a
        st.session_state.match_data.at[idx, f"{m_type}_선수"] = [l_h, l_a]
        st.session_state.match_data.at[idx, '확정'] = finalized
        save_to_gsheets(st.session_state.match_data)
        st.rerun()
    if c2.button("❌ 취소", use_container_width=True): st.rerun()


# 필터 및 입력 UI... (생략 없이 기존 코드와 동일하게 작동)
available_groups = ["전체"] + list(st.session_state.groups.keys())
f_group = st.radio("조 필터:", available_groups, horizontal=True)
m_df = st.session_state.match_data
if f_group != "전체": m_df = m_df[m_df['조'] == f_group]

opts = [f"[{r['조']}] {r['홈']} vs {r['어웨이']}" for _, r in m_df.iterrows()]
sel_raw = st.selectbox("대진 선택:", range(len(opts)), format_func=lambda x: opts[x])
real_idx = m_df.index[sel_raw]
curr_match = st.session_state.match_data.loc[real_idx]

st.markdown("---")
m_type = st.radio("🔢 종목 선택:", ["남단", "남복", "여복"], horizontal=True)

# (선수 라인업 필터링 및 multiselect 로직 그대로 유지...)
pdb = st.session_state.player_db.copy()
pdb['소속'] = pdb['소속'].astype(str).str.strip()
pdb['성별'] = pdb['성별'].astype(str).str.strip()
gender_query = "남" if m_type in ["남단", "남복"] else "여"
p_count = 1 if m_type == "남단" else 2

h_filtered = pdb[(pdb['소속'] == curr_match['홈'].strip()) & (pdb['성별'].str.contains(gender_query))]['이름'].tolist()
a_filtered = pdb[(pdb['소속'] == curr_match['어웨이'].strip()) & (pdb['성별'].str.contains(gender_query))]['이름'].tolist()

l_col, r_col = st.columns(2)
with l_col:
    st.markdown(f"**🏠 {curr_match['홈']}**")
    sel_h = st.multiselect(f"선수", h_filtered, max_selections=p_count, key=f"h_{real_idx}_{m_type}")
    sc_h = st.number_input("점수", 0, 6, key=f"sh_{real_idx}_{m_type}")
with r_col:
    st.markdown(f"**🚀 {curr_match['어웨이']}**")
    sel_a = st.multiselect(f"선수 ", a_filtered, max_selections=p_count, key=f"a_{real_idx}_{m_type}")
    sc_a = st.number_input("점수 ", 0, 6, key=f"sa_{real_idx}_{m_type}")

if st.button("💾 데이터 저장", use_container_width=True):
    if len(sel_h) == p_count and len(sel_a) == p_count:
        confirm_save_dialog(real_idx, m_type, sc_h, sc_a, sel_h, sel_a, True)
    else:
        st.error(f"❌ 인원수를 맞추세요.")