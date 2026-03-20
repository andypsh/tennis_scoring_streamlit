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
    try:
        df = conn.read(worksheet="Matches", ttl=0)
        if not df.empty:
            # 💡 [중요] 교류전용 선수 컬럼 리스트로 변환 ㅡㅡ^
            for col in ['홈_선수', '어웨이_선수']:
                if col in df.columns:
                    df[col] = df[col].apply(
                        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else (
                            x if isinstance(x, list) else [])
                    )
        return df
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}")
        return pd.DataFrame()


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
    # 리스트 데이터를 시트에 저장하기 위해 문자열로 변환 ㅡㅡ^
    for col in ['홈_선수', '어웨이_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    conn.update(worksheet="Matches", data=save_df)


def save_players_to_gsheets(df):
    if df is None or df.empty: return
    conn = get_gsheets_conn()
    conn.update(worksheet="Players", data=df)
    st.success("✅ 선수 명단이 저장되었습니다!")


# --- 3. 데이터 초기화 ---
if 'match_data' not in st.session_state:
    st.session_state.match_data = load_from_gsheets()
if 'player_db' not in st.session_state:
    st.session_state.player_db = load_players_from_gsheets()
if 'groups' not in st.session_state:
    st.session_state.groups = {"교류전": ["CJ", "FRIDAY"]}  # 교류전 고정 ㅡㅡ^

# --- 4. 메인 화면 ---
st.header("🎾 CJ vs FRIDAY 교류전")
current_role = st.session_state.get('role', 'User')

if current_role == "Admin":
    st.markdown("### ⚙️ 관리자 설정")

    with st.expander("📂 1단계: 선수 명단 업로드"):
        uploaded_file = st.file_uploader("명단 업로드 (Excel)", type=['xlsx', 'xls'])
        if uploaded_file:
            pdf = pd.read_excel(uploaded_file)
            st.session_state.player_db = pdf
            save_players_to_gsheets(pdf)

    with st.expander("🚀 2단계: 교류전 대진표 생성", expanded=st.session_state.match_data.empty):
        st.info("입력하신 스케줄 데이터를 기반으로 대진표를 초기화합니다.")
        if st.button("🔥 대진표 생성 및 시트 덮어쓰기"):
            schedule_data = {
                "시간": ["18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30"],
                "1코트": [
                    "[남복] 현준/규찬 (3.5) vs 태훈/재환 (5.5)",
                    "[여복] 혜린/유진 (1.5) vs 은채/새롬 (2.5)",
                    "[남복] 현준/두영 (3.5) vs 태훈/익성(5.5)",
                    "[혼복] 현준/유진 (3.0) vs 경랑/승은 (4.5)",
                    "[혼복] 소휘/혜린 (4.5) vs 태훈/승은 (3.0)",
                    "[혼복] 규찬/문정 (3.0) vs 태훈/새롬 (4.0)",
                    "[남복] 예준/두영 (2.0) vs 동희/익성 (3.0)",
                    "[여복] 유진/혜린 (1.5) vs 새롬/성희 (2.5)"
                ],
                "2코트": [
                    "[남복] 예준/소휘 (3.5) vs 병호/동희 (2.5)",
                    "[혼복] 성혁/민영 (3.6) vs 익성/성희 (3.0)",
                    "[남복] 성혁/소휘 (5.5) vs 경랑/병호 (4.0)",
                    "[혼복] 소휘/문정 (4.0) vs 동희/새롬 (2.5)",
                    "[남복] 성혁/두영 (4.5) vs 익성/재환 (5.5)",
                    "[혼복] 예준/민영 (1.1) vs 병호/은채 (4.0)",
                    "[남복] 성혁/현준 (5.5) vs 재환/경랑 (5.5)",
                    "[혼복] 규찬/문정 (3.0) vs 태훈/은채 (4.0)"
                ],
                "3코트": [
                    "[여복] 문정/유진 (2.5) vs 승은/은채 (3.0)",
                    "[남복] 예준/두영 (2.0) vs 경랑/동희 (4.0)",
                    "[여복] 민영/혜린 (0.6) vs 승은/성희 (3.0)",
                    "[남복] 규찬/예준 (2.5) vs 재환/병호 (4.0)",
                    "[여복] 민영/문정 (1.5) vs 은채/성희 (3.0)",
                    "[남복] 성혁/현준 (6.0) vs 재환/동희 (4.0)",
                    "[여복] 민영/유진 (1.1) vs 승은/새롬 (3.0)",
                    "[남복] 소휘/두영 (3.5) vs 익성/병호 (3.0)"
                ]
            }
            matches = []
            for i, time in enumerate(schedule_data["시간"]):
                for court in ["1코트", "2코트", "3코트"]:
                    raw = schedule_data[court][i]
                    # 파싱 로직 ㅡㅡ^
                    cat = raw.split(']')[0][1:]
                    p_part = raw.split(']')[1].split(' vs ')
                    h_p = [p.split('(')[0].strip() for p in p_part[0].split('/')]
                    a_p = [p.split('(')[0].strip() for p in p_part[1].split('/')]
                    matches.append({
                        "조": "교류전", "시간": time, "코트": court, "종목": cat,
                        "홈": "CJ", "어웨이": "FRIDAY", "홈_점수": 0, "어웨이_점수": 0,
                        "홈_선수": h_p, "어웨이_선수": a_p, "확정": False
                    })
            new_df = pd.DataFrame(matches)
            save_matches_to_gsheets(new_df)
            st.session_state.match_data = new_df
            st.rerun()

st.divider()


# --- 5. 계산 및 출력 (교류전 전용) ---
def calculate_exchange_standings(df):
    df['확정_val'] = pd.to_numeric(df['확정'], errors='coerce').fillna(0)
    confirmed = df[df['확정_val'] > 0]

    standings = []
    for team in ["CJ", "FRIDAY"]:
        m = confirmed[(confirmed['홈'] == team) | (confirmed['어웨이'] == team)]
        w, d, l, gd = 0, 0, 0, 0
        for _, row in m.iterrows():
            is_home = (row['홈'] == team)
            h_s, a_s = int(row['홈_점수']), int(row['어웨이_점수'])
            if h_s == a_s:
                d += 1
            elif (h_s > a_s and is_home) or (a_s > h_s and not is_home):
                w += 1
            else:
                l += 1
            gd += (h_s - a_s) if is_home else (a_s - h_s)
        standings.append({"팀명": team, "경기": len(m), "승": w, "무": d, "패": l, "득실": gd})
    return pd.DataFrame(standings).sort_values(by=["승", "무", "득실"], ascending=False)


def calculate_player_ranking(df):
    # 1. 숫자형 변환 및 확정 경기 필터링 ㅡㅡ^
    df['확정_val'] = pd.to_numeric(df['확정'], errors='coerce').fillna(0)
    confirmed = df[df['확정_val'] > 0]

    stats = {}

    for _, row in confirmed.iterrows():
        h_s, a_s = int(row['홈_점수']), int(row['어웨이_점수'])

        # '홈'팀(CJ)과 '어웨이'팀(FRIDAY)을 번갈아 처리 ㅡㅡ^
        for side in ['홈', '어웨이']:
            players = row[f'{side}_선수']
            team_name = str(row[side]).strip()

            my_s = h_s if side == '홈' else a_s
            opp_s = a_s if side == '홈' else h_s

            # 승무패 판정
            if my_s > opp_s:
                res = '승'
            elif my_s < opp_s:
                res = '패'
            else:
                res = '무'

            for p in players:
                p = str(p).strip()
                if not p: continue

                # 선수별 통계 저장 (득점, 실점 추가) ㅡㅡ^
                if p not in stats:
                    stats[p] = {"소속": team_name, "경기": 0, "승": 0, "무": 0, "패": 0, "득점": 0, "실점": 0, "득실": 0}

                stats[p]["경기"] += 1
                stats[p][res] += 1
                stats[p]["득점"] += my_s   # 💡 내 점수 합계 ㅡㅡ^
                stats[p]["실점"] += opp_s   # 💡 상대 점수 합계 ㅡㅡ^
                stats[p]["득실"] += (my_s - opp_s)

    # 2. 데이터프레임 변환
    res_df = pd.DataFrame([{"선수명": k, **v} for k, v in stats.items()])

    if not res_df.empty:
        # 💡 요청하신 대로 득점, 실점을 득실 왼쪽에 배치 ㅡㅡ^
        cols = ["선수명", "소속", "경기", "승", "무", "패", "득점", "실점", "득실"]
        res_df = res_df[cols]
        # 승 -> 득실 -> 득점(다득점) 순으로 정렬 ㅡㅡ^
        return res_df.sort_values(by=["승", "득실", "득점"], ascending=[False, False, False]).reset_index(drop=True)

    return pd.DataFrame()


@st.fragment(run_every=30)
def show_live_rankings_area():
    live_df = load_from_gsheets()
    if not live_df.empty:
        # 점수 컬럼들을 확실하게 정수형으로 변환 ㅡㅡ^
        for col in ['홈_점수', '어웨이_점수']:
            live_df[col] = pd.to_numeric(live_df[col], errors='coerce').fillna(0).astype(int)

        st.subheader("🏆 팀별 스코어 현황")
        st.dataframe(calculate_exchange_standings(live_df), use_container_width=True, hide_index=True)

        st.subheader("🏅 개인 다승 순위")
        p_df = calculate_player_ranking(live_df)
        if not p_df.empty:
            st.dataframe(p_df.style.highlight_max(subset=['승'], color='#D1E7DD'), use_container_width=True)

        st.divider()
        st.subheader("📅 상세 타임테이블")

        # 🔍 1. 선수명 검색 기능 추가 ㅡㅡ^
        search_name = st.text_input("👤 내 경기 찾기 (이름 입력)", placeholder="이름을 입력하면 해당 경기만 표시됩니다.")

        # 🎾 2. 코트 선택 (검색어가 없을 때만 유효하게 하거나, 검색과 병행)
        selected_court = st.radio("코트 선택", ["전체", "1코트", "2코트", "3코트"], horizontal=True)

        # 필터링 로직 ㅡㅡ^
        display_df = live_df.copy()

        if search_name:
            # 홈_선수나 어웨이_선수 리스트 안에 이름이 포함되어 있는지 확인
            display_df = display_df[
                display_df['홈_선수'].apply(lambda x: search_name in x) |
                display_df['어웨이_선수'].apply(lambda x: search_name in x)
                ]

        if selected_court != "전체":
            display_df = display_df[display_df['코트'] == selected_court]

        if display_df.empty:
            st.warning(f"'{search_name}' 선수의 경기가 없습니다.")
        else:
            for _, row in display_df.iterrows():
                is_conf = str(row['확정']).upper() in ['TRUE', '1', '1.0']
                # 점수를 int로 변환하여 제목 구성 ㅡㅡ^
                h_s, a_s = int(row['홈_점수']), int(row['어웨이_점수'])

                title = f"{'✅' if is_conf else '🎾'} [{row['코트']} {row['시간']}] {', '.join(row['홈_선수'])} {h_s}:{a_s} {', '.join(row['어웨이_선수'])}"

                with st.expander(title):
                    c1, c2, c3 = st.columns([2, 1, 2])
                    # metric에서도 f-string으로 int 형변환 확인 ㅡㅡ^
                    c1.metric("CJ", f"{h_s}점")
                    c2.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
                    c3.metric("FRIDAY", f"{a_s}점")
                    st.caption(f"종목: {row['종목']} | 상태: {'경기 종료' if is_conf else '진행 중'}")

        st.caption(f"🕒 자동 갱신 중: {pd.Timestamp.now().strftime('%H:%M:%S')}")


if not st.session_state.match_data.empty:
    show_live_rankings_area()
else:
    st.info("📢 관리자 메뉴에서 '대진표 생성'을 눌러주세요.")