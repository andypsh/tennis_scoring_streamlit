import streamlit as st
from st_pages import Page, show_pages, add_page_title
import importlib
import os
import sys
import datetime
import extra_streamlit_components as stx
import hydralit_components as hc
import pandas as pd
import numpy as np
#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))


login_dir = os.path.join(current_dir + '/login/')
sys.path.append(login_dir)
login_module = importlib.import_module("lgn")

def main():
    st.set_page_config(layout="wide", page_title = 'Write Your Page name' , page_icon=":memo:")
    with st.sidebar:
    ################## [login_module] ##################

    # login_module 내 get_conf() 함수를 통해 로그인 정보를 갖고 온다. 
    # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다

    #####################################################config = login_module.get_conf()
        config = login_module.get_conf()
        login_module.login_check(config)
    # df = pd.DataFrame(np.empty((3, 3))*np.nan, columns=['A', 'B', 'C'])
    # df.iloc[0,1] = 22
    # st.write(df)
    # st.stop()
    with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3,0,5]):
        #####################################################
        if st.session_state.get('authentication_status'):
                
            st.header('옆에 PAGE를 클릭하세요!')
            ################## [Side bar Menu Tree] ##################

            # st-pages 모듈 내 show_pages 클래스 import 
            # Page('구동할 파일' , '이름' , '이모티콘')
        
            #####################################################
            show_pages(
                [
                    Page('main.py', 'Home', "🏠"),
                    Page("pages/01_Firstpage/first_main.py", "First_page", ":smile:"),
                    Page("pages/02_Secondpage/second_main.py", "Second_page", ":books:"),
                    Page("pages/03_Thirdpage/third_main.py", "Third_page", ":pig:"),
                    Page("pages/04_Fourthpage/fourth_main.py" , "Fourth_page" , ":horse:")
                ]
            )
            # st.write(st.session_state)

        else:
            st.header('로그인하세요!')


if __name__ == "__main__":
    # 로그인 성공 후 메인 함수 실행
    main()  
