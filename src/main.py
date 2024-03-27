import streamlit as st
from st_pages import Page, show_pages, add_page_title
import importlib
import os
import sys

#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))


login_dir = os.path.join(current_dir + '/login/')
sys.path.append(login_dir)
login_module = importlib.import_module("lgn")

def main():
    st.header('로그인하세요!')
    with st.sidebar:
        config = login_module.get_conf()

        # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
        login_module.login_check(config)
    

    # Optional -- adds the title and icon to the current page
    # add_page_title('로그인하세요!')
    
    # Specify what pages should be shown in the sidebar, and what their titles 
    # and icons should be

    if st.session_state.get('authentication_status'):   
        show_pages(
            [
                Page("pages/01_Firstpage/first_main.py", "Home", "🏠"),
                Page("pages/02_Secondpage/second_main.py", "Second_page", ":books:"),
                Page("pages/03_Thirdpage/third_main.py", "Third_page", ":pig:"),
                Page("pages/04_Fourthpage/fourth_main.py" , "Fourth_page" , ":horse:")
            ]
        )


if __name__ == "__main__":
    # 로그인 성공 후 메인 함수 실행
    main()  