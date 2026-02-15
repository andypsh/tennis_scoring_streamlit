from datetime import datetime
import streamlit as st

import os
import sys
import importlib
import extra_streamlit_components as stx
import hydralit_components as hc



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
    st.set_page_config(layout="wide")
    with st.sidebar:

    ################## [login_module] ##################

    # login_module 내 get_conf() 함수를 통해 로그인 정보를 갖고 온다. 
    # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다

    #####################################################

        config = login_module.get_conf()
        login_module.login_check(config)

    ################## [hydralit_components] ##################

    # nav_bar 메서드 확인은 하단 링크 참조
    # https://github.com/TangleSpace/hydralit_components/blob/main/hydralit_components/NavBar/__init__.py
    # menu_definition 파라미터에 부여할 menu_data 양식은 , 딕셔너리 형태로 지정
    
    # {'id' : id 명 , 'icon' : 사용할 icon , 'label' : 표시할 label 명}

    #####################################################
    if st.session_state.get('authentication_status'):
        menu_data = [
            {'id' :'tab1' ,'icon': "far fa-copy", 'label':"TAB1"},
            {'id':'tab2','label':"TAB2"},
            {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':'subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': ":book:", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
            {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
            {'id':'tab3','icon': ":book:", 'label':"TAB3"},
            {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message
        
        ]
    ################## [hydralit_components , nav_bar 파라미터] ##################

    # 1. menu_definition : 딕셔너리 형태의 인자 상단참고
    # 2. first_select : 2자리 숫자 형식
    # 3. override_theme : 색깔 지정
    # ㄴ ex) 'txc_inactive': 'white','menu_background':'purple','txc_active':'yellow','option_active':'blue'}
    # txc_inactive : tab 기본 텍스트 색상 , menu_background : 메뉴 배경색 , 
    # txc_active : tab이 선택되었을때의 텍스트 색상 , option_actvie : tab이 선택되었을때 해당 탭의 배경색
    # 4. home_name : home 인자 추가 가능(필수요소X) , login_name : login 인자 추가 가능(필수요소X)
    # 5. hide_streamlit_markers : bool 형식(default True), 맨 오른쪽 상단의 'Running' 표시 삭제 -> nav_bar 최상단 위치 가능
    # 6. sticky_nav : bool 형식(default True) , Whether the navbar should be stuck to the top of the window
    # 7. sticky_mode : str 형식 (default 'pinned') , The sticky mode, if permenantly stuck to the top when srolling or not
    #####################################################
        over_theme = {'txc_inactive': 'black' , 'menu_background' : 'skyblue' ,'txc_active' : 'red' , 'option_active' : 'white'}
        chosen_id = hc.nav_bar(
            menu_definition=menu_data,
            first_select = 00,
            override_theme=over_theme,
            # home_name='Home',
            login_name='Logout',
            hide_streamlit_markers= True, #will show the st hamburger as well as the navbar now!
            sticky_nav=False, #at the top or not
            sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
        )
  

        with hc.HyLoader('Now Data loading',hc.Loaders.standard_loaders,index=[3,0,5]):
            with st.container():
                ########### [데이터 갖고 오기] ##############
                
                # data_loader : get_databricks_data 클래스의 인스턴스를 참조하는 변수
                # data_loader는 get_databricks_data 인스턴스내 참조되어있는 메서드 load_all_data 갖고 온다.
                #############################################
                data_loader = get_databricks_data()
                data_loader.load_all_data()
                ################## [hydralit_components] ##################

                # nav_bar내 id 부여에 따른 선택가능

                #####################################################
                if chosen_id == 'tab1':
                    load_and_run_module("first_tab", "run_sum_main",data_loader)


                elif chosen_id == 'tab2':
                    load_and_run_module("second_tab", "run_anomaly_main" ,data_loader)
                    st.write('tab2')
                    print('tab2')
                elif chosen_id == 'subid11' :
                    st.write('this is subid11')
                elif chosen_id == 'subid12' :
                    st.write('this is subid12')
                elif chosen_id == 'subid13' :
                    st.write('this is subid13')
                elif chosen_id == 'Chart':
                    load_and_run_module("third_tab", "FirstContents" ,data_loader)
                    print('tab3')
                elif chosen_id == 'tab3':
                    st.write('tab3')
                elif chosen_id == 'tab4':
                    st.write('tab4')
                elif chosen_id == 'Logout':
                    st.write('아직 로그아웃 기능 사용법 찾는중')
           
    else:
        st.header('로그인 하세요!')

    
if __name__ == "__main__":
    

    # 로그인 성공 후 메인 함수 실행
    main()  
    
    
