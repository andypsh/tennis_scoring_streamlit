import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import ast


# 🚨 [중요] st.set_page_config는 main.py에만 있어야 하므로 여기서는 삭제했습니다 ㅡㅡ^

# --- 1. 구글 시트 연동 헬퍼 ---
def get_gsheets_conn():
    return st.connection("gsheets", type=GSheetsConnection)


def load_from_gsheets():
    conn = get_gsheets_conn()
    try:
        df = conn.read(ttl="5s")
        for col in ['남단_선수', '남복_선수', '여복_선수']:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x)
        return df
    except:
        return pd.DataFrame()


def save_to_gsheets(df, p_db=None):
    if df.empty: return
    conn = get_gsheets_conn()
    save_df = df.copy()
    for col in ['남단_선수', '남복_선수', '여복_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

    # 대진표 저장
    conn.update(data=save_df)

    # 선수 명단이 있다면 'PlayerList' 탭에 별도 저장 ㅡㅡ^
    if p_db is not None:
        conn.update(worksheet="PlayerList", data=p_db)

    st.success("✅ 모든 데이터가 구글 시트에 영구 저장되었습니다!")


# --- 2. 데이터 동기화 ---
# main.py에서 로그인 성공 후 넘어왔으므로 role은 이미 세션에 있습니다.
st.session_state.match_data = load_from_gsheets()

# --- 3. 메인 화면 ---
st.header("🏆 대회 실시간 운영 센터")

# 관리자(Admin) 권한일 때만 설정창 노출 ㅡㅡ^
if st.session_state.get('role') == "Admin":
    with st.expander("⚙️ 대회 초기 설정 (명단 업로드 및 조 편성)", expanded=st.session_state.match_data.empty):
        uploaded_file = st.file_uploader("선수 명단 업로드 (Excel)", type=['xlsx'])
        if uploaded_file:
            st.session_state.player_db = pd.read_excel(uploaded_file)
            st.success("✅ 명단 로드 완료")

        if st.session_state.get('player_db') is not None:
            pdb = st.session_state.player_db
            all_teams = sorted(pdb['소속'].unique().tolist())
            num_groups = st.selectbox("조 개수:", [2, 3, 4, 5], index=0)

            temp_groups = {}
            already_selected = []
            for i in range(num_groups):
                g_name = f"{chr(65 + i)}조"
                avail = [t for t in all_teams if t not in already_selected]
                selected = st.multiselect(f"📍 {g_name} 선택", options=sorted(avail), key=f"sel_{g_name}")
                temp_groups[g_name] = selected
                already_selected.extend(selected)

            if st.button("🚀 대진표 생성 및 시트 저장"):
                matches = []
                for gn, gt in temp_groups.items():
                    if len(gt) < 2: continue
                    for i in range(len(gt)):
                        for j in range(i + 1, len(gt)):
                            matches.append({
                                "조": gn, "홈": gt[i], "어웨이": gt[j],
                                "남단_홈": 0, "남단_어웨이": 0, "남복_홈": 0, "남복_어웨이": 0, "여복_홈": 0, "여복_어웨이": 0,
                                "남단_선수": [], "남복_선수": [], "여복_선수": [], "확정": False
                            })
                if matches:
                    new_df = pd.DataFrame(matches)
                    st.session_state.match_data = new_df
                    st.session_state.groups = temp_groups
                    # 대진표와 명단을 동시에 시트에 저장 ㅡㅡ^
                    save_to_gsheets(new_df, st.session_state.player_db)
                    st.rerun()

st.divider()

# --- 4. 실시간 순위 현황 (에러 방지 로직 강화) ---
if not st.session_state.match_data.empty:
    def calculate_standings(df_matches, target_group):
        # 해당 조에 속한 팀 추출
        m_group = df_matches[df_matches['조'] == target_group]
        group_teams = sorted(list(set(m_group['홈'].tolist() + m_group['어웨이'].tolist())))

        standings = []
        for team in group_teams:
            # 확정된 경기만 필터링
            m = m_group[((m_group['홈'] == team) | (m_group['어웨이'] == team)) & (m_group['확정'] == True)]
            w, d, l, pts, gd = 0, 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (row['홈'] == team)
                h_wins = (row['남단_홈'] > row['남단_어웨이']) + (row['남복_홈'] > row['남복_어웨이']) + (row['여복_홈'] > row['여복_어웨이'])
                a_wins = (row['남단_어웨이'] > row['남단_홈']) + (row['남복_어웨이'] > row['남복_홈']) + (row['여복_어웨이'] > row['여복_홈'])
                c_gd = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
                gd += c_gd if is_home else -c_gd
                if h_wins == a_wins:
                    d += 1; pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1; pts += 3
                else:
                    l += 1
            standings.append({"팀명": team, "경기": len(m), "승": w, "무": d, "패": l, "승점": pts, "득실": gd})

        return pd.DataFrame(standings)


    st.subheader("📊 실시간 조별 순위")
    unique_groups = sorted(st.session_state.match_data['조'].unique())

    for gn in unique_groups:
        st.markdown(f"#### 📍 {gn} 현황")
        df_res = calculate_standings(st.session_state.match_data, gn)

        # 🚨 [승점 에러 해결] 데이터가 있을 때만 스타일링 적용 ㅡㅡ^
        if not df_res.empty and '승점' in df_res.columns:
            df_res = df_res.sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)
            st.dataframe(
                df_res.style.highlight_max(subset=['승점'], color='#D1E7DD'),
                use_container_width=True, hide_index=True
            )
        else:
            st.info(f"{gn}에 아직 완료된 경기가 없습니다.")
else:
    st.info("📢 대진표가 없습니다. 관리자 계정으로 대진표를 먼저 생성해 주세요.")