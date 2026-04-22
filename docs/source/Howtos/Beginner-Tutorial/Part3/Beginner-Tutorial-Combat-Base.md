(combat-base-framework)=
# 作戰基地框架

戰鬥是許多遊戲的核心。其具體運作方式很大程度取決於遊戲。在本課中，我們將建立一個框架來實現兩種常見的風格：

- 「基於抽搐的」戰鬥（[此處的特定課程](./Beginner-Tutorial-Combat-Twitch.md)）意味著您透過輸入指令來執行戰鬥動作，並在一段延遲後（這可能取決於您的技能等），該動作發生。之所以稱為“抽搐”，是因為行動通常發生得足夠快，以至於改變策略可能需要快速思考和“抽動扳機手指”。
- 「回合製」戰鬥（[具體教訓]（./Beginner-Tutorial-Combat-Turnbased.md））意味著玩家以清晰的回合輸入動作。輸入/排隊操作的超時通常比基於抽搐的風格長得多。一旦每個人都做出了選擇（或達到超時），每個人的行動都會立即發生，然後在下一回合開始。這種戰鬥方式需要較少的玩家反應。

我們將設計一個支援這兩種風格的基礎戰鬥系統。

- 我們需要`CombatHandler`來追蹤戰鬥進度。這將是 [Script](../../../Components/Scripts.md)。 Twitch 戰鬥和回合製戰鬥的具體工作方式（以及存放位置）會有所不同。我們將在本課中建立其通用框架。
- 戰鬥分為_動作_。我們希望能夠透過更多可能的行動輕鬆擴充套件我們的戰鬥。操作需要 Python 程式碼來顯示執行操作時實際發生的情況。我們將在`Action`類別中定義這樣的程式碼。
- 我們還需要一種方法來描述給定操作的_特定例項_。也就是說，當我們做出「攻擊」動作時，我們至少需要知道誰在被攻擊。為此，我們將使用 Python `dicts`，我們稱之為 `action_dicts`。

(combathandler)=
## CombatHandler

> 建立一個新模組`evadventure/combat_base.py`

```{sidebar}
在 `evennia/contrib/tutorials/evadventure/` 下的 [combat_base.py](evennia.contrib.tutorials.evadventure.combat_base) 中，您將找到基本戰鬥模組的完整實作。
```
我們的「戰鬥處理程式」將負責戰鬥方面的管理。它需要是_持久的_（即使我們重新載入伺服器，你的戰鬥也應該繼續進行）。

建立 CombatHandler 有點像第 22 條軍規 - 它的工作原理取決於 Actions 和 Action-dicts 的外觀。但如果沒有 CombatHandler，就很難知道如何設計 Actions 和 Action-dicts。因此，我們將從其總體結構開始，並在本課後面填寫詳細資料。

下面，帶有 `pass` 的方法將在本課中填寫，而那些提高 `NotImplementedError` 的方法將在 Twitch/回合製戰鬥中有所不同，並將在本課之後的各自課程中實施。

```python 
# in evadventure/combat_base.py 

from evennia import DefaultScript


class CombatFailure(RuntimeError):
	"""If some error happens in combat"""
    pass


class EvAdventureCombatBaseHandler(DefaultSCript): 
    """ 
	This should be created when combat starts. It 'ticks' the combat 
	and tracks all sides of it.
	
    """
    # common for all types of combat

    action_classes = {}          # to fill in later 
    fallback_action_dict = {}

    @classmethod 
    def get_or_create_combathandler(cls, obj, **kwargs): 
        """ Get or create combathandler on `obj`.""" 
        pass

    def msg(self, message, combatant=None, broadcast=True, location=True): 
        """ 
        Send a message to all combatants.
		
        """
        pass  # TODO
     
    def get_combat_summary(self, combatant):
        """ 
        Get a nicely formatted 'battle report' of combat, from the 
        perspective of the combatant.
        
    	""" 
        pass  # TODO

	# implemented differently by Twitch- and Turnbased combat

    def get_sides(self, combatant):
        """ 
        Get who's still alive on the two sides of combat, as a 
        tuple `([allies], [enemies])` from the perspective of `combatant` 
	        (who is _not_ included in the `allies` list.
        
        """
        raise NotImplementedError 

    def give_advantage(self, recipient, target): 
        """ 
        Give advantage to recipient against target.
        
        """
        raise NotImplementedError 

    def give_disadvantage(self, recipient, target): 
        """
        Give disadvantage to recipient against target. 

        """
        raise NotImplementedError

    def has_advantage(self, combatant, target): 
        """ 
        Does combatant have advantage against target?
        
        """ 
        raise NotImplementedError 

    def has_disadvantage(self, combatant, target): 
        """ 
        Does combatant have disadvantage against target?
        
        """ 
        raise NotImplementedError

    def queue_action(self, combatant, action_dict):
        """ 
        Queue an action for the combatant by providing 
        action dict.
        
        """ 
        raise NotImplementedError

    def execute_next_action(self, combatant): 
        """ 
        Perform a combatant's next action.
        
        """ 
        raise NotImplementedError

    def start_combat(self): 
        """ 
        Start combat.
        
    	""" 
    	raise NotImplementedError
    
    def check_stop_combat(self): 
        """
        Check if the combat is over and if it should be stopped.
         
        """
        raise NotImplementedError 
        
    def stop_combat(self): 
        """ 
        Stop combat and do cleanup.
        
        """
        raise NotImplementedError


```

