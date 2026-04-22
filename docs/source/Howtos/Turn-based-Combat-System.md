(turn-based-combat-system)=
# 回合製戰鬥系統


本教學提供了 Evennia 的完整（如果簡化）戰鬥系統的範例。受到了啟發
透過在[郵寄
列表](https://groups.google.com/forum/#!msg/evennia/wnJNM2sXSfs/-dbLRrgWnYMJ)。

(overview-of-combat-system-concepts)=
## 戰鬥系統概念概述

大多數MUDs會使用某種戰鬥系統。有幾個主要的變體：

- _自由形式_ - 最簡單的戰鬥形式，常見於 MUSH 風格的角色扮演遊戲。這意味著系統僅提供骰子滾輪或可能的指令來比較技能並吐出結果。擲骰子是為了根據遊戲規則解決戰鬥並指揮場景。可能需要遊戲管理員來解決規則爭議。
- _Twitch_ - 這是傳統的 MUD hack&slash 風格的戰鬥。在抽搐系統中，正常的「移動和探索模式」和「戰鬥模式」之間通常沒有區別。你輸入攻擊指令，系統會計算攻擊是否命中以及造成了多少傷害。通常，攻擊指令具有某種逾時或恢復/平衡概念，以減少垃圾郵件或用戶端指令碼的優勢。最簡單的系統只意味著一遍又一遍地輸入`kill <target>`，而更複雜的抽搐系統包括從防禦姿態到戰術定位的任何內容。
- _回合製_ - 回合製系統意味著系統會暫停以確保所有戰鬥人員可以在繼續之前選擇他們的行動。在某些系統中，此類輸入的動作會立即發生（例如基於抽搐），而在其他系統中，解決方案會在回合結束時同時發生。回合製的缺點是遊戲必須切換到“戰鬥模式”，並且還需要特別注意如何應對新的戰鬥人員和時間的流逝。優點是成功不依賴打字速度或設定快速用戶端巨集。這可能允許將情緒作為戰鬥的一部分，這對角色扮演遊戲來說是一個優勢。

要實現自由形式的戰鬥系統，您只需要一個擲骰子和一本角色扮演規則手冊。有關骰子滾輪的範例，請參閱 [contrib/dice.py](../Contribs/Contrib-Dice.md)。要在基於抽搐的系統上實施，您基本上需要一些戰鬥[指令](../Components/Commands.md)，可能是帶有[冷卻時間](./Howto-Command-Cooldown.md)的指令。您還需要一個使用它的[遊戲規則模組](./Implementing-a-game-rule-system.md)。我們將在這裡重點關注回合製遊戲。

(tutorial-overview)=
## 教學概述

本教學將實現稍微複雜的回合製戰鬥系統。我們的範例具有以下屬性：

- 戰鬥以`attack <target>`開始，這將啟動戰鬥模式。
- 角色可以使用 `attack <target>` 加入正在進行的戰鬥，對抗已經在場的角色
戰鬥。
- 每個回合，每個戰鬥角色都會輸入兩個指令，它們的內部順序很重要，並且按照每個戰鬥者給出的順序進行一對一比較。  `say` 和 `pose` 的使用是免費的。
- 指令（在我們的範例中）很簡單；它們可以是`hit <target>`、`feint <target>` 或`parry <target>`。他們還可以`defend`，一種通用的被動防禦。最後他們可能會選擇`disengage/flee`。
- 攻擊時，我們使用經典的[石頭剪刀布](https://en.wikipedia.org/wiki/Rock-paper- scissors)機制來確定成功：`hit`擊敗`feint`，`feint`擊敗`parry`，`hit`擊敗`hit`。 `defend` 是一般被動動作，有一定百分比的機會戰勝 `hit`（僅）。
- `disengage/flee` 必須連續輸入兩次，並且只有在當時沒有 `hit` 反對的情況下才會成功。如果是這樣，他們將離開戰鬥模式。
- 一旦每個玩家輸入兩個指令，所有指令將按順序解析並報告結果。然後新的回合開始。
- 如果玩家太慢，回合將逾時，任何未設定的指令將被設定為`defend`。

為了建立戰鬥系統，我們需要以下元件：

- 戰鬥處理者。這是系統的主要機制。這是為每次戰鬥建立的 [Script](../Components/Scripts.md) 物件。  它不分配給特定的物件，而是由戰鬥角色共享並處理所有戰鬥資訊。由於 Scripts 是資料庫實體，這也意味著戰鬥不會受到伺服器重新載入的影響。
- 戰鬥[指令集](../Components/Command-Sets.md)，包含戰鬥所需的相關指令，例如各種攻擊/防禦選項和退出戰鬥模式的`flee/disengage`指令。
- 規則解析系統。 [規則系統教學](./Implementing-a-game-rule-system.md)中描述了製作此類模組的基礎知識。我們只會在這裡為我們的最終回合戰鬥解決方案繪製這樣一個模組。
- 用於啟動戰鬥模式的`attack` [指令](../Components/Commands.md)。這被新增到預設指令集中。它將建立戰鬥處理程式並向其中新增角色。它還會將戰鬥指令集指派給角色。

(the-combat-handler)=
## 戰鬥處理者

_combat handler_ 是作為獨立的 [Script](../Components/Scripts.md) 實現的。  當第一個角色決定攻擊另一個角色時，會建立此Script，並在無人再戰鬥時刪除。每個處理程式代表一次戰鬥例項，並且僅代表一次戰鬥。每個戰鬥例項可以容納任意數量的角色，但每個角色一次只能參與一場戰鬥（玩家將
需要先脫離第一次戰鬥才能加入另一場戰鬥）。

我們不將這個 Script 儲存在任何特定角色上的原因是因為任何角色都可能隨時離開戰鬥。相反，script 包含對參與戰鬥的所有角色的引用。  反之亦然，所有角色都持有對當前戰鬥處理程式的反向引用。雖然我們在這裡不經常使用它，但這可能允許角色上的戰鬥指令直接存取和更新戰鬥處理程式狀態。

_注意：實現戰鬥處理程式的另一種方法是使用普通的 Python 物件並使用 [TickerHandler](../Components/TickerHandler.md) 處理計時。這需要在角色上新增自訂掛鉤方法或實作 TickerHandler 類別的自訂子層級來追蹤回合。雖然 TickerHandler 易於使用，但 Script 在此 case._ 中提供了更多功能

這是一個基本的戰鬥處理程式。假設我們的遊戲資料夾名為`mygame`，我們將其儲存在
`mygame/typeclasses/combat_handler.py`：

```python
# mygame/typeclasses/combat_handler.py

import random
from evennia import DefaultScript
from world.rules import resolve_combat

class CombatHandler(DefaultScript):
    """
    This implements the combat handler.
    """

    # standard Script hooks 

    def at_script_creation(self):
        "Called when script is first created"

        self.key = f"combat_handler_{random.randint(1, 1000)}"
        self.desc = "handles combat"
        self.interval = 60 * 2  # two minute timeout
        self.start_delay = True
        self.persistent = True   

        # store all combatants
        self.db.characters = {}
        # store all actions for each turn
        self.db.turn_actions = {}
        # number of actions entered per combatant
        self.db.action_count = {}

    def _init_character(self, character):
        """
        This initializes handler back-reference 
        and combat cmdset on a character
        """
        character.ndb.combat_handler = self
        character.cmdset.add("commands.combat.CombatCmdSet")

    def _cleanup_character(self, character):
        """
        Remove character from handler and clean 
        it of the back-reference and cmdset
        """
        dbref = character.id 
        del self.db.characters[dbref]
        del self.db.turn_actions[dbref]
        del self.db.action_count[dbref]        
        del character.ndb.combat_handler
        character.cmdset.delete("commands.combat.CombatCmdSet")

    def at_start(self):
        """
        This is called on first start but also when the script is restarted
        after a server reboot. We need to re-assign this combat handler to 
        all characters as well as re-assign the cmdset.
        """
        for character in self.db.characters.values():
            self._init_character(character)

    def at_stop(self):
        "Called just before the script is stopped/destroyed."
        for character in list(self.db.characters.values()):
            # note: the list() call above disconnects list from database
            self._cleanup_character(character)

    def at_repeat(self):
        """
        This is called every self.interval seconds (turn timeout) or 
        when force_repeat is called (because everyone has entered their 
        commands). We know this by checking the existence of the
        `normal_turn_end` NAttribute, set just before calling 
        force_repeat.
        
        """
        if self.ndb.normal_turn_end:
            # we get here because the turn ended normally
            # (force_repeat was called) - no msg output
            del self.ndb.normal_turn_end
        else:        
            # turn timeout
            self.msg_all("Turn timer timed out. Continuing.")
        self.end_turn()

    # Combat-handler methods

    def add_character(self, character):
        "Add combatant to handler"
        dbref = character.id
        self.db.characters[dbref] = character        
        self.db.action_count[dbref] = 0
        self.db.turn_actions[dbref] = [("defend", character, None),
                                       ("defend", character, None)]
        # set up back-reference
        self._init_character(character)
       
    def remove_character(self, character):
        "Remove combatant from handler"
        if character.id in self.db.characters:
            self._cleanup_character(character)
        if not self.db.characters:
            # if no more characters in battle, kill this handler
            self.stop()

    def msg_all(self, message):
        "Send message to all combatants"
        for character in self.db.characters.values():
            character.msg(message)

    def add_action(self, action, character, target):
        """
        Called by combat commands to register an action with the handler.

         action - string identifying the action, like "hit" or "parry"
         character - the character performing the action
         target - the target character or None

        actions are stored in a dictionary keyed to each character, each
        of which holds a list of max 2 actions. An action is stored as
        a tuple (character, action, target). 
        """
        dbref = character.id
        count = self.db.action_count[dbref]
        if 0 <= count <= 1: # only allow 2 actions            
            self.db.turn_actions[dbref][count] = (action, character, target)
        else:        
            # report if we already used too many actions
            return False
        self.db.action_count[dbref] += 1
        return True

    def check_end_turn(self):
        """
        Called by the command to eventually trigger 
        the resolution of the turn. We check if everyone
        has added all their actions; if so we call force the
        script to repeat immediately (which will call
        `self.at_repeat()` while resetting all timers). 
        """
        if all(count > 1 for count in self.db.action_count.values()):
            self.ndb.normal_turn_end = True
            self.force_repeat() 

    def end_turn(self):
        """
        This resolves all actions by calling the rules module. 
        It then resets everything and starts the next turn. It
        is called by at_repeat().
        """        
        resolve_combat(self, self.db.turn_actions)

        if len(self.db.characters) < 2:
            # less than 2 characters in battle, kill this handler
            self.msg_all("Combat has ended")
            self.stop()
        else:
            # reset counters before next turn
            for character in self.db.characters.values():
                self.db.characters[character.id] = character
                self.db.action_count[character.id] = 0
                self.db.turn_actions[character.id] = [("defend", character, None),
                                                  ("defend", character, None)]
            self.msg_all("Next turn begins ...")
```

這實現了我們的戰鬥處理程式的所有有用屬性。此 Script 將在重新啟動後繼續存在
當它重新上線時會自動重新宣告自己。即使是目前的狀態
戰鬥應該不受影響，因為它每次都會儲存在屬性中。需要注意的重要部分
是使用Script的標準`at_repeat`鉤子和`force_repeat`方法來結束每一回合。
這允許一切都透過相同的機制，並且程式碼重複最少。

此處理程式中不存在玩家檢視他們設定或更改的操作的方法
新增後（但在最後一個新增他們的操作之前）他們的操作。我們將此作為練習。

(combat-commands)=
## 戰鬥指令

我們的戰鬥指令 - 在戰鬥期間我們可以使用的指令 - （在我們的範例中）非常簡單。在完整的實現中，可用的指令可能由玩家持有的武器或他們所知道的技能決定。

我們在`mygame/commands/combat.py`中建立它們。

```python
# mygame/commands/combat.py

from evennia import Command

class CmdHit(Command):
    """
    hit an enemy

    Usage:
      hit <target>

    Strikes the given enemy with your current weapon.
    """
    key = "hit"
    aliases = ["strike", "slash"]
    help_category = "combat"

    def func(self):
        "Implements the command"
        if not self.args:
            self.caller.msg("Usage: hit <target>")
            return 
        target = self.caller.search(self.args)
        if not target:
            return
        ok = self.caller.ndb.combat_handler.add_action("hit", 
                                                       self.caller, 
                                                       target) 
        if ok:
            self.caller.msg("You add 'hit' to the combat queue")
        else:
            self.caller.msg("You can only queue two actions per turn!")
 
        # tell the handler to check if turn is over
        self.caller.ndb.combat_handler.check_end_turn()
```

其他指令`CmdParry`、`CmdFeint`、`CmdDefend` 和`CmdDisengage` 看起來基本上相同。我們還應該新增一個自訂 `help` 指令來列出所有可用的戰鬥指令及其用途。

我們只需要將它們全部放在cmdset中。我們在同一模組的末尾執行此操作：

```python
# mygame/commands/combat.py

from evennia import CmdSet
from evennia import default_cmds

class CombatCmdSet(CmdSet):
    key = "combat_cmdset"
    mergetype = "Replace"
    priority = 10 
    no_exits = True

    def at_cmdset_creation(self):
        self.add(CmdHit())
        self.add(CmdParry())
        self.add(CmdFeint())
        self.add(CmdDefend())
        self.add(CmdDisengage())    
        self.add(CmdHelp())
        self.add(default_cmds.CmdPose())
        self.add(default_cmds.CmdSay())
```

(rules-module)=
## 規則模組

實作規則模組的一般方法可以在[規則系統教學](Implementing-a-game- rule-system)中找到。正確的解決方案可能需要我們更改角色來儲存力量、武器技能等內容。因此，對於這個例子，我們將採用一個非常簡單的石頭剪刀布型別的設定，並新增一些隨機性。我們不會在這裡處理傷害，而只是宣佈每回合的結果。在真實的系統中，角色物件將儲存統計資料來影響他們的技能，他們選擇的武器會影響選擇，他們將能夠失去生命值等。

每個回合中都有“子回合”，每個子回合由每個角色的一個動作組成。每個子回合中的動作同時發生，只有當它們全部解決後，我們才會進入下一個子回合（或結束整個回合）。

*注意：在我們的簡單範例中，子回合不會相互影響（`disengage/flee` 除外），回合之間也不會延續任何效果。回合製系統的真正威力在於新增
不過，這裡有真正的戰術可能性；例如，如果你的攻擊被招架，你可能會出局
平衡，你的下一步就會處於不利地位。一次成功的佯攻將會為
隨後的攻擊等等......*

我們的石頭剪刀布設定是這樣的：

- `hit` 擊敗 `feint` 和 `flee/disengage`。它有隨機機會失敗於 `defend`。
- `parry` 勝過 `hit`。
- `feint` 擊敗 `parry`，然後算 `hit`。
- `defend`什麼都不做，但有機會擊敗`hit`。
- `flee/disengage`必須連續成功兩次（i.e。在回合中一次未被`hit`擊敗）。如果是這樣，角色就會離開戰鬥。

```python
# mygame/world/rules.py

import random


# messages 

def resolve_combat(combat_handler, actiondict):
    """
    This is called by the combat handler
    actiondict is a dictionary with a list of two actions
    for each character:
    {char.id:[(action1, char, target), (action2, char, target)], ...}
    """
    flee = {}  # track number of flee commands per character
    for isub in range(2):
        # loop over sub-turns
        messages = []
        for subturn in (sub[isub] for sub in actiondict.values()):
            # for each character, resolve the sub-turn
            action, char, target = subturn
            if target:
                taction, tchar, ttarget = actiondict[target.id][isub]
            if action == "hit":
                if taction == "parry" and ttarget == char:
                    messages.append(
                        f"{char} tries to hit {tchar}, but {tchar} parries the attack!"
                    )
                elif taction == "defend" and random.random() < 0.5:
                    messages.append(
                        f"{tchar} defends against the attack by {char}."
                    )
                elif taction == "flee":
                    flee[tchar] = -2
                    messages.append(
                        f"{char} stops {tchar} from disengaging, with a hit!"
                    )
                else:
                    messages.append(
                        f"{char} hits {tchar}, bypassing their {taction}!"
                    )
            elif action == "parry":
                if taction == "hit":
                    messages.append(f"{char} parries the attack by {tchar}.")
                elif taction == "feint":
                    messages.append(
                        f"{char} tries to parry, but {tchar} feints and hits!"
                    )
                else:
                    messages.append(f"{char} parries to no avail.")
            elif action == "feint":
                if taction == "parry":
                    messages.append(
                        f"{char} feints past {tchar}'s parry, landing a hit!"
                    )
                elif taction == "hit":
                    messages.append(f"{char} feints but is defeated by {tchar}'s hit!")
                else:
                    messages.append(f"{char} feints to no avail.")
            elif action == "defend":
                messages.append(f"{char} defends.")
            elif action == "flee":
                if char in flee:
                    flee[char] += 1
                else:
                    flee[char] = 1
                    messages.append(
                        f"{char} tries to disengage (two subsequent turns needed)"
                    )

        # echo results of each subturn
        combat_handler.msg_all("\n".join(messages))

    # at the end of both sub-turns, test if anyone fled
    for (char, fleevalue) in flee.items():
        if fleevalue == 2:
            combat_handler.msg_all(f"{char} withdraws from combat.")
            combat_handler.remove_character(char)
```

為了簡單起見（並節省空間），這個範例規則模組實際上解析每個交換兩次 - 第一次是在到達每個字元時，然後是在處理目標時。另外，由於我們在這裡使用戰鬥處理程式的 `msg_all` 方法，系統將變得相當垃圾。為了清理它，我們可以想像追蹤所有可能的互動，以確保每一對僅被處理和報告一次。

(combat-initiator-command)=
## 戰鬥發動者指令

這是我們需要的最後一個元件，啟動戰鬥的指令。這會將一切聯絡在一起。我們將其與其他戰鬥指令一起儲存。

```python
# mygame/commands/combat.py

from evennia import create_script


class CmdAttack(Command):
    """
    initiates combat

    Usage:
      attack <target>

    This will initiate combat with <target>. If <target is
    already in combat, you will join the combat. 
    """
    key = "attack"
    help_category = "General"

    def func(self):
        "Handle command"
        if not self.args:
            self.caller.msg("Usage: attack <target>")
            return
        target = self.caller.search(self.args)
        if not target:
            return
        # set up combat
        if target.ndb.combat_handler:
            # target is already in combat - join it            
            target.ndb.combat_handler.add_character(self.caller)
            target.ndb.combat_handler.msg_all(f"{self.caller} joins combat!")
        else:
            # create a new combat handler
            chandler = create_script("combat_handler.CombatHandler")
            chandler.add_character(self.caller)
            chandler.add_character(target)
            self.caller.msg(f"You attack {target}! You are in combat.")
            target.msg(f"{self.caller} attacks you! You are in combat.")       
```

`attack` 指令不會進入戰鬥 cmdset，而是進入預設的 cmdset。請參閱e.g。如果您不確定如何執行此操作，請參閱[新增指令教學](Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)。

(expanding-the-example)=
## 擴充範例

此時你應該有一個簡單但靈活的回合製戰鬥系統。在這個例子中我們採取了一些捷徑和簡化。在戰鬥中向玩家輸出的內容可能過於冗長，而在告知周圍事物時又過於有限。可能需要更改指令或列出指令、檢視誰在戰鬥等的方法 - 這將需要對每個遊戲和風格進行遊戲測試。目前還沒有顯示與戰鬥在同一個房間的其他人的資訊 - 一些不太詳細的資訊可能應該回顯到房間中
向其他人展示正在發生的事情。