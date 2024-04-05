import importlib
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_dynamic_filters_andy import DynamicFilters
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from matplotlib.colors import rgb2hex
import seaborn as sns
import os
import sys

#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))
# src 디렉토리로 이동하기 위해 두 단계 위로 올라감
src_dir = os.path.dirname(os.path.dirname(current_dir))
# src 디렉토리에서 lib 폴더의 경로를 구성

src_dir = os.path.join(current_dir, '..', '..', '..' , '..')
library_path = os.path.join(src_dir ,'lib')
###############################################
sys.path.append(library_path)
###############################################
library_module = importlib.import_module("lib")
###############################################
get_lib_module = getattr(library_module ,'Trend_AnalysisTools')


analysis_tools = get_lib_module()
class FirstContents:
    
    
    def __init__(self ,data_loader):
        self.data_loader = data_loader
        self.setup_state(data_loader)

    ########### [DynamicFilters 클래스 갖고오기] ##############

    # DynamicFilters(갖고올 데이터 변수명 , filters = [필터 리스트]  , filters_name = 'key값')
    # 하단 링크 참조
    # https://discuss.streamlit.io/t/new-component-dynamic-multi-select-filters/49595

    ###########################################################
    def initialize_dynamic_filters(self, data):
        # 'dynamic_filters_instance'가 세션 상태에 없으면 초기화 실행
        if 'dynamic_filters_instance' not in st.session_state:
            st.session_state.dynamic_filters_instance = DynamicFilters(data, filters=[
                'plant_division', 'wname1', 'lcls_nm', 'mcls_nm', 'scls_nm',
                'prdha1_nm', 'prdha2_nm', 'prdha3_nm', 'maktx', 'unsati_cause_nm',
                'buy_way_nm', 'buy_place', 'claim_grd_cd'
            ], filters_name='filters1')

    
    def setup_state(self , data_loader):
        
        plant_list = ['공주공장', '남원공장', '논산1공장', '부산공장', '삼해상사(김포)', '삼해상사(부안1)', '씨푸드_성남', '씨푸드_음성', '씨푸드_이천', '양산공장', '영등포공장', '인천1)당', '인천2)유', '인천3공장', '인천냉동식품', '진천)B2B', '진천)B2B생산', '진천)두부', '진천)육가공', '진천BC']

        oem_list = ['ABRIL', 'C&amp;S (제당)', 'REY PASTIFICIO', 'SFS', 'SHINWIL', '경북과학대', '교동(HMR)_1공장', '교동(HMR)_4공장', '국제제과', '까우제', '꿈꾸는콩', '꿈터식품', '노바렉스(1공장)', '노바렉스(2공장)', '더큰정성', '도야지식품(제당)', '동방푸드마스타(HMR)', '동방푸드마스타(김치)', '동방푸드마스타(냉장수프)', '동방푸드마스타(밥이랑)', '동방푸드마스타(소스드레싱)', '동표', '동화식품', '동희', '두메', '뚜또', '맑은동해', '맑은식품', '미정식품', '미정식품(HMR)', '반찬단지', '본사', '부귀농협', '삼광식품', '삼양패키징 광혜원공장', '상신(2공장_치킨)', '상신(2공장_튀김)', '서울F&amp;B', '서울식품공업(피자)', '서흥 오송공장', '선양', '성보(HMR)', '성보(까페소재)', '성보(덮밥)', '세린식품', '소디프', '시아스(냉동)', '신라에스지', '신미', '신선음성공장', '신선촌', '싱그람', '쌍인', '안산공장', '안성공장', '애드팜', '엄지식품', '엄지식품_성형밥', '에스앤푸드', '영우냉동', '영진그린식품', '오성식품', '우양냉동(장항)', '우양냉동(청양_냉동)', '원일식품(HMR)', '웰츄럴바이오', '이든푸드영농조합', '잇츠올레', '정다운(자연일가)', '제이앤이 아산공장', '진안_건강', '진안공장', '진천선물세트', '진천센터', '참바다', '참프레(HMR)', '참프레(냉동)', '청수', '청우식품', '초록웰푸드', '푸드빌', '푸드빌(HMR)', '푸드웨어', '푸르온(만두)', '풍국면', '하북율원식품', '하이푸드텍', '한국농수산', '한국농협김치_북파주', '한국농협김치_전북지사', '한국농협김치_화성', '한국에스비식품', '한우물 영농조합', '함소아제약']
        
        ########### [데이터 갖고 오기] ##############

        # data_loader : get_databricks_data 클래스의 인스턴스를 참조하는 변수
        # data_loader는 get_databricks_data 인스턴스내 참조되어있는 메서드 load_all_data 갖고 온다.
        # get_databricks_data 인스턴스내 dm_clm_proc_data 함수를 갖고 온다.
        #############################################

        self.df = data_loader.setup_data(return_full_df=True)
        
        col_cal = st.container()

        with col_cal:

            st.header("Third Page Header1")
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
            st.subheader("Filter 선택")

        

            # 컬럼 레이아웃 설정
            name_1,col_space1, name_2, col_space1_2 = st.columns([2, 7.5, 2 , 2.5])
            col_quick_select1, col_quick_select2, col_space4, col_quick_left_select1, col_quick_left_select2 , col_space4_2= st.columns([1,1,7.5,  1, 1 , 2.5])
            col_date_left1, col_date_left2, col1_1, col1_2 , col_mid,  col_date_right1, col_date_right2  ,col1_3, col1_4 = st.columns([1.5,1.5, 1, 1.5, 5 , 1, 1 ,1, 0.5])
                    
        ########### [날짜 지정 필터] ##############

        # st.date_input 파라미터는 하단 링크 참조 
        # https://docs.streamlit.io/library/api-reference/widgets/st.date_input
            
        #############################################
            max_date = today
            default_start_date1 = max_date - pd.DateOffset(months=3)
            with col_date_left1:
                start_date = st.date_input('Start date:', default_start_date1, key = 'start_date_input')
                self.start_date = start_date

            with col_date_left2:
                end_date = st.date_input('End date:', today, key = 'end_date_input')
          
                self.end_date = end_date

            data = self.df


