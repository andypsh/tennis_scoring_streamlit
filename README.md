# 프로젝트 이름 : Streamlit Starter Package

- Ver 0.1
    - 240404 Andy 수정
- Ver 0.2
    - 240405 Andy 수정
- ver 0.3
    - 240408 Andy 수정 
---
## 아이콘 표시
- ✏️ : **직접 수정해야할 사항**
- ✅  : **Loop 링크**
- 🚨 : **주의 사항**
---
### ⓐ 템플릿 다운 받기

#### 1. git clone/pull 을 통하여 사용하세요.

- ✅ **LOOP 참고 링크** : [git pull 방법](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/Eee0lnt2irFAun5oKqVO4fsBid-Dhx28dz2ny0flcXT1OA?e=BXX1OT&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHUEhXU0xIVzVVS1dGQUxVN1RJRktTVTVZUDMmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODhhMCUyMiU3RA%3D%3D)

---

### ⓑ  패키지 설치하기

#### 1. setup.cfg 내 package들 설치(base / 가상환경)
- ```sh
  pip install . 
  ```
- setup.cfg 가 있는 **폴더 Tree**로 이동 이후에 "**pip install .**" 실행해주세요.
    ![setup.cfg 위치](/readme_images/setup.PNG)

#### 2. "**pip install .**" 를 시행하였으나, 아래와 같은 오류가 발생시 "**하단 Loop 참고하여 Pypi 설정**" 
>``` ignored the following versions that require a different python version : 0.55.2 Requires-Python<3.5 " ```
- ✅ **LOOP 참고 링크** : [CJ PYPI 설정방법](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EStqSnylB_tBiKJQx9SrrhUBZyiI0eoavncavkS1T_M3ug?e=SBBg0h&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHSkxOSkZIWkpJSDdOQVlSSVNRWTdLS1hMUVYmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjg1YmZmZWZiLTUyMzAtNGVmOS05MmVlLTYyZjIxYTUxODJiMiUyMiU3RA%3D%3D) 

#### 3. 이후 "**pip install .**" 재 시행시 **템플릿 관련 패키지 설치 완료**
![package 설치](/readme_images/setup_cfg.PNG)

---
## ⓒ  사용법 _1 (Resource 갖고오기)
#####  🚨 ️폴더 Tree 둘러보기

<img src="/readme_images/folder_Tree1.PNG" width="300" height="500"></img>
![폴더Tree2](/readme_images/folder_Tree.PNG)
#### 1. **resource/databricks.py** 내 "**get_dm_clm_proc**" 메서드 코드 변경

```python
class get_databricks_data :
    def __init__(self):
        self.dm_clm_proc_data = None
        self.dm_trend_data = None
    #################[Resource 불러오기]###################
        
    #cache_resource(ttl 변경)
    # table 명 변경
    # databricks 경로 변경
    # ds_databricks 내 모듈 'select_all' or 'select_query' 사용

    ######################################################
    @st.cache_resource(ttl = 7200)
    def get_dm_clm_proc(_self):
    
        table = 'dm_clm_proc'
        df_raw = ds_databricks.select_all("*", "b10g000565.cis_ano." + f"{table}")

        return df_raw
```
❗ **변경해야할 사항**
- ️✏️  @st.cache_resource()내 ttl 변경. 7200 초 = 2시간
    - ✅ **Loop 참고링크** [Streamlit Cache 참고](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/ETo-vd9MXvRGiroB8sCfiowBxuU3l2U0LvqI66YpqhdI5w?e=wAbfAV&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHSjJIMjY1NlRDNjZSRElWT1FCNkxBSjdDVU0mYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODhkNCUyMiU3RA%3D%3D)
- ✏️ **table명 변경**
- ✏️ ️ds_databricks.select_all("*" , **table 이 위치한  databricks 경로** )

