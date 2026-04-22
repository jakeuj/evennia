(parsing-command-input)=
# 解析指令輸入

在本課中，我們學習一些關於解析指令輸入的基礎知識。我們會
也瞭解如何新增、修改和擴充套件 Evennia 的預設指令。

(more-advanced-parsing)=
## 更進階的解析

在[上一課](./Beginner-Tutorial-Adding-Commands.md)中，我們發出了`hit`指令並用它攻擊了一條龍。您應該還保留著該程式碼。

讓我們擴充套件簡單的 `hit` 指令來接受更複雜的輸入：

    hit <target> [[with] <weapon>]

也就是說，我們要支援所有這些形式

    hit target
    hit target weapon
    hit target with weapon

如果你沒有指定武器，你就會使用拳頭。能夠跳過“with”if也很好
你很著急。是時候再修改`mygame/commands/mycommands.py`了。讓我們用一種新方法 `parse` 稍微分解解析一下：


```{code-block} python
:linenos:
:emphasize-lines: 14,15,16,18,29,35,41
#...

class CmdHit(Command):
    """
    Hit a target.

    Usage:
      hit <target>

    """
    key = "hit"

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = ""

    def func(self):
        if not self.args:
            self.caller.msg("Who do you want to hit?")
            return
        # get the target for the hit
        target = self.caller.search(self.target)
        if not target:
            return
        # get and handle the weapon
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weaponstr = "bare fists"

        self.caller.msg(f"You hit {target.key} with {weaponstr}!")
        target.msg(f"You got hit by {self.caller.key} with {weaponstr}!")
# ...
```

`parse` 方法是一種特殊的方法，Evennia 知道在 _before_ `func` 之前呼叫。此時，它可以存取與 `func` 相同的所有指令變數。使用 `parse` 不僅使內容更容易閱讀，還意味著您可以輕鬆地讓其他指令_繼承_您的解析 - 如果您希望其他指令也理解 `<arg> with <arg>` 形式的輸入，您可以從此類繼承，並且只需實現該指令所需的 `func` 而無需重新實現 `parse`。

```{sidebar} 元組和列表

- `list` 寫為 `[a, b, c, d,...]`。您可以在首次建立清單後新增和擴大/縮小清單。
- `tuple` 寫為 `(a, b, c, d,...)`。元組一旦建立就無法修改。

```
- **第 14 行** - 我們在這裡一勞永逸地剝離 `self.args`。我們還將剝離版本儲存回來
到 `self.args` 中，覆蓋它。所以從現在開始就沒有辦法找回未剝離的版本，這很好
  對於這個指令。
