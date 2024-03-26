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