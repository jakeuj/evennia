(web-character-view-tutorial)=
# 網頁角色檢視教學


**在學習本教學之前，您可能需要閱讀[更改網頁教學](./Web-Changing-Webpage.md) 中的介紹。 **

在本教學中，我們將建立一個顯示遊戲角色統計資料的網頁。為此，以及我們想要針對我們的遊戲製作的所有其他頁面，我們需要建立我們自己的 Django「應用程式」。我們將呼叫我們的應用程式`character`，因為它將處理字元資訊。從你的遊戲目錄執行

    evennia startapp character

這將在 `mygame` 內建立一個名為 `character` 的新目錄。為了保留
東西整理好了，讓我們將其移動到 `web/` 子目錄中。

    mv character web  (linux/mac)
    move character web  (windows)

我們將其放在 `web/` 中以保持整潔，但您可以將其放在任何位置
喜歡。它包含 Django 應用程式所需的所有基本檔案。

請注意，我們不會編輯這個新目錄中的所有檔案，許多產生的檔案超出了本教學的範圍。

為了讓 Django 找到我們的新 Web 應用程式，我們需要將其新增到 `INSTALLED_APPS` 設定中。 Evennia 的預設安裝應用程式已設定，因此在 `server/conf/settings.py` 中，我們將擴充套件它們：

```python
INSTALLED_APPS += ('web.character',)
```

> 注意：結尾逗號很重要。它確保 Python 將加法解釋為元組而不是字串。

我們需要做的第一件事是建立一個*檢視*和一個指向它的*URL模式*。一個檢視是一個
產生訪客想要檢視的網頁的函式，而 URL 模式讓 Django 知道什麼 URL 應該觸發檢視。正如我們將看到的，該模式還可以提供其自身的一些資訊。

這是我們的 `character/urls.py` 檔案（**注意**：如果是空白檔案，您可能需要建立此檔案
不是為您產生的）：

```python
# URL patterns for the character app

from django.urls import path
from web.character.views import sheet

urlpatterns = [
    path("sheet/<int:object_id>", sheet, name="sheet")
]
```

