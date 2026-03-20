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

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # 로그인 위젯 호출 (쿠키가 있으면 여기서 자동으로 세션을 True로 바꿔줍니다)
    authenticator.login(location='main')

    auth_status = st.session_state.get("authentication_status")

    if auth_status:
        st.session_state['logout_button'] = authenticator.logout('Logout', 'sidebar')

        # ㅡㅡ^ 핵심 추가: 모바일 백그라운드 전환으로 세션이 초기화됐을 때,
        # 쿠키로 자동 로그인은 성공했지만 네비게이션이 안 바뀌는 현상을 강제로 갱신합니다.
        st.rerun()

        return True
    elif auth_status is False:
        st.error('ID 또는 비밀번호가 틀렸습니다.')

    return False