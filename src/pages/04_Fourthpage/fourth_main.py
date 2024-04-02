from datetime import datetime
import streamlit as st
from st_pages import hide_pages
import os
import sys
import importlib
import pandas as pd
from datetime import datetime


login_dir = os.path.join('../../../login/')

sys.path.append(login_dir)

login_module = importlib.import_module("lgn")




def main():
    st.set_page_config(layout="wide")
    st.header('Fourth Page')

   
    with st.sidebar:
        config = login_module.get_conf()

        # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
        login_module.login_check(config)

    st.write(st.session_state)
    if st.session_state.get('authentication_status'):
        tab1, tab2, tab3, tab4=st.tabs([
            "TAB 1",
            "TAB 2",
            "TAB 3",
            "TAB 4"
            ])

        # -------------------------------------------------------------------------------------------------------------------------------
        # tab1 데이터 소개
        # -------------------------------------------------------------------------------------------------------------------------------
        to_date = pd.to_datetime(datetime.today())
        # from_date를 오늘 날짜로부터 3개월 전으로 설정
        from_date = to_date - pd.DateOffset(months=3)
        st.markdown("""
        <style>
        .colored-bg {
            background-color: #f0f0f0;  /* 배경색 설정 */
            border: 1px solid #e0e0e0;  /* 테두리 설정 */
            padding: 10px;
            margin: 10px 0;  /* 위아래 여백 설정 */
        }
            </style>""", unsafe_allow_html=True)
        with tab1:
            col1, col2, col3, col4 = st.columns([8, 0.8, 0.8, 0.8])
            with st.container():
                with col1 : 
                    st.header("Header")
                    st.markdown('<div class="colored-bg">st.columns col1 범위</div>', unsafe_allow_html=True)
                    st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)

                with col2 :
                    st.markdown('<div class="colored-bg">st.columns col2 범위</div>', unsafe_allow_html=True)
                    select_options = ['전체', 'SELECT1', 'SELECT2']
                    select_value = st.selectbox("Select BOX:", select_options)
                    
                with col3 :
                    st.markdown('<div class="colored-bg">st.columns col3 범위</div>', unsafe_allow_html=True)
                    from_date = st.date_input('from_date:', from_date, key = 'from_date')
                    from_date = pd.Timestamp(from_date)
                with col4 :
                    st.markdown('<div class="colored-bg">st.columns col4 범위</div>', unsafe_allow_html=True)
                    to_date = st.date_input('to_date:', to_date, key = 'to_date')
                    to_date = pd.Timestamp(to_date)

            layout1, layout2 = st.columns([10,2.4])
            with layout1:
                st.subheader('Subheader')
                st.markdown('<div class="colored-bg">st.columns layout1 범위</div>', unsafe_allow_html=True)
                with st.container(height=400, border=None):
                    st.write('Contents')

            with layout2:
                st.subheader('Subheader2')
                st.markdown('<div class="colored-bg">st.columns layout2 범위</div>', unsafe_allow_html=True)
                with st.container(height=400, border=None):
                    st.write('Contents2')


        # -------------------------------------------------------------------------------------------------------------------------------
        # tab2 기본 용어 및 수집·분석 정보
        # -------------------------------------------------------------------------------------------------------------------------------

        with tab2:
            st.write('tab2')
    else :
        st.header('로그인 하세요!')

    # with st.sidebar:
    #     config = login_module.get_conf()

    #     # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    #     login_module.login_check(config)


if __name__ == "__main__":
    # 로그인 성공 후 메인 함수 실행
    main()  
    