- **第 15 行** - 這使用了字串的 `.split` 方法。 `.split` 將依照某種標準分割字串。
    `.split(" with ", 1)` means "split the string once, around the substring `" with "` if it exists". The result
    of this split is a _list_. Just how that list looks depends on the string we are trying to split:
    1. If we entered just `hit smaug`, we'd be splitting just `"smaug"` which would give the result `["smaug"]`.
    2. `hit smaug sword` gives `["smaug sword"]`
    3. `hit smaug with sword` gives `["smaug", "sword"]`

    So we get a list of 1 or 2 elements. We assign it to two variables like this, `target, *weapon = `. That asterisk in `*weapon` is a nifty trick - it will automatically become a tuple of _0 or more_ values. It sorts of "soaks" up everything left over.
    1. `target` becomes `"smaug"` and `weapon` becomes `()` (an empty tuple)
    2. `target` becomes `"smaug sword"` and `weapon` becomes `()`
    3. `target` becomes `"smaug"` and `weapon` becomes `("sword",)` (this is a tuple with one element, the comma [is required](https://docs.python.org/3/tutorial/datastructures.html?highlight=tuple#tuples-and-sequences) to indicate this).
	
- **第 16-17 行** - 在這個 `if` 條件下，我們檢查 `weapon` 是否為假（即空清單）。這可能會發生
    under two conditions (from the example above):
    1. `target` is simply `smaug`
    2. `target` is `smaug sword`

    To separate these cases we split `target` once again, this time by empty space `" "`. Again we store the result back with `target, *weapon =`. The result will be one of the following:
    1. `target` remains `"smaug"` and `weapon` remains `[]`
    2. `target` becomes `"smaug"` and `weapon` becomes `("sword",)`
- **第 18-22 行** - 我們現在將 `target` 和 `weapon` 儲存到 `self.target` 和 `self.weapon` 中。我們必須儲存在 `self` 上，以便這些區域性變數稍後在 `func` 中可用。請注意，一旦我們知道 `weapon` 存在，它一定是一個元組（如 `("sword",)`），因此我們使用 `weapon[0]` 來獲取該元組的第一個元素（Python 中的元組和列表從 0 開始索引）。指令 `weapon[0].strip()` 可以理解為「取得儲存在元組 `weapon` 中的第一個字串，並使用 `.strip()` 刪除其上的所有多餘空格」。如果我們忘記了 `[0]` ，我們會得到一個錯誤，因為元組（與元組中的字串不同）沒有 `.strip()` 方法。

現在進入 `func` 方法。主要差異是我們現在有 `self.target` 和 `self.weapon` 可供方便使用。
```{sidebar}
在這裡，我們建立要明確傳送給戰鬥各方的訊息。稍後我們將瞭解如何使用 Evennia 的[行內函數](../../../Components/FuncParser.md) 傳送看起來不同的字串，具體取決於誰看到它。
```

- **第 29 行和第 35 行** - 我們利用先前解析的目標和武器搜尋字詞來找出
    respective resource.
- **第 34-39 行** - 由於武器是可選的，因此如果未設定，我們需要提供預設值（使用我們的拳頭！）。我們
    use this to create a `weaponstr` that is different depending on if we have a weapon or not.
- **第 41-42 行** - 我們將 `weaponstr` 與我們的攻擊文字合併，並將其分別傳送給攻擊者和目標。

我們來嘗試一下吧！

    > reload
    > hit smaug with sword
    Could not find 'sword'.
    You hit smaug with bare fists!

糟糕，`self.caller.search(self.weapon)` 告訴我們它沒有找到劍。這是合理的（我們沒有劍）。因為我們不會像找不到`target`時那樣`return`找不到武器，所以我們仍然繼續徒手戰鬥。

這不行。讓我們為自己打造一把劍：

    > create sword

由於我們沒有指定 `/drop`，劍最終會出現在我們的庫存中，並且可以使用 `i` 或 `inventory` 指令看到。 `.search` 助手仍會在那裡找到它。無需重新載入即可看到此更改（未更改程式碼，僅更改資料庫中的內容）。

    > hit smaug with sword
    You hit smaug with sword!

可憐的史矛革。

(adding-a-command-to-an-object)=
## 向物件新增指令

```{sidebar} 角色指令集
如果您想知道，`Characters` 上的「角色 CmdSet」被設定為_僅_該角色可用。如果沒有，每當您與使用相同指令集的另一個角色在同一個房間時，您都會獲得諸如 `look` 之類的指令多重匹配。有關詳細資訊，請參閱[指令集](../../../Components/Command-Sets.md) 檔案。
```
正如我們在[新增指令](./Beginner-Tutorial-Adding-Commands.md) 課程中學到的，指令被分組在指令集中。此類指令集附加到具有 `obj.cmdset.add()` 的物件，然後可供該物件使用。

我們之前沒有提到的是，預設情況下，這些指令_也可供與該物件位於相同位置的指令使用_。如果您上過[建立快速入門課程](./Beginner-Tutorial-Building-Quickstart.md)，您會看到帶有「紅色按鈕」物件的範例。 [教學世界](./Beginner-Tutorial-Tutorial-World.md) 還有許多帶有指令的物件範例。

為了展示這是如何運作的，讓我們將「hit」指令放在上一節中的簡單 `sword` 物件上。

    > py self.search("sword").cmdset.add("commands.mycommands.MyCmdSet", persistent=True)

我們找到了劍（它仍在我們的庫存中，所以`self.search`應該能夠找到它），然後
新增 `MyCmdSet` 到它。這實際上給劍增加了`hit`和`echo`，這很好。

讓我們試著搖擺它吧！

    > hit
    More than one match for 'hit' (please narrow target):
    hit-1 (sword #11)
    hit-2

```{sidebar} 多場比賽

有些遊戲引擎在找到多個時只會選擇第一個命中。 Evennia總是會給你一個選擇。原因是 Evennia 無法知道 `hit` 和 `hit` 是否不同或相同 - 也許它的行為不同取決於它所在的物件？此外，想像一下如果您有一個紅色和一個藍色按鈕，上面都帶有指令`push`。現在你只需寫`push`。難道您不想被問到您真正想按哪個按鈕嗎？
```

哇哦，事情沒有照計劃進行。 Evennia 實際上找到_兩個_ `hit` 指令，但不知道該使用哪一個（_我們_知道它們是相同的，但 Evennia 無法確定）。正如我們所看到的，`hit-1`是在劍上發現的。另一種是之前給我們自己加上`MyCmdSet`。很容易告訴 Evennia 你指的是哪一個：

    > hit-1
    Who do you want to hit?
    > hit-2
    Who do you want to hit?

在這種情況下，我們不需要這兩個指令集，我們應該放棄我們自己的 `hit` 版本。

轉到`mygame/commands/default_cmdsets.py`並找到您新增的行
`MyCmdSet` 在上一堂課中。刪除或註解掉：

```python
# mygame/commands/default_cmdsets.py 

# ...

class CharacterCmdSet(default_cmds.CharacterCmdSet):

    # ... 
    def at_object_creation(self): 

        # self.add(MyCmdSet)    # <---------

```

接下來`reload`，您將只有一個可用的`hit`指令：

    > hit
    Who do you want to hit?

現在嘗試建立一個新位置，然後將劍放入其中。

    > tunnel n = kitchen
    > n
    > drop sword
    > s
    > hit
    Command 'hit' is not available. Maybe you meant ...
    > n
    > hit
    Who do you want to hit?

只有當您持有或與劍位於同一房間時，`hit` 指令才可用。

(you-need-to-hold-the-sword)=
### 你需要握緊劍！

```{sidebar} 鎖具

Evennia 鎖定被定義為 `lockstrings` 中定義的迷你語言。鎖定字串採用 `<situation>:<lockfuncs>` 形式，其中 `situation` 確定何時應用此 lock，並根據情況執行 `lockfuncs`（可以有多個）來確定 lock 檢查是否透過。
```

讓我們稍微超前一點，讓你必須握住劍才能使用 `hit` 指令。這涉及到[Lock](../../../Components/Locks.md)。稍後我們將更詳細地介紹鎖，只需知道它們對於限制您可以對物件執行的操作型別非常有用，包括限制您何時可以對其呼叫指令。

    > py self.search("sword").locks.add("call:holds()")

我們為劍增加了一個新的lock。 _lockstring_ `"call:holds()"` 表示如果您_持有_該物件（也就是說，它在您的庫存中），您只能_呼叫_該物件上的指令。

要使鎖發揮作用，您不能成為_超級使用者_，因為超級使用者會傳遞所有鎖。你需要先`quell`自己：

```{sidebar} 平息/取消平息

壓制讓您作為開發者可以扮演許可權較低的玩家角色。這對於測試和除錯很有用，特別是因為超級使用者有時有一點 `too` 的權力。使用`unquell`恢復正常。
```

    > quell
	
如果劍落在地上，請嘗試

    > hit
    Command 'hit' is not available. ..
    > get sword
    > hit
    > Who do you want to hit?

在我們揮舞劍（擊中一兩條龍）後，我們將擺脫我們的劍，這樣我們就可以重新開始，不再有 `hit` 指令漂浮在周圍。我們可以透過兩種方式做到這一點：

    delete sword

或者

    py self.search("sword").delete()


(adding-the-command-to-a-default-cmdset)=
## 將指令新增到預設Cmdset


正如我們所看到的，我們可以使用 `obj.cmdset.add()` 向物件新增新的 cmdset，無論該對像是我們自己 (`self`) 還是其他物件，例如 `sword`。雖然這樣做有點麻煩。最好將這個新增到所有字元中。

預設的 cmdset 在 `mygame/commands/default_cmdsets.py` 中定義。現在開啟該檔案：

```python
"""
(module docstring)
"""

from evennia import default_cmds

class CharacterCmdSet(default_cmds.CharacterCmdSet):

    key = "DefaultCharacter"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #

class AccountCmdSet(default_cmds.AccountCmdSet):

    key = "DefaultAccount"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #

class SessionCmdSet(default_cmds.SessionCmdSet):

    key = "DefaultSession"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #
```

```{sidebar} 極好的（）

`super()` 函式引用目前類別的父類，通常用於呼叫父類上的同名方法。
```
`evennia.default_cmds` 是一個容器，包含Evennia 的所有預設指令和cmdsets。在此模組中，我們可以看到它已匯入，然後為每個 cmdset 建立了一個新的子類別。每個類別看起來都很熟悉（`key` 除外，它主要用於輕鬆識別清單中的 cmdset）。在每個 `at_cmdset_creation` 中，我們所做的就是呼叫 `super().at_cmdset_creation`，這表示我們在 _parent_ CmdSet 上呼叫 `at_cmdset_creation()。

這就是將所有預設指令新增到每個 CmdSet 的原因。

當建立 `DefaultCharacter` （或其子層級）時，您會發現呼叫了 `self.cmdset.add("default_cmdsets.CharacterCmdSet, persistent=True")` 的等效項。這意味著所有新角色都會獲得此 cmdset。新增更多指令後，您只需重新載入即可讓所有角色看到它。

- 角色（即遊戲世界中的「你」）具有`CharacterCmdSet`。
- 帳戶（代表您在伺服器上的異常存在的事物）具有 `AccountCmdSet`
- Sessions（代表一個用戶端連線）具有`SessionCmdSet`
- 在您登入之前（在連線畫面上），您的 Session 可以存取 `UnloggedinCmdSet`。

現在，讓我們將自己的 `hit` 和 `echo` 指令加入 `CharacterCmdSet` 中：


```python
# ...

from commands import mycommands

class CharacterCmdSet(default_cmds.CharacterCmdSet):

    key = "DefaultCharacter"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #
        self.add(mycommands.CmdEcho)
        self.add(mycommands.CmdHit)

```

    > reload
    > hit
    Who do you want to hit?

您的新指令現在可用於遊戲中的所有玩家角色。還有另一種方法可以一次加一堆指令，那就是把你自己的_CmdSet_加到其他cmdset中。

```python
from commands import mycommands

class CharacterCmdSet(default_cmds.CharacterCmdSet):

    key = "DefaultCharacter"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #
        self.add(mycommands.MyCmdSet)
```

你使用哪種方式取決於你想要多少控制權，但如果你已經有CmdSet，
這是實用的。一個指令可以是任意數量的不同CmdSets的一部分。

(removing-commands)=
### 刪除指令

要再次刪除自訂指令，您當然只需刪除您所做的更改即可
`mygame/commands/default_cmdsets.py`。但是如果您想刪除預設指令怎麼辦？

我們已經知道我們使用 `cmdset.remove()` 來刪除 cmdset。事實證明你可以
在 `at_cmdset_creation` 中執行相同操作。例如，讓我們刪除預設的 `get` 指令
從Evennia開始。如果您調查 `default_cmds.CharacterCmdSet` 父級，您會發現它的類別是 `default_cmds.CmdGet`（「真實」位置是 `evennia.commands.default.general.CmdGet`）。


```python
# ...
from commands import mycommands

class CharacterCmdSet(default_cmds.CharacterCmdSet):

    key = "DefaultCharacter"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #
        self.add(mycommands.MyCmdSet)
        self.remove(default_cmds.CmdGet)
# ...
```

    > reload
    > get
    Command 'get' is not available ...

(replace-a-default-command)=
## 替換預設指令

此時，您已經掌握瞭如何執行此操作的所有內容！我們只需要增加一個新的
指令中的`CharacterCmdSet`用相同的`key`來替換預設的。

讓我們將其與我們對類別的瞭解以及如何_覆蓋_父類結合。開啟 `mygame/commands/mycommands.py` 並建立一個新的 `get` 指令：

```{code-block} python
:linenos:
:emphasize-lines: 2,7,8,9

# up top, by the other imports
from evennia import default_cmds

# somewhere below
class MyCmdGet(default_cmds.CmdGet):

    def func(self):
        super().func()
        self.caller.msg(str(self.caller.location.contents))
```

- **第2行**：我們匯入`default_cmds`，這樣我們就可以獲得父類別。
我們建立了一個新類，並使其_繼承_`default_cmds.CmdGet`。我們不
需要設定 `.key` 或 `.parse`，這已由父級處理。
在 `func` 中，我們呼叫 `super().func()` 讓父行程做正常的事情，
- **第 7 行**：透過新增我們自己的`func`，我們取代了父級中的`func`。
- **第 8 行**：對於這個簡單的更改，我們仍然希望該指令能夠正常工作
和以前一樣，所以我們使用 `super()` 來呼叫父級上的 `func` 。
- **第 9 行**：`.location` 是物件所在的位置。 `.contents` 包含，嗯，
    contents of an object. If you tried `py self.contents` you'd get a list that equals
    your inventory. For a room, the contents is everything in it.
    So `self.caller.location.contents` gets the contents of our current location. This is
    a _list_. In order send this to us with `.msg` we turn the list into a string. Python
    has a special function `str()` to do this.

我們現在只需新增此指令即可替換預設的 `get` 指令。開啟
再次`mygame/commands/default_cmdsets.py`：

```python
# ...
from commands import mycommands

class CharacterCmdSet(default_cmds.CharacterCmdSet):

    key = "DefaultCharacter"

    def at_cmdset_creation(self):

        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones
        #
        self.add(mycommands.MyCmdSet)
        self.add(mycommands.MyCmdGet)
# ...
```

我們不需要先使用`self.remove()`；只需新增具有相同`key` (`get`) 的指令將替換我們之前的預設`get`。

```{sidebar} 另一種方式

您也可以將其新增到 `mycommands.MyCmdSet` 中，並讓它在此處自動新增，而不是在 default_cmdset.py 中明確新增 `MyCmdGet`。
```

    > reload
    > get
    Get What?
    [smaug, fluffy, YourName, ...]

我們剛剛建立了一個新的 `get` 指令，它告訴我們可以拾取的所有內容（好吧，我們無法拾取自己，所以還有一些改進的空間...）。

(summary)=
## 概括

在本課中，我們學習了一些更高階的字串格式 - 其中許多技巧將對您將來有很大幫助！我們還製作了一把實用的劍。最後我們討論瞭如何新增、擴充套件和替換我們自己的預設指令。知道新增指令是製作遊戲的重要組成部分！

我們已經打敗可憐的史矛革太久了。接下來我們將創造更多可以玩的東西。