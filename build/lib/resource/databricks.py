import sys
import os
import pandas as pd
# from ds_dbconn import ds_databricks
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
        self.dm_trend_data = None
    #################[Resource 불러오기]###################
        
    # cache_resource(ttl 변경)
    # table 명 변경
    # databricks 경로 변경
    # ds_databricks 내 모듈 'select_all' or 'select_query' 사용

    ######################################################
    @st.cache_resource(ttl = 7200 ,show_spinner  = False)
    def get_dm_clm_proc(_self):

        table = 'dm_clm_proc'
        df_raw = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")
        return df_raw

    #################[Resource 불러오기_ setup_resource 메서드]###################
        
    # 예시용
    # 03_tab/third_tab.py 에서 해당 메서드 활용하여 인스턴스 생성.

    ######################################################
    @st.cache_resource(ttl = 7200,show_spinner  = False)
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
            st.write(df_filtered.tail(10))
            return df_filtered
    

    def load_all_data(self):
        self.dm_clm_proc_data = self.get_dm_clm_proc()
        self.dm_trend_data = self.setup_data(return_full_df=True)

