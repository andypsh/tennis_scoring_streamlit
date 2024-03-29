import streamlit as st
import os
import sys
import importlib
import warnings
import extra_streamlit_components as stx
import base64
import json
# FutureWarning을 무시하도록 설정
warnings.filterwarnings("ignore")






#################[Module PATH 지정]###################

# 현재 python 파일과 여려 모듈간 연결을 위한 path 지정

######################################################

current_dir = os.path.dirname(os.path.realpath(__file__))
first_tab_path = os.path.join(current_dir + '/tabs/01_tab/')
second_tab_path = os.path.join(current_dir + '/tabs/02_tab/')
third_tab_path = os.path.join(current_dir + '/tabs/03_tab/')
resource_path = os.path.join('../../resource/')
login_dir = os.path.join('../../../login/')


sys.path.append(first_tab_path)
sys.path.append(second_tab_path)
sys.path.append(third_tab_path)
sys.path.append(resource_path)
sys.path.append(login_dir)


resource_module = importlib.import_module("resource.databricks")
get_databricks_data = getattr(resource_module, 'get_databricks_data')
login_module = importlib.import_module("lgn")

######################################################

def load_and_run_module(module_name, function_name , *args):
    # 모듈 동적 임포트
    module = importlib.import_module(module_name)
    # 모듈 내 함수 실행
    function_to_run = getattr(module, function_name)
    return function_to_run(*args)

def main():

    ################### [st.set_page_config] ####################

    # page_title : Page Title 지정
    # page_icon : emoji 지정 

    #############################################################
    st.set_page_config(layout="wide", page_title = 'Write your Page Title' , page_icon=":memo:")

    


    with st.sidebar:

        ################## [login_module] ##################

        # login_module 내 get_conf() 함수를 통해 로그인 정보를 갖고 온다. 
        # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    
        #####################################################

        config = login_module.get_conf()
        a= login_module.login_check(config)
        print(a)


        ################## [login_module] ##################

        # login_module 내 get_conf() 함수를 통해 로그인 정보를 갖고 온다. 
        # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
        
        #####################################################




    


        ################## [stx.tab_bar] ###################

        # id : 각 TAB 별로 부여할 ID
        # title : TAB 이름 부여
        # description : TAB 설명 부여
        # default : TAB에 대한 default값 지정
        # key : 고유한 key 값 지정

        ####################################################

    unique_key = "tab_bar_" + str(os.getpid())
    
    chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="01.TAB", description="description"),
    stx.TabBarItemData(id="tab2", title="02.TAB", description="description"),
    stx.TabBarItemData(id="tab3", title="03.TAB", description="description")
    ],default = 'tab1' , key =unique_key)
    # if f'tab_bar_{unique_key}' not in st.session_state:
    #     st.session_state[f'tab_bar_{unique_key}'] = False
    #     a=0
    # if st.session_state[f'tab_bar_{unique_key}'] == False  and a==0: 
    #     st.rerun()
    #     a+=1
    print(chosen_id)
    # st.write('is it working')
    st.write(st.session_state)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJ1c2FuIiwiZXhwX2RhdGUiOjE3MTQyMzcwNjcuMjg4Nzc0fQ.WOp8u6gXNM9JUc39F3W1SNXKbQIoMlYBvrS69pkME7c"
    payload = jwt_token.split('.')[1]  # JWT의 두 번째 부분(페이로드)을 가져옵니다.
    decoded_payload = base64.b64decode(payload + "==").decode('utf-8')  # Base64 디코딩
    print(json.loads(decoded_payload))

    with st.container():
        
        ####################################################
        data_loader = get_databricks_data()
        data_loader.load_all_data()



        ########### [동적모듈로딩 방식 활용하여 TAB별 불러오기] ##############
        
        # chosen_id = "TAB ID"
        # load_and_run_module("TAB 이름" , "TAB 내 실행할 모듈 이름" , 데이터 로더 객체)

        ##################################################S##################

        if chosen_id == "tab1":
            load_and_run_module("first_tab", "run_sum_main",data_loader)
        elif chosen_id == "tab2":
            load_and_run_module("second_tab", "run_anomaly_main" ,data_loader)
        elif chosen_id == "tab3":
            load_and_run_module("third_tab", "FirstContents" ,data_loader)







if __name__ == "__main__":
    main()  