#### 2. 🚨  **resource/databricks.py** 내 "**setup_data**" 메서드는 "**01_Firstpage/tabs/03_tab/**" 내에서 쓰이는 "**예시 DATA 이므로 참고용으로만 보세요.**"(지우셔도 무방합니다.) 
```python
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
```
#### 3. resource/databricks.py내 'load_all_data' 메서드는 페이지를 실행할때 쓰이는 databiricks의 DATA를 한번에 불러올수 있게하는 메서드 입니다.
```
    def load_all_data(self):
        self.dm_clm_proc_data = self.get_dm_clm_proc()
        self.dm_trend_data = self.setup_data(return_full_df=True)
```
- 메서드를 직접 선언하시어, 위의 **"self.dm_trend_data"** 와 같이 인스턴스 변수를 직접 만드셔도 됩니다!

#### 4. Resource 한번에 로드하여 각 페이지의 main.py 에 인스턴스 형태로 불러하기. 
- **EX)** src/pages/01_Firstpage/first_main.py 코드참조 
```python
resource_path = os.path.join('../../resource/')
sys.path.append(resource_path)
resource_module = importlib.import_module("resource.databricks")
get_databricks_data = getattr(resource_module, 'get_databricks_data')

            with st.container():
                
                ########### [데이터 갖고 오기] ##############
                
                # data_loader : get_databricks_data 클래스의 인스턴스를 참조하는 변수
                # data_loader는 get_databricks_data 인스턴스내 참조되어있는 메서드 load_all_data 갖고 온다.
                #############################################
                data_loader = get_databricks_data()
                data_loader.load_all_data()
                
                ########### [동적모듈로딩 방식 활용하여 TAB별 불러오기] ##############
                
                # chosen_id = "TAB ID"
                # load_and_run_module("TAB 이름" , "TAB 내 실행할 모듈 이름" ,  "resource를 갖고오는 클래스 인스턴스 변수")

                ##################################################S##################

                if chosen_id == "tab1":
                    load_and_run_module("first_tab", "run_sum_main",data_loader)
                elif chosen_id == "tab2":
                    load_and_run_module("second_tab", "run_anomaly_main" ,data_loader)
                elif chosen_id == "tab3":
                    load_and_run_module("third_tab", "FirstContents" ,data_loader)
```
- 각 페이지의 main.py 에서 Data를 불러와야 한번에 데이터 로드시 효율적(**시간단축**)으로 불러올수 있게 된다.
- 각 tab에 "**data_loader 인스턴스**"를 부여한다. 
#### 5. 각 TAB에서 data_loader 인스턴스내 메서드 불러오기.
- **EX)** pages/01_Firstpage/tabs/01_tab/first_tab.py 코드 참조
```python
def run_sum_main(data_loader):

    ########### [데이터 갖고 오기] ##############
    
    # data_loader : get_databricks_data 클래스의 인스턴스를 참조하는 변수
    # data_loader는 get_databricks_data 인스턴스내 참조되어있는 메서드 load_all_data 갖고 온다.
    # get_databricks_data 인스턴스내 dm_clm_proc_data 함수를 갖고 온다.
    
    #############################################
    
    df_raw = data_loader.dm_clm_proc_data
```
- dm_clm_proc_data 메서드를 tab에서 불러왔다.
- 이미 main.py에서 데이터를 불러오면서 **CASCHE 처리가 완료** 되어있기 때문에, 빠르게 데이터를 볼수 있다.
---
## ⓒ  사용법 _2(PAGE 형식  갖추기)
#### 1. SidebarMenu Tree 형태 , src/main.py 참조
```python
from st_pages import Page, show_pages, add_page_title
            ################## [Side bar Menu Tree] ##################

            # st-pages 모듈 내 show_pages 클래스 import 
            # Page('구동할 파일' , '이름' , '이모티콘')
        
            #####################################################
            show_pages(
                [
                    Page('main.py', 'Home', "🏠"),
                    Page("pages/01_Firstpage/first_main.py", "First_page", ":smile:"),
                    Page("pages/02_Secondpage/second_main.py", "Second_page", ":books:"),
                    Page("pages/03_Thirdpage/third_main.py", "Third_page", ":pig:"),
                    Page("pages/04_Fourthpage/fourth_main.py" , "Fourth_page" , ":horse:")
                ]
            )
```
- ✏️**Page('구동할 파일', '이름', '이모티콘')**
- ![SideMenu Tree](/readme_images/sidemenuTree.PNG)
- ✅ **Loop 참고링크** : [SideBarMenu Tree](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EdCGG07rf55Oh9wVNcGdb8YBO3uajjdplNfXE8VacERoTQ?e=STfg3j&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHT1FRWU5VNTIzN1RaSElQWEFWR1hBWjIzNkcmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjZhZGYzN2ExLTNkOGMtNGYzNS1iZGNjLTA3NDk1MjU4NTBlNCUyMiU3RA%3D%3D)
---
## ⓒ  사용법 _3(TAB 형식 갖추기)

