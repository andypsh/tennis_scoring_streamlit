from datetime import datetime
import streamlit as st
import pandas as pd

# --- 1. 시각적 대진표 전용 CSS --- [cite: 2026-02-16]
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container {
            padding-top: 0rem !important;
            margin-top: -1rem !important;
            max-width: 98% !important;
        }

        /* 대진표 박스 스타일 */
        .bracket-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px 0;
            background-color: #ffffff;
            border-radius: 10px;
        }
        .match-box {
            border: 2px solid #333;
            border-radius: 8px;
            width: 180px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        .match-header {
            background-color: #333;
            color: white;
            text-align: center;
            font-size: 0.8rem;
            padding: 2px;
            border-radius: 5px 5px 0 0;
        }
        .team-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 12px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        .team-winner {
            background-color: #e6fffa;
            color: #2c7a7b;
        }
        .score {
            color: #007bff;
        }

        /* 연결선(Connector) 구현 */
        .connector-line {
            height: 2px;
            background-color: #999;
            flex-grow: 1;
            position: relative;
        }
    </style>
""", unsafe_allow_html=True)


# --- 2. 예선 데이터 실시간 연동 로직 --- [cite: 2026-02-16]
def get_live_rankings():
    if 'match_data' not in st.session_state: return None
    df_matches = st.session_state.match_data
    res = []
    teams = ["제당 A", "제당 B", "ENM-CM-A", "ENM-CM-B", "ENM-ENT-A", "ENM-ENT-B", "올네A", "CJ테니스클럽", "올영A", "올영B"]

    for team in teams:
        group = "A조" if team in st.session_state.group_a else "B조"
        m = df_matches[((df_matches['홈'] == team) | (df_matches['어웨이'] == team)) & (df_matches['확정'])]
        win_ties = 0
        game_diff = 0
        for _, row in m.iterrows():
            is_home = (row['홈'] == team)
            s_win = (row['단식_홈'] > row['단식_어웨이']) if is_home else (row['단식_어웨이'] > row['단식_홈'])
            m_win = (row['남복_홈'] > row['남복_어웨이']) if is_home else (row['남복_어웨이'] > row['남복_홈'])
            w_win = (row['여복_홈'] > row['여복_어웨이']) if is_home else (row['여복_어웨이'] > row['여복_홈'])
            if (int(s_win) + int(m_win) + int(w_win)) >= 2: win_ties += 1
            diff = (row['단식_홈'] - row['단식_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
            game_diff += diff if is_home else -diff
        res.append({"조": group, "팀명": team, "승점": win_ties * 3, "게임득실": game_diff})

    df = pd.DataFrame(res)
    rank_a = df[df['조'] == 'A조'].sort_values(by=["승점", "게임득실"], ascending=False).reset_index(drop=True)
    rank_b = df[df['조'] == 'B조'].sort_values(by=["승점", "게임득실"], ascending=False).reset_index(drop=True)
    return {"A1": rank_a.iloc[0]['팀명'], "A2": rank_a.iloc[1]['팀명'], "A3": rank_a.iloc[2]['팀명'],
            "B1": rank_b.iloc[0]['팀명'], "B2": rank_b.iloc[1]['팀명'], "B3": rank_b.iloc[2]['팀명']}


live = get_live_rankings()

if 'ko_data' not in st.session_state:
    st.session_state.ko_data = pd.DataFrame([
        {"단계": "6강 PO(1)", "H": live["A2"], "A": live["B3"], "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "C": False},
        {"단계": "6강 PO(2)", "H": live["A3"], "A": live["B2"], "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "C": False},
        {"단계": "4강(1)", "H": live["B1"], "A": "PO(1) 승자", "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "C": False},
        {"단계": "4강(2)", "H": live["A1"], "A": "PO(2) 승자", "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "C": False},
        {"단계": "결승", "H": "4강(1) 승자", "A": "4강(2) 승자", "W": "", "S_H": 0, "S_A": 0, "M_H": 0, "M_A": 0, "W_H": 0,
         "W_A": 0, "C": False}
    ])

# --- 3. 시각적 대진표 렌더링 ---
st.header("🏆 3월 8일 본선 토너먼트 대진")
st.markdown("<hr style='border-top: 3px solid black; margin-top: 10px; margin-bottom: 20px'/>", unsafe_allow_html=True)


def match_card(idx):
    m = st.session_state.ko_data.iloc[idx]
    h_m_wins = (m['S_H'] > m['S_A']) + (m['M_H'] > m['M_A']) + (m['W_H'] > m['W_A'])
    a_m_wins = (m['S_A'] > m['S_H']) + (m['M_A'] > m['M_H']) + (m['W_A'] > m['W_H'])

    st.markdown(f"""
        <div class="match-box">
            <div class="match-header">{m['단계']}</div>
            <div class="team-row {'team-winner' if h_m_wins >= 2 else ''}">
                <span>{m['H']}</span><span class="score">{h_m_wins}</span>
            </div>
            <div class="team-row {'team-winner' if a_m_wins >= 2 else ''}">
                <span>{m['A']}</span><span class="score">{a_m_wins}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# 3단 컬럼 레이아웃 (6강 / 4강 / 결승) [cite: 2026-02-16]
col_po, col_arrow1, col_sf, col_arrow2, col_f = st.columns([1, 0.2, 1, 0.2, 1])

with col_po:
    st.write("### 6강 PO")
    match_card(0)  # A2 vs B3 [cite: 2026-02-16]
    st.write("<div style='height:40px'></div>", unsafe_allow_html=True)
    match_card(1)  # A3 vs B2 [cite: 2026-02-16]

with col_arrow1:
    st.markdown("<div style='height:100px'></div> ➔ <div style='height:150px'></div> ➔", unsafe_allow_html=True)

with col_sf:
    st.write("### 4강")
    match_card(2)  # B1 vs PO(1) [cite: 2026-02-16]
    st.write("<div style='height:40px'></div>", unsafe_allow_html=True)
    match_card(3)  # A1 vs PO(2) [cite: 2026-02-16]

with col_arrow2:
    st.markdown("<div style='height:150px'></div> ➔", unsafe_allow_html=True)

with col_f:
    st.write("### 결승")
    st.write("<div style='height:80px'></div>", unsafe_allow_html=True)
    match_card(4)

# --- 4. 상세 스코어 입력 구역 ---
st.divider()
st.subheader("📝 본선 세부 스코어 입력 (단식/남복/여복)")
options = [f"[{r['단계']}] {r['H']} vs {r['A']}" for _, r in st.session_state.ko_data.iterrows()]
sel_idx = st.selectbox("경기를 선택하세요:", range(len(options)), format_func=lambda x: options[x])

curr = st.session_state.ko_data.iloc[sel_idx]
c1, c2, c3 = st.columns(3)
with c1:
    sh = st.number_input(f"{curr['H']} (단)", 0, 6, int(curr['S_H']), key=f"s1_{sel_idx}")
    sa = st.number_input(f"{curr['A']} (단)", 0, 6, int(curr['S_A']), key=f"s2_{sel_idx}")
with c2:
    mh = st.number_input(f"{curr['H']} (남복)", 0, 6, int(curr['M_H']), key=f"m1_{sel_idx}")
    ma = st.number_input(f"{curr['A']} (남복)", 0, 6, int(curr['M_A']), key=f"m2_{sel_idx}")
with c3:
    wh = st.number_input(f"{curr['H']} (여복)", 0, 6, int(curr['W_H']), key=f"w1_{sel_idx}")
    wa = st.number_input(f"{curr['A']} (여복)", 0, 6, int(curr['W_A']), key=f"w2_{sel_idx}")

if st.button("💾 본선 결과 저장"):
    st.session_state.ko_data.at[sel_idx, 'S_H'], st.session_state.ko_data.at[sel_idx, 'S_A'] = sh, sa
    st.session_state.ko_data.at[sel_idx, 'M_H'], st.session_state.ko_data.at[sel_idx, 'M_A'] = mh, ma
    st.session_state.ko_data.at[sel_idx, 'W_H'], st.session_state.ko_data.at[sel_idx, 'W_A'] = wh, wa
    st.session_state.ko_data.at[sel_idx, 'C'] = True

    # 승자 결정 및 전파
    h_wins = (sh > sa) + (mh > ma) + (wh > wa)
    winner = curr['H'] if h_wins >= 2 else curr['A']
    st.session_state.ko_data.at[sel_idx, 'W'] = winner

    if sel_idx == 0: st.session_state.ko_data.at[2, 'A'] = winner  # 4강 진출
    if sel_idx == 1: st.session_state.ko_data.at[3, 'A'] = winner
    if sel_idx == 2: st.session_state.ko_data.at[4, 'H'] = winner  # 결승 진출
    if sel_idx == 3: st.session_state.ko_data.at[4, 'A'] = winner

    st.rerun()