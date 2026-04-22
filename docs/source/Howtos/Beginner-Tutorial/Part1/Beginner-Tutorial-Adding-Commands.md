(adding-custom-commands)=
# 新增自訂指令

在本課中，我們將學習如何建立自己的 Evennia [指令](../../../Components/Commands.md) 如果您是 Python 新手，您還將學習一些有關如何操作字串並從 Evennia 中獲取資訊的更多基礎知識。

指令是處理使用者輸入並導致結果發生的東西。
例如 `look`，它會檢查您目前的位置並告訴您它的外觀以及其中的內容。

```{sidebar} 指令沒有型別分類

如果您剛學完上一課，您可能想知道指令和 CommandSets 不是 `typeclassed`。也就是說，它們的例項不會儲存到資料庫中。它們「只是」普通的 Python 類別。
```

在 Evennia 中，指令是 Python _class_。如果您不確定什麼是類，請檢視
[上一課關於它](./Beginner-Tutorial-Python-classes-and-objects.md)！指令繼承自 `evennia.Command` 或替代指令類別之一，例如 `MuxCommand`，這是大多數預設指令使用的。

所有指令都分組在另一個稱為「指令集」的類別中。將指令集視為包含許多不同指令的袋子。例如，一個 CmdSet 可以儲存所有戰鬥指令，另一個用於建築等。

然後指令集與物件相關聯，例如與您的角色相關聯。這樣做會使 cmdset 中的指令可供該物件使用。預設情況下，Evennia 將所有字元指令分組為一個大的 cmdset，稱為 `CharacterCmdSet`。它位於 `DefaultCharacter`（因此，透過繼承，位於 `typeclasses.characters.Character`）。

(creating-a-custom-command)=
## 建立自訂指令

開啟`mygame/commands/command.py`。該檔案已為您填寫了內容。

```python
"""
(module docstring)
"""

from evennia import Command as BaseCommand
# from evennia import default_cmds

class Command(BaseCommand):
    """
    (class docstring)
    """
    pass

# (lots of commented-out stuff)
# ...
```

忽略檔案字串（如果需要，您可以閱讀），這是模組中唯一真正活躍的程式碼。

我們可以看到，我們從`evennia`匯入`Command`，並使用`from... import... as...`形式將其重新命名為`BaseCommand`。這樣我們就可以讓我們的子類別也命名為`Command`，以方便引用。  類別本身不執行任何操作，它只具有`pass`。因此，與前面課程的 `Object` 和 `Character` 相同，該類別與其父類相同。

> 註解掉的 `default_cmds` 使我們能夠存取 Evennia 的預設指令，以便於覆蓋。我們稍後會嘗試一下。

我們可以直接修改這個模組，但是讓我們在一個單獨的模組中工作只是為了它。開啟一個新檔案`mygame/commands/mycommands.py`並新增以下程式碼：

```python
# in mygame/commands/mycommands.py

from commands.command import Command

class CmdEcho(Command):
    key = "echo"

```

這是您能想像到的最簡單的指令形式。它只是給自己起了一個名字，「echo」。這是您稍後將用來呼叫此指令的內容。

接下來我們需要將其放入 CmdSet 中。現在這將是一個單一指令CmdSet！更改您的檔案如下：


```python
# in mygame/commands/mycommands.py

from commands.command import Command
from evennia import CmdSet

class CmdEcho(Command):
    key = "echo"


class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEcho)

```

我們的 `MyCmdSet` 類別必須有一個 `at_cmdset_creation` 方法，其命名與此完全相同 - 這是 Evennia 稍後在設定 cmdset 時將要查詢的內容，因此，如果您沒有設定它，它將使用父級的版本，該版本為空。裡面我們透過`self.add()`將指令類別加入到cmdset中。如果您想為 CmdSet 新增更多指令，您可以在此之後新增更多 `self.add` 行。

最後，讓我們自己加入這個指令，以便我們可以嘗試一下。在遊戲中你可以再嘗試`py`：

    > py me.cmdset.add("commands.mycommands.MyCmdSet")

`me.cmdset` 是我們儲存的所有 cmdsets 的儲存。透過提供 CmdSet 類別的路徑，它將被新增。

現在嘗試

    > echo
    Command "echo" has no defined `func()`. Available properties ...
    ...(lots of stuff)...

`echo` 有效！您應該會得到一長串輸出。您的 `echo` 函式還沒有真正「執行」任何操作，預設函式是在您使用指令時顯示所有可用的有用資源。讓我們看看其中列出的一些：

