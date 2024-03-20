import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# @st.cache_resource

def get_conf():
    """
    config.yaml 파일 정보 갖고오기
    """
    with open('.streamlit/config.yaml') as file:
        config = yaml.load(file , Loader = SafeLoader)

    return config


def login_check(config):
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    authenticator.login()
    if st.session_state['authentication_status']:
        authenticator.logout()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
        st.stop()
    
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

        st.stop()