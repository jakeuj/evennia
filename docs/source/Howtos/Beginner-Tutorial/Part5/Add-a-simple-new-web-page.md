(add-a-simple-new-web-page)=
# 新增一個簡單的新網頁
Evennia 利用 [Django](https://docs.djangoproject.com)，這是一個 Web 開發框架。
龐大的專業網站是用 Django 製作的，並且有大量的文件（和書籍）。
我們鼓勵您至少檢視 Django 基礎教學。這裡我們就簡單介紹一下
介紹事物如何結合在一起，幫助您入門。

我們假設您已安裝並設定 Evennia 來執行。 webserver 及網站附帶
預設 Evennia 開箱即用安裝。您可以透過網頁瀏覽器檢視預設網站
到`http://localhost:4001`。您將看到一個通用的歡迎頁面，其中包含一些遊戲統計資料和連結
到 Evennia Web 使用者端。

在本教學中，我們將新增一個頁面，您可以在 `http://localhost:4001/story` 造訪該頁面。

(create-the-view)=
### 建立檢視

django「檢視」是一個普通的Python函式，django呼叫它來呈現您將看到的HTML頁面
在網頁瀏覽器中。 Django 可以透過使用檢視功能對頁面執行各種很酷的操作 –喜歡
新增動態內容或動態變更頁面 –但是，在這裡，我們只會讓它吐
返回原始HTML。

開啟 `mygame/web/website` 資料夾並在其中建立一個名為 `story.py` 的新模組檔案。 （你也可以
如果您想保持整潔，請將其放在自己的資料夾中，但是如果您這樣做，請不要忘記新增一個空的
`__init__.py` 檔案位於新資料夾中。加 `__init__.py` 檔案告訴 Python 模組可以
從新資料夾匯入。對於本教學，以下是新 `story.py` 的範例內容
模組應如下所示：

```python
# in mygame/web/website/story.py

from django.shortcuts import render

def storypage(request):
    return render(request, "story.html")
```

上面的檢視利用了 Django 提供的捷徑：_render_。渲染快捷方式
給出請求中的模板資訊。例如，它可能提供遊戲名稱，然後
渲染它。

(the-html-page)=
### HTML頁面

接下來，我們需要找到Evennia（和Django）來找出HTML檔案的位置，這些檔案被引用
用 Django 的話說就是「模板」。您可以在設定中指定此類位置（請參閱
`default_settings.py` 中的 `TEMPLATES` 變數以獲取更多資訊）但是，這裡我們將使用現有的變數。

導航至 `mygame/web/templates/website/` 並在其中建立一個名為 `story.html` 的新檔案。這個
不是 HTML 教學，因此該檔案的內容很簡單：

```html
{% extends "base.html" %}
{% block content %}
<div class="row">
  <div class="col">
    <h1>A story about a tree</h1>
    <p>
        This is a story about a tree, a classic tale ...
    </p>
  </div>
</div>
{% endblock %}
```

如上所示，Django 將允許我們輕鬆擴充套件我們的基本樣式，因為我們使用了
_渲染_快捷方式。如果您不想利用 Evennia 的基本樣式，您可以
而是做這樣的事情：

```html
<html>
  <body>
    <h1>A story about a tree</h1>
    <p>
    This is a story about a tree, a classic tale ...
  </body>
</html>
```

(the-url)=
### URL

當你在瀏覽器中輸入位址`http://localhost:4001/story`時，Django會解析這個位址
連線埠後面的存根 –這裡，`/story`－找出您想要顯示的頁面。如何
Django 知道 HTML 檔案 `/story` 應該連結到什麼嗎？你告訴 Django 什麼位址存根
模式對應於檔案 `mygame/web/website/urls.py` 中的哪些檔案。現在在編輯器中開啟它。

Django 在此檔案中尋找變數 `urlpatterns`。您將需要新增的 `story` 模式
以及 `urlpatterns` 清單的對應路徑 -然後，依序與預設值合併
`urlpatterns`。它看起來是這樣的：

```python
"""
This reroutes from an URL to a python view-function/class.
The main web/urls.py includes these routes for all urls (the root of the url)
so it can reroute to all website pages.
"""
from django.urls import path

from web.website import story

from evennia.web.website.urls import urlpatterns as evennia_website_urlpatterns

# add patterns here
urlpatterns = [
    # path("url-pattern", imported_python_view),
    path(r"story", story.storypage, name="Story"),
]

# read by Django
urlpatterns = urlpatterns + evennia_website_urlpatterns
```

上面的程式碼從我們之前建立的位置匯入我們的 `story.py` Python 檢視模組 –在
`mygame/web/website/`－然後加入對應的`path`例項。第一個引數
`path` 是我們要找的 URL (`"story"`) 作為正規表示式的模式，並且
然後是我們要呼叫的 `story.py` 的檢視函式。

應該是這樣。重新載入Evennia—— `evennia reload`——現在您應該能夠導航
將您的瀏覽器轉到 `http://localhost:4001/story` 位置並檢視您的新故事頁面
由Python渲染！
