import streamlit as st
import os
import sys
import importlib
import warnings
import extra_streamlit_components as stx
from st_tabs import TabBar
from st_pages import Page , show_pages
# FutureWarning을 무시하도록 설정
warnings.filterwarnings("ignore")


#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))
first_tab_path = os.path.join(current_dir + '/tabs/01_tab/')
second_tab_path = os.path.join(current_dir + '/tabs/02_tab/')
third_tab_path = os.path.join(current_dir + '/tabs/03_tab/')
resource_path = os.path.join('../../resource/')
login_dir = os.path.join('../../../login/')
###############################################
sys.path.append(first_tab_path)
sys.path.append(second_tab_path)
sys.path.append(third_tab_path)
sys.path.append(resource_path)
sys.path.append(login_dir)
###############################################
resource_module = importlib.import_module("resource.databricks")
get_databricks_data = getattr(resource_module, 'get_databricks_data')
login_module = importlib.import_module("lgn")

def load_and_run_module(module_name, function_name , *args):
    # 모듈 동적 임포트
    module = importlib.import_module(module_name)
    # 모듈 내 함수 실행
    function_to_run = getattr(module, function_name)
    return function_to_run(*args)

def main():
    st.set_page_config(layout="wide", page_title = 'Write your Page Title' , page_icon=":memo:")
    st.header('Fourth Page')

    """
    page_title : 브라우저에 띄울 Page 제목
    page_icon : 브라우저에 띄울 Page Icon
    """
    #######################################################################################
    with st.sidebar:
        config = login_module.get_conf()

        # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
        login_module.login_check(config)
    if st.session_state.get('authentication_status'):
        st.header('FIRST PAGE HEADER')



        chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="tab1", title="01.PAGE", description="description"),
        stx.TabBarItemData(id="tab2", title="02.PAGE", description="description"),
        stx.TabBarItemData(id="tab3", title="03.PAGE", description="description")
        ],default = "tab1" , key = "default")


        """
        id : 각 TAB 별로 부여할 ID
        title : TAB 이름 부여
        description : TAB 설명 부여
        """
        #######################################################################################

        ###########data 한번에 불러오기 ##############
        # 데이터 로더 인스턴스를 생성합니다.
        data_loader = get_databricks_data()
        data_loader.load_all_data()
        """
        resource.py 내 load_all_data 함수 불러온다.
        """
        #############################################
        if chosen_id == "tab1":
        
            load_and_run_module("first_tab", "run_sum_main",data_loader)
        elif chosen_id == "tab2":
            load_and_run_module("second_tab", "run_anomaly_main" ,data_loader)
        elif chosen_id == "tab3":
            load_and_run_module("third_tab", "FirstContents" ,data_loader)




if __name__ == "__main__":
    # 로그인 성공 후 메인 함수 실행
    main()  
    


