import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import ast

# --- 1. UI 및 CSS 설정 ---
st.set_page_config(page_title="CJ Tennis Club", layout="wide")
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none !important; }
        .stMainBlockContainer.block-container { padding-top: 1rem !important; margin-top: 0rem !important; max-width: 95% !important; }
        .stHeadingContainer { margin-bottom: -1.5rem !important; }
        hr { margin-top: 0.5rem !important; margin-bottom: 1rem !important; }
        .group-card { background-color: #ffffff; border-radius: 12px; border: 1px solid #e0e0e0; border-top: 6px solid #FF4B4B; padding: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .group-title { font-size: 1.5rem; font-weight: 800; color: #1E1E1E; margin-bottom: 18px; }
    </style>
""", unsafe_allow_html=True)


# --- 2. 구글 시트 연동 헬퍼 함수 --- ㅡㅡ^
def get_gsheets_conn():
    # secrets.toml의 [connections.gsheets] 설정을 자동으로 읽어옵니다.
    return st.connection("gsheets", type=GSheetsConnection)


def load_from_gsheets():
    conn = get_gsheets_conn()
    try:
        # 10초 캐싱으로 데이터 로드 (실시간성 확보)
        df = conn.read(ttl="10s")
        # 구글 시트에서 읽어온 문자열 리스트를 실제 파이썬 리스트로 복구 ㅡㅡ^
        for col in ['남단_선수', '남복_선수', '여복_선수']:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x)
        return df
    except Exception as e:
        # 데이터가 아예 없거나 시트가 비어있을 경우 빈 프레임 반환
        return pd.DataFrame()


def save_to_gsheets(df):
    if df.empty:
        return
    conn = get_gsheets_conn()
    save_df = df.copy()
    # 구글 시트는 리스트 타입을 저장할 수 없으므로 문자열로 변환 ㅡㅡ^
    for col in ['남단_선수', '남복_선수', '여복_선수']:
        if col in save_df.columns:
            save_df[col] = save_df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

    # 구글 시트 업데이트 수행
    conn.update(data=save_df)
    st.success("✅ 구글 시트 동기화가 완료되었습니다!")


# --- 3. 세션 및 초기 데이터 동기화 ---
if 'role' not in st.session_state: st.session_state.role = "Public"
if 'player_db' not in st.session_state: st.session_state.player_db = None
if 'groups' not in st.session_state: st.session_state.groups = {}
if 'mode' not in st.session_state: st.session_state.mode = "토너먼트 (조별 예선)"
if 'num_groups' not in st.session_state: st.session_state.num_groups = 2

# 시작할 때 구글 시트에서 최신 데이터를 가져와 세션에 저장 ㅡㅡ^
st.session_state.match_data = load_from_gsheets()

# --- 4. 사이드바 (로그인 시스템 - 관리자 2명 대응) ---
with st.sidebar:
    st.title("🔐 사용자 인증")
    if st.session_state.role == "Public":
        input_user = st.text_input("아이디")
        input_pw = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            # Secrets에 설정된 2개 관리자 계정 체크
            is_admin1 = (input_user == st.secrets["auth"]["admin_user"] and
                         input_pw == st.secrets["auth"]["admin_password"])
            is_admin2 = (input_user == st.secrets["auth"]["admin_user2"] and
                         input_pw == st.secrets["auth"]["admin2_password"])

            if is_admin1 or is_admin2:
                st.session_state.role = "Admin"
                st.rerun()
            elif input_user == st.secrets["auth"]["general_user"] and \
                    input_pw == st.secrets["auth"]["general_password"]:
                st.session_state.role = "User"
                st.rerun()
            else:
                st.error("정보가 일치하지 않습니다.")
    else:
        st.write(f"✅ **{st.session_state.role}** 접속 중")
        if st.button("로그아웃"):
            st.session_state.role = "Public"
            st.rerun()

# --- 5. 메인 화면 운영 센터 ---
st.header("🏆 대회 실시간 운영 센터")

if st.session_state.role == "Admin":
    st.markdown("### ⚙️ 대회 관리 설정")
    st.session_state.mode = st.radio("대회 유형 설정:", ["토너먼트 (조별 예선)", "교류전 (2개 팀 맞대결)"],
                                     index=0 if "토너먼트" in st.session_state.mode else 1, horizontal=True)

    with st.expander("📂 1단계: 선수 명단 업로드", expanded=(st.session_state.player_db is None)):
        uploaded_file = st.file_uploader("명단 업로드 (Excel)", type=['xlsx', 'xls'])
        if uploaded_file:
            st.session_state.player_db = pd.read_excel(uploaded_file)
            st.success("✅ 로드 완료")

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
                    selected = st.multiselect(f"📍 {g_name} 선택", options=sorted(list(set(avail + prev))), default=prev,
                                              key=f"sel_{g_name}")
                    temp_groups[g_name] = selected
                    already_selected.extend(selected)

                if st.button("🚀 대진표 생성 및 구글 시트 저장"):
                    matches = []
                    for gn, gt in temp_groups.items():
                        for i in range(len(gt)):
                            for j in range(i + 1, len(gt)):
                                matches.append({
                                    "조": gn, "홈": gt[i], "어웨이": gt[j],
                                    "남단_홈": 0, "남단_어웨이": 0, "남복_홈": 0, "남복_어웨이": 0, "여복_홈": 0, "여복_어웨이": 0,
                                    "남단_선수": [], "남복_선수": [], "여복_선수": [], "확정": False
                                })
                    st.session_state.match_data = pd.DataFrame(matches)
                    st.session_state.groups = temp_groups
                    # 로컬 DB 대신 구글 시트에 저장! ㅡㅡ^
                    save_to_gsheets(st.session_state.match_data)
                    st.rerun()

st.divider()

# --- 6. 실시간 순위 현황 로직 (생략 없음) ---
if not st.session_state.match_data.empty:
    def calculate_standings(df_matches, target_group):
        # 만약 조 정보가 없으면 빈 프레임 반환
        if target_group not in st.session_state.groups:
            return pd.DataFrame()

        group_teams = st.session_state.groups[target_group]
        standings = []
        for team in group_teams:
            # 확정된 경기만 계산
            m = df_matches[((df_matches['홈'] == team) | (df_matches['어웨이'] == team)) & (df_matches['확정'] == True)]
            w, d, l, pts, gd = 0, 0, 0, 0, 0
            for _, row in m.iterrows():
                is_home = (row['홈'] == team)
                h_wins = (row['남단_홈'] > row['남단_어웨이']) + (row['남복_홈'] > row['남복_어웨이']) + (row['여복_홈'] > row['여복_어웨이'])
                a_wins = (row['남단_어웨이'] > row['남단_홈']) + (row['남복_어웨이'] > row['남복_홈']) + (row['여복_어웨이'] > row['여복_홈'])

                # 득실차 계산
                c_gd = (row['남단_홈'] - row['남단_어웨이']) + (row['남복_홈'] - row['남복_어웨이']) + (row['여복_홈'] - row['여복_어웨이'])
                gd += c_gd if is_home else -c_gd

                if h_wins == a_wins:
                    d += 1;
                    pts += 1
                elif (h_wins > a_wins and is_home) or (a_wins > h_wins and not is_home):
                    w += 1;
                    pts += 3
                else:
                    l += 1
            standings.append({"팀명": team, "경기": len(m), "승": w, "무": d, "패": l, "승점": pts, "득실": gd})

        return pd.DataFrame(standings).sort_values(by=["승점", "득실"], ascending=False).reset_index(drop=True)


    st.subheader("📊 실시간 조별 순위 (Live)")
    # 세션에 저장된 조 이름들을 기반으로 순위표 출력
    if not st.session_state.groups:
        # 시트에서 조 정보를 역으로 추출 (조 편성 데이터가 이미 시트에 있을 경우)
        unique_groups = sorted(st.session_state.match_data['조'].unique())
        for gn in unique_groups:
            st.session_state.groups[gn] = sorted(
                list(set(st.session_state.match_data[st.session_state.match_data['조'] == gn]['홈'].tolist() +
                         st.session_state.match_data[st.session_state.match_data['조'] == gn]['어웨이'].tolist())))

    for gn in st.session_state.groups.keys():
        st.markdown(f"#### 📍 {gn} 현황")
        df_res = calculate_standings(st.session_state.match_data, gn)
        if not df_res.empty:
            st.dataframe(
                df_res.style.highlight_max(subset=['승점'], color='#D1E7DD').highlight_min(subset=['패'], color='#F8D7DA'),
                use_container_width=True, hide_index=True)
        else:
            st.info(f"{gn}에 아직 확정된 경기 결과가 없습니다.")
else:
    st.info("📢 현재 진행 중인 대진표 데이터가 없습니다. 관리자 계정으로 접속하여 대진표를 생성해 주세요.")