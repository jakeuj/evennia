(twitch-combat)=
# 抽搐戰鬥

在本課中，我們將在[上一課中](./Beginner-Tutorial-Combat-Base.md)設計的基本戰鬥框架的基礎上建立一個「類似抽搐」的戰鬥系統。
```shell
> attack troll 
  You attack the Troll! 

The Troll roars!

You attack the Troll with Sword: Roll vs armor(11):
 rolled 3 on d20 + strength(+1) vs 11 -> Fail
 
Troll attacks you with Terrible claws: Roll vs armor(12): 
 rolled 13 on d20 + strength(+3) vs 12 -> Success
 Troll hits you for 5 damage! 
 
You attack the Troll with Sword: Roll vs armor(11):
 rolled 14 on d20 + strength(+1) vs 11 -> Success
 You hit the Troll for 2 damage!
 
> look 
  A dark cave 
  
  Water is dripping from the ceiling. 
  
  Exits: south and west 
  Enemies: The Troll 
  --------- Combat Status ----------
  You (Wounded)  vs  Troll (Scraped)

> use potion 
  You prepare to use a healing potion! 
  
Troll attacks you with Terrible claws: Roll vs armor(12): 
 rolled 2 on d20 + strength(+3) vs 12 -> Fail
 
You use a healing potion. 
 You heal 4 damage. 
 
Troll attacks you with Terrible claws: Roll vs armor(12): 
 rolled 8 on d20 + strength(+3) vs 12 -> Fail
 
You attack the troll with Sword: Roll vs armor(11):
 rolled 20 on d20 + strength(+1) vs 11 -> Success (critical success)
 You critically hit the Troll for 8 damage! 
 The Troll falls to the ground, dead. 
 
The battle is over. You are still standing. 
```
> 請注意，本文件不顯示遊戲中的顏色。如果您對替代方案感興趣，請參閱[下一課](./Beginner-Tutorial-Combat-Turnbased.md)，我們將製作一個回合製、基於選單的系統。

