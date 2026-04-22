(evennia-rest-api)=
# Evennia REST API

Evennia 使其資料庫可透過 REST API 訪問
[http://localhost:4001/api](http://localhost:4001/api) 如果使用預設設定在本地執行。 API 允許您從遊戲外部擷取、編輯和建立資源，例如使用您自己的自訂使用者端或遊戲編輯器。  雖然您可以在 Web 瀏覽器中檢視和了解 api，但它實際上是
意味著可以由其他程式以程式碼形式存取。

API 正在使用 [Django Rest Framework][drf]。這使該過程自動化
設定 _views_ （Python 程式碼）來處理 Web 請求的結果。
檢索資料的過程類似於
[Webserver](./Webserver.md) 頁，但此處的檢視將返回 [JSON][json]
您想要的資源的資料。您還可以_傳送_這樣的JSON資料
為了從外部更新資料庫。


(usage)=
## 用法

要啟動API，請將其新增至您的設定檔。

    REST_API_ENABLED = True

主要控制設定是`REST_FRAMEWORK`，它是一個字典。鑰匙
`DEFAULT_LIST_PERMISSION` 和 `DEFAULT_CREATE_PERMISSIONS` 控制誰可以
分別透過 api 檢視和建立新物件。預設情況下，使用者具有
['Builder'等級許可權](./Permissions.md) 或更高等級可以存取這兩個操作。

雖然 api 旨在擴充套件，但 Evennia 提供了多種操作
開箱即用。如果點選`/api`右上角的`Autodoc`按鈕
網站上您將獲得可用端點的精美圖形演示。

以下是使用標準 `requests` 函式庫在 Python 中呼叫 api 的範例。

    >>> import requests
    >>> response = requests.get("https://www.mygame.com/api", auth=("MyUsername", "password123"))
    >>> response.json()
    {'accounts': 'http://www.mygame.com/api/accounts/',
     'objects': 'http://www.mygame.com/api/objects/',
    'characters': 'http://www.mygame.comg/api/characters/',
    'exits': 'http://www.mygame.com/api/exits/',
    'rooms': 'http://www.mygame.com/api/rooms/',
    'scripts': 'http://www.mygame.com/api/scripts/'
    'helpentries': 'http://www.mygame.com/api/helpentries/' }

列出特定型別的物件：

    >>> response = requests.get("https://www.mygame.com/api/objects",
                                auth=("Myusername", "password123"))
    >>> response.json()
    {
    "count": 125,
    "next": "https://www.mygame.com/api/objects/?limit=25&offset=25",
    "previous": null,
    "results" : [{"db_key": "A rusty longsword", "id": 57, "db_location": 213, ...}]}

在上面的範例中，它現在顯示「結果」陣列內的物件，同時它具有表示物件總數的「計數」值，以及下一頁和上一頁的「下一頁」和「上一頁」連結（如果有）。  這稱為[pagination][pagination]，連結顯示「limit」和「offset」作為查詢引數，可以新增到url中以控制輸出。


其他查詢引數可以定義為[過濾器][filters]，它允許您進一步縮小結果範圍。例如，僅取得具有開發者許可權的帳戶：

    >>> response = requests.get("https://www.mygame.com/api/accounts/?permission=developer",
                                auth=("MyUserName", "password123"))
    >>> response.json()
    {
    "count": 1,
    "results": [{"username": "bob",...}]
    }

現在假設您想使用API建立一個[物件](./Objects.md)：

    >>> data = {"db_key": "A shiny sword"}
    >>> response = requests.post("https://www.mygame.com/api/objects",
                                 data=data, auth=("Anotherusername", "mypassword"))
    >>> response.json()
    {"db_key": "A shiny sword", "id": 214, "db_location": None, ...}


在這裡，我們向 `/api/objects` 端點發出了 HTTP POST 請求，其中包含我們想要的 `db_key`。我們得到了新建立的物件的資訊。現在您可以使用 PUT（替換所有內容）或 PATCH（僅替換您提供的內容）發出另一個請求。透過向端點提供 id (`/api/objects/214`)，我們確保更新正確的劍：

    >>> data = {"db_key": "An even SHINIER sword", "db_location": 50}
    >>> response = requests.put("https://www.mygame.com/api/objects/214",
                                data=data, auth=("Anotherusername", "mypassword"))
    >>> response.json()
    {"db_key": "An even SHINIER sword", "id": 214, "db_location": 50, ...}


在大多數情況下，您不會使用 Python 向後端發出 API 請求，
但使用來自某些前端應用程式的Javascript。
有許多 Javascript 庫旨在完成此過程
對於來自前端的請求更容易，例如[AXIOS][axios]，或使用
本機[獲取][fetch]。

(customizing-the-api)=
## 自訂API

總的來說，閱讀 [Django Rest Framework ViewSets](https://www.django-rest-framework.org/api-guide/viewsets) 並
擴充和擴充需要其檔案的其他部分
自訂API。

請檢視[網站](./Website.md)頁面以取得有關如何覆蓋程式碼、範本的協助
和靜態檔案。
- API 範本（用於網頁顯示）位於 `evennia/web/api/templates/rest_framework/`（它必須
如此命名以允許覆蓋原始 REST 框架模板）。
- 靜態檔案位於`evennia/web/api/static/rest_framework/`
- api程式碼位於`evennia/web/api/` - 這裡的`url.py`檔案負責
收集所有檢視類別。

與其他 Web 元件相反，沒有預先設定 `urls.py`
`mygame/web/api/`。這是因為使用 api 註冊模型是
與 REST api 功能緊密整合。最簡單的可能是
複製`evennia/web/api/urls.py`並就地修改。


[wiki-api]: https://en.wikipedia.org/wiki/Application_programming_interface
[drf]: https://www.django-rest-framework.org/
[pagination]: https://www.django-rest-framework.org/api-guide/pagination/
[filters]: https://www.django-rest-framework.org/api-guide/filtering/#filtering
[json]: https://en.wikipedia.org/wiki/JSON
[crud]: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[serializers]: https://www.django-rest-framework.org/api-guide/serializers/
[ajax]: https://en.wikipedia.org/wiki/Ajax_(programming)
[rest]: https://en.wikipedia.org/wiki/Representational_state_transfer
[requests]: https://requests.readthedocs.io/en/master/
[axios]: https://github.com/axios/axios
[fetch]: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
