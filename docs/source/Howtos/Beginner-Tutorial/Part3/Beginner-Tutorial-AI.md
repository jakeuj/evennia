(npc-and-monster-ai)=
# NPC和怪物AI

```{sidebar} 人工智慧聽起來很複雜
「人工智慧」這個詞聽起來令人畏懼。它讓人想起超級電腦、機器學習、神經網路和大型語言模型。不過，對於我們的用例，您只需使用一些 if 語句就可以獲得感覺非常「聰明」的東西。
```
並非遊戲中的每個實體都由玩家控制。 NPCs而敵人需要由電腦控制－也就是說，我們需要賦予他們人工智慧（AI）。

對於我們的遊戲，我們將實現一種稱為「狀態機」的 AI 型別。這意味著實體（如 NPC 或生物）始終處於給定的「狀態」。狀態的範例可以是「空閒」、「漫遊」或「攻擊」。 
每隔一段時間，AI 實體將被「勾選」Evennia。這個「勾選」從一個評估開始，該評估確定實體是否應該切換到另一個狀態，或停留在目前狀態內並執行一個（或多個）操作。

```{sidebar} 生物和NPC
「Mob」是「Mobile」的縮寫，是一個常見的 MUD 術語，表示可以在房間之間移動的實體。該術語通常用於攻擊性的敵人。暴民也是「NPC」（非玩家角色），但後一個術語通常用於更和平的實體，例如店主和任務提供者。
```

例如，如果處於「漫遊」狀態的生物遇到玩家角色，它可能會切換到「攻擊」狀態。在戰鬥中，它可以在不同的戰鬥行動之間移動，如果它在戰鬥中倖存下來，它會回到「漫遊」狀態。

根據遊戲的運作方式，AI 可以在不同的時間尺度上「勾選」。例如，當生物移動時，它們可能每 20 秒自動從一個房間移動到另一個房間。但是一旦進入回合製戰鬥（如果你使用它），AI 只會在每個回合中「滴答」。

(our-requirements)=
## 我們的要求

```{sidebar} 店主和任務提供者
NPC 在我們的遊戲中，店主和任務提供者將被假定始終處於「空閒」狀態 - 與他們交談或向他們購物的功能將在以後的課程中探討。
```

對於本教學遊戲，我們需要 AI 實體才能處於以下狀態：

- _閒置_ - 什麼都不做，只是站在旁邊。
- _漫遊_ - 從一個房間移動到另一個房間。重要的是，我們增加了限制 AI 可以漫遊到的位置的功能。例如，如果我們有非戰鬥區域，我們希望能夠[lock](../../../Components/Locks.md)通往這些區域的所有出口，這樣侵略性的模組就不會走進它們。
- _戰鬥_ - 啟動並與電腦進行戰鬥。此狀態將利用[戰鬥教學](./Beginner-Tutorial-Combat-Base.md)隨機選擇戰鬥動作(回合製或滴答式)。
- _Flee_ - 這就像_Roam_，除了 AI 會移動以避免進入有電腦的房間（如果可能的話）。

我們將這樣組織 AI 程式碼：
- `AIHandler` 這將是在 AI 實體上儲存為 `.ai` 的處理程式。它負責儲存AI的狀態。為了「勾選」AI，我們執行`.ai.run()`。我們多久以這種方式轉動 AI 的輪子，我們就留給其他遊戲系統。
- NPC/Mob 類別上的 `.ai_<state_name>` 方法 - 當呼叫 `ai.run()` 方法時，它負責尋找與其目前狀態類似的方法（e.g。`.ai_combat` 如果我們處於 _combat_ 狀態）。擁有這樣的方法可以輕鬆新增新狀態 - 只需新增一個適當命名的新方法，AI 現在就知道如何處理該狀態！

(the-aihandler)=
## AIHandler

```{{sidebar}}
You can find an AIHandler implemented in `evennia/contrib/tutorials`, in [evadventure/tests/test_ai.py](evennia.contrib.tutorials.evadventure.ai)
```
這是管理AI狀態的核心邏輯。建立一個新檔案`evadventure/ai.py`。

