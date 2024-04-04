import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import extra_streamlit_components as stx
import os
from uuid import uuid4

@st.cache_resource()
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

    name, authentication_status, username = authenticator.login('main')
    st.session_state['authentication_status'] = authentication_status
    if st.session_state['authentication_status']:
        st.session_state['logout2'] = authenticator.logout()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
        st.stop()
    
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

        st.stop()
