(web-character-generation)=
# 網頁角色生成


(introduction)=
## 介紹

本教學將建立一個簡單的基於 Web 的介面，用於產生新的遊戲角色。帳戶需要先登入網站（使用其 `AccountDB` 帳戶）。一旦完成角色生成，角色將立即建立，然後帳戶可以登入遊戲並立即玩（角色不需要工作人員批准或類似的東西）。本指南不會介紹如何在網站上建立 AccountDB 並具有正確的許可權來傳輸到其網路建立的角色。

設定 `AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False` 可能是最有用的，這樣所有玩家角色都可以透過它建立。

您應該熟悉 Django 如何設定其模型模板檢視框架。您需要了解基本的[網頁角色檢視教學](./Web-Character-View-Tutorial.md)中發生了什麼。如果您不理解列出的教學或掌握 Django 基礎知識，請先檢視 [Django 教學](https://docs.djangoproject.com/en/4.1/intro/) 以瞭解 Django 的功能，然後再將 Evennia 加入其中（Evennia 與網站介面共享其 API 和屬性）。本指南將概述所需的模型、檢視、url 和 html 範本的格式。

(pictures)=
## 圖片

以下是我們將製作的簡單應用程式的一些螢幕截圖。

索引頁，尚未完成字元應用：

***
![索引頁，尚未完成字元應用。 ](https://lh3.googleusercontent.com/-57KuSWHXQ_M/VWcULN152tI/AAAAAAAAEZg/kINTmVlHf6M/w425-h189-no/webchargen_index2.gif)
***

點選“建立”連結後，您可以建立角色（這裡我們只有名稱和背景，您可以新增適合您的遊戲所需的任何內容）：

***
![角色建立。 ](https://lh3.googleusercontent.com/-ORiOEM2R_yQ/VWcUKgy84rI/AAAAAAAAEZY/B3CBh3FHii4/w607-h60-no/webchargen_creation.gif)
***

返回索引頁。輸入我們的角色應用程式（我們將角色稱為“TestApp”）後，您會看到它列出：

***
![已提交申請。 ](https://lh6.googleusercontent.com/-HlxvkvAimj4/VWcUKjFxEiI/AAAAAAAAEZo/gLppebr05JI/w321-h194-no/webchargen_index1.gif)
***

我們還可以透過點選檢視已編寫的角色應用程式 - 這會將我們帶到*詳細*頁面：

***
![角色應用的詳細檢視。 ](https://lh6.googleusercontent.com/-2m1UhSE7s_k/VWcUKfLRfII/AAAAAAAAEZc/UFmBOqVya4k/w267-h175-no/webchargen_detail.gif)
***

(installing-an-app)=
## 安裝應用程式

假設您的遊戲名為“mygame”，導航到您的 `mygame/` 目錄，然後輸入：

    cd web
    evennia startapp chargen

這將初始化一個新的 Django 應用程式，我們選擇在 `mygame/web/` 中呼叫“chargen”。我們將其放在 `web/` 下，以將所有網路內容放在一起，但您可以按照自己的喜好進行組織。它是包含 Django 需要的一些基本啟動內容的目錄。

接下來，導航到 `mygame/server/conf/settings.py` 並新增或編輯以下行以使 Evennia（和 Django）瞭解我們的新應用程式：

    INSTALLED_APPS += ('web.chargen',)

之後，我們將開始定義我們的*模型*（資料庫儲存的描述），
*檢視*（伺服器端網站內容產生器）、*urls*（網頁瀏覽器如何尋找頁面）和*範本*（網頁應如何建置）。

(installing-checkpoint)=
### 安裝 - 檢查點：

* 你應該有一個名為 `chargen` 的資料夾或你在 mygame/web/ 目錄中選擇的任何資料夾
* 您應該將應用程式名稱新增到 `settings.py` 中的 INSTALLED_APPS

(create-models)=
## 建立模型

模型在 `mygame/web/chargen/models.py` 中建立。

[Django 資料庫模型](../Concepts/Models.md) 是一個 Python 類，描述了資料庫儲存
您想要管理的資料。您選擇儲存的任何資料都儲存在與遊戲相同的資料庫中，並且您可以在此處存取遊戲的所有物件。

我們需要定義角色應用程式實際上是什麼。這因遊戲而異，因此在本教學中，我們將使用以下資料庫欄位定義一個簡單的角色表：

* `app_id` (AutoField)：此字元應用程式表的主鍵。
* `char_name` (CharField)：新角色的名字。
* `date_applied` (DateTimeField)：收到此申請的日期。
* `background` (TextField)：人物故事背景。
* `account_id` (IntegerField)：此應用程式屬於哪個帳戶ID？這是一個
來自 AccountDB 物件的 AccountID。
* `submitted` (BooleanField): `True`/`False` 取決於申請是否已提交。

> 注意：在成熟的遊戲中，您可能希望他們能夠選擇種族、技能、屬性等。

我們的 `models.py` 檔案應該如下所示：

```python
# in mygame/web/chargen/models.py

from django.db import models

class CharApp(models.Model):
    app_id = models.AutoField(primary_key=True)
    char_name = models.CharField(max_length=80, verbose_name='Character Name')
    date_applied = models.DateTimeField(verbose_name='Date Applied')
    background = models.TextField(verbose_name='Background')
    account_id = models.IntegerField(default=1, verbose_name='Account ID')
    submitted = models.BooleanField(default=False)
```

您應該考慮如何將您的應用程式連結到您的帳戶。在本教學中，我們在角色應用程式模型上使用 account_id attribute 來追蹤哪些角色屬於哪些帳戶。由於帳戶 ID 是 Evennia 中的主鍵，因此它是一個很好的候選者，因為在 Evennia 中永遠不會有兩個相同的 ID。您可以隨意使用其他任何內容，但出於本指南的目的，我們將使用帳戶 ID 透過正確的帳戶加入角色應用程式。

(model-checkpoint)=
### 型號 - 檢查點：

* 您應該使用上面顯示的模型類別填寫`mygame/web/chargen/models.py`（最終新增與您的遊戲所需匹配的欄位）。

(create-views)=
## 建立檢視

*檢視*是伺服器端結構，使動態資料可用於網頁。我們將把它們新增到`mygame/web/chargen.views.py`。我們範例中的每個檢視都代表了一個
具體網頁。我們將在這裡使用三個檢視和三個頁面：

* 指數（管理`index.html`）。這是您導航到時看到的內容
`http://yoursite.com/chargen`。
* 詳細顯示表（管理`detail.html`）。被動顯示給定角色統計資料的頁面。
* 角色建立表（管理`create.html`）。這是需要填寫欄位的主表單。

(index-view)=
### *索引*檢視

我們先從索引開始。

我們希望角色能夠看到他們創造的角色，所以讓我們

```python
# file mygame/web/chargen.views.py

from .models import CharApp

def index(request):
    current_user = request.user # current user logged in
    p_id = current_user.id # the account id
    # submitted Characters by this account
    sub_apps = CharApp.objects.filter(account_id=p_id, submitted=True)
    context = {'sub_apps': sub_apps}
    # make the variables in 'context' available to the web page template
    return render(request, 'chargen/index.html', context)
```

(detail-view)=
### *詳細*檢視

我們的詳細資訊頁面將包含使用者可以看到的相關角色應用資訊。由於這是一個基本演示，因此我們的詳細資訊頁面將僅顯示兩個欄位：

* 角色名稱
* 人物背景

我們將再次使用帳戶 ID 只是為了再次檢查嘗試檢查我們的角色頁面的人實際上是擁有該應用程式的帳戶。

```python
# file mygame/web/chargen.views.py

def detail(request, app_id):
    app = CharApp.objects.get(app_id=app_id)
    name = app.char_name
    background = app.background
    submitted = app.submitted
    p_id = request.user.id
    context = {'name': name, 'background': background,
        'p_id': p_id, 'submitted': submitted}
    return render(request, 'chargen/detail.html', context)
```

(creating-view)=
## *建立*檢視

可以預見的是，我們的 *create* 函式將是最複雜的檢視，因為它需要接受來自使用者的資訊，驗證訊息並將訊息傳送到伺服器。一旦表單內容被驗證，將實際建立一個可玩的角色。

我們將首先定義表單本身。在我們的簡單範例中，我們只是尋找角色的名稱和背景。我們在`mygame/web/chargen/forms.py`中建立這個表單：

```python
# file mygame/web/chargen/forms.py

from django import forms

class AppForm(forms.Form):
    name = forms.CharField(label='Character Name', max_length=80)
    background = forms.CharField(label='Background')
```

現在我們在我們看來利用了這種形式。

```python
# file mygame/web/chargen/views.py

from web.chargen.models import CharApp
from web.chargen.forms import AppForm
from django.http import HttpResponseRedirect
from datetime import datetime
from evennia.objects.models import ObjectDB
from django.conf import settings
from evennia.utils import create

def creating(request):
    user = request.user
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            background = form.cleaned_data['background']
            applied_date = datetime.now()
            submitted = True
            if 'save' in request.POST:
                submitted = False
            app = CharApp(char_name=name, background=background,
            date_applied=applied_date, account_id=user.id,
            submitted=submitted)
            app.save()
            if submitted:
                # Create the actual character object
                typeclass = settings.BASE_CHARACTER_TYPECLASS
                home = ObjectDB.objects.get_id(settings.GUEST_HOME)
                # turn the permissionhandler to a string
                perms = str(user.permissions)
                # create the character
                char = create.create_object(typeclass=typeclass, key=name,
                    home=home, permissions=perms)
                user.add_character(char)
                # add the right locks for the character so the account can
                #  puppet it
                char.locks.add(" or ".join([
                    f"puppet:id({char.id})",
                    f"pid({user.id})",
                    "perm(Developers)",
                    "pperm(Developers)",
                ]))
                char.db.background = background # set the character background
            return HttpResponseRedirect('/chargen')
    else:
        form = AppForm()
    return render(request, 'chargen/create.html', {'form': form})
```

> 另請注意，我們基本上使用 Evennia API 建立角色，並從 `AccountDB` 物件取得適當的許可權並將其複製到角色物件。我們取得使用者許可權 attribute 並將該字串清單轉換為字串物件，以便 create_object 函式正確處理許可權。

最重要的是，必須在建立的角色物件上設定以下屬性：

* Evennia [許可權](../Components/Permissions.md)（從`AccountDB`複製）。
* 右側的`puppet` [鎖定](../Components/Locks.md)，以便該帳戶稍後可以實際扮演該角色。
* 相關字元[typeclass](../Components/Typeclasses.md)
* 角色名稱（鍵）
* 角色的家庭房間位置（預設為`#2`）

其他屬性嚴格來說是可選的，例如我們角色上的`background` attribute。分解此函式並建立一個單獨的 _create_character 函式可能是一個好主意，以便設定帳戶擁有的角色物件。但使用 Evennia API，設定自訂屬性就像在 Evennia 遊戲目錄中一樣簡單。

完成所有這些之後，我們的 `views.py` 檔案應該如下所示：

```python
# file mygame/web/chargen/views.py

from django.shortcuts import render
from web.chargen.models import CharApp
from web.chargen.forms import AppForm
from django.http import HttpResponseRedirect
from datetime import datetime
from evennia.objects.models import ObjectDB
from django.conf import settings
from evennia.utils import create

def index(request):
    current_user = request.user # current user logged in
    p_id = current_user.id # the account id
    # submitted apps under this account
    sub_apps = CharApp.objects.filter(account_id=p_id, submitted=True)
    context = {'sub_apps': sub_apps}
    return render(request, 'chargen/index.html', context)

def detail(request, app_id):
    app = CharApp.objects.get(app_id=app_id)
    name = app.char_name
    background = app.background
    submitted = app.submitted
    p_id = request.user.id
    context = {'name': name, 'background': background,
        'p_id': p_id, 'submitted': submitted}
    return render(request, 'chargen/detail.html', context)

def creating(request):
    user = request.user
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            background = form.cleaned_data['background']
            applied_date = datetime.now()
            submitted = True
            if 'save' in request.POST:
                submitted = False
            app = CharApp(char_name=name, background=background,
            date_applied=applied_date, account_id=user.id,
            submitted=submitted)
            app.save()
            if submitted:
                # Create the actual character object
                typeclass = settings.BASE_CHARACTER_TYPECLASS
                home = ObjectDB.objects.get_id(settings.GUEST_HOME)
                # turn the permissionhandler to a string
                perms = str(user.permissions)
                # create the character
                char = create.create_object(typeclass=typeclass, key=name,
                    home=home, permissions=perms)
                user.add_character(char)
                # add the right locks for the character so the account can
                #  puppet it
                char.locks.add(" or ".join([
                    f"puppet:id({char.id})",
                    f"pid({user.id})",
                    "perm(Developers)",
                    "pperm(Developers)",
                ]))
                char.db.background = background # set the character background
            return HttpResponseRedirect('/chargen')
    else:
        form = AppForm()
    return render(request, 'chargen/create.html', {'form': form})
```

(create-views-checkpoint)=
### 建立檢視 - 檢查點：

* 您已經定義了一個具有索引、詳細資訊和建立函式的 `views.py`。
* 您已使用 `views.py` 的 `creating` 函式所需的 `AppForm` 類別定義了 forms.py。
* 您的 `mygame/web/chargen` 目錄現在應該有 `views.py` 和 `forms.py` 檔案

(create-urls)=
## 建立URLs

URL 模式有助於將來自 Web 瀏覽器的請求重新導向到正確的檢視。這些模式是在 `mygame/web/chargen/urls.py` 中建立的。

```python
# file mygame/web/chargen/urls.py

from django.urls import path
from web.chargen import views

urlpatterns = [
    # url: /chargen/
    path("", views.index, name='chargen-index'),
    # url: /chargen/5/
    path("<int:app_id>/", views.detail, name="chargen-detail"),
    # url: /chargen/create
    path("create/", views.creating, name='chargen-creating'),
]
```

您可以根據需要變更格式。為了使其更安全，您可以從「詳細」URL 中刪除 app_id，而只需使用 account_id 等統一欄位來獲取帳戶的應用程式，以查詢要顯示的所有角色應用程式物件。

要將其新增至我們的網站，我們還必須更新主 `mygame/website/urls.py` 檔案；這將有助於將我們的新 Chargen 應用程式與網站的其餘部分結合。 `urlpatterns` 變數，並將其更改為包括：

```python
# in file mygame/website/urls.py

from django.urls import path, include

urlpatterns = [
    # make all chargen endpoints available under /chargen url
    path("chargen/", include("web.chargen.urls")
]

```

(urls-checkpoint)=
### URLs - 檢查點：

* 您已在 `mygame/web/chargen` 目錄中建立了 `urls.py` 檔案
* 您已編輯主 `mygame/web/urls.py` 檔案以包含 `chargen` 目錄的 URL。

(html-templates)=
## HTML 模板

這樣我們就定義了 url 模式、檢視和模型。現在我們必須定義實際使用者將看到並與之互動的 HTML 範本。在本教學中，我們使用 Evennia 附帶的基本 *prosimii* 範本。

請注意，我們使用 `user.is_authenticated` 來確保使用者在未登入的情況下無法建立角色。

這些檔案將全部進入`/mygame/web/chargen/templates/chargen/`目錄。

(indexhtml)=
### index.html

此 HTML 範本應包含該帳戶目前處於活動狀態的所有應用程式的清單。在本次演示中，我們將僅列出該帳戶已提交的申請。您可以輕鬆調整它以包括已儲存的應用程式或其他型別的應用程式（如果您有不同型別的應用程式）。

請回傳 `views.py` 檢視我們在哪裡定義這些範本使用的變數。

```html
<!-- file mygame/web/chargen/templates/chargen/index.html-->

{% extends "base.html" %}
{% block content %}
{% if user.is_authenticated %}
    <h1>Character Generation</h1>
    {% if sub_apps %}
        <ul>
        {% for sub_app in sub_apps %}
            <li><a href="/chargen/{{ sub_app.app_id }}/">{{ sub_app.char_name }}</a></li>
        {% endfor %}
        </ul>
    {% else %}
        <p>You haven't submitted any character applications.</p>
    {% endif %}
  {% else %}
    <p>Please <a href="{% url 'login'%}">login</a>first.<a/></p>
{% endif %}
{% endblock %}
```

(detailhtml)=
### detail.html

此頁面應顯示其應用程式的詳細特徵表。這只會顯示他們的名字和角色背景。您可能希望擴充套件它以顯示遊戲的更多欄位。在成熟的角色生成中，您可能需要擴充套件提交的布林值attribute，以允許帳戶儲存角色申請並稍後提交。

```html
<!-- file mygame/web/chargen/templates/chargen/detail.html-->

{% extends "base.html" %}
{% block content %}
<h1>Character Information</h1>
{% if user.is_authenticated %}
    {% if user.id == p_id %}
        <h2>{{name}}</h2>
        <h2>Background</h2>
        <p>{{background}}</p>
        <p>Submitted: {{submitted}}</p>
    {% else %}
        <p>You didn't submit this character.</p>
    {% endif %}
{% else %}
<p>You aren't logged in.</p>
{% endif %}
{% endblock %}
```

(createhtml)=
### create.html

我們的建立 HTML 範本將使用我們在 views.py/forms.py 中定義的 Django 表單來驅動大部分應用程式程式。我們在`forms.py`中定義的每個欄位都會有表單輸入，這很方便。我們使用 POST 作為我們的方法，因為我們將資訊傳送到將更新資料庫的伺服器。作為替代方案，GET 的安全性會低得多。您可以在網路上其他地方閱讀 GET 與 POST 的檔案。

```html
<!-- file mygame/web/chargen/templates/chargen/create.html-->

{% extends "base.html" %}
{% block content %}
<h1>Character Creation</h1>
{% if user.is_authenticated %}
<form action="/chargen/create/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" name="submit" value="Submit"/>
</form>
{% else %}
<p>You aren't logged in.</p>
{% endif %}
{% endblock %}
```

(templates-checkpoint)=
### 模板 - 檢查點：

* 在您的 `mygame/web/chargen/templates/chargen` 目錄中建立 `index.html`、`detail.html` 和 `create.html` 模板

(activating-your-new-character-generation)=
## 啟動你的新角色生成

完成本教學後，您應該已經編輯或建立了以下檔案：

```bash
mygame/web/website/urls.py
mygame/web/chargen/models.py
mygame/web/chargen/views.py
mygame/web/chargen/urls.py
mygame/web/chargen/templates/chargen/index.html
mygame/web/chargen/templates/chargen/create.html
mygame/web/chargen/templates/chargen/detail.html
```

將所有這些檔案放入 `mygame/` 資料夾後，執行：

```bash
evennia makemigrations
evennia migrate
```

這將建立並更新模型。如果您在此階段看到任何錯誤，請仔細閱讀回溯，應該相對容易找出錯誤所在。

登入網站（您需要事先在遊戲中註冊玩家帳戶才能執行此操作）。接下來，您導航到`http://yourwebsite.com/chargen`（如果您在本地執行，這將類似於`http://localhost:4001/chargen`，您將看到正在執行的新應用程式。

希望這能為您提供一個良好的起點，幫助您瞭解如何實現自己的網路世代。主要的困難在於對新建立的角色物件進行適當的設定。值得慶幸的是，Evennia API 使這變得容易。

(adding-a-no-capcha-recapcha-on-your-character-generation)=
## 在您的角色生成中新增 no CAPCHA reCAPCHA

可悲的是，如果您的伺服器向網路開放，機器人可能會來存取並利用您的開放表單來建立數百、數千、數百萬個字元（如果您給它們機會）。  本節向您展示如何使用[否CAPCHA
reCAPCHA](https://www.google.com/recaptcha/intro/invisible.html) 由 Google 設計。  它不僅易於使用，而且對人類來說是使用者友好的。  一個簡單的核取方塊來檢查，除非谷歌有一些懷疑，在這種情況下，你將有一個更困難的測試，其中包含影象和通常的文字。  值得指出的是，只要谷歌不懷疑你是機器人，這就非常有用，不僅對於普通使用者，而且對於螢幕閱讀器使用者來說，閱讀影象內部即使不是不可能，也是相當困難的。  最重要的是，將其新增到您的網站中將非常容易。

(step-1-obtain-a-sitekey-and-secret-from-google)=
### 第 1 步：從 Google 取得 SiteKey 和機密

第一件事是向 Google 詢問一種方法來安全地驗證您的網站的服務。  為此，我們需要建立一個網站金鑰和一個秘密。  前往 [https://www.google.com/recaptcha/admin](https://www.google.com/recaptcha/admin) 建立這樣的網站金鑰。  當您擁有 Google 帳戶時，這很容易。

建立網站金鑰後，請安全儲存。  也要複製您的金鑰。  您應該在網頁上找到這兩個資訊。  兩者都包含大量字母和數字。

(step-2-installing-and-configuring-the-dedicated-django-app)=
### 第 2 步：安裝和設定專用 Django 應用程式

由於 Evennia 在 Django 上執行，因此新增 CAPCHA 並執行正確檢查的最簡單方法是安裝專用的 Django 應用程式。  很簡單：

    pip install django-nocaptcha-recaptcha

並將其新增到設定中已安裝的應用程式中。  在你的`mygame/server/conf/settings.py`中，你可能有這樣的東西：

```python
# ...
INSTALLED_APPS += (
    'web.chargen',
    'nocaptcha_recaptcha',
)
```

暫時不要關閉設定檔。  我們必須新增網站金鑰和秘密金鑰。  您可以在下面新增它們：

```python
# NoReCAPCHA site key
NORECAPTCHA_SITE_KEY = "PASTE YOUR SITE KEY HERE"
# NoReCAPCHA secret key
NORECAPTCHA_SECRET_KEY = "PUT YOUR SECRET KEY HERE"
```

(step-3-adding-the-capcha-to-our-form)=
### 步驟 3：將 CAPCHA 加入我們的表單中

最後我們必須將 CAPCHA 加入我們的表單。  這也會很容易。  首先，開啟您的`web/chargen/forms.py` 檔案。  我們將新增一個新欄位，但希望所有艱苦的工作都已為我們完成。  在您方便的時候更新，您最終可能會得到這樣的結果：

```python
from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

class AppForm(forms.Form):
    name = forms.CharField(label='Character Name', max_length=80)
    background = forms.CharField(label='Background')
    captcha = NoReCaptchaField()
```

如您所看到的，我們在表單中新增了一行匯入（第 2 行）和一個欄位。

最後，我們需要更新 HTML 檔案以新增到 Google 庫中。  你可以開啟
`web/chargen/templates/chargen/create.html`。  只需要新增一行：

```html
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
```

你應該把它放在頁面的底部。  就在結束正文之前就好了，但目前基礎頁面不提供頁尾區塊，因此我們將其放在內容區塊中。  請注意，這不是最好的地方，但它會起作用。  最後，你的
`web/chargen/templates/chargen/create.html` 檔案應如下所示：

```html
{% extends "base.html" %}
{% block content %}
<h1>Character Creation</h1>
{% if user.is_authenticated %}
<form action="/chargen/create/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" name="submit" value="Submit"/>
</form>
{% else %}
<p>You aren't logged in.</p>
{% endif %}
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
{% endblock %}
```

重新載入並開啟 [http://localhost:4001/chargen/create](http://localhost:4001/chargen/create/)，您應該在「提交」按鈕之前看到漂亮的 CAPCHA。  盡量不要選中該核取方塊來看看會發生什麼。  並在選中復選框時執行相同的操作！