對於「Twitch」戰鬥，我們指的是一種沒有任何明確的「回合」劃分的戰鬥系統（與[回合製戰鬥](./Beginner-Tutorial-Combat-Turnbased.md)相反）。它的靈感來自於舊的 [DikuMUD](https://en.wikipedia.org/wiki/DikuMUD) 程式碼庫中的戰鬥方式，但更靈活。

```{sidebar} 與DIKU戰鬥的差異
在 DIKU 中，戰鬥中的所有動作都在 _global_ 'tick' 內發生，例如 3 秒。在我們的系統中，每個戰鬥人員都有自己的“tick”，彼此完全獨立。現在，在Evadventure中，每個戰鬥人員都會以相同的速率滴答，從而模仿DIKU…但他們_沒有_這樣做。
```

基本上，使用者輸入一個操作，並在一段時間後執行該操作（通常是攻擊）。如果他們不採取任何行動，攻擊就會一遍又一遍地重複（結果隨機），直到敵人或你被擊敗。

您可以透過執行其他動作（例如喝藥水或施法）來改變您的策略。你也可以簡單地移動到另一個房間來「逃離」戰鬥（但敵人當然可能會跟著你）

(general-principle)=
## 一般原則

```{sidebar}
已實現的 Twitch 戰鬥系統的範例可以在 `evennia/contrib/tutorials`、[evadventure/combat_twitch.py](evennia.contrib.tutorials.evadventure.combat_twitch) 中找到。
```
以下是基於 Twitch 的戰鬥處理程式的整體設計：

- 每當戰鬥開始時，CombatHandler 的抽搐版本將儲存在每個戰鬥人員身上。當戰鬥結束，或他們離開房間進行戰鬥時，處理程式將被刪除。
- 處理程式將獨立對每個操作進行排隊，啟動計時器直到它們觸發。
- 所有輸入均透過Evennia [指令](../../../Components/Commands.md) 處理。

(twitch-combat-handler)=
## Twitch 戰鬥處理程式

> 建立一個新模組`evadventure/combat_twitch.py`。

我們將利用_Combat Actions_、_Action dicts_ 和父`EvAdventureCombatBaseHandler` [我們先前建立的](./Beginner-Tutorial-Combat-Base.md)。

```python 
# in evadventure/combat_twitch.py

from .combat_base import (
   CombatActionAttack,
   CombatActionHold,
   CombatActionStunt,
   CombatActionUseItem,
   CombatActionWield,
   EvAdventureCombatBaseHandler,
)

from .combat_base import EvAdventureCombatBaseHandler

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):
    """
    This is created on the combatant when combat starts. It tracks only 
    the combatant's side of the combat and handles when the next action 
    will happen.
 
    """
 
    def msg(self, message, broadcast=True):
        """See EvAdventureCombatBaseHandler.msg"""
        super().msg(message, combatant=self.obj, 
                    broadcast=broadcast, location=self.obj.location)
```

我們為 Twitch 戰鬥建立了一個 `EvAdventureCombatBaseHandler` 的子類別。父類別是 [Script](../../../Components/Scripts.md)，當 Script 位於某個物件「之上」時，該物件在 script 上可用作 `self.obj`。由於該處理程式旨在坐在戰鬥人員“身上”，因此 `self.obj` 是戰鬥人員，`self.obj.location` 是戰鬥人員所在的當前房間。透過使用 `super()`，我們可以使用這些 Twitch 特定的詳細資訊重複使用父類別的 `msg()` 方法。

(getting-the-sides-of-combat)=
### 取得戰鬥雙方

```python
# in evadventure/combat_twitch.py 

from evennia.utils import inherits_from

# ...

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):

    # ... 

    def get_sides(self, combatant):
         """
         Get a listing of the two 'sides' of this combat, from the 
         perspective of the provided combatant. The sides don't need 
         to be balanced.
 
         Args:
             combatant (Character or NPC): The basis for the sides.
             
         Returns:
             tuple: A tuple of lists `(allies, enemies)`, from the 
                 perspective of `combatant`. Note that combatant itself 
                 is not included in either of these.

        """
        # get all entities involved in combat by looking up their combathandlers
        combatants = [
            comb
            for comb in self.obj.location.contents
            if hasattr(comb, "scripts") and comb.scripts.has(self.key)
        ]
        location = self.obj.location

        if hasattr(location, "allow_pvp") and location.allow_pvp:
            # in pvp, everyone else is an enemy
            allies = [combatant]
            enemies = [comb for comb in combatants if comb != combatant]
        else:
            # otherwise, enemies/allies depend on who combatant is
            pcs = [comb for comb in combatants if inherits_from(comb, EvAdventureCharacter)]
            npcs = [comb for comb in combatants if comb not in pcs]
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

接下來我們加入我們自己的 `get_sides()` 方法的實作。這從所提供的`combatant`的角度呈現了戰鬥的各個方面。在 Twitch 戰鬥中，有一些東西可以識別戰鬥者：

- 他們在同一個位置
- 他們每個人都有一個 `EvAdventureCombatTwitchHandler` script 執行在自己身上

```{sidebar} inherits_from
由於如果您的類別以 _any_ 距離從父類別繼承，則 `inherits_from` 為 True，因此如果您要將 NPC 類別變更為也從我們的 Character 類別繼承，則此特定檢查將無法運作。在這種情況下，我們必須想出一些其他方法來比較這兩種型別的實體。
```
在 PvP 開放房間中，一切都是為了他們自己 - 其他人都被視為“敵人”。  否則，我們透過檢視 PC 是否繼承自 `EvAdventureCharacter`（我們的 PC 類）來將 PC 與 NPCs 分開 - 如果你是 PC，那麼 NPCs 就是你的敵人，反之亦然。 [inherits_from](evennia.utils.utils.inherits_from) 對於執行這些檢查非常有用 - 如果您以 _any_ 距離從 `EvAdventureCharacter` 繼承，它也會透過。

請注意，`allies` 不包括 `combatant` 本身，因此如果您正在與孤獨的敵人作戰，此方法的返回將為 `([], [enemy_obj])`。

(tracking-advantage-disadvantage)=
### 追蹤優勢/劣勢

```python
# in evadventure/combat_twitch.py 

from evennia import AttributeProperty

# ... 

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):

    self.advantage_against = AttributeProperty(dict) 
    self.disadvantage_against = AttributeProperty(dict)

    # ... 

    def give_advantage(self, recipient, target):
        """Let a recipient gain advantage against the target."""
        self.advantage_against[target] = True

    def give_disadvantage(self, recipient, target):
        """Let an affected party gain disadvantage against a target."""
        self.disadvantage_against[target] = True

    def has_advantage(self, combatant, target):
        """Check if the combatant has advantage against a target."""
        return self.advantage_against.get(target, False)

    def has_disadvantage(self, combatant, target):
        """Check if the combatant has disadvantage against a target."""
        return self.disadvantage_against.get(target, False)1

```

如上一課所示，操作呼叫這些方法來儲存以下事實：
特定的戰鬥者俱有優勢。

在這種 Twitch-combat 情況下，獲得優勢的總是定義了戰鬥處理程式的那個，因此我們實際上不需要使用 `recipient/combatant` 引數（它總是 `self.obj`） - 只有 `target` 很重要。

我們建立兩個新屬性來將關係儲存為字典。

(queue-action)=
### 佇列動作

```{code-block} python
:linenos:
:emphasize-lines: 17,26,30,43,44, 48, 49
# in evadventure/combat_twitch.py 

