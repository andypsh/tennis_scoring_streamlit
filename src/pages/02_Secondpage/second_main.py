import streamlit as st
import hydralit_components as hc
import importlib
import os
import sys


def run_prelim_page():
    # 현재 파일의 경로를 기준으로 tabs 폴더 경로 설정
    current_dir = os.path.dirname(os.path.realpath(__file__))
    tabs_path = os.path.join(current_dir, 'tabs', '01_tab')

    if tabs_path not in sys.path:
        sys.path.append(tabs_path)

    # --- 서브 탭 내비게이션 바 (검은색 테마) ---
    sub_menu_data = [
        {'id': 'prelim_draw', 'icon': "fas fa-users", 'label': "조편성/대진표"},
        {'id': 'prelim_score', 'icon': "fas fa-edit", 'label': "결과 입력"},
        {'id': 'prelim_status', 'icon': "fas fa-poll", 'label': "조별 현황"},
    ]

    # Specialist 취향 저격 올 블랙 테마
    sub_over_theme = {
        'txc_inactive': '#AAAAAA',  # 비활성: 회색
        'menu_background': '#111111',  # 배경: 아주 진한 검정
        'txc_active': '#FFFFFF',  # 활성: 흰색
        'option_active': '#444444'  # 활성 배경: 진회색
    }

    chosen_tab = hc.nav_bar(
        menu_definition=sub_menu_data,
        override_theme=sub_over_theme,
        key='prelim_sub_nav',  # 메인 내비와 겹치지 않게 고유 키 부여
        hide_streamlit_markers=True
    )

    # 탭별 모듈 호출
    if chosen_tab == 'prelim_draw':
        # tabs/01_tab/first_tab.py 호출
        try:
            tab_module = importlib.import_module("first_tab")
            tab_module.run_tab_content()
        except ImportError as e:
            st.error(f"모듈을 찾을 수 없습니다: {e}")

    elif chosen_tab == 'prelim_score':
        st.info("결과 입력 화면 준비 중...")

    elif chosen_tab == 'prelim_status':
        st.info("조별 리그 순위표 준비 중...")