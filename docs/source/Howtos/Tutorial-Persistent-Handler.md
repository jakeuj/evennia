(making-a-persistent-object-handler)=
# 製作持久物件處理程式

_handler_ 是將物件上的功能分組的便捷方法。這使您能夠從邏輯上
將與該事物相關的所有操作集中在一個地方。本教學舉例說明如何使您的
擁有自己的處理程式，並確保您儲存在其中的資料在重新載入後仍然存在。

例如，當您執行 `obj.attributes.get("key")` 或 `obj.tags.add('tagname')` 時，您正在喚起
處理程式在 `obj` 上儲存為 `.attributes` 和 `tags`。這些處理程式上有方法（`get()`
以及本例中的`add()`）。

(base-handler-example)=
## 基本處理程式範例

這是設定物件處理程式的基本方法：

```python

from evennia import DefaultObject, create_object
from evennia.utils.utils import lazy_property

class NameChanger:
    def __init__(self, obj):
        self.obj = obj

    def add_to_key(self, suffix):
        self.obj.key = f"{self.obj.key}_{suffix}"

# make a test object
class MyObject(DefaultObject):
    @lazy_property:
    def namechange(self):
       return NameChanger(self)


obj = create_object(MyObject, key="test")
print(obj.key)
>>> "test"
obj.namechange.add_to_key("extra")
print(obj.key)
>>> "test_extra"
```

這裡發生的是我們建立一個新類別`NameChanger`。我們使用
`@lazy_property` 裝飾器來設定它 - 這意味著處理程式將不會
實際建立直到有人真正想要使用它，透過訪問
`obj.namechange` 稍後。修飾的 `namechange` 方法傳回處理程式
並確保使用 `self` 對其進行初始化 - 這將成為 `obj` 內的
處理程式！

然後我們建立一個愚蠢的方法`add_to_key`，它使用處理程式來操作
物件的鍵。在這個例子中，處理程式毫無意義，但是
這種方式的分組功能既可以使 API 易於記憶，又可以
還可以允許您快取資料以便於存取 - 這就是
`AttributeHandler` (`.attributes`) 和 `TagHandler` (`.tags`) 有效。

(persistent-storage-of-data-in-handler)=
## 資料永續性儲存在handler中

假設我們想在處理程式中追蹤「任務」。 「任務」是一個常規課程
這代表著追求。我們舉個簡單的例子：

```python
# for example in mygame/world/quests.py


class Quest:

    key = "The quest for the red key"

    def __init__(self):
        self.current_step = "start"

    def check_progress(self):
        # uses self.current_step to check
        # progress of this quest
        getattr(self, f"step_{self.current_step}")()

    def step_start(self):
        # check here if quest-step is complete
        self.current_step = "find_the_red_key"
    def step_find_the_red_key(self):
        # check if step is complete
        self.current_step = "hand_in_quest"
    def step_hand_in_quest(self):
        # check if handed in quest to quest giver
        self.current_step = None  # finished

```

我們希望開發人員建立其子類別來實現不同的任務。具體是如何運作的
沒關係，關鍵是我們想要追蹤 `self.current_step` - _should 的屬性
在伺服器重新載入後倖存_。但到目前為止`Quest`還沒有辦法做到這一點，這只是一個
沒有連線到資料庫的普通 Python 類別。

(handler-with-saveload-capability)=
### 具有儲存/載入功能的處理程式

讓我們建立一個 `QuestHandler` 來管理角色的任務。

```python
# for example in the same mygame/world/quests.py


class QuestHandler:
    def __init__(self, obj):
        self.obj = obj
        self.do_save = False
        self._load()

    def _load(self):
        self.storage = self.obj.attributes.get(
            "quest_storage", default={}, category="quests")

    def _save(self):
        self.obj.attributes.add(
            "quest_storage", self.storage, category="quests")
        self._load()  # important
        self.do_save = False

    def add(self, questclass):
        self.storage[questclass.key] = questclass(self.obj)
        self._save()

    def check_progress(self):
            quest.check_progress()
        if self.do_save:
            # .do_save is set on handler by Quest if it wants to save progress
            self._save()

```

