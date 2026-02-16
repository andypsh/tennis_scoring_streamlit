import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os


@st.cache_resource()
def get_conf():
    config_path = os.path.join('.streamlit', 'config.yaml')

    # 1. 로컬 환경 (YAML 파일 존재 시)
    if os.path.exists(config_path):
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config

    # 2. 클라우드 환경 (Secrets 사용 시) ㅡㅡ^
    elif "credentials" in st.secrets:
        # 핵심: st.secrets는 수정 불가하므로 '진짜 딕셔너리'로 깊은 복사를 해야 합니다.
        # 아래처럼 수동으로 딕셔너리를 생성하면 수정 가능한 객체가 됩니다.
        config = {
            "credentials": {
                "usernames": {
                    username: dict(user_info)
                    for username, user_info in st.secrets["credentials"]["usernames"].items()
                }
            },
            "cookie": dict(st.secrets["cookie"]),
            "preauthorized": dict(st.secrets["preauthorized"]) if "preauthorized" in st.secrets else {"emails": []}
        }
        return config

    else:
        st.error("❌ 설정 정보를 찾을 수 없습니다.")
        return None


def login_check(config):
    if config is None:
        return False

    # 이제 config는 일반 딕셔너리이므로 라이브러리가 맘껏 수정해도 에러가 안 납니다! ㅡㅡ^
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