```
Command "echo" has no defined `func()` method. Available properties on this command are:

     self.key (<class 'str'>): "echo"
     self.cmdname (<class 'str'>): "echo"
     self.raw_cmdname (<class 'str'>): "echo"
     self.raw_string (<class 'str'>): "echo
"
     self.aliases (<class 'list'>): []
     self.args (<class 'str'>): ""
     self.caller (<class 'typeclasses.characters.Character'>): YourName
     self.obj (<class 'typeclasses.characters.Character'>): YourName
     self.session (<class 'evennia.server.serversession.ServerSession'>): YourName(#1)@1:2:7:.:0:.:0:.:1
     self.locks (<class 'str'>): "cmd:all();"
     self.help_category (<class 'str'>): "general"
     self.cmdset (... a long list of commands ...)
```
這些都是您可以在指令例項上使用 `.` 存取的所有屬性，例如 `.key`、`.args` 等。 Evennia 使這些可供您使用，並且每次執行指令時它們都會不同。我們現在將使用的最重要的是：

 - `caller` - 這是“你”，呼叫指令的人。
 - `args` - 這是指令的所有引數。現在它是空的，但如果您嘗試 `echo foo bar`，您會發現這將是 `" foo bar"`（包括您可能想要刪除的 `echo` 和 `foo` 之間的額外空格）。
 - `obj` - 這是此指令（和 CmdSet）「所在」的物件。所以，在這種情況下，你。
 - `raw_string` 不常用，但它是使用者完全未修改的輸入。它甚至包括用於將指令傳送到伺服器的換行符（這就是為什麼結束引號出現在下一行的原因）。

我們的指令尚未執行任何操作的原因是它缺少 `func` 方法。這就是 Evennia 尋找的內容來找出指令的實際作用。修改你的`CmdEcho`類：

```python
# in mygame/commands/mycommands.py
# ...

class CmdEcho(Command):
    """
    A simple echo command

    Usage:
        echo <something>

    """
    key = "echo"

    def func(self):
        self.caller.msg(f"Echo: '{self.args}'")

# ...
```

首先我們加入了一個文件字串。一般來說，這總是一件好事，但對於 Command 類別來說，它也會自動成為遊戲中的幫助條目！

```{sidebar} 使用指令.msg
在 Command 類別中，`self.msg()` 充當 `self.caller.msg()` 的便捷快捷方式。它不僅更短，而且還具有一些優點，因為該指令可以在訊息中包含更多元資料。所以使用 `self.msg()` 通常會更好。但對於本教學來說，`self.caller.msg()` 更明確地顯示了正在發生的情況。
```

接下來我們加入 `func` 方法。它有一個活動行，它使用 Command 類別向我們提供的一些變數。如果您完成了[基礎Python教學](./Beginner-Tutorial-Python-basic-introduction.md)，您將識別`.msg` - 這將向它附加到我們的物件傳送一條訊息 - 在本例中為`self.caller`，即我們。我們抓取 `self.args` 並將其包含在訊息中。

由於我們沒有更改 `MyCmdSet`，因此它將像以前一樣工作。重新載入並重新新增此指令給我們自己來嘗試新版本：

    > reload
    > py self.cmdset.add("commands.mycommands.MyCmdSet")
    > echo
    Echo: ''

嘗試傳遞一個引數：

    > echo Woo Tang!
    Echo: ' Woo Tang!'

請注意，`Woo` 之前有一個額外的空格。這是因為 self.args 包含指令名稱後的_所有內容_，包括空格。讓我們透過一個小調整來刪除多餘的空間：

```python
# in mygame/commands/mycommands.py
# ...

class CmdEcho(Command):
    """
    A simple echo command

    Usage:
        echo <something>

    """
    key = "echo"

    def func(self):
        self.caller.msg(f"Echo: '{self.args.strip()}'")

# ...
```

唯一的差異是我們在 `self.args` 上呼叫了 `.strip()`。這是一個可用於所有字串的輔助方法 - 它刪除字串前後的所有空格。現在指令引數前面將不再有任何空格。

    > reload
    > py self.cmdset.add("commands.mycommands.MyCmdSet")
    > echo Woo Tang!
    Echo: 'Woo Tang!'

不要忘記檢視 echo 指令的幫助：

    > help echo

您將獲得放入 Command 類別中的檔案字串！

(making-our-cmdset-persistent)=
### 讓我們的cmdset持久

每次重新載入時都必須重新新增cmdset，這有點煩人，對吧？不過，將 `echo` 改為 _persistent_ 就夠簡單了：

    > py self.cmdset.add("commands.mycommands.MyCmdSet", persistent=True)

現在您可以根據需要`reload`，並且您的程式碼變更將直接可用，而無需再次重新新增MyCmdSet。

我們將以另一種方式新增這個cmdset，所以手動刪除它：

    > py self.cmdset.remove("commands.mycommands.MyCmdSet")

(add-the-echo-command-to-the-default-cmdset)=
### 新增echo指令預設cmdset

上面我們給自己加了`echo`指令。它_僅_對我們可用，而遊戲中的其他人無法使用。但是 Evennia 中的所有指令都是指令集的一部分，包括我們一直在使用的普通 `look` 和 `py` 指令。您可以使用 `echo` 指令輕鬆擴充套件預設指令集 - 這樣遊戲中的_每個人_都可以存取它！

在 `mygame/commands/` 中，您會發現一個名為 `default_cmdsets.py` 的現有模組，開啟它，您會發現四個空的 cmdset 類別：

- `CharacterCmdSet` - 這適用於所有角色（這是我們通常要修改的角色）
- `AccountCmdSet` - 這位於所有帳戶上（在角色之間共享，例如 `logout` 等）
- `UnloggedCmdSet` - 登入前可用的指令，例如建立密碼和連線遊戲的指令。
- `SessionCmdSet` - 您的Session（您的特定使用者端連線）獨有的指令。預設未使用此功能。

如下調整該檔案：

```python
# in mygame/commands/default_cmdsets.py 

# ... 

from . import mycommands    # <-------  

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
 
    key = "DefaultCharacter"
 
    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(mycommands.CmdEcho)    # <-----------

# ... 
```

```{sidebar} super() 和覆蓋預設值
`super()` Python 關鍵字意味著 _parent_ 被呼叫。在這種情況下，父級將所有預設指令新增至此cmdset。

巧合的是，這也是你將 Evennia!jj 中的預設指令替換為 e.g 的方法。指令 `get`，您只需為替換指令提供 `key` 'get' 並將其新增到此處 - 因為它是在 `super()` 之後新增的，所以它將替換預設版本的 `get`。
```
這與將 `CmdEcho` 新增到 `MyCmdSet` 的方式相同。唯一的差異 cmdsets 會自動新增到所有角色/帳戶等中，因此您無需手動執行此操作。我們還必須確保從 `mycommands` 模組匯入 `CmdEcho`，以便該模組瞭解它。 `from. import mycommands` 中的句點「`.`」表示我們告訴 Python `mycommands.py` 與目前模組位於同一目錄中。我們想要匯入整個模組。再往下，我們訪問 `mycommands.CmdEcho` 將其新增到字元 cmdset。

只需 `reload` 伺服器和您的 `echo` 指令將再次可用。給定指令可以包含多少個 cmdsets 沒有限制。

要刪除，只需註解掉或刪除 `self.add()` 行即可。不過現在就保持這樣——我們將在下面對其進行擴充套件。
(figuring-out-who-to-hit)=
### 弄清楚該打誰

讓我們嘗試一些比 echo 更令人興奮的東西。讓我們建立一個 `hit` 指令，用於打某人的臉！這就是我們希望它能運作的方式：

    > hit <target>
    You hit <target> with full force!

不僅如此，我們還希望`<target>`看到

    You got hit by <hitter> with full force!

這裡，`<hitter>`是使用`hit`指令的人，`<target>`是進行打孔的人；因此，如果您的名字是 `Anna`，並且您擊中了名為 `Bob` 的人，則結果將如下所示：

    > hit bob
    You hit Bob with full force!

鮑伯會看到

    You got hit by by Anna with full force!

仍在 `mygame/commands/mycommands.py` 中，新增一個新類，位於 `CmdEcho` 和 `MyCmdSet` 之間。

```{code-block} python
:linenos:
:emphasize-lines: 5,6,13,16,19,20,21,23
# in mygame/commands/mycommands.py

# ...

class CmdHit(Command):
    """
    Hit a target.

    Usage:
      hit <target>

    """
    key = "hit"

    def func(self):
        args = self.args.strip()
        if not args:
            self.caller.msg("Who do you want to hit?")
            return
        target = self.caller.search(args)
        if not target:
            return
        self.caller.msg(f"You hit {target.key} with full force!")
        target.msg(f"You got hit by {self.caller.key} with full force!")

# ...
```

這裡有很多東西要剖析：
- **第 5 行**：正常的 `class` 標頭。我們繼承了在此檔案頂部匯入的`Command`。
- **第 6-12 行**：指令的文件字串和說明條目。您可以根據需要對此進行擴充。
- **第13行**：我們想寫`hit`來使用這個指令。
- **第 16 行**：我們像以前一樣從引數中刪除空格。由於我們不想一遍又一遍地執行 `self.args.strip()`，因此我們將剝離的版本儲存在_區域性變數_ `args` 中。請注意，我們不會透過這樣做來修改 `self.args`，`self.args` 仍然會有空格，並且與本範例中的 `args` 不同。

```{sidebar} if 語句
if 語句的完整形式是
	
如果條件：
	    …
	elif 其他條件：
	    …
	其他：
	    …

可以有任意數量的 `elifs` 來標記程式碼的不同分支何時應執行。如果提供了 `else`，則在其他條件都不為真時它將執行。
```

- **第 17 行**有我們的第一個_條件_，一個 `if` 語句。它以 `if <condition>:` 的形式編寫，只有當條件為「true」時，`if` 語句下的縮排程式碼區塊才會運作。要了解 Python 中什麼是真實的，通常更容易瞭解什麼是「虛假」：
    - `False` - 這是 Python 中的保留布林詞。相反的是`True`。
    - `None` - 另一個保留字。這代表什麼也沒有，一個空結果或值。
    - `0` 或 `0.0`
    - 空字串 `""`、`''` 或空三字串，例如 `""""""`、`''''''`
    - 我們還沒有使用空_iterables_，例如空列表`[]`、空元組`()`和空字典`{}`。
    - 其他一切都是「真實的」。

    The conditional on **Line 16**'s condition is `not args`. The `not` _inverses_ the result, so if `args` is the empty string (falsy), the whole conditional becomes truthy. Let's continue in the code:
```{sidebar} 您的程式碼中的錯誤

透過嘗試更長的程式碼片段，您將越來越有可能
重新載入時出錯並收到 `traceback`。這將出現
直接在遊戲中或在日誌中（在終端中使用 `evennia -l` 檢視）。

不要驚慌－回溯是你的朋友！它們應該自下而上地閱讀，並且通常準確地描述了您的問題所在。更多提示請參考[Python入門課](./Beginner-Tutorial-Python-basic-introduction.md)。如果您遇到困難，請向 Evennia 社群尋求協助。
```
- **第 16-17 行**：僅當 `if` 語句為真時，此程式碼才會執行，在本例中，如果 `args` 為空字串。
- **第 19 行**：`return` 是一個保留的 Python 字，立即退出 `func`。
- **第20行**：我們使用`self.caller.search`在目前位置找出目標。
- **第21-22行**：`.search`的一個特點是，如果它找不到目標，它會通知`self.caller`。在這種情況下，`target` 將是 `None`，我們應該直接`return`。
- **第23-24行**：此時我們有了一個合適的目標，並且可以向​​每個目標傳送我們的打孔字串。

最後我們還必須將其新增到CmdSet。讓我們將其新增到`MyCmdSet`。

```python
# in mygame/commands/mycommands.py

# ...
class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEcho)
        self.add(CmdHit)

```

請注意，由於我們之前執行了 `py self.cmdset.remove("commands.mycommands.MyCmdSet")`，因此該 cmdset 在我們的角色上不再可用。相反，我們將這些指令直接新增到我們的預設cmdset。

```python
# in mygame/commands/default_cmdsets.py 

# ,.. 

from . import mycommands    

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
 
    key = "DefaultCharacter"
 
    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(mycommands.MyCmdSet)    # <-----------
# ... 
```

我們從新增單一 `echo` 指令更改為一次性新增整個 `MyCmdSet`！這會將 cmdset 中的所有指令新增到 `CharacterCmdSet` 中，並且是一次性新增大量指令的實用方法。一旦你進一步探索Evennia，你會發現[Evennia contribs](../../../Contribs/Contribs-Overview.md)都在cmdsets中分發了他們的新指令，所以你可以像這樣輕鬆地將它們新增到你的遊戲中。

接下來我們重新載入，讓Evennia知道這些程式碼更改並嘗試：

    > reload
    hit
    Who do you want to hit?
    hit me
    You hit YourName with full force!
    You got hit by YourName with full force!

缺乏目標，我們就打擊了自己。如果你還有上一課中的一條龍，你可以嘗試擊中它（如果你敢的話）：

    hit smaug
    You hit Smaug with full force!

您將看不到第二根字串。只有史矛革看到了這一點（而且不覺得好笑）。


(summary)=
## 概括

在本課中，我們學習如何建立自己的指令，將其新增到 CmdSet，然後新增到我們自己。我們還惹惱了一條龍。

在下一課中，我們將學習如何使用不同的武器攻擊史矛革。我們也會
瞭解我們如何替換和擴充套件 Evennia 的預設指令。