######################################################################################################################
######################################################################################################################
            ########### [로그인 코드] ##############

            # session_state 내에서 name의 key 값의 value 값에 login username이 지정
            
            ########################################
            if 'name' in st.session_state:
                current_user = st.session_state['name']
                if current_user == 'busan':
                    data = data[data['wname1'] == '부산공장']
                elif current_user == 'jincheon':
                    data = data[data['wname1'].isin(['진천BC', '진천)두부', '진천선물세트', '진천)B2B', '진천)육가공', '진천)B2B생산'])]

######################################################################################################################
######################################################################################################################


            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            df_date_range = pd.DataFrame(date_range, columns=['bsymd'])

            data = pd.merge(df_date_range, data, on=['bsymd'], how='left')
            data.dropna(subset=['voc_id' , 'rece_dttm'] , inplace= True)
            
            conditions = [
                data['wname1'].isin(plant_list),  # wname1의 값이 plant_list 내에 있는 경우
                data['wname1'].isin(oem_list)     # wname1의 값이 oem_list 내에 있는 경우
            ]
            choices = ['사업장', 'OEM']

            data['plant_division'] = np.select(conditions, choices, default='Not Specified')
            with st.container():
############################################################################################################################################################
############################################################################################################################################################
                ########### [DynamicFilter(andy) 하이퍼파라미터 부여방법] ##############

                # 1. Filter를 위치시킬 layout 설정을 우선 먼저한다. ex) name_1 , name_2,col_space1, col_space1_2 = st.columns([3, 3, 5.5 , 2.5])v
                # 2. dictionary 형태로 인자들을 받아온다. 
                #    └ {필터적용할 '열' 명 : ('화면에 표시할 이름' , 해당 필터를 위치시킬 위치 변수)} 
                # 3. DynamicFilters 클래스 불러오기.
                #    └ DynamicFilters(데이터 , filters = [필터 적용할 '열' 명 리스트] , 필터 key 값)
                # 자세한 설명은 하단 Loop 참조
                # Loop > 전략적 데이터 분석을 위한 현대적인 분석환경과 프레임워크 > 분석과제 수행 Framework > 기술문서 > streamlit > 기능 > Dynamic Filter 참조

                #################################################################
                name_1 , name_2,col_space1, col_space1_2 = st.columns([3, 3, 5.5 , 2.5])
                col_quick_select1, col_quick_select2, col_quick_select3 , col_space2= st.columns([3,3,3 ,5])
                col_ph_select1, col_ph_select2, col_ph_select3 ,col_maktx_select3 , col_space3_1 = st.columns([3,3,3 , 3, 2])
                col_cause, col_buy_way, col_buy_place, col4_1 = st.columns([3,3,3,5])
                col_grade , col_grade_space = st.columns([3, 11])


                custom_layout_first = {
                'plant_division': ('사업장/OEM', name_1),
                'wname1': ('사업소', name_2),
                'lcls_nm': ('대분류', col_quick_select1),
                'mcls_nm': ('중분류', col_quick_select2),
                'scls_nm': ('소분류', col_quick_select3),
                'prdha1_nm' : ('PH1' , col_ph_select1),
                'prdha2_nm': ('PH2', col_ph_select2),
                'prdha3_nm': ('PH3', col_ph_select3),
                'maktx': ('자재', col_maktx_select3),
                'unsati_cause_nm': ('불만원인', col_cause),
                'buy_way_nm': ('구입경로', col_buy_way),
                'buy_place': ('구입처', col_buy_place),
                'claim_grd_cd' : ('Claim Grade' , col_grade)
                }

                dynamic_filters = DynamicFilters(data, filters= ['plant_division', 'wname1' , 'lcls_nm' ,'mcls_nm' , 'scls_nm' ,'prdha1_nm', 'prdha2_nm' , 'prdha3_nm' ,'maktx' ,'unsati_cause_nm' ,'buy_way_nm' , 'buy_place' ,'claim_grd_cd'], filters_name = 'filters1')

                dynamic_filters.display_filters(location="columns", num_columns=3 , gap="large"  ,custom_layout_definitions = custom_layout_first )
                self.dynamic_filter_df = dynamic_filters.filter_df()
