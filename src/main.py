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
def setup_sidebar():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    login_dir = os.path.join(current_dir, 'login')
    sys.path.append(login_dir)
    login_module = importlib.import_module("lgn")

    config = login_module.get_conf()
    login_module.login_check(config)
    # with st.sidebar:
    #     config = login_module.get_conf()

    #     # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    #     login_module.login_check(config)


# def  __login__obj = __login__(auth_token = "courier_auth_token", 
#                     company_name = "Shims",
#                     width = 200, height = 250, 
#                     logout_button_name = 'Logout', hide_menu_bool = False, 
#                     hide_footer_bool = False, 
#                     lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

# LOGGED_IN = __login__obj.build_login_ui()


def main():
    
    # setup_sidebar()
    with st.sidebar:
        config = login_module.get_conf()

        # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
        login_module.login_check(config)

    # st.session_state['authentication_status'] = None
    # st.session_state['authentication_status'] = "Aa"
    # Optional -- adds the title and icon to the current page
    # add_page_title('로그인하세요!')
    
    # Specify what pages should be shown in the sidebar, and what their titles 
    # and icons should be

    if st.session_state.get('authentication_status'):
            
        st.header('옆에 PAGE를 클릭하세요!')   
        show_pages(
            [
                Page('main.py', 'Home', "🏠"),
                Page("pages/01_Firstpage/first_main.py", "First_page", ":smile:"),
                Page("pages/02_Secondpage/second_main.py", "Second_page", ":books:"),
                Page("pages/03_Thirdpage/third_main.py", "Third_page", ":pig:"),
                Page("pages/04_Fourthpage/fourth_main.py" , "Fourth_page" , ":horse:")
            ]
        )
        # with st.sidebar:
        #     config = login_module.get_conf()

        #     # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
        #     login_module.login_check(config)
    else:
        st.header('로그인하세요!')


if __name__ == "__main__":
    # 로그인 성공 후 메인 함수 실행
    main()  
