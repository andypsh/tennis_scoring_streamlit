import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

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
        st.header("Critical Issue")
        

    with col2:
        wname1_options = ["All"] + list(df_raw['wname1'].unique())
        wname1_value = st.selectbox("Select plant:", wname1_options, key='wname1_value1000')
    with col3:
        start_date = st.date_input('Start date', default_start_date, key = 'start_date1001')
        start_date = pd.Timestamp(start_date)
    with col4:
        end_date = st.date_input('End date', max_date, key='end_date1001')
        end_date = pd.Timestamp(end_date)

    # [PANEL1] 치명이슈 Main Table 
    df_filtered = df_raw.copy()
    if wname1_value != "All":
        df_filtered = df_filtered[df_filtered['wname1'] == wname1_value]
    df_filtered = df_filtered[(df_filtered['bsymd'] >= start_date) & (df_filtered['bsymd'] <= end_date) & (df_filtered['scls'].isin(A_grd))]
    df_filtered = df_filtered[['rece_dttm', 'maktx', 'prdha2_nm', 'prdha3_nm','scls', 'scls_nm', 'making_ymd', 'expiry_ymd', 'lotno', 'wname1']].sort_values(by=['rece_dttm'], ascending=False) 


    left_col, right_col = st.columns([6, 6])

    with left_col:
        # GridOptionsBuilder를 사용하여 그리드의 옵션을 설정합니다.
        st.subheader('A grade Issue')    
        gb = GridOptionsBuilder.from_dataframe(df_filtered)

        # 컬럼 너비 조정
        gb.configure_column("rece_dttm", width=120)  
        gb.configure_column("scls", width=100) 
        gb.configure_column("scls_nm", width=100) 
        gb.configure_column("making_ymd", width=80) 
        gb.configure_column("expiry_ymd", width=80)  
        gb.configure_column("lotno", width=80) 
        gb.configure_selection(selection_mode="single", use_checkbox=True) # 싱글 셀렉션과 체크박스 사용 설정
        
        # 그리드 옵션 구성 완료
        grid_options = gb.build()

        # # AgGrid 함수를 사용하여 데이터를 스트림릿 앱에 표시합니다.
        grid_response = AgGrid(df_filtered, 
                            gridOptions=grid_options, 
                            height=700, 
                            update_mode=GridUpdateMode.SELECTION_CHANGED) # SELECTION_CHANGED, FILTERING_CHANGED
        # df_filtered.insert(0, 'check', (((df_filtered["making_ymd"] > 0) | (df_filtered["expiry_ymd"] > 0))))
        # grid_response = st.data_editor(df_filtered)
    # 선택된 행을 selected_rows 변수에 저장
    if 'selected_id' not in st.session_state:
        st.session_state.selected_id = None


    with right_col:
        # [PANEL2] Raw Subject & Question
        with st.container() :
            st.subheader('Raw Subject & Question')    
            selected_rows = grid_response['selected_rows']
            if selected_rows:
                # session_sate dictionary 저장
                st.session_state.selected_id = {'rece_dttm' : selected_rows[0]['rece_dttm'],
                                                'maktx' : selected_rows[0]['maktx'],
                                                'prdha3_nm' : selected_rows[0]['prdha3_nm'],
                                                'scls' : selected_rows[0]['scls']}
                
                selected_df = df_raw[(df_raw['rece_dttm'] == st.session_state.selected_id['rece_dttm'])
                                    & (df_raw['maktx'] == st.session_state.selected_id['maktx'])
                                    & (df_raw['scls'] == st.session_state.selected_id['scls'])]


                st.write(selected_df[['subject', 'qstn_cntn']].reset_index(drop=True))
            else:
                # 선택된 값이 없으면, 두 번째 테이블의 전체 데이터를 표시합니다.
                st.write('※ 왼쪽에서 하나의 제품을 선택하세요.')
        
        # [PANEL3] Prod History
        with st.container() :
            st.subheader('Prod History')  
            if selected_rows:
                selected_df2 = df_raw[(df_raw['maktx'] == st.session_state.selected_id['maktx'])
                                    & (df_raw['scls'] == st.session_state.selected_id['scls'])]
                selected_df2 = selected_df2.sort_values(by=['rece_dttm'], ascending=False)
                selected_df2['making_ymd'] = selected_df2['making_ymd'].fillna(0)
                selected_df2['making_ymd'] = selected_df2['making_ymd'].astype(int)
                selected_df2['expiry_ymd'] = selected_df2['expiry_ymd'].fillna(0)
                selected_df2['expiry_ymd'] = selected_df2['expiry_ymd'].astype(int)
                selected_df2 = selected_df2[['rece_dttm', 'maktx', 'prdha3_nm','scls_nm', 'making_ymd', 'expiry_ymd', 'lotno', 'wname1']]
                st.write(selected_df2.reset_index(drop=True))
            else:
                # 선택된 값이 없으면, 두 번째 테이블의 전체 데이터를 표시합니다.
                st.write('')
                
        # [PANEL4] Prod History
        with st.container() :
            st.subheader('Category History')
            if selected_rows:
                df_ph3 = df_raw.copy()
                if wname1_value != "All":
                    df_ph3 = df_ph3[df_ph3['wname1'] == wname1_value]
                
                df_ph3 = df_ph3[(df_ph3['scls'].isin(A_grd))]
                selected_df3 = df_ph3[(df_ph3['prdha3_nm'] == st.session_state.selected_id['prdha3_nm']) 
                                    & (df_raw['scls'] == st.session_state.selected_id['scls'])]
                
                selected_df3['making_ymd'] = selected_df3['making_ymd'].fillna(0)
                selected_df3['making_ymd'] = selected_df3['making_ymd'].astype(int)
                selected_df3['expiry_ymd'] = selected_df3['expiry_ymd'].fillna(0)
                selected_df3['expiry_ymd'] = selected_df3['expiry_ymd'].astype(int)
                selected_df3 = selected_df3[['rece_dttm', 'maktx', 'prdha3_nm','scls_nm', 'making_ymd', 'expiry_ymd', 'lotno', 'wname1']].sort_values(by=['rece_dttm'], ascending=False)
                st.write(selected_df3.reset_index(drop=True))
            else:
                st.write('')
    st.markdown("---")

                
    #################################################################
    ######################### 🧨Anomaly Detection ##################
    #################################################################
    df_ano = dm_anomaly_results_data
    # Period1&2 Date Filter
    col1, col2, col3, col4, col5, col6 = st.columns([8, 1, 1, 0.05, 1, 1])

    default_start_date2 = max_date - pd.DateOffset(months=13)
    default_start_date3 = default_start_date2 - pd.DateOffset(months=12)
    default_end_date3 = max_date - pd.DateOffset(months=12)

    with col1:
        st.header("Anomaly Detection")
    with col2:
        start_date99 = st.date_input('Start date(period1)', default_start_date2, key='start_date1002')
        start_date99 = pd.Timestamp(start_date99)
    with col3:
        end_date99 = st.date_input('End date(period1)', max_date, key='end_date1002')
        end_date99 = pd.Timestamp(end_date99)
    with col4:
        st.markdown(
        """
        <style>
        .vertical-line {
        border-left: 2px solid #808080;
        height: 100px;
        margin-left: auto;
        margin-right: auto;
        }
        </style>
        <div class="vertical-line"></div>
        """,
        unsafe_allow_html=True)
    with col5:
        start_date100 = st.date_input('Start date(period2)', default_start_date3, key='start_date1003')
        start_date100 = pd.Timestamp(start_date100)
    with col6:
        end_date100 = st.date_input('End date(period2)', default_end_date3, key='end_date1003')
        end_date100 = pd.Timestamp(end_date100)




    left_col, right_col = st.columns([4, 8])

    with left_col:
        # [PANEL5] AI Detection Status
        with st.container() :
            st.subheader("AI Detection Status")
            gb = GridOptionsBuilder.from_dataframe(df_ano)
            # 컬럼 너비 조정
            gb.configure_column("code", width=150)
            gb.configure_column("sku", width=300)
            gb.configure_column("ano_cnt", width=80)
            gb.configure_selection(selection_mode="single", use_checkbox=True) # 싱글 셀렉션과 체크박스 사용 설정
            # 그리드 옵션 구성 완료
            grid_options = gb.build()
            # AgGrid 함수를 사용하여 데이터를 스트림릿 앱에 표시합니다.
            grid_response2 = AgGrid(df_ano, 
                                gridOptions=grid_options, 
                                height=650, update_mode=GridUpdateMode.SELECTION_CHANGED)
            

    with right_col: 
        i = grid_response2['selected_rows']
        if i:
            # Timestamp 설정
            mat_df = df_raw[(df_raw['maktx'] == i[0]['sku']) & (df_raw['bsymd'] >= start_date99)].groupby('bsymd')['voc_id'].count()
            mat_df.index = pd.to_datetime(mat_df.index)
            mat_df = mat_df.resample('D').asfreq() 
            mat_df.fillna(0, inplace=True)

            # Plotly
            # [PANEL6] Trend Plot1 
            st.subheader('[period1] Trend')
            fig = px.line(mat_df, x=mat_df.index, y='voc_id', labels={'voc_id': 'VOC ID Count'})
            fig.update_yaxes(title='')
            fig.update_xaxes(title='')
            fig.update_layout( xaxis=dict(tickformat='%y/%m/%d'), height=300)
            fig.update_traces(line=dict(color='red')) 
            st.plotly_chart(fig, use_container_width=True)


            mat_df_y = df_raw[(df_raw['maktx'] == i[0]['sku']) & (df_raw['bsymd'] >= start_date100) & (df_raw['bsymd'] <= end_date100) ].groupby('bsymd')['voc_id'].count()
            mat_df_y.index = pd.to_datetime(mat_df_y.index)
            mat_df_y = mat_df_y.resample('D').asfreq() 
            mat_df_y.fillna(0, inplace=True)

            # Plotly
            # [PANEL7] Trend Plot2
            st.subheader('[period2] Trend')
            fig = px.line(mat_df_y, x=mat_df_y.index, y='voc_id', labels={'voc_id': 'VOC ID Count'})
            fig.update_yaxes(title='')
            fig.update_xaxes(title='')
            fig.update_layout( xaxis=dict(tickformat='%y/%m/%d'), height=300)
            fig.update_traces(line=dict(color='gray'))
            st.plotly_chart(fig, use_container_width=True)
        else :
            st.write('※ 왼쪽에서 하나의 제품을 선택하세요.')
