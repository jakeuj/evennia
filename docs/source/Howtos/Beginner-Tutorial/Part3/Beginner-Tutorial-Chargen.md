(character-generation)=
# 角色生成

在先前的課程中，我們已經確定了角色的外觀。現在我們需要給玩家一個創造機會。
(how-it-will-work)=
## 它將如何運作

當您登入時，全新的 Evennia 安裝將自動建立與您的帳戶同名的新角色。這快速又簡單，並模仿舊的 MUD 樣式。您可以想像這樣做，然後就地自訂角色。

不過我們會更複雜一些。我們希望使用者在登入時能夠使用選單建立角色。

我們透過編輯 `mygame/server/conf/settings.py` 並新增行來做到這一點

    AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False

執行此操作時，使用新帳戶連線遊戲將使您進入「OOC」模式。 `look` 的 ooc 版本（位於帳戶 cmdset 中）將顯示可用字元清單（如果有）。您也可以輸入`charcreate`來建立新角色。 `charcreate` 是一個簡單的指令，附帶 Evennia，它只允許您建立一個具有給定名稱和描述的新角色。我們稍後將對其進行修改以啟動我們的充電。現在我們只需記住這就是我們從選單開始的方式。

在_Knave_中，大部分的角色產生都是隨機。這意味著這個教學會很漂亮
緊湊，同時仍然展示基本思想。我們將建立一個如下所示的選單：


```
Silas

STR +1
DEX +2
CON +1
INT +3
WIS +1
CHA +2

You are lanky with a sunken face and filthy hair, breathy speech, and foreign clothing.
You were a herbalist, but you were pursued and ended up a knave. You are honest but also
suspicious. You are of the neutral alignment.

Your belongings:
Brigandine armor, ration, ration, sword, torch, torch, torch, torch, torch,
tinderbox, chisel, whistle

----------------------------------------------------------------------------------------
1. Change your name
2. Swap two of your ability scores (once)
3. Accept and create character
```

如果選擇 1，您將獲得一個新的選單節點：

```
Your current name is Silas. Enter a new name or leave empty to abort.
-----------------------------------------------------------------------------------------
```
現在您可以輸入新名稱。當按回車鍵時，您將返回到第一個選單節點
顯示你的性格，現在用新名字。

如果選擇 2，您將轉到另一個選單節點：

```
Your current abilities:

STR +1
DEX +2
CON +1
INT +3
WIS +1
CHA +2

You can swap the values of two abilities around.
You can only do this once, so choose carefully!

To swap the values of e.g. STR and INT, write 'STR INT'. Empty to abort.
------------------------------------------------------------------------------------------
```
如果您在此輸入`WIS CHA`，WIS 將變為`+2` 和`CHA` `+1`。然後，您將再次返回主節點檢視您的新角色，但這次交換選項將不再可用（您只能執行一次）。

如果您最終選擇`Accept and create character`選項，角色將被建立並且您將離開選單；

    Character was created!

(random-tables)=
## 隨機表

```{sidebar}
完整的無賴隨機表位於
[evennia/contrib/tutorials/evadventure/random_tables.py](../../../api/evennia.contrib.tutorials.evadventure.random_tables.md)。
```

> 建立一個新模組`mygame/evadventure/random_tables.py`。

由於 _Knave_ 的大部分角色生成都是隨機的，我們需要在隨機表上滾動
來自_Knave_規則手冊。雖然我們新增了在隨機表上滾動的功能
[規則教學](./Beginner-Tutorial-Rules.md)，我們還沒有加入相關表格。

```
# in mygame/evadventure/random_tables.py

chargen_tables = {
    "physique": [
        "athletic", "brawny", "corpulent", "delicate", "gaunt", "hulking", "lanky",
        "ripped", "rugged", "scrawny", "short", "sinewy", "slender", "flabby",
        "statuesque", "stout", "tiny", "towering", "willowy", "wiry",
    ],
    "face": [
        "bloated", "blunt", "bony", # ...
    ], # ...
}

```

這些表只是從 _Knave_ 規則中複製的。我們將各個方面分組到一個字典中
`character_generation` 將僅充電表與其他隨機表分開，我們也將
留在這裡。

