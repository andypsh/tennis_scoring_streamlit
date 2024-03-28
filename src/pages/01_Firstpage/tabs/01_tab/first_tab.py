import streamlit as st
import pandas as pd
## 추가


def run_sum_main(data_loader):
    
    df_raw = data_loader.dm_clm_proc_data

    from_date, to_date = pd.to_datetime(df_raw['bsymd'].max()).replace(day=1), df_raw['bsymd'].max()

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
    with st.container():
        with col1 : 
            st.header("Header")
            st.markdown('<div class="colored-bg">st.columns col1 범위</div>', unsafe_allow_html=True)
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)

        with col2 :
            st.markdown('<div class="colored-bg">st.columns col2 범위</div>', unsafe_allow_html=True)
            select_options = ['전체', 'SELECT1', 'SELECT2']
            select_value = st.selectbox("Select BOX:", select_options)
            
        with col3 :
            st.markdown('<div class="colored-bg">st.columns col3 범위</div>', unsafe_allow_html=True)
            from_date = st.date_input('from_date:', from_date, key = 'from_date')
            from_date = pd.Timestamp(from_date)
        with col4 :
            st.markdown('<div class="colored-bg">st.columns col4 범위</div>', unsafe_allow_html=True)
            to_date = st.date_input('to_date:', to_date, key = 'to_date')
            to_date = pd.Timestamp(to_date)

    layout1, layout2 = st.columns([10,2.4])
    with layout1:
        st.subheader('Subheader')
        st.markdown('<div class="colored-bg">st.columns layout1 범위</div>', unsafe_allow_html=True)
        with st.container(height=400, border=None):
            st.write('Contents')
            st.write(df_raw.head(20))
    with layout2:
        st.subheader('Subheader2')
        st.markdown('<div class="colored-bg">st.columns layout2 범위</div>', unsafe_allow_html=True)
        with st.container(height=400, border=None):
            st.write('Contents2')
            st.dataframe(df_raw.head(100))