戰鬥處理程式是[Script](../../../Components/Scripts.md)。 Scripts 是型別分類實體，這意味著它們永續性地儲存在資料庫中。 Scripts 可以選擇儲存在其他物件「上」（例如角色或房間），或在沒有任​​何此類連線的情況下儲存為「全域」。雖然 Scripts 有一個可選的計時器元件，但預設情況下它不處於活動狀態，並且 Scripts 通常用作普通儲存。由於 Scripts 在遊戲中不存在，因此它們非常適合在各種「系統」上儲存資料，包括我們的戰鬥。

讓我們實作我們需要的通用方法。

(combathandlerget_or_create_combathandler)=
### CombatHandler。 get_or_create_combathandler

一種快速獲取正在進行的戰鬥和戰鬥人員的戰鬥處理程式的輔助方法。

我們期望在一個物件「上」建立script（我們還不知道哪個物件，但我們期望它是一個型別分類的實體）。

```python
# in evadventure/combat_base.py

from evennia import create_script

# ... 

class EvAdventureCombatBaseHandler(DefaultScript): 

    # ... 

    @classmethod
    def get_or_create_combathandler(cls, obj, **kwargs):
        """
        Get or create a combathandler on `obj`.
    
        Args:
            obj (any): The Typeclassed entity to store this Script on. 
        Keyword Args:
            combathandler_key (str): Identifier for script. 'combathandler' by
                default.
            **kwargs: Extra arguments to the Script, if it is created.
    
        """
        if not obj:
            raise CombatFailure("Cannot start combat without a place to do it!")
    
        combathandler_key = kwargs.pop("key", "combathandler")
        combathandler = obj.ndb.combathandler
        if not combathandler or not combathandler.id:
            combathandler = obj.scripts.get(combathandler_key).first()
            if not combathandler:
                # have to create from scratch
                persistent = kwargs.pop("persistent", True)
                combathandler = create_script(
                    cls,
                    key=combathandler_key,
                    obj=obj,
                    persistent=persistent,
                    **kwargs,
                )
            obj.ndb.combathandler = combathandler
        return combathandler

	# ... 

```

此輔助方法使用 `obj.scripts.get()` 來查詢戰鬥 script 是否已經存在於所提供的 `obj` 上。如果沒有，它將使用 Evennia 的 [create_script](evennia.utils.create.create_script) 函式來建立它。為了獲得額外的速度，我們將處理程式快取為 `obj.ndb.combathandler` `.ndb.`（非資料庫）意味著處理程式僅快取在記憶體中。

```{sidebar} 檢查.id（或.pk）
當從快取中獲取它時，我們確保也檢查我們獲得的戰鬥處理程式是否有一個不是 `None` 的資料庫 `.id` （我們還可以檢查 `.pk`，代表「主鍵」）。如果是 `None`，這表示資料庫實體已被刪除，我們剛剛從記憶體中獲取了其快取的 Python 表示形式 - 我們需要重新建立它。
```