#### 1. TAB의 경우 2가지 형식을 구현했습니다. 원하시는 TAB을 사용하시면 됩니다.
🚨 기본 **st.tabs** 의 경우 TAB별로 ID 부여가 불가하여, **속도 저하**의 원인이 될수 있습니다.
아래 **2가지 라이브러리** 中 1가지를 사용하시는 것을 추천드립니다.
(**저는 hydralit_components 라이브러리 사용하는 것을 추천합니다.**)

#### 2-1. "extra_streamlit_components" 내 TabBarItemData 메서드 활용
##### - ✏️ src/pages/01_Firstpage/first_main.py 참조

```python
    ################## [stx.tab_bar] ###################

    # id : 각 TAB 별로 부여할 ID
    # title : TAB 이름 부여
    # description : TAB 설명 부여
    # default : TAB에 대한 default값 지정
    # key : 고유한 key 값 지정

    ####################################################
    if st.session_state.get('authentication_status'):
        unique_key = "tab_bar_" + str(os.getpid())
        
        chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id="tab1", title="01.TAB", description="description"),
        stx.TabBarItemData(id="tab2", title="02.TAB", description="description"),
        stx.TabBarItemData(id="tab3", title="03.TAB", description="description")
        ],default = 'tab1' , key =unique_key)
```
- ️✏️ **id(필수수정)** , **title(필수수정)** , **description**(선택기능, **공백처리**[""]시 화면에 안보입니다.)
- ✅  **Loop 참조 링크** : [TabBarItemData](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/Eb-W87ideFxDrTGo2imrIv0Br8kvgZsMytQwlsLfEzYDBA?e=wOCIyM&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTjdTM1ozUkhMWUxSQjIyTU5JM0lVMldJWDUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjBmNmZhMTg5LWM1NTUtNDhjNi1iODAwLTA2ZWU2OWU3YjUzNSUyMiU3RA%3D%3D)

#### 2-2) "hydralit_components" 내 nav_bar 메서드 활용

- ✏️  src/pages/02_Secondpage/second_main.py 참조
```python
################## [hydralit_components] ##################

# nav_bar 메서드 확인은 하단 링크 참조
# https://github.com/TangleSpace/hydralit_components/blob/main/hydralit_components/NavBar/__init__.py
# menu_definition 파라미터에 부여할 menu_data 양식은 , 딕셔너리 형태로 지정

# {'id' : id 명 , 'icon' : 사용할 icon , 'label' : 표시할 label 명}
#####################################################

menu_data = [
    {'id' :'tab1' ,'icon': "far fa-copy", 'label':"TAB1"},
    {'id':'tab2','label':"TAB2"},
    {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':'subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': ":book:", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
    {'id':'tab3','icon': ":book:", 'label':"TAB3"},
    {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message

]

over_theme = {'txc_inactive': 'black' , 'menu_background' : 'skyblue' ,'txc_active' : 'red' , 'option_active' : 'white'}
chosen_id = hc.nav_bar(
    menu_definition=menu_data,
    first_select = 00,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers= True, #will show the st hamburger as well as the navbar now!
    sticky_nav=False, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)
```
![SubMenu ITEM](/readme_images/submenuitem.PNG)
- ✏️  menu_data 변수 수정(딕셔너리 형태) 
    - **id**(필수) , icon(선택) , **label**(필수 , 화면에 표시할 문구)
    - submenu를 구성하기 위해서는 딕셔너리 내에서 다시 선언
    ```python
    {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':'subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': ":book:", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]}
    ```

- ✏️ **파라미터 수정사항**
    - first_select(**필수수정**) : PAGE 로드시 뜨는 첫번째 TAB
    - override_theme(**필수수정**) : TAB 속성 지정
    - home_name , login_name(선택적으로 수정)
    - hide_streamlit_markers(**필수수정**) : bool 형식
    - sticky_nav, sticky_mode(**필수수정**) : False(default) , 'pinned'(defualt)
    
