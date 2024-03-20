import importlib
import streamlit as st
import pandas as pd
import os
import plotly.graph_objs as go
import sys
from matplotlib.colors import rgb2hex
import seaborn as sns


#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))
# src 디렉토리로 이동하기 위해 두 단계 위로 올라감
src_dir = os.path.dirname(os.path.dirname(current_dir))
# src 디렉토리에서 lib 폴더의 경로를 구성
library_path = os.path.join(src_dir , 'lib')
# resource_path = os.path.join(src_dir, 'resource')
###############################################
sys.path.append(library_path)
# sys.path.append(resource_path)
###############################################
# resource_module = importlib.import_module("resource.databricks")
# print(f'1 : {library_path}')
library_module = importlib.import_module("lib")
# print(f'2 : {library_module}')
###############################################
# 모듈에서 'get_databricks_data' 클래스 접근
# get_databricks_data = getattr(resource_module, 'get_databricks_data')
get_lib_module = getattr(library_module ,'Trend_AnalysisTools')
# print(f'3 : {get_lib_module}')
###############################################
# 모듈에서 함수 접근
# databricks_data = get_databricks_data()

analysis_tools = get_lib_module()

class SecondContents:
    def __init__(self, first_contents_instance):
        self.first_contents_instance = first_contents_instance
        self.second()
        
    
    
    def second(self):
        ##################################################################################################
     
        # 작은 크기 left right -> 3개
        # 컬럼의 너비를 조정합니다.
        

        # setup_state 메서드 호출로 필요한 상태 설정
        

        # dynamic_filter_df 속성에 접근
        
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        dynamic_filter_df = self.first_contents_instance.dynamic_filter_df

        ################################차트#####################################################
        df_classify = dynamic_filter_df
        df_classify.index = pd.to_datetime(df_classify['bsymd'], format='%Y%m%d', errors='coerce')
        # 불량유형에 따른 그래프를 그리기 위한 빈 Figure 생성

        fig = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()
        # 대분류에 따른 색상 매핑

        # # 조합된 팔레트에서 색상 선택
        # # 필요하다면 팔레트의 색상을 반복하거나 추가하여 100개를 만듭니다.
        palette = sns.color_palette("tab20", 40)
        color_palette = [rgb2hex(rgb) for rgb in palette]
        # color_palette = px.colors.qualitative.Alphabet *2 
        palette2 = sns.color_palette("Dark2", 40)
        color_palette2 = [rgb2hex(rgb) for rgb in palette2]
 

        if self.first_contents_instance.filter_name  == False:

            fig , fig2 = analysis_tools.create_graphs_by_classification(
                filter_name='lcls_nm', 
                df_classify=df_classify, 
                fig_bar=fig, 
                fig_pie=fig2, 
                color_palette=color_palette, 
                create_bar=True, 
                create_pie=True
            )

            _, fig3 = analysis_tools.create_graphs_by_classification(
                filter_name='buy_way_nm',
                df_classify=df_classify,
                fig_bar=fig,
                fig_pie=fig3,
                color_palette=color_palette2,
                create_bar=False,
                create_pie=True
            )

            _, fig4 = analysis_tools.create_graphs_by_classification(
                filter_name='unsati_cause_nm',
                df_classify=df_classify,
                fig_bar=fig,
                fig_pie=fig4,
                color_palette=color_palette2,
                create_bar=False,
                create_pie=True
            )

            fig2.update_layout(
                legend=dict(traceorder='normal'),  # 범례의 순서를 정상적으로(추가된 순서대로) 표시합니다.
                title_text='대분류 별 비율'
            )


        # 중분류 'All' 선택 시 중분류 내 키워드 별로 막대그래프 표시
        elif self.first_contents_instance.filter_name  == 'lcls_nm':
            fig , fig2 = analysis_tools.create_graphs_by_classification(
                filter_name='mcls_nm', 
                df_classify=df_classify, 
                fig_bar=fig, 
                fig_pie=fig2, 
                color_palette=color_palette, 
                create_bar=True, 
                create_pie=True
            )

            _, fig3 = analysis_tools.create_graphs_by_classification(
                filter_name='buy_way_nm',
                df_classify=df_classify,
                fig_bar=fig,
                fig_pie=fig3,
                color_palette=color_palette2,
                create_bar=False,
                create_pie=True
            )

            _, fig4 = analysis_tools.create_graphs_by_classification(
                filter_name='unsati_cause_nm',
                df_classify=df_classify,
                fig_bar=fig,
                fig_pie=fig4,
                color_palette=color_palette2,
                create_bar=False,
                create_pie=True
            )

            fig2.update_layout(
                legend=dict(traceorder='normal'),  # 범례의 순서를 정상적으로(추가된 순서대로) 표시합니다.
                title_text='중분류 별 비율'
            )

        # 대분류와 중분류가 특정 값일 경우 해당 값에 대한 막대그래프 표시
        elif self.first_contents_instance.filter_name  == 'mcls_nm' or 'scls_nm':
            fig , fig2 = analysis_tools.create_graphs_by_classification(
                filter_name='scls_nm', 
                df_classify=df_classify, 
                fig_bar=fig, 
                fig_pie=fig2, 
                color_palette=color_palette, 
                create_bar=True, 
                create_pie=True
            )

            _, fig3 = analysis_tools.create_graphs_by_classification(
                filter_name='buy_way_nm',
                df_classify=df_classify,
                fig_bar=fig,
                fig_pie=fig3,
                color_palette=color_palette2,
                create_bar=False,
                create_pie=True
            )

            _, fig4 = analysis_tools.create_graphs_by_classification(
                filter_name='unsati_cause_nm',
                df_classify=df_classify,
                fig_bar=fig,
                fig_pie=fig4,
                color_palette=color_palette2,
                create_bar=False,
                create_pie=True
            )

            fig2.update_layout(
                legend=dict(traceorder='normal'),  # 범례의 순서를 정상적으로(추가된 순서대로) 표시합니다.
                title_text='소분류 별 비율'
            )

        # 레이아웃 설정
        fig.update_layout(
            title='VOC Counts by Classification',
            xaxis_title='Date',
            yaxis_title='VOC Count',
            barmode='stack',  # 바를 나란히 표시
            showlegend=True,
            legend=dict(traceorder='normal')
        )
        fig2.update_layout(
            legend=dict(traceorder='normal'),  # 범례의 순서를 정상적으로(추가된 순서대로) 표시합니다.
        )
        fig3.update_layout(
            title='VOC Counts by 구매경로',  # 범례의 순서를 정상적으로(추가된 순서대로) 표시합니다.
        )

        fig4.update_layout(
            title ='VOC Counts by 불만원인'
        )
        # Streamlit 대시보드에 그래프를 표시

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        col1,col2, col3 = st.columns(3)
        with col1:
            with st.container(height=400, border=None):
                st.plotly_chart(fig2, use_container_width=True)
        with col2:
            with st.container(height=400, border=None):
                st.plotly_chart(fig3, use_container_width=True)
        with col3:
            with st.container(height=400, border=None):
                st.plotly_chart(fig4, use_container_width=True)
        df_classify = df_classify.sort_index(ascending=False)

        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        st.subheader("RAW DATA")
        st.dataframe(df_classify , use_container_width=True , height = 400)
    

