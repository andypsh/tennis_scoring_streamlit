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
    def __init__(self):
        self.dm_clm_proc_data = None
        self.dm_world_c_data = None
        self.dm_anomaly_results_data = None
        self.dm_rule_detection_data = None


    @st.cache_resource(ttl = 7200)
    def get_dm_clm_proc(_self):
        table = 'dm_clm_proc'
        
        # 데이터 로드
        
        df_raw = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")
        df_raw['bsym'] = df_raw['bsym'].astype(str)
        df_raw['bsymd'] = df_raw['bsymd'].astype(str)
        df_raw['bsymd'] = pd.to_datetime(df_raw['bsymd'])
        
        return df_raw


    @st.cache_resource(ttl = 7200)
    def setup_data(_self, return_full_df = False):
        table = 'dm_trend_all_filter'
 
        df = ds_databricks.select_query(f"select * from b10g000565.cis_ano.{table}")
        df['bsymd'] = pd.to_datetime(df['bsymd'])
        df.dropna(subset=['voc_id', 'rece_dttm'], inplace=True)
        if return_full_df:
            return df
        else:
            df_filtered = df[['bsymd', 'wname1', 'maktx', 'prdha1_nm', 'prdha2_nm', 'prdha3_nm', 
                'lcls_nm', 'mcls_nm', 'scls_nm', 'making_ymd', 'expiry_ymd', 
                'lotno', 'buy_way_nm', 'voc_id_count' , 'claim_grd_cd']]
            return df_filtered
    

    def load_all_data(self):
        self.dm_clm_proc_data = self.get_dm_clm_proc()
        # self.dm_world_c_data = self.get_dm_world_c()
        # self.dm_anomaly_results_data = self.get_dm_anomaly_results()
        # self.dm_rule_detection_data = self.get_dm_rule_detection()
        self.dm_trend_data = self.setup_data(return_full_df=True)