from evennia.utils import repeat, unrepeat
from .combat_base import (
    CombatActionAttack,
    CombatActionHold,
    CombatActionStunt,
    CombatActionUseItem,
    CombatActionWield,
    EvAdventureCombatBaseHandler,
)

# ... 

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):

    action_classes = {
         "hold": CombatActionHold,
         "attack": CombatActionAttack,
         "stunt": CombatActionStunt,
         "use": CombatActionUseItem,
         "wield": CombatActionWield,
     }

    action_dict = AttributeProperty(dict, autocreate=False)
    current_ticker_ref = AttributeProperty(None, autocreate=False)

    # ... 

    def queue_action(self, action_dict, combatant=None):
        """
        Schedule the next action to fire.

        Args:
            action_dict (dict): The new action-dict to initialize.
            combatant (optional): Unused.

        """
        if action_dict["key"] not in self.action_classes:
            self.obj.msg("This is an unknown action!")
            return

        # store action dict and schedule it to run in dt time
        self.action_dict = action_dict
        dt = action_dict.get("dt", 0)

        if self.current_ticker_ref:
            # we already have a current ticker going - abort it
            unrepeat(self.current_ticker_ref)
        if dt <= 0:
            # no repeat
            self.current_ticker_ref = None
        else:
                # always schedule the task to be repeating, cancel later
                # otherwise. We store the tickerhandler's ref to make sure 
                # we can remove it later
            self.current_ticker_ref = repeat(
                dt, self.execute_next_action, id_string="combat")

```

- **第 30 行**：`queue_action` 方法採用一個“Action dict”，表示戰鬥者下一步想要執行的動作。它必須是新增到 `action_classes` 屬性中的處理程式的鍵控操作之一（**第 17 行**）。我們沒有使用 `combatant` 關鍵字引數，因為我們已經知道戰鬥者是 `self.obj`。
- **第 43 行**：我們只是將給定的操作字典儲存在處理程式的 Attribute `action_dict` 中。簡單又有效！
- **第 44 行**：當您輸入 e.g 時。 `attack`，您希望在這種型別的戰鬥中看到 `attack` 指令自動重複，即使您不再輸入任何內容。為此，我們正在操作字典中尋找一個新鍵，指示該操作應該以一定的速率_重複_（`dt`，以秒為單位）。  如果沒有指定，我們只需假設它為零，就可以使其與所有操作指令相容。

[evennia.utils.utils.repeat](evennia.utils.utils.repeat) 和 [evennia.utils.utils.unrepeat](evennia.utils.utils.unrepeat) 是 [TickerHandler](../../../Components/TickerHandler.md) 的便利捷徑。您告訴 `repeat` 以一定的速率呼叫給定的方法/函式。您返回的是一個參考，您可以稍後使用該參考來「取消重複」（停止重複）。  我們確保將此引用儲存在 `current_ticker_ref` Attribute（**第 26 行**）中（我們並不關心它到底是什麼樣子，只是我們需要儲存它）。
 
- **第 48 行**：每當我們對新操作進行排隊（它可能會替換現有操作）時，我們必須確保殺死（不重複）任何正在進行的舊重複操作。否則，我們會一遍又一遍地觸發舊的操作，同時開始新的操作。
- **第 49 行**：如果設定了 `dt`，我們呼叫 `repeat` 以給定速率設定新的重複操作。我們儲存這個新參考。 `dt` 秒後，`.execute_next_action` 方法將觸發（我們將在下一節中建立它）。

(execute-an-action)=
### 執行一個動作

```{code-block} python
:linenos:
:emphasize-lines: 5,15,16,18,22,27

# in evadventure/combat_twitch.py

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):

    fallback_action_dict = AttributeProperty({"key": "hold", "dt": 0})

    # ... 

    def execute_next_action(self):
        """
        Triggered after a delay by the command
        """
        combatant = self.obj
        action_dict = self.action_dict
        action_class = self.action_classes[action_dict["key"]]
        action = action_class(self, combatant, action_dict)

        if action.can_use():
            action.execute()
            action.post_execute()

        if not action_dict.get("repeat", True):
            # not a repeating action, use the fallback (normally the original attack)
            self.action_dict = self.fallback_action_dict
            self.queue_action(self.fallback_action_dict)

        self.check_stop_combat()
