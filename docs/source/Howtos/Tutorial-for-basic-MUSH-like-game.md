(tutorial-for-basic-mush-like-game)=
# 基本MUSH類遊戲教學


本教學讓您可以在 Evennia 中編寫一個小型但完整且功能性類似於 MUSH 的遊戲。一個
[MUSH](https://en.wikipedia.org/wiki/MUSH) 就我們的目的而言，是一類以角色扮演為中心的遊戲
專注於自由形式的故事敘述。即使你對 MUSH:es 不感興趣，這仍然是一個很好的選擇
第一個嘗試的遊戲型別，因為它的程式碼量不是很大。您將能夠使用相同的原則
建構其他型別的遊戲。

本教學從頭開始。如果您完成了[第一步編碼](Beginner-Tutorial/Part1/Beginner-Tutorial-Part1-Overview.md)教學
您應該已經對如何執行某些步驟有了一些想法。

以下是我們將實現的（非常簡單和精簡的）功能（摘自
來自新加入 Evennia 的 MUSH 使用者的功能請求）。該系統中的角色應該：

- 有一個從 1 到 10 的「力量」分數，衡量他們的實力（代表統計資料）
系統）。
- 有一個指令（e.g。`+setpower 4`）來設定他們的力量（替代角色生成
程式碼）。
- 有一個指令（e.g。`+attack`）讓他們滾動他們的力量並產生“戰鬥分數”
`1` 和 `10*Power` 之間，顯示結果並編輯其物件以記錄此數字
（代表指令程式碼中的`+actions`）。
- 有一個指令可以顯示房間中的每個人以及他們最近的“戰鬥分數”卷
是（戰鬥程式碼的替代）。
- 有一個指令（e.g。`+createNPC Jenkins`）建立一個具有全部能力的NPC。
- 有一個指令來控制NPCs，例如`+npc/cmd (name)=(command)`（取代NPC
控制程式碼）。

在本教學中，我們假設您從空資料庫開始，之前沒有任何資料庫
修改。

(server-settings)=
## 伺服器設定

要模擬 MUSH，預設的 `MULTISESSION_MODE=0` 就足夠了（每個 session 一個唯一的 session）
帳戶/角色）。這是預設設定，因此您無需更改任何內容。你仍然可以
操縱/取消操縱您有權操縱的物件，但沒有從中選擇角色
在此模式下的框框。

我們假設我們的遊戲資料夾從此被稱為`mygame`。  你應該可以使用預設值
SQLite3 資料庫。

(creating-the-character)=
## 建立角色

首先是選擇我們的角色類別的工作方式。我們不需要定義特殊的NPC物件
-- NPC 畢竟只是一個角色，目前沒有帳戶控制它們。

在 `mygame/typeclasses/characters.py` 檔案中進行更改：

```python
# mygame/typeclasses/characters.py

from evennia import DefaultCharacter

class Character(DefaultCharacter):
    """
     [...]
    """
    def at_object_creation(self):
        "This is called when object is first created, only."
        self.db.power = 1
        self.db.combat_score = 1
```

我們定義了兩個新的[屬性](../Components/Attributes.md)`power`和`combat_score`並將它們設為預設值
價值觀。如果伺服器已經在執行，請確保 `@reload` 伺服器（您需要重新載入每個
當你更新你的Python程式碼時，不用擔心，重新載入不會斷開任何帳戶的連線）。

請注意，只有*新*字元才會看到您的新屬性（因為 `at_object_creation` 鉤子是
首次建立物件時呼叫，現有角色不會擁有它）。  為了更新自己，
跑

     @typeclass/force self

這會重置您自己的typeclass（`/force`開關是一種安全措施，不這樣做
意外），這意味著 `at_object_creation` 重新執行。

     examine self

在「永續性屬性」標題下，您現在應該找到新屬性 `power` 和 `score`
`at_object_creation` 為你自己設定。如果不這樣做，請先確保您 `@reload`ed 進入新的
程式碼，接下來檢視您的伺服器日誌（在終端機/控制檯中）以檢視是否存在任何語法錯誤
在您的程式碼中，這可能會阻止您的新程式碼正確載入。

(character-generation)=
## 角色生成

在此範例中，我們假設帳戶首先連線到「字元產生區域」。 Evennia
也支援完整的OOC選單驅動的角色生成，但對於這個例子，一個簡單的開始房間
就足夠了。當在這個房間（或多個房間）中時，我們允許角色產生指令。其實性格
產生指令*僅*在此類房間中可用。

請注意，這樣做是為了易於擴充套件為成熟的遊戲。用我們簡單的
例如，我們可以簡單地在帳戶上設定 `is_in_chargen` 標誌並使用 `+setpower` 指令
檢查一下。然而，使用此方法將使以後新增更多功能變得容易。

我們需要的是以下內容：

- 產生一個字元[指令](../Components/Commands.md)來設定`Character`上的「力量」。
- 一個 Chargen [CmdSet](../Components/Command-Sets.md) 來儲存此指令。我們稱之為`ChargenCmdset`。
- 自訂 `ChargenRoom` 型別，使此類房間中的玩家可以使用這組指令。
- 一間這樣的房間來測試東西。

(the-setpower-command)=
### +setpower 指令

在本教學中，我們將所有新指令新增至`mygame/commands/command.py`，但您可以
如果您願意，可以將指令拆分為多個模組。

對於本教學，角色生成僅包含一個 [指令](../Components/Commands.md) 來設定
角色的「力量」統計。它將以以下類似 MUSH 的形式呼叫：

     +setpower 4

開啟 `command.py` 檔案。它包含基本指令和
Evennia 中預設使用「MuxCommand」型別。我們將在這裡使用簡單的 `Command` 型別，
`MuxCommand` 類提供了一些額外的功能，例如可能有用的剝離空格 - 如果是這樣，
只需從中匯入即可。

將以下內容新增至 `command.py` 檔案的末尾：

```python
# end of command.py
from evennia import Command # just for clarity; already imported above

class CmdSetPower(Command):
    """
    set the power of a character

    Usage:
      +setpower <1-10>

    This sets the power of the current character. This can only be
    used during character generation.
    """

    key = "+setpower"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "You must supply a number between 1 and 10."
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            power = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= power <= 10):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.power = power
        self.caller.msg(f"Your Power was set to {power}.")
```
這是一個非常簡單的指令。我們進行一些錯誤檢查，然後自行啟動。
我們對所有指令使用 `help_category` 的“mush”，這樣它們就很容易找到和分離
在幫助清單中。

儲存檔案。我們現在將其新增到新的 [CmdSet](../Components/Command-Sets.md) 中，以便可以存取它（以完整的方式）
chargen 系統你當然會在這裡有多個指令）。

開啟 `mygame/commands/default_cmdsets.py` 並在頂部匯入您的 `command.py` 模組。我們也
匯入預設的 `CmdSet` 類別以進行下一步：

```python
from evennia import CmdSet
from commands import command
```

接下來向下捲動並定義一個新的指令集（基於我們剛剛匯入的基本 `CmdSet` 類別）
該檔案的末尾，僅儲存我們特定於 chargen 的指令：

```python
# end of default_cmdsets.py

class ChargenCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "Chargen"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(command.CmdSetPower())
```

將來你可以為這個cmdset新增任意數量的指令，以擴充套件你的角色生成
系統如你所願。現在我們需要實際將 cmdset 放在某個東西上，以便它可供使用
使用者。  我們可以將其直接放在角色上，但這將使其始終可用。
把它放在房間裡會更乾淨，所以只有當玩家在那個房間時它才可用。

(chargen-areas)=
### 電荷區

我們將建立一個簡單的 Room typeclass 作為我們所有 Chargen 區域的模板。編輯
`mygame/typeclasses/rooms.py` 接下來：

```python
from commands.default_cmdsets import ChargenCmdset

# ...
# down at the end of rooms.py

class ChargenRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(ChargenCmdset, persistent=True)
```
請注意，使用 typeclass 建立的新房間將始終以 `ChargenCmdset` 開頭。
不要忘記 `persistent=True` 關鍵字，否則伺服器重新載入後您將丟失 cmdset。對於
有關[指令集](../Components/Command-Sets.md) 和[指令](../Components/Commands.md) 的更多資訊，請參閱相應的
連結。

(testing-chargen)=
### 測試電荷

首先，請確保您已`@reload`ed伺服器（或從終端使用`evennia reload`）
您的新 Python 程式碼已新增至遊戲中。檢查您的終端並修復您看到的任何錯誤 - 錯誤
回溯準確地列出了發現錯誤的位置 - 檢視已更改的檔案中的行號。

除非我們有一些帶電區域要測試，否則我們無法測試事物。登入遊戲（您應該在
此時將使用新的自訂字元類別）。我們挖一個帶電區域來測試一下。

     @dig chargen:rooms.ChargenRoom = chargen,finish

如果您閱讀`@dig`的幫助，您會發現這將建立一個名為`chargen`的新房間。的
`:` 之後的部分是您要使用的 Typeclass 的 python 路徑。由於 Evennia 將
自動嘗試我們遊戲目錄的`typeclasses`資料夾，我們只需指定
`rooms.ChargenRoom`，這意味著它將在模組 `rooms.py` 中尋找名為的類
`ChargenRoom`（這是我們上面建立的）。 `=` 之後給出的名稱是出口的名稱
以及從您目前位置的房間。您也可以為每個名稱附加別名，例如
為`chargen;character generation`。

總而言之，這將建立一個型別為 ChargenRoom 的新房間，並為其開啟一個出口 `chargen`，
一個名為 `finish` 的出口。如果您在此階段看到錯誤，則必須在程式碼中修復它們。
`@reload`
修復之間。在建立看起來工作正常之前不要繼續。

     chargen

這應該會帶你到充電室。在那裡你現在應該有`+setpower`
指令可用，所以測試一下。當您離開時（透過 `finish` 出口），該指令將消失
嘗試 `+setpower` 現在應該會給你一個指令找不到的錯誤。使用`ex me`（作為特權
使用者）檢查 `Power` [Attribute](../Components/Attributes.md) 是否設定正確。

如果出現問題，請確保您的 typeclasses 和指令沒有錯誤，並且您
已正確輸入各種指令集和指令的路徑。檢查日誌或指令
用於回溯和錯誤的行。

(combat-system)=
## 戰鬥系統

我們將把戰鬥指令新增到預設指令集中，這意味著每個人都可以使用它
任何時候。戰鬥系統由 `+attack` 指令組成，用於獲取我們的攻擊有多成功。
我們還更改了預設的 `look` 指令來顯示當前的戰鬥分數。


(attacking-with-the-attack-command)=
### 使用+attack指令進行攻擊

在這個簡單的系統中攻擊意味著滾動一個受 `power` 統計影響的隨機“戰鬥分數”
在角色生成期間設定：

    > +attack
    You +attack with a combat score of 12!

返回 `mygame/commands/command.py` 並將指令新增到末尾，如下所示：

```python
import random

# ...

class CmdAttack(Command):
    """
    issues an attack

    Usage:
        +attack

    This will calculate a new combat score based on your Power.
    Your combat score is visible to everyone in the same location.
    """
    key = "+attack"
    help_category = "mush"

    def func(self):
        "Calculate the random score between 1-10*Power"
        caller = self.caller
        power = caller.db.power
        if not power:
            # this can happen if caller is not of
            # our custom Character typeclass
            power = 1
        combat_score = random.randint(1, 10 * power)
        caller.db.combat_score = combat_score

        # announce
        message_template = "{attacker} +attack{s} with a combat score of {c_score}!"
        caller.msg(message_template.format(
            attacker="You",
            s="",
            c_score=combat_score,
        ))
        caller.location.msg_contents(message_template.format(
            attacker=caller.key,
            s="s",
            c_score=combat_score,
        ), exclude=caller)
```

我們在這裡所做的只是使用Python內建的`random.randint()`來產生“戰鬥分數”
功能。然後我們儲存該結果並將結果回顯給所有相關人員。

要使 `+attack` 指令在遊戲中可用，請返回
`mygame/commands/default_cmdsets.py` 並向下捲動至 `CharacterCmdSet` 類。在正確的
地方加入這一行：

```python
self.add(command.CmdAttack())
```

`@reload` Evennia 和 `+attack` 指令應該可供您使用。執行它並使用e.g。 `@ex` 至
確保 `combat_score` attribute 已正確儲存。

(have-look-show-combat-scores)=
### 「看」顯示戰鬥分數

玩家應該能夠檢視房間中所有當前的戰鬥分數。  我們可以透過簡單地做到這一點
新增第二個名為 `+combatscores` 的指令，但我們將使用預設值
`look` 指令為我們完成繁重的工作並將我們的分數顯示為正常輸出的一部分，例如
這個：

    >  look Tom
    Tom (combat score: 3)
    This is a great warrior.

然而，我們實際上不必修改 `look` 指令本身。要了解原因，請看一下
預設 `look` 是如何實際定義的。它位於 [evennia/commands/default/general.py](evennia.commands.default.general)。

你會發現實際的回傳文字是透過`look`指令呼叫*hook方法*完成的
在所檢視的物件上命名為 `return_appearance`。 `look` 所做的只是回顯該鉤子的任何內容
返回。  所以我們需要做的是編輯我們的自訂角色typeclass並過載它
`return_appearance` 回傳我們想要的內容（這就是自訂 typeclass 的優勢所在
真正發揮作用）。

傳回 `mygame/typeclasses/characters.py` 中的自訂角色 typeclass。預設
`return appearance` 的實現位於 [evennia.DefaultCharacter](evennia.objects.objects.DefaultCharacter) 中。

如果您想進行更大的更改，您可以將整個預設內容複製並貼上到我們的過載方法中。在我們的例子中，變化很小：

```python
class Character(DefaultCharacter):
    """
     [...]
    """
    def at_object_creation(self):
        "This is called when object is first created, only."
        self.db.power = 1
        self.db.combat_score = 1

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = super().return_appearance(looker)
        cscore = f" (combat score: {self.db.combat_score})"
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            text = first_line + cscore + "\n" + rest
        else:
            # text is only one line; add score to end
            text += cscore
        return text
```

我們所做的就是簡單地讓預設的 `return_appearance` 做它的事情（`super` 將呼叫
相同方法的父母版本）。然後我們分割出該文字的第一行，並附加我們的
`combat_score` 並再次將其放回原處。

`@reload` 伺服器，你應該能夠檢視其他角色並瞭解他們當前的戰鬥
分數。

> 注意：一個可能更有用的方法是過載整個 `return_appearance`
`Room`s 的糊狀內容並更改它們列出內容的方式；這樣人們就可以看到所有
檢視房間的同時顯示所有在場角色的戰鬥分數。我們將其保留為
鍛煉。

(npc-system)=
## NPC系統

這裡我們將透過引入一個可以建立NPC物件的指令來重複使用Character類別。我們
還應該能夠設定其功率並對其進行排序。

有幾種方法可以定義 NPC 類別。理論上我們可以為它建立一個自訂的 typeclass
並將自訂NPC-特定cmdset放在所有NPCs上。這個cmdset可以容納所有的操作指令。
然而，由於我們預期 NPC 操縱在使用者群中很常見，因此我們將
相反，將所有相關的 NPC 指令放入預設指令集中，並限制最終訪問
[許可權和鎖定](../Components/Permissions.md)。

(creating-an-npc-with-createnpc)=
### 使用 +createNPC 建立 NPC

我們需要一個指令來建立NPC，這是一個非常簡單的指令：

    > +createnpc Anna
    You created the NPC 'Anna'.

在`command.py`末尾，建立我們的新指令：

```python
from evennia import create_object

class CmdCreateNPC(Command):
    """
    create a new npc

    Usage:
        +createNPC <name>

    Creates a new, named NPC. The NPC will start with a Power of 1.
    """
    key = "+createnpc"
    aliases = ["+createNPC"]
    locks = "call:not perm(nonpcs)"
    help_category = "mush"

    def func(self):
        "creates the object and names it"
        caller = self.caller
        if not self.args:
            caller.msg("Usage: +createNPC <name>")
            return
        if not caller.location:
            # may not create npc when OOC
            caller.msg("You must have a location to create an npc.")
            return
        # make name always start with capital letter
        name = self.args.strip().capitalize()
        # create npc in caller's location
        npc = create_object("characters.Character",
                      key=name,
                      location=caller.location,
                      locks=f"edit:id({caller.id}) and perm(Builders);call:false()")
        # announce
        message_template = "{creator} created the NPC '{npc}'."
        caller.msg(message_template.format(
            creator="You",
            npc=name,
        ))
        caller.location.msg_contents(message_template.format(
            creator=caller.key,
            npc=name,
        ), exclude=caller)
```
這裡我們定義了一個 `+createnpc` （`+createNPC` 也可以），每個*不*擁有
`nonpcs`「[許可權](../Components/Permissions.md)」（在Evennia中，「許可權」也可以用於
阻止訪問，這取決於我們定義的lock）。我們在呼叫者的目前物件中建立 NPC 物件
位置，使用我們自訂的 `Character` typeclass 來執行此操作。

我們在 NPC 上設定了一個額外的 lock 條件，我們將用它來檢查誰可以稍後編輯 NPC --
我們允許建立者以及任何擁有建構者許可權（或更高許可權）的人這樣做。參見
[鎖定](../Components/Locks.md) 以瞭解更多有關 lock 系統的資訊。

請注意，我們只是授予物件預設許可權（透過不指定 `permissions` 關鍵字
到 `create_object()` 呼叫）。  在某些遊戲中，人們可能會想給予 NPC 相同的許可權
作為建立它們的角色，這可能會帶來安全風險。

將此指令新增至預設的 cmdset 中，就像之前執行 `+attack` 指令一樣。
`@reload` 並且可以進行測試。

(editing-the-npc-with-editnpc)=
### 使用 +editNPC 編輯 NPC

由於我們重新使用了自定義角色 typeclass，因此我們的新 NPC 已經具有 *Power* 值 - 它
預設為 1。我們如何更改它？

我們可以透過幾種方法來做到這一點。最簡單的是記住 `power` attribute 只是一個
簡單 [Attribute](../Components/Attributes.md) 儲存在 NPC 物件上。所以身為建構者或管理員我們可以設定這個
立即使用預設的 `@set` 指令：

     @set mynpc/power = 6

但 `@set` 指令過於強大，因此僅對工作人員可用。我們將新增一個
自訂指令僅更改我們希望允許玩家更改的內容。我們可以在
原則上重新工作我們舊的 `+setpower` 指令，但讓我們嘗試一些更有用的東西。讓我們做一個
`+editNPC` 指令。

    > +editNPC Anna/power = 10
    Set Anna's property 'power' to 10.

這是一個稍微複雜的指令。它像以前一樣位於 `command.py` 檔案的末尾。

```python
class CmdEditNPC(Command):
    """
    edit an existing NPC

    Usage:
      +editnpc <name>[/<attribute> [= value]]

    Examples:
      +editnpc mynpc/power = 5
      +editnpc mynpc/power    - displays power value
      +editnpc mynpc          - shows all editable
                                attributes and values

    This command edits an existing NPC. You must have
    permission to edit the NPC to use this.
    """
    key = "+editnpc"
    aliases = ["+editNPC"]
    locks = "cmd:not perm(nonpcs)"
    help_category = "mush"

    def parse(self):
        "We need to do some parsing here"
        args = self.args
        propname, propval = None, None
        if "=" in args:
            args, propval = [part.strip() for part in args.rsplit("=", 1)]
        if "/" in args:
            args, propname = [part.strip() for part in args.rsplit("/", 1)]
        # store, so we can access it below in func()
        self.name = args
        self.propname = propname
        # a propval without a propname is meaningless
        self.propval = propval if propname else None

    def func(self):
        "do the editing"

        allowed_propnames = ("power", "attribute1", "attribute2")

        caller = self.caller
        if not self.args or not self.name:
            caller.msg("Usage: +editnpc name[/propname][=propval]")
            return
        npc = caller.search(self.name)
        if not npc:
            return
        if not npc.access(caller, "edit"):
            caller.msg("You cannot change this NPC.")
            return
        if not self.propname:
            # this means we just list the values
            output = f"Properties of {npc.key}:"
            for propname in allowed_propnames:
                propvalue = npc.attributes.get(propname, default="N/A")
                output += f"\n {propname} = {propvalue}"
            caller.msg(output)
        elif self.propname not in allowed_propnames:
            caller.msg("You may only change %s." %
                              ", ".join(allowed_propnames))
        elif self.propval:
            # assigning a new propvalue
            # in this example, the properties are all integers...
            intpropval = int(self.propval)
            npc.attributes.add(self.propname, intpropval)
            caller.msg("Set %s's property '%s' to %s" %
                         (npc.key, self.propname, self.propval))
        else:
            # propname set, but not propval - show current value
            caller.msg("%s has property %s = %s" %
                         (npc.key, self.propname,
                          npc.attributes.get(self.propname, default="N/A")))
```

此指令範例展示了更高階解析的使用，但否則主要是錯誤
檢查。它會在同一個房間中搜尋給定的 npc，並檢查呼叫者是否確實擁有
在繼續之前「編輯」它的許可權。未經適當許可的帳戶甚至不會
能夠檢視給定 NPC 上的屬性。這取決於每場比賽是否應該如此。

像以前一樣將其新增到預設指令集中，您應該可以嘗試一下。

_注意：如果您希望玩家使用此指令來更改物件屬性，例如 NPC
name（`key` 屬性），您需要修改指令，因為「key」不是 Attribute（它是
無法透過 `npc.attributes.get` 檢索，但可以直接透過 `npc.key` 檢索）。我們將其保留為可選
exercise._

(making-the-npc-do-stuff-the-npc-command)=
### 讓 NPC 做事 - +npc 指令

最後，我們將發出一個指令來對 NPC 進行排序。目前，我們將限制此指令僅
可供對 NPC 具有「編輯」許可權的人員使用。如果可能的話，可以更改此設定
任何人都可以使用NPC。

NPC，因為它繼承了我們的角色typeclass，因此可以存取玩家執行的大多數指令。什麼
它無權訪問Session 和基於玩家的cmdsets（這意味著，除其他外，
他們無法在頻道上聊天，但如果您剛剛新增這些指令，他們就可以這樣做）。這使得
`+npc` 指令很簡單：

    +npc Anna = say Hello!
    Anna says, 'Hello!'

再次，新增到 `command.py` 模組的末尾：

```python
class CmdNPC(Command):
    """
    controls an NPC

    Usage:
        +npc <name> = <command>

    This causes the npc to perform a command as itself. It will do so
    with its own permissions and accesses.
    """
    key = "+npc"
    locks = "call:not perm(nonpcs)"
    help_category = "mush"

    def parse(self):
        "Simple split of the = sign"
        name, cmdname = None, None
        if "=" in self.args:
            name, cmdname = [part.strip()
                             for part in self.args.rsplit("=", 1)]
        self.name, self.cmdname = name, cmdname

    def func(self):
        "Run the command"
        caller = self.caller
        if not self.cmdname:
            caller.msg("Usage: +npc <name> = <command>")
            return
        npc = caller.search(self.name)
        if not npc:
            return
        if not npc.access(caller, "edit"):
            caller.msg("You may not order this NPC to do anything.")
            return
        # send the command order
        npc.execute_cmd(self.cmdname)
        caller.msg(f"You told {npc.key} to do '{self.cmdname}'.")
```

請注意，如果您發出錯誤的指令，您將不會看到任何錯誤訊息，因為該錯誤
將會回傳給npc物件，而不是你。如果你想讓玩家看到這個，你可以給
呼叫者的 session ID 到 `execute_cmd` 呼叫，如下所示：

```python
npc.execute_cmd(self.cmdname, sessid=self.caller.sessid)
```

然而，要記住的另一件事是，這是控制 NPCs 的非常簡單的方法。 Evennia
非常輕鬆地支援完整的木偶操作。一個帳戶（假設“puppet”許可權設定正確）
可以簡單地執行`@ic mynpc`並能夠「像」NPC那樣玩遊戲。這實際上就是這樣
當帳戶也控制其正常角色時就會發生。

(concluding-remarks)=
## 結束語

教學到此結束。看起來文字很多，但你需要寫的程式碼量是
其實比較短。至此，您應該已經瞭解了遊戲的基本框架並感受到了
遊戲編碼涉及哪些內容。

從這裡開始，您可以再建立一些 ChargenRooms 並將其連結到更大的網格。 `+setpower`
指令可以建立在更多指令之上或伴隨更多指令來獲得更複雜的角色
一代。

簡單的「力量」遊戲機制應該很容易擴充套件到更成熟和更成熟的東西。
有用，戰鬥得分原理也是如此。 `+attack` 可以針對
特定玩家（或NPC）並自動比較其相關屬性以確定結果。

要從這裡繼續，您可以檢視[教學世界](Beginner-Tutorial/Part1/Beginner-Tutorial-Tutorial-World.md)。對於
更具體的想法，請參閱[其他教學和提示](./Howtos-Overview.md)
如[Evennia元件概述](../Components/Components-Overview.md)。