- ✅  **Loop 참조 링크** : [hydralit_components , nav_bar](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/Eb-W87ideFxDrTGo2imrIv0Br8kvgZsMytQwlsLfEzYDBA?e=wOCIyM&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTjdTM1ozUkhMWUxSQjIyTU5JM0lVMldJWDUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjBmNmZhMTg5LWM1NTUtNDhjNi1iODAwLTA2ZWU2OWU3YjUzNSUyMiU3RA%3D%3D)
---
## ⓒ  사용법 _4(Layout 구조 반영하기)

#### 1. LayOut 구조 잡기
##### - ✏️ src/pages/01_Firstpage/tabs/01_tab/first_tab.py 참조
```python
st.markdown("""
        <style>
        .colored-bg {
            background-color: #f0f0f0;  /* 배경색 설정 */
            border: 1px solid #e0e0e0;  /* 테두리 설정 */
            padding: 10px;
            margin: 10px 0;  /* 위아래 여백 설정 */
        }
            </style>""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([8, 0.8, 0.8, 0.8])
########### [Layout] ##############

# st.container() 안에 columns들 설정해야 레이아웃 잡는데 편합니다.
# markdown은 기호에 따라 삭제하셔도 무방합니다.

#######################################
with st.container():
    with col1 : 
        st.header("Header")
        st.markdown('<div class="colored-bg">st.columns col1 범위</div>', unsafe_allow_html=True)
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)

    with col2 :
        st.markdown('<div class="colored-bg">st.columns col2 범위</div>', unsafe_allow_html=True)
        select_options = ['전체', 'SELECT1', 'SELECT2']
        select_value = st.selectbox("Select BOX:", select_options)
        
    with col3 :
        st.markdown('<div class="colored-bg">st.columns col3 범위</div>', unsafe_allow_html=True)
        from_date = st.date_input('from_date:', from_date, key = 'from_date')
        from_date = pd.Timestamp(from_date)
    with col4 :
        st.markdown('<div class="colored-bg">st.columns col4 범위</div>', unsafe_allow_html=True)
        to_date = st.date_input('to_date:', to_date, key = 'to_date')
        to_date = pd.Timestamp(to_date)
```
- ✏️ **LayOut 구조 설정 사항**
    - st.markdown("""<style></style>""") : HTML 형식, LayOut 구조를 **시각적**으로 파악할때 유용(실제 서비스 배포시 **해당부분 삭제**)
    ```python
    st.markdown("""
        <style>
        .colored-bg {
            background-color: #f0f0f0;  /* 배경색 설정 */
            border: 1px solid #e0e0e0;  /* 테두리 설정 */
            padding: 10px;
            margin: 10px 0;  /* 위아래 여백 설정 */
        }
            </style>""", unsafe_allow_html=True)
    ```
    →  **상단**에서 선언
    ```python
    with col1 : 
        st.header("Header")
        st.markdown('<div class="colored-bg">st.columns col1 범위</div>', unsafe_allow_html=True)
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
    ```
    - **st.columns() 메서드를 활용하여 열 Layout을 잡은뒤 st.container() 사용 추천**
    - ![LayOut](/readme_images/Layout.PNG)
    - **st.container()** & **st.columns()** 활용
    
    - **st.container()** 의 경우 내부 파라미터로 크기,높이,테두리를 설정할 수 있다.
    EX) **st.container(height=400 , border=None)**
    ```python
    layout1, layout2 = st.columns([10,2.4])
    with layout1:
        st.subheader('Subheader')
        st.markdown('<div class="colored-bg">st.columns layout1 범위</div>', unsafe_allow_html=True)
        with st.container(height=400, border=None):
            st.write('Contents')
            st.write(df_raw.head(20))
    with layout2:
        st.subheader('Subheader2')
        st.markdown('<div class="colored-bg">st.columns layout2 범위</div>', unsafe_allow_html=True)
        with st.container(height=400, border=None):
            st.write('Contents2')
            st.dataframe(df_raw.head(100))
    ```
    - ![st.container](/readme_images/container.PNG)