> 建立一個新檔案`evadventure/ai.py`。

```{code-block} python
:linenos: 
:emphasize-lines: 10,11-13,16,23
# in evadventure/ai.py

from evennia.logger import log_trace

class AIHandler:
    attribute_name = "ai_state"
    attribute_category = "ai_state"

    def __init__(self, obj):
        self.obj = obj
        self.ai_state = obj.attributes.get(self.attribute_name,
                                           category=self.attribute_category,
                                           default="idle")
    def set_state(self, state):
        self.ai_state = state
        self.obj.attributes.add(self.attribute_name, state, category=self.attribute_category)

    def get_state(self):
        return self.ai_state

    def run(self):
        try:
            state = self.get_state()
            getattr(self.obj, f"ai_{state}")()
        except Exception:
            log_trace(f"AI error in {self.obj.name} (running state: {state})")


```

AIHandler 是[物件處理程式](../../Tutorial-Persistent-Handler.md) 的範例。這是一種將所有功能組合在一起的設計風格。稍微向前看一下，這個處理程式將會被加入到物件中，如下所示：
```{sidebar} lazy_property
這是一個 Evennia [@decorator](https://realpython.com/primer-on-python-decorators/)，它使得處理程式在有人真正第一次嘗試訪問 `obj.ai` 之前不會被初始化。在後續呼叫中，將傳回已初始化的處理程式。當您有很多物件時，這是非常有用的效能最佳化，並且對於處理程式的功能也很重要。
```

```python
# just an example, don't put this anywhere yet

from evennia.utils import lazy_property
from evadventure.ai import AIHandler 

class MyMob(SomeParent): 

    @lazy_property
    class ai(self): 
        return AIHandler(self)
```

簡而言之，存取 `.ai` 屬性將初始化 `AIHandler` 的例項，我們將 `self` （目前物件）傳遞給該例項。在 `AIHandler.__init__` 中，我們取得此輸入並將其儲存為 `self.obj`（**第 10-13 行**）。這樣，處理程式始終可以透過存取 `self.obj` 對其「所在」的實體進行操作。  `lazy_property` 確保每次伺服器重新載入時此初始化僅發生一次。

更多關鍵功能：

- **第 11 行**：我們透過造訪 `self.obj.attributes.get()`（重新）載入 AI 狀態。這將載入具有給定名稱和類別的資料庫 [Attribute](../../../Components/Attributes.md)。如果尚未儲存，則傳回「idle」。請注意，我們必須訪問 `self.obj`（NPC/mob），因為這是唯一可以存取資料庫的東西。
- **第 16 行**：在 `set_state` 方法中，我們強制處理程式切換到給定狀態。當我們這樣做時，我們確保將其也儲存到資料庫中，以便其狀態在重新載入後仍然存在。但我們也將其儲存在 `self.ai_state` 中，因此我們不需要在每次獲取時都存取資料庫。
- **第 23 行**：`getattr` 函式是一個內建的 Python 函式，用於取得物件的命名屬性。這允許我們根據當前狀態呼叫NPC/mob 上定義的方法`ai_<statename>`。我們必須將此呼叫包裝在 `try...except` 區塊中才能正確處理 AI 方法中的錯誤。 Evennia 的 `log_trace` 將確保記錄錯誤，包括其偵錯回溯。

(more-helpers-on-the-ai-handler)=
### AI 處理程式上有更多幫助程式

在AIHandler上放幾個助手也很方便。這使得它們可以從 `ai_<state>` 方法內部輕鬆使用，可作為 e.g 呼叫。 `self.ai.get_targets()`。