該檔案包含應用程式的所有 URL 模式。 `url` 函式在
`urlpatterns` 列表給出了三個引數。第一個引數是一個模式字串，用於
確定哪些 URLs 是有效的。模式被指定為*正規表示式*。正規表示式用於匹配字串，並以特殊的、非常緊湊的語法編寫。正規表示式的詳細描述超出了本教學的範圍，但您可以[此處](https://docs.python.org/2/howto/regex.html)瞭解有關它們的更多資訊。現在，只需接受此正規表示式要求訪客的 URL 看起來像這樣：

````
sheet/123/
````

也就是說，`sheet/` 後面跟著一個數字，而不是其他一些可能的 URL 模式。我們將把這個數字解釋為物件ID。由於正規表示式的製定方式，模式識別器將數字儲存在名為 `object_id` 的變數中。這將被傳遞到檢視（見下文）。我們在第二個引數中新增匯入的檢視函式（`sheet`）。我們也新增 `name` 關鍵字來識別 URL 模式本身。您應該始終命名您的 URL 模式，這使得可以使用 `{% url %}` tag 在 html 模板中輕鬆引用它們（但我們不會在本教學中對此進行更多介紹）。

> 安全說明：通常，使用者無法在遊戲中檢視物件 ID（僅限超級使用者）。像這樣向公眾公開遊戲的物件 ID 使得惡意破壞者能夠執行所謂的[帳號列舉攻擊](http://www.sans.edu/research/security-laboratory/article/attacks-browsing)，以劫持您的超級使用者帳號。考慮一下：在每個 Evennia 安裝中，我們*總是*期望存在兩個物件，並且具有相同的物件 ID - Limbo (#2) 和您在開始時建立的超級使用者 (#1)。因此，惡意破壞者只需導航到 `sheet/1` 即可獲得劫持管理員帳戶（管理員的使用者名稱）所需的 50% 資訊！

接下來我們建立`views.py`，`urls.py` 引用的檢視檔案。

```python
# Views for our character app

from django.http import Http404
from django.shortcuts import render
from django.conf import settings

from evennia.utils.search import object_search
from evennia.utils.utils import inherits_from

def sheet(request, object_id):
    object_id = '#' + object_id
    try:
        character = object_search(object_id)[0]
    except IndexError:
        raise Http404("I couldn't find a character with that ID.")
    if not inherits_from(character, settings.BASE_CHARACTER_TYPECLASS):
        raise Http404("I couldn't find a character with that ID. "
                      "Found something else instead.")
    return render(request, 'character/sheet.html', {'character': character})
```

如前所述，`urls.py` 中的 URL 模式解析器解析 URL 並將 `object_id` 傳遞給我們的檢視函式 `sheet`。我們使用該編號在資料庫中搜尋該物件。我們還確保這樣的物件存在並且它實際上是一個角色。檢視函式也被傳遞了一個 `request` 物件。這為我們提供了有關請求的資訊，例如登入使用者是否檢視了該請求 - 我們不會在此處使用該資訊，但最好記住。

在最後一行，我們呼叫 `render` 函式。除了 `request` 物件之外，`render`
函式採用一個 html 模板的路徑和一個字典，其中包含要傳遞到所述模板的額外資料。作為額外資料，我們傳遞剛剛找到的 Character 物件。在模板中，它將作為變數“字元”使用。

html 模板在您的 `character` 應用程式資料夾下建立為 `templates/character/sheet.html`。您可能必須手動建立 `template` 及其子資料夾 `character`。這是要建立的模板：

````html
{% extends "base.html" %}
{% block content %}

    <h1>{{ character.name }}</h1>

    <p>{{ character.db.desc }}</p>

    <h2>Stats</h2>
    <table>
      <thead>
        <tr>
          <th>Stat</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Strength</td>
          <td>{{ character.db.str }}</td>
        </tr>
        <tr>
          <td>Intelligence</td>
          <td>{{ character.db.int }}</td>
        </tr>
        <tr>
          <td>Speed</td>
          <td>{{ character.db.spd }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Skills</h2>
    <ul>
      {% for skill in character.db.skills %}
        <li>{{ skill }}</li>
      {% empty %}
        <li>This character has no skills yet.</li>
      {% endfor %}
    </ul>

    {% if character.db.approved %}
      <p class="success">This character has been approved!</p>
    {% else %}
      <p class="warning">This character has not yet been approved!</p>
    {% endif %}
{% endblock %}
````

在 Django 模板中，`{%... %}` 表示 Django 理解的特殊模板內「函式」。 `{{... }}` 塊用作“槽”。它們將被替換為區塊內程式碼返回的任何值。

第一行 `{% extends "base.html" %}` 告訴 Django 該模板擴充套件了 Evennia 正在使用的基本模板。基本模板由主題提供。 Evennia 附帶開源第三方主題 `prosimii`。您可以在以下位置找到它及其 `base.html`
`evennia/web/templates/prosimii`。與其他模板一樣，這些模板可以被覆蓋。

下一行是`{% block content %}`。 `base.html` 檔案有 `block`s，它們是佔位符
模板可以擴充。我們使用的主區塊被命名為 `content`。

我們可以在模板中的任何位置訪問 `character` 變數，因為我們在 `view.py` 末尾的 `render` 呼叫中傳遞了它。這意味著我們還可以存取角色的 `db` 屬性，就像在普通的 Python 程式碼中一樣。您無法在模板中使用引數呼叫函式——事實上，如果您需要執行任何複雜的邏輯，您應該在 `view.py` 中執行，並將結果作為更多變數傳遞給模板。但您在顯示資料的方式上仍然具有很大的靈活性。

我們也可以在這裡做一些邏輯。我們使用 `{% for %}... {% endfor %}` 和 `{% if %}... {% else %}... {% endif %}` 結構來根據使用者擁有的技能數量或使用者是否獲得批准（假設您的遊戲有批准系統）來更改模板的呈現方式。

我們需要編輯的最後一個檔案是主URLs 檔案。這是為了將新 `character` 應用程式中的 URLs 與 Evennia 現有頁面中的 URLs 順利整合所必需的。找到檔案 `web/website/urls.py` 並更新其 `patterns` 列表，如下所示：

```python
# web/website/urls.py

urlpatterns = [
    # ...
    path("character/", include('web.character.urls'))
   ]
```

現在使用 `evennia reload` 重新載入伺服器並在瀏覽器中造訪該頁面。如果你還沒有
更改了預設值，您應該能夠在以下位置找到字元 `#1` 的工作表
`http://localhost:4001/character/sheet/1/`

嘗試更新遊戲中的統計資料並重新整理瀏覽器中的頁面。結果應該立即顯示。

作為可選的最後一步，您還可以將角色 typeclass 變更為具有名為「get_absolute_url」的方法。
```python
# typeclasses/characters.py

    # inside Character
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('character:sheet', kwargs={'object_id':self.id})
```
這樣做會在 Django 管理物件的右上角顯示一個「現場檢視」按鈕
連結到新角色表的變更頁面，並允許您在具有給定物件的任何範本中使用 `{{ object.get_absolute_url }}` 來取得角色頁面的連結。

*現在您已經使用 Django 製作了基本頁面和應用程式，您可能需要閱讀完整的 Django 教學以更好地瞭解它的功能。 [你可以找到Django的教學
這裡](https://docs.djangoproject.com/en/4.1/intro/tutorial01/).*
