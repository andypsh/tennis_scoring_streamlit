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

# 현재 스크립트의 위치를 기준으로 app_andy_main.py가 있는 경로를 계산합니다.

# Python의 모듈 검색 경로에 andy_main_path를 추가합니다.
#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))
summary_main_path = os.path.join(current_dir + '/page/01_page/')
anomaly_main_path = os.path.join(current_dir + '/page/02_page/')
trend_main_path = os.path.join(current_dir + '/page/03_page/')
login_dir = os.path.join(current_dir + '/login/')
###############################################
resource_path = os.path.join(current_dir + '/resource/')
###############################################
###############################################
#################[Docker Path]#################
#summary_main_path = os.path.join('/workdir/src/page/01.su_page/')
# trend_main_path = os.path.join('/workdir/src/page/02.tr_page/')
# anomaly_main_path = os.path.join( '/workdir/src/page/03.an_page/')
###############################################
###############################################

sys.path.append(summary_main_path)
sys.path.append(anomaly_main_path)
sys.path.append(trend_main_path)
sys.path.append(login_dir)
sys.path.append(resource_path)
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

    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="01.PAGE", description="description"),
    stx.TabBarItemData(id="tab2", title="02.PAGE", description="description"),
    stx.TabBarItemData(id="tab3", title="03.PAGE", description="description")
    ],default = "tab1" , key = "default")

    # show_pages(
    #     [
    #         Page('page/01_page/first_page.py', '1번째 Page' , ":memo:"),
    #         Page('page/02_page/an_page.py', '2번째 Page' , ":memo:"),
    #         Page('page/03_page/app_trend_main.py', '3번째 Page' , ":memo:"),
          
    #     ]
    # )
    # config = login_module.get_conf()
    # login_module.login_check(config)
    # config = get_conf()
    # login_check(config)
    
    ###########data 한번에 불러오기 ##############
    # 데이터 로더 인스턴스를 생성합니다.
    data_loader = get_databricks_data()
    data_loader.load_all_data()

    #############################################
    if chosen_id == "tab1":
        load_and_run_module("first_page", "run_sum_main",data_loader)
    elif chosen_id == "tab2":
        load_and_run_module("second_page", "run_anomaly_main" ,data_loader)
    elif chosen_id == "tab3":
        load_and_run_module("app_third_page_main", "run_trend_main" ,data_loader)




if __name__ == "__main__":

    main()  # 로그인 성공 후 메인 함수 실행


