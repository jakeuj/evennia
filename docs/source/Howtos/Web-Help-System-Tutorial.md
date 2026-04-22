(web-help-system-tutorial)=
# 網路幫助系統教學


**在學習本教學之前，您可能需要閱讀 [更改網頁教學](./Web-Changing-Webpage.md) 中的介紹。 ** 閱讀 [Django 教學](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) 的前三個部分也可能有所幫助。

本教學將向您展示如何透過網站存取幫助系統。  幫助指令和常規幫助條目都將可見，具體取決於登入使用者或匿名角色。

本教學將向您展示如何：

- 建立一個新頁面以新增到您的網站。
- 利用基本檢視和基本模板。
- 造訪您網站上的幫助系統。
- 確定此頁面的檢視者是否已登入，如果已登入，則使用什麼帳戶登入。

(creating-our-app)=
## 建立我們的應用程式

第一步是建立新的 Django *app*。  Django 中的應用程式可以包含頁面和機制：您的網站可能包含不同的應用程式。  實際上，Evennia 提供的開箱即用的網站已經有三個應用程式：一個「webclient」應用程式，用於處理整個 webclient，一個「網站」應用程式用於包含基本頁面，以及 Django 提供的第三個應用程式，用於建立一個簡單的管理介面。  因此，我們將並行建立另一個應用程式，為其指定一個清晰的名稱來代表我們的幫助系統。

從您的遊戲目錄中，使用以下指令：

    cd web
    evennia startapp help_system

這將在您的 `mygame/` 資料夾中建立一個新資料夾 `help_system`。為了保留東西
整潔，讓我們將其移動到 `web/` 資料夾：

    mv help_system web  (linux)
    move help_system web  (windows)

> 注意：呼叫應用程式「help」會更明確，但 Django 已使用該名稱。

我們將新應用程式放在 `web/` 下，以便將所有與網路相關的內容放在一起，但您可以按照自己的喜好進行組織。結構如下所示：

    mygame/
        ...
        web/
            help_system/
            ...

“web/help_system”目錄包含Django所建立的檔案。  我們將使用其中的一些，但如果您想了解更多有關它們的資訊，您應該閱讀[Django 教學](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)。

還有最後一件事要做：您的資料夾已新增，但 Django 不知道它，它不知道這是一個新應用程式。  我們需要告訴它，我們透過編輯一個簡單的設定來做到這一點。  開啟“server/conf/settings.py”檔案並新增或編輯以下行：

```python
# Web configuration
INSTALLED_APPS += (
        "web.help_system",
)
```

如果需要，您可以啟動 Evennia，然後造訪您的網站，可能位於 [http://localhost:4001](http://localhost:4001) 。不過，您不會看到任何不同的東西：我們新增了應用程式，但它相當空。

(our-new-page)=
## 我們的新頁面

此時，我們的新 *app* 大部分包含您可以探索的空檔。  為了為我們的幫助系統建立頁面，我們需要新增：

- 一個*檢視*，處理我們頁面的邏輯。
- 用於顯示新頁面的*模板*。
- 一個新的 *URL* 指向我們的頁面。

> 我們可以透過只建立一個檢視和一個新的 URL 來擺脫困境，但這不是推薦的使用您的網站的方式。  基於模板進行建置要方便得多。

(create-a-view)=
### 建立檢視

Django 中的 *view* 是一個簡單的 Python 函式，放​​置在應用程式的 `views.py` 檔案中。  它將
處理當使用者透過輸入 *URL* 請求此資訊時觸發的行為（*views* 和 *URLs* 之間的連線將在稍後討論）。

那麼讓我們建立我們的檢視。  您可以開啟 `web/help_system/views.py` 檔案並貼上以下行：

```python
from django.shortcuts import render

def index(request):
    """The 'index' view."""
    return render(request, "help_system/index.html")
```

我們的檢視處理所有程式碼邏輯。  這次，沒有太多內容：當呼叫此函式時，它將呈現我們現在將建立的模板。  但這就是我們之後將完成大部分工作的地方。

(create-a-template)=
### 建立模板

呼叫我們的*檢視*的`render`函式詢問*模板*`help_system/index.html`。  我們應用程式的「模板」儲存在應用程式目錄的「templates」子目錄中。  Django 可能已經建立了「templates」資料夾。  如果沒有，請自行建立。  在其中建立另一個資料夾“help_system”，並在此資料夾內建立一個名為“index.html”的檔案。  哇，這是一些層次結構。  您的目錄結構（從 `web` 開始）應如下所示：

    web/
        help_system/
            ...
            templates/
                help_system/
                    index.html

開啟「index.html」檔案並貼上以下行：

```
{% extends "base.html" %}
{% block titleblock %}Help index{% endblock %}
{% block content %}
<h2>Help index</h2>
{% endblock %}
```

以下是此模板功能的逐行解釋：

1. 它載入“base.html”*模板*。  這描述了所有頁面的基本結構，頂部有一個選單和頁尾，也許還包括其他訊息，例如影象和每個頁面上顯示的內容。  您可以建立不繼承自「base.html」的模板，但您應該有這樣做的充分理由。
2. 「base.html」*範本*定義了頁面的所有結構。  剩下的就是覆蓋我們頁面的某些部分。  這些部分稱為*塊*。  在第 2 行，我們覆蓋名為「blocktitle」的區塊，其中包含頁面的標題。
3. 同樣的事情，我們覆蓋名為「內容」的*區塊*，其中包含網頁的主要內容。  該區塊較大，因此我們將其定義在幾行中。
4. 這是顯示 2 級標題的完全正常的 HTML 程式碼。
5. 最後我們關閉名為「內容」的*區塊*。

(create-a-new-url)=
### 創造一個新的URL

新增頁面的最後一步：我們需要新增一個 *URL* 指向它...否則使用者將無法存取它。  我們的URLs的應用程式儲存在應用程式的目錄`urls.py`檔案中。

開啟 `web/help_system/urls.py` 檔案（您可能必須建立它）並使其如下所示：

```python
# URL patterns for the help_system app

from django.urls import path
from .views import index

urlpatterns = [
    path('', index)
]
```

`urlpatterns` 變數是 Django/Evennia 尋找的變數，以找出如何引導使用者在瀏覽器中輸入 URL 到您編寫的檢視程式碼。

最後，我們需要將其繫結到您遊戲的主名稱空間。  編輯檔案`mygame/web/urls.py`。  在其中您將再次找到 `urlpatterns` 清單。將新的 `path` 新增到清單末尾。

```python
# mygame/web/urls.py
# [...]

# add patterns
urlpatterns = [
    # website
    path("", include("web.website.urls")),
    # webclient
    path("webclient/", include("web.webclient.urls")),
    # web admin
    path("admin/", include("web.admin.urls")),

    # my help system
    path('help/', include('web.help_system.urls'))   # <--- NEW
]

# [...]
```

當使用者在您的網站上請求特定的 *URL* 時，Django 將：

1. 讀取“web/urls.py”中定義的自訂模式清單。  這裡有一個模式，它向 Django 描述所有以 'help/' 開頭的 URLs 都應該傳送到 'help_system' 應用程式。  “幫助/”部分被刪除。
2. 然後Django將檢查“web.help_system/urls.py”檔案。  它只包含一個 URL，它是空的 (`^$`)。

換句話說，如果URL是'/help/'，那麼Django就會執行我們定義的檢視。

(lets-see-it-work)=
### 讓我們看看它的工作原理

現在您可以重新載入或啟動Evennia。  在瀏覽器中開啟一個選項卡並轉到 [http://localhost:4001/help/](http://localhost:4001/help/) 。  如果一切順利，您應該會看到新頁面...該頁面不為空，因為 Evennia 使用我們的“base.html”*模板*。  在我們頁面的內容中，只有一個標題為「幫助索引」。  請注意，我們頁面的標題是“mygame - 幫助索引”（“mygame”被替換為您的遊戲名稱）。

從現在開始，繼續前進和新增功能將變得更加容易。

(a-brief-reminder)=
### 簡短提醒

我們將嘗試以下幾件事：

- 獲得線上存取的指令和幫助條目的幫助。
- 根據使用者是否登入，有各種指令和幫助條目。

就頁面而言，我們將有：

- 其一用於顯示幫助主題清單。
- 用於顯示幫助主題的內容。

第一個將連結到第二個。

> 我們應該創造兩個URLs嗎？

答案是……也許吧。  這取決於你想做什麼。  我們可以透過「/help/」URL 存取幫助索引。  我們可以透過「/help/desc」存取幫助條目的詳細資訊（請參閱「desc」指令的詳細資訊）。  問題是我們的指令或幫助主題可能包含 URLs 中不存在的特殊字元。  解決這個問題有不同的方法。  我決定在這裡使用 *GET 變數*，這將建立 URLs ，如下所示：

    /help?name=desc

如果您使用此係統，則不必新增新的 URL：GET 和 POST 變數可以透過我們的請求訪問，我們很快就會看到。

(handling-logged-in-users)=
## 處理登入使用者

我們的要求之一是擁有適合我們帳戶的幫助系統。  如果具有管理員存取許可權的帳戶登入，頁面應該會顯示許多普通使用者無法存取的指令。甚至可能還有一些額外的幫助主題。

幸運的是，在我們的檢視中取得登入帳戶相當容易（請記住，我們將在那裡完成大部分編碼）。  傳遞給我們的函式的 *request* 物件包含 `user` attribute。這個 attribute 將永遠存在：例如，我們無法測試它是否是 `None`。  但是，當請求來自未登入的使用者時，`user` attribute 將包含匿名 Django 使用者。  然後我們可以使用 `is_anonymous` 方法來檢視使用者是否登入。  最後Evennia贈送的，如果使用者登入了，`request.user`包含了一個帳戶物件的引用，這對於我們耦合遊戲和線上系統有很大的幫助。

所以我們最終可能會得到這樣的結果：

```python
def index(request):
    """The 'index' view."""
    user = request.user
    if not user.is_anonymous() and user.character:
        character = user.character
```

> 注意：當您的 MULTISESSION_MODE 設定為 0 或 1 時，此程式碼有效。當它位於上面時，您將看到類似以下內容的內容：

```python
def index(request):
    """The 'index' view."""
    user = request.user
    if not user.is_anonymous() and user.characters:
        character = user.characters[0]
```

在第二種情況下，它將選擇帳戶的第一個字元。

但是如果使用者沒有登入怎麼辦？  同樣，我們有不同的解決方案。  最簡單的方法之一是建立一個角色，該角色將充當幫助系統的預設角色。  您可以透過遊戲建立它：連線到它並輸入：

    @charcreate anonymous

系統應該回答：

        Created new character anonymous. Use @ic anonymous to enter the game as this character.

所以在我們看來，我們可以有這樣的東西：

```python
from typeclasses.characters import Character

def index(request):
    """The 'index' view."""
    user = request.user
    if not user.is_anonymous() and user.character:
        character = user.character
    else:
        character = Character.objects.get(db_key="anonymous")
```

這次，無論如何我們都有一個有效的字元：如果您在高於 1 的多會話模式下執行，請記住調整此程式碼。

(the-full-system)=
## 完整的系統

我們要做的是瀏覽所有指令和幫助條目，並列出該角色（無論是我們的「匿名」角色，還是我們的登入角色）可以看到的所有指令。

程式碼較長，但它呈現了我們認為的整個概念。  編輯“web/help_system/views.py”檔案並貼上到其中：

```python
from django.http import Http404
from django.shortcuts import render
from evennia.help.models import HelpEntry

from typeclasses.characters import Character

def index(request):
    """The 'index' view."""
    user = request.user
    if not user.is_anonymous() and user.character:
        character = user.character
    else:
        character = Character.objects.get(db_key="anonymous")

    # Get the categories and topics accessible to this character
    categories, topics = _get_topics(character)

    # If we have the 'name' in our GET variable
    topic = request.GET.get("name")
    if topic:
        if topic not in topics:
            raise Http404("This help topic doesn't exist.")

        topic = topics[topic]
        context = {
                "character": character,
                "topic": topic,
        }
        return render(request, "help_system/detail.html", context)
    else:
        context = {
                "character": character,
                "categories": categories,
        }
        return render(request, "help_system/index.html", context)

def _get_topics(character):
    """Return the categories and topics for this character."""
    cmdset = character.cmdset.all()[0]
    commands = cmdset.commands
    entries = [entry for entry in HelpEntry.objects.all()]
    categories = {}
    topics = {}

    # Browse commands
    for command in commands:
        if not command.auto_help or not command.access(character):
            continue

        # Create the template for a command
        template = {
                "name": command.key,
                "category": command.help_category,
                "content": command.get_help(character, cmdset),
        }

        category = command.help_category
        if category not in categories:
            categories[category] = []
        categories[category].append(template)
        topics[command.key] = template

    # Browse through the help entries
    for entry in entries:
        if not entry.access(character, 'view', default=True):
            continue

        # Create the template for an entry
        template = {
                "name": entry.key,
                "category": entry.help_category,
                "content": entry.entrytext,
        }

        category = entry.help_category
        if category not in categories:
            categories[category] = []
        categories[category].append(template)
        topics[entry.key] = template

    # Sort categories
    for entries in categories.values():
        entries.sort(key=lambda c: c["name"])

    categories = list(sorted(categories.items()))
    return categories, topics
```

這裡有點複雜，但總而言之，它可以分成小塊：

- `index` 函式是我們的觀點：
    - 首先取得我們在上一節看到的角色。
    - 它會取得該角色可以存取的幫助主題（指令和幫助條目）。  這是處理該部分的另一個函式。
    - 如果我們的 URL 中有一個 *GET 變數*「name」（如「/help?name=drop」），它將檢索它。  如果它不是有效的主題名稱，則傳回 *404*。  否則，它會呈現名為“detail.html”的模板，以顯示我們主題的詳細資訊。
    - 如果沒有*GET變數*“名稱”，則渲染“index.html”，以顯示主題清單。
- `_get_topics` 是私有函式。  它的唯一任務是檢索角色可以執行的指令，以及該角色可以看到的幫助條目。  此程式碼比 Django 特定的程式碼更特定於 Evennia，本教學中不會對其進行詳細說明。  請注意，所有幫助主題都儲存在字典中。  這是為了簡化我們在模板中顯示它們時的工作。

請注意，在這兩種情況下，當我們要求渲染 *template* 時，我們都會向 `render` 傳遞第三個引數，它是模板中使用的變數字典。  我們可以透過這種方式傳遞變數，並且我們將在模板中使用它們。

(the-index-template)=
### 索引模板

讓我們看看完整的“索引”*模板*。  您可以開啟“web/help_system/templates/help_sstem/index.html”檔案並將以下內容貼到其中：

```
{% extends "base.html" %}
{% block titleblock %}Help index{% endblock %}
{% block content %}
<h2>Help index</h2>
{% if categories %}
    {% for category, topics in categories %}
        <h2>{{ category|capfirst }}</h2>
        <table>
        <tr>
        {% for topic in topics %}
            {% if forloop.counter|divisibleby:"5" %}
                </tr>
                <tr>
            {% endif %}
            <td><a href="{% url 'help_system:index' %}?name={{ topic.name|urlencode }}">
            {{ topic.name }}</td>
        {% endfor %}
        </tr>
        </table>
    {% endfor %}
{% endif %}
{% endblock %}
```

這個模板肯定更詳細。  它的作用是：

1. 瀏覽所有類別。
2. 對於所有類別，顯示帶有類別名稱的 2 級標題。
3. 類別中的所有主題（請記住，它們可以是指令或幫助條目）都顯示在表格中。  更棘手的部分可能是，當迴圈次數超過 5 時，它將建立一個新行。  該表每行最多有 5 列。
4. 對於表中的每個單元格，我們建立一個重定向到詳細資訊頁面的連結（見下文）。  URL 看起來像「help?name=say」。  我們使用 `urlencode` 來確保特殊字元被正確轉義。

(the-detail-template)=
### 詳細模板

現在是時候顯示主題的詳細資訊（指令或幫助條目）。  您可以建立檔案“web/help_system/templates/help_system/detail.html”。  您可以將以下程式碼貼到其中：

```
{% extends "base.html" %}
{% block titleblock %}Help for {{ topic.name }}{% endblock %}
{% block content %}
<h2>{{ topic.name|capfirst }} help topic</h2>
<p>Category: {{ topic.category|capfirst }}</p>
{{ topic.content|linebreaks }}
{% endblock %}
```

這個模板更容易閱讀。  有些*過濾器*您可能不知道，但它們只是用來格式化的。

(put-it-all-together)=
### 把它們放在一起

請記住重新載入或啟動Evennia，然後轉到[http://localhost:4001/help](http://localhost:4001/help/)。  您應該看到所有角色都可以存取的指令和主題清單。  嘗試登入（點選網站選單中的「登入」連結）並再次前往同一頁面。  現在您應該看到更詳細的指令和幫助條目清單。  點選其中一項即可檢視其詳細資訊。

(to-improve-this-feature)=
## 為了改進這個功能

像往常一樣，這裡的教學可以幫助您輕鬆地自行新增新功能和程式碼。以下是改進這個小功能的一些想法：

- 詳細資訊範本底部用於返回索引的連結可能很有用。
- 主選單中的連結到此頁面會很棒...暫時您必須輸入URL，使用者不會猜到它在那裡。
- 此時尚未處理顏色，這並不奇怪。  不過你可以新增它。
- 將幫助條目相互連結並不簡單，但這會很棒。  例如，如果您看到有關如何使用多個指令的幫助條目，如果這些指令本身是顯示其詳細資訊的連結，那就太好了。
