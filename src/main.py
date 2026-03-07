import numpy as np
import sys
import os
import streamlit as st
import streamlit_authenticator as stauth  # 추가 ㅡㅡ^

# [NumPy 2.x Patch] 최상단 고정
try:
    import numpy.lib.arraysetops as _unused
except ImportError:
    from types import ModuleType

    mock_module = ModuleType("numpy.lib.arraysetops")
    mock_module.isin = np.isin
    sys.modules["numpy.lib.arraysetops"] = mock_module

# 1. 최상단 설정
if 'config_set' not in st.session_state:
    st.set_page_config(layout="wide", page_title='CJ Tennis Scoring System', page_icon="🎾")
    st.session_state.config_set = True

# 2. 경로 및 모듈 로드
current_dir = os.path.dirname(os.path.realpath(__file__))
login_dir = os.path.join(current_dir, 'login')
if login_dir not in sys.path:
    sys.path.append(login_dir)

try:
    import lgn as login_module
except Exception as e:
    st.error(f"❌ 모듈 로드 에러: {e}")
    st.stop()


# --- [홈 화면] ---
def home_view():
    st.header('🏠 CJ Tennis 운영 허브')
    st.info('3월 8일 장충 테니스 대회 (50인) 운영 시스템입니다.')

    st.markdown("### 🧭 빠른 페이지 이동 (모바일용)")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎾 예선 조별순위 보기", use_container_width=True, icon="📈"):
            st.switch_page("pages/01_Firstpage/first_page.py")
        if st.button("💯 예선 점수 입력하기", use_container_width=True, icon="📝"):
            st.switch_page("pages/02_Secondpage/second_page.py")
    with c2:
        if st.button("🆚 본선 대진표 확인", use_container_width=True, icon="🏆"):
            st.switch_page("pages/03_Thirdpage/third_page.py")
        if st.button("📚 선수 명단 관리", use_container_width=True, icon="👥"):
            st.switch_page("pages/04_Fourthpage/fourth_page.py")


def login_page_view():
    config = login_module.get_conf()
    login_module.login_check(config)


# --- 3. 실행부 ---
auth_status = st.session_state.get('authentication_status')

if auth_status:
    # [권한 설정] secrets.toml 기반 Role 부여 ㅡㅡ^
    current_user = st.session_state.get('username')
    admin_users = [st.secrets["auth"]["admin_user"], st.secrets["auth"]["admin_user2"]]

    if current_user in admin_users:
        st.session_state.role = "Admin"
    else:
        st.session_state.role = "User"

    # [사이드바 로그아웃 구현] lgn 모듈 대신 직접 Authenticator 생성 ㅡㅡ^
    config = login_module.get_conf()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.get('name')}님")
        st.info(f"접속 권한: **{st.session_state.role}**")
        authenticator.logout('로그아웃', 'sidebar')
        st.divider()

        # 🔄 구글 시트 동기화 버튼 (관리자 전용) ㅡㅡ^
        if st.session_state.role in ["Admin", "User"]:
            st.write("")
            if st.button("🔄 구글 시트 전체 동기화", use_container_width=True, help="구글 시트의 최신 데이터를 강제로 불러옵니다."):
                # 1. 세션에 저장된 데이터 키값들 삭제 ㅡㅡ^
                sync_keys = ['match_data', 'player_db', 'ko_data', 'groups']
                for key in sync_keys:
                    if key in st.session_state:
                        del st.session_state[key]

                # 2. 버튼을 눌렀을 때만 작동하도록 안으로 이동! ㅡㅡ^
                st.toast("데이터 동기화 완료! 최신 정보를 불러옵니다.")
                st.rerun()

            st.divider()

    # 메뉴 구성
    pages = [
        st.Page(home_view, title="대회 홈", icon="🏠", default=True),
        st.Page("pages/01_Firstpage/first_page.py", title="예선 조별순위", icon="🎾"),
        st.Page("pages/02_Secondpage/second_page.py", title="예선 점수 입력", icon="💯"),
        st.Page("pages/03_Thirdpage/third_page.py", title="본선 대진표", icon="🆚"),
        st.Page("pages/04_Fourthpage/fourth_page.py", title="모집요강", icon="📚")
    ]
else:
    pages = [st.Page(login_page_view, title="Login", icon="🔒")]

# 4. 내비게이션 실행
try:
    pg = st.navigation(pages)
    pg.run()
except Exception as e:
    st.error(f"❌ 시스템 렌더링 오류: {e}")