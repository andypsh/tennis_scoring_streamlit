from datetime import datetime
import streamlit as st
from st_pages import hide_pages
import os
import sys
import importlib
import extra_streamlit_components as stx
import hydralit_components as hc

#################[Module PATH 지정]###################
current_dir = os.path.dirname(os.path.realpath(__file__))
first_tab_path = os.path.join(current_dir, 'tabs', '01_tab')
second_tab_path = os.path.join(current_dir, 'tabs', '02_tab')
third_tab_path = os.path.join(current_dir, 'tabs', '03_tab')
resource_path = os.path.abspath(os.path.join(current_dir, '../../resource/'))
login_dir = os.path.abspath(os.path.join(current_dir, '../../../login/'))

for p in [first_tab_path, second_tab_path, third_tab_path, resource_path, login_dir]:
    if p not in sys.path:
        sys.path.append(p)

login_module = importlib.import_module("lgn")


######################################################

def load_and_run_module(module_name, function_name, *args):
    module = importlib.import_module(module_name)
    importlib.reload(module)
    function_to_run = getattr(module, function_name)
    return function_to_run(*args)


# --- 실제 실행부 ---

# 1. ULTIMATE 모바일 뷰 차단 & 풀사이즈 밀착 CSS [cite: 2026-02-16]
st.markdown("""
    <style>
        /* 상단 헤더 공간 제거 */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* 메인 컨테이너 모든 여백 제거 및 가로 100% 강제 */
        .main .block-container {
            max-width: 100% !important;
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            margin: 0rem !important;
        }

        /* [핵심] 모바일 모드(세션 스택) 강제 차단 및 가로 유지 */
        .stCustomComponentV1 {
            width: 100% !important;
            margin-top: -3.7rem !important; 
            display: flex !important;
            justify-content: center !important;
        }

        /* Hydralit 내부 요소가 세로로 꺾이지 않게 강제 설정 */
        iframe[title="hydralit_components.nav_bar.nav_bar"] {
            min-width: 1000px !important; /* 최소 가로폭을 강제하여 꺾임 방지 */
            width: 100% !important;
        }

        /* 본문 내용 여백 */
        .stVerticalBlock {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            gap: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    config = login_module.get_conf()
    login_module.login_check(config)

if st.session_state.get('authentication_status'):
    # 메뉴 데이터 [cite: 2026-01-27]
    menu_data = [
        {'id': 'tab1', 'icon': "fas fa-users", 'label': "조편성/대진표"},
        {'id': 'tab2', 'icon': "fas fa-edit", 'label': "결과 입력"},
        {'icon': "fa-solid fa-radar", 'label': "상세 현황",
         'submenu': [{'id': 'subid11', 'icon': "fa fa-paperclip", 'label': "승점표"},
                     {'id': 'subid12', 'icon': ":book:", 'label': "득실차"},
                     {'id': 'subid13', 'icon': "fa fa-database", 'label': "Raw Data"}]},
        {'icon': "far fa-chart-bar", 'label': "통계"},
        {'id': 'tab3', 'icon': "fas fa-user-shield", 'label': "운영진 확인"},
        {'id': 'Logout', 'icon': "fas fa-sign-out-alt", 'label': "Logout"}
    ]

    # [COLOR] 클릭 시 흰색 배경 + 검정 글자 [cite: 2026-02-16]
    over_theme = {
        'txc_inactive': 'white',
        'menu_background': 'black',
        'txc_active': 'black',  # 클릭 시 글자색: 검정
        'option_active': 'white'  # 클릭 시 배경색: 흰색
    }

    chosen_id = hc.nav_bar(
        menu_definition=menu_data,
        first_select=0,
        override_theme=over_theme,
        key='prelim_sub_nav',
        hide_streamlit_markers=True,
        sticky_nav=True,
        sticky_mode='pinned',
    )

    with hc.HyLoader('페이지 로딩 중...', hc.Loaders.standard_loaders, index=[3, 0, 5]):
        with st.container():
            if chosen_id == 'tab1':
                load_and_run_module("first_tab", "run_tab_content")
            elif chosen_id == 'tab2':
                load_and_run_module("second_tab", "run_anomaly_main")
            elif chosen_id == 'Logout':
                st.session_state.clear()
                st.rerun()
else:
    st.header('🔐 로그인이 필요한 서비스입니다.')