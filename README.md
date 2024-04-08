# 프로젝트 이름 : Streamlit Starter Package

- Ver 0.1
    - 240404 Andy 수정
- Ver 0.2
    - 240405 Andy 수정
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
- ✅  **Loop 참조 링크 ** : [TabBarItemData](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/Eb-W87ideFxDrTGo2imrIv0Br8kvgZsMytQwlsLfEzYDBA?e=wOCIyM&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTjdTM1ozUkhMWUxSQjIyTU5JM0lVMldJWDUmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjBmNmZhMTg5LWM1NTUtNDhjNi1iODAwLTA2ZWU2OWU3YjUzNSUyMiU3RA%3D%3D)

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

## ⓒ  사용법 _5(내 DATA 에 Filter 적용하기)
#### 1. DynamicFilter 사용하기
##### - ✏️ src/pages/01_Firstpage/tabs/01_tab/third_tab.py 참조

## ⓓ 기능
| 기능 | 기술명  | Loop 링크
| ------ | ------ | ------ |
| login | Streamlit_Authenticator |[streamlit_authenticator](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EXb2JNORODNErAV4z6LA-aMBvDeA5N3OGO1vtFmNaPW9Tg?e=7NL8vf&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTFc2WVNOSEVKWUdOQ0tZQkxZWjZSTUI2TkQmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODg2ZiUyMiU3RA%3D%3D) | |
| GitHub | Git Push/Merge/Pull |
| Page 구성하기 | SideBarMenu Tree |
| Tab 구성하기  | hydralit_components |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Features

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF

Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Tech

Dillinger uses a number of open source projects to work properly:

- [AngularJS] - HTML enhanced for web apps!
- [Ace Editor] - awesome web-based text editor
- [markdown-it] - Markdown parser done right. Fast and easy to extend.
- [Twitter Bootstrap] - great UI boilerplate for modern web apps
- [node.js] - evented I/O for the backend
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML
to Markdown converter
- [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```

This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