```

這是在 `queue_action` 中 `dt` 秒後呼叫的方法。

- **第 5 行**：我們定義了「後備操作」。這是在一次性操作（不應重複的操作）完成後使用的。
- **第 15 行**：我們從 `action_dict` 中獲取 `'key'` 並使用 `action_classes` 對映來獲取操作類別（e.g。`ActionAttack` 我們在[此處]定義（./Beginner-Tutorial-Combat-Base.md#attack-action））。
- **第 16 行**：這裡我們用實際的當前資料初始化動作類別 - 戰鬥人員和 `action_dict`。這將呼叫類別上的 `__init__` 方法並使該操作可供使用。
```{sidebar} 新的動作字典鍵
總而言之，對於 twitch-combat 使用，我們現在引入了兩個新的操作字典鍵：
- `dt`：從將操作排隊到觸發需要等待多長時間（以秒為單位）。
- `repeat`：布林值決定操作在觸發後是否應自動再次排隊。
```
- **第 18 行**：這裡我們執行操作的使用方法 - 我們執行操作的地方。我們讓動作本身處理所有邏輯。
- **第 22 行**：我們檢查操作字典上的另一個可選標誌：`repeat`。除非已設定，否則我們將使用 **第 5 行** 上定義的後備操作。許多動作不應該重複 - 例如，對同一武器重複執行 `wield` 是沒有意義的。
- **第 27 行**：我們知道如何停止戰鬥非常重要。接下來我們就來寫這個方法。

(checking-and-stopping-combat)=
### 檢查並停止戰鬥

```{code-block} python 
:linenos: 
:emphasize-lines: 12,18,19

# in evadventure/combat_twitch.py 

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):

    # ... 

    def check_stop_combat(self):
        """
        Check if the combat is over.
        """

        allies, enemies = self.get_sides(self.obj)

        location = self.obj.location

        # only keep combatants that are alive and still in the same room
        allies = [comb for comb in allies if comb.hp > 0 and comb.location == location]
        enemies = [comb for comb in enemies if comb.hp > 0 and comb.location == location]

        if not allies and not enemies:
            self.msg("The combat is over. No one stands.", broadcast=False)
            self.stop_combat()
            return
        if not allies: 
            self.msg("The combat is over. You lost.", broadcast=False)
            self.stop_combat()
        if not enemies:
            self.msg("The combat is over. You won!", broadcast=False)
            self.stop_combat()

    def stop_combat(self):
        pass  # We'll finish this last
```

我們必須確保檢查戰鬥是否結束。

- **第12行**：透過我們的`.get_sides()`方法，我們可以輕鬆獲得衝突的雙方。
- **第 18、19 行**：我們讓每個人都還活著_並且仍然在同一個房間_。後一個條件很重要，以防我們離開戰鬥——你無法從另一個房間擊中敵人。

在 `stop_combat` 方法中，我們需要進行大量清理。我們將推遲實施此操作，直到我們寫出指令為止。請繼續閱讀。

(commands)=
## 指令

我們希望每個動作對映到一個 [Command](../../../Components/Commands.md) - 玩家可以傳遞給遊戲的實際輸入。

(base-combat-class)=
### 基礎戰鬥類

我們應該嘗試找到我們需要的指令之間的相似之處，並將它們分組到一個父類別中。當指令觸發時，它將按順序觸發自身的以下方法：

1. `cmd.at_pre_command()`
2. `cmd.parse()`
3. `cmd.func()`
4. `cmd.at_post_command()`

我們將為我們的父母覆蓋前兩個。

```{code-block} python
:linenos: 
:emphasize-lines: 23,49

# in evadventure/combat_twitch.py

from evennia import Command
from evennia import InterruptCommand 

# ... 

# after the combat handler class

class _BaseTwitchCombatCommand(Command):
    """
    Parent class for all twitch-combat commands.

    """

    def at_pre_command(self):
        """
        Called before parsing.

        """
        if not self.caller.location or not self.caller.location.allow_combat:
            self.msg("Can't fight here!")
            raise InterruptCommand()

    def parse(self):
        """
        Handle parsing of most supported combat syntaxes (except stunts).

        <action> [<target>|<item>]
        or
        <action> <item> [on] <target>

        Use 'on' to differentiate if names/items have spaces in the name.

        """
        self.args = args = self.args.strip()
        self.lhs, self.rhs = "", ""

        if not args:
            return

        if " on " in args:
            lhs, rhs = args.split(" on ", 1)
        else:
            lhs, *rhs = args.split(None, 1)
            rhs = " ".join(rhs)
        self.lhs, self.rhs = lhs.strip(), rhs.strip()

    def get_or_create_combathandler(self, target=None, combathandler_name="combathandler"):
        """
        Get or create the combathandler assigned to this combatant.

        """
        if target:
            # add/check combathandler to the target
            if target.hp_max is None:
                self.msg("You can't attack that!")
                raise InterruptCommand()

            EvAdventureCombatTwitchHandler.get_or_create_combathandler(target)
        return EvAdventureCombatTwitchHandler.get_or_create_combathandler(self.caller)