`get_or_create_combathandler` 被修飾為 [classmethod](https://docs.python.org/3/library/functions.html#classmethod)，這意味著它應該直接在處理程式類別上使用（而不是在所述類別的例項上）。這是有道理的，因為該方法實際上應該傳回新例項。

作為類別方法，我們需要直接在類別上呼叫它，如下所示：

```python
combathandler = EvAdventureCombatBaseHandler.get_or_create_combathandler(combatant)
```

結果將會是一個新的處理程式或一個已定義的處理程式。


(combathandlermsg)=
### CombatHandler.msg

```python 
# in evadventure/combat_base.py 

# ... 

class EvAdventureCombatBaseHandler(DefaultScript): 
	# ... 

	def msg(self, message, combatant=None, broadcast=True, location=None):
        """
        Central place for sending messages to combatants. This allows
        for adding any combat-specific text-decoration in one place.

        Args:
            message (str): The message to send.
            combatant (Object): The 'You' in the message, if any.
            broadcast (bool): If `False`, `combatant` must be included and
                will be the only one to see the message. If `True`, send to
                everyone in the location.
            location (Object, optional): If given, use this as the location to
                send broadcast messages to. If not, use `self.obj` as that
                location.

        Notes:
            If `combatant` is given, use `$You/you()` markup to create
            a message that looks different depending on who sees it. Use
            `$You(combatant_key)` to refer to other combatants.

        """
        if not location:
            location = self.obj

        location_objs = location.contents

        exclude = []
        if not broadcast and combatant:
            exclude = [obj for obj in location_objs if obj is not combatant]

        location.msg_contents(
            message,
            exclude=exclude,
            from_obj=combatant,
            mapping={locobj.key: locobj for locobj in location_objs},
        )

	# ... 
```

```{sidebar}
Script 的 `self.obj` 屬性是 Script “所在”的實體。如果在角色上設定，`self.obj` 將是該角色。如果在一個房間裡，那就是那個房間。對於全域 script，`self.obj` 是 `None`。
```

我們之前在[物件課的武器類](./Beginner-Tutorial-Objects.md#weapons)中看到了`location.msg_contents()`方法。其目的是獲取 `"$You() do stuff against $you(key)"` 形式的字串，並確保各方都能看到適合自己的字串。預設情況下，我們的 `msg()` 方法會將訊息廣播給房間中的每個人。 
<div style="clear: right;"></div>


你會這樣使用它：
```python
combathandler.msg(
	f"$You() $conj(throw) {item.key} at $you({target.key}).", 
	combatant=combatant, 
	location=combatant.location
)
```

如果戰鬥者是`Trickster`，`item.key`是“綵球”，`target.key`是“哥布林”，那麼

戰鬥者會看到：

    You throw a colorful ball at Goblin.

哥布林看見了

騙子丟一個彩色的球給你。

房間裡的其他人都看到了

騙子向哥布林丟了一個彩色球。

(combathandlerget_combat_summary)=
### 戰鬥人員。 get_combat_summary

我們希望能夠展示當前戰鬥的精彩總結：


```shell
                                        Goblin shaman (Perfect)
        Gregor (Hurt)                   Goblin brawler(Hurt)
        Bob (Perfect)         vs        Goblin grunt 1 (Hurt)
                                        Goblin grunt 2 (Perfect)
                                        Goblin grunt 3 (Wounded)
```

```{code-block} python
:linenos:
:emphasize-lines: 15,17,21,22,28,41

# in evadventure/combat_base.py

# ...

from evennia import EvTable

# ... 

class EvAdventureCombatBaseHandler(DefaultScript):

	# ... 

	def get_combat_summary(self, combatant):

        allies, enemies = self.get_sides(combatant)
        nallies, nenemies = len(allies), len(enemies)

        # prepare colors and hurt-levels
        allies = [f"{ally} ({ally.hurt_level})" for ally in allies]
        enemies = [f"{enemy} ({enemy.hurt_level})" for enemy in enemies]

        # the center column with the 'vs'
        vs_column = ["" for _ in range(max(nallies, nenemies))]
        vs_column[len(vs_column) // 2] = "|wvs|n"

        # the two allies / enemies columns should be centered vertically
        diff = abs(nallies - nenemies)
        top_empty = diff // 2
        bot_empty = diff - top_empty
        topfill = ["" for _ in range(top_empty)]
        botfill = ["" for _ in range(bot_empty)]

        if nallies >= nenemies:
            enemies = topfill + enemies + botfill
        else:
            allies = topfill + allies + botfill

        # make a table with three columns
        return evtable.EvTable(
            table=[
                evtable.EvColumn(*allies, align="l"),
                evtable.EvColumn(*vs_column, align="c"),
                evtable.EvColumn(*enemies, align="r"),
            ],
            border=None,
            maxwidth=78,
        )

	# ... 

```

這看起來可能很複雜，但複雜之處僅在於弄清楚如何組織三列，尤其是如何調整到兩側的`vs`大致垂直對齊。

- **第 15 行**：我們使用了 `self.get_sides(combatant)` 方法，但我們尚未實際實現。這是因為基於回合和基於抽搐的戰鬥需要不同的方式來找出雙方是誰。 `allies` 和 `enemies` 是清單。
- **第 17 行**：`combatant` 不是 `allies` 清單的一部分（這就是我們定義 `get_sides` 的工作方式），因此我們將其插入清單的頂部（因此它們首先顯示在左側）。
- **第 21、22 行**：我們利用所有生物的 `.hurt_level` 值（請參閱[角色課程的LivingMixin](./Beginner-Tutorial-Characters.md)）。
- **第28-39行**：我們透過在內容的上方和下方新增空行來確定如何使兩側垂直居中。
- **第 41 行**：[Evtable](../../../Components/EvTable.md) 是一個用於製作文字表的 Evennia 實用程式。一旦我們對這些列感到滿意，我們就把它們輸入到表中，然後讓 Evennia 完成剩下的工作。 `EvTable` 值得探索，因為它可以幫助您建立各種漂亮的佈局。

(actions)=
## 行動

在EvAdventure中，我們將只支援一些常見的戰鬥動作，對映到_Knave_中使用的等效擲骰和檢定。我們將設計我們的戰鬥框架，以便以後可以輕鬆地透過其他動作進行擴充套件。

- `hold` - 最簡單的操作。你只是向後靠，什麼都不做。
- `attack` - 你使用目前裝備的武器攻擊給定的`target`。這將成為針對目標ARMOR的STR或WIS擲骰。
- `stunt` - 你做了一個“特技”，用角色扮演的術語來說，這意味著你絆倒你的對手，嘲諷或以其他方式試圖在不傷害他們的情況下佔據上風。您可以這樣做，為自己（或盟友）在下一步行動中提供_優勢_`target`。您也可以針對您或盟友的下一步給予 `target` _disadvantage_。
- `use item` - 您使用庫存中的`Consumable`。當對自己使用時，它通常就像治療藥水一樣。如果對敵人使用，它可能是燃燒彈或一瓶酸。
- `wield` - 你擁有一件物品。根據所使用的物品，它會以不同的方式使用：頭盔會戴在頭上，一件盔甲會戴在胸前。一隻手揮舞著劍，另一手揮舞著盾牌。雙手斧頭會用掉兩隻手。這樣做會將之前的所有內容移至揹包中。
- `flee` - 你逃跑/脫離。此動作僅適用於回合製戰鬥（在基於抽搐的戰鬥中，您只需移動到另一個房間即可逃離）。因此，我們將等到[回合製戰鬥課程](./Beginner-Tutorial-Combat-Turnbased.md)後再定義此動作。

(action-dicts)=
## 行動指令

為了傳遞攻擊的詳細資訊（上面的第二點），我們將使用 `dict`。 `dict` 很簡單，也很容易儲存在 `Attribute` 中。我們稱之為 `action_dict`，這是每個操作所需的內容。

> 您無需在任何地方輸入這些內容，此處列出以供參考。我們將在呼叫 `combathandler.queue_action(combatant, action_dict)` 時使用這些字典。

```python 
hold_action_dict = {
	"key": "hold"
}
attack_action_dict = { 
	"key": "attack",
	"target": <Character/NPC> 
}
stunt_action_dict = { 
    "key": "stunt",					
	"recipient": <Character/NPC>, # who gains advantage/disadvantage
	"target": <Character/NPC>,  # who the recipient gainst adv/dis against
	"advantage": bool,  # grant advantage or disadvantage?
	"stunt_type": Ability,   # Ability to use for the challenge
	"defense_type": Ability, # what Ability for recipient to defend with if we
                    	     # are trying to give disadvantage 
}
use_item_action_dict = { 
    "key": "use", 
    "item": <Object>
    "target": <Character/NPC/None> # if using item against someone else			   
}
wield_action_dict = { 
    "key": "wield",
    "item": <Object>					
}

# used only for the turnbased combat, so its Action will be defined there
flee_action_dict = { 
    "key": "flee"                   
}
```

除了 `stunt` 操作之外，這些指令都非常簡單。 `key` 標識要執行的操作，其他欄位標識解決每個操作所需瞭解的最少內容。

我們還沒有編寫程式碼來設定這些指令，但我們假設我們知道誰在執行這些操作。因此，如果 `Beowulf` 攻擊 `Grendel`，貝奧武夫本人並不包含在攻擊字典中：

```python
attack_action_dict = { 
    "key": "attack",
    "target": Grendel
}
```

讓我們更詳細地解釋最長的動作字典，即 `Stunt` 動作字典。在此範例中，`Trickster` 正在表演_特技_，以幫助他的朋友 `Paladin` 獲得 INT- _優勢_ 對抗 `Goblin`（也許聖武士正準備施展某種咒語）。由於 `Trickster` 正在執行該操作，因此他沒有出現在字典中：

```python 
stunt_action_dict - { 
    "key": "stunt", 
    "recipient": Paladin,
    "target": Goblin,
    "advantage": True,
    "stunt_type": Ability.INT,
    "defense_type": Ability.INT,
}
```
```{sidebar}
在 EvAdventure 中，為了簡單起見，我們將始終設定 `stunt_type == defense_type`。但你也可以考慮將事情混合起來，這樣你就可以使用 DEX 來迷惑某人，並給他們帶來 INT 的劣勢，例如。
```
這應該會導致 `Trickster` 和 `Goblin` 之間基於 INT 與 INT 的檢查（也許騙子試圖用一些巧妙的文字遊戲來迷惑妖精）。如果 `Trickster` 獲勝，則 `Paladin` 在 `Paladin` 的下一步行動中獲得對抗哥布林的優勢。


(action-classes)=
## 動作類

一旦我們的 `action_dict` 確定了我們應該使用的特定操作，我們就需要一些東西來讀取這些鍵/值並實際_執行_該操作。


```python 
# in evadventure/combat_base.py 

class CombatAction: 

    def __init__(self, combathandler, combatant, action_dict):
        self.combathandler = combathandler
        self.combatant = combatant

        for key, val in action_dict.items(); 
            if key.startswith("_"):
                setattr(self, key, val)
```

我們將在_每次發生操作時_建立該類別的新例項。因此，我們儲存每個操作都需要的一些關鍵內容 - 我們需要對常見的 `combathandler` （我們將在下一節中設計）和 `combatant` （執行此操作的那個）的引用。 `action_dict` 是一個與我們要執行的操作相符的字典。

`setattr` Python 標準函式將 `action_dict` 的鍵/值指派為「關於」此操作的屬性。這在其他方法中使用起來非常方便。因此，對於`stunt`操作，其他方法可以直接存取`self.key`、`self.recipient`、`self.target`等。

```python 
# in evadventure/combat_base.py 

class CombatAction: 

    # ... 

    def msg(self, message, broadcast=True):
        "Send message to others in combat"
        self.combathandler.msg(message, combatant=self.combatant, broadcast=broadcast)

    def can_use(self): 
       """Return False if combatant can's use this action right now""" 
        return True 

    def execute(self): 
        """Does the actional action"""
        pass

    def post_execute(self):
        """Called after `execute`"""
        pass 
```

想要向戰鬥中的每個人傳送訊息是很常見的——你需要告訴人們他們正在受到攻擊，他們是否受傷等等。因此，在操作上使用 `msg` 輔助方法很方便。我們將所有複雜性轉移到 combathandler.msg() 方法。


`can_use`、`execute` 和 `post_execute` 都應該在鏈中呼叫，我們應該確保 `combathandler` 像這樣呼叫它們：

```python
if action.can_use(): 
    action.execute() 
    action.post_execute()
```

(hold-action)=
### 保持行動

```python
# in evadventure/combat_base.py 

# ... 

class CombatActionHold(CombatAction): 
    """ 
    Action that does nothing 
    
    action_dict = {
        "key": "hold"
    }
    
    """
```

Holding 不執行任何操作，但為其提供一個單獨的類別會更乾淨。我們使用檔案字串來指定其操作字典的外觀。

(attack-action)=
### 攻擊動作

```python
# in evadventure/combat_base.py

# ... 

class CombatActionAttack(CombatAction):
     """
     A regular attack, using a wielded weapon.
 
     action-dict = {
             "key": "attack",
             "target": Character/Object
         }
 
     """
 
     def execute(self):
         attacker = self.combatant
         weapon = attacker.weapon
         target = self.target
 
         if weapon.at_pre_use(attacker, target):
             weapon.use(
                 attacker, target, advantage=self.combathandler.has_advantage(attacker, target)
             )
             weapon.at_post_use(attacker, target)
```

請參閱我們如何[設計Evadventure武器](./Beginner-Tutorial-Objects.md#weapons)來瞭解這裡發生的情況 - 大部分工作是由武器類執行的 - 我們只需插入相關引數即可。

(stunt-action)=
### 特技動作

```python
# in evadventure/combat_base.py 

# ... 

class CombatActionStunt(CombatAction):
    """
    Perform a stunt the grants a beneficiary (can be self) advantage on their next action against a 
    target. Whenever performing a stunt that would affect another negatively (giving them
    disadvantage against an ally, or granting an advantage against them, we need to make a check
    first. We don't do a check if giving an advantage to an ally or ourselves.

    action_dict = {
           "key": "stunt",
           "recipient": Character/NPC,
           "target": Character/NPC,
           "advantage": bool,  # if False, it's a disadvantage
           "stunt_type": Ability,  # what ability (like STR, DEX etc) to use to perform this stunt. 
           "defense_type": Ability, # what ability to use to defend against (negative) effects of
            this stunt.
        }

    """

    def execute(self):
        combathandler = self.combathandler
        attacker = self.combatant
        recipient = self.recipient  # the one to receive the effect of the stunt
        target = self.target  # the affected by the stunt (can be the same as recipient/combatant)
        txt = ""

        if recipient == target:
            # grant another entity dis/advantage against themselves
            defender = recipient
        else:
            # recipient not same as target; who will defend depends on disadvantage or advantage
            # to give.
            defender = target if self.advantage else recipient

        # trying to give advantage to recipient against target. Target defends against caller
        is_success, _, txt = rules.dice.opposed_saving_throw(
            attacker,
            defender,
            attack_type=self.stunt_type,
            defense_type=self.defense_type,
            advantage=combathandler.has_advantage(attacker, defender),
            disadvantage=combathandler.has_disadvantage(attacker, defender),
        )

        self.msg(f"$You() $conj(attempt) stunt on $You({defender.key}). {txt}")

        # deal with results
        if is_success:
            if self.advantage:
                combathandler.give_advantage(recipient, target)
            else:
                combathandler.give_disadvantage(recipient, target)
            if recipient == self.combatant:
                self.msg(
                    f"$You() $conj(gain) {'advantage' if self.advantage else 'disadvantage'} "
                    f"against $You({target.key})!"
                )
            else:
                self.msg(
                    f"$You() $conj(cause) $You({recipient.key}) "
                    f"to gain {'advantage' if self.advantage else 'disadvantage'} "
                    f"against $You({target.key})!"
                )
            self.msg(
                "|yHaving succeeded, you hold back to plan your next move.|n [hold]",
                broadcast=False,
            )
        else:
            self.msg(f"$You({defender.key}) $conj(resist)! $You() $conj(fail) the stunt.")

```

這裡的主要動作是呼叫`rules.dice.opposed_saving_throw`來決定特技是否成功。之後，大多數線路都是關於確定誰應該獲得優勢/劣勢，並將結果傳達給受影響的各方。

請注意，我們在 `combathandler` 上大量使用了輔助方法，即使是尚未實現的方法。只要我們將 `action_dict` 傳遞到 `combathandler` 中，該操作實際上並不關心接下來會發生什麼。

在我們成功表演了特技之後，我們將 `combathandler.fallback_action_dict` 排隊。這是因為特技本來就是一次性的事情，如果我們重複動作，那麼一遍又一遍地重複特技就沒有意義。

(use-item-action)=
### 使用專案操作

```python
# in evadventure/combat_base.py 

# ... 

class CombatActionUseItem(CombatAction):
    """
    Use an item in combat. This is meant for one-off or limited-use items (so things like scrolls and potions, not swords and shields). If this is some sort of weapon or spell rune, we refer to the item to determine what to use for attack/defense rolls.

    action_dict = {
            "key": "use",
            "item": Object
            "target": Character/NPC/Object/None
        }

    """

    def execute(self):
        item = self.item
        user = self.combatant
        target = self.target

        if item.at_pre_use(user, target):
            item.use(
                user,
                target,
                advantage=self.combathandler.has_advantage(user, target),
                disadvantage=self.combathandler.has_disadvantage(user, target),
            )
            item.at_post_use(user, target)
```

請參閱[物件課程中的消耗品](./Beginner-Tutorial-Objects.md) 以瞭解消耗品的工作原理。就像武器一樣，我們將所有邏輯轉移到我們使用的物品上。

(wield-action)=
### 揮舞動作

```python
# in evadventure/combat_base.py 

# ... 

class CombatActionWield(CombatAction):
    """
    Wield a new weapon (or spell) from your inventory. This will 
	    swap out the one you are currently wielding, if any.

    action_dict = {
            "key": "wield",
            "item": Object
        }

    """

    def execute(self):
        self.combatant.equipment.move(self.item)

```

我們依靠我們建立的[裝置處理程式](./Beginner-Tutorial-Equipment.md)來為我們處理物品的交換。由於不斷地交換是沒有意義的，因此我們將後備操作排在這個操作之後。

(testing)=
## 測試

> 建立模組`evadventure/tests/test_combat.py`。

```{sidebar}
檢視`evennia/contrib/tutorials/evadventure/`下的[tests/test_combat.py](evennia.contrib.tutorials.evadventure.tests.test_combat)中的現成戰鬥單元測試。
```

對戰鬥基類進行單元測試似乎是不可能的，因為我們還沒有實現其中的大部分。然而，透過使用 [Mocks](https://docs.python.org/3/library/unittest.mock.html)，我們可以走得更遠。模擬的想法是用虛擬物件（“模擬”）_替換_一段程式碼，可以呼叫該虛擬物件來傳回某些特定值。

例如，考慮以下 `CombatHandler.get_combat_summary` 的測試。我們不能直接呼叫它，因為它在內部呼叫 `.get_sides`，這會引發 `NotImplementedError`。

```{code-block} python 
:linenos:
:emphasize-lines: 25,32

# in evadventure/tests/test_combat.py 

from unittest.mock import Mock

from evennia.utils.test_resources import EvenniaTestCase
from evennia import create_object
from .. import combat_base
from ..rooms import EvAdventureRoom
from ..characters import EvAdventureCharacter


class TestEvAdventureCombatBaseHandler(EvenniaTestCase):

    def setUp(self): 

		self.location = create_object(EvAdventureRoom, key="testroom")
		self.combatant = create_object(EvAdventureCharacter, key="testchar")
		self.target = create_object(EvAdventureMob, key="testmonster")

        self.combathandler = combat_base.get_combat_summary(self.location)

    def test_get_combat_summary(self):

        # do the test from perspective of combatant
	    self.combathandler.get_sides = Mock(return_value=([], [self.target]))
        result = str(self.combathandler.get_combat_summary(self.combatant))
		self.assertEqual(
		    result, 
		    " testchar (Perfect)  vs  testmonster (Perfect)"
		)
		# test from the perspective of the monster 
		self.combathandler.get_sides = Mock(return_value=([], [self.combatant]))
		result = str(self.combathandler.get_combat_summary(self.target))
		self.assertEqual(
			result,
			" testmonster (Perfect)  vs  testchar (Perfect)"
		)
```

有趣的地方是我們應用模擬的地方：

- **第 25 行**和 **第 32 行**：雖然 `get_sides` 尚未實現，但我們知道_應該_返回什麼 - 列表元組。因此，為了進行測試，我們將 `get_sides` 方法替換為模擬，該模擬在呼叫時會傳回有用的內容。

透過這種方法，即使系統尚未“完成”，也可以對其進行全面測試。

(conclusions)=
## 結論

我們擁有戰鬥系統所需的核心功能！在接下來的兩節課中，我們將利用這些構建塊來建立兩種風格的戰鬥。
