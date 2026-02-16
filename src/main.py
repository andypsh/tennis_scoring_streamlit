import numpy as np
import sys
import os

# [NumPy 2.x Patch] 최상단 고정
try:
    import numpy.lib.arraysetops as _unused
except ImportError:
    from types import ModuleType

    mock_module = ModuleType("numpy.lib.arraysetops")
    mock_module.isin = np.isin
    sys.modules["numpy.lib.arraysetops"] = mock_module

import streamlit as st
import importlib

# 1. 최상단 설정
st.set_page_config(layout="wide", page_title='CJ Tennis Scoring System', page_icon="🎾")

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


# --- [홈 화면: 모바일용 바로가기 버튼 추가] --- ㅡㅡ^
def home_view():
    st.header('🏠 CJ Tennis 운영 허브')
    st.info('3월 8일 장충 테니스 대회 (50인) 운영 시스템입니다.')

    st.markdown("### 🧭 빠른 페이지 이동 (모바일용)")
    # 모바일에서는 한 줄에 하나씩, PC에서는 나란히 보이게 구성 ㅡㅡ^
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
    # 로그인 성공 시: Home을 포함한 전체 메뉴 구성 ㅡㅡ^
    pages = [
        st.Page(home_view, title="대회 홈", icon="🏠", default=True),
        st.Page("pages/01_Firstpage/first_page.py", title="예선 조별순위", icon="🎾"),
        st.Page("pages/02_Secondpage/second_page.py", title="예선 점수 입력", icon="💯"),
        st.Page("pages/03_Thirdpage/third_page.py", title="본선 대진표", icon="🆚"),
        st.Page("pages/04_Fourthpage/fourth_page.py", title="선수 등록", icon="📚")
    ]
else:
    # 로그인 전: 오직 로그인 페이지만!
    pages = [st.Page(login_page_view, title="Login", icon="🔒")]

# 4. 내비게이션 실행
try:
    pg = st.navigation(pages)
    pg.run()
except Exception as e:
    # 렌더링 에러 시 세부 정보 출력 (디버깅용) ㅡㅡ^
    st.error(f"❌ 시스템 렌더링 오류: {e}")
    if "NoneType" in str(e):
        st.info("💡 팁: 각 페이지 파일 내부의 st.set_page_config를 모두 지워주세요. main.py에서 한 번만 설정해야 합니다.")