#### 2. LayOut 구조 잡기-TIP
##### - ✏️ src/pages/01_Firstpage/tabs/01_tab/second_tab.py 참조
- ![Layout2](/readme_images/Layout2.PNG)
```python
left_col, right_col = st.columns([6, 6])

    with left_col:
        st.subheader('Second Left col SubHeader')
        st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
        ########### [st.container() Layout 잡기] ##############

        # st.container()의 파라미터는 하단 링크 참조
        # https://docs.streamlit.io/library/api-reference/layout/st.container  

        #############################################
        with st.container(height=1450, border=None):
            st.write('Contents')
            st.write(df_raw.head(10))

    with right_col:
        with st.container() :
            st.subheader('Right col Subheader')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)    
            with st.container(height=400, border=None):
                st.write('Contents2')
        
        with st.container() :
            st.subheader('Right col Subheader2')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)  
            with st.container(height=400, border=None):
                st.write('Contents3')

        with st.container() :
            st.subheader('Right col Subheader3')
            st.markdown("<hr style='border-top: 3px solid black; margin-top: 20px; margin-bottom: 20px'/>", unsafe_allow_html=True)
            with st.container(height=400, border=None):
                st.write('Contents4')
```
- ✏️   **st.columns()** 활용하여, 열  Layout 구조를 정한뒤에 , **st.container()** 의 height 파라미터 활용하여 행에 대한 구조를 짠다.  
- 🚨 st.columns() 활용법 : [st.columns](https://docs.streamlit.io/develop/api-reference/layout/st.columns)
- 🚨 st.container()활용법: [st.container](https://docs.streamlit.io/library/api-reference/layout/st.container)
---
## ⓒ  사용법 _5(내 DATA 에 Filter 적용하기)
#### 1. DynamicFilter 사용하기
##### - ✏️ src/pages/01_Firstpage/tabs/01_tab/third_tab.py 참조

```python
with st.container():

    ########### [DynamicFilter(andy) 하이퍼파라미터 부여방법] ##############

    # 1. Filter를 위치시킬 layout 설정을 우선 먼저한다. ex) name_1 , name_2,col_space1, col_space1_2 = st.columns([3, 3, 5.5 , 2.5])v
    # 2. dictionary 형태로 인자들을 받아온다. 
    #    └ {필터적용할 '열' 명 : ('화면에 표시할 이름' , 해당 필터를 위치시킬 위치 변수)} 
    # 3. DynamicFilters 클래스 불러오기.
    #    └ DynamicFilters(데이터 , filters = [필터 적용할 '열' 명 리스트] , 필터 key 값)
    # 자세한 설명은 하단 Loop 참조
    # Loop > 전략적 데이터 분석을 위한 현대적인 분석환경과 프레임워크 > 분석과제 수행 Framework > 기술문서 > streamlit > 기능 > Dynamic Filter 참조

    #################################################################
    col_frst1 , col_frst2 ,col_frst3, col_frst4 = st.columns([3, 3, 5.5 , 2.5])
    col_second1, col_second2, col_second3 , col_second4= st.columns([3,3,3 ,5])
    col_thrd1, col_thrd2, col_thrd3 ,col_thrd4 , col_thrd5 = st.columns([3,3,3 , 3, 2])
    col_fourth1, col_fourth2, col_fourth3, col_fourth4 = st.columns([3,3,3,5])
    col_fifth1 , col_fifth2 = st.columns([3, 11])


    custom_layout_first = {
    'plant_division': ('사업장/OEM', col_frst1),
    'wname1': ('사업소', col_frst2),
    'lcls_nm': ('대분류', col_second1),
    'mcls_nm': ('중분류', col_second2),
    'scls_nm': ('소분류', col_second3),
    'prdha1_nm' : ('PH1' , col_thrd1),
    'prdha2_nm': ('PH2', col_thrd2),
    'prdha3_nm': ('PH3', col_thrd3),
    'maktx': ('자재', col_thrd4),
    'unsati_cause_nm': ('불만원인', col_fourth1),
    'buy_way_nm': ('구입경로', col_fourth2),
    'buy_place': ('구입처', col_fourth3),
    'claim_grd_cd' : ('Claim Grade' , col_fifth1)
    }

    dynamic_filters = DynamicFilters(data, filters= ['plant_division', 'wname1' , 'lcls_nm' ,'mcls_nm' , 'scls_nm' ,'prdha1_nm', 'prdha2_nm' , 'prdha3_nm' ,'maktx' ,'unsati_cause_nm' ,'buy_way_nm' , 'buy_place' ,'claim_grd_cd'], filters_name = 'filters1')
    # ※ num_columns 값 무시
    dynamic_filters.display_filters(location="columns", num_columns=3 , gap="large"  ,custom_layout_definitions = custom_layout_first )
    self.dynamic_filter_df = dynamic_filters.filter_df()
```
 - ① **st.columns()** 활용하여 Filter 위치 지정. 
 - ②  key : value  의 딕셔너리 형태로, {filter  적용할  **'열'**  : **'표시될  이름'** ,  **'위치'**    }
 - ③  display_filters() :  화면에  표시 하는  메서드
 - ④  filter_df () :  **내 DATA 에 Filter 적용**
![Dynamic_Filter](/readme_images/dynamic.PNG)

- ✅  **Loop 참조 링크** : [Dynamic-Filter](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EUkFSyloe1ROsk3J9EBO028BwJV9i_jawwlfnwvROJjEDQ?e=tBHRxR&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHS0pBVkZTUzJEM0tSSExFVE9KNlJBRTVVM1AmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjdiNzdkYTA3LTZjZTItNGJkYi1hMDY3LTU3OGM4OTA5YTRmMyUyMiU3RA%3D%3D)

#### 2. 일반 Filter 사용하기
##### - ✏️ src/pages/01_Firstpage/tabs/01_tab/third_tab.py 참조
- 예시 코드(어떻게 쓰이는지만 파악하시면 됩니다.)
- **pandas**를 활용하여 Filter에 대한 변수를 활용하여 **DataFrame을 수정** 하시면 됩니다. 
```python
default_start_date1 = max_date - pd.DateOffset(months=3)
with col_date_left1:
    start_date = st.date_input('Start date:', default_start_date1, key = 'start_date_input')
    self.start_date = start_date

with col_date_left2:
    end_date = st.date_input('End date:', today, key = 'end_date_input')

    self.end_date = end_date

data = self.df

########### [날짜에 대한 NULL 값 처리로직] ##############

# 원본 DATA 의 날짜가 비어(NULL)있을 경우 채워넣는 코드.
# ※ 지우셔도 무방합니다.
                    
########################################

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
```
---
## ⓒ  사용법 _6(Login 기능 , Streamlit _Authenticator 활용)
#### 1. config.yaml 파일 생성하기
##### - ✏️ src/.streamlit/config.yaml 참조
```
credentials:
  usernames:
    andy:
      name: andy
      password: test # To be replaced with hashed password
    busan:
        name: busan
        password: test # To be replaced with hashed password
    user01 :
        name : user01
        password : "1234" # 숫자는 큰 따옴표 처리
cookie:
  expiry_days: 1
  key: random_signature_key # Must be string
  name: random_cookie_name
preauthorized:
  emails:
  - sunghyuk.park@cj.net
```
① **ID , Password 지정**
```
    지정할 ID:
      name: ID를 사용하는 사람 이름
      password: password (숫자의 경우에는 큰 따옴표("")처리) 
```
② **쿠키 설정**(**exipiry_days** 이외 값  변경 X)
```
cookie:
  expiry_days: 1
  key: random_signature_key # Must be string
  name: random_cookie_name
```

#### 2. 각 페이지의 main.py내에 login 관련 메서드 적용하기
##### - src/main.py 참조
```python
login_dir = os.path.join(current_dir + '/login/')
sys.path.append(login_dir)
login_module = importlib.import_module("lgn")
def main():
    with st.sidebar:
    ################## [login_module] ##################
    
    # login_module 내 get_conf() 함수를 통해 로그인 정보를 갖고 온다. 
    # 사이드바에서 로그인 체크 함수를 호출하고 로그인 상태를 확인한다
    
    #####################################################
        config = login_module.get_conf()
        login_module.login_check(config)

```

>  🚨 Login 기능을 사용하기 위해서는, **각 페이지의 main.py** 내에 
```python
config = login_module.get_conf()
login_module.login_check(config)
```
→  **이 2줄을**  넣어야한다. 
![login](/readme_images/login.PNG)

#### 3. login 이후 권한별로 볼수 있게끔하는 예시코드
##### - ✏️ src/Pages/01_Firstpage/tabs/03_tab/third_tab.py 참조
```python
########### [로그인 코드] ##############

# session_state 내에서 name의 key 값의 value 값에 login username이 지정

########################################
if 'name' in st.session_state:
    current_user = st.session_state['name']
    if current_user == 'busan':
        data = data[data['wname1'] == '부산공장']
    elif current_user == 'jincheon':
        data = data[data['wname1'].isin(['진천BC', '진천)두부', '진천선물세트', '진천)B2B', '진천)육가공', '진천)B2B생산'])]
```
→  ID 에 따라  **DataFrame을 Filter** 처리 하였다. 


- ✅  **Loop 참조 링크** : [Streamlit Authenticator](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EXb2JNORODNErAV4z6LA-aMBvDeA5N3OGO1vtFmNaPW9Tg?e=oDgMSv&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTFc2WVNOSEVKWUdOQ0tZQkxZWjZSTUI2TkQmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODg2ZiUyMiU3RA%3D%3D)
---
## ⓒ  사용법 _7(기타  기능)
#### 1. 차트내 색상 지정
##### - ✏️ src/Pages/01_Firstpage/tabs/03_tab/third_tab.py 참조
```python
import seaborn as sns
from matplotlib.colors import rgb2hex

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

```
① **sns.color_pallete("팔렛트 이름",rgb로 변환시 갯수 )** :
→ Seaborn 라이브러리의 color_palette 함수를 사용하여 "tab20"이라는 미리 정의된 색상 팔레트를 가져옵니다.  Seaborn은 "tab20" 팔레트의 색상을 반복하여 **총 40가지** 색상을 생성

② **color_palette = [rgb2hex(rgb) for rgb in palette]** : 
→  palette 리스트의 각 RGB 색상을 HEX 형식으로 변환

- ✅  **Loop 참조 링크** : [색상 지정](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/Ebll3Ugm72xGvxmEl1_H2PUBlCQheUH3ao89ZJb-a5_1og?e=2tBYg6&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTlpNWE9VUUpYUE5SREw2R01FUzVQNFBXSFYmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmQ1NzZlZTdkLTdlY2UtNGM4NC05NzM1LTk3OGIxY2IzODBlZiUyMiU3RA%3D%3D)

#### 2. Data 로딩 표시
##### - ✏️ src/Pages/01_Firstpage/first_main.py 참조

```
        with hc.HyLoader('Now Data loading',hc.Loaders.standard_loaders,index=[3,0,5]):
            with st.container():
```

- ✅**Streamlit 커뮤니티 링크:** [Hydralit Components](   https://discuss.streamlit.io/t/new-component-20-animated-loaders-updated-navbar-and-more-from-hydralit-components/17650)

![loding](/readme_images/loding.PNG)

#### 3. ICON 및 브라우저에 띄울 이름 설정
##### - ✏️ src/Pages/01_Firstpage/first_main.py 참조
```
def main():

    ################### [st.set_page_config] ####################

    # page_title : Page Title 지정
    # page_icon : emoji 지정 
    #############################################################
    st.set_page_config(layout="wide", page_title = 'Write your Page Title' , page_icon=":memo:")
```

![page_name](/readme_images/page_name.PNG)
## ⓓ 기능
| 기능 | 기술명  | Loop 링크
| ------ | ------ | ------ |
| login | Streamlit_Authenticator |[streamlit_authenticator](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EXb2JNORODNErAV4z6LA-aMBvDeA5N3OGO1vtFmNaPW9Tg?e=7NL8vf&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTFc2WVNOSEVKWUdOQ0tZQkxZWjZSTUI2TkQmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODg2ZiUyMiU3RA%3D%3D) | |
| GitHub | Git Push/Merge/Pull |
| Page 구성하기 | SideBarMenu Tree |
| Tab 구성하기  | hydralit_components |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |