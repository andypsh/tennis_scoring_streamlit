import streamlit as st
import pandas as pd
from datetime import datetime


## 추가

def run_tab_content():  # Specialist님 요청대로 함수명 통일

    ########### [데이터 갖고 오기] ##############

    # 현재 SQL이 없으므로 테스트를 위한 가짜 데이터 생성 [cite: 2026-02-15]
    # 추후 SQL 연결 시 이 부분을 data_loader 호출로 변경하시면 됩니다.
    data = {
        "No": range(1, 51),
        "성명": [f"CJ_테니스꾼_{i:02d}" for i in range(1, 51)],
        "레벨": ["A", "B", "C"] * 16 + ["A", "B"],
        "조": [f"{(i - 1) // 5 + 1}조" for i in range(1, 51)]
    }
    df_raw = pd.DataFrame(data)

    # 현재 날짜를 datetime.date 객체로 얻기
    today = datetime.today().date()
    # 3월 8일 대회 기준 3개월 전 계산 [cite: 2026-01-27]
    default_start_date = (today - pd.DateOffset(months=3)).date()
    from_date = default_start_date
    to_date = today

    ########### [HTML 형식] ##############

    # HTML  형식으로 color background 설정

    #######################################
    st.markdown("""
            <style>
            .colored-bg {
                background-color: #f0f0f0;  /* 배경색 설정 */
                border: 1px solid #e0e0e0;  /* 테두리 설정 */
                padding: 10px;
                margin: 10px 0;  /* 위아래 여백 설정 */
            }
                </style>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([8, 0.8, 0.8, 0.8])

    ########### [Layout] ##############

    # st.container() 안에 columns들 설정해야 레이아웃 잡는데 편합니다.
    # markdown은 기호에 따라 삭제하셔도 무방합니다.

    #######################################
    with st.container():
        with col1:
            st.header("🎾 3월 8일 장충 테니스 대회 예선")
            st.markdown('<div class="colored-bg">50인 참가자 조편성 현황</div>', unsafe_allow_html=True)
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>",
                        unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="colored-bg">필터</div>', unsafe_allow_html=True)
            select_options = ['전체'] + [f'{i}조' for i in range(1, 11)]
            select_value = st.selectbox("Select Group:", select_options)

        with col3:
            st.markdown('<div class="colored-bg">조회 시작</div>', unsafe_allow_html=True)
            from_date_input = st.date_input('from_date:', from_date, key='from_date')
            from_date = pd.Timestamp(from_date_input)
        with col4:
            st.markdown('<div class="colored-bg">조회 종료</div>', unsafe_allow_html=True)
            to_date_input = st.date_input('to_date:', to_date, key='to_date')
            to_date = pd.Timestamp(to_date_input)

    layout1, layout2 = st.columns([10, 2.4])
    with layout1:
        st.subheader('📍 참가자 명단')
        st.markdown('<div class="colored-bg">실시간 엔트리 확인</div>', unsafe_allow_html=True)
        with st.container(height=400, border=None):
            if select_value != '전체':
                st.write(df_raw[df_raw['조'] == select_value])
            else:
                st.write(df_raw)

    with layout2:
        st.subheader('📊 조별 정보')
        st.markdown('<div class="colored-bg">통계</div>', unsafe_allow_html=True)
        with st.container(height=400, border=None):
            st.write(f"선택된 조: {select_value}")
            st.write(f"인원: {len(df_raw[df_raw['조'] == select_value]) if select_value != '전체' else 50}명")