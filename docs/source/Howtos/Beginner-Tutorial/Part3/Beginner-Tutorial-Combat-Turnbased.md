(turnbased-combat)=
# 回合製戰鬥

在本課程中，我們將在[戰鬥基礎](./Beginner-Tutorial-Combat-Base.md) 的基礎上實現一個輪流執行的戰鬥系統，您可以在選單中選擇操作，如下所示：

```shell

> attack Troll
______________________________________________________________________________

 You (Perfect)  vs  Troll (Perfect)
 Your queued action: [attack] (22s until next round,
 or until all combatants have chosen their next action).
______________________________________________________________________________

 1: attack an enemy
 2: Stunt - gain a later advantage against a target
 3: Stunt - give an enemy disadvantage against yourself or an ally
 4: Use an item on yourself or an ally
 5: Use an item on an enemy
 6: Wield/swap with an item from inventory
 7: flee!
 8: hold, doing nothing

> 4
_______________________________________________________________________________

Select the item
_______________________________________________________________________________

 1: Potion of Strength
 2. Potion of Dexterity
 3. Green Apple
 4. Throwing Daggers
 back
 abort

> 1
_______________________________________________________________________________

Choose an ally to target.
_______________________________________________________________________________

 1: Yourself
 back
 abort

> 1
_______________________________________________________________________________

 You (Perfect)  vs Troll (Perfect)
 Your queued action: [use] (6s until next round,
 or until all combatants have chosen their next action).
_______________________________________________________________________________

 1: attack an enemy
 2: Stunt - gain a later advantage against a target
 3: Stunt - give an enemy disadvantage against yourself or an ally
 4: Use an item on yourself or an ally
 5: Use an item on an enemy
 6: Wield/swap with an item from inventory
 7: flee!
 8: hold, doing nothing

Troll attacks You with Claws: Roll vs armor (12):
 rolled 4 on d20 + strength(+3) vs 12 -> Fail
 Troll missed you.

You use Potion of Strength.
 Renewed strength coarses through your body!
 Potion of Strength was used up.
```
> 請注意，本文件不顯示遊戲中的顏色。另外，如果您對替代方案感興趣，請參閱[上一課](./Beginner-Tutorial-Combat-Twitch.md)，其中我們透過為每個動作輸入直接指令來實現類似「抽搐」的戰鬥系統。

對於「回合製」戰鬥，我們指的是以較慢的速度「滴答作響」的戰鬥，速度足夠慢，足以讓參與者在選單中選擇他們的選項（選單並不是絕對必要的，但它也是學習如何製作選單的好方法）。他們的行動會排隊，並在回合計時器用完時執行。為了避免不必要的等待，當大家做出選擇後，我們也會進入下一輪。

回合製系統的優點是它消除了玩家的速度。你的戰鬥能力並不取決於你輸入指令的速度。對於 RPG- 重型遊戲，您還可以讓玩家有時間在戰鬥回合中做出 RP 表情，以充實動作。

使用選單的優點是您可以直接執行所有可能的操作，這使得初學者友好且易於知道您可以做什麼。這也意味著更少的寫作，這對某些玩家來說可能是一個優勢。

(general-principle)=
## 一般原則

```{sidebar}
已實施的回合製戰鬥系統的範例可以在 `evennia/contrib/tutorials/evadventure/` 下的 [combat_turnbased.py](evennia.contrib.tutorials.evadventure.combat_turnbased) 中找到。
```
以下是回合製戰鬥處理程式的一般原理：

- CombatHandler 的回合製版本將儲存在_目前位置_。這意味著每個地點只會發生一場戰鬥。任何其他開始戰鬥的人都會加入同一個處理者並被分配到一邊戰鬥。
- 處理程式將執行 30 秒的中央計時器（在本例中）。當它觸發時，所有排隊的操作都將被執行。如果每個人都提交了他們的操作，那麼這將在最後一個提交時立即發生。
- 在戰鬥中你將無法走動——你被困在房間裡。逃離戰鬥是一個單獨的動作，需要幾個回合才能完成（我們需要建立這個）。
- 開始戰鬥是透過`attack <target>`指令完成的。之後，您將進入戰鬥選單，並將使用該選單執行所有後續操作。

(turnbased-combat-handler)=
## 回合製戰鬥處理程式

> 建立一個新模組`evadventure/combat_turnbased.py`。

```python
# in evadventure/combat_turnbased.py

from .combat_base import (
   CombatActionAttack,
   CombatActionHold,
   CombatActionStunt,
   CombatActionUseItem,
   CombatActionWield,
   EvAdventureCombatBaseHandler,
)

from .combat_base import EvAdventureCombatBaseHandler

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    action_classes = {
        "hold": CombatActionHold,
        "attack": CombatActionAttack,
        "stunt": CombatActionStunt,
        "use": CombatActionUseItem,
        "wield": CombatActionWield,
        "flee": None # we will add this soon!
    }

    # fallback action if not selecting anything
    fallback_action_dict = AttributeProperty({"key": "hold"}, autocreate=False)

	# track which turn we are on
    turn = AttributeProperty(0)
    # who is involved in combat, and their queued action
    # as {combatant: actiondict, ...}
    combatants = AttributeProperty(dict)

    # who has advantage against whom. This is a structure
    # like {"combatant": {enemy1: True, enemy2: True}}
    advantage_matrix = AttributeProperty(defaultdict(dict))
    # same for disadvantages
    disadvantage_matrix = AttributeProperty(defaultdict(dict))

    # how many turns you must be fleeing before escaping
    flee_timeout = AttributeProperty(1, autocreate=False)

	# track who is fleeing as {combatant: turn_they_started_fleeing}
    fleeing_combatants = AttributeProperty(dict)

    # list of who has been defeated so far
    defeated_combatants = AttributeProperty(list)

```

我們為 `"flee"` 操作留下一個佔位符，因為我們還沒有建立它。

由於回合製戰鬥處理程式在所有戰鬥人員之間共享，因此我們需要在處理程式上儲存對這些戰鬥人員的引用，在 `combatants` [Attribute](Attribute) 中。  以同樣的方式，我們必須儲存一個誰對誰有優勢/劣勢的_矩陣_。我們還必須追蹤誰在逃跑，特別是他們逃跑了多長時間，因為在那之後他們就會離開戰鬥。

(getting-the-sides-of-combat)=
### 取得戰鬥雙方

雙方的差異取決於我們是否在[PvP房間](./Beginner-Tutorial-Rooms.md)中：在PvP房間中，其他人都是你的敵人。否則，戰鬥中只有 NPCs 是你的敵人（假設你與其他玩家組隊）。

