(game-website)=
# 遊戲網站

當 Evennia 啟動時，它還將啟動 [Webserver](./Webserver.md) 作為 [伺服器](./Portal-And-Server.md) 程式的一部分。這使用[Django](https://docs.djangoproject.com)來呈現一個簡單但實用的預設遊戲網站。  使用預設設定，開啟瀏覽器到 [localhost:4001](http://localhost:4001) 或 [127.0.0.1:4001](http://127.0.0.1:4001) 來檢視它。

該網站允許現有玩家使用他們之前註冊遊戲時使用的帳戶名稱和密碼登入。如果使用者使用 [Webclient](./Webclient.md) 登入，他們也會登入網站，反之亦然。因此，如果您登入了該網站，開啟 webclient 將會自動以該帳號登入遊戲。

預設網站顯示「歡迎！」頁麵包含一些有用資源的連結。它還顯示了有關當前連線的玩家數量的一些統計資料。

在頂部選單中您可以找到
- _Home_ - 返回首頁。
- _文件_ - 最新穩定Evennia文件的連結。
- _Characters_ - 這是將遊戲中的角色連線到網站的演示。
它將顯示所有實體的列表
  _typeclasses.characters.Character` typeclass 並允許您檢視他們的
  帶有可選影象的描述。此列表僅適用於登入的使用者
  使用者。
- _Channels_ - 這是將遊戲內聊天連線到網站的演示。它將
顯示您可以使用的所有頻道的列表，並允許您檢視最新的頻道
  討論。大多數頻道需要登入，但`Public`頻道可以
  未登入的使用者也可以檢視。
- _幫助_ - 這會將遊戲中的[幫助系統](./Help-System.md) 與網站連結。全部
公開可用或可供您存取的基於資料庫的說明條目
  帳戶可以讀取。這是向人們提供幫助的好方法
  在遊戲之外閱讀。
- _線上播放_ - 這將在瀏覽器中開啟 [Webclient](./Webclient.md)。
- _管理員_ [Web 管理員](Web admin) 僅在您登入時才會顯示。
- _登入/登出_ - 允許您使用您使用的相同憑證進行身份驗證
在遊戲中。
- _註冊_ - 允許您註冊一個新帳戶。這與
首次登入遊戲時建立一個新帳戶）。

(modifying-the-default-website)=
## 修改預設網站

您可以從遊戲目錄修改和覆蓋網站的所有方面。您主要會在設定檔中執行此操作（`mygame/server/conf/settings.py` 和遊戲目錄的`web/folder`（如果您的遊戲資料夾是`mygame/`，則為`mygame/web/`）。

> 測試您的修改時，最好將 `DEBUG = True` 新增到
> 您的設定檔。這將直接為您提供資訊豐富的回溯
> 在您的瀏覽器中，而不是通用的 404 或 500 錯誤頁面。只要記住這一點
> DEBUG 模式會洩漏記憶體（用於保留偵錯資訊）並且使用*不*安全
> 對於製作遊戲來說！

如[Webserver](./Webserver.md)頁面所解釋的，取得網頁的過程是

1. Web 瀏覽器向伺服器傳送 HTTP 請求，帶有 URL
2. `urls.py` 使用正規表示式將 URL 與 _view_ （Python 函式或可呼叫類別）進行配對。
3. 正確的 Python 檢視已載入並執行。
4. 此檢視拉入一個 _template_，一個帶有佔位符標記的 HTML 文件，
並根據需要填寫這些內容（它也可以使用_form_以相同的方式自訂使用者輸入）。
   HTML 頁面也可能依序指向靜態資源（通常是 CSS，有時是影象等）。
5. 呈現的 HTML 頁面以 HTTP 回應返回瀏覽器。  如果
HTML頁面需要靜態資源，瀏覽器會要求
   在向使用者顯示之前分別獲取它們。

如果您檢視 [evennia/web/](github:evennia/web) 目錄，您會發現以下結構（省略與網站無關的內容）：

```
  evennia/web/
    ...
    static/
        website/
            css/
               (css style files)
            images/
               (images to show)

    templates/
        website/
          (html files)

    website/
      urls.py
      views/
        (python files related to website)

    urls.py

```

頂級 `web/urls.py` 檔案「包含」`web/website/urls.py` 檔案 - 這樣所有與網站相關的 url 處理都儲存在同一個位置。

這是與網站相關的 `mygame/web/` 資料夾的佈局：

```
  mygame/web/
    ...
    static/
      website/
        css/
        images/

    templates/
      website/

      website/
        urls.py
        views/

    urls.py

```

```{versionchanged} 1.0

  Game folders created with older versions of Evennia will lack most of this
  convenient `mygame/web/` layout. If you use a game dir from an older version,
  you should copy over the missing `evennia/game_template/web/` folders from
  there, as well as the main `urls.py` file.

```

如您所見，`mygame/web/` 資料夾是 `evennia/web/` 資料夾結構的副本，除了 `mygame` 資料夾大部分為空。

對於靜態檔案和模板檔案，Evennia 將_首先_查詢 `mygame/static` 和 `mygame/templates`，然後轉到 `evennia/web/` 中的預設位置。  所以要覆蓋這些資源，你只需要把一個同名的檔案放在`mygame/web/`下的正確位置（然後重新載入伺服器）。最簡單的方法通常是複製原始檔案並進行修改。

覆蓋檢視（Python 模組）還需要對 `website/urls.py` 檔案進行額外調整 - 您必須確保將 url 重新指向新版本，而不是使用原始版本。

(examples-of-commom-web-changes)=
## 常見 Web 變更的範例

```{important}

Django 是一個非常成熟的網頁設計框架。還有無窮無盡的
  可用於解釋如何使用 Django 的網路教學、課程和書籍。
  因此，這些範例僅作為您入門的入門指南。

```

(change-title-and-blurb)=
### 更改標題和簡介

網站的標題和簡介只需透過調整即可更改
`settings.SERVERNAME` 和 `settings.GAME_SLOGAN`。您的設定檔位於
`mygame/server/conf/settings.py`，只需設定/新增

    SERVERNAME = "My Awesome Game"
    GAME_SLOGAN = "The best game in the world"

(change-the-logo)=
### 更改標誌

Evennia 瞪大眼睛的蛇標誌可能不是您想要的遊戲。
此範本查詢檔案 `web/static/website/images/evennia_logo.png`。只是
將您自己的 PNG 徽標（64x64 畫素大）放在那裡，並命名為相同的名稱。


(change-front-page-html)=
### 更改首頁HTML

網站的首頁通常被稱為HTML中的“索引”
說法。

首頁模板位於`evennia/web/templates/website/index.html`。
只需將其複製到 `mygame/web/` 中的相應位置即可。在那裡修改它並
重新載入伺服器以檢視您的變更。

Django 模板有一些特殊的功能，將它們與普通的HTML 區分開來
檔案 - 它們包含特殊的模板語言，標記為 `{%... %}` 和
`{{... }}`。

需要了解的一些重要事項：

- `{% extends "base.html" %}` - 這相當於 Python `from othermodule import *` 語句，但用於模板。它允許給定模板使用匯入（擴充套件）模板中的所有內容，但也可以覆蓋它想要更改的任何內容。這樣可以輕鬆保持所有頁面看起來相同，並避免大量樣板。
- `{% block blockname %}...{% endblock %}` - 區塊是可繼承的、命名的程式碼片段，可以在一個位置進行修改，然後在其他地方使用。這與正常繼承有點相反，因為它通常以這樣的方式 `base.html` 定義一個空塊，比方說 `contents`：`{% block contents %}{% endblock %}` 但確保將其放在_正確的位置_，比如在主體中，側邊欄旁邊等。然後每個頁面執行 `{% extends "base.html %"}` 並建立自己的 `{% block contents} <actual content> {% endblock %}`。他們的 `contents` 區塊現在將覆蓋 `base.html` 中的空區塊並出現在檔案中的正確位置，而擴充範本不必指定其他所有內容
圍繞它！
- `{{... }}` 是“槽”，通常嵌入在 HTML tags 或內容中。它們引用 Python _view_ 提供的_context_（基本上就是字典）。上下文中的鍵透過點表示法進行訪問，因此，如果您向模板提供上下文 `{"stats": {"hp": 10, "mp": 5}}`，則可以將其訪問為 `{{ stats.hp }}`，以在該位置顯示 `10`，從而在該位置顯示 `10`。

這允許模板繼承（更容易使所有頁面看起來相同，而無需一遍又一遍地重寫相同的內容）

在[Django 範本語言檔案](https://docs.djangoproject.com/en/4.1/ref/templates/language/) 中可以找到更多資訊。

(change-webpage-colors-and-styling)=
### 變更網頁顏色和樣式

您可以調整整個網站的[CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)。如果您調查 `evennia/web/templates/website/base.html` 檔案，您會發現我們使用 [Bootstrap 4](https://getbootstrap.com/docs/4.6/getting-started/introduction/) 工具包。

許多結構性 HTML 功能實際上來自 bootstrap，因此您通常只需將 bootstrap CSS 類別新增到 HTML 檔案中的元素即可獲得各種效果，例如文字居中或類似效果。

網站的自訂 CSS 在 `evennia/web/static/website/css/website.css` 中找到，但我們仍在同一位置尋找（目前為空）`custom.css`。您可以覆蓋其中任何一個，但如果您只將內容新增至 `custom.css`，則恢復變更可能會更容易。

將要修改的CSS檔案複製到`mygame/web`中對應位置。修改它並重新載入伺服器以檢視您的更改。

您也可以應用靜態檔案而不重新載入，但在終端機中執行：

    evennia collectstatic --no-input

（重新載入伺服器時會自動運作）。

> 請注意，在看到應用程式的新 CSS 檔案之前，您可能需要重新整理您的
> 沒有快取的瀏覽器（例如​​，Firefox 中的 Ctrl-F5）。

例如，將 `custom.css` 新增/複製到 `mygame/web/static/website/css/` 並新增以下內容：


```css

.navbar {
  background-color: #7a3d54;
}

.footer {
  background-color: #7a3d54;
}

```

重新載入，您的網站現在有紅色主題！

> 提示：學習使用網頁瀏覽器的[開發者工具](https://torquemag.io/2020/06/browser-developer-tools-tutorial/)。
> 這些允許您調整CSS“實時”以找到您喜歡的外觀並將其複製到
> 僅當您想要使變更永久時才使用.css 檔案。


(change-front-page-functionality)=
### 變更首頁功能

邏輯盡在眼前。要查詢索引頁面檢視的位置，我們檢視 `evennia/web/website/urls.py`。在這裡我們找到以下行：

```python
# in evennia/web/website/urls.py

  ...
  # website front page
  path("", index.EvenniaIndexView.as_view(), name="index"),
  ...

```

第一個 `""` 是空 url - root - 如果你輸入 `localhost:4001/` 你會得到什麼
沒有額外的路徑。正如預期的那樣，這將導致索引頁。透過檢視進口
我們發現該檢視位於 `evennia/web/website/views/index.py` 中。

將此檔案複製到`mygame/web`中對應位置。然後調整 `mygame/web/website/urls.py` 檔案以指向新檔案：

```python
# in mygame/web/website/urls.py

# ...

from web.website.views import index

urlpatterns = [
    path("", index.EvenniaIndexView.as_view(), name="index")

]
# ...

```

所以我們只需從新位置匯入 `index` 並指向它。重新載入後，首頁現在將重定向以使用您的副本而不是原始頁面。

首頁檢視是一個類別`EvenniaIndexView`。這是一個[Django 基於類別的檢視](https://docs.djangoproject.com/en/4.1/topics/class-based-views/)。在基於類別的檢視中發生的事情比函式中發生的事情不太明顯（因為類別以方法的形式實現了許多功能），但它很強大並且更容易擴充套件/修改。

類別屬性 `template_name` 設定 `templates/` 資料夾下使用的範本的位置。所以 `website/index.html` 指向 `web/templates/website/index.html` （如我們上面已經探討過的。

`get_context_data` 是為範本提供上下文的便捷方法。在索引頁的情況下，我們需要遊戲統計資料（最近玩家的數量等）。然後，它們可在模板中的 `{{... }}` 槽中使用，如上一節所述。

(change-other-website-pages)=
### 更改其他網站頁面

其他子頁面以相同的方式處理 - 將範本或靜態資源複製到正確的位置，或複製檢視並將 `website/urls.py` 重新指向您的副本。只要記住重新載入即可。

(adding-a-new-web-page)=
## 新增網頁

(using-flat-pages)=
### 使用平面頁面

新增網頁的最簡單方法是使用 [Web 管理](./Web-Admin.md) 中提供的 `Flat Pages` 應用程式。該頁面將以與網站其他部分相同的樣式顯示。

為了使 `Flat pages` 模組正常運作，您必須先設定要使用的_站點_（或網域）。您只需要這樣做一次。

- 前往 Web 管理並選擇 `Sites`。如果您的遊戲位於 `mygreatgame.com`，則這就是您需要新增的網域。對於本地實驗，請新增網域 `localhost:4001`。記下網域的`id`（點選新網域時檢視url，如果是`http://localhost:4001/admin/sites/site/2/change/`，那麼id就是`2`）。
- 現在將行 `SITE_ID = <id>` 新增到您的設定檔中。

接下來您可以輕鬆建立新頁面。

- 前往 `Flat Pages` 網路管理員並選擇新增新的平面頁面。
- 設定網址。如果您希望頁面顯示為e.g。 `localhost:4001/test/`，那麼
此處新增`/test/`。您需要新增前導斜線和尾隨斜線。
- 將 `Title` 設定為頁面名稱。
- `Content` 是頁面正文的 HTML 內容。瘋狂吧！
- 最後選擇你之前製作的`Site`，並儲存。
- （在進階部分，您可以設定為必須登入才能檢視頁面等）。

現在您可以轉到`localhost:4001/test/`並檢視您的新頁面！

(add-custom-new-page)=
### 新增自訂新頁面

`Flat Pages` 頁面不允許（太多）動態內容和自訂。為此，您需要自行新增所需的元件。

讓我們看看如何從頭開始製作 `/test/` 頁面。

- 在 `mygame/web/templates/website/` 下新增新的 `test.html` 檔案。最簡單的方法是基於現有檔案。如果您想獲得與網站其他部分相同的樣式，請確保`{% extend base.html %}`。
- 在 `mygame/web/website/views/` 下新增檢視 `testview.py`（不要將其命名為 `test.py` 或
Django/Evennia 會認為它包含單元測試）。在那裡新增一個檢視來處理您的頁面。這是一個最小的開始檢視（閱讀更多內容[在 Django 檔案中](https://docs.djangoproject.com/en/4.1/topics/class-based-views/)）：

    ```python
    # mygame/web/website/views/testview.py

    from django.views.generic import TemplateView

    class MyTestView(TemplateView):
        template_name = "website/test.html"


    ```

- 最後，從`mygame/web/website/urls.py`來說你的看法：

    ```python
    # in mygame/web/website/urls.py

    # ...
    from web.website.views import testview

    urlpatterns = [
        # ...
        # we can skip the initial / here
        path("test/", testview.MyTestView.as_view())
    ]

    ```
- 重新載入伺服器，您的新頁面就可用了。現在您可以繼續新增
透過您的檢視和模板提供各種高階動態內容！


(user-forms)=
## 使用者表格

到目前為止建立的所有頁面都是向使用者呈現資訊。
使用者也可以透過_表單_在頁面上_輸入_資料。安
範例將是您填寫以建立一個欄位和滑桿的頁面
字元，底部有一個大的“提交”按鈕。

首先，這必須以 HTML 表示。 `<form>... </form>` 是一個
您需要新增到模板中的標準 HTML 元素。它還有一些其他的
要求，例如 `<input>` 以及通常的 Javascript 元件（但是
通常 Django 會幫助解決這個問題）。如果您不熟悉 HTML 的形成方式
工作，[在這裡閱讀有關它們](https://docs.djangoproject.com/en/4.1/topics/forms/#html-forms)。

其基本要點是，當您按一下「提交」表單時，會出現 POST HTML
請求將被傳送到包含使用者輸入的資料的伺服器。這是
現在由伺服器來確保資料有意義（驗證），然後
以某種方式處理輸入（例如建立一個新角色）。

在後端，我們需要指定驗證和處理的邏輯
表單資料。這是由 `Form` [Django 類別](https://docs.djangoproject.com/en/4.1/topics/forms/#forms-in-django) 完成的。
這指定了_fields_本身來定義如何驗證該資料。

然後透過新增 `form_class = MyFormClass` 將表單連結到檢視類
檢視（`template_name` 旁邊）。

`evennia/web/website/forms.py`中有幾個範例表單。也是不錯的
建議閱讀 Django 網站上的 [Building a form in Django](https://docs.djangoproject.com/en/4.1/topics/forms/#building-a-form-in-django) - 它涵蓋了您需要的所有內容。
