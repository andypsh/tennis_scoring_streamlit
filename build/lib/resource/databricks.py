import sys
import os
import pandas as pd
from ds_dbconn import ds_databricks
import streamlit as st

#################[Local Path]#################
current_dir = os.path.dirname(os.path.realpath(__file__))
# src 디렉토리로 이동하기 위해 두 단계 위로 올라감
src_dir = os.path.dirname(os.path.dirname(current_dir))
# src 디렉토리에서 lib 폴더의 경로를 구성
library_path = os.path.join(src_dir, 'lib')
###############################################

class get_databricks_data :
    @st.cache_resource(ttl = 7200)
    def get_dm_clm_proc(_self):
        table = 'dm_clm_proc'
        
        # 데이터 로드
        
        df_raw = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")
        # df_raw = ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table} where wname1 in ({_self.user_plant_str})")
        #df_raw = analysis_tools.load_data(table).copy()
        df_raw['bsym'] = df_raw['bsym'].astype(str)
        df_raw['bsymd'] = df_raw['bsymd'].astype(str)
        df_raw['bsymd'] = pd.to_datetime(df_raw['bsymd'])
        
        return df_raw
    @st.cache_resource(ttl = 7200)
    def get_dm_world_c(_self):
        table = 'dm_world_c'
   
        df_wordc = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")
        #df_wordc = ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table} where wname1 in ({_self.user_plant_str})")
        df_wordc['Date'] = df_wordc['Date'].astype(str)
        df_wordc['Date'] = pd.to_datetime(df_wordc['Date'])
        return df_wordc

    @st.cache_resource(ttl = 7200)
    def setup_data(_self, return_full_df = False):
        table = 'dm_trend_all_filter'
 
        # df = ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table} where wname1 in ({_self.user_plant_str})")
        df = ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table}")
        df['bsymd'] = pd.to_datetime(df['bsymd'])
        df.dropna(subset=['voc_id', 'rece_dttm'], inplace=True)
        if return_full_df:
            # st.write('where is na')
            # st.dataframe(df[df['voc_id'].isnull()])
            
            return df
        else:
            df_filtered = df[['bsymd', 'wname1', 'maktx', 'prdha1_nm', 'prdha2_nm', 'prdha3_nm', 
                'lcls_nm', 'mcls_nm', 'scls_nm', 'making_ymd', 'expiry_ymd', 
                'lotno', 'buy_way_nm', 'voc_id_count' , 'claim_grd_cd']]
            # st.write('where is na2')
            # st.dataframe(df_filtered)
            return df_filtered
        

    @st.cache_resource(ttl = 7200)
    def get_dm_anomaly_results(_self):
        table = 'dm_anomaly_results'
        df_ano= ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}").copy()
        #df_ano= ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table} where wname1 in ({_self.user_plant_str})")
        #df_ano = analysis_tools.load_data(table).copy()
        df_ano = df_ano.sort_values(by=['anomaly_count_30d'], ascending = False)
        df_ano = df_ano[['matnr', 'maktx', 'lot_issue']]
        df_ano.columns = ['code','sku', 'lot_issue']

        return df_ano
    
    @st.cache_resource(ttl = 7200)
    def get_dm_rule_detection(_self):
        table = 'dm_rule_detection'

        #rule_df = analysis_tools.load_data(table)
        rule_df = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")
        #rule_df= ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table} where wname1 in ({_self.user_plant_str})")
        return rule_df