```python
# in evadventure/combat_turnbased.py

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

	# ...

    def get_sides(self, combatant):
           """
           Get a listing of the two 'sides' of this combat,
           from the perspective of the provided combatant.
           """
           if self.obj.allow_pvp:
               # in pvp, everyone else is an ememy
               allies = [combatant]
               enemies = [comb for comb in self.combatants if comb != combatant]
           else:
               # otherwise, enemies/allies depend on who combatant is
               pcs = [comb for comb in self.combatants if inherits_from(comb, EvAdventureCharacter)]
               npcs = [comb for comb in self.combatants if comb not in pcs]
               if combatant in pcs:
                   # combatant is a PC, so NPCs are all enemies
                   allies = pcs
                   enemies = npcs
               else:
                   # combatant is an NPC, so PCs are all enemies
                   allies = npcs
                   enemies = pcs
        return allies, enemies
```

請注意，由於 `EvadventureCombatBaseHandler`（我們的回合處理程式所基於的）是 [Script](../../../Components/Scripts.md)，因此它提供了許多有用的功能。例如，`self.obj` 是 Script “所在”的實體。由於我們計劃將此處理程式放在目前位置，因此 `self.obj` 將是該房間。

我們在這裡所做的就是檢查它是否是 PvP 房間，並用它來確定誰是盟友還是敵人。請注意，`combatant` _不_包含在 `allies` 回傳值中 - 我們需要記住這一點。

(tracking-advantagedisadvantage)=
### 追蹤優勢/劣勢

```python
# in evadventure/combat_turnbased.py

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

	# ...

    def give_advantage(self, combatant, target):
        self.advantage_matrix[combatant][target] = True

    def give_disadvantage(self, combatant, target, **kwargs):
        self.disadvantage_matrix[combatant][target] = True

    def has_advantage(self, combatant, target, **kwargs):
        return (
	        target in self.fleeing_combatants
	        or bool(self.advantage_matrix[combatant].pop(target, False))
        )
    def has_disadvantage(self, combatant, target):
        return bool(self.disadvantage_matrix[combatant].pop(target, False))
```

我們使用 `advantage/disadvantage_matrix` 屬性來追蹤誰對誰有優勢。

```{sidebar} 。流行音樂（）
Python `.pop()` 方法從清單或字典中刪除一個元素並傳回它。對於列表，它按索引刪除（或預設情況下最後一個元素）。對於字典（如此處），您指定要刪除的鍵。提供預設值作為第二個引數可以防止在鍵不存在時出現錯誤。
```
在 `has dis/advantage` 方法中，我們從矩陣中提取 `pop` 目標，這將導致值 `True` 或 `False`（如果目標不在矩陣中，我們給出的預設值為 `pop`）。這意味著優勢一旦獲得，就只能使用一次。

我們也認為每個人在對抗逃跑的戰鬥人員時都具有優勢。

(adding-and-removing-combatants)=
### 新增和刪除戰鬥人員

由於戰鬥處理程式是共享的，我們必須能夠輕鬆新增和刪除戰鬥人員。
與基本處理程式相比，這是新的。

```python
# in evadventure/combat_turnbased.py

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    # ...

    def add_combatant(self, combatant):
        """
        Add a new combatant to the battle. Can be called multiple times safely.
        """
        if combatant not in self.combatants:
            self.combatants[combatant] = self.fallback_action_dict
            return True
        return False

    def remove_combatant(self, combatant):
        """
        Remove a combatant from the battle.
        """
        self.combatants.pop(combatant, None)
        # clean up menu if it exists
		# TODO!
```

我們只需新增帶有後備動作字典的戰鬥人員即可。我們從`add_combatant`返回`bool`，以便呼叫函式知道它們是否實際上是重新新增的（如果它們是新的，我們可能需要做一些額外的設定）。

現在我們只是 `pop` 戰鬥人員，但將來我們需要在戰鬥結束時對選單進行一些額外的清理（我們會做到這一點）。

(flee-action)=
### 逃跑行動