```

- **第23行**：如果目前位置不允許戰鬥，則所有戰鬥指令應立即退出。要在指令到達 `.func()` 之前停止該指令，我們必須提高 `InterruptCommand()`。
- **第 49 行**：新增一個輔助方法來取得指令處理程式很方便，因為我們所有的指令都將使用它。它依序呼叫我們從 `EvAdventureCombatTwitchHandler` 的父級繼承的類別方法 `get_or_create_combathandler`。

(in-combat-look-command)=
### 戰鬥中檢視指令

```python
# in evadventure/combat_twitch.py 

from evennia import default_cmds
from evennia.utils import pad

# ...

class CmdLook(default_cmds.CmdLook, _BaseTwitchCombatCommand):
    def func(self):
        # get regular look, followed by a combat summary
        super().func()
        if not self.args:
            combathandler = self.get_or_create_combathandler()
            txt = str(combathandler.get_combat_summary(self.caller))
            maxwidth = max(display_len(line) for line in txt.strip().split("\n"))
            self.msg(f"|r{pad(' Combat Status ', width=maxwidth, fillchar='-')}|n\n{txt}")
```

在戰鬥中，我們希望能夠執行 `look` 並獲得正常的外觀，但最後有額外的 `combat summary` （形式為 `Me (Hurt)  vs  Troll (Perfect)`）。所以

最後一行使用Evennia的`utils.pad`函式將文字「戰鬥狀態」兩邊用一條線包圍起來。

結果將是look指令輸出，後面緊接著

```shell
--------- Combat Status ----------
You (Wounded)  vs  Troll (Scraped)
```

(hold-command)=
### 保持指令

```python
class CmdHold(_BaseTwitchCombatCommand):
    """
    Hold back your blows, doing nothing.

    Usage:
        hold

    """

    key = "hold"

    def func(self):
        combathandler = self.get_or_create_combathandler()
        combathandler.queue_action({"key": "hold"})
        combathandler.msg("$You() $conj(hold) back, doing nothing.", self.caller)
```

「不執行任何操作」指令展示了以下所有指令如何運作的基本原理：

1. 取得戰鬥處理程式（如果已存在，則將建立或載入）。
2. 透過將操作字典傳遞給 `combathandler.queue_action` 方法來對操作進行排隊。
3. 向呼叫者確認他們現在已將此操作排隊。

(attack-command)=
### 攻擊指令

```python
# in evadventure/combat_twitch.py 

# ... 

class CmdAttack(_BaseTwitchCombatCommand):
    """
    Attack a target. Will keep attacking the target until
    combat ends or another combat action is taken.

    Usage:
        attack/hit <target>

    """

    key = "attack"
    aliases = ["hit"]
    help_category = "combat"

    def func(self):
        target = self.caller.search(self.lhs)
        if not target:
            return

        combathandler = self.get_or_create_combathandler(target)
        combathandler.queue_action(
            {"key": "attack", 
             "target": target, 
             "dt": 3, 
             "repeat": True}
        )
        combathandler.msg(f"$You() $conj(attack) $You({target.key})!", self.caller)
```

`attack` 指令變得非常簡單，因為我們在戰鬥處理程式和 `ActionAttack` 類別中完成了所有繁重的工作。請注意，我們在這裡將 `dt` 設定為固定的 `3`，但在更複雜的系統中，人們可以想像你的技能、武器和環境會影響你的攻擊所需的時間。

```python
# in evadventure/combat_twitch.py 

from .enums import ABILITY_REVERSE_MAP

# ... 

