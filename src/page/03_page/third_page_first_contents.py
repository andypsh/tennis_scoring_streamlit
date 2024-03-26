import streamlit as st
import pandas as pd
import numpy as np
from streamlit_dynamic_filters_andy import DynamicFilters


class FirstContents:
    
    
    def __init__(self ,data_loader):
        self.data_loader = data_loader
        self.setup_state(data_loader)
    
    def setup_state(self , data_loader):

        category_list = ['사업장', 'OEM']

        plant_list = ['공주공장', '남원공장', '논산1공장', '부산공장', '삼해상사(김포)', '삼해상사(부안1)', '씨푸드_성남', '씨푸드_음성', '씨푸드_이천', '양산공장', '영등포공장', '인천1)당', '인천2)유', '인천3공장', '인천냉동식품', '진천)B2B', '진천)B2B생산', '진천)두부', '진천)육가공', '진천BC']

        oem_list = ['ABRIL', 'C&amp;S (제당)', 'REY PASTIFICIO', 'SFS', 'SHINWIL', '경북과학대', '교동(HMR)_1공장', '교동(HMR)_4공장', '국제제과', '까우제', '꿈꾸는콩', '꿈터식품', '노바렉스(1공장)', '노바렉스(2공장)', '더큰정성', '도야지식품(제당)', '동방푸드마스타(HMR)', '동방푸드마스타(김치)', '동방푸드마스타(냉장수프)', '동방푸드마스타(밥이랑)', '동방푸드마스타(소스드레싱)', '동표', '동화식품', '동희', '두메', '뚜또', '맑은동해', '맑은식품', '미정식품', '미정식품(HMR)', '반찬단지', '본사', '부귀농협', '삼광식품', '삼양패키징 광혜원공장', '상신(2공장_치킨)', '상신(2공장_튀김)', '서울F&amp;B', '서울식품공업(피자)', '서흥 오송공장', '선양', '성보(HMR)', '성보(까페소재)', '성보(덮밥)', '세린식품', '소디프', '시아스(냉동)', '신라에스지', '신미', '신선음성공장', '신선촌', '싱그람', '쌍인', '안산공장', '안성공장', '애드팜', '엄지식품', '엄지식품_성형밥', '에스앤푸드', '영우냉동', '영진그린식품', '오성식품', '우양냉동(장항)', '우양냉동(청양_냉동)', '원일식품(HMR)', '웰츄럴바이오', '이든푸드영농조합', '잇츠올레', '정다운(자연일가)', '제이앤이 아산공장', '진안_건강', '진안공장', '진천선물세트', '진천센터', '참바다', '참프레(HMR)', '참프레(냉동)', '청수', '청우식품', '초록웰푸드', '푸드빌', '푸드빌(HMR)', '푸드웨어', '푸르온(만두)', '풍국면', '하북율원식품', '하이푸드텍', '한국농수산', '한국농협김치_북파주', '한국농협김치_전북지사', '한국농협김치_화성', '한국에스비식품', '한우물 영농조합', '함소아제약']
        

        self.df = data_loader.setup_data(return_full_df=True)
        
        df = self.df
        ##########################################################################################################################
##########################################################################################################################

        
        # 큰 크기 하나
        col_cal = st.container()

        # Streamlit 대시보드 메인 로직
        with col_cal:

            st.header("Third Page Header1")
            st.markdown('---')
            st.subheader("Filter 선택")


            ################# 날짜 선택###############
            today = pd.to_datetime("today")


            # 컬럼 레이아웃 설정
            name_1,col_space1, name_2, col_space1_2 = st.columns([2, 7.5, 2 , 2.5])
            col_quick_select1, col_quick_select2, col_space4, col_quick_left_select1, col_quick_left_select2 , col_space4_2= st.columns([1,1,7.5,  1, 1 , 2.5])
            col_date_left1, col_date_left2, col1_1, col1_2 , col_mid,  col_date_right1, col_date_right2  ,col1_3, col1_4 = st.columns([1.5,1.5, 1, 1.5, 5 , 1, 1 ,1, 0.5])

            max_date = today
            default_start_date1 = max_date - pd.DateOffset(months=3)
            with col_date_left1:
                start_date = st.date_input('Start date:', default_start_date1, key = 'start_date_input')
                self.start_date = start_date

            with col_date_left2:
                end_date = st.date_input('End date:', today, key = 'end_date_input')
          
                self.end_date = end_date

            data = self.df


#################################################### 로그인 코드 ####################################################
            if 'name' in st.session_state:
                current_user = st.session_state['name']
                if current_user == 'busan':
                    data = data[data['wname1'] == '부산공장']
                elif current_user == 'jincheon':
                    data = data[data['wname1'].isin(['진천BC', '진천)두부', '진천선물세트', '진천)B2B', '진천)육가공', '진천)B2B생산'])]

#####################################################################################################################


            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            # # 날짜 범위를 사용하여 새 DataFrame 생성
            df_date_range = pd.DataFrame(date_range, columns=['bsymd'])

             # 새 DataFrame과 기존 df_grouped 병합
            data = pd.merge(df_date_range, data, on=['bsymd'], how='left')
            data.dropna(subset=['voc_id' , 'rece_dttm'] , inplace= True)
            

           
            # 조건 설정
            conditions = [
                data['wname1'].isin(plant_list),  # wname1의 값이 plant_list 내에 있는 경우
                data['wname1'].isin(oem_list)     # wname1의 값이 oem_list 내에 있는 경우
            ]
            # 조건에 따른 결과 값
            choices = ['사업장', 'OEM']

            # np.select를 사용하여 조건에 따른 결과를 새 열에 할당
            data['plant_division'] = np.select(conditions, choices, default='Not Specified')
            with st.container():
#################################################### 이부분 패키지화 했을때 처리 고려 해야함####################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
                name_1 , name_2,col_space1, col_space1_2 = st.columns([3, 3, 5.5 , 2.5])
                # st.markdown('<div class="colored-bg">col1_4</div>', unsafe_allow_html=True)
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
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
                               
                dynamic_filters = DynamicFilters(data, filters=['plant_division', 'wname1' , 'lcls_nm' ,'mcls_nm' , 'scls_nm' ,'prdha1_nm', 'prdha2_nm' , 'prdha3_nm' ,'maktx' ,'unsati_cause_nm' ,'buy_way_nm' , 'buy_place' ,'claim_grd_cd'], filters_name = 'filters1')
                dynamic_filters.display_filters(location="columns", num_columns=3 , gap="large"  ,custom_layout_definitions = custom_layout_first )
                self.dynamic_filter_df = dynamic_filters.filter_df()
                # dynamic_filters.display_df()
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
                

