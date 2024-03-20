import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
from datetime import datetime, timedelta
import plotly.graph_objs as go
## 추가
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np

########################################### 추가 ###########################################

def run_sum_main(data_loader):

    df_raw = data_loader.dm_clm_proc_data
    dm_world_c_data = data_loader.dm_world_c_data
    dm_anomaly_results_data = data_loader.dm_anomaly_results_data



    from_date, to_date = pd.to_datetime(df_raw['bsymd'].max()).replace(day=1), df_raw['bsymd'].max()


    col1, col2, col3, col4 = st.columns([8, 0.8, 0.8, 0.8])
    with col1 : 
        st.header("CLAIM SUMMARY")
    with col2 :
        factory_options = ['전체', '사업장', 'OEM']
        factory_value = st.selectbox("Select plant:", factory_options)
    with col3 :
        from_date = st.date_input('from_date:', from_date, key = 'from_date')
        from_date = pd.Timestamp(from_date)
    with col4 :
        to_date = st.date_input('to_date:', to_date, key = 'to_date')
        to_date = pd.Timestamp(to_date)

 
    df_filtered = df_raw.copy()
    df_filtered = df_filtered[(df_filtered['bsymd'] >= from_date) & (df_filtered['bsymd'] <= to_date)]

    if factory_value == "전체" :
        df_filtered = df_filtered
      
    elif factory_value == "사업장" :
        plant_list = ['공주공장', '남원공장', '논산1공장', '부산공장', '삼해상사(김포)', '삼해상사(부안1)', '씨푸드_성남', '씨푸드_음성', '씨푸드_이천', '양산공장', '영등포공장', '인천1)당', '인천2)유', '인천3공장', '인천냉동식품', '진천)B2B', '진천)B2B생산', '진천)두부', '진천)육가공', '진천BC']
        df_filtered = df_filtered.loc[df_filtered['wname1'].isin(plant_list)]
        
    else :
        oem_list = ['ABRIL', 'C&amp;S (제당)', 'REY PASTIFICIO', 'SFS', 'SHINWIL', '경북과학대', '교동(HMR)_1공장', '교동(HMR)_4공장', '국제제과', '까우제', '꿈꾸는콩', '꿈터식품', '노바렉스(1공장)', '노바렉스(2공장)', '더큰정성', '도야지식품(제당)', '동방푸드마스타(HMR)', '동방푸드마스타(김치)', '동방푸드마스타(냉장수프)', '동방푸드마스타(밥이랑)', '동방푸드마스타(소스드레싱)', '동표', '동화식품', '동희', '두메', '뚜또', '맑은동해', '맑은식품', '미정식품', '미정식품(HMR)', '반찬단지', '본사', '부귀농협', '삼광식품', '삼양패키징 광혜원공장', '상신(2공장_치킨)', '상신(2공장_튀김)', '서울F&amp;B', '서울식품공업(피자)', '서흥 오송공장', '선양', '성보(HMR)', '성보(까페소재)', '성보(덮밥)', '세린식품', '소디프', '시아스(냉동)', '신라에스지', '신미', '신선음성공장', '신선촌', '싱그람', '쌍인', '안산공장', '안성공장', '애드팜', '엄지식품', '엄지식품_성형밥', '에스앤푸드', '영우냉동', '영진그린식품', '오성식품', '우양냉동(장항)', '우양냉동(청양_냉동)', '원일식품(HMR)', '웰츄럴바이오', '이든푸드영농조합', '잇츠올레', '정다운(자연일가)', '제이앤이 아산공장', '진안_건강', '진안공장', '진천선물세트', '진천센터', '참바다', '참프레(HMR)', '참프레(냉동)', '청수', '청우식품', '초록웰푸드', '푸드빌', '푸드빌(HMR)', '푸드웨어', '푸르온(만두)', '풍국면', '하북율원식품', '하이푸드텍', '한국농수산', '한국농협김치_북파주', '한국농협김치_전북지사', '한국농협김치_화성', '한국에스비식품', '한우물 영농조합', '함소아제약']
        df_filtered = df_filtered.loc[df_filtered['wname1'].isin(oem_list)]
        
    
    # https://arnaudmiribel.github.io/streamlit-extras/extras/metric_cards/    
    # st.warning('【EWS점검사항】 ① 쁘띠첼 날파리', icon="⚠️")

    layout1, layout2 = st.columns([10,3])

    with layout1 :
        col1, col2, col3, col4 = st.columns([3, 3, 3, 3])
        df_ano_cnt = len(dm_anomaly_results_data)
        col1.metric(label="Anomaly Detecion(AI)", value=f"{df_ano_cnt} cnt")

        A_grd = ['S21S01S04', 'S21S01S06', 'S21S02S03', 'S21S02S04', 'S21S03S01', 'S24S03S01', 'S24S03S02']
        df_agrade_cnt = len(df_filtered[df_filtered['scls'].isin(A_grd)])
        col2.metric(label="A-grade", value=f"{df_agrade_cnt} cnt")

        md1_cnt = len(df_filtered[(df_filtered['rece_way_nm'] == '엠디원(APP)') | (df_filtered['rece_way_nm'] == '엠디원(APP)')])
        col3.metric(label="MD-Claim", value=f"{md1_cnt} cnt")

        col4.metric(label="TBD", value=f"- cnt")
        style_metric_cards(border_left_color='#FA8825', border_size_px=1, box_shadow=True)

        ######################################### Trend 
        # 불량유형 Rename
        df_line = df_filtered[df_filtered['claim_grd_cd'].isin(['A','B'])]
        replacements = {'A': '01.일반', 'B': '02.중대', 'C': '03.위험', 'etc': '04.기타'}
        df_line['claim_grd_cd'] = df_line['claim_grd_cd'].replace(replacements)

        # 데이터 그룹핑 
        grouped_df = df_line.groupby(['bsymd', 'claim_grd_cd'])['voc_id'].count().reset_index()
        grouped_df = grouped_df.sort_values(by=['bsymd'])
        grouped_df['bsymd'] = pd.to_datetime(grouped_df['bsymd'])
        # grouped_df = grouped_df.resample('D').asfreq()

    
        
        max_date = grouped_df['bsymd'].max()
        end_of_month = pd.to_datetime(f"{max_date.year}-{max_date.month + 1}-01") - timedelta(days=1)
        date_range = pd.date_range(start=grouped_df['bsymd'].min(), end=end_of_month)

        
        df_full = pd.DataFrame(date_range, columns=['bsymd'])
        categories = grouped_df['claim_grd_cd'].unique()
        df_final = pd.DataFrame()
        grouped_df.set_index('bsymd', inplace = True)

        for category in categories:
            # 카테고리와 날짜에 대해 임시 데이터프레임 생성
            temp_df = df_full.copy()
            temp_df['claim_grd_cd'] = category
            
            # 원본 데이터셋과 결합
            temp_df = temp_df.merge(grouped_df[grouped_df['claim_grd_cd'] == category], on=['bsymd', 'claim_grd_cd'], how='left')
            
            # 누락된 'voc_id' 값에 0을 할당
            temp_df['voc_id'] = temp_df['voc_id'].fillna(0)
            
            # 최종 데이터프레임에 결합
            df_final = pd.concat([df_final, temp_df], ignore_index=True)

        # 최종 데이터프레임 정렬
        df_final = df_final.sort_values(by=['bsymd', 'claim_grd_cd']).reset_index(drop=True)
        df_final['voc_id'] = np.where(df_final['bsymd']>=to_date, np.nan, df_final['voc_id'])
        
        fig = go.Figure()

        category_colors = {
        '01.일반': 'rgb(31, 119, 180)',  # Tableau Blue
        '02.중대': 'rgb(255, 127, 14)'   # Tableau Red (이 색상은 대략적인 값이며, 실제 Tableau의 레드와 다를 수 있습니다)
        }
        # 고유한 'claim_grd_cd' 값에 대해 반복하여 각각의 라인을 그립니다.
        for category in df_final['claim_grd_cd'].unique():
            df_filtered2 = df_final[df_final['claim_grd_cd'] == category]
            fig.add_trace(go.Scatter(
                x=df_filtered2['bsymd'],
                y=df_filtered2['voc_id'],
                mode='lines+markers',  # 선과 마커 모두를 포함합니다.
                name=category,
                line=dict(color=category_colors[category]),
                marker=dict(
                    symbol='circle',  # 마커를 뚫린 동그라미로 설정합니다.
                    size=6,  # 마커 크기를 설정합니다.
                    line=dict(color='rgba(0, 0, 0, 1)', width=1)  # 마커의 테두리 두께를 설정합니다.
                )
            ))

        all_dates = df_final['bsymd'].unique()  # 모든 고유 날짜 추출
        fig.update_xaxes(
            tickvals=all_dates,  # 모든 날짜를 tickvals로 설정
        )


        # x축과 y축의 레이블을 설정합니다.
        fig.update_layout(
            yaxis_title='VOC ID Count',
            xaxis=dict(tickformat='%m/%d'),
            height=350,

            legend_yanchor="top",
            legend_y=0.99,
            legend_xanchor="right",
            legend_x=0.99
        )

        st.plotly_chart(fig, use_container_width=True)
        ######################################### Trend ####################
        st.warning('【EWS점검사항】 ① 쁘띠첼 날파리', icon="⚠️")


        col1, col2, col3 = st.columns([5,1.5,6.5])
        with col1 : 
            ######################################### Keyword #################
            with st.container(height=450, border=None):
            
                df_wordc = dm_world_c_data


                if factory_value == "전체" :
                    df_wordc = df_wordc
                
                elif factory_value == "사업장" :
                    plant_list = ['공주공장', '남원공장', '논산1공장', '부산공장', '삼해상사(김포)', '삼해상사(부안1)', '씨푸드_성남', '씨푸드_음성', '씨푸드_이천', '양산공장', '영등포공장', '인천1)당', '인천2)유', '인천3공장', '인천냉동식품', '진천)B2B', '진천)B2B생산', '진천)두부', '진천)육가공', '진천BC']
                    df_wordc = df_wordc.loc[df_wordc['Plant'].isin(plant_list)]
                    
                else :
                    oem_list = ['ABRIL', 'C&amp;S (제당)', 'REY PASTIFICIO', 'SFS', 'SHINWIL', '경북과학대', '교동(HMR)_1공장', '교동(HMR)_4공장', '국제제과', '까우제', '꿈꾸는콩', '꿈터식품', '노바렉스(1공장)', '노바렉스(2공장)', '더큰정성', '도야지식품(제당)', '동방푸드마스타(HMR)', '동방푸드마스타(김치)', '동방푸드마스타(냉장수프)', '동방푸드마스타(밥이랑)', '동방푸드마스타(소스드레싱)', '동표', '동화식품', '동희', '두메', '뚜또', '맑은동해', '맑은식품', '미정식품', '미정식품(HMR)', '반찬단지', '본사', '부귀농협', '삼광식품', '삼양패키징 광혜원공장', '상신(2공장_치킨)', '상신(2공장_튀김)', '서울F&amp;B', '서울식품공업(피자)', '서흥 오송공장', '선양', '성보(HMR)', '성보(까페소재)', '성보(덮밥)', '세린식품', '소디프', '시아스(냉동)', '신라에스지', '신미', '신선음성공장', '신선촌', '싱그람', '쌍인', '안산공장', '안성공장', '애드팜', '엄지식품', '엄지식품_성형밥', '에스앤푸드', '영우냉동', '영진그린식품', '오성식품', '우양냉동(장항)', '우양냉동(청양_냉동)', '원일식품(HMR)', '웰츄럴바이오', '이든푸드영농조합', '잇츠올레', '정다운(자연일가)', '제이앤이 아산공장', '진안_건강', '진안공장', '진천선물세트', '진천센터', '참바다', '참프레(HMR)', '참프레(냉동)', '청수', '청우식품', '초록웰푸드', '푸드빌', '푸드빌(HMR)', '푸드웨어', '푸르온(만두)', '풍국면', '하북율원식품', '하이푸드텍', '한국농수산', '한국농협김치_북파주', '한국농협김치_전북지사', '한국농협김치_화성', '한국에스비식품', '한우물 영농조합', '함소아제약']
                    df_wordc = df_wordc.loc[df_wordc['Plant'].isin(oem_list)]
                
                df_wordc = df_wordc[(df_wordc['Date'] >= from_date) & (df_wordc['Date'] <= to_date)]
                gp = df_wordc.groupby('Word')['Count'].sum().reset_index()
    
                with open('./resource/data.pkl', 'rb') as infile:
                    exclude_words = pickle.load(infile)

                # 불용어 제거
                gp_exclude = gp[~gp['Word'].isin(exclude_words)].sort_values('Count', ascending=False)

                gp_dict = pd.Series(gp_exclude['Count'].values, index=gp_exclude['Word']).to_dict()
                top10 = dict(sorted(gp_dict.items(), key=lambda item: item[1], reverse=True)[:10])
                

                # 워드 클라우드 생성
                wordcloud = WordCloud(font_path = './resource/NanumGothic.ttf', width = 1200, height = 1200,
                                        background_color ='white',
                                        min_font_size = 10).generate_from_frequencies(top10)
                # 워드 클라우드 표시
                wordcloud_image = wordcloud.to_array()

                # matplotlib를 사용하여 워드 클라우드 표시
                plt.imshow(wordcloud_image, interpolation="bilinear")  # interpolation는 이미지 품질 개선을 위해 추가
                plt.axis("off")
                plt.tight_layout(pad=0)
                st.pyplot(plt)

            ######################################### Keyword
        with col2 : 
            with st.container(height=450, border=None):
                top10 = pd.DataFrame(list(top10.items()), columns=['키워드', '빈도'])
                top10.set_index('키워드', inplace = True)
                st.dataframe(top10)
        with col3 :
            
            with st.container(height=450):
                st.image('EWS.png')

    st.markdown('---')


    with layout2 :
        # prev
        previous_from_date = from_date - pd.DateOffset(years=1)
        previous_to_date = to_date - pd.DateOffset(years=1)

        df_filtered_prev = df_raw[(df_raw['bsymd'] >= previous_from_date) & (df_raw['bsymd'] <= previous_to_date)]
        
        if factory_value == "전체" :
            df_filtered_prev = df_filtered_prev      
        elif factory_value == "사업장" :
            plant_list = ['공주공장', '남원공장', '논산1공장', '부산공장', '삼해상사(김포)', '삼해상사(부안1)', '씨푸드_성남', '씨푸드_음성', '씨푸드_이천', '양산공장', '영등포공장', '인천1)당', '인천2)유', '인천3공장', '인천냉동식품', '진천)B2B', '진천)B2B생산', '진천)두부', '진천)육가공', '진천BC']
            df_filtered_prev = df_filtered_prev.loc[df_filtered_prev['wname1'].isin(plant_list)]
        else :
            oem_list = ['ABRIL', 'C&amp;S (제당)', 'REY PASTIFICIO', 'SFS', 'SHINWIL', '경북과학대', '교동(HMR)_1공장', '교동(HMR)_4공장', '국제제과', '까우제', '꿈꾸는콩', '꿈터식품', '노바렉스(1공장)', '노바렉스(2공장)', '더큰정성', '도야지식품(제당)', '동방푸드마스타(HMR)', '동방푸드마스타(김치)', '동방푸드마스타(냉장수프)', '동방푸드마스타(밥이랑)', '동방푸드마스타(소스드레싱)', '동표', '동화식품', '동희', '두메', '뚜또', '맑은동해', '맑은식품', '미정식품', '미정식품(HMR)', '반찬단지', '본사', '부귀농협', '삼광식품', '삼양패키징 광혜원공장', '상신(2공장_치킨)', '상신(2공장_튀김)', '서울F&amp;B', '서울식품공업(피자)', '서흥 오송공장', '선양', '성보(HMR)', '성보(까페소재)', '성보(덮밥)', '세린식품', '소디프', '시아스(냉동)', '신라에스지', '신미', '신선음성공장', '신선촌', '싱그람', '쌍인', '안산공장', '안성공장', '애드팜', '엄지식품', '엄지식품_성형밥', '에스앤푸드', '영우냉동', '영진그린식품', '오성식품', '우양냉동(장항)', '우양냉동(청양_냉동)', '원일식품(HMR)', '웰츄럴바이오', '이든푸드영농조합', '잇츠올레', '정다운(자연일가)', '제이앤이 아산공장', '진안_건강', '진안공장', '진천선물세트', '진천센터', '참바다', '참프레(HMR)', '참프레(냉동)', '청수', '청우식품', '초록웰푸드', '푸드빌', '푸드빌(HMR)', '푸드웨어', '푸르온(만두)', '풍국면', '하북율원식품', '하이푸드텍', '한국농수산', '한국농협김치_북파주', '한국농협김치_전북지사', '한국농협김치_화성', '한국에스비식품', '한우물 영농조합', '함소아제약']
            df_filtered_prev = df_filtered_prev.loc[df_filtered_prev['wname1'].isin(oem_list)]

        previous_summary = df_filtered_prev.groupby('wname1')['voc_id'].count().fillna(0)
        current_summary = df_filtered.groupby('wname1')['voc_id'].count().fillna(0)

        yearly_comparison = pd.DataFrame({
        'Current Year': current_summary,
        'Previous Year': previous_summary,
        'diff': current_summary- previous_summary}).fillna(0)

        yearly_comparison = yearly_comparison.sort_values(by='diff', ascending = False)
        st.dataframe(yearly_comparison, height = 1035)
        
    
#---------------------------------↑↑↑↑(new)----------------------------------------------------