```{code-block} python
:linenos:
:emphasize-lines: 41,42,47,49
# in evadventure/ai.py 

# ... 
import random

class AIHandler:

    # ...

    def get_targets(self):
        """
        Get a list of potential targets for the NPC to combat.

        """
        return [obj for obj in self.obj.location.contents if hasattr(obj, "is_pc") and obj.is_pc]

    def get_traversable_exits(self, exclude_destination=None):
        """
        Get a list of exits that the NPC can traverse. Optionally exclude a destination.
        
        Args:
            exclude_destination (Object, optional): Exclude exits with this destination.

        """
        return [
            exi
            for exi in self.obj.location.exits
            if exi.destination != exclude_destination and exi.access(self, "traverse")
        ]
    
    def random_probability(self, probabilities):
        """
        Given a dictionary of probabilities, return the key of the chosen probability.

        Args:
            probabilities (dict): A dictionary of probabilities, where the key is the action and the
                value is the probability of that action.

        """
        # sort probabilities from higheest to lowest, making sure to normalize them 0..1
        prob_total = sum(probabilities.values())
        sorted_probs = sorted(
            ((key, prob / prob_total) for key, prob in probabilities.items()),
            key=lambda x: x[1],
            reverse=True,
        )
        rand = random.random()
        total = 0
        for key, prob in sorted_probs:
            total += prob
            if rand <= total:
                return key
```

```{sidebar} 鎖定出口
「遍歷」lock 是預設的 lock 型別，在允許某些東西透過出口之前由 Evennia 檢查。由於只有 PC 具有 `is_pc` 屬性，因此我們可以 lock 向下退出以_僅_允許具有該屬性的實體透過。

遊戲中：

    lock north = traverse:attr(is_pc, True)

或在程式碼中：

    exit_obj.locks.add(
        "traverse:attr(is_pc, True)")

有關 Evennia 鎖的更多資訊，請參閱[鎖](../../../Components/Locks.md)。
```
- `get_targets` 檢查是否有任何其他物件與在其 typeclass 上設定的 `is_pc` 屬性位於相同位置。為簡單起見，我們假設怪物只會攻擊 PC（沒有怪物內鬥！）。
- `get_traversable_exits` 從目前位置取得所有有效出口，不包括具有提供的目的地的出口或未透過「遍歷」訪問檢查的出口。
- `get_random_probability` 採用字典 `{action: probability,...}`。這將隨機選擇一個動作，但機率越高，它被選中的可能性就越大。稍後我們將在戰鬥狀態中使用它，以允許不同的戰鬥人員或多或少地執行不同的戰鬥動作。該演演算法使用了一些有用的 Python 工具：
    - **第 41 行**：記住 `probabilities` 是 `dict` `{key: value,...}`，其中值是機率。因此 `probabilities.values()` 為我們提供了僅包含機率的清單。對它們執行 `sum()` 可以得到這些機率的總和。我們需要它來標準化下面一行中 0 到 1.0 之間的所有機率。
    - **第 42-46 行**：這裡我們建立一個新的元組可迭代`(key, prob/prob_total)`。我們使用 Python `sorted` 幫助器對它們進行排序。 `key=lambda x: x[1]` 意味著我們對每個元組的第二個元素（機率）進行排序。 `reverse=True` 意味著我們將從最高機率到最低機率排序。
    - **第 47 行**：`random.random()` 呼叫產生一個 0 到 1 之間的隨機值。
    - **第 49 行**：由於機率是從最高到最低排序的，因此我們迴圈遍歷它們，直到找到第一個適合隨機值的機率 - 這就是我們正在尋找的操作/鍵。
    - 舉個例子，如果你有一個`{"attack": 0.5, "defend": 0.1, "idle": 0.4}`的`probability`輸入，這將變成一個排序的可迭代`(("attack", 0.5), ("idle", 0.4), ("defend": 0.1))`，如果`random.random()`返回0.65，結果將是「空閒」。如果`random.random()`回傳`0.90`，那就是「防禦」。  也就是說，這個AI實體會在50%的時間攻擊，40%的時間閒置，10%的時間防禦。


(adding-ai-to-an-entity)=
## 將 AI 新增至實體

我們需要向遊戲實體新增 AI- 支援，只需將 AI 處理程式和一堆 `.ai_statename()` 方法新增到該物件的 typeclass 上。

我們已經在 [NPC 教學](Beginner-Tutorial_NPCs) 中勾畫出了 NPCs 和 Mob typeclasses。開啟 `evadventure/npcs.py` 並展開迄今為止空的 `EvAdventureMob` 類。

