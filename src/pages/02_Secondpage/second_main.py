from datetime import datetime
import streamlit as st
from st_pages import hide_pages
import os
import sys
import importlib
import extra_streamlit_components as stx
import hydralit_components as hc



#################[Module PATH 지정]###################

# 현재 python 파일과 여려 모듈간 연결을 위한 path 지정

######################################################

login_dir = os.path.join('../../../login/')

sys.path.append(login_dir)

login_module = importlib.import_module("lgn")




def main():
    st.set_page_config(layout="wide")
    ################## [login_module] ##################

    # login_module 내 get_conf() 함수를 통해 로그인 정보를 갖고 온다. 
    # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다

    #####################################################
    # with st.sidebar:
    #     config = login_module.get_conf()

    #     # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    #     login_module.login_check(config)
    #     with st.sidebar:
    # config = login_module.get_conf()

    # # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    # login_module.login_check(config)

    menu_data = [
        {'id' :'tab1' ,'icon': "far fa-copy", 'label':"TAB1"},
        {'id':'tab2','label':"TAB2"},
        # {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
        # {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
        {'id':'tab3','icon': "💀", 'label':"TAB3"},
        # {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message
       
    ]

    over_theme = {'txc_inactive': '#FFFFFF'}
    chosen_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        # home_name='Home',
        login_name='Logout',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )
    # with st.sidebar:
    #     config = login_module.get_conf()
    #     login_module.login_check(config)
    # st.session_state['selected_tab_id'] = chosen_id
    # st.write(st.session_state['selected_tab_id'])
    # st.write(chosen_id)
    # st.write(st.session_state)
    # print('Second Page')

    # if st.session_state.get('authentication_status'):
    #     if st.session_state['chosen_id'] == True:
    #         st.write('이전선택')
    #         st.write(chosen_id)
    #     unique_key = "tab_bar_" + str(os.getpid())
    #     chosen_id = stx.tab_bar(data=[
    #     stx.TabBarItemData(id="tab1", title="데이터 소개", description="description"),
    #     stx.TabBarItemData(id="tab2", title="기본 용어 및 수집·분석 정보", description="description"),
    #     stx.TabBarItemData(id="tab3", title="데이터 수집 시점별 정보", description="description"),
    #     stx.TabBarItemData(id="tab4", title="자주 묻는 질문", description="description")
    #     ],default = "tab1" , key =unique_key)
    #     st.session_state['chosen_id'] = chosen_id
        
        # tab1, tab2, tab3, tab4=st.tabs([
        #     "데이터 소개",
        #     "기본 용어 및 수집·분석 정보",
        #     "데이터 수집 시점별 정보",
        #     "자주 묻는 질문"
        #     ])
        
        # -------------------------------------------------------------------------------------------------------------------------------
        # tab1 데이터 소개
        # -------------------------------------------------------------------------------------------------------------------------------
    with st.container():
        if chosen_id == 'tab1':
            col1, col2=st.columns([7,3])
            with col1:
                st.write('tab1')

        # -------------------------------------------------------------------------------------------------------------------------------
        # tab2 기본 용어 및 수집·분석 정보
        # -------------------------------------------------------------------------------------------------------------------------------

        if chosen_id == 'tab2':
            st.write('tab2')
        
        elif chosen_id == 'tab3':
            st.write('tab3')
        elif chosen_id == 'tab4':
            st.write('tab4')
        



if __name__ == "__main__":
    

    # 로그인 성공 후 메인 함수 실행
    main()  
    
    
