import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os


@st.cache_resource()
def get_conf():
    """
    로컬에 파일이 있으면 YAML을 읽고, 없으면 Secrets를 읽는 하이브리드 로직 ㅡㅡ^
    """
    config_path = os.path.join('.streamlit', 'config.yaml')

    # 1. 로컬 환경 체크: 파일이 존재하는지 먼저 확인
    if os.path.exists(config_path):
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config

    # 2. 클라우드 환경 체크: 파일이 없으면 Secrets에서 가져옴 ㅡㅡ^
    elif "credentials" in st.secrets:
        # st.secrets를 딕셔너리 형태로 변환하여 반환
        return {
            "credentials": st.secrets["credentials"],
            "cookie": st.secrets["cookie"],
            "preauthorized": st.secrets["preauthorized"]
        }

    else:
        st.error("❌ 설정 파일(YAML) 또는 Secrets 정보를 찾을 수 없습니다.")
        return None


def login_check(config):
    if config is None:
        return False

    # Authenticate 객체 생성 (로컬/클라우드 공용)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # 로그인 위젯 호출
    authenticator.login(location='main')

    auth_status = st.session_state.get("authentication_status")

    if auth_status:
        st.session_state['logout_button'] = authenticator.logout('Logout', 'sidebar')
        return True
    elif auth_status is False:
        st.error('ID 또는 비밀번호가 틀렸습니다.')

    return False