```python
# in evadventure/npcs.py 

# ... 

from evennia.utils import lazy_property 
from .ai import AIHandler

# ... 

class EvAdventureMob(EvAdventureNPC):

    @lazy_property
    def ai(self): 
        return AIHandler(self)

    def ai_idle(self): 
        pass 

    def ai_roam(self): 
        pass 

    def ai_roam(self): 
        pass 

    def ai_combat(self): 
        pass 

    def ai_flee(self):
        pass

```

所有剩餘的邏輯將進入每個狀態方法。

(idle-state)=
### 空閒狀態

在空閒狀態下，生物不執行任何操作，因此我們將 `ai_idle` 方法保留原樣 - 其中只有一個空的 `pass` 。這意味著它也不會攻擊同一個房間內的PC - 但如果PC攻擊它，我們必須確保強制它進入戰鬥狀態（否則它將毫無防禦能力）。

(roam-state)=
### 漫遊狀態

在這種狀態下，生物應該從一個房間移動到另一個房間，直到找到要攻擊的電腦。

```python
# in evadventure/npcs.py

# ... 

import random

class EvAdventureMob(EvAdventureNPC): 

    # ... 

    def ai_roam(self):
        """
        roam, moving randomly to a new room. If a target is found, switch to combat state.

        """
        if targets := self.ai.get_targets():
            self.ai.set_state("combat")
            self.execute_cmd(f"attack {random.choice(targets).key}")
        else:
            exits = self.ai.get_traversable_exits()
            if exits:
                exi = random.choice(exits)
                self.execute_cmd(f"{exi.key}")
```

每次勾選AI時，都會呼叫該方法。它將首先檢查房間中是否有任何有效目標（使用我們在 `AIHandler` 上製作的 `get_targets()` 助手）。如果是這樣，我們切換到`combat`狀態並立即呼叫`attack`指令來發起/加入戰鬥（請參閱[戰鬥教學](./Beginner-Tutorial-Combat-Base.md)）。

如果未找到目標，我們將獲得可遍歷出口的清單（未透過 `traverse` lock 檢查的出口已從該清單中排除）。使用 Python 的內建 `random.choice` 函式，我們從該列表中隨機取得一個出口，並按其名稱在其中移動。

(flee-state)=
### 逃離狀態

逃跑與_Roam_類似，除了AI從不嘗試攻擊任何東西，並且會確保不按原路返回。

```python
# in evadventure/npcs.py

# ... 

class EvAdventureMob(EvAdventureNPC):

    # ... 

    def ai_flee(self):
        """
        Flee from the current room, avoiding going back to the room from which we came. If no exits
        are found, switch to roam state.

        """
        current_room = self.location
        past_room = self.attributes.get("past_room", category="ai_state", default=None)
        exits = self.ai.get_traversable_exits(exclude_destination=past_room)
        if exits:
            self.attributes.set("past_room", current_room, category="ai_state")
            exi = random.choice(exits)
            self.execute_cmd(f"{exi.key}")
        else:
            # if in a dead end, roam will allow for backing out
            self.ai.set_state("roam")

```

我們將 `past_room` 儲存在我們自己的 Attribute「past_room」中，並確保在嘗試找到要遍歷的隨機出口時排除它。

如果我們最終陷入死衚衕，我們會切換到_漫遊_模式，以便它可以退出（並再次開始攻擊事物）。因此，這樣做的效果是，暴民會在「平靜下來」之前在恐懼中逃得盡可能遠。

(combat-state)=
### 戰鬥狀態

在戰鬥狀態下，生物將使用我們設計的戰鬥系統之一（[基於抽搐的戰鬥](./Beginner-Tutorial-Combat-Twitch.md) 或 [回合製戰鬥](./Beginner-Tutorial-Combat-Turnbased.md)）。這意味著每次 AI 滴答時，並且我們處於戰鬥狀態，該實體需要執行可用的戰鬥動作之一，_hold_、_attack_、_do a 特技_、_use an item_ 或_flee_。

