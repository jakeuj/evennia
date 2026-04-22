(game-quests)=
# 遊戲任務

```{warning}
本教學尚未完成，並且在實作中存在一些嚴重的錯誤。所以以此作為參考，但程式碼還不能直接使用。
```

_quest_是遊戲的一個共同特徵。從經典的取回任務（如取回 10 朵花）到涉及戲劇和陰謀的複雜任務鏈，任務需要在我們的遊戲中正確追蹤。

任務遵循特定的發展：

1. 任務已_開始_。這通常涉及玩家從任務提供者、工作委員會或其他來源接受任務。但這個任務也可以強加給玩家（「在房子倒塌之前將家人從著火的房子中拯救出來！」）
2. 一旦任務被接受並分配給角色，它要麼是`Started`（即「進行中」）、`Abandoned`、`Failed` 要麼`Complete`。
3. 一項任務可能包含一個或多個「步驟」。每個步驟都有自己的一組完成條件。
4. 在適當的時間檢查任務的_進度_。這可能會在計時器上或嘗試“提交”任務時發生。檢查時，將根據其完成條件檢查當前“步驟”。如果正常，則關閉該步驟並檢查下一步，直到遇到尚未完成的步驟，或沒有更多步驟，在這種情況下整個任務已完成。

```{sidebar} 
任務的範例實作可在 `evennia/contrib/tutorials` 下的 [evadventure/quests.py](evennia.contrib.tutorials.evadventure.quests) 中找到。
```
為了用程式碼表示任務，我們需要
- 一種方便且靈活的方法來編碼我們如何檢查任務的狀態和當前步驟。我們希望這個指令碼盡可能靈活。理想情況下，我們希望能夠用完整的 Python 來寫任務的邏輯。
- 堅持。我們接受任務的事實以及它的狀態和其他標誌必須儲存在資料庫中並在伺服器重新啟動後繼續存在。

我們將使用兩段 Python 程式碼來完成此任務：
- `EvAdventureQuest`：一個有輔助方法的Python類，我們可以呼叫它來檢查目前的任務狀態，判斷給定的任務步驟是否完成。我們將透過簡單地繼承這個基類並以標準化的方式在其上實現新方法來建立script新任務。
- `EvAdventureQuestHandler` 將作為 `character.quests` 坐在每個角色上。它將儲存角色正在或已經參與的所有 `EvAdventureQuest`s。它也負責使用角色上的[屬性](../../../Components/Attributes.md) 來儲存任務狀態。

(the-quest-handler)=
## 工作人員

> 建立一個新模組`evadventure/quests.py`。