class CmdStunt(_BaseTwitchCombatCommand):
    """
    Perform a combat stunt, that boosts an ally against a target, or
    foils an enemy, giving them disadvantage against an ally.

    Usage:
        boost [ability] <recipient> <target>
        foil [ability] <recipient> <target>
        boost [ability] <target>       (same as boost me <target>)
        foil [ability] <target>        (same as foil <target> me)

    Example:
        boost STR me Goblin
        boost DEX Goblin
        foil STR Goblin me
        foil INT Goblin
        boost INT Wizard Goblin

    """

    key = "stunt"
    aliases = (
        "boost",
        "foil",
    )
    help_category = "combat"

    def parse(self):
        args = self.args

        if not args or " " not in args:
            self.msg("Usage: <ability> <recipient> <target>")
            raise InterruptCommand()

        advantage = self.cmdname != "foil"

        # extract data from the input

        stunt_type, recipient, target = None, None, None

        stunt_type, *args = args.split(None, 1)
        if stunt_type:
            stunt_type = stunt_type.strip().lower()

        args = args[0] if args else ""

        recipient, *args = args.split(None, 1)
        target = args[0] if args else None

        # validate input and try to guess if not given

        # ability is requried
        if not stunt_type or stunt_type not in ABILITY_REVERSE_MAP:
            self.msg(
                f"'{stunt_type}' is not a valid ability. Pick one of"
                f" {', '.join(ABILITY_REVERSE_MAP.keys())}."
            )
            raise InterruptCommand()

        if not recipient:
            self.msg("Must give at least a recipient or target.")
            raise InterruptCommand()

        if not target:
            # something like `boost str target`
            target = recipient if advantage else "me"
            recipient = "me" if advantage else recipient
        # if any values are still None at this point, we can't continue
        if None in (stunt_type, recipient, target):
            self.msg("Both ability, recipient and  target of stunt must be given.")
            raise InterruptCommand()

        # save what we found so it can be accessed from func()
        self.advantage = advantage
        self.stunt_type = ABILITY_REVERSE_MAP[stunt_type]
        self.recipient = recipient.strip()
        self.target = target.strip()

    def func(self):
        target = self.caller.search(self.target)
        if not target:
            return
        recipient = self.caller.search(self.recipient)
        if not recipient:
            return

        combathandler = self.get_or_create_combathandler(target)

        combathandler.queue_action(
            {
                "key": "stunt",
                "recipient": recipient,
                "target": target,
                "advantage": self.advantage,
                "stunt_type": self.stunt_type,
                "defense_type": self.stunt_type,
                "dt": 3,
            },
        )
        combathandler.msg("$You() prepare a stunt!", self.caller)

```

這看起來更長，但這只是因為特技指令應該理解許多不同的輸入結構，這取決於您是否試圖創造優勢或劣勢，以及盟友或敵人是否應該收到特技的效果。

請注意 `enums.ABILITY_REVERSE_MAP`（在[實用工具課程](./Beginner-Tutorial-Utilities.md) 中建立）對於將「str」輸入轉換為操作字典所需的 `Ability.STR` 非常有用。

一旦我們完成了字串解析，`func` 就很簡單了 - 我們找到目標和接收者，並使用它們來建立所需的操作字典來排隊。

(using-items)=
### 使用物品

```python
# in evadventure/combat_twitch.py 

# ... 

class CmdUseItem(_BaseTwitchCombatCommand):
    """
    Use an item in combat. The item must be in your inventory to use.

    Usage:
        use <item>
        use <item> [on] <target>

    Examples:
        use potion
        use throwing knife on goblin
        use bomb goblin

    """

    key = "use"
    help_category = "combat"

    def parse(self):
        super().parse()

        if not self.args:
            self.msg("What do you want to use?")
            raise InterruptCommand()

        self.item = self.lhs
        self.target = self.rhs or "me"

    def func(self):
        item = self.caller.search(
            self.item,
            candidates=self.caller.equipment.get_usable_objects_from_backpack()
        )
        if not item:
            self.msg("(You must carry the item to use it.)")
            return
        if self.target:
            target = self.caller.search(self.target)
            if not target:
                return

        combathandler = self.get_or_create_combathandler(self.target)
        combathandler.queue_action(
            {"key": "use", 
             "item": item, 
             "target": target, 
             "dt": 3}
        )
        combathandler.msg(
            f"$You() prepare to use {item.get_display_name(self.caller)}!", self.caller
        )
```

要使用某件物品，我們需要確保攜帶它。幸運的是，我們在[裝備課](./Beginner-Tutorial-Equipment.md)中的工作為我們提供了簡單的方法來搜尋合適的物件。

(wielding-new-weapons-and-equipment)=
### 揮舞新的武器和裝備

```python
# in evadventure/combat_twitch.py 

# ... 

class CmdWield(_BaseTwitchCombatCommand):
    """
    Wield a weapon or spell-rune. You wield the item,
        swapping with any other item(s) you were wielding before.

    Usage:
      wield <weapon or spell>

    Examples:
      wield sword
      wield shield
      wield fireball

    Note that wielding a shield will not replace the sword in your hand, 
        while wielding a two-handed weapon (or a spell-rune) will take 
        two hands and swap out what you were carrying.

    """

    key = "wield"
    help_category = "combat"

    def parse(self):
        if not self.args:
            self.msg("What do you want to wield?")
            raise InterruptCommand()
        super().parse()

    def func(self):
        item = self.caller.search(
            self.args, candidates=self.caller.equipment.get_wieldable_objects_from_backpack()
        )
        if not item:
            self.msg("(You must carry the item to wield it.)")
            return
        combathandler = self.get_or_create_combathandler()
        combathandler.queue_action({"key": "wield", "item": item, "dt": 3})
        combathandler.msg(f"$You() reach for {item.get_display_name(self.caller)}!", self.caller)

