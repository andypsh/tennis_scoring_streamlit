import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os


@st.cache_resource()
def get_conf():
    """
    config.yaml 파일 정보 로드
    """
    # 경로를 확실히 하기 위해 .streamlit 폴더 내부를 확인합니다.
    config_path = os.path.join('.streamlit', 'config.yaml')
    if not os.path.exists(config_path):
        # 만약 경로가 다를 경우를 대비한 예외 처리
        st.error(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}")
        return None

    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def login_check(config):
    if config is None:
        return

    # 1. Authenticate 객체 생성 (최신 v0.3.0+ 방식)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # 2. 로그인 위젯 호출 (이 함수 자체가 화면에 폼을 그립니다)
    # 최신 버전에서는 반환값을 받지 않고 세션 상태를 직접 확인합니다.
    authenticator.login(location='main')

    # 3. 인증 상태 확인 (절대로 st.stop()을 쓰지 마세요!)
    auth_status = st.session_state.get("authentication_status")

    if auth_status:
        # 인증 성공 시 로그아웃 버튼 배치
        st.session_state['logout'] = authenticator.logout('Logout', 'sidebar')
    elif auth_status is False:
        st.error('ID 또는 비밀번호가 틀렸습니다.')
    # auth_status가 None인 경우는 아무것도 하지 않고 로그인 폼만 보여줍니다.