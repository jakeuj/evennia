(add-a-wiki-on-your-website)=
# 在您的網站上新增 wiki

```{warning}
截至 2023 年，[django wiki](https://django-wiki.readthedocs.io/en/main/) 僅支援 Django 4.0。 Evennia 需要 Django 4.1+。雖然 django-wiki 仍然處於活動狀態並且最終有望更新，但目前安裝可能會出現問題或麻煩。本教學可能不會一開始就起作用。
```

```{note}
在學習本教學之前，您可能需要閱讀[基本 Web 教學](./Web-Changing-Webpage.md) 中的介紹。  閱讀 [Django 教學](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) 的前三個部分可能也會有所幫助。

```
本教學將提供在您的網站上安裝 wiki 的逐步流程。
幸運的是，您不必手動建立功能，因為其他人已經完成了這些工作，我們可以輕鬆地將他們的工作與 Django 整合。  我決定專注於
[Django 維基](https://django-wiki.readthedocs.io/)。

[Django-wiki](https://django-wiki.readthedocs.io/) 提供了許多與 wiki 相關的功能，得到了積極的維護（無論如何，此時），並且在 Evennia 中安裝並不太困難。  您可以在[此處檢視 Django-wiki 演示](https://demo.django-wiki.org)。

(basic-installation)=
## 基本安裝

您應該先關閉 Evennia 伺服器（如果它正在執行）。  我們將執行遷移並稍微更改虛擬環境。  開啟終端機並啟動您的 Python 環境，即用於執行 `evennia` 指令的環境。

如果您使用 Evennia 安裝說明中的預設位置，則它應該是以下位置之一：

* 在 Linux 上：
    ```
    source evenv/bin/activate
    ```
* 或Windows：
    ```
    evenv\bin\activate
    ```

(installing-with-pip)=
### 使用 pip 安裝

使用 pip 安裝 wiki：

    pip install wiki

這可能需要一些時間，Django-wiki 有一些依賴項。

(adding-the-wiki-in-the-settings)=
### 在設定中新增 wiki

您需要新增一些設定才能在您的網站上使用 wiki 應用程式。  開啟 `server/conf/settings.py` 檔案並在底部新增以下內容（但在匯入 `secret_settings`1% 之前）。  以下是新增了 Django-wiki 的設定檔範例：

```python
# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "demowiki"

######################################################################
# Django-wiki settings
######################################################################
INSTALLED_APPS += (
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',
)

# Disable wiki handling of login/signup, so that it uses your Evennia login system instead
WIKI_ACCOUNT_HANDLING = False
WIKI_ACCOUNT_SIGNUP_ALLOWED = False

# Enable wikilinks, e.g. [[Getting Started]]
WIKI_MARKDOWN_KWARGS = {
    'extensions': [
        'wikilinks',
    ]
}

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
```

「Django-wiki 設定」部分中的所有內容都是您需要包含的內容。

(adding-the-new-urls)=
### 增加新的URLs

接下來，您需要將兩個 URLs 新增至檔案 `web/urls.py` 中。你可以透過修改來做到這一點
`urlpatterns` 看起來像這樣：

```python
# add patterns
urlpatterns = [
    # website
    path("", include("web.website.urls")),
    # webclient
    path("webclient/", include("web.webclient.urls")),
    # web admin
    path("admin/", include("web.admin.urls")),
    # wiki
    path("wiki/", include("wiki.urls")),
    path("notifications/", include("django_nyt.urls")),
]
```

最後兩行是您需要新增的內容。

(running-migrations)=
### 執行遷移

接下來您需要執行遷移，因為 wiki 應用程式在我們的資料庫中新增了一些表：

    evennia migrate


(initializing-the-wiki)=
### 初始化維基

最後一步！繼續並再次啟動您的伺服器。

    evennia start

啟動完成後，請造訪您的 evennia 網站 (e.g.http://localhost:4001 ) 並使用您的超級使用者帳號登入（如果您尚未登入）。然後，前往您的新 wiki (e.g.http://localhost:4001/wiki )。它會提示您建立起始頁面 - 放置您想要的任何內容，您可以稍後更改它。

恭喜！你都完成了！

(defining-wiki-permissions)=
## 定義 wiki 許可權

維基通常旨在作為一種協作成果 - 但您可能仍然想設定一些關於允許誰做什麼的規則。誰可以創造新文章？編輯它們？刪除它們？ ETC。

最簡單的兩種方法是使用 Django-wiki 的基於群組的許可權
系統 - 或者，因為這是一個 Evennia 站點，所以在您的設定檔中定義與 Evennia 的許可權系統相關聯的您自己的自訂許可權規則。

(group-permissions)=
### 群組許可權

維基本身控制每篇文章的閱讀/編輯許可權。文章的建立者將始終擁有該文章的讀取/寫入許可權。此外，該文章將具有基於群組的許可權和一般許可權。

預設情況下，Evennia 的許可權群組 *不會* 被 wiki 識別，因此您必須建立自己的許可權群組。前往遊戲 Django 管理面板的「群組」頁面，並在此處新增您想要的 wiki 許可權群組。

***注意：*** *如果您想將這些群組連線到遊戲的許可權級別，您需要修改遊戲以將這兩個群組套用到帳戶。 *

新增這些群組後，它們將立即在您的 wiki 中可用！

(settings-permissions)=
### 設定許可權

Django-wiki 還允許您使用設定檔中的自訂網站範圍許可權規則來繞過其基於文章的許可權。如果您不想使用群組系統，或者您想要一個簡單的解決方案來將 Evennia 許可權等級連線到 wiki 訪問，那麼這就是您要走的路。

以下是 `settings.py` 檔案中的基本設定範例：

```python
# In server/conf/settings.py
# ...

# Custom methods to link wiki permissions to game perms
def is_superuser(article, user):
    """Return True if user is a superuser, False otherwise."""
    return not user.is_anonymous and user.is_superuser

def is_builder(article, user):
    """Return True if user is a builder, False otherwise."""
    return not user.is_anonymous and user.permissions.check("Builder")

def is_player(article, user):
    """Return True if user is a builder, False otherwise."""
    return not user.is_anonymous and user.permissions.check("Player")

# Create new users
WIKI_CAN_ADMIN = is_superuser

# Change the owner and group for an article
WIKI_CAN_ASSIGN = is_superuser

# Change the GROUP of an article, despite the name
WIKI_CAN_ASSIGN_OWNER = is_superuser

# Change read/write permissions on an article
WIKI_CAN_CHANGE_PERMISSIONS = is_superuser

# Mark an article as deleted
WIKI_CAN_DELETE = is_builder

# Lock or permanently delete an article
WIKI_CAN_MODERATE = is_superuser

# Create or edit any pages
WIKI_CAN_WRITE = is_builder

# Read any pages
WIKI_CAN_READ = is_player

# Completely disallow editing and article creation when not logged in
WIKI_ANONYMOUS_WRITE = False
```

許可權函式可以檢查存取使用者的任何內容，只要函式傳回 True（允許）或 False（不允許）。

有關可能設定的完整列表，您可以檢視[django-wiki 檔案](https://django-wiki.readthedocs.io/en/latest/settings.html)。
