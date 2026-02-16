import streamlit as st
import pandas as pd

# --- 1. UI 및 CSS (디자인 100% 유지) ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container {
            padding-top: 0rem !important;
            margin-top: -1rem !important;
            max-width: 98% !important;
        }
        .match-box {
            border: 2px solid #333; border-radius: 8px; width: 190px;
            background-color: #f9f9f9; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); margin: 10px 0;
        }
        .match-header { background-color: #333; color: white; text-align: center; font-size: 0.85rem; padding: 4px; border-radius: 6px 6px 0 0; font-weight: bold; }
        .team-row { display: flex; justify-content: space-between; padding: 10px 14px; font-weight: bold; font-size: 0.95rem; }
        .team-winner { background-color: #e6fffa; color: #2c7a7b; border-radius: 0 0 6px 6px; }
        .score { color: #007bff; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 예선 데이터 연동 가드 (조 2개 확인) ---
if 'groups' not in st.session_state or len(st.session_state.groups) != 2:
    st.info("ℹ️ 본선 대진표는 예선이 **2개 조(A조, B조)**로 편성된 경우에만 활성화됩니다.")
    st.stop()


def get_live_rankings():
    if 'match_data' not in st.session_state: return None
    df_m = st.session_state.match_data
    g_names = sorted(list(st.session_state.groups.keys()))
    res = []
    for gn in g_names:
        for team in st.session_state.groups[gn]:
            m = df_m[((df_m['홈'] == team) | (df_m['어웨이'] == team)) & (df_m['확정'])]
            pts, gd = 0, 0
            for _, row in m.iterrows():
                is_h = (row['홈'] == team)
                s_w = (row['남단_홈'] > row['남단_어웨이']) if is_h else (row['남단_어웨이'] > row['남단_홈'])
                m_w = (row['남복_홈'] > row['남복_어웨이']) if is_h else (row['남복_어웨이'] > row['남복_홈'])
                w_w = (row['여복_홈'] > row['여복_어웨이']) if is_h else (row['여복_어웨이'] > row['여복_홈'])
                if (int(s_w) + int(m_w) + int(w_w)) >= 2: pts += 3
                diff = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
                gd += diff if is_h else -diff
            res.append({"조": gn, "팀명": team, "승점": pts, "득실": gd})
    df = pd.DataFrame(res)
    r_a = df[df['조'] == g_names[0]].sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)
    r_b = df[df['조'] == g_names[1]].sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)

    def get_t(df, idx, def_val):
        return df.iloc[idx]['팀명'] if len(df) > idx else def_val

    return {"A1": get_t(r_a, 0, "A1 대기"), "A2": get_t(r_a, 1, "A2 대기"), "A3": get_t(r_a, 2, "A3 대기"),
            "B1": get_t(r_b, 0, "B1 대기"), "B2": get_t(r_b, 1, "B2 대기"), "B3": get_t(r_b, 2, "B3 대기")}


live = get_live_rankings()

# --- 3. 본선 데이터 초기화 ---
if 'ko_data' not in st.session_state:
    st.session_state.ko_data = pd.DataFrame([
        {"단계": "6강 PO(1)", "H": live["A2"], "A": live["B3"], "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "S_선수": [], "M_선수": [], "W_선수": [], "C": False},
        {"단계": "6강 PO(2)", "H": live["A3"], "A": live["B2"], "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "S_선수": [], "M_선수": [], "W_선수": [], "C": False},
        {"단계": "4강(1)", "H": live["B1"], "A": "PO(1) 승자", "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "S_선수": [], "M_선수": [], "W_선수": [], "C": False},
        {"단계": "4강(2)", "H": live["A1"], "A": "PO(2) 승자", "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "S_선수": [], "M_선수": [], "W_선수": [], "C": False},
        {"단계": "결승", "H": "4강(1) 승자", "A": "4강(2) 승자", "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "S_선수": [], "M_선수": [], "W_선수": [], "C": False}
    ])


# --- 4. [저장 확인 팝업창] --- ㅡㅡ^
@st.dialog("📝 본선 결과 최종 확인")
def confirm_ko_save_dialog(idx, m_type_key, v_h, v_a, l_h, l_a, finalized):
    m = st.session_state.ko_data.iloc[idx]
    st.write(f"### ⚔️ {m['단계']} - {m_type_key} 결과 확인")
    st.write(f"**{m['H']}**: {', '.join(l_h)} ({v_h}점)")
    st.write(f"**{m['A']}**: {', '.join(l_a)} ({v_a}점)")
    st.divider()

    if st.button("✅ 데이터 저장", use_container_width=True):
        # 데이터 업데이트
        st.session_state.ko_data.at[idx, f"{m_type_key}_H"] = v_h
        st.session_state.ko_data.at[idx, f"{m_type_key}_A"] = v_a
        st.session_state.ko_data.at[idx, f"{m_type_key}_선수"] = [l_h, l_a]
        st.session_state.ko_data.at[idx, 'C'] = finalized

        # 승자 전파 로직
        curr = st.session_state.ko_data.iloc[idx]
        h_total = (curr['S_H'] > curr['S_A']) + (curr['M_H'] > curr['M_A']) + (curr['W_H'] > curr['W_A'])
        a_total = (curr['S_A'] > curr['S_H']) + (curr['M_A'] > curr['M_H']) + (curr['W_A'] > curr['W_H'])

        if h_total >= 2 or a_total >= 2:
            winner = curr['H'] if h_total > a_total else curr['A']
            st.session_state.ko_data.at[idx, 'W'] = winner
            if idx == 0: st.session_state.ko_data.at[2, 'A'] = winner
            if idx == 1: st.session_state.ko_data.at[3, 'A'] = winner
            if idx == 2: st.session_state.ko_data.at[4, 'H'] = winner
            if idx == 3: st.session_state.ko_data.at[4, 'A'] = winner
        st.rerun()


# --- 5. 대진표 렌더링 ---
st.header("🏆 3월 8일 본선 토너먼트 대진")
st.markdown("<hr style='border-top: 3px solid black; margin-top: 10px; margin-bottom: 20px'/>", unsafe_allow_html=True)


def match_card(idx):
    m = st.session_state.ko_data.iloc[idx]
    h_w = (m['S_H'] > m['S_A']) + (m['M_H'] > m['M_A']) + (m['W_H'] > m['W_A'])
    a_w = (m['S_A'] > m['S_H']) + (m['M_A'] > m['M_H']) + (m['W_A'] > m['W_H'])
    st.markdown(f"""
        <div class="match-box">
            <div class="match-header">📍 {m['단계']}</div>
            <div class="team-row {'team-winner' if h_w >= 2 else ''}"><span>{m['H']}</span><span class="score">{h_w}</span></div>
            <div class="team-row {'team-winner' if a_w >= 2 else ''}"><span>{m['A']}</span><span class="score">{a_w}</span></div>
        </div>
    """, unsafe_allow_html=True)


col_po, _, col_sf, _, col_f = st.columns([1, 0.2, 1, 0.2, 1])
with col_po: match_card(0); match_card(1)
with col_sf: match_card(2); match_card(3)
with col_f: st.write("<div style='height:40px'></div>", unsafe_allow_html=True); match_card(4)

# --- 6. 스코어보드 입력 섹션 (라디오 버튼 기반) --- ㅡㅡ^
st.divider()
st.subheader("📝 본선 경기 스코어보드 입력")

opts = [f"[{r['단계']}] {r['H']} vs {r['A']}" for _, r in st.session_state.ko_data.iterrows()]
sel_idx = st.selectbox("진행할 대진을 선택하세요:", range(len(opts)), format_func=lambda x: opts[x])
curr_match = st.session_state.ko_data.iloc[sel_idx]

# [핵심] 라디오 버튼으로 종목 선택 ㅡㅡ^
m_label = st.radio("🔢 종목 선택:", ["남단", "남복", "여복"], horizontal=True)
m_type_map = {"남단": "S", "남복": "M", "여복": "W"}
m_type = m_type_map[m_label]

# 중복 출전 방지
used_h, used_a = [], []
for key in ["S", "M", "W"]:
    if key != m_type:
        lineup = curr_match.get(f"{key}_선수", [])
        if lineup and len(lineup) == 2:
            used_h.extend(lineup[0]);
            used_a.extend(lineup[1])

# 라인업 필터링
pdb = st.session_state.player_db
gender = "남" if m_label in ["남단", "남복"] else "여"
p_count = 1 if m_label == "남단" else 2

h_pool = [p for p in pdb[(pdb['소속'] == curr_match['H']) & (pdb['성별'] == gender)]['이름'].tolist() if p not in used_h]
a_pool = [p for p in pdb[(pdb['소속'] == curr_match['A']) & (pdb['성별'] == gender)]['이름'].tolist() if p not in used_a]

l_col, r_col = st.columns(2)
with l_col:
    st.markdown(
        f'<div style="background-color:#f0f2f6; padding:10px; border-radius:10px; text-align:center;"><b>🏠 {curr_match["H"]}</b></div>',
        unsafe_allow_html=True)
    sel_h = st.multiselect("선수 명단", h_pool, max_selections=p_count, key=f"h_l_{sel_idx}_{m_type}")
    sc_h = st.number_input("세트 스코어", 0, 6, value=int(curr_match[f"{m_type}_H"]), key=f"h_s_{sel_idx}_{m_type}")

with r_col:
    st.markdown(
        f'<div style="background-color:#f0f2f6; padding:10px; border-radius:10px; text-align:center;"><b>🚀 {curr_match["A"]}</b></div>',
        unsafe_allow_html=True)
    sel_a = st.multiselect("선수 명단 ", a_pool, max_selections=p_count, key=f"a_l_{sel_idx}_{m_type}")
    sc_a = st.number_input("세트 스코어 ", 0, 6, value=int(curr_match[f"{m_type}_A"]), key=f"a_s_{sel_idx}_{m_type}")

is_final = st.checkbox("이 대진 최종 결과 확정", value=curr_match['C'], key=f"final_{sel_idx}")

if st.button("💾 본선 데이터 저장하기", use_container_width=True):
    if len(sel_h) == p_count and len(sel_a) == p_count:
        confirm_ko_save_dialog(sel_idx, m_type, sc_h, sc_a, sel_h, sel_a, is_final)
    else:
        st.error(f"❌ {m_label} 인원 수({p_count}명)를 정확히 선택하세요.")