(storing-state-of-the-menu)=
## 儲存選單狀態

```{sidebar}
Chargen 中有一個完整的實現
[evennia/contrib/tutorials/evadventure/chargen.py](../../../api/evennia.contrib.tutorials.evadventure.chargen.md)。
```
> 建立一個新模組`mygame/evadventure/chargen.py`。

在角色生成過程中，我們需要一個實體來儲存/保留更改，例如
「臨時字元表」。


```python
# in mygame/evadventure/chargen.py

from .random_tables import chargen_tables
from .rules import dice

class TemporaryCharacterSheet:

    def _random_ability(self):
        return min(dice.roll("1d6"), dice.roll("1d6"), dice.roll("1d6"))

    def __init__(self):
        self.ability_changes = 0  # how many times we tried swap abilities

        # name will likely be modified later
        self.name = dice.roll_random_table("1d282", chargen_tables["name"])

        # base attribute values
        self.strength = self._random_ability()
        self.dexterity = self._random_ability()
        self.constitution = self._random_ability()
        self.intelligence = self._random_ability()
        self.wisdom = self._random_ability()
        self.charisma = self._random_ability()

        # physical attributes (only for rp purposes)
        physique = dice.roll_random_table("1d20", chargen_tables["physique"])
        face = dice.roll_random_table("1d20", chargen_tables["face"])
        skin = dice.roll_random_table("1d20", chargen_tables["skin"])
        hair = dice.roll_random_table("1d20", chargen_tables["hair"])
        clothing = dice.roll_random_table("1d20", chargen_tables["clothing"])
        speech = dice.roll_random_table("1d20", chargen_tables["speech"])
        virtue = dice.roll_random_table("1d20", chargen_tables["virtue"])
        vice = dice.roll_random_table("1d20", chargen_tables["vice"])
        background = dice.roll_random_table("1d20", chargen_tables["background"])
        misfortune = dice.roll_random_table("1d20", chargen_tables["misfortune"])
        alignment = dice.roll_random_table("1d20", chargen_tables["alignment"])

        self.desc = (
            f"You are {physique} with a {face} face, {skin} skin, {hair} hair, {speech} speech,"
            f" and {clothing} clothing. You were a {background.title()}, but you were"
            f" {misfortune} and ended up a knave. You are {virtue} but also {vice}. You are of the"
            f" {alignment} alignment."
        )

        #
        self.hp_max = max(5, dice.roll("1d8"))
        self.hp = self.hp_max
        self.xp = 0
        self.level = 1

        # random equipment
        _armor = dice.roll_random_table("1d20", chargen_tables["armor"])
        self.armor = None if "no armor" in _armor else _armor

        _helmet_and_shield = dice.roll_random_table("1d20", chargen_tables["helmets and shields"])
        self.helmet = (
            None
            if "no" in _helmet_and_shield
            else ("helmet" if "helmet" in _helmet_and_shield else None)
        )
        self.shield = (
            None
            if "no" in _helmet_and_shield
            else ("shield" if "shield" in _helmet_and_shield else None)
        )

        self.weapon = dice.roll_random_table("1d20", chargen_tables["starting weapon"])

        self.backpack = [
            "ration",
            "ration",
            dice.roll_random_table("1d20", chargen_tables["dungeoning gear"]),
            dice.roll_random_table("1d20", chargen_tables["dungeoning gear"]),
            dice.roll_random_table("1d20", chargen_tables["general gear 1"]),
            dice.roll_random_table("1d20", chargen_tables["general gear 2"]),
        ]
```

在這裡，我們遵循_Knave_規則手冊來隨機化能力、描述和裝備。  `dice.roll()` 和 `dice.roll_random_table` 方法現在變得非常有用！這裡的一切都應該很容易理解。

與基準 _Knave_ 的主要區別是我們製作了一個「起始武器」表（在 Knave 中你可以選擇任何你喜歡的武器）。

我們也初始化`.ability_changes = 0`。 Knave 只允許我們交換兩個值
能力_一次_。我們將用它來知道它是否已經完成。

(showing-the-sheet)=
### 顯示工作表

現在我們有了臨時字元表，我們應該使其易於視覺化。