```{code-block} python
:linenos: 
:emphasize-lines: 7,22,24,25
# in evadventure/npcs.py 

# ... 

class EvAdventureMob(EvAdventureNPC): 

    combat_probabilities = {
        "hold": 0.0,
        "attack": 0.85,
        "stunt": 0.05,
        "item": 0.0,
        "flee": 0.05,
    }

    # ... 

    def ai_combat(self):
        """
        Manage the combat/combat state of the mob.

        """
        if combathandler := self.nbd.combathandler:
            # already in combat
            allies, enemies = combathandler.get_sides(self)
            action = self.ai.random_probability(self.combat_probabilities)

            match action:
                case "hold":
                    combathandler.queue_action({"key": "hold"})
                case "combat":
                    combathandler.queue_action({"key": "attack", "target": random.choice(enemies)})
                case "stunt":
                    # choose a random ally to help
                    combathandler.queue_action(
                        {
                            "key": "stunt",
                            "recipient": random.choice(allies),
                            "advantage": True,
                            "stunt": Ability.STR,
                            "defense": Ability.DEX,
                        }
                    )
                case "item":
                    # use a random item on a random ally
                    target = random.choice(allies)
                    valid_items = [item for item in self.contents if item.at_pre_use(self, target)]
                    combathandler.queue_action(
                        {"key": "item", "item": random.choice(valid_items), "target": target}
                    )
                case "flee":
                    self.ai.set_state("flee")

        elif not (targets := self.ai.get_targets()):
            self.ai.set_state("roam")
        else:
            target = random.choice(targets)
            self.execute_cmd(f"attack {target.key}")

```

- **第 7-13 行**：該指令描述了生物執行給定戰鬥動作的可能性。透過修改這個字典，我們可以輕鬆地建立行為非常不同的生物，例如更多地使用物品或更容易逃跑。您也可以完全關閉某些操作 - 預設情況下，他的暴徒從不「持有」或「使用物品」。
- **第 22 行**：如果我們處於戰鬥狀態，則應在我們身上初始化 `CombadHandler`，可用作 `self.ndb.combathandler`（請參閱 [基礎戰鬥教學](./Beginner-Tutorial-Combat-Base.md)）。
- **第 24 行**：`combathandler.get_sides()` 為傳遞給它的人生成盟友和敵人。
- **第 25 行**：現在我們在本課前面建立的 `random_probability` 方法變得很方便！

此方法的其餘部分僅採用隨機選擇的操作並執行所需的操作，以將其作為具有 `CombatHandler` 的新操作進行排隊。  為簡單起見，我們僅使用特技來增強我們的盟友，而不是阻礙我們的敵人。

最後，如果我們目前沒有處於戰鬥狀態並且附近沒有敵人，我們就會切換到漫遊 - 否則我們會開始另一場戰鬥！

(unit-testing)=
## 單元測試

```{{sidebar}}
Find an example of AI tests in [evennia/contrib/tutorials/tests/test_ai.py](evennia.contrib.tutorials.evadventure.tests.test_ai).
```
> 建立一個新檔案`evadventure/tests/test_ai.py`。

如果您遵循了先前的課程，那麼測試 AI 處理程式和生物會很簡單。建立一個 `EvAdventureMob` 並測試呼叫其上的各種與 ai 相關的方法和處理程式是否如預期運作。複雜之處在於模擬 `random` 的輸出，以便您始終獲得相同的隨機結果進行比較。我們將 AI 測驗的實作留給讀者作為額外的練習。

(conclusions)=
## 結論

您可以輕鬆擴充套件這個簡單的系統，使生物變得更加「聰明」。例如，暴民不只是隨機決定在戰鬥中採取哪種行動，而是可以考慮更多因素 - 也許一些支援暴徒可以使用特技為他們的重擊者鋪平道路，或者在嚴重受傷時使用生命藥水。

新增“狩獵”狀態也很簡單，小怪在移動到那裡之前會檢查相鄰房間的目標。

雖然實現功能性遊戲 AI 系統不需要高階數學或機器學習技術，但如果您真的願意，您可以新增什麼樣的高階東西當然是沒有限制的！

