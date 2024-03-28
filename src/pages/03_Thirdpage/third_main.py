from datetime import datetime
import streamlit as st
from st_pages import hide_pages
import os
import sys
import importlib

login_dir = os.path.join('../../../login/')

sys.path.append(login_dir)

login_module = importlib.import_module("lgn")




def main():
    st.set_page_config(layout="wide")
    st.header('Third Page')


    # with st.sidebar:
    #     config = login_module.get_conf()

    #     # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    #     login_module.login_check(config)

    if st.session_state.get('authentication_status'):
        tab1, tab2, tab3, tab4=st.tabs([
            "데이터 소개",
            "기본 용어 및 수집·분석 정보",
            "데이터 수집 시점별 정보",
            "자주 묻는 질문"
            ])

        # -------------------------------------------------------------------------------------------------------------------------------
        # tab1 데이터 소개
        # -------------------------------------------------------------------------------------------------------------------------------

        with tab1:
            col1, col2=st.columns([7,3])
            with col1:
                st.write('tab1')

        # -------------------------------------------------------------------------------------------------------------------------------
        # tab2 기본 용어 및 수집·분석 정보
        # -------------------------------------------------------------------------------------------------------------------------------

        with tab2:
            st.write('tab2')


if __name__ == "__main__":
    # 로그인 성공 후 메인 함수 실행
    main()  
    