```python
# in mygame/evadventure/chargen.py

_TEMP_SHEET = """
{name}

STR +{strength}
DEX +{dexterity}
CON +{constitution}
INT +{intelligence}
WIS +{wisdom}
CHA +{charisma}

{description}

Your belongings:
{equipment}
"""

class TemporaryCharacterSheet:

    # ...

    def show_sheet(self):
        equipment = (
            str(item)
            for item in [self.armor, self.helmet, self.shield, self.weapon] + self.backpack
            if item
        )

        return _TEMP_SHEET.format(
            name=self.name,
            strength=self.strength,
            dexterity=self.dexterity,
            constitution=self.constitution,
            intelligence=self.intelligence,
            wisdom=self.wisdom,
            charisma=self.charisma,
            description=self.desc,
            equipment=", ".join(equipment),
        )

```

新的 `show_sheet` 方法從臨時表中收集資料並以漂亮的形式傳回。如果您想更改內容的外觀，製作像 `_TEMP_SHEET` 這樣的「模板」字串可以更輕鬆地更改內容。

(apply-character)=
### 應用字元

一旦我們對自己的角色感到滿意，我們就需要用我們選擇的統計資料來實際建立它。
這有點涉及更多。

```python
# in mygame/evadventure/chargen.py

# ...

from .characters import EvAdventureCharacter
from evennia import create_object
from evennia.prototypes.spawner import spawn


class TemporaryCharacterSheet:

    # ...

    def apply(self):
        # create character object with given abilities
        new_character = create_object(
            EvAdventureCharacter,
            key=self.name,
            attrs=(
                ("strength", self.strength),
                ("dexterity", self.dexterity),
                ("constitution", self.constitution),
                ("intelligence", self.intelligence),
                ("wisdom", self.wisdom),
                ("charisma", self.wisdom),
                ("hp", self.hp),
                ("hp_max", self.hp_max),
                ("desc", self.desc),
            ),
        )
        # spawn equipment (will require prototypes created before it works)
        if self.weapon:
            weapon = spawn(self.weapon)
            new_character.equipment.move(weapon)
        if self.shield:
            shield = spawn(self.shield)
            new_character.equipment.move(shield)
        if self.armor:
            armor = spawn(self.armor)
            new_character.equipment.move(armor)
        if self.helmet:
            helmet = spawn(self.helmet)
            new_character.equipment.move(helmet)

        for item in self.backpack:
            item = spawn(item)
            new_character.equipment.store(item)

        return new_character
```

我們使用 `create_object` 建立一個新的 `EvAdventureCharacter`。我們向它提供臨時字元表中的所有相關資料。這就是它們成為實際角色的時候。

```{sidebar}
原型基本上是 `dict` 描述應該如何建立物件。自從
它只是一段程式碼，它可以儲存在Python模組中並用於快速_spawn_（建立）
來自那些原型的東西。
```

每件裝置本身就是一個物件。我們在這裡假設所有遊戲
物品被定義為[原型](../../../Components/Prototypes.md)，並鍵入其名稱，例如“sword”、“brigandine”
鎧甲」等

我們還沒有真正建立這些原型，所以現在我們需要假設它們在那裡。一旦產生了一件裝備，我們確保將其移動到我們在[裝備課程](./Beginner-Tutorial-Equipment.md)中建立的`EquipmentHandler`中。


(initializing-evmenu)=
## 正在初始化EvMenu

Evennia帶有一個基於[指令集](../../../Components/Command-Sets.md)的完整選單產生系統，稱為
[EvMenu](../../../Components/EvMenu.md)。

```python
# in mygame/evadventure/chargen.py

from evennia import EvMenu

# ...

# chargen menu


# this goes to the bottom of the module

def start_chargen(caller, session=None):
    """
    This is a start point for spinning up the chargen from a command later.

    """

    menutree = {}  # TODO!

    # this generates all random components of the character
    tmp_character = TemporaryCharacterSheet()

    EvMenu(
        caller,
        menutree,
        session=session,
        startnode="node_chargen",
        startnode_input=("", {"tmp_character": tmp_character}),
    )

```