```

使用指令遵循與其他指令相同的模式。

(grouping-commands-for-use)=
## 使用分組指令

為了使這些指令可用，我們必須將它們新增至[指令集](../../../Components/Command-Sets.md)。

```python 
# in evadventure/combat_twitch.py 

from evennia import CmdSet

# ... 

# after the commands 

class TwitchCombatCmdSet(CmdSet):
    """
    Add to character, to be able to attack others in a twitch-style way.
    """

    def at_cmdset_creation(self):
        self.add(CmdAttack())
        self.add(CmdHold())
        self.add(CmdStunt())
        self.add(CmdUseItem())
        self.add(CmdWield())


class TwitchLookCmdSet(CmdSet):
    """
    This will be added/removed dynamically when in combat.
    """

    def at_cmdset_creation(self):
        self.add(CmdLook())


```

第一個 cmdset、`TwitchCombatCmdSet` 旨在新增到角色中。我們可以透過將 cmdset 新增至預設字元 cmdset 來永久執行此操作（如[初學者指令課程](../Part1/Beginner-Tutorial-Adding-Commands.md) 中所述）。在下面的測試部分中，我們將以另一種方式執行此操作。

那`TwitchLookCmdSet`呢？我們無法將其永久新增到我們的角色中，因為我們只希望這個特定版本的 `look` 在我們戰鬥時執行。

我們必須確保在戰鬥開始和結束時新增並清理它。

(combat-startup-and-cleanup)=
### 戰鬥啟動和清理

```{code-block} python 
:linenos: 
:emphasize-lines: 9,13,14,15,16

# in evadventure/combat_twitch.py

# ... 

class EvAdventureCombatTwitchHandler(EvAdventureCombatBaseHandler):

    # ... 

    def at_init(self): 
        self.obj.cmdset.add(TwitchLookCmdSet, persistent=False)

    def stop_combat(self): 
        self.queue_action({"key": "hold", "dt": 0})  # make sure ticker is killed
        del self.obj.ndb.combathandler
        self.obj.cmdset.remove(TwitchLookCmdSet)
        self.delete()
```

現在我們有了 Look 指令集，我們可以完成 Twitch 戰鬥處理程式了。

- **第 9 行**：`at_init` 方法是可用於所有型別分類實體的標準 Evennia 方法（包括 `Scripts`，這是我們的戰鬥處理程式）。與`at_object_creation`（僅在第一次建立物件時觸發一次）不同，每次將物件載入記憶體時都會呼叫`at_init`（通常在執行伺服器`reload`之後）。所以我們在這裡新增`TwitchLookCmdSet`。我們這樣做不是持久的，因為我們不希望每次重新載入時都新增越來越多的cmdsets。
- **第 13 行**：透過將 `dt` 的 `0` 的保留作業排隊，我們確保終止正在進行的 `repeat` 操作。如果沒有，它稍後仍會開火 - 並發現戰鬥處理程式已經消失。
- **第 14 行**：如果檢視我們如何定義 `get_or_create_combathandler` 類方法（我們在戰鬥期間用來獲取/建立戰鬥處理程式的方法），您會發現它將處理程式快取為我們傳送給它的對像上的 `.ndb.combathandler`。因此，我們刪除此處快取的引用以確保它已消失。
- **第15行**：我們刪除我們自己的表情-cmdset（記住`self.obj`是你，剛結束戰鬥的戰鬥者）。
- **第 16 行**：我們刪除戰鬥處理程式本身。


(unit-testing)=
## 單元測試

```{sidebar} 
有關單元測試的範例，請參閱 [evadventure/tests/test_combat.py](evennia.contrib.tutorials.evadventure.tests.test_combat) 中的 `evennia/contrib/tutorials`，以瞭解全套戰鬥測試的範例。
```

> 建立`evadventure/tests/test_combat.py`（如果您還沒有）。

Twitch 指令處理程式和指令都可以而且應該進行單元測試。  Evennia 的特殊 `EvenniaCommandTestMixin` 類別使指令測試變得更加容易。這使得 `.call` 方法可用，並且可以輕鬆檢查指令是否返回您期望的結果。

這是一個例子：

```python 
# in evadventure/tests/test_combat.py 

from unittest.mock import Mock, patch
from evennia.utils.test_resources import EvenniaCommandTestMixin

from .. import combat_twitch

# ...