############################################################################################################################################################
############################################################################################################################################################

                # 특정 필터에 대한 사용자 선택 옵션을 가져옴

                filters_to_check = ['lcls_nm', 'mcls_nm', 'scls_nm']
                selections_results = {}
                for filter_name in filters_to_check:
                    selections = dynamic_filters.get_user_selections(filter_name)
                    # 선택된 옵션이 없는 경우 False로 설정
                    selections_results[filter_name] = False if selections is False else True

                self.filter_name = False
                # 선택된 옵션 출력
                for filter_name, is_selected in selections_results.items():
                    if not is_selected:
                        pass
                    else:
                        self.filter_name = filter_name

        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        dynamic_filter_df = self.dynamic_filter_df

        df_classify = dynamic_filter_df
        df_classify.index = pd.to_datetime(df_classify['bsymd'], format='%Y%m%d', errors='coerce')
        # 불량유형에 따른 그래프를 그리기 위한 빈 Figure 생성
        fig = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()
        # 대분류에 따른 색상 매핑
        ########### [차트내 색깔 적용] ##############

        # seaborn 내 color_palette 활용
        # https://seaborn.pydata.org/generated/seaborn.color_palette.html
            
        #############################################
        # # 조합된 팔레트에서 색상 선택
        # # 필요하다면 팔레트의 색상을 반복하거나 추가하여 100개를 만듭니다.
        palette = sns.color_palette("tab20", 40)
        color_palette = [rgb2hex(rgb) for rgb in palette]
        palette2 = sns.color_palette("Dark2", 40)
        color_palette2 = [rgb2hex(rgb) for rgb in palette2]


        if self.filter_name  == False:

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
        elif self.filter_name  == 'lcls_nm':
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
        elif self.filter_name  == 'mcls_nm' or 'scls_nm':
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
        st.dataframe(df_classify.head(100) , use_container_width=True , height = 400)