我們將從其他地方（例如從自訂 `charcreate` 指令）呼叫第一個函式來啟動選單。

它需要 `caller` （要啟動選單的那個）和 `session` 引數。後者將幫助追蹤我們正在使用哪個用戶端連線（根據 Evennia 設定，您可能正在與多個用戶端連線）。

我們建立一個 `TemporaryCharacterSheet` 並將所有這些輸入到 `EvMenu` 中。 `startnode` 和 `startnode_input` 關鍵字確保在「node_chargen」節點（我們將在下面建立）處進入選單，並使用提供的引數呼叫它。

一旦發生這種情況，使用者將進入選單，無需執行進一步的步驟。

`menutree` 是我們接下來要建立的。它描述了可以在哪些選單“節點”之間跳轉。

(main-node-choosing-what-to-do)=
## 主節點：選擇要做什麼

這是第一個選單節點。它將充當一個中心樞紐，人們可以從中選擇不同的
行動。

```python
# in mygame/evadventure/chargen.py

# ...

# at the end of the module, but before the `start_chargen` function

def node_chargen(caller, raw_string, **kwargs):

    tmp_character = kwargs["tmp_character"]

    text = tmp_character.show_sheet()

    options = [
        {
           "desc": "Change your name",
           "goto": ("node_change_name", kwargs)
        }
    ]
    if tmp_character.ability_changes <= 0:
        options.append(
            {
                "desc": "Swap two of your ability scores (once)",
                "goto": ("node_swap_abilities", kwargs),
            }
        )
    options.append(
        {
            "desc": "Accept and create character",
            "goto": ("node_apply_character", kwargs)
        },
    )

    return text, options

# ...
```

這裡有很多東西要解壓縮！在 Evennia 中，依照慣例將節點函式命名為 `node_*`。同時
不是必需的，它可以幫助您追蹤什麼是節點，什麼不是節點。

每個選單節點都應該接受 `caller, raw_string, **kwargs` 作為引數。這裡 `caller` 是您傳遞到 `EvMenu` 呼叫中的 `caller`。 `raw_string` 是使用者為了_到達此節點_而給出的輸入，因此目前為空。 `**kwargs` 是傳遞到 `EvMenu` 的所有額外關鍵字引數。它們也可以在節點之間傳遞。在本例中，我們將關鍵字 `tmp_character` 傳遞給 `EvMenu`。現在，我們在節點中擁有了可用的臨時字元表！

> 請注意，上面我們使用 `startnode="node_chargen"` 和元組 `startnode_input=("", {"tmp_character": tmp_character})` 建立了選單。假設我們將上述函式註冊為節點 `"node_chargen"`，它將開始被呼叫為 `node_chargen(caller, "", tmp_character=tmp_character)`（EvMenu 將自行新增 `caller`）。這是我們在選單啟動時將外部資料傳遞到選單中的一種方法。

`EvMenu` 節點必須始終傳回兩個內容 - `text` 和 `options`。 `text` 是什麼
當使用者檢視此節點時顯示給使用者。 `options` 是，嗯，應該是什麼選項
提出從這裡前往其他地方。

對於文字，我們只需獲得臨時字元表的漂亮列印即可。單一選項定義為 `dict`，如下所示：

```python
{
    "key": ("name". "alias1", "alias2", ...),  # if skipped, auto-show a number
    "desc": "text to describe what happens when selecting option",.
    "goto": ("name of node or a callable", kwargs_to_pass_into_next_node_or_callable)
}
```

多個選項字典以列表或元組形式傳回。 `goto` 選項鍵很重要
明白。其作用是直接指向另一個節點（透過給出其名稱），或者
透過指向一個Python可呼叫（如函式）_然後傳回該名稱_。您還可以
透過 kwargs （作為字典）。這將在可呼叫節點或下一個節點中作為 `**kwargs` 提供。

雖然選項可以有 `key`，但您也可以跳過它而只獲取執行數字。

在我們的`node_chargen`節點中，我們透過名稱指向三個節點：`node_change_name`，
`node_swap_abilities`和`node_apply_character`。我們也確保傳遞`kwargs`
到每個節點，因為它包含我們的臨時字元表。