這個處理程式只是一個普通的 Python 類，它自己沒有資料庫儲存。但它有一個連結
到`.obj`，假設它是一個完整的型別實體，我們可以在其上建立
持久[屬性](../Components/Attributes.md)來儲存我們喜歡的東西！

我們製作兩種輔助方法 `_load` 和
`_save` 處理本地提取並將 `storage` 儲存到物件上的 Attribute。為了避免
節省超過必要的錢，我們有財產`do_save`。這個我們將在下面的`Quest`中設定。

> 請注意，一旦我們`_save`資料，我們需要再次呼叫`_load`。這是為了確保我們儲存在處理程式上的版本已正確反序列化。如果您收到有關資料為 `bytes` 的錯誤，您可能錯過了此步驟。


(make-quests-storable)=
### 使任務可儲存

處理程式會將所有 `Quest` 物件儲存為 `dict`，位於 `obj` 上的 Attribute 中。我們還沒有完成
不過，`Quest` 物件也需要存取 `obj` - 這不僅對計算很重要
任務是否完成（`Quest` 必須能夠檢查任務者的庫存以檢視是否
例如，它們有紅色鑰匙），它還允許 `Quest` 告訴處理程式其狀態
改變了，應該要儲存。

我們將 `Quest` 改為：

```python
from evennia.utils import dbserialize


class Quest:

    def __init__(self, obj):
        self.obj = obj
        self._current_step = "start"

    def __serialize_dbobjs__(self):
        self.obj = dbserialize.dbserialize(self.obj)

    def __deserialize_dbobjs__(self):
        if isinstance(self.obj, bytes):
            self.obj = dbserialize.dbunserialize(self.obj)

    @property
    def questhandler(self):
        return self.obj.quests

    @property
    def current_step(self):
        return self._current_step

    @current_step.setter
    def current_step(self, value):
        self._current_step = value
        self.questhandler.do_save = True  # this triggers save in handler!

    # [same as before]

```

`Quest.__init__` 現在採用 `obj` 作為引數，以符合我們傳遞給它的內容
`QuestHandler.add`。我們想要監控`current_step`的變化，所以我們
把它變成`property`。當我們編輯該值時，我們將 `do_save` 標誌設為
處理程式，這表示檢查後會將狀態儲存到資料庫
所有任務都取得進展。 `Quest.questhandler` 屬性允許輕鬆
傳回處理程式（及其所在的物件）。

需要 `__serialize__dbobjs__` 和 `__deserialize_dbobjs__` 方法
因為 `Attributes` 無法儲存「隱藏」資料庫物件（`Quest.obj`
財產。這些方法可以幫助 Evennia 正確地序列化/反序列化 `Quest`
處理程式儲存它。  有關詳細資訊，請參閱[儲存單個
屬性中的物件](../Components/Attributes.md#storing-single-objects)

(tying-it-all-together)=
### 將它們結合在一起

我們需要做的最後一件事是將任務處理程式新增至角色：

```python
# in mygame/typeclasses/characters.py

from evennia import DefaultCharacter
from evennia.utils.utils import lazy_property
from .world.quests import QuestHandler  # as an example


class Character(DefaultCharacter):
    # ...
    @lazy_property
    def quests(self):
        return QuestHandler(self)

```


現在您可以建立任務類別來描述您的任務並將它們新增至
字元與

```python
character.quests.add(FindTheRedKey)
```

稍後可以做

```python
character.quests.check_progress()
```

並確保任務資料在重新載入之間不會遺失。

您可以找到一個成熟的任務處理程式範例，如 [EvAdventure
任務](evennia.contrib.tutorials.evadventure.quests) contrib 在 Evennia
儲存庫。
