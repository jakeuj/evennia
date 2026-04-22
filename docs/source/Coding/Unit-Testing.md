(unit-testing)=
# 單元測試

*單元測試*意味著對程式的各個元件進行相互隔離的測試，以確保每個部分在與其他部分一起使用之前可以獨立工作。廣泛的測試有助於避免新的更新導致意外的副作用，並減少一般的程式碼腐爛（可以在[此處](https://en.wikipedia.org/wiki/Unit_test)找到有關單元測試的更全面的維基百科文章）。

典型的單元測試集使用給定的輸入呼叫某些函式或方法，檢視結果並確保結果符合預期。 Evennia 使用中央*測試執行程式*，而不是使用大量獨立的測試程式。這是一個程式，它收集 Evennia 原始程式碼（稱為*測試套件*）中的所有可用測試並一次執行它們。報告錯誤和回溯。

預設 Evennia 僅測試自身。但您也可以將自己的測試加入遊戲程式碼中，並讓 Evennia 為您執行這些測試。
(running-the-evennia-test-suite)=
## 執行 Evennia 測試套件

要執行完整的 Evennia 測試套件，請前往您的遊戲資料夾並發出指令

    evennia test evennia

這將使用預設設定執行所有 evennia 測試。您也可以透過指定庫的子包來僅執行所有測試的子集：

    evennia test evennia.commands.default

將例項化一個臨時資料庫來管理測試。如果一切順利，您將看到執行了多少測試以及花費了多長時間。如果出現問題，您將收到錯誤訊息。如果您對 Evennia 做出了貢獻，那麼這是一個有用的健全性檢查，可以確定您沒有引入意外的錯誤。

(running-custom-game-dir-unit-tests)=
## 執行自訂 game-dir 單元測試

如果您已經為您的遊戲實現了自己的測試，您可以從您的遊戲目錄中執行它們

    evennia test --settings settings.py .

句點（`.`）表示執行目前目錄和所有子目錄中找到的所有測試。如果您只想在這些子目錄中執行測試，您也可以指定 `typeclasses` 或 `world`。

需要注意的重要一點是，這些測試都將使用_預設Evennia 設定_執行。要使用您自己的設定檔執行測試，您必須使用 `--settings` 選項：

    evennia test --settings settings.py .

Evennia 的`--settings` 選項採用`mygame/server/conf` 資料夾中的檔案名稱。它通常用於交換設定檔以進行測試和開發。與 `test` 結合使用，它會強制 Evennia 使用此設定檔而不是預設設定檔。

您也可以透過給出特定的路徑來測試它們

    evennia test --settings settings.py world.tests.YourTest

(writing-new-unit-tests)=
## 編寫新的單元測試

Evennia 的測試套件使用 Django 單元測試系統，而該系統又依賴 Python 的 *unittest* 模組。

為了讓測試執行程式找到測試，必須將它們放入名為 `test*.py` 的模組中（例如 `test.py`、`tests.py` 等）。這樣的測試模組可以在套件中的任何位置找到。檢視 Evennia 的 `tests.py` 模組中的一些模組以瞭解它們的外觀可能是個好主意。

在模組內部，您需要放置一個從 `unittest.TestCase` 繼承（任意距離）的類別。在該類別上以 `test_` 開頭的每個方法都將作為單元測試單獨執行。有兩種特殊的可選方法 `setUp` 和 `tearDown`（如果您定義了它們）分別在 _every_ 測試之前和之後執行。這對於建立、設定和清理類別中每個測試所需的內容非常有用。

要實際測試，您可以在類別上使用特殊的 `assert...` 方法。最常見的是 `assertEqual`，它確保結果符合您的預期。

這是原理的例子。假設您將其放入 `mygame/world/tests.py`
想要測試 `mygame/world/myfunctions.py` 中的函式

```python
    # in a module tests.py somewhere i your game dir
    import unittest

    from evennia import create_object
    # the function we want to test
    from .myfunctions import myfunc


    class TestObj(unittest.TestCase):
       """This tests a function myfunc."""

       def setUp(self):
           """done before every of the test_ * methods below"""
           self.obj = create_object("mytestobject")

       def tearDown(self):
           """done after every test_* method below """
           self.obj.delete()

       def test_return_value(self):
           """test method. Makes sure return value is as expected."""
           actual_return = myfunc(self.obj)
           expected_return = "This is the good object 'mytestobject'."
           # test
           self.assertEqual(expected_return, actual_return)
       def test_alternative_call(self):
           """test method. Calls with a keyword argument."""
           actual_return = myfunc(self.obj, bad=True)
           expected_return = "This is the baaad object 'mytestobject'."
           # test
           self.assertEqual(expected_return, actual_return)
```

要測試這一點，請執行

    evennia test --settings settings.py .

執行整個測試模組

    evennia test --settings settings.py world.tests

或特定類別：

    evennia test --settings settings.py world.tests.TestObj

您也可以執行特定測試：

    evennia test --settings settings.py world.tests.TestObj.test_alternative_call

您可能還想閱讀 [unittest 模組的 Python 檔案](https://docs.python.org/library/unittest.html)。

(using-the-evennia-testing-classes)=
### 使用 Evennia 測試類

Evennia 提供了許多自訂測試類，有助於測試 Evennia 功能。它們都可以在[evennia.utils.test_resources](evennia.utils.test_resources)中找到。

```{important}
請注意，這些基類已經實現了 `setUp` 和 `tearDown`，因此如果您想自己在其中新增內容，您應該記住使用 e.g。 `super().setUp()` 在你的程式碼中。
```
(classes-for-testing-your-game-dir)=
#### 用於測試您的遊戲目錄的類

這些都使用您傳遞給它們的任何設定，並且非常適合測試遊戲目錄中的程式碼。

- `EvenniaTest` - 這為您的測試設定了完整的物件環境。所有已建立的實體
可以作為類別的屬性進行存取：
  - `.account` - 一個名為「TestAccount」的假[帳戶](evennia.accounts.accounts.DefaultAccount)。
  - `.account2` - 另一個名為「TestAccount2」的[帳戶](evennia.accounts.accounts.DefaultAccount)。
  - `.char1` - 連結到`.account`的[角色](evennia.objects.objects.DefaultCharacter)，名為`Char`。
    This has 'Developer' permissions but is not a superuser.
  - `.char2` - 另一個[角色](evennia.objects.objects.DefaultCharacter)連結到`account2`，名為`Char2`。
    This has base permissions (player).
  - `.obj1` - 一個名為「Obj」的常規[物件](evennia.objects.objects.DefaultObject)。
  - `.obj2` - 另一個名為「Obj2」的[物件](evennia.objects.objects.DefaultObject)。
  - `.room1` - 一個名為「房間」的[房間](evennia.objects.objects.DefaultRoom)。兩個角色和兩個
    objects are located inside this room. It has a description of "room_desc".
  - `.room2` - 另一個名為「Room2」的[房間](evennia.objects.objects.DefaultRoom)。它是空的並且沒有固定的描述。
  - `.exit` - 名為「out」的出口，從 `.room1` 通往 `.room2`。
  - `.script` - 名為「Script」的 [Script](evennia.scripts.scripts.DefaultScript)。這是一個惰性script
    without a timing component.
  - `.session` - 模仿玩家的假 [Session](evennia.server.serversession.ServerSession)
    connecting to the game. It is used by `.account1` and has a sessid of 1.
- `EvenniaCommandTest` - 與 `EvenniaTest` 具有相同的環境，但也增加了一個特殊的 [.call()](evennia.utils.test_resources.EvenniaCommandTestMixin.call) 方法，專門用於測試 Evennia [指令](../Components/Commands.md)。它允許您將指令_實際_返回給玩家的內容與您期望的內容進行比較。請閱讀 `call` api 檔案以獲取更多資訊。
- `EvenniaTestCase` - 這與常規 Python `TestCase` 類別相同，它是
只是為了命名對稱性，下面有 `BaseEvenniaTestCase` 。

這是使用 `EvenniaTest` 的範例

```python
# in a test module

from evennia.utils.test_resources import EvenniaTest

class TestObject(EvenniaTest):
    """Remember that the testing class creates char1 and char2 inside room1 ..."""
    def test_object_search_character(self):
        """Check that char1 can search for char2 by name"""
        self.assertEqual(self.char1.search(self.char2.key), self.char2)

    def test_location_search(self):
        """Check so that char1 can find the current location by name"""
        self.assertEqual(self.char1.search(self.char1.location.key), self.char1.location)
        # ...
```

此範例測試自訂指令。

```python
    from evennia.commands.default.tests import EvenniaCommandTest
from commands import command as mycommand


class TestSet(EvenniaCommandTest):
    """Tests the look command by simple call, using Char2 as a target"""

    def test_mycmd_char(self):
        self.call(mycommand.CmdMyLook(), "Char2", "Char2(#7)")

    def test_mycmd_room(self):
        """Tests the look command by simple call, with target as room"""
        self.call(mycommand.CmdMyLook(), "Room",
                  "Room(#1)\nroom_desc\nExits: out(#3)\n"
                  "You see: Obj(#4), Obj2(#5), Char2(#7)")
```

使用`.call`時，不需要指定整個字串；你可以只給出它的開頭，如果匹配，就足夠了。使用 `\n` 表示換行符號（這是 `.call` 幫助器的特殊用法），`||` 表示在指令中多次使用 `.msg()`。 `.call` 幫助器有很多引數用於模仿呼叫指令的不同方式，因此請務必[閱讀.call() 的 API 檔案](evennia.utils.test_resources.EvenniaCommandTestMixin.call)。

(classes-for-testing-evennia-core)=
#### 用於測試Evennia核心的類

這些用於測試 Evennia 本身。他們提供與課程相同的資源
以上，但強制執行 `evennia/settings_default.py` 中找到的 Evennias 預設設定，忽略遊戲目錄中的任何設定更改。

- `BaseEvenniaTest` - 以上所有預設物件，但具有強制預設設定
- `BaseEvenniaCommandTest` - 用於測試指令，但具有強制預設設定
- `BaseEvenniaTestCase` - 無預設物件，僅強制執行預設設定

還有兩個特殊的「mixin」類別。這些是上面的類別中的用途，但也可以
如果您想混合自己的測試類，這會很有用：

- `EvenniaTestMixin` - 建立所有測試環境物件的類別 mixin。
- `EvenniaCommandMixin` - 新增 `.call()` 指令測試幫助器的類別 mixin。

如果您想幫助編寫 Evennia 的單元測試，請檢視 Evennia 的 [coveralls.io
頁](https://coveralls.io/github/evennia/evennia)。在那裡您可以看到哪些模組具有任何形式的測試覆蓋率，哪些沒有。感謝所有幫助！

(unit-testing-contribs-with-custom-models)=
### 使用自訂模型進行單元測試contribs

一種特殊情況是，如果您要建立一個貢獻以轉到使用其[自己的資料庫模型](../Concepts/Models.md) 的 `evennia/contrib` 資料夾。問題在於 Evennia （和 Django）會
只辨識`settings.INSTALLED_APPS`中的模型。如果使用者想要使用您的contrib，他們將需要將您的模型新增至他們的設定檔。但由於 contribs 是可選的，因此您無法將模型新增至 Evennia 的中央 `settings_default.py` 檔案 - 這將始終建立您的可選模型，無論使用者是否需要它們。但同時，貢獻是 Evennia 分佈的一部分，其單元測試應與使用 `evennia test evennia` 的所有其他 Evennia 測試一起執行。

執行此操作的方法是僅在測試執行時暫時將模型新增至 `INSTALLED_APPS` 目錄。這是如何執行此操作的範例。

> 請注意，此解決方案源自此 [stackexchange 答案](http://stackoverflow.com/questions/502916/django-how-to-create-a-model-dynamically-just-for-testing#503435) 目前未經測試！請報告您的發現。

```python
# a file contrib/mycontrib/tests.py

from django.conf import settings
import django
from evennia.utils.test_resources import BaseEvenniaTest

OLD_DEFAULT_SETTINGS = settings.INSTALLED_APPS
DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        'contrib.mycontrib.tests',
    ),
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3"
        }
    },
    SILENCED_SYSTEM_CHECKS=["1_7.W001"],
)


class TestMyModel(BaseEvenniaTest):
    def setUp(self):
        if not settings.configured:
            settings.configure(**DEFAULT_SETTINGS)
        django.setup()

        from django.core.management import call_command
        from django.db.models import loading
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

    def tearDown(self):
        settings.configure(**OLD_DEFAULT_SETTINGS)
        django.setup()

        from django.core.management import call_command
        from django.db.models import loading
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

    # test cases below ...

    def test_case(self):
# test case here
```


(a-note-on-making-the-test-runner-faster)=
### 關於使測試執行速度更快的注意事項

如果您的自訂模型具有大量遷移，則建立測試資料庫可能需要很長時間。如果您不需要為測試執行遷移，則可以使用 django-test-without-migrations 套件停用它們。要安裝它，只需：

```
$ pip install django-test-without-migrations
```

然後將其新增到您的`server.conf.settings.py`中的`INSTALLED_APPS`：

```python
INSTALLED_APPS = (
    # ...
    'test_without_migrations',
)
```

執行此操作後，您可以透過新增 `--nomigrations` 引數來執行測試而不進行遷移：

```
evennia test --settings settings.py --nomigrations .
```
