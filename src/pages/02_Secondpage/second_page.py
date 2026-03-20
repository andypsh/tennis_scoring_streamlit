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
        .blur-container { filter: blur(4px); pointer-events: none; opacity: 0.6; }
        .entered-msg { background-color: #2E7D32; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 15px; }
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
            # 💡 교류전용 컬럼명으로 변경 ㅡㅡ^
            for col in ['홈_선수', '어웨이_선수']:
                if col in m_df.columns:
                    m_df[col] = m_df[col].apply(
                        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else (
                            x if isinstance(x, list) else [])
                    )
        p_df = conn.read(worksheet="Players", ttl=0)
        return m_df, p_df
    except:
        return pd.DataFrame(), None


def save_to_gsheets(df):
    if df.empty: return
    conn = get_gsheets_conn()
    save_df = df.copy()
    for col in ['홈_선수', '어웨이_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    conn.update(worksheet="Matches", data=save_df)
    st.success("✅ 경기 결과가 실시간으로 반영되었습니다!")


# --- 3. 데이터 동기화 ---
if 'match_data' not in st.session_state or 'player_db' not in st.session_state:
    st.session_state.match_data, st.session_state.player_db = load_data()

# --- 4. 화면 구성 ---
st.header("📝 교류전 스코어보드 입력")

if st.session_state.match_data.empty:
    st.error("❌ 대진표 데이터가 없습니다. 메인 페이지에서 대진표를 먼저 생성하세요.")
    st.stop()

# --- 3. 데이터 동기화 부분 수정 ㅡㅡ^ ---
# 세션에 데이터가 없거나, 강제 새로고침이 필요할 때 호출
if 'match_data' not in st.session_state or st.session_state.get('needs_sync', False):
    st.session_state.match_data, st.session_state.player_db = load_data()
    st.session_state.needs_sync = False  # 동기화 완료 후 플래그 초기화


@st.dialog("📝 경기 결과 최종 확정")
def confirm_save_dialog(idx, v_h, v_a, l_h, l_a):
    curr = st.session_state.match_data.loc[idx]
    st.write(f"### ⚔️ [{curr['코트']} {curr['시간']}] {curr['종목']} 결과")
    st.write(f"**{curr['홈']}** ({', '.join(l_h)}): **{int(v_h)}점**")
    st.write(f"**{curr['어웨이']}** ({', '.join(l_a)}): **{int(v_a)}점**")
    st.divider()

    c1, c2 = st.columns(2)
    if c1.button("✅ 확정 및 저장", use_container_width=True):
        # 1. 먼저 로컬 세션 데이터를 업데이트 ㅡㅡ^
        st.session_state.match_data.at[idx, "홈_점수"] = int(v_h)
        st.session_state.match_data.at[idx, "어웨이_점수"] = int(v_a)
        st.session_state.match_data.at[idx, "확정"] = True
        st.session_state.match_data.at[idx, "홈_선수"] = l_h
        st.session_state.match_data.at[idx, "어웨이_선수"] = l_a

        # 2. DB(구글 시트)에 전송 ㅡㅡ^
        save_to_gsheets(st.session_state.match_data)

        # 3. [핵심] 다음 리런(Rerun) 때 시트에서 최신 데이터를 다시 읽어오도록 플래그 설정 ㅡㅡ^
        st.session_state.needs_sync = True

        st.rerun()

    if c2.button("❌ 취소", use_container_width=True):
        st.rerun()


# 🎾 코트 및 시간 필터 ㅡㅡ^
c_filter = st.radio("코트 선택:", ["1코트", "2코트", "3코트"], horizontal=True)
m_df = st.session_state.match_data[st.session_state.match_data['코트'] == c_filter]

if not m_df.empty:
    # 💡 시간대별 경기 선택 ㅡㅡ^
    opts = [f"[{r['시간']}] {r['종목']} | {', '.join(r['홈_선수'])} vs {', '.join(r['어웨이_선수'])}" for _, r in m_df.iterrows()]
    sel_raw = st.selectbox("진행할 경기 선택:", range(len(opts)), format_func=lambda x: opts[x])

    real_idx = m_df.index[sel_raw]
    curr_match = st.session_state.match_data.loc[real_idx]

    # 상태 확인
    is_already_entered = str(curr_match['확정']).upper() in ['TRUE', '1', '1.0']

    if is_already_entered:
        st.markdown(
            f'<div class="entered-msg">✅ 종료된 경기입니다. ({int(curr_match["홈_점수"])} : {int(curr_match["어웨이_점수"])})</div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # 블러 처리
    input_container = st.container()
    if is_already_entered:
        st.markdown('<div class="blur-container">', unsafe_allow_html=True)



    with input_container:
        st.info(f"📍 {curr_match['코트']} - {curr_match['시간']} | 종목: **{curr_match['종목']}**")

        l_col, r_col = st.columns(2)

        # 💡 [핵심] 전체 명단 대신, 해당 매치에 이미 등록된 선수들만 리스트로 만듭니다 ㅡㅡ^
        h_match_players = [str(p).strip() for p in curr_match['홈_선수']]
        a_match_players = [str(p).strip() for p in curr_match['어웨이_선수']]

        with l_col:
            st.markdown(f"**🏠 {curr_match['홈']} (CJ)**")
            # 💡 options를 전체 명단이 아니라 h_match_players로 제한합니다 ㅡㅡ^
            sel_h = st.multiselect("선수 확인",
                                   options=h_match_players,
                                   default=h_match_players,
                                   disabled=is_already_entered)
            sc_h = st.number_input("최종 점수", 0, 30, value=int(curr_match.get('홈_점수', 0)), step=1,
                                   key=f"sh_{real_idx}", disabled=is_already_entered)

        with r_col:
            st.markdown(f"**🚀 {curr_match['어웨이']} (FRIDAY)**")
            # 💡 여기도 배정된 선수들만 보이게 제한 ㅡㅡ^
            sel_a = st.multiselect("선수 확인 ",
                                   options=a_match_players,
                                   default=a_match_players,
                                   disabled=is_already_entered)
            sc_a = st.number_input("최종 점수 ", 0, 30, value=int(curr_match.get('어웨이_점수', 0)), step=1,
                                   key=f"sa_{real_idx}", disabled=is_already_entered)

            # (이하 저장 로직 동일...)

        if st.button("💾 경기 결과 전송", use_container_width=True, disabled=is_already_entered):
            if not sel_h or not sel_a:
                st.error("❌ 선수가 선택되지 않았습니다.")
            else:
                confirm_save_dialog(real_idx, sc_h, sc_a, sel_h, sel_a)

    if is_already_entered:
        st.markdown('</div>', unsafe_allow_html=True)