class TestEvAdventureTwitchCombat(EvenniaCommandTestMixin):

    def setUp(self): 
        self.combathandler = (
                combat_twitch.EvAdventureCombatTwitchHandler.get_or_create_combathandler(
            self.char1, key="combathandler") 
        )
   
    @patch("evadventure.combat_twitch.unrepeat", new=Mock())
    @patch("evadventure.combat_twitch.repeat", new=Mock())
    def test_hold_command(self): 
        self.call(combat_twitch, CmdHold(), "", "You hold back, doing nothing.")
        self.assertEqual(self.combathandler.action_dict, {"key": "hold"})
            
```

`EvenniaCommandTestMixin` 有一些預設物件，包括我們在這裡使用的 `self.char1`。

兩行 `@patch` 是 Python [裝飾器](https://realpython.com/primer-on-python-decorators/)，用於「修補」`test_hold_command` 方法。他們所做的基本上是說「在下面的方法中，每當任何程式碼嘗試存取 `evadventure.combat_twitch.un/repeat` 時，只需返回模擬物件」。

我們進行此修補是一種簡單的方法，以避免在單元測試中建立計時器 - 這些計時器將在測試完成後完成（包括刪除其物件），從而失敗。

在測試中，我們使用 `self.call()` 方法明確觸發指令（不含引數）並檢查輸出是否符合我們的預期。  最後，我們檢查戰鬥處理程式是否設定正確，並將操作字典儲存在其自身上。

(a-small-combat-test)=
## 實戰小測試

```{sidebar}
您可以在 [batchscripts/twitch_combat_demo.ev](github:evennia/contrib/tutorials/evadventure/batchscripts/twitch_combat_demo.ev) `evennia/contrib/tutorials/evadventure` 處找到範例批次指令 script
```
顯示各個程式碼片段的工作（單元測試）並不足以確保您的戰鬥系統確實運作。我們需要一起測試所有部分。這通常稱為_功能測試_。雖然功能測試也可以自動化，但能夠實際看到我們的程式碼在執行不是很有趣嗎？

這是我們進行最小測試所需的：

 - 一個可以進行戰鬥的房間。
 - NPC 進行攻擊（它不會做任何反擊，因為我們還沒有增加任何 AI）
 - 我們可以`wield`的武器
 - 一個物品（例如藥水）我們可以`use`。

雖然您可以在遊戲中手動建立這些，但建立 [batch-command script](../../../Components/Batch-Command-Processor.md) 來設定測試環境會很方便。

> 建立一個新的子資料夾 `evadventure/batchscripts/` （如果它尚不存在）


> 建立一個新檔案`evadventure/combat_demo.ev`（注意，它是`.ev`而不是`.py`！）

批次指令檔案是一個文字檔案，其中包含正常的遊戲內指令，每行一個，以 `#` 開頭的行分隔（所有指令列之間都需要這些指令）。它看起來是這樣的：

```
# Evadventure combat demo 

# start from limbo

tel #2

# turn ourselves into a evadventure-character

type self = evadventure.characters.EvAdventureCharacter

# assign us the twitch combat cmdset (requires superuser/developer perms)

py self.cmdset.add("evadventure.combat_twitch.TwitchCombatCmdSet", persistent=True)

# Create a weapon in our inventory (using all defaults)

create sword:evadventure.objects.EvAdventureWeapon

# create a consumable to use

create potion:evadventure.objects.EvAdventureConsumable

# dig a combat arena

dig arena:evadventure.rooms.EvAdventureRoom = arena,back

# go to arena

arena

# allow combat in this room

set here/allow_combat = True

# create a dummy enemy to hit on

create/drop dummy puppet;dummy:evadventure.npcs.EvAdventureNPC

# describe the dummy

desc dummy = This is is an ugly training dummy made out of hay and wood.

# make the dummy crazy tough

set dummy/hp_max = 1000

# 

set dummy/hp = 1000
```

使用開發者/超級使用者帳戶登入遊戲並執行

    > batchcmd evadventure.batchscripts.twitch_combat_demo 
    
這應該會將您置於與虛擬人一起的競技場中（如果沒有，請檢查輸出中是否有錯誤！如果需要重新開始，請使用 `objects` 和 `delete` 指令列出並刪除物件。）

現在您可以嘗試`attack dummy`，並且應該能夠猛擊假人（降低其生命值以測試摧毀它）。使用`back`「逃離」戰鬥。

(conclusions)=
## 結論

這是一個很大的教訓！儘管我們的戰鬥系統不是很複雜，但仍然有許多活動部件需要記住。

此外，雖然非常簡單，但該系統也有很大的發展空間。您可以輕鬆地從中擴充套件或將其用作您自己的遊戲的靈感。

接下來我們將嘗試在回合製框架中實現同樣的目標！