我們在[有關 NPC 和怪物 AI 的課程](./Beginner-Tutorial-AI.md#the-aihandler)（`AIHandler`）中看到了物件處理程式的實作。

```{code-block} python
:linenos: 
:emphasize-lines: 9,10,13-17,20,23-27
# in evadventure/quests.py

class EvAdventureQuestHandler:
    quest_storage_attribute_key = "_quests"
    quest_storage_attribute_category = "evadventure"

    def __init__(self, obj):
        self.obj = obj
        self.quest_classes = {}
        self.quests = {}
        self._load()

    def _load(self):
        self.quest_classes = self.obj.attributes.get(
            self.quest_storage_attribute_key,
            category=self.quest_storage_attribute_category,
            default={},
        )
        # instantiate all quests
        for quest_key, quest_class in self.quest_classes.items():
            self.quests[quest_key] = quest_class(self.obj, questhandler=self)

    def _save(self):
        self.obj.attributes.add(
            self.quest_storage_attribute_key,
            self.quest_classes,
            category=self.quest_storage_attribute_category,
        )
    
    def get(self, quest_key):
        return self.quests.get(quest_key)

    def all(self):
        return list(self.quests.values())

    def add(self, quest_class):
        self.quest_classes[quest_class.key] = quest_class
        self.quests[quest_class.key] = quest_class(self.obj, questhandler=self)
        self._save()

    def remove(self, quest_key):
        quest = self.quests.pop(quest_key, None)
        self.quest_classes.pop(quest_key, None)
        self.quests.pop(quest_key, None)
        self._save()

```

```{sidebar} 持久處理程式模式
持久處理程式在 Evennia 中普遍使用。您可以在[製作永續性物件處理程式](../../Tutorial-Persistent-Handler.md)教學中閱讀有關它們的更多資訊。
```
- **第 9 行**：我們知道任務本身將是繼承自 `EvAdventureQuest`（我們尚未建立）的 Python 類別。我們將這些類別儲存在處理程式的 `self.quest_classes` 中。請注意，類別和類別的_例項_之間是有區別的！該類別本身無法儲存任何狀態，例如該任務的狀態是針對該特定角色的。該類別僅包含 python 程式碼。
- **第 10 行**：我們在處理程式上預留另一個屬性 - `self.quest` 這是將儲存 `EvAdventureQuest` _instances_ 的字典。
- **第 11 行**：請注意，我們在這裡呼叫 `self._load()` 方法，每當訪問此處理程式時，都會從資料庫載入資料。
- **第 14-18 行**：我們使用 `self.obj.attributes.get` 來取得名為 `_quests` 且類別為 `evadventure` 的角色上的 [Attribute](../../../Components/Attributes.md)。如果它還不存在（因為我們從未開始任何任務），我們只會回傳一個空字典。
- **第 21 行**：這裡我們迴圈所有類別並例項化它們。我們還沒有定義這些任務類的外觀，但是透過用 `self.obj` （角色）例項化它們，我們應該被覆蓋 - 從角色類，任務將能夠訪問其他所有內容（畢竟，這個處理程式本身可以從該任務例項作為 `obj.quests` 訪問）。
- **第24行**：這裡我們進行對應的儲存操作。

處理程式的其餘部分只是用於從處理程式取得、新增和刪除任務的存取方法。我們在這些程式碼中做出一個假設，即任務類別有一個屬性 `.key` 作為唯一的任務名稱。

這就是它在實踐中的使用方式：

```python 
# in some questing code 

from evennia import search_object
from evadventure import quests 

class EvAdventureSuperQuest(quests.EvAdventureQuest):
    key = "superquest"
    # quest implementation here

def start_super_quest(character):
    character.quests.add(EvAdventureSuperQuest)

```
```{sidebar} 屬性中可以儲存什麼？
有關更多詳細資訊，請參閱有關此事的[屬性檔案](../../../Components/Attributes.md#what-types-of-data-can-i-save-in-an-attribute)。
```
我們選擇儲存類別而不是上面類別的例項。這樣做的原因與資料庫中可以儲存的內容有關`Attribute` - Attribute 的一個限制是我們無法儲存類別例項_與其中烘焙的其他資料庫實體_。如果我們按原樣儲存任務例項，它們很可能會包含「隱藏」在其中的資料庫實體 - 對角色的引用，可能是完成任務所需的物件等。 Evennia 將無法嘗試儲存該資料。 
相反，我們只儲存類，用角色例項化這些類，並讓任務單獨儲存其狀態標誌，如下所示：

```python 
# in evadventure/quests.py 

class EvAdventureQuestHandler: 

    # ... 
    quest_data_attribute_template = "_quest_data_{quest_key}"
    quest_data_attribute_category = "evadventure"

    # ... 

    def save_quest_data(self, quest_key):
        quest = self.get(quest_key)
        if quest:
            self.obj.attributes.add(
                self.quest_data_attribute_template.format(quest_key=quest_key),
                quest.data,
                category=self.quest_data_attribute_category,
            )

    def load_quest_data(self, quest_key):
        return self.obj.attributes.get(
            self.quest_data_attribute_template.format(quest_key=quest_key),
            category=self.quest_data_attribute_category,
            default={},
        )

```

這與 `_load` 和 `_save` 方法的工作方式相同，不同之處在於它會取得任務例項上的屬性 `.data`（這將是 `dict`）並儲存它。只要我們確保在 `.data` 屬性發生更改時從任務中呼叫這些方法，一切都會好起來 - 這是因為屬性知道如何正確分析 `dict` 以查詢並安全地序列化其中找到的任何資料庫實體。

我們的處理程式已準備就緒。我們在 [角色課程](./Beginner-Tutorial-Characters.md) 中建立了 `EvAdventureCharacter` 類別 - 讓我們為它新增任務支援。

```python
# in evadventure/characters.py

# ...

from evennia.utils import lazy_property
from evadventure.quests import EvAdventureQuestHandler

class EvAdventureCharacter(LivingMixin, DefaultCharacter): 
    # ...

    @lazy_property
    def quests(self): 
        return EvAdventureQuestHandler(self)

    # ...

```

不過，我們還需要一種方法來代表任務本身！
(the-quest-class)=
## 探索類


```{code-block} python
:linenos:
:emphasize-lines: 7,10-14,17,24,31
# in evadventure/quests.py

# ...

class EvAdventureQuest:

    key = "base-quest"
    desc = "Base quest"
    start_step = "start"

    def __init__(self, quester, questhandler=None):
        self.quester = quester
        self._questhandler = questhandler
        self.data = self.questhandler.load_quest_data(self.key)
        self._current_step = self.get_data("current_step")

        if not self.current_step:
            self.current_step = self.start_step

    def add_data(self, key, value):
        self.data[key] = value
        self.questhandler.save_quest_data(self.key)

    def get_data(self, key, default=None):
        return self.data.get(key, default)

    def remove_data(self, key):
        self.data.pop(key, None)
        self.questhandler.save_quest_data(self.key)
    
    @property
    def questhandler(self):
        return self._questhandler if self._questhandler else self.quester.quests

    @property
    def current_step(self):
        return self._current_step

    @current_step.setter
    def current_step(self, step_name):
        self._current_step = step_name
        self.add_data("current_step", step_name)

```

- **第 7 行**：每個類別必須有一個 `.key` 屬性來唯一標識任務。我們在任務處理程式中依賴於此。
- **第 12 行**：`quester`（角色）在 `EvAdventureQuestHandler._load()` 內部啟動時傳遞到該類別。
- **第13行**：handler也是在載入時傳入的，所以這個任務例項可以直接使用它，而不會在延遲載入時觸發遞迴。
- **第 17、24 和 31 行**：`add_data` 和 `remove_data` 回撥到 `questhandler.save_quest_data`，因此永續性發生在一個地方。

`add/get/remove_data` 方法是用於將資料傳入和傳出資料庫的便捷包裝器。當我們實現一個任務時，我們應該更喜歡使用 `.get_data`、`add_data` 和 `remove_data` 而不是直接操作 `.data`，因為前者會確保自動將所述內容儲存到資料庫中。

`current_step` 追蹤我們目前所處的任務「步驟」；這意味著什麼取決於每個任務。我們設定了方便的屬性來設定`current_state`，並確保將其儲存在資料字典中為「current_step」。

任務可以有幾種可能的狀態：「開始」、「完成」、「放棄」和「失敗」。我們建立了一些屬性和方法來輕鬆控制它，同時儲存所有內容：

```python
# in evadventure/quests.py

# ... 

class EvAdventureQuest:

    # ... 

    @property
    def status(self):
        return self.get_data("status", "started")

    @status.setter
    def status(self, value):
        self.add_data("status", value)

    @property
    def is_completed(self):
        return self.status == "completed"

    @property
    def is_abandoned(self):
        return self.status == "abandoned"

    @property
    def is_failed(self):
        return self.status == "failed"

    def complete(self):
        self.status = "completed"

    def abandon(self):
        self.status = "abandoned"

    def fail(self):
        self.status = "failed"


```

到目前為止，我們僅新增了用於檢查狀態的便利功能。這項工作的實際「任務」方面將如何進行？

當系統想要檢查任務的進度時，會發生什麼，它會呼叫此類的方法`.progress()`。同樣，要獲取當前步驟的幫助，它將呼叫方法`.help()`

```python

    start_step = "start"

    # help entries for quests (could also be methods)
    help_start = "You need to start first"
    help_end = "You need to end the quest"

    def progress(self, *args, **kwargs):
        getattr(self, f"step_{self.current_step}")(*args, **kwargs)

    def help(self, *args, **kwargs):
        if self.status in ("abandoned", "completed", "failed"):
            help_resource = getattr(self, f"help_{self.status}",
                                    f"You have {self.status} this quest.")
        else:
            help_resource = getattr(self, f"help_{self.current_step}", "No help available.")

        if callable(help_resource):
            # the help_* methods can be used to dynamically generate help
            return help_resource(*args, **kwargs)
        else:
            # normally it's just a string
            return str(help_resource)

```

```{sidebar} *args、**kwargs 是怎麼回事？
這些是可選的，但允許您將額外的資訊傳遞到任務檢查中。如果您想要新增額外的上下文來確定任務步驟目前是否完成，這可能非常強大。
```
呼叫 `.progress(*args, **kwargs)` 方法將呼叫此類上名為 `step_<current_step>(*args, **kwargs)` 的方法。也就是說，如果我們處於 _start_ 步驟，則呼叫的方法將為 `self.step_start(*args, **kwargs)`。這個方法在哪裡呢？還沒實施！事實上，我們需要為每個任務實現這樣的方法。只需新增正確新增的方法，我們就可以輕鬆地為任務新增更多步驟。

同樣，呼叫 `.help(*args, **kwargs)` 將嘗試尋找屬性 `help_<current_step>`。如果這是可呼叫的，則它將被呼叫，例如 `self.help_start(*args, **kwargs)`。如果它以字串形式給出，則該字串將按原樣返回，並且 `*args, **kwargs` 將被忽略。

(example-quest)=
### 範例任務

```python
# in some quest module, like world/myquests.py

from evadventure.quests import EvAdventureQuest 

class ShortQuest(EvAdventureQuest): 

    key = "simple-quest"
    desc = "A very simple quest."

    def step_start(self, *args, **kwargs): 
        """Example step!"""
        self.quester.msg("Quest started!")
        self.current_step = "end"

    def step_end(self, *args, **kwargs): 
        if not self.is_completed:
            self.quester.msg("Quest ended!")
            self.complete()

```

這是一個非常簡單的任務，在兩次 `.progress()` 檢查後將自行解決。這是此任務的完整生命週期：

```python 
# in some module somewhere, using evennia shell or in-game using py

from evennia import search_object 
from world.myquests import ShortQuest 

character = search_object("MyCharacterName")[0]
character.quests.add(ShortQuest)

# this will echo "Quest started!" to character
character.quests.get("short-quest").progress()                     
# this will echo "Quest ended!" to character
character.quests.get("short-quest").progress()

```

(a-useful-command)=
### 一個有用的指令

玩家必須知道他們有哪些任務並能夠檢查它們。這是一個簡單的 `quests` 指令來處理這個問題：

```python
# in evadventure/quests.py

class CmdQuests(Command):
    """
    List all quests and their statuses as well as get info about the status of
    a specific quest.

    Usage:
        quests
        quest <questname>

    """
    key = "quests"
    aliases = ["quest"]

    def parse(self):
        self.quest_name = self.args.strip()

    def func(self):
        if self.quest_name:
            quest = self.caller.quests.get(self.quest_name)
            if not quest:
                self.msg(f"Quest {self.quest_name} not found.")
                return
            self.msg(f"Quest {quest.key}: {quest.status}\n{quest.help()}")
            return

        quests = self.caller.quests.all()
        if not quests:
            self.msg("No quests.")
            return

        for quest in quests:
            self.msg(f"Quest {quest.key}: {quest.status}")
```

將其新增到 `mygame/commands/default_cmdsets.py` 中的 `CharacterCmdSet`。如果您不確定如何執行此操作，請按照[新增指令課程](../Part1/Beginner-Tutorial-Adding-Commands.md#add-the-echo-command-to-the-default-cmdset) 進行操作。重新載入，如果您以 `EvAdventureCharacter` 身份玩遊戲，您應該能夠使用 `quests` 檢視您的任務。

(testing)=
## 測試

> 建立一個新資料夾`evadventure/tests/test_quests.py`。

```{sidebar} 
任務測試套件範例位於 `evennia/contrib/tutorials/evadventure`，如 [tests/test_quests.py](evennia.contrib.tutorials.evadventure.tests.test_quests)。
```
任務測試意味著建立一個測試角色，製作一個虛擬任務，將其新增到角色的任務處理程式中，並確保所有方法都能正確工作。建立測試任務，以便在呼叫 `.progress()` 時自動前進，這樣您就可以確保它按預期工作。

(conclusions)=
## 結論

我們在這裡建立的只是探索的框架。實際的複雜性將在建立任務本身（即實現 `step_<current_step>(*args, **kwargs)` 方法）時出現，這是我們稍後將在本教學的[第 4 部分](../Part4/Beginner-Tutorial-Part4-Overview.md) 中介紹的內容。
