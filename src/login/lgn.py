import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import extra_streamlit_components as stx
import os
from uuid import uuid4

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
        #CookieManager 인스턴스 생성
    # unique_key = "bar_" + str(os.getpid())
    # cookie_manager = stx.CookieManager(key=unique_key)

    # # 쿠키 이름을 지정합니다. 예를 들어 'my_cookie_name'입니다.
    # cookie_name = "my_cookie_name"

    # # 쿠키 조회
    # cookie_value = cookie_manager.get(cookie_name)
    # st.write(cookie_value)
    authenticator.login(location = 'sidebar')
    if st.session_state['authentication_status']:
        authenticator.logout()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
        st.stop()
    
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

        st.stop()



# def login_check(config):
#     # 세션 상태에서 CookieManager를 재사용하거나 새로 생성합니다.
#     if 'cookie_manager' not in st.session_state:
#         st.session_state['cookie_manager'] = stx.CookieManager(key=str(uuid4()))
    
#     authenticator = stauth.Authenticate(
#         config['credentials'],
#         config['cookie']['name'],
#         config['cookie']['key'],
#         config['cookie']['expiry_days'],
#         config['preauthorized'],
#         # 여기에 CookieManager 인스턴스를 전달합니다.
#         cookie_manager=st.session_state['cookie_manager']
#     )

#     authenticator.login(location='sidebar')
    
#     if st.session_state['authentication_status']:
#         authenticator.logout('Logout', 'sidebar', key='logout')
#     elif st.session_state['authentication_status'] is False:
#         st.error('Username/password is incorrect')
#         st.stop()
#     elif st.session_state['authentication_status'] is None:
#         st.warning('Please enter your username and password')
#         st.stop()
