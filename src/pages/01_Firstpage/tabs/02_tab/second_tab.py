import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
########### [Layout] ##############

# st.container() 안에 columns들 설정해야 레이아웃 잡는데 편합니다.
# markdown은 기호에 따라 삭제하셔도 무방합니다.

#######################################
def run_anomaly_main(data_loader):

    ########### [데이터 갖고 오기] ##############

    # data_loader : get_databricks_data 클래스의 인스턴스를 참조하는 변수
    # data_loader는 get_databricks_data 인스턴스내 참조되어있는 메서드 load_all_data 갖고 온다.
    # get_databricks_data 인스턴스내 dm_clm_proc_data 함수를 갖고 온다.
    #############################################
    df_raw = data_loader.dm_clm_proc_data
    col1, col2, col3, col4 = st.columns([8, 1, 1, 1])

    min_date, max_date = df_raw['bsymd'].min(), df_raw['bsymd'].max()


    today = pd.to_datetime("today")
    max_date = today
    default_start_date = max_date - pd.DateOffset(months=3)

    with col1:
        st.header("Second Page Header1")
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
      

    with col2:
        select_options = ['전체', 'SELECT1', 'SELECT2']
        select_value = st.selectbox("Select BOX:", select_options , key='select_options_1')
    with col3:
        start_date = st.date_input('Start date', default_start_date, key = 'start_date1001')
        
    with col4:
        end_date = st.date_input('End date', max_date, key='end_date1001')
        

    left_col, right_col = st.columns([6, 6])

    with left_col:
        st.subheader('Second Left col SubHeader')
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        ########### [st.container() Layout 잡기] ##############

        # st.container()의 파라미터는 하단 링크 참조
        # https://docs.streamlit.io/library/api-reference/layout/st.container  

        #############################################
        with st.container(height=1450, border=None):
            st.write('Contents')
            st.write(df_raw.head(10))

    with right_col:
        with st.container() :
            st.subheader('Right col Subheader')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)    
            with st.container(height=400, border=None):
                st.write('Contents2')
        
        with st.container() :
            st.subheader('Right col Subheader2')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)  
            with st.container(height=400, border=None):
                st.write('Contents3')

        with st.container() :
            st.subheader('Right col Subheader3')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
            with st.container(height=400, border=None):
                st.write('Contents4')

    col1, col2, col3, col4, col5, col6 = st.columns([8, 1, 1, 0.05, 1, 1])



    with col1:
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        st.header("Second Page Header2")
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)

