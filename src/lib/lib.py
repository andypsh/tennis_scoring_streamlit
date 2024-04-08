import plotly.graph_objects as go

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