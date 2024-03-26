import streamlit as st
import pandas as pd
## 추가


def run_sum_main(data_loader):

    df_raw = data_loader.dm_clm_proc_data

    from_date, to_date = pd.to_datetime(df_raw['bsymd'].max()).replace(day=1), df_raw['bsymd'].max()


    col1, col2, col3, col4 = st.columns([8, 0.8, 0.8, 0.8])
    with st.container():
        with col1 : 
            st.header("Header")
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
            st.subheader('Subheader')
            with st.container(height=400, border=None):
                st.write('Contents')
                st.write(df_raw.head(20))
        with col2 :
            select_options = ['전체', 'SELECT1', 'SELECT2']
            select_value = st.selectbox("Select BOX:", select_options)
        with col3 :
            from_date = st.date_input('from_date:', from_date, key = 'from_date')
            from_date = pd.Timestamp(from_date)
        with col4 :
            to_date = st.date_input('to_date:', to_date, key = 'to_date')
            to_date = pd.Timestamp(to_date)