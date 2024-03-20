import pandas as pd
from datetime import timedelta
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
import numpy as np
from ds_dbconn import ds_databricks


class Summary_AnalysisTools:

    # 이 함수는 float 타입의 값을 백분율로 변환합니다.

    def format_inf(self,value):
        if value == float("inf") or value == float("-inf") or pd.isnull(value):
            return np.nan
        return value

    def format_percentage(self,value):
        if value == float("inf") or value == float("-inf") or pd.isnull(value):
            return "-"
        return f"{value:,.1f}%"

    # 'Signal' 컬럼을 추가합니다.
    def signal_indicator(self,change):
        if change < 0:
            return '🟢'  # 양수인 경우 녹색 원
        elif change > 0:
            return '🔴'  # 음수인 경우 빨간색 원
        else:
            return '🟡'  # 0인 경우 노란색 원

    def noun_extractor(self,text):
        results = []
        try:
            result = kiwi.analyze(text)
            for token, pos, _, _ in result[0][0]:
                if len(token) != 1 and pos.startswith('N'):
                    results.append(token)
        except Exception:
            # 예외가 발생해도 아무 조치를 취하지 않고 넘어갑니다.
            pass
        return results
    
class Trend_AnalysisTools:
  
            
    def select_fault_type(self, df_classify ,start_date, end_date ,selected_plant ,key_suffix, col6_1, col6_2, col6_3):
        df_classify = df_classify[df_classify['wname1'] == selected_plant]
        df_classify['bsymd'] = pd.to_datetime(df_classify['bsymd'])
    
        start_date = pd.to_datetime(start_date).strftime('%Y%m%d')
        end_date = pd.to_datetime(end_date).strftime('%Y%m%d')
        df_classify= df_classify[(df_classify['bsymd'] >= start_date) & (df_classify['bsymd'] <= end_date)].reset_index()

        lcls_nm =df_classify.groupby(['lcls_nm']).sum().sort_values(by='voc_id_count' , ascending = False).index.tolist()
        lcls_nm.insert(0, 'All')  # 목록 시작에 'All' 옵션 추가

        with col6_1:
            self.selected_lcls = st.selectbox('불량유형 선택(대분류)', lcls_nm, key=f'detail_key_lcls_{key_suffix}')
            selected_lcls  = self.selected_lcls
            with col6_2:
                if selected_lcls == 'All':
                    self.selected_mcls = st.selectbox('불량유형 선택(중분류)', ['All'], key=f'detail_key_lcls_idx_{key_suffix}')
                    selected_mcls  = self.selected_mcls
                
                elif selected_lcls != 'All':
                    df_classify = df_classify[df_classify['lcls_nm'] == selected_lcls]
                    mcls_nm =df_classify.groupby(['mcls_nm']).sum().sort_values(by='voc_id_count' , ascending = False).index.tolist()
                    #mcls_nm = df_classify['mcls_nm'].unique().tolist()
                    
                    mcls_nm.insert(0, 'All')
                    self.selected_mcls = st.selectbox('불량유형 선택(중분류)', mcls_nm, key=f'detail_key_mcls_{key_suffix}')
                    selected_mcls  = self.selected_mcls

                with col6_3:
                        if selected_mcls == 'All':
                            self.selected_scls = st.selectbox('불량유형 선택(소분류)', ['All'], key=f'detail_key_mcls_idx_{key_suffix}')
                            selected_scls = self.selected_scls
                        elif selected_mcls != 'All':
                            df_classify = df_classify[df_classify['mcls_nm'] == selected_mcls]
                            scls_nm =df_classify.groupby(['scls_nm']).sum().sort_values(by='voc_id_count' , ascending = False).index.tolist()
                            #scls_nm = df_classify['scls_nm'].unique().tolist()
                            scls_nm.insert(0, 'All')
                            self.selected_scls = st.selectbox('불량유형 선택(소분류)', scls_nm, key=f'detail_key_scls_{key_suffix}')
                            selected_scls = self.selected_scls
                            
                            if selected_scls != 'All':
                                df_classify = df_classify[df_classify['scls_nm'] == selected_scls]
        return df_classify


    def prepare_anomaly_data(self,df, start_date_key ,end_date_key, count_column, date_column , selected_plant):
        # 한 해 전 날짜 계산
        one_year_ago = pd.to_datetime(end_date_key) - timedelta(days=365)
        df_grouped = df.groupby(['bsymd' , 'wname1'])['voc_id_count'].sum().reset_index()
        df_grouped.set_index('bsymd', inplace=True)

        # 날짜 컬럼을 날짜 타입으로 변환
        if not df_grouped.empty:
            bsymd_as_datetime = pd.to_datetime(df_grouped.index.get_level_values('bsymd'))

            # 새로운 datetime 인덱스로 설정
            df_grouped.index = bsymd_as_datetime
            df_grouped = df_grouped.resample('D').asfreq()
        

        #st.session_state[start_date]부터 시작하는 날짜 범위 생성
        start_date = pd.to_datetime(start_date_key)
        end_date = pd.to_datetime(end_date_key)  # df_grouped의 최대 날짜

        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        # 날짜 범위를 사용하여 새 DataFrame 생성
        df_date_range = pd.DataFrame(date_range, columns=[date_column])

        # 새 DataFrame과 기존 df_grouped 병합
        df_grouped = pd.merge(df_date_range, df_grouped, on=date_column, how='left')

        

        # wname1 열의 결측치를 첫 번째 유효한 값으로 채움
   
        first_valid_wname1 = selected_plant
        df_grouped['wname1'].fillna(first_valid_wname1, inplace=True)
        
        # voc_id 열의 결측치를 0으로 채움
        df_grouped['voc_id_count'].fillna(0, inplace=True)
    
        # 날짜를 기준으로 필터링
        df_filtered = df_grouped[df_grouped[date_column] >= one_year_ago]

        # 평균과 표준 편차 계산
        mean = df_filtered[count_column].mean()
        std = df_filtered[count_column].std()

        # 이상치 계산
        df_filtered = df_grouped[df_grouped[date_column] >= start_date]
        df_filtered['upper_bound'] = mean + 3*std
        df_filtered['anomaly'] = df_filtered[count_column] > df_filtered['upper_bound']
        return df_filtered, mean
    


    


    def plot_anomalies(self, df, mean, date_column, count_column, line_color='blue'):
        fig = go.Figure()

        # 원본 데이터 플롯
        fig.add_trace(go.Scatter(
            x=df[date_column], 
            y=df[count_column],
            mode='lines',
            name='Count',
            line=dict(color=line_color),
            opacity=0.25,
            hovertemplate=f'{date_column}: %{{x}}<br>{count_column}: %{{y}}<extra></extra>'
        ))

        # 평균선 플롯
        fig.add_trace(go.Scatter(
            x=df[date_column], 
            y=[mean]*len(df),
            mode='lines',
            name='Average',
            line=dict(color='green', dash='dash'),
            hoverinfo='skip'
        ))

        # 이상치 표시
        anomalies = df[df['anomaly']]
        fig.add_trace(go.Scatter(
            x=anomalies[date_column], 
            y=anomalies[count_column],
            mode='markers',
            name = 'mean(s) + 3sigma(σ)',
            marker=dict(color='red', size=5),
            hovertemplate=f'{date_column}: %{{x}}<br>{count_column}: %{{y}}<extra></extra>'
        ))

        # 레이아웃 설정
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Count',
            showlegend=True
        )
        fig.update_xaxes(range=[df[date_column].min(), df[date_column].max()])

        return fig
    

    def create_combined_anomaly_chart(self, df1, df2, start_date1, end_date1, start_date2, end_date2):
        fig = make_subplots(specs=[[{"secondary_y": False}]])

        # 첫 번째 데이터 세트 처리
        anomalies1 = df1[df1['anomaly']]
        fig.add_trace(
            go.Scatter(
                x=df1.index,
                y=df1['voc_id_count'],
                mode='lines',
                name=f'"{start_date1}" ~ "{end_date1}" 기간',
                line=dict(color='blue'),
                opacity = 0.25,
                text = df1['bsymd'].dt.strftime('%Y/%m/%d'),
                hovertemplate= f'bsymd: %{{text}}<br>voc_id Count: %{{y}}<extra></extra>'
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=anomalies1.index,
                y=anomalies1['voc_id_count'],
                mode='markers',
                name='Period 1 mean(s) + 3sigma(σ)',
                marker=dict(color='#FF8C00', size=5),
                text=anomalies1['bsymd'].dt.strftime('%Y/%m/%d'),
                hovertemplate= f'bsymd: %{{text}}<br>voc_id Count: %{{y}}<extra></extra>'
            ),
            secondary_y=False
        )

        # 두 번째 데이터 세트 처리
        anomalies2 = df2[df2['anomaly']]
        fig.add_trace(
            go.Scatter(
                x=df2.index,
                y=df2['voc_id_count'],
                mode='lines',
                name=f'"{start_date2}" ~ "{end_date2}" 기간',
                line=dict(color='red'),
                opacity = 0.25,
                text=df2['bsymd'].dt.strftime('%Y/%m/%d'),
                hovertemplate= f'bsymd: %{{text}}<br>voc_id Count: %{{y}}<extra></extra>'
            ),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(
                x=anomalies2.index,
                y=anomalies2['voc_id_count'],
                mode='markers',
                name='Period 2 mean(s) + 3sigma(σ)',
                marker=dict(color='red', size=5),
                text=anomalies2['bsymd'].dt.strftime('%Y/%m/%d'),
                hovertemplate= f'bsymd: %{{text}}<br>voc_id Count: %{{y}}<extra></extra>'
            ),
            secondary_y=False
        )

        # 레이아웃 설정
        fig.update_layout(
            title="결합된 일별 VOC 추세 분석",
            xaxis_title='Date',
            yaxis_title='VOC Count',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.5,
                xanchor='center',
                x=0.5
            )
        )
        fig.update_xaxes(range=[df1.index.min(), df1.index.max()])

        return fig
    
    def create_graphs_by_classification(self,filter_name, df_classify, fig_bar, fig_pie, color_palette, create_bar=True, create_pie=True):
        total_counts = df_classify.groupby(filter_name)['voc_id_count'].sum()
        unique_keys = total_counts.index.sort_values(ascending=False).tolist()
        colors = color_palette[:len(unique_keys)]
        color_dict = dict(zip(unique_keys, colors))
        
        # 막대 그래프 생성
        if create_bar:
            sorted_keywords = total_counts.sort_values(ascending=False).index.tolist()

            for keyword in sorted_keywords:
                keyword_df = df_classify[df_classify[filter_name] == keyword]
                keyword_counts = keyword_df.groupby(keyword_df.index)['voc_id_count'].sum()
                
                fig_bar.add_trace(go.Bar(
                    x=keyword_counts.index,
                    y=keyword_counts,
                    name=f'{keyword} VOC Count',
                    marker=dict(color=color_dict[keyword]),
                    hoverinfo='none',
                    hovertemplate=f'{keyword} VOC Count<br>' +'bsymd: %{x|%Y/%m/%d}<br>voc_id: %{y}<extra></extra>'

                ))
            fig_bar.update_layout(xaxis=dict(tickformat='%y/%m/%d'), height=500)

        # 파이 차트 생성
        if create_pie:
            fig_pie.add_trace(go.Pie(
                labels=unique_keys,
                values=[total_counts[keyword] for keyword in unique_keys],
                hole=.3,
                marker=dict(colors=[color_dict[keyword] for keyword in unique_keys]),
                sort=True
            ))

        return fig_bar, fig_pie






class Anomaly_AnalysisTools:
    
    def load_data(self,table):
        # 데이터 로드
        df = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")
        return df