這些選項的中間僅在我們尚未切換兩種能力時才會出現 - 要了解這一點，我們檢查 `.ability_changes` 屬性以確保它仍然為 0。


(node-changing-your-name)=
## 節點：更改你的名字

如果您選擇在 `node_chargen` 中更改您的姓名，這就是您最終的位置。

```python
# in mygame/evadventure/chargen.py

# ...

# after previous node

def _update_name(caller, raw_string, **kwargs):
    """
    Used by node_change_name below to check what user
    entered and update the name if appropriate.

    """
    if raw_string:
        tmp_character = kwargs["tmp_character"]
        tmp_character.name = raw_string.lower().capitalize()

    return "node_chargen", kwargs


def node_change_name(caller, raw_string, **kwargs):
    """
    Change the random name of the character.

    """
    tmp_character = kwargs["tmp_character"]

    text = (
        f"Your current name is |w{tmp_character.name}|n. "
        "Enter a new name or leave empty to abort."
    )

    options = {
                   "key": "_default",
                   "goto": (_update_name, kwargs)
              }

    return text, options
```

這裡有兩個函式 - 選單節點本身 (`node_change_name`) 和
helper _goto_function_ (`_update_name`) 來處理使用者的輸入。

對於（單一）選項，我們使用名為 `_default` 的特殊 `key`。這使得這個選項
包羅永珍：如果使用者輸入的內容與任何其他選項都不匹配，則這是
將使用的選項。由於我們這裡沒有其他選項，因此無論使用者輸入什麼，我們都將始終使用此選項。

另請注意，選項的 `goto` 部分指向 `_update_name` 可呼叫函式，而不是指向
節點的名稱。重要的是我們要不斷傳遞 `kwargs` 給它！

當使用者在此節點寫入任何內容時，將呼叫 `_update_name` 可呼叫函式。這有
與節點相同的引數，但它_不是_節點 - 我們只會用它來_找出_哪個
轉到下一個節點。

在 `_update_name` 中，我們現在可以使用 `raw_string` 引數 - 這是使用者在前一個節點上編寫的內容，還記得嗎？現在它要麼是一個空字串（意味著忽略它）要麼是角色的新名稱。

像 `_update_name` 這樣的 goto 函式必須傳回要使用的下一個節點的名稱。還可以
可選擇返回 `kwargs` 以傳遞到該節點 - 我們希望始終這樣做，所以我們不這樣做
放開我們的臨時角色表。在這裡我們總是會回到`node_chargen`。

> 提示：如果從 goto-callable 回傳 `None`，您將始終回到最後一個節點
> 是在。

(node-swapping-abilities-around)=
## 節點：交換能力

您可以從 `node_chargen` 節點中選擇第二個選項來到達此處。

```python
# in mygame/evadventure/chargen.py

# ...

# after previous node

_ABILITIES = {
    "STR": "strength",
    "DEX": "dexterity",
    "CON": "constitution",
    "INT": "intelligence",
    "WIS": "wisdom",
    "CHA": "charisma",
}


def _swap_abilities(caller, raw_string, **kwargs):
    """
    Used by node_swap_abilities to parse the user's input and swap ability
    values.

    """
    if raw_string:
        abi1, *abi2 = raw_string.split(" ", 1)
        if not abi2:
            caller.msg("That doesn't look right.")
            return None, kwargs
        abi2 = abi2[0]
        abi1, abi2 = abi1.upper().strip(), abi2.upper().strip()
        if abi1 not in _ABILITIES or abi2 not in _ABILITIES:
            caller.msg("Not a familiar set of abilites.")
            return None, kwargs

        # looks okay = swap values. We need to convert STR to strength etc
        tmp_character = kwargs["tmp_character"]
        abi1 = _ABILITIES[abi1]
        abi2 = _ABILITIES[abi2]
        abival1 = getattr(tmp_character, abi1)
        abival2 = getattr(tmp_character, abi2)

        setattr(tmp_character, abi1, abival2)
        setattr(tmp_character, abi2, abival1)

        tmp_character.ability_changes += 1

    return "node_chargen", kwargs


def node_swap_abilities(caller, raw_string, **kwargs):
    """
    One is allowed to swap the values of two abilities around, once.

    """
    tmp_character = kwargs["tmp_character"]

    text = f"""
Your current abilities:

STR +{tmp_character.strength}
DEX +{tmp_character.dexterity}
CON +{tmp_character.constitution}
INT +{tmp_character.intelligence}
WIS +{tmp_character.wisdom}
CHA +{tmp_character.charisma}

You can swap the values of two abilities around.
You can only do this once, so choose carefully!

To swap the values of e.g.  STR and INT, write |wSTR INT|n. Empty to abort.
"""

    options = {"key": "_default", "goto": (_swap_abilities, kwargs)}

        return text, options
```

