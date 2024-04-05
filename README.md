# 프로젝트 이름 : Streamlit Starteer Package

- Ver 0.1
    - 240404 Andy 수정
- Ver 0.2
    - 240405 Andy 수정
---

### ⓐ 템플릿 다운 받기

1. git clone/pull 을 통하여 사용하세요.

    - ✅ **LOOP 참고 링크** : [git pull 방법](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/Eee0lnt2irFAun5oKqVO4fsBid-Dhx28dz2ny0flcXT1OA?e=BXX1OT&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHUEhXU0xIVzVVS1dGQUxVN1RJRktTVTVZUDMmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODhhMCUyMiU3RA%3D%3D)

---

### ⓑ  패키지 설치하기

1. setup.cfg 내 package들 설치(base / 가상환경)
- ```sh
  pip install . 
  ```
- setup.cfg 가 있는 **폴더 Tree**로 이동 이후에 "**pip install .**" 실행해주세요.
    ![setup.cfg 위치](/readme_images/setup.PNG)

2. "**pip install .**" 를 시행하였으나, 아래와 같은 오류가 발생시 "**하단 Loop 참고하여 Pypi 설정**" 
>``` ignored the following versions that require a different python version : 0.55.2 Requires-Python<3.5 " ```
- ✅ **LOOP 참고 링크** : [CJ PYPI 설정방법](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EStqSnylB_tBiKJQx9SrrhUBZyiI0eoavncavkS1T_M3ug?e=SBBg0h&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHSkxOSkZIWkpJSDdOQVlSSVNRWTdLS1hMUVYmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMjg1YmZmZWZiLTUyMzAtNGVmOS05MmVlLTYyZjIxYTUxODJiMiUyMiU3RA%3D%3D) 

3. 이후 "**pip install .**" 재 시행시 **템플릿 관련 패키지 설치 완료**
![package 설치](/readme_images/setup_cfg.PNG)

---
## ⓒ  사용법 
#####  🚨 ️폴더 Tree 둘러보기
- ![폴더Tree1](/readme_images/folder_Tree1.PNG)
<img src="/readme_images/folder_Tree1.PNG" width="300" height="500"></img>
- ![폴더Tree2](/readme_images/folder_Tree.PNG)
1. **resource/databricks.py** 내 "**get_dm_clm_proc**" 메서드 코드 변경

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
<div style="padding-left:30px;"> ❗ **변경해야할 사항** 
- ️✏️  @st.cache_resource()내 ttl 변경. 7200 초 = 2시간
    - ✅ **Loop 참고링크** [Streamlit Cache 참고](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/ETo-vd9MXvRGiroB8sCfiowBxuU3l2U0LvqI66YpqhdI5w?e=wAbfAV&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHSjJIMjY1NlRDNjZSRElWT1FCNkxBSjdDVU0mYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODhkNCUyMiU3RA%3D%3D)
- ✏️ **table명 변경**
- ✏️ ️ds_databricks.select_all("*" , **table 이 위치한  databricks 경로** )
</div>
2. 🚨  **resource/databricks.py** 내 "**setup_data**" 메서드는 "**01_Firstpage/tabs/03_tab/**" 내에서 쓰이는 "**예시 DATA 이므로 참고용으로만 보세요.**"(지우셔도 무방합니다.) 
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


---
## ⓓ 기능
| 기능 | 기술명  | Loop 링크
| ------ | ------ | ------ |
| login | Streamlit_Authenticator |[streamlit_authenticator](https://cjworld.sharepoint.com/:fl:/g/contentstorage/CSP_80efb4a4-591c-46ab-b2c7-56d8114f0b8c/EXb2JNORODNErAV4z6LA-aMBvDeA5N3OGO1vtFmNaPW9Tg?e=7NL8vf&nav=cz0lMkZjb250ZW50c3RvcmFnZSUyRkNTUF84MGVmYjRhNC01OTFjLTQ2YWItYjJjNy01NmQ4MTE0ZjBiOGMmZD1iJTIxcExUdmdCeFpxMGF5eDFiWUVVOExqTjNheXg2QVc4Vk1zMGNxdlV3b3FQTjgwaWtQUDFKeVQ3cGVvV2tfNmRZVSZmPTAxN1hWUTRHTFc2WVNOSEVKWUdOQ0tZQkxZWjZSTUI2TkQmYz0lMkYmYT1Mb29wQXBwJnA9JTQwZmx1aWR4JTJGbG9vcC1wYWdlLWNvbnRhaW5lciZ4PSU3QiUyMnclMjIlM0ElMjJUMFJUVUh4amFuZHZjbXhrTG5Ob1lYSmxjRzlwYm5RdVkyOXRmR0loY0V4VWRtZENlRnB4TUdGNWVERmlXVVZWT0V4cVRqTmhlWGcyUVZjNFZrMXpNR054ZGxWM2IzRlFUamd3YVd0UVVERktlVlEzY0dWdlYydGZObVJaVlh3d01UZFlWbEUwUjBsSFRWcExUVmhDUTBWVVFrTmFVREpSVWtFM1JVeEdNMHhaJTIyJTJDJTIyaSUyMiUzQSUyMmZjNjQ0M2RjLTczYzAtNGU4ZC05ZWU0LTBkNmY3NWUyODg2ZiUyMiU3RA%3D%3D) | |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
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
