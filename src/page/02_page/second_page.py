import streamlit as st
import pandas as pd
import plotly.express as px

# 프로젝트 루트 디렉터리를 sys.path에 추가

#################################################################
######################### 🔥 Critical Issue #####################
#################################################################
def run_anomaly_main(data_loader):
    # 원본 데이터 로드
    df_raw = data_loader.dm_clm_proc_data
    dm_anomaly_results_data = data_loader.dm_anomaly_results_data
    # 치명 Issu List
    A_grd = ['S21S01S04', 'S21S01S06', 'S21S02S03', 'S21S02S04', 'S21S03S01', 'S24S03S01', 'S24S03S02']

    # Date Filter 배치
    col1, col2, col3, col4 = st.columns([8, 1, 1, 1])

    # 날짜 필터를 위한 최소/최대 날짜 설정
    min_date, max_date = df_raw['bsymd'].min(), df_raw['bsymd'].max()
    default_start_date = max_date - pd.DateOffset(months=3)

    with col1:
        st.header("Second Page Header1")
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
      

    with col2:
        select_options = ['전체', 'SELECT1', 'SELECT2']
        select_value = st.selectbox("Select BOX:", select_options , key='select_options_1')
        # wname1_options = ["All", "Selec"] + list(df_raw['wname1'].unique())
        # wname1_value = st.selectbox("Select plant:", wname1_options, key='wname1_value1000')
    with col3:
        start_date = st.date_input('Start date', default_start_date, key = 'start_date1001')
        start_date = pd.Timestamp(start_date)
    with col4:
        end_date = st.date_input('End date', max_date, key='end_date1001')
        end_date = pd.Timestamp(end_date)

    left_col, right_col = st.columns([6, 6])

    with left_col:
        # GridOptionsBuilder를 사용하여 그리드의 옵션을 설정합니다.
        st.subheader('Second Left col SubHeader')
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        
        with st.container(height=1450, border=None):
            st.write('Contents')
            st.write(df_raw.head(10))

    with right_col:
        # [PANEL2] Raw Subject & Question
        with st.container() :
            st.subheader('Right col Subheader')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)    
            with st.container(height=400, border=None):
                st.write('Contents')
        
    #     # [PANEL3] Prod History
        with st.container() :
            st.subheader('Right col Subheader2')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)  
            with st.container(height=400, border=None):
                st.write('Contents')

                
    #     # [PANEL4] Prod History
        with st.container() :
            st.subheader('Right col Subheader3')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
            with st.container(height=400, border=None):
                st.write('Contents')

                
    # #################################################################
    # ######################### 🧨Anomaly Detection ##################
    # #################################################################
    col1, col2, col3, col4, col5, col6 = st.columns([8, 1, 1, 0.05, 1, 1])



    with col1:
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        st.header("Second Page Header2")
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)

