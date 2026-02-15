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

# 1. 최상단 설정 (이게 최우선입니다)
st.set_page_config(layout="wide", page_title='CJ Tennis Scoring System', page_icon="🎾")

# st.write("### 🔎 시스템 가동 테스트") # 화면에 이 글자가 뜨는지 확인하세요.

# 2. 경로 설정
current_dir = os.path.dirname(os.path.realpath(__file__))
login_dir = os.path.join(current_dir, 'login')
if login_dir not in sys.path:
    sys.path.append(login_dir)

# 3. 로그인 모듈 로드
try:
    import lgn as login_module
    # st.write("✅ 1단계: 모듈 로드 완료")
except Exception as e:
    st.error(f"❌ 모듈 로드 에러: {e}")
    st.stop()

# --- 화면 함수 정의 ---
def home_view():
    st.header('🏠 CJ Tennis Scoring System')
    st.info('CJ제일제당 DT솔루션팀 전용 대시보드입니다.')
    st.write("### 3월 8일 장충 테니스 대회 현황 (50인)")

def login_page_view():
    # st.write("🔐 로그인 정보 입력 중...")
    config = login_module.get_conf()
    login_module.login_check(config)

# --- 실행부 (main 함수 없이 직결) ---
# st.write("🚀 2단계: 화면 구성 시작")

# 로그인 상태 확인 (st.stop()이 lgn.py에 있으면 여기서 멈출 수 있음)
auth_status = st.session_state.get('authentication_status')
# st.write(f"📊 현재 인증 상태: `{auth_status}`")

if auth_status:
    # 로그인 성공 시 페이지 구성
    pages = [
        # st.Page(home_view, title="Home", icon="🏠", default=True),
        st.Page("pages/01_Firstpage/first_main.py", title="대진표 확인", icon="🎾"),
        st.Page("pages/02_Secondpage/second_main.py", title="경기 기록", icon="📚")
    ]
else:
    # 로그인 전: 로그인 페이지만 노출
    pages = [st.Page(login_page_view, title="Login", icon="🔒")]

# 4. 내비게이션 실행
try:
    pg = st.navigation(pages)
    # st.write("🎬 3단계: 내비게이션 가동")
    pg.run()
except Exception as e:
    st.error(f"❌ 렌더링 에러: {e}")