這是更多程式碼，但邏輯是相同的 - 我們有一個節點 (`node_swap_abilities`) 和
和一個 goto 可呼叫的助手 (`_swap_abilities`)。我們捕獲使用者在上面寫的所有內容
節點（例如 `WIS CON`）並將其輸入到助手中。

在`_swap_abilities`中，我們需要分析來自使用者的`raw_string`，看看他們做了什麼
想做。

幫助程式中的大多數程式碼都會驗證使用者沒有輸入廢話。如果他們這樣做了，
我們使用 `caller.msg()` 告訴他們，然後返回 `None, kwargs`，這會再次重新執行相同的節點（名稱選擇）。

由於我們希望使用者能夠編寫“CON”而不是更長的“憲法”，因此我們需要一個對映 `_ABILITIES` 來輕鬆地在兩者之間進行轉換（它在臨時字元表上儲存為 `consitution`）。一旦我們知道他們想要交換哪些能力，我們就會這樣做並勾選 `.ability_changes` 計數器。這意味著主節點將不再提供此選項。

最後，我們再次回到`node_chargen`。

(node-creating-the-character)=
## 節點：建立角色

我們透過選擇完成 chargen 從主節點到達這裡。

```python
node_apply_character(caller, raw_string, **kwargs):
    """
    End chargen and create the character. We will also puppet it.

    """
    tmp_character = kwargs["tmp_character"]
    new_character = tmp_character.apply(caller)

    caller.account.add_character(new_character)

    text = "Character created!"

    return text, None
```
進入節點時，我們會取出臨時角色表，並使用其`.apply`方法建立一個帶有所有裝備的新角色。

這就是所謂的_結束節點_，因為它傳回 `None` 而不是選項。此後，選單將退出。我們將回到預設的角色選擇畫面。在該螢幕上找到的字元是 `_playable_characters` Attribute 中列出的字元，因此我們還需要將新字元新增到其中。


(tying-the-nodes-together)=
## 將節點連線在一起

```python
def start_chargen(caller, session=None):
    """
    This is a start point for spinning up the chargen from a command later.

    """
    menutree = {  # <----- can now add this!
        "node_chargen": node_chargen,
        "node_change_name": node_change_name,
        "node_swap_abilities": node_swap_abilities,
        "node_apply_character": node_apply_character,
    }

    # this generates all random components of the character
    tmp_character = TemporaryCharacterSheet()

    EvMenu(
        caller,
        menutree,
        session=session,
        startnode="node_chargen",  # <-- make sure it's set!
        startnode_input=("", {"tmp_character": tmp_character}),
    )
```

現在我們有了所有節點，我們將它們新增到之前留空的 `menutree` 中。我們只加入節點，而不是 goto-helpers！我們在 `menutree` 字典中設定的鍵是我們應該用來從選單內部指向節點的名稱（我們確實這樣做了）。

我們也新增一個關鍵字引數 `startnode` 指向 `node_chargen` 節點。這告訴 EvMenu 在選單啟動時首先跳到該節點。

(conclusions)=
## 結論

本課程教我們如何使用`EvMenu`製作互動式字元產生器。在比 _Knave_ 更複雜的 RPG 中，選單會更大、更複雜，但同樣的原則也適用。

結合之前的課程，我們現在已經掌握了有關玩家的大部分基礎知識
角色 - 他們如何儲存他們的統計資料，處理他們的裝備以及如何建立它們。

在下一課中，我們將討論 EvAdventure _Rooms_ 的工作原理。