由於你不能只是離開房間來逃離回合製戰鬥，我們需要新增一個新的 `CombatAction` 子類，就像我們在 [基礎戰鬥課程](./Beginner-Tutorial-Combat-Base.md#actions) 中建立的子類一樣。


```python
# in evadventure/combat_turnbased.py

from .combat_base import CombatAction

# ...

class CombatActionFlee(CombatAction):
    """
    Start (or continue) fleeing/disengaging from combat.

    action_dict = {
           "key": "flee",
        }
    """

    def execute(self):
        combathandler = self.combathandler

        if self.combatant not in combathandler.fleeing_combatants:
            # we record the turn on which we started fleeing
            combathandler.fleeing_combatants[self.combatant] = self.combathandler.turn

        # show how many turns until successful flight
        current_turn = combathandler.turn
        started_fleeing = combathandler.fleeing_combatants[self.combatant]
        flee_timeout = combathandler.flee_timeout
        time_left = flee_timeout - (current_turn - started_fleeing) - 1

        if time_left > 0:
            self.msg(
                "$You() $conj(retreat), being exposed to attack while doing so (will escape in "
                f"{time_left} $pluralize(turn, {time_left}))."
            )


class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

	action_classes = {
        "hold": CombatActionHold,
        "attack": CombatActionAttack,
        "stunt": CombatActionStunt,
        "use": CombatActionUseItem,
        "wield": CombatActionWield,
        "flee": CombatActionFlee # < ---- added!
    }

	# ...
```

我們建立動作來利用我們在戰鬥處理程式中設定的 `fleeing_combatants` 字典。該指令儲存了逃跑的戰鬥人員及其逃跑開始的`turn`。如果多次執行 `flee` 操作，我們將只顯示剩餘的回合數。

最後，我們確保將新的 `CombatActionFlee` 新增至戰鬥處理程式的 `action_classes` 登錄檔中。

(queue-action)=
### 佇列動作

```python
# in evadventure/combat_turnbased.py

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    # ...

    def queue_action(self, combatant, action_dict):
        self.combatants[combatant] = action_dict

        # track who inserted actions this turn (non-persistent)
        did_action = set(self.ndb.did_action or set())
        did_action.add(combatant)
        if len(did_action) >= len(self.combatants):
            # everyone has inserted an action. Start next turn without waiting!
            self.force_repeat()

```

為了對一個動作進行排隊，我們只需將其 `action_dict` 與戰鬥者一起存放在 `combatants` Attribute 中。

我們使用 Python `set()` 來追蹤本回合誰已將操作排隊。如果本回合所有戰鬥人員都輸入了新的（或更新的）動作，我們將使用 `.force_repeat()` 方法，該方法適用於所有 [Scripts](../../../Components/Scripts.md)。當呼叫此函式時，下一輪將立即觸發，而不是等到逾時。

(execute-an-action-and-tick-the-round)=
### 執行一個動作並勾選該回合

```{code-block} python
:linenos:
:emphasize-lines: 13,16,17,22,43,49

# in evadventure/combat_turnbased.py

import random

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    # ...

    def execute_next_action(self, combatant):
        # this gets the next dict and rotates the queue
        action_dict = self.combatants.get(combatant, self.fallback_action_dict)

        # use the action-dict to select and create an action from an action class
        action_class = self.action_classes[action_dict["key"]]
        action = action_class(self, combatant, action_dict)

        action.execute()
        action.post_execute()

        if action_dict.get("repeat", False):
            # queue the action again *without updating the
            # *.ndb.did_action list* (otherwise
            # we'd always auto-end the turn if everyone used
            # repeating actions and there'd be
            # no time to change it before the next round)
            self.combatants[combatant] = action_dict
        else:
            # if not a repeat, set the fallback action
            self.combatants[combatant] = self.fallback_action_dict


   def at_repeat(self):
        """
        This method is called every time Script repeats
        (every `interval` seconds). Performs a full turn of
        combat, performing everyone's actions in random order.
        """
        self.turn += 1
        # random turn order
        combatants = list(self.combatants.keys())
        random.shuffle(combatants)  # shuffles in place

        # do everyone's next queued combat action
        for combatant in combatants:
            self.execute_next_action(combatant)

        self.ndb.did_action = set()

        # check if one side won the battle
        self.check_stop_combat()

```

我們的操作執行由兩部分組成 - `execute_next_action`（在父類中定義供我們實現）和 `at_repeat` 方法，該方法是 [Script](../../../Components/Scripts.md) 的一部分

對於`execute_next_action`：

- **第 13 行**：我們從 `combatants` Attribute 得到 `action_dict`。如果沒有任何內容排隊，我們將返回 `fallback_action_dict`（預設為 `hold`）。
- **第 16 行**：我們使用 `action_dict` 的 `key`（類似「攻擊」、「使用」、「揮舞」等）從 `action_classes` 字典中取得符合 Action 的類別。
- **第 17 行**：這裡使用戰鬥人員和動作字典例項化動作類，使其準備好執行。然後在以下幾行執行此操作。
- **第 22 行**：我們在這裡引入一個新的可選 `action-dict`，即布林值 `repeat` 鍵。這允許我們重新排隊操作。如果不是，將使用後備操作。

Script 觸發後，每 `interval` 秒重複呼叫 `at_repeat`。這是我們用來追蹤每輪結束時間的方法。

- **第 43 行**：在此範例中，我們的操作之間沒有內部順序。所以我們只是隨機化它們的發射順序。
- **第 49 行**：這個 `set` 被分配給 `queue_action` 方法，以瞭解每個人何時提交新作業。我們必須確保在下一輪之前在這裡取消設定。

(check-and-stop-combat)=
### 檢查並停止戰鬥

```{code-block} python
:linenos:
:emphasize-lines: 28,41,49,60

# in evadventure/combat_turnbased.py

import random
from evennia.utils.utils import list_to_string

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    # ...

     def stop_combat(self):
        """
        Stop the combat immediately.

        """
        for combatant in self.combatants:
            self.remove_combatant(combatant)
        self.stop()
        self.delete()

    def check_stop_combat(self):
        """Check if it's time to stop combat"""

        # check if anyone is defeated
        for combatant in list(self.combatants.keys()):
            if combatant.hp <= 0:
                # PCs roll on the death table here, NPCs die.
                # Even if PCs survive, they
                # are still out of the fight.
                combatant.at_defeat()
                self.combatants.pop(combatant)
                self.defeated_combatants.append(combatant)
                self.msg("|r$You() $conj(fall) to the ground, defeated.|n", combatant=combatant)
            else:
                self.combatants[combatant] = self.fallback_action_dict

        # check if anyone managed to flee
        flee_timeout = self.flee_timeout
        for combatant, started_fleeing in self.fleeing_combatants.items():
            if self.turn - started_fleeing >= flee_timeout - 1:
                # if they are still alive/fleeing and have been fleeing long enough, escape
                self.msg("|y$You() successfully $conj(flee) from combat.|n", combatant=combatant)
                self.remove_combatant(combatant)

        # check if one side won the battle
        if not self.combatants:
            # noone left in combat - maybe they killed each other or all fled
            surviving_combatant = None
            allies, enemies = (), ()
        else:
            # grab a random survivor and check if they have any living enemies.
            surviving_combatant = random.choice(list(self.combatants.keys()))
            allies, enemies = self.get_sides(surviving_combatant)

        if not enemies:
            # if one way or another, there are no more enemies to fight
            still_standing = list_to_string(f"$You({comb.key})" for comb in allies)
            knocked_out = list_to_string(comb for comb in self.defeated_combatants if comb.hp > 0)
            killed = list_to_string(comb for comb in self.defeated_combatants if comb.hp <= 0)

            if still_standing:
                txt = [f"The combat is over. {still_standing} are still standing."]
            else:
                txt = ["The combat is over. No-one stands as the victor."]
            if knocked_out:
                txt.append(f"{knocked_out} were taken down, but will live.")
            if killed:
                txt.append(f"{killed} were killed.")
            self.msg(txt)
            self.stop_combat()
```

`check_stop_combat` 在回合結束時被呼叫。我們想弄清楚誰死了以及“一方”是否獲勝。

- **第28-38行**：我們檢查所有戰鬥人員並確定他們是否在HP之外。如果是這樣，我們觸發相關的鉤子並將它們新增到 `defeated_combatants` Attribute 中。
- **第 38 行**：對於所有倖存的戰鬥人員，我們確保給他們`fallback_action_dict`。
- **第 41-46 行**：`fleeing_combatant` Attribute 是 `{fleeing_combatant: turn_number}` 形式的字典，追蹤他們第一次開始逃跑的時間。我們將其與當前回合數和 `flee_timeout` 進行比較，看看他們是否現在逃跑並應該被允許從戰鬥中移除。
- **第 49-56 行**：這裡我們正在確定衝突的一方是否擊敗了另一方。
- **第 60 行**：`list_to_string` Evennia 實用程式將條目清單（例如 `["a", "b", "c"`）轉換為漂亮的字串 `"a, b and c"`。我們用它來向戰鬥人員呈現一些美好的結局訊息。

(start-combat)=
### 開始戰鬥

由於我們使用 [Script](../../../Components/Scripts.md) 的計時器元件來計時我們的戰鬥，因此我們還需要一個輔助方法來「啟動」它。

```python
from evennia.utils.utils import list_to_string

# in evadventure/combat_turnbased.py

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    # ...

    def start_combat(self, **kwargs):
        """
        This actually starts the combat. It's safe to run this multiple times
        since it will only start combat if it isn't already running.

        """
        if not self.is_active:
            self.start(**kwargs)

```

`start(**kwargs)` 方法是 Script 上的方法，並且將使其開始每 `interval` 秒呼叫 `at_repeat`。我們將在 `kwargs` 內傳遞 `interval`（例如，我們稍後將傳遞 `combathandler.start_combat(interval=30)`）。

(using-evmenu-for-the-combat-menu)=
## 使用EvMenu作為戰鬥選單

_EvMenu_ 用於在 Evennia 中建立遊戲內選單。我們在[角色生成課程](./Beginner-Tutorial-Chargen.md)中已經使用了一個簡單的EvMenu。這次我們需要更先進一點。  雖然[EvMenu 檔案](../../../Components/EvMenu.md) 更詳細地描述了其功能，但我們將在此快速概述其工作原理。

EvMenu 由 _nodes_ 組成，它們是此表單上的常規函式（這裡有些簡化，有更多選項）：

```python
def node_somenodename(caller, raw_string, **kwargs):

    text = "some text to show in the node"
    options = [
        {
           "key": "Option 1", # skip this to get a number
           "desc": "Describing what happens when choosing this option."
           "goto": "name of the node to go to"  # OR (callable, {kwargs}}) returning said name
        },
        # other options here
    ]
    return text, options
```

因此，基本上每個節點都採用 `caller`（使用選單的節點）、`raw_string`（空字串或使用者在前一個節點上輸入的內容）和 `**kwargs` 引數，可用於在節點之間傳遞資料。它返回 `text` 和 `options`。

`text`是使用者進入這部分選單時會看到的內容，例如「選擇你想要攻擊的人！」。 `options` 是描述每個選項的字典清單。它們將顯示為節點文字下方的多項選擇清單（請參閱本課程頁面頂部的範例）。

當我們稍後建立 EvMenu 時，我們將建立一個_節點索引_ - 唯一名稱和這些「節點函式」之間的對應。所以像這樣：

```python
# example of a EvMenu node index
    {
      "start": node_combat_main,
      "node1": node_func1,
      "node2": node_func2,
      "some name": node_somenodename,
      "end": node_abort_menu,
    }
```
每個 `option` 字典都有一個鍵 `"goto"` ，用於確定玩家選擇該選項時應跳到哪個節點。在選單內部，每個節點都需要用這些名稱來引用（如 `"start"`、`"node1"` 等）。

每個選項的 `"goto"` 值可以直接指定名稱（如 `"node1"`）_或_它可以作為元組 `(callable, {keywords})` 給出。這個 `callable` 被稱為_並且預計會傳回下一個要使用的節點名稱（如 `"node1"`）。

`callable`（通常稱為「goto callable」）看起來與節點函式非常相似：

```python
def _goto_when_choosing_option1(caller, raw_string, **kwargs):
    # do whatever is needed to determine the next node
    return nodename  # also nodename, dict works
```

```{sidebar} 將節點函式與 goto 可呼叫函式分離
為了使節點函式與 goto-callables 明顯分開，Evennia 檔案總是在節點函式前加上 `node_` 字首，並在選單 goto 函式前加上下劃線 `_`（這也使 goto 函式在 Python 術語中成為「私有」）。
```
這裡，`caller` 仍然是使用選單的字串，`raw_string` 是您輸入的用於選擇此選項的實際字串。 `**kwargs` 是您新增至 `(callable, {keywords})` 元組中的關鍵字。

goto-callable 必須傳回下一個節點的名稱。或者，您可以同時返回 `nodename, {kwargs}`。如果您這樣做，下一個節點將獲得這些 kwargs 作為傳入 `**kwargs`。透過這種方式，您可以將資訊從一個節點傳遞到下一個節點。一個特殊的功能是，如果 `nodename` 回傳為 `None`，則 _current_ 節點將再次_rerun_。

這是一個（有點做作的）範例，說明瞭 goto-callable 和 node-function 如何結合在一起：

```
# goto-callable
def _my_goto_callable(caller, raw_string, **kwargs):
    info_number = kwargs["info_number"]
    if info_number > 0:
        return "node1"
    else:
        return "node2", {"info_number": info_number}  # will be **kwargs when "node2" runs next


# node function
def node_somenodename(caller, raw_string, **kwargs):
    text = "Some node text"
    options = [
        {
            "desc": "Option one",
            "goto": (_my_goto_callable, {"info_number", 1})
        },
        {
            "desc": "Option two",
            "goto": (_my_goto_callable, {"info_number", -1})
        },
    ]
```

(menu-for-turnbased-combat)=
## 回合製戰鬥選單


我們的戰鬥選單將非常簡單。我們將有一個中央選單節點，其中包含指示所有不同戰鬥動作的選項。當在選單中選擇一個操作時，應該向玩家提出一系列問題，每個問題都指定該操作所需的一條資訊。最後一步是將這些資訊建構到我們可以與戰鬥處理程式一起排隊的`action-dict`中。

若要了解流程，請瞭解操作選擇的工作原理（從左到右閱讀）：

| 在基節點中 | 步驟1 | 步驟2 | 步驟3 | 步驟4 |
| --- | --- | --- | --- | --- |
| 選擇`attack` | 選擇`target` | 佇列動作字典 | - | - |
| 選擇`stunt - give advantage` | 選擇`Ability`| 選擇`allied recipient` | 選擇`enemy target` | 佇列動作字典 |
| 選擇`stunt - give disadvantage` | 選擇`Ability` | 選擇`enemy recipient` | 選擇`allied target` | 佇列動作字典 |
| 選擇`use item on yourself or ally` | 從庫存中選擇`item` | 選擇`allied target` | 佇列動作字典 | - |
| 選擇`use item on enemy` | 從庫存中選擇`item` | 選擇`enemy target` | 佇列動作字典 | - |
| 選擇`wield/swap item from inventory` | 從庫存中選擇`item`` | 佇列動作字典 | - | - |
| 選擇`flee` | 佇列動作字典 | - | - | - |
| 選擇`hold, doing nothing` | 佇列動作字典 | - | - | - |

檢視上表，我們可以看到我們有_很多_重複使用。盟友/敵人/目標/接收者/物品的選擇代表可以被不同行動共享的節點。

每個操作也遵循線性順序，就像您在某些軟體中看到的逐步「嚮導」一樣。我們希望能夠在每個序列中來回移動，如果您在過程中改變主意，您也可以中止操作。

對操作進行排隊後，我們應該始終返回到基本節點，在那裡我們將等待，直到回合結束並且所有操作都執行。

我們將建立一些幫助程式，使我們的特定選單易於使用。

(the-node-index)=
### 節點索引

這些是我們的選單所需的節點：

```python
# not coded anywhere yet, just noting for reference
node_index = {
    # node names                # callables   # (future callables)
    "node_choose_enemy_target": None, # node_choose_enemy_target,
    "node_choose_allied_target": None, # node_choose_allied_target,
    "node_choose_enemy_recipient": None, # node_choose_enemy_recipient,
    "node_choose_allied_recipient": None, # node_choose_allied_recipient,
    "node_choose_ability": None, # node_choose_ability,
    "node_choose_use_item": None, # node_choose_use_item,
    "node_choose_wield_item": None, # node_choose_wield_item,
    "node_combat": None, # node_combat,
}
```

所有可呼叫專案都保留為 `None`，因為我們還沒有建立它們。但最好記下預期的名稱，因為我們需要它們才能從一個節點跳到另一個節點。需要注意的重要一點是 `node_combat` 將是我們應該一遍又一遍地返回的基本節點。

(getting-or-setting-the-combathandler)=
### 取得或設定戰鬥處理程式

```python
# in evadventure/combat_turnbased.py

from evennia import EvMenu

# ...

def _get_combathandler(caller, turn_timeout=30, flee_time=3, combathandler_key="combathandler"):
    return EvAdventureTurnbasedCombatHandler.get_or_create_combathandler(
        caller.location,
        interval=turn_timeout,
        attributes=[("flee_time", flee_time)],
        key=combathandler_key,
    )
```

我們新增這個只是為了以後呼叫它時不必寫那麼多。我們傳遞`caller.location`，這是在目前位置檢索/建立戰鬥處理程式的內容。 `interval` 是戰鬥處理程式（這是一個 [Script](../../../Components/Scripts.md)）呼叫其 `at_repeat` 方法的頻率。我們同時設定`flee_time` Attribute。

(queue-an-action)=
### 對操作進行排隊

這是我們的第一個「goto 函式」。這將被呼叫以實際將我們完成的動作字典與戰鬥處理程式排隊。完成此操作後，它應該會返回到基址 `node_combat`。

```python
# in evadventure/combat_turnbased.py

# ...

def _queue_action(caller, raw_string, **kwargs):
    action_dict = kwargs["action_dict"]
    _get_combathandler(caller).queue_action(caller, action_dict)
    return "node_combat"
```

我們在這裡做出一個假設 - `kwargs` 包含 `action_dict` 鍵，並且 action-dict 已準備就緒。

由於這是一個可呼叫的 goto，因此我們必須傳回要轉到的下一個節點。由於這是最後一步，我們總是會回到 `node_combat` 基節點，所以這就是我們返回的內容。

(rerun-a-node)=
### 重新執行節點

goto 可呼叫物件的一個特殊功能是能夠透過傳回 `None` 來重新執行相同節點。

```python
# in evadventure/combat_turnbased.py

# ...

def _rerun_current_node(caller, raw_string, **kwargs):
    return None, kwargs
```

在選項中使用此選項將重新執行目前節點，但將保留傳送的`kwargs`。

(stepping-through-the-wizard)=
### 單步執行嚮導

我們的特殊選單非常對稱 - 您選擇一個選項，然後您在回來之前只需選擇一系列選項。因此，我們將建立另一個 goto 函式來幫助我們輕鬆地做到這一點。為了理解，我們首先展示我們計劃如何使用它：

```python
# in the base combat-node function (just shown as an example)

options = [
    # ...
    "desc": "use an item on an enemy",
    "goto": (
       _step_wizard,
       {
           "steps": ["node_choose_use_item", "node_choose_enemy_target"],
           "action_dict": {"key": "use", "item": None, "target": None},
       }
    )
]
```

當使用者選擇對敵人使用物品時，我們將使用兩個關鍵字`steps`和`action_dict`來呼叫`_step_wizard`。第一個是我們需要引導玩家透過的選單節點_序列_，以建立我們的動作字典。

後者是 `action_dict` 本身。每個節點都會逐漸填入這個字典中的 `None` 位置，直到我們有一個完整的字典並且可以將其傳送到我們之前定義的 [`_queue_action`](#queue-an-action) goto 函式。

此外，我們希望能夠像這樣「返回」到前一個節點：


```python
# in some other node (shown only as an example)

def some_node(caller, raw_string, **kwargs):

    # ...

    options = [
        # ...
        {
            "key": "back",
            "goto": ( _step_wizard, {**kwargs, **{"step": "back"}})
        },
    ]

    # ...
```

注意這裡使用`**`。 `{**dict1, **dict2}` 是一種強大的單行語法，可將兩個字典合併為一個。這會保留（並傳遞）傳入的 `kwargs` 並僅向其新增一個新的關鍵「步驟」。最終效果類似於我們在單獨的行上執行 `kwargs["step"] = "back"`（除非我們在使用 `**` 方法時最終得到 _new_ `dict`）。

因此，讓我們實作一個 `_step_wizard` goto 函式來處理這個問題！

```python
# in evadventure/combat_turnbased.py

# ...

def _step_wizard(caller, raw_string, **kwargs):

    # get the steps and count them
    steps = kwargs.get("steps", [])
    nsteps = len(steps)

    # track which step we are on
    istep = kwargs.get("istep", -1)

    # check if we are going back (forward is default)
    step_direction = kwargs.get("step", "forward")

    if step_direction == "back":
        # step back in wizard
        if istep <= 0:
            # back to the start
            return "node_combat"
        istep = kwargs["istep"] = istep - 1
        return steps[istep], kwargs
    else:
        # step to the next step in wizard
        if istep >= nsteps - 1:
            # we are already at end of wizard - queue action!
            return _queue_action(caller, raw_string, **kwargs)
        else:
            # step forward
            istep = kwargs["istep"] = istep + 1
            return steps[istep], kwargs

```

這取決於透過 `**kwargs` 傳遞 `steps`、`step` 和 `istep`。  如果 `step` 是“後退”，那麼我們將按 `steps` 的順序後退，否則向前。我們增加/減少 `istep` 鍵值來追蹤我們所在的位置。

如果到達末尾，我們將直接呼叫 `_queue_action` 輔助函式。如果我們回到開頭，我們將返回到基本節點。

我們將建立一個最終輔助函式，以快速將 `back`（和 `abort`）選項新增至需要它的節點：

```python
# in evadventure/combat_turnbased.py

# ...

def _get_default_wizard_options(caller, **kwargs):
    return [
        {
            "key": "back",
            "goto": (_step_wizard, {**kwargs, **{"step": "back"}})
        },
        {
            "key": "abort",
            "goto": "node_combat"
        },
        {
            "key": "_default",
            "goto": (_rerun_current_node, kwargs),
        },
    ]
```

這不是一個 goto 函式，它只是一個幫助器，我們將呼叫它來快速將這些額外選項新增到節點的選項清單中，而不必一遍又一遍地鍵入它。

正如我們之前所看到的，`back` 選項將使用 `_step_wizard` 在嚮導中後退。 `abort` 選項將簡單地跳回主節點，中止精靈。

`_default` 選項很特殊。此選項鍵告訴 EvMenu：「如果其他選項都不匹配，則使用此選項」。也就是說，如果他們輸入空輸入或垃圾，我們將重新顯示該節點。不過，我們確保傳遞 `kwargs`，這樣我們就不會失去我們在嚮導中所處位置的任何資訊。

最後我們準備好要寫我們的選單節點了！

(choosing-targets-and-recipients)=
### 選擇目標和接受者

這些節點的工作方式都是相同的：它們應該提供合適的目標/收件者清單以供選擇，然後將結果作為 `target` 或 `recipient` 鍵放入操作字典中。

```{code-block} python
:linenos:
:emphasize-lines: 11,13,15,18,23

# in evadventure/combat_turnbased.py

# ...

def node_choose_enemy_target(caller, raw_string, **kwargs):

    text = "Choose an enemy to target"

    action_dict = kwargs["action_dict"]
    combathandler = _get_combathandler(caller)
    _, enemies = combathandler.get_sides(caller)

    options = [
        {
            "desc": target.get_display_name(caller),
            "goto": (
                _step_wizard,
                {**kwargs, **{"action_dict": {**action_dict, **{"target": target}}}},
            )
        }
        for target in enemies
    ]
    options.extend(_get_default_wizard_options(caller, **kwargs))
    return text, options


def node_choose_enemy_recipient(caller, raw_string, **kwargs):
     # almost the same, except storing "recipient"


def node_choose_allied_target(caller, raw_string, **kwargs):
     # almost the same, except using allies + yourself


def node_choose_allied_recipient(caller, raw_string, **kwargs):
     # almost the same, except using allies + yourself and storing "recipient"

```

- **第11行**：這裡我們使用`combathandler.get_sides(caller)`從`caller`（使用選單的那個）的角度來取得「敵人」。
- **第 13-31 行**：這是我們發現的所有敵人的迴圈。
    - **第 15 行**：我們使用 `target.get_display_name(caller)`。此方法（所有 Evennia `Objects` 上的預設方法）允許目標傳回名稱，同時知道是誰在詢問。這使得管理員看到 `Name (#5)`，而普通使用者只能看到 `Name`。如果你不關心這個，你可以在這裡做`target.key`。
    - **第 18 行**：這一行看起來很複雜，但請記住 `{**dict1, **dict2}` 是一種將兩個字典合併在一起的單行方法。其作用是分三步驟完成：
        - 首先，我們將 `action_dict` 與字典 `{"target": target}` 加在一起。這與 `action_dict["target"] = target` 具有相同的效果，只不過我們透過合併建立了一個新的字典。
        - 接下來我們採用這個新的合併並建立一個新的字典`{"action_dict": new_action_dict}`。
        - 最後我們將其與現有的 `kwargs` 字典合併。結果是一個新的字典，現在具有更新的 `"action_dict"` 鍵，指向設定了 `target` 的操作字典。
- **第 23 行**：我們使用預設精靈選項（`back`、`abort`）擴充套件 `options` 清單。由於我們為此建立了一個輔助函式，因此這只是一行。

建立另外三個所需的節點 `node_choose_enemy_recipient`、`node_choose_allied_target` 和 `node_choose_allied_recipient` 也遵循相同的模式；它們只是改用 `combathandler.get_sides()` 回傳的 `allies` 或 `enemies`，然後在 `action_dict` 中設定 `target` 或 `recipient` 欄位。我們把這部分留給讀者自行實作。

(choose-an-ability)=
### 選擇一種能力

對於特技，我們需要能夠選擇您想要增強/挫敗的 _Knave_ 能力（STR、DEX 等）。

```python
# in evadventure/combat_turnbased.py

from .enums import Ability

# ...

def node_choose_ability(caller, raw_string, **kwargs):
    text = "Choose the ability to apply"
    action_dict = kwargs["action_dict"]

    options = [
        {
            "desc": abi.value,
            "goto": (
                _step_wizard,
                {
                    **kwargs,
                    **{
                        "action_dict": {**action_dict, **{"stunt_type": abi, "defense_type": abi}},
                    },
                },
            ),
        }
        for abi in (
            Ability.STR,
            Ability.DEX,
            Ability.CON,
            Ability.INT,
            Ability.WIS,
            Ability.CHA,
        )
    ]
    options.extend(_get_default_wizard_options(caller, **kwargs))
    return text, options

```

其原理與目標/接收者設定者節點相同，只是我們只提供可供選擇的能力清單。我們根據 Stunt 動作的需要更新 `action_dict` 中的 `stunt_type` 和 `defense_type` 鍵。

(choose-an-item-to-use-or-wield)=
### 選擇要使用或揮舞的物品

```python
# in evadventure/combat_turnbased.py

# ...

def node_choose_use_item(caller, raw_string, **kwargs):
    text = "Select the item"
    action_dict = kwargs["action_dict"]

    options = [
        {
            "desc": item.get_display_name(caller),
            "goto": (
                _step_wizard,
                {**kwargs, **{"action_dict": {**action_dict, **{"item": item}}}},
            ),
        }
        for item in caller.equipment.get_usable_objects_from_backpack()
    ]
    if not options:
        text = "There are no usable items in your inventory!"

    options.extend(_get_default_wizard_options(caller, **kwargs))
    return text, options


def node_choose_wield_item(caller, raw_string, **kwargs):
     # same except using caller.equipment.get_wieldable_objects_from_backpack()

```

我們的[裝置處理程式](./Beginner-Tutorial-Equipment.md)有非常有用的幫助方法`.get_usable_objects_from_backpack`。我們只是呼叫它來獲取我們想要選擇的所有專案的列表。否則這個節點現在看起來應該非常熟悉了。

`node_choose_wield_item` 非常相似，只不過它使用 `caller.equipment.get_wieldable_objects_from_backpack()` 代替。我們將把這個的實作留給讀者。

(the-main-menu-node)=
### 主選單節點

這將它們聯絡在一起。

```python
# in evadventure/combat_turnbased.py

# ...

def node_combat(caller, raw_string, **kwargs):
    """Base combat menu"""

    combathandler = _get_combathandler(caller)

    text = combathandler.get_combat_summary(caller)
    options = [
        {
            "desc": "attack an enemy",
            "goto": (
                _step_wizard,
                {
                    "steps": ["node_choose_enemy_target"],
                    "action_dict": {"key": "attack", "target": None, "repeat": True},
                },
            ),
        },
        {
            "desc": "Stunt - gain a later advantage against a target",
            "goto": (
                _step_wizard,
                {
                    "steps": [
                        "node_choose_ability",
                        "node_choose_enemy_target",
                        "node_choose_allied_recipient",
                    ],
                    "action_dict": {"key": "stunt", "advantage": True},
                },
            ),
        },
        {
            "desc": "Stunt - give an enemy disadvantage against yourself or an ally",
            "goto": (
                _step_wizard,
                {
                    "steps": [
                        "node_choose_ability",
                        "node_choose_enemy_recipient",
                        "node_choose_allied_target",
                    ],
                    "action_dict": {"key": "stunt", "advantage": False},
                },
            ),
        },
        {
            "desc": "Use an item on yourself or an ally",
            "goto": (
                _step_wizard,
                {
                    "steps": ["node_choose_use_item", "node_choose_allied_target"],
                    "action_dict": {"key": "use", "item": None, "target": None},
                },
            ),
        },
        {
            "desc": "Use an item on an enemy",
            "goto": (
                _step_wizard,
                {
                    "steps": ["node_choose_use_item", "node_choose_enemy_target"],
                    "action_dict": {"key": "use", "item": None, "target": None},
                },
            ),
        },
        {
            "desc": "Wield/swap with an item from inventory",
            "goto": (
                _step_wizard,
                {
                    "steps": ["node_choose_wield_item"],
                    "action_dict": {"key": "wield", "item": None},
                },
            ),
        },
        {
            "desc": "flee!",
            "goto": (_queue_action, {"action_dict": {"key": "flee", "repeat": True}}),
        },
        {
            "desc": "hold, doing nothing",
            "goto": (_queue_action, {"action_dict": {"key": "hold"}}),
        },
        {
            "key": "_default",
            "goto": "node_combat",
        },
    ]

    return text, options
```

這從每個操作選擇的 `_step_wizard` 開始。它還為每個操作列出 `action_dict`，為將由以下節點設定的欄位留下 `None` 值。

請注意我們如何將 `"repeat"` 鍵新增到某些操作中。讓它們自動重複意味著玩家不必每次都插入相同的動作。

(attack-command)=
## 攻擊指令

我們只需要一個指令來執行回合製戰鬥系統。這是`attack` 指令。一旦你使用它一次，你就會進入選單。


```python
# in evadventure/combat_turnbased.py

from evennia import Command, CmdSet, EvMenu

# ...

class CmdTurnAttack(Command):
    """
    Start or join combat.

    Usage:
      attack [<target>]

    """

    key = "attack"
    aliases = ["hit", "turnbased combat"]

    turn_timeout = 30  # seconds
    flee_time = 3  # rounds

    def parse(self):
        super().parse()
        self.args = self.args.strip()

    def func(self):
        if not self.args:
            self.msg("What are you attacking?")
            return

        target = self.caller.search(self.args)
        if not target:
            return

        if not hasattr(target, "hp"):
            self.msg("You can't attack that.")
            return

        elif target.hp <= 0:
            self.msg(f"{target.get_display_name(self.caller)} is already down.")
            return

        if target.is_pc and not target.location.allow_pvp:
            self.msg("PvP combat is not allowed here!")
            return

        combathandler = _get_combathandler(
            self.caller, self.turn_timeout, self.flee_time)

        # add combatants to combathandler. this can be done safely over and over
        combathandler.add_combatant(self.caller)
        combathandler.queue_action(self.caller, {"key": "attack", "target": target})
        combathandler.add_combatant(target)
        target.msg("|rYou are attacked by {self.caller.get_display_name(self.caller)}!|n")
        combathandler.start_combat()

        # build and start the menu
        EvMenu(
            self.caller,
            {
                "node_choose_enemy_target": node_choose_enemy_target,
                "node_choose_allied_target": node_choose_allied_target,
                "node_choose_enemy_recipient": node_choose_enemy_recipient,
                "node_choose_allied_recipient": node_choose_allied_recipient,
                "node_choose_ability": node_choose_ability,
                "node_choose_use_item": node_choose_use_item,
                "node_choose_wield_item": node_choose_wield_item,
                "node_combat": node_combat,
            },
            startnode="node_combat",
            combathandler=combathandler,
            auto_look=False,
            # cmdset_mergetype="Union",
            persistent=True,
        )


class TurnCombatCmdSet(CmdSet):
    """
    CmdSet for the turn-based combat.
    """

    def at_cmdset_creation(self):
        self.add(CmdTurnAttack())
```

`attack target`指令將確定目標是否有生命值（只有有生命值的物體才能被攻擊）以及房間是否允許戰鬥。如果目標是 PC，它會檢查是否允許 PvP。

然後，它繼續啟動一個新的指令處理程式或重複使用一個新的指令處理程式，同時向其中新增攻擊者和目標。如果目標已經處於戰鬥狀態，則不會執行任何操作（與 `.start_combat()` 呼叫相同）。

當我們建立 `EvMenu` 時，我們將其傳遞給我們之前討論過的“選單索引”，現在每個槽中都有實際的節點功能。  我們使選單持久化，以便它在重新載入後仍然存在。

要使該指令可用，請將 `TurnCombatCmdSet` 新增至角色的預設 cmdset 中。


(making-sure-the-menu-stops)=
## 確保選單停止

戰鬥可能會因多種原因而結束。發生這種情況時，我們必須確保清理選單，以便恢復正常操作。我們將其新增到戰鬥處理程式的 `remove_combatant` 方法中（我們之前在那裡留下了 TODO）：

```python

# in evadventure/combat_turnbased.py

# ...

class EvadventureTurnbasedCombatHandler(EvAdventureCombatBaseHandler):

    # ...
    def remove_combatant(self, combatant):
        """
        Remove a combatant from the battle.
        """
        self.combatants.pop(combatant, None)
        # clean up menu if it exists
        if combatant.ndb._evmenu:                   # <--- new
            combatant.ndb._evmenu.close_menu()      #     ''

```

當 evmenu 處於活動狀態時，使用者可以使用 `.ndb._evmenu`（請參閱 EvMenu 檔案）。當我們退出戰鬥時，我們使用它來獲取evmenu並呼叫它的`close_menu()`方法來關閉選單。

我們的回合製戰鬥系統已經完成！


(testing)=
## 測試

```{sidebar}
請參閱 `evennia/contrib/tutorials`、[evadventure/tests/test_combat.py](evennia.contrib.tutorials.evadventure.tests.test_combat) 中的範例測試
```
Turnbased 戰鬥處理程式的單元測試非常簡單，您可以按照前面課程的程式來測試處理程式上的每個方法是否返回您所期望的模擬輸入。

對選單進行單元測試更加複雜。您可以在 [evennia.utils.tests.test_evmenu](github:main/evennia/utils/testss/test_evmenu.py) 中找到執行此操作的範例。

(a-small-combat-test)=
## 實戰小測試

對程式碼進行單元測試不足以看出戰鬥是否有效。我們還需要進行一些「功能」測試，看看它在實踐中是如何運作的。

這是我們進行最小測試所需的：

 - 一個可以進行戰鬥的房間。
 - NPC 進行攻擊（它不會做任何反擊，因為我們還沒有增加任何 AI）
 - 我們可以`wield`的武器。
 - 一個物品（例如藥水）我們可以`use`。

```{sidebar}
您可以在[batchscripts/turnbased_combat_demo.py](github:evennia/contrib/tutorials/evadventure/batchscripts/turnbased_combat_demo.py)中的`evennia/contrib/tutorials/evadventure/`中找到範例戰鬥批次程式碼script
```

在[Twitch實戰課](./Beginner-Tutorial-Combat-Twitch.md)中，我們使用了[批次指令script](../../../Components/Batch-Command-Processor.md)來創造遊戲中的測試環境。這將按順序執行遊戲中的 Evennia 指令。出於演示目的，我們將使用 [batch-code script](../../../Components/Batch-Code-Processor.md)，它以可重複的方式執行原始 Python 程式碼。批次程式碼 script 比批次指令 script 靈活得多。

> 建立一個新的子資料夾 `evadventure/batchscripts/`（如果它尚不存在）

> 建立一個新的Python模組`evadventure/batchscripts/combat_demo.py`

批次程式碼檔案是有效的 Python 模組。唯一的區別是它有一個 `# HEADER` 區塊和一個或多個 `# CODE` 部分。當處理器執行時，在單獨執行該程式碼區塊之前，`# HEADER` 部分將新增到每個 `# CODE` 部分的頂部。由於您可以在遊戲中執行該檔案（包括在不重新載入伺服器的情況下重新整理它），因此可以按需執行更長的 Python 程式碼。

```python
# Evadventure (Turnbased) combat demo - using a batch-code file.
#
# Sets up a combat area for testing turnbased combat.
#
# First add mygame/server/conf/settings.py:
#
#    BASE_BATCHPROCESS_PATHS += ["evadventure.batchscripts"]
#
# Run from in-game as `batchcode turnbased_combat_demo`
#

# HEADER

from evennia import DefaultExit, create_object, search_object
from evennia.contrib.tutorials.evadventure.characters import EvAdventureCharacter
from evennia.contrib.tutorials.evadventure.combat_turnbased import TurnCombatCmdSet
from evennia.contrib.tutorials.evadventure.npcs import EvAdventureNPC
from evennia.contrib.tutorials.evadventure.rooms import EvAdventureRoom

# CODE

# Make the player an EvAdventureCharacter
player = caller  # caller is injected by the batchcode runner, it's the one running this script # E: undefined name 'caller'
player.swap_typeclass(EvAdventureCharacter)

# add the Turnbased cmdset
player.cmdset.add(TurnCombatCmdSet, persistent=True)

# create a weapon and an item to use
create_object(
    "contrib.tutorials.evadventure.objects.EvAdventureWeapon",
    key="Sword",
    location=player,
    attributes=[("desc", "A sword.")],
)

create_object(
    "contrib.tutorials.evadventure.objects.EvAdventureConsumable",
    key="Potion",
    location=player,
    attributes=[("desc", "A potion.")],
)

# start from limbo
limbo = search_object("#2")[0]

arena = create_object(EvAdventureRoom, key="Arena", attributes=[("desc", "A large arena.")])

# Create the exits
arena_exit = create_object(DefaultExit, key="Arena", location=limbo, destination=arena)
back_exit = create_object(DefaultExit, key="Back", location=arena, destination=limbo)

# create the NPC dummy
create_object(
    EvAdventureNPC,
    key="Dummy",
    location=arena,
    attributes=[("desc", "A training dummy."), ("hp", 1000), ("hp_max", 1000)],
)

```

如果在 IDE 中編輯此內容，您可能會在 `player = caller` 行上收到錯誤。這是因為 `caller` 未在此檔案中的任何位置定義。相反，`caller`（執行script的那個）由`batchcode`執行器注入。

但除了 `# HEADER` 和 `# CODE` 特殊之外，這只是一系列正常的 Evennia api 呼叫。

使用開發者/超級使用者帳戶登入遊戲並執行

    > batchcode evadventure.batchscripts.turnbased_combat_demo

這應該會將您置於與虛擬物件一起的競技場中（如果沒有，請檢查輸出中是否有錯誤！如果需要重新開始，請使用 `objects` 和 `delete` 指令列出並刪除物件。）

現在您可以嘗試`attack dummy`，並且應該能夠猛擊假人（降低其生命值以測試摧毀它）。如果您需要修復某些內容，請使用 `q` 退出選單並存取 `reload` 指令（對於最終戰鬥，您可以在建立 `EvMenu` 時透過傳遞 `auto_quit=False` 來停用此功能）。

(conclusions)=
## 結論

至此，我們已經介紹了一些關於如何實現基於抽搐和回合的戰鬥系統的想法。在這個過程中，您已經接觸到了許多概念，例如類別、scripts 和處理程式、指令、EvMenus 等等。

在我們的戰鬥系統真正可用之前，我們需要敵人真正反擊。我們接下來會討論這個問題。
