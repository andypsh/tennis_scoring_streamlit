import numpy as np
import sys
import os
import streamlit as st
import streamlit_authenticator as stauth  # 추가 ㅡㅡ^



# --- 3. 실행부 준비 (최상단 단일 인증 객체 생성) ---
config = login_module.get_conf()
authenticator = login_module.get_authenticator(config)
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
    st.header('🏠 CJ Tennis CLUB')
    st.info('3월 21일 CJ 교류전 운영 시스템입니다.')

    st.markdown("### 🧭 빠른 페이지 이동 (모바일용)")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎾 순위 보기", use_container_width=True, icon="📈"):
            st.switch_page("pages/01_Firstpage/first_page.py")
        if st.button("💯 점수 입력하기", use_container_width=True, icon="📝"):
            st.switch_page("pages/02_Secondpage/second_page.py")
    with c2:

        if st.button("📚 선수 명단 관리", use_container_width=True, icon="👥"):
            st.switch_page("pages/04_Fourthpage/fourth_page.py")


def login_page_view():
    if authenticator:
        # 로그인 위젯 렌더링 (여기서 내부적으로 쿠키 검증이 일어남)
        authenticator.login(location='main')

        auth_status = st.session_state.get("authentication_status")
        if auth_status:
            # 쿠키로 자동 로그인 되었거나 방금 로그인 성공한 경우
            st.rerun()
        elif auth_status is False:
            st.error('ID 또는 비밀번호가 틀렸습니다.')


# --- 4. 실행부 ---
auth_status = st.session_state.get('authentication_status')

if auth_status:
    # [권한 설정] secrets.toml 기반 Role 부여 ㅡㅡ^
    current_user = st.session_state.get('username')
    admin_users = [st.secrets["auth"]["admin_user"], st.secrets["auth"]["admin_user2"]]

    if current_user in admin_users:
        st.session_state.role = "Admin"
    else:
        st.session_state.role = "User"

    # [사이드바 로그아웃 구현] 이미 생성된 authenticator 재사용! ㅡㅡ^
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.get('name')}님")
        st.info(f"접속 권한: **{st.session_state.role}**")
        authenticator.logout('로그아웃', 'sidebar')
        st.divider()

        # 🔄 구글 시트 동기화 버튼 (관리자 전용) ㅡㅡ^
        if st.session_state.role in ["Admin", "User"]:
            st.write("")
            if st.button("🔄 구글 시트 전체 동기화", use_container_width=True):
                # 1. [핵심] 운영 서버 메모리에 저장된 모든 캐시를 강제로 비웁니다! ㅡㅡ^
                st.cache_data.clear()

                # 2. 내 세션에 저장된 데이터 키값들도 삭제
                sync_keys = ['match_data', 'player_db', 'ko_data', 'groups']
                for key in sync_keys:
                    if key in st.session_state:
                        del st.session_state[key]

                st.toast("🔥 서버 캐시와 세션을 모두 초기화했습니다! 최신 시트 정보를 읽어옵니다.")
                st.rerun()

            st.divider()

    # 메뉴 구성
    pages = [
        st.Page(home_view, title="대회 홈", icon="🏠", default=True),
        st.Page("pages/01_Firstpage/first_page.py", title="순위", icon="🎾"),
        st.Page("pages/02_Secondpage/second_page.py", title="점수 입력", icon="💯"),
        st.Page("pages/04_Fourthpage/fourth_page.py", title="모집요강", icon="📚")
    ]
else:
    pages = [st.Page(login_page_view, title="Login", icon="🔒")]

# 5. 내비게이션 실행
try:
    pg = st.navigation(pages)
    pg.run()
except Exception as e:
    st.error(f"❌ 시스템 렌더링 오류: {e}")