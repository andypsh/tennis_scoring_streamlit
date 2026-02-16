import streamlit as st
import pandas as pd

# --- [저장 확인 팝업창] ---
@st.dialog("📝 경기 결과 최종 확인")
def confirm_save_dialog(idx, m_type, v_h, v_a, l_h, l_a, finalized):
    curr = st.session_state.match_data.iloc[idx]
    st.write(f"### ⚔️ {m_type} 결과 확인")
    st.write(f"**{curr['홈']}**: {', '.join(l_h)} ({v_h}점)")
    st.write(f"**{curr['어웨이']}**: {', '.join(l_a)} ({v_a}점)")
    st.divider()

    c1, c2 = st.columns(2)
    if c1.button("✅ 데이터 저장", use_container_width=True):
        st.session_state.match_data.at[idx, f"{m_type}_홈"] = v_h
        st.session_state.match_data.at[idx, f"{m_type}_어웨이"] = v_a
        st.session_state.match_data.at[idx, f"{m_type}_선수"] = [l_h, l_a]
        st.session_state.match_data.at[idx, '확정'] = finalized
        st.success("성공적으로 저장되었습니다!")
        st.rerun()

    if c2.button("❌ 취소", use_container_width=True):
        st.rerun()

# --- [메인 입력 섹션] ---
st.header("📝 실시간 경기 스코어보드 입력")
st.markdown("<hr style='border-top: 3px solid black; margin-top: 10px; margin-bottom: 20px'/>", unsafe_allow_html=True)

# 0. 데이터 존재 여부 체크 (groups 포함)
if 'match_data' not in st.session_state or 'player_db' not in st.session_state or 'groups' not in st.session_state:
    st.warning("⚠️ FIRST_PAGE에서 명단 업로드 및 조 편성을 먼저 완료해 주세요.")
    st.stop()

# 1. 조 필터 연동 (FIRST_PAGE의 groups 정보 사용) ㅡㅡ^
available_groups = ["전체"] + list(st.session_state.groups.keys())

filter_col1, filter_col2 = st.columns([1, 2])
with filter_col1:
    f_group = st.radio("조 필터:", available_groups, horizontal=True)

m_df = st.session_state.match_data
if f_group != "전체":
    m_df = m_df[m_df['조'] == f_group]

# 2. 대진 선택
m_opts = [f"[{r['조']}] {r['홈']} vs {r['어웨이']}" for _, r in m_df.iterrows()]
with filter_col2:
    selected_idx_raw = st.selectbox("진행할 대진을 선택하세요:", range(len(m_opts)), format_func=lambda x: m_opts[x])

real_idx = m_df.index[selected_idx_raw]
curr_match = st.session_state.match_data.iloc[real_idx]

# 3. 종목 선택
st.markdown("---")
m_type = st.radio("🔢 종목 선택:", ["남단", "남복", "여복"], horizontal=True)

# 4. 중복 출전 방지 로직
used_h, used_a = [], []
for match_name in ["남단", "남복", "여복"]:
    if match_name != m_type:
        lineup = curr_match.get(f"{match_name}_선수", [])
        if lineup and len(lineup) == 2:
            used_h.extend(lineup[0]); used_a.extend(lineup[1])

# 5. 라인업 입력
pdb = st.session_state.player_db
gender = "남" if m_type in ["남단", "남복"] else "여"
p_count = 1 if m_type == "남단" else 2

h_pool = [p for p in pdb[(pdb['소속']==curr_match['홈']) & (pdb['성별']==gender)]['이름'].tolist() if p not in used_h]
a_pool = [p for p in pdb[(pdb['소속']==curr_match['어웨이']) & (pdb['성별']==gender)]['이름'].tolist() if p not in used_a]

l_col, r_col = st.columns(2)
with l_col:
    st.markdown(f'<div style="background-color:#f0f2f6; padding:10px; border-radius:10px; text-align:center;"><b>🏠 {curr_match["홈"]}</b></div>', unsafe_allow_html=True)
    sel_h = st.multiselect("선수 명단", h_pool, max_selections=p_count, key=f"h_l_{real_idx}_{m_type}")
    sc_h = st.number_input("세트 스코어", 0, 6, key=f"h_s_{real_idx}_{m_type}")

with r_col:
    st.markdown(f'<div style="background-color:#f0f2f6; padding:10px; border-radius:10px; text-align:center;"><b>🚀 {curr_match["어웨이"]}</b></div>', unsafe_allow_html=True)
    sel_a = st.multiselect("선수 명단 ", a_pool, max_selections=p_count, key=f"a_l_{real_idx}_{m_type}")
    sc_a = st.number_input("세트 스코어 ", 0, 6, key=f"a_s_{real_idx}_{m_type}")

is_final = st.checkbox("이 매치를 최종 결과로 확정합니다.", value=curr_match['확정'])

if st.button("💾 경기 데이터 저장하기", use_container_width=True):
    if len(sel_h) == p_count and len(sel_a) == p_count:
        confirm_save_dialog(real_idx, m_type, sc_h, sc_a, sel_h, sel_a, is_final)
    else:
        st.error(f"❌ {m_type} 인원 수({p_count}명)를 정확히 선택하세요.")