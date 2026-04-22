(commands)=
# 指令


指令與[指令集](./Command-Sets.md) 密切相關，您也需要閱讀該頁面才能
熟悉指令系統的工作原理。為了方便閱讀，將兩頁分開。

使用者與遊戲溝通的基本方式是透過*指令*。這些可以是與遊戲世界直接相關的指令，例如 *look*、*get*、*drop* 等，也可以是管理指令，例如 *examine* 或 *dig*。

Evennia 附帶的[預設指令](./Default-Commands.md) 與“MUX-類似”，因為它們使用@作為管理指令，支援開關、帶有“=”符號的語法等，但沒有什麼可以阻止您為遊戲實現完全不同的指令方案。您可以在 `evennia/commands/default` 中找到預設指令。您不應直接編輯這些內容 - 隨著新功能的新增，Evennia 團隊將更新它們。相反，你應該向他們尋求靈感，並從他們那裡繼承你自己的設計。

執行指令有兩個元件 - *Command* 類別和 [指令集](./Command-Sets.md)（為了方便閱讀，指令集被分成一個單獨的 wiki 頁面）。

1. *Command* 是一個 Python 類，包含指令執行的所有功能程式碼 - 例如，*get* 指令將包含用於拾取物件的程式碼。
1. *指令集*（通常稱為 CmdSet 或 cmdset）就像一個或多個指令的容器。給定的指令可以進入任意數量的不同指令集。只有將指令集放在角色物件上，您才能使該角色可以使用其中的所有指令。如果您希望使用者能夠以各種方式使用物件，您也可以在普通對像上儲存指令集。考慮一個「樹」物件，其中 cmdset 定義了指令 *climb* 和 *chop down*。或一個帶有 cmdset 的“時鐘”，其中包含單一指令*檢查時間*。

本頁詳細介紹如何使用指令。要充分使用它們，您還必須閱讀詳細說明[指令集](./Command-Sets.md) 的頁面。  還有一個逐步的[新增指令教學](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)，可以讓您快速入門，無需額外的解釋。

(defining-commands)=
## 定義指令

所有指令都作為從基底類別繼承的普通Python類別來實現`Command`
(`evennia.Command`)。你會發現這個基類非常「裸露」。預設指令為
Evennia 實際上繼承自 `Command` 的名為 `MuxCommand` 的子級 - 這是這樣的類
知道所有類似 `/switches` 的類似 mux 的語法，用「=」等分割。下面我們將避免 mux-
具體情況並直接使用基 `Command` 類。

```python
    # basic Command definition
    from evennia import Command

    class MyCmd(Command):
       """
       This is the help-text for the command
       """
       key = "mycommand"
       def parse(self):
           # parsing the command line here
       def func(self):
           # executing the command here
```

這是一個沒有自訂解析的簡約指令：

```python
    from evennia import Command

    class CmdEcho(Command):
        key = "echo"

        def func(self):
            # echo the caller's input back to the caller
            self.caller.msg(f"Echo: {self.args}")

```

您可以透過在繼承的類別上指派一些類別全域屬性來定義一個新指令，
過載一兩個鉤子函式。找到了指令工作原理背後的完整機制
到本頁末；現在你只需要知道指令處理程式建立了一個
此類別的例項，並在您使用此指令時使用該例項 - 它也是動態的
為新指令例項指派一些有用的屬性，您可以假設它們始終可用。

(who-is-calling-the-command)=
### 誰在發出指令？

在Evennia中，有三種型別的物件可以呼叫該指令。  重要的是要意識到
因為這也將分配適當的 `caller`、`session`、`sessid` 和 `account`
執行時指令主體上的屬性。最常見的呼叫型別是 `Session`。

* 一個[Session](./Sessions.md)。這是迄今為止最常見的情況，當使用者在
他們的客戶。
    * `caller` - 如果存在這樣的物件，則將其設為傀儡的[物件](./Objects.md)。如果沒有
找到木偶，`caller` 設定為等於 `account`。僅當未找到帳戶時（例如
在登入之前）這將被設定為 Session 物件本身。
    * `session` - 對 [Session](./Sessions.md) 物件本身的引用。
    * `sessid` - `sessid.id`，session 的唯一整數識別碼。
    * `account` - 連線到此 Session 的 [帳戶](./Accounts.md) 物件。如果沒有登入則無。
* 一個[帳戶](./Accounts.md)。只有在使用 `account.execute_cmd()` 時才會發生這種情況。沒有Session
在這種情況下可以獲得資訊。
    * `caller` - 如果可以確定傀儡物件（無需
Session資訊只能在`MULTISESSION_MODE=0`或`1`中確定。如果沒有找到木偶，
這等於`account`。
    * `session` - `None*`
    * `sessid` - `None*`
    * `account` - 設定為帳戶物件。
* 一個[物件](./Objects.md)。只有在使用 `object.execute_cmd()` 時才會發生這種情況（例如由
NPC）。
    * `caller` - 這被設定為有問題的呼叫物件。
    * `session` - `None*`
    * `sessid` - `None*`
    * `account` - `None`

> `*)`：有一種方法可以使 Session 在直接在帳戶和物件上執行的測試中也可用，即將其傳遞給 `execute_cmd`，如下所示：`account.execute_cmd("...", session=<Session>)`。這樣做*將使 `.session` 和 `.sessid` 屬性在指令中可用。

(properties-assigned-to-the-command-instance-at-run-time)=
### 在執行時分配給指令例項的屬性

假設帳號 *Bob* 的角色為 *BigGuy* 輸入指令 *look at Sword*。在系統成功地將其識別為「look」指令並確定 BigGuy 確實有權存取名為 `look` 的指令後，它會從儲存中取出 `look` 指令類，並從快取中載入現有的指令例項或建立一個例項。經過更多檢查後，它會為其分配以下屬性：

- `caller` - 在此範例中為字元 BigGuy。這是對執行指令的物件的參考。該值取決於呼叫該指令的物件型別；請參閱上一節。
- `session` - Bob 用於連線到遊戲並控制 BigGuy 的 [Session](./Sessions.md)（另請參閱上一節）。
- `sessid` - `self.session`的唯一ID，用於快速尋找。
- `account` - [帳戶](./Accounts.md) Bob（請參閱上一節）。
- `cmdstring` - 指令的匹配鍵。在我們的範例中，這將是*look*。
- `args` - 這是字串的其餘部分，指令名稱除外。因此，如果輸入的字串是 *look at Sword*，`args` 將是「*at Sword*」。請注意保留的空格 - Evennia 也會正確解釋 `lookat sword`。這對於像 `/switches` 這樣不應該使用空間的東西很有用。在用於預設指令的 `MuxCommand` 類別中，該空格被刪除。如果要強制使用空格以使 `lookat sword` 給出指令未找到錯誤，另請參閱 `arg_regex` 屬性。
- `obj` - 定義此指令的遊戲[物件](./Objects.md)。  這不一定是呼叫者，但由於 `look` 是常見（預設）指令，因此可能直接在 *BigGuy* 上定義 - 因此 `obj` 將指向 BigGuy。  否則 `obj` 可以是一個帳戶或任何在其上定義了指令的互動式物件，例如在「時鐘」對像上定義的「檢查時間」指令的範例。 - `cmdset` - 這是對該指令的合併CmdSet（見下文）的引用
匹配。這個變數很少使用，它的主要用途是用於[自動幫助系統]（./Help-System.md#command-auto-help-system）（*高階注意：合併的cmdset需要NOT與`BigGuy.cmdset`相同。合併的集合可以是房間中其他物件的cmdsets的組合，例如*）。
- `raw_string` - 這是來自使用者的原始輸入，沒有剝離任何周圍的內容
空白。唯一被刪除的是結束換行符。

(other-useful-utility-methods)=
#### 其他有用的實用方法：

- `.get_help(caller, cmdset)` - 取得此指令的說明條目。預設情況下，不使用引數，但它們可用於實現備用幫助顯示系統。
- `.client_width()` - 取得使用者端螢幕寬度的捷徑。請注意，並非所有客戶都會
如實報告該值 - 這種情況將返回 `settings.DEFAULT_SCREEN_WIDTH`。 - `.styled_table(*args, **kwargs)` - 這將傳回基於呼叫此指令的 session 樣式的 [EvTable](module- evennia.utils.evtable)。 args/kwargs 與 EvTable 相同，但設定了預設樣式。
- `.styled_header`、`_footer`、`separator` - 這些將產生樣式裝飾以顯示給使用者。它們對於建立可按使用者調整顏色的清單和表單非常有用。

(defining-your-own-command-classes)=
### 定義您自己的指令類

除了屬性 Evennia 始終在執行時指派給指令（上面列出）之外，您的工作是定義以下類別屬性：

- `key`（字串）- 指令的識別符號，如 `look`。  這應該（理想情況下）是唯一的。一把鑰匙可以由多個單字組成，例如「按下按鈕」或「拉左控制桿」。請注意，下面的*`key` 和`aliases` 都確定了指令的標識。因此，如果兩個指令匹配，則考慮兩個指令。這對於下面描述的合併 cmdsets 很重要。
- `aliases`（可選清單）- 指令的備用名稱清單 (`["glance", "see", "l"]`)。適用與 `key` 相同的名稱規則。
- `locks`（字串）- [lock 定義](./Locks.md)，通常採用 `cmd:<lockfuncs>` 形式。鎖是一個相當大的主題，因此在您瞭解有關鎖的更多資訊之前，請堅持提供鎖字串 `"cmd:all()"` 以使該指令可供所有人使用（如果您不提供 lock 字串，則會為您分配該字串）。
- `help_category`（可選字串）- 設定此專案有助於將自動幫助分類。如果未設定，則將設定為*常規*。
- `save_for_next`（可選布林值）。預設為`False`。如果 `True`，則係統將儲存此指令物件的副本（以及您對其所做的任何更改），並且可以透過檢索 `self.caller.ndb.last_cmd` 來由下一個指令存取。下一個執行指令將清除或替換儲存。
- `arg_regex`（可選原始字串）：用於強制解析器限制自身並告訴它指令名稱結束和引數開始的時間（例如要求這是一個空格或/開關）。這是透過正規表示式完成的。 [詳情請參閱arg_regex部分](./Commands.md#arg_regex)。
- `auto_help`（可選布林值）。預設為`True`。這允許在每個指令的基礎上關閉[自動幫助系統](./Help-System.md#command-auto-help-system)。如果您想手動編寫說明條目或隱藏 `help` 的生成清單中指令的存在，這可能很有用。
- `is_exit` (bool) - 這將指令標記為用於遊戲內退出。預設情況下，這是由所有 Exit 物件設定的，除非您建立自己的 Exit 系統，否則不需要手動設定它。它用於最佳化，並允許 cmdhandler 在 cmdset 設定了 `no_exits` 標誌時輕鬆忽略此指令。
- `is_channel`（布林）- 這將指令標記為用於遊戲內頻道。預設情況下，這是由所有 Channel 物件設定的，除非您建立自己的 Channel 系統，否則不需要手動設定它。  用於最佳化，並允許 cmdhandler 在其 cmdset 設定了 `no_channels` 標誌時輕鬆忽略此指令。
- `msg_all_sessions`（布林值）：這會影響 `Command.msg` 方法的行為。如果未設定（預設），從指令呼叫 `self.msg(text)` 將始終僅將文字傳送到實際觸發此指令的 Session。但是，如果設定，`self.msg(text)` 將傳送到與此指令所在物件相關的所有 Sessions。到底哪個 Sessions 接收文字取決於物件和伺服器的 `MULTISESSION_MODE`。

您還應該至少實現兩個方法，`parse()` 和 `func()`（您也可以實現
`perm()`，但這不是必需的，除非您想從根本上改變訪問檢查的工作方式）。

- `at_pre_cmd()` 在指令中首先被呼叫。如果此函式傳回任何計算結果為 `True` 的指令，則此時將中止指令執行。
- `parse()` 用於解析函式的引數 (`self.args`)。您可以按照您喜歡的任何方式執行此操作，然後將結果儲存在指令物件本身的變數中（i.e。在 `self` 上）。舉個例子，預設的類似mux的系統使用這種方法來檢測「指令開關」並將它們作為列表儲存在`self.switches`中。由於指令方案中的解析通常非常相似，因此您應該使 `parse()` 盡可能通用，然後繼承它，而不是一遍又一遍地重新實現它。這樣，預設的 `MuxCommand` 類別就實現了 `parse()` 供所有子指令使用。
- `func()` 在 `parse()` 之後被呼叫，並且應該利用預先解析的輸入來實際執行指令應該執行的任何操作。這是指令的主體。此方法的傳回值將從執行中以 Twisted Deferred 傳回。
- `at_post_cmd()` 在 `func()` 之後呼叫以處理最終的清理。

最後，您應該始終在班級頂部製作一個內容豐富的 [doc string](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring) (`__doc__`)。 [幫助系統](./Help-System.md) 動態讀取該字串，以建立該指令的幫助條目。您應該決定一種格式化幫助的方法並堅持下去。

以下是如何定義一個簡單的替代「`smile`」指令：

```python
from evennia import Command

class CmdSmile(Command):
    """
    A smile command

    Usage:
      smile [at] [<someone>]
      grin [at] [<someone>]

    Smiles to someone in your vicinity or to the room
    in general.

    (This initial string (the __doc__ string)
    is also used to auto-generate the help
    for this command)
    """

    key = "smile"
    aliases = ["smile at", "grin", "grin at"]
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller

        if not self.target or self.target == "here":
            string = f"{caller.key} smiles"
        else:
            target = caller.search(self.target)
            if not target:
                return
            string = f"{caller.key} smiles at {target.key}"

        caller.location.msg_contents(string)

```

將指令作為類別並分隔 `parse()` 和 `func()` 的強大之處在於能夠繼承功能，而無需單獨解析每個指令。例如，如上所述，預設指令全部繼承自 `MuxCommand`。 `MuxCommand` 實現了自己的 `parse()` 版本，它理解 MUX- 之類指令的所有細節。因此，幾乎沒有一個預設指令根本不需要實現 `parse()`，但可以假設傳入的字串已經被其父級以適當的方式分割和解析。

在您實際在遊戲中使用該指令之前，您現在必須將其儲存在*指令集*中。請參閱[指令集](./Command-Sets.md) 頁面。

(command-prefixes)=
### 指令字首

從歷史上看，許多 MU* 伺服器過去使用字首，例如 `@` 或 `&` 來表示指令用於管理或需要員工許可權。這樣做的問題是，MU 的新手經常會發現這些額外的符號令人困惑。 Evennia 允許使用或不使用這樣的字首來存取指令。

    CMD_IGNORE_PREFIXES = "@&/+`

這是一個由字串組成的設定。每個都是一個字首，將被視為可跳過的字首 - _如果跳過字首時該指令在其 cmdset 中仍然是唯一的_。

因此，如果您想寫 `@look` 而不是 `look`，您可以這樣做 - `@` 將被忽略。但如果我們加入了實際的 `@look` 指令（有 `key` 或別名 `@look`），那麼我們需要使用 `@` 來分隔兩者。

這也用在預設指令中。例如，`@open` 是一個建築指令，允許您建立新出口以將兩個房間連線在一起。其 `key` 設定為 `@open`，包括 `@`（未設定別名）。預設情況下，您可以為此指令使用 `@open` 和 `open`。但「開啟」是一個非常常見的詞，假設開發人員新增了一個新的 `open` 指令來開啟門。現在 `@open` 和 `open` 是兩個不同的指令，必須使用 `@` 來分隔它們。

> `help` 指令會優先顯示所有不含字首的指令名稱，如果
> 可能的。只有發生衝突時，字首才會顯示在幫助系統中。

(arg_regex)=
### arg_regex

指令解析器非常通用，不需要空格來結束指令名稱。這意味著別名 `:` 到 `emote` 可以像 `:smiles` 一樣使用，無需修改。這也意味著`getstone`會給你石頭（除非有一個專門命名為`getstone`的指令，那麼就會使用它）。如果您想告訴解析器在指令名稱與其引數之間需要特定的分隔符號（以便 `get stone` 有效，但 `getstone` 會給您一個「指令未找到」錯誤），您可以使用 `arg_regex` 屬性來實現。

`arg_regex` 是[原始正規表示式字串](https://docs.python.org/library/re.html)。正規表示式將由系統在執行時編譯。這允許您自訂指令名稱（或別名）*緊接*之後的部分必須如何顯示，以便解析器符合該指令。一些例子：

- `commandname argument` (`arg_regex = r"\s.+"`)：這會強制解析器要求指令名稱後面接著一個或多個空格。空格後輸入的任何內容都將被視為引數。但是，如果您忘記了空格（例如沒有引數的指令），則這將 *不* 匹配 `commandname`。
- `commandname` 或 `commandname argument` (`arg_regex = r"\s.+|$"`)：這使得 `look` 和 `look me` 都起作用，但 `lookme` 不起作用。
- `commandname/switches arguments` (`arg_regex = r"(?:^(?:\s+|\/).*$)|^$"`。如果您正在使用 Evennia 的 `MuxCommand` 指令父級，您可能想要使用它，因為它允許 `/switche`s 工作以及有或沒有空格。

`arg_regex` 允許您自訂指令的行為。您可以將其放在指令的父類別中以自訂指令的所有子級。但是，您也可以透過修改 `settings.COMMAND_DEFAULT_ARG_REGEX` 來變更所有指令的基本預設行為。

(exiting-a-command)=
## 退出指令

通常，您只需在 Command 類別的掛鉤方法之一中使用 `return` 即可退出該方法。然而，這仍然會按順序觸發指令的其他鉤子方法。這通常是您想要的，但有時中止指令可能會很有用，例如，如果您在解析方法中發現一些不可接受的輸入。要以這種方式退出指令，您可以提高 `evennia.InterruptCommand`：

```python
from evennia import InterruptCommand

class MyCommand(Command):

   # ...

   def parse(self):
       # ...
       # if this fires, `func()` and `at_post_cmd` will not
       # be called at all
       raise InterruptCommand()

```

(pauses-in-commands)=
## 指令中的暫停

有時您想在繼續執行指令之前暫停一會兒 - 也許您想模擬需要一些時間才能完成的劇烈擺動，也許您希望聲音的迴聲以更長的延遲返回給您。由於 Evennia 是非同步執行的，因此您不能在指令中（或任何地方，實際上）使用 `time.sleep()`。  如果你這樣做，*整個遊戲*將會
為大家凍結！所以不要這樣做。幸運的是，Evennia 提供了一個非常快速的語法
在指令中暫停。

在您的 `func()` 方法中，您可以使用 `yield` 關鍵字。  這是一個會凍結的Python關鍵字
指令的當前執行並在處理之前等待更多。

> 請注意，您*不能*只是將 `yield` 放入任何程式碼中並期望它暫停。只有當您在指令的 `func()` 方法中執行 `yield` 時，Evennia 才會為您暫停。不要指望它在其他地方也能工作。

以下是在訊息之間使用五秒小停頓的指令範例：

```python
from evennia import Command

class CmdWait(Command):
    """
    A dummy command to show how to wait

    Usage:
      wait

    """

    key = "wait"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """Command execution."""
        self.msg("Beginner-Tutorial to wait ...")
        yield 5
        self.msg("... This shows after 5 seconds. Waiting ...")
        yield 2
        self.msg("... And now another 2 seconds have passed.")
```

重要的行是 `yield 5` 和 `yield 2` 行。它將告訴 Evennia 在此處暫停執行，直到給定的秒數過去後才繼續執行。

在指令的 `func` 方法中使用 `yield` 時需要記住兩件事：

1. `yield` 產生的暫停狀態不會儲存在任何地方。因此，如果伺服器在指令暫停期間重新載入，那麼當伺服器恢復時它將*不會*恢復 - 指令的其餘部分將永遠不會觸發。因此請小心，不要以在重新載入時不會被清除的方式凍結角色或帳戶。
2. 如果您使用 `yield`，則您不能在 `func` 方法中同時使用 `return <values>`。你會得到一個錯誤來解釋這一點。這是由 Python 生成器的工作方式決定的。但是，您可以使用「裸」`return` 就可以了。通常不需要 `func` 回傳值，但如果您確實需要將 `yield` 與最終回傳值混合在同一個 `func` 中，請檢視 [twisted.internet.defer.returnValue](https://twistedmatrix.com/documents/current/api/twisted.internet.defer.html#returnValue)。

(asking-for-user-input)=
## 請求使用者輸入

`yield` 關鍵字也可用於請求使用者輸入。  同樣，您不能在指令中使用 Python 的 `input`，因為在等待使用者輸入文字時，它會凍結每個人的 Evennia。在指令的 `func` 方法中，也可以使用下列語法：

```python
answer = yield("Your question")
```

這是一個非常簡單的例子：

```python
class CmdConfirm(Command):

    """
    A dummy command to show confirmation.

    Usage:
        confirm

    """

    key = "confirm"

    def func(self):
        answer = yield("Are you sure you want to go on?")
        if answer.strip().lower() in ("yes", "y"):
            self.msg("Yes!")
        else:
            self.msg("No!")
```

這次，當使用者輸入「確認」指令時，系統會詢問她是否要繼續。輸入“yes”或“y”（無論大小寫）將給出第一個回覆，否則將顯示第二個回覆。

> 再次注意，`yield` 關鍵字不儲存狀態。  如果遊戲在等待使用者回答時重新載入，則使用者將不得不重新開始。對於重要或複雜的選擇使用 `yield` 不是一個好主意，在這種情況下，持久的 [EvMenu](./EvMenu.md) 可能更合適。

(system-commands)=
## 系統指令

*注意：這是一個高階主題。如果這是您第一次學習指令，請跳過它。 *

在伺服器看來，有幾種特殊的指令情況。如果帳戶輸入空字串會發生什麼？如果給出的「指令」實際上是使用者想要向其傳送訊息的頻道的名稱怎麼辦？或者是否有多個指令的可能性？

這種「特殊情況」由所謂的「系統指令」處理。  系統指令的定義方式與其他指令相同，只是其名稱（鍵）必須設定為引擎保留的名稱（名稱定義在`evennia/commands/cmdhandler.py`頂端）。您可以在 `evennia/commands/default/system_commands.py` 中找到系統指令的（未使用的）實作。由於這些（預設）不包含在任何 `CmdSet` 中，因此它們實際上並未使用，因此它們只是用於展示。當特殊情況發生時，Evennia 將尋找所有有效的 `CmdSet`s 來尋找您的自訂系統指令。只有在那之後，它才會訴諸自己的硬編碼實現。

以下是觸發系統指令的異常情況。您可以在 `evennia.syscmdkeys` 上找到它們用作屬性的指令鍵：

- 無輸入 (`syscmdkeys.CMD_NOINPUT`) - 帳戶只是按了回車鍵而沒有任何輸入。預設不執行任何操作，但對於某些實作（例如將非指令解釋為文字輸入（編輯緩衝區中的空白行）的行編輯器），在此處執行某些操作可能很有用。
- 未找到指令 (`syscmdkeys.CMD_NOMATCH`) - 未找到符合的指令。預設是顯示“嗯？”錯誤訊息。
- 找到多個符合指令 (`syscmdkeys.CMD_MULTIMATCH`) - 預設顯示符合清單。
- 不允許使用者執行該指令 (`syscmdkeys.CMD_NOPERM`) - 預設顯示“Huh？”錯誤訊息。
- 頻道 (`syscmdkeys.CMD_CHANNEL`) - 這是您正在訂閱的頻道的 [頻道](./Channels.md) 名稱 - 預設是將指令的引數中繼到該頻道。此類指令由通訊系統根據您的訂閱動態建立。
- 新session連線(`syscmdkeys.CMD_LOGINSTART`)。這個指令名應該放在`settings.CMDSET_UNLOGGEDIN`中。每當建立新連線時，總是在伺服器上呼叫此指令（預設是顯示登入畫面）。

以下是重新定義當帳戶不提供任何輸入（e.g。只需按回車鍵）時會發生什麼情況的範例。當然，新的系統指令也必須加入 cmdset 才能運作。

```python
    from evennia import syscmdkeys, Command

    class MyNoInputCommand(Command):
        "Usage: Just press return, I dare you"
        key = syscmdkeys.CMD_NOINPUT
        def func(self):
            self.caller.msg("Don't just press return like that, talk to me!")
```

(dynamic-commands)=
## 動態指令

*注意：這是一個高階主題。 *

通常指令被建立為固定類別並且無需修改即可使用。然而，在某些情況下，不可能（或不切實際）預先編碼確切的金鑰、別名或其他屬性。

若要建立具有動態呼叫簽署的指令，首先通常在類別中定義指令主體（將 `key`、`aliases` 設為預設值），然後使用下列呼叫（假設您建立的指令類別名稱為 `MyCommand`）：

```python
     cmd = MyCommand(key="newname",
                     aliases=["test", "test2"],
                     locks="cmd:all()",
                     ...)
```

您提供給 Command 建構函式的*所有* 關鍵字引數都會作為屬性儲存在指令物件上。這將過載父類別中定義的現有屬性。

通常，您會定義您的類，並且僅在執行時過載 `key` 和 `aliases` 之類的內容。但原則上您也可以將方法物件（如 `func`）作為關鍵字引數傳送，以使您的指令在執行時完全自訂。

(dynamic-commands-exits)=
### 動態指令 - 退出

退出是使用[動態指令](./Commands.md#dynamic-commands) 的範例。

Evennia 中的 [Exit](./Objects.md) 物件的功能未在引擎中硬編碼。相反，退出是正常的[型別分類](./Typeclasses.md)物件，它們在載入時自動建立[CmdSet](./Command-Sets.md)。該 cmdset 有一個動態建立的 Command，其屬性（鍵、別名和鎖定）與 Exit 物件本身相同。當輸入出口名稱時，會觸發此動態出口指令並（在訪問檢查後）將角色移至出口的目的地。

雖然您可以自訂 Exit 物件及其指令來實現完全不同的行為，但通常只需在 Exit 物件上使用適當的 `traverse_*` 掛鉤即可。但如果您有興趣真正改變底層的工作方式，請檢視 `evennia/objects/objects.py` 以瞭解 `Exit` typeclass 的設定方式。

(command-instances-are-re-used)=
## 指令例項被重用

*注意：這是一個高階主題，首次學習指令時可以跳過。 *

位於物件上的 Command 類別被例項化一次，然後重新使用。因此，如果您一遍又一遍地從 object1 執行指令，您實際上會一遍又一遍地執行相同的指令例項（如果您執行相同的指令但坐在 object2 上，它將是一個不同的例項）。您通常不會注意到這一點，因為每次使用指令例項時，其上的所有相關屬性都會被覆寫。但是有了這些知識，您就可以實現一些更奇特的指令機制，例如具有您上次輸入內容的“記憶”的指令，以便您可以反向引用先前的引數等。

> 注意：伺服器重新載入時，所有指令都會重建，記憶體也會被重新整理。

為了在實踐中展示這一點，請考慮以下指令：

```python
class CmdTestID(Command):
    key = "testid"

    def func(self):

        if not hasattr(self, "xval"):
            self.xval = 0
        self.xval += 1

        self.caller.msg(f"Command memory ID: {id(self)} (xval={self.xval})")

```

將其新增到預設角色 cmdset 會在遊戲中得到以下結果：

```
> testid
Command memory ID: 140313967648552 (xval=1)
> testid
Command memory ID: 140313967648552 (xval=2)
> testid
Command memory ID: 140313967648552 (xval=3)
```

請注意 `testid` 指令的記憶體位址永遠不會改變，但 `xval` 會不斷上升。

(create-a-command-on-the-fly)=
## 即時建立指令

*這也是一個高階主題。 *

還可以動態建立指令並將其新增至 cmdset。使用關鍵字引數建立類別例項，將該關鍵字引數指派為該特定指令的屬性：

```
class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):

        self.add(MyCommand(myvar=1, foo="test")

```

這將啟動 `MyCommand`，並將 `myvar` 和 `foo` 設定為屬性（可透過 `self.myvar` 和 `self.foo` 存取）。如何使用它們取決於司令部。但請記住上一節的討論 - 由於指令例項被重複使用，只要 cmdset 及其所在的物件位於記憶體中（i.e。直到下一次重新載入），這些屬性將「保留」在指令上。除非 `myvar` 和 `foo` 在指令執行時以某種方式重置，否則可以修改它們，並且將記住該變更以供後續使用該指令。

(how-commands-actually-work)=
## 指令實際上是如何工作的

*注意：這是一個高階主題，主要是伺服器開發人員感興趣的。 *

每當使用者將文字傳送到 Evennia 時，伺服器都會嘗試確定輸入的文字是否為
對應已知指令。這是指令處理程式序列尋找登入使用者的方式：

1. 使用者輸入一串文字並按 Enter 鍵。
2. 使用者的 Session 確定文字不是某些協定特定的控制序列或 OOB 指令，但將其傳送到指令處理程式。
3. Evennia 的*指令處理程式* 分析 Session 並取得對帳戶和最終傀儡角色的最終引用（這些將稍後儲存在指令物件上）。 *caller* 屬性已適當設定。
4. 如果輸入為空字串，則將指令重新傳送為 `CMD_NOINPUT`。如果在cmdset中沒有找到這樣的指令，則忽略。
5. 如果 command.key 與 `settings.IDLE_COMMAND` 匹配，則更新計時器，但不再執行任何操作。
6. 指令處理程式此時收集*呼叫者*可用的CmdSets：
    - 呼叫者自己的目前活動CmdSet。
    - 如果呼叫者是傀儡物件，則在目前帳戶上定義 CmdSets。
    - CmdSets 在 Session 本身上定義。
    - 同一位置中活動的 CmdSets 最終物件（如果有）。這包括[退出](./Objects.md#exits) 上的指令。
    - 代表可用[通訊]的動態建立的*系統指令*集(./Channels.md)
7. 所有CmdSets*相同優先順序*都合併到群組中。  分組避免了將多個相同優先集合併到較低優先集上的與順序相關的問題。
8. 根據每一組的合併規則，所有分組的 CmdSets 以相反的優先順序「合併」為一個組合的 CmdSet。
9. Evennia 的 *指令解析器* 採用合併的 cmdset 並將其每個指令（使用其鍵和別名）與 *呼叫者 * 輸入的字串的開頭進行匹配。這會產生一組候選者。
10. *cmd 解析器* 接下來根據匹配的字元數量以及與相應已知指令的匹配百分比來對匹配進行評級。只有當候選者無法分開時，才會傳回多個匹配項。
    - 如果傳回多個符合項，則重新傳送為 `CMD_MULTIMATCH`。如果在 cmdset 中沒有找到這樣的指令，則傳回硬編碼的符合清單。
    - 如果未找到匹配項，則重新傳送為 `CMD_NOMATCH`。如果在 cmdset 中沒有找到這樣的指令，則給出硬編碼的錯誤訊息。
11. 如果解析器找到單一指令，則會從儲存體中取出正確的指令物件。這通常並不意味著重新初始化。
12. 透過驗證指令的 *lockstring* 來檢查呼叫者是否確實有權存取該指令。如果不是，則不認為是合適的匹配，並觸發 `CMD_NOMATCH`。
13. 如果新指令被標記為通道指令，則重新傳送為 `CMD_CHANNEL`。如果在cmdset中沒有找到這樣的指令，則使用硬編碼實作。
14. 為指令例項指派幾個有用的變數（請參閱前面的部分）。
15. 在指令例項上呼叫 `at_pre_command()`。
16. 在指令例項上呼叫 `parse()`。這是在指令名稱之後提供的字串的其餘部分。它的目的是將字串預先解析為對 `func()` 方法有用的形式。
17. 在指令例項上呼叫 `func()`。這是指令的功能體，實際上在做有用的事情。
18. 在指令例項上呼叫 `at_post_command()`。

(assorted-notes)=
## 什錦筆記

`Command.func()` 的回傳值是 Twisted [deferred](https://twistedmatrix.com/documents/current/core/howto/defer.html)。
Evennia 預設完全不使用此回傳值。如果你這樣做，你必須
因此，使用回撥非同步執行此操作。

```python
     # in command class func()
     def callback(ret, caller):
        caller.msg(f"Returned is {ret}")
     deferred = self.execute_command("longrunning")
     deferred.addCallback(callback, self.caller)
```

除了最先進/奇怪的設計之外，這可能與任何其他設計都不相關（例如，可以使用它來建立“巢狀”指令結構）。

`save_for_next` 類別變數可用於實作狀態持久指令。例如，它可以使指令對“it”進行操作，其中它由前一個指令所操作的內容決定。
