(evennia-for-roleplaying-sessions)=
# Evennia 用於角色扮演 sessions

本教學將說明如何使用
新鮮Evennia伺服器。

場景是這樣的：你和一群朋友想玩線上桌上角色扮演遊戲。
你們中的一位將成為遊戲大師，你們都可以使用書寫文字進行遊戲。你想要
即時角色扮演的能力（當人們碰巧同時線上時）
以及人們能夠在可能的情況下發布並瞭解自發布以來發生的事情的能力
最後線上。

這是我們需要和使用的功能：

* 使你們中的一個人成為*GM*（遊戲大師）的能力，具有特殊能力。
* 玩家可以建立、檢視和填寫的*角色表*。它也可以被鎖定，這樣只有
GM可以修改。
* *骰子滾輪*機制，適用於 RPG 規則所需的任何型別的骰子。
* *房間*，提供位置感並劃分正在進行的遊戲 - 這意味著兩者
角色從一個位置移動到另一個位置，並且GM明確地移動它們。
* *頻道*，用於輕鬆向所有訂閱帳戶傳送文字，無論其位置如何。
* 帳戶到帳戶*訊息傳送*功能，包括傳送給多個收件者
同時，無論位置如何。

我們會發現其中大部分內容已經是原版Evennia的一部分，但我們可以對其進行擴充套件
我們特定用例的預設值。下面我們將從頭到尾充實這些元件。

(starting-out)=
## 開始

我們假設您從頭開始。您需要安裝 Evennia，依照[安裝快速入門](../Setup/Installation.md)
說明操作。使用 `evennia init <gamedirname>` 初始化一個新的遊戲目錄。在本教學中，我們假設您的遊戲目錄就叫做 `mygame`。目前可以使用預設資料庫，其他設定也先保持預設值。熟悉一下
`mygame` 資料夾，然後再繼續。您也可以先瀏覽[初學者教學](Beginner-Tutorial/Part1/Beginner-Tutorial-Part1-Overview.md)，大致看看哪些地方會被修改。

(the-game-master-role)=
## 遊戲大師角色

簡而言之：

* 最簡單的方法：身為管理員，只需使用標準 `perm` 指令授予一個帳戶 `Admins` 許可權。
* 更好但更多的工作：建立自訂指令來設定/取消設定上述內容，同時調整角色以向其他帳戶顯示您更新的 GM 狀態。

(the-permission-hierarchy)=
### 許可權層次結構

Evennia 具有以下開箱即用的[許可權層次結構](../Components/Permissions.md)：*玩家、助手、建構者、管理者*，最後是*開發者*。我們可以更改這些，但隨後我們需要更新預設指令才能使用更改。我們希望保持簡單，因此我們將不同的角色對應到這個許可權階梯之上。

1. `Players`是給普通玩家設定的許可權。這是任何建立新專案的人的預設設定
伺服器上的帳戶。
2. `Helpers` 與 `Players` 類似，只不過它們也能夠建立/編輯新的幫助條目。
這可以授予願意幫助編寫傳說或自訂日誌的玩家
大家。
3. 在我們的例子中沒有使用`Builders`，因為GM應該是唯一的世界建構者。
4. `Admins` 是 GM 應具有的許可權等級。管理員可以做建構者可以做的一切
（建立/描述房間等）還可以踢帳戶，重新命名它們等等。
5. `Developers`級許可權是伺服器管理員，有能力
重新啟動/關閉伺服器以及變更許可權等級。

> _superuser_ 不是層次結構的一部分，實際上完全繞過了它。我們假設伺服器管理員“只是”開發人員。

(how-to-grant-permissions)=
### 如何授予許可權

只有 `Developers` 可以（預設）更改許可權等級。只有他們有權訪問 `@perm`
指令：

```
> perm Yvonne
Permissions on Yvonne: accounts

> perm Yvonne = Admins
> perm Yvonne
Permissions on Yvonne: accounts, admins

> perm/del Yvonne = Admins
> perm Yvonne
Permissions on Yvonne: accounts
```

新增更高許可權時無需刪除基本`Players`許可權：
將使用最高的。許可權等級名稱*不*區分大小寫。您也可以同時使用複數
並且是單數，因此“Admins”具有與“Admin”相同的權力。


(optional-making-a-gm-granting-command)=
### 可選：建立GM-授予指令

`perm` 的使用是開箱即用的，但這實際上是最低限度的。如果是其他的豈不是很好
帳戶一眼就能看出GM是誰？另外，我們真的不需要記住
許可權級別稱為“管理員”。如果我們可以只做 `@gm <account>` 並且會更容易
`@notgm <account>` 並同時更改某些內容，使新的 GM 狀態變得明顯。

讓我們讓這一切成為可能。這就是我們要做的：

1. 我們將自訂預設的字元類別。如果此類的物件具有特定標誌，
它的名稱將在末尾新增字串`(GM)`。
2. 我們將新增一個指令，以便伺服器管理員正確分配 GM- 標誌。

(character-modification)=
#### 人物修改

讓我們先從自訂角色開始。我們建議您瀏覽開頭部分
[帳戶](../Components/Accounts.md) 頁面，以確保您瞭解 Evennia 如何區分 OOC「帳戶
物件」（不要與 `Accounts` 許可權混淆，後者只是一個指定您的字串
訪問）和IC“字元物件”。

開啟`mygame/typeclasses/characters.py`並修改預設的`Character`類：

```python
# in mygame/typeclasses/characters.py

# [...]

class Character(DefaultCharacter):
    # [...]
    def get_display_name(self, looker, **kwargs):
        """
        This method customizes how character names are displayed. We assume
        only permissions of types "Developers" and "Admins" require
        special attention.
        """
        name = self.key
        selfaccount = self.account     # will be None if we are not puppeted
        lookaccount = looker.account   #              - " -

        if selfaccount and selfaccount.db.is_gm:
           # A GM. Show name as name(GM)
           name = f"{name}(GM)"

        if lookaccount and \
          (lookaccount.permissions.get("Developers") or lookaccount.db.is_gm):
            # Developers/GMs see name(#dbref) or name(GM)(#dbref)
            name = f"{name}(#{self.id})"

        return name
```

上面，我們更改了角色名稱的顯示方式：如果控制該角色的帳戶是
a GM，我們將字串`(GM)`附加到角色的名字上，這樣每個人都可以知道誰是老闆。如果我們
我們自己是開發人員或GM，我們將看到資料庫 ID 附加到角色名稱，這可以
如果對完全相同名稱的字元進行資料庫搜尋，會有所幫助。我們以「gm-
ingness”，具有名為 `is_gm` 的標誌（[Attribute](../Components/Attributes.md)）。我們將確保新的GM
實際上得到下面這個標誌。

> **額外練習：** 這只會顯示由 GM 帳戶操縱的*字元*上的 `(GM)` 文字，
也就是說，它只會顯示給位於相同位置的人。如果我們希望它也彈出，比如說，
`who` 清單和頻道，我們需要對 `Account` typeclass 進行類似的更改
`mygame/typeclasses/accounts.py`。我們將其作為練習留給讀者。

(new-gmungm-command)=
#### 新@gm/@ungm指令

我們將在這裡詳細描述如何建立和新增 Evennia [指令](../Components/Commands.md)
希望以後加上指令的時候不需要那麼詳細。我們將在此基礎上
Evennia 的預設“mux-like”指令在這裡。

開啟`mygame/commands/command.py`並在底部新增一個新的Command類別：

```python
# in mygame/commands/command.py

from evennia import default_cmds

# [...]

import evennia

class CmdMakeGM(default_cmds.MuxCommand):
    """
    Change an account's GM status

    Usage:
      @gm <account>
      @ungm <account>

    """
    # note using the key without @ means both @gm !gm etc will work
    key = "gm"
    aliases = "ungm"
    locks = "cmd:perm(Developers)"
    help_category = "RP"

    def func(self):
        "Implement the command"
        caller = self.caller

        if not self.args:
            caller.msg("Usage: @gm account or @ungm account")
            return

        accountlist = evennia.search_account(self.args) # returns a list
        if not accountlist:
            caller.msg(f"Could not find account '{self.args}'")
            return
        elif len(accountlist) > 1:
            caller.msg(f"Multiple matches for '{self.args}': {accountlist}")
            return
        else:
            account = accountlist[0]

        if self.cmdstring == "gm":
            # turn someone into a GM
            if account.permissions.get("Admins"):
                caller.msg(f"Account {account} is already a GM.")
            else:
                account.permissions.add("Admins")
                caller.msg(f"Account {account} is now a GM.")
                account.msg(f"You are now a GM (changed by {caller}).")
                account.character.db.is_gm = True
        else:
            # @ungm was entered - revoke GM status from someone
            if not account.permissions.get("Admins"):
                caller.msg(f"Account {account} is not a GM.")
            else:
                account.permissions.remove("Admins")
                caller.msg(f"Account {account} is no longer a GM.")
                account.msg(f"You are no longer a GM (changed by {caller}).")
                del account.character.db.is_gm

```

該指令所做的只是找到帳戶目標並為其分配 `Admins` 許可權（如果我們
使用 `gm` 或撤銷它（如果使用 `ungm` 別名）。我們也設定/取消設定 `is_gm` Attribute 即
我們之前的新 `Character.get_display_name` 方法預期如此。

> 我們可以將其分成兩個單獨的指令，或者選擇像 `gm/revoke <accountname>` 這樣的語法。相反，我們檢查該指令是如何呼叫的（儲存在 `self.cmdstring` 中）以便採取相應的行動。無論哪種方式都有效，實用性和程式設計風格決定採用哪種方式。

為了真正使該指令可用（僅對開發人員可用，因為其上有 lock），我們將其新增至預設帳戶指令集中。開啟檔案`mygame/commands/default_cmdsets.py`並找到`AccountCmdSet`類：

```python
# mygame/commands/default_cmdsets.py

# [...]
from commands.command import CmdMakeGM

class AccountCmdSet(default_cmds.AccountCmdSet):
    # [...]
    def at_cmdset_creation(self):
        # [...]
        self.add(CmdMakeGM())

```

最後，發出 `reload` 指令將伺服器更新為您的變更。開發者級玩家
（或超級使用者）現在應該可以使用 `gm/ungm` 指令。

(character-sheet)=
## 字元表

簡而言之：

* 使用Evennia的EvTable/EvForm建立角色表
* 將單獨的紙張綁在給定的角色上。
* 新增指令以透過帳戶和 GM 修改角色表。
* 讓角色表可鎖定GM，讓玩家無法再修改它。

(building-a-character-sheet)=
### 建構角色表

在文字中建立字元表的方法有很多，從手動將字串貼到一起到更自動化的方法。到底什麼是最好/最簡單的方法取決於人們試圖建立的工作表。我們將在這裡展示兩個使用 *EvTable* 和 *EvForm* 實用程式的範例。稍後我們將建立指令來編輯和顯示這些實用程式的輸出。

> 請注意，這些檔案不顯示顏色。  有關如何向表格和表單新增顏色的資訊，請參閱[文字tag 檔案](../Concepts/Tags-Parsed-By-Evennia.md)。

(making-a-sheet-with-evtable)=
#### 用 EvTable 製作一張紙

[EvTable](../Components/EvTable.md) 是一個文字表產生器。它有助於以有序的行和列顯示文字。這是在程式碼中使用它的範例：

````python
# this can be tried out in a Python shell like iPython

from evennia.utils import evtable

# we hardcode these for now, we'll get them as input later
STR, CON, DEX, INT, WIS, CHA = 12, 13, 8, 10, 9, 13

table = evtable.EvTable("Attr", "Value",
                        table = [
                           ["STR", "CON", "DEX", "INT", "WIS", "CHA"],
                           [STR, CON, DEX, INT, WIS, CHA]
                        ], align='r', border="incols")
````

上面，我們透過直接提供兩列來建立一個兩個清單。我們還告訴表格右對齊並使用“incols”邊框型別（僅在列之間繪製邊框）。 `EvTable` 類別需要很多引數來自訂其外觀，您可以在此處檢視[一些可能的關鍵字引數](github:evennia.utils.evtable#evtable__init__)。一旦您擁有`table`，您還可以使用`table.add_row()` 和`table.add_column()` 追溯新增新的列和行：如有必要，表格將用空行/列擴充套件以始終保持矩形。

列印上表的結果將是

```python
table_string = str(table)

print(table_string)

 Attr | Value
~~~~~~+~~~~~~~
  STR |    12
  CON |    13
  DEX |     8
  INT |    10
  WIS |     9
  CHA |    13
```

這是一個簡約但有效的角色表。透過將 `table_string` 與其他組合
字串可以建構一個字元的相當完整的圖形表示。瞭解更多
接下來我們將研究 EvForm 的高階佈局。

(making-a-sheet-with-evform)=
#### 用 EvForm 製作一張紙

[EvForm](../Components/EvForm.md) 允許建立由文字字元組成的二維「圖形」。在此表面上，一個標記和 tags 矩形區域（「單元格」）將被填滿內容。此內容可以是普通字串或 `EvTable` 例項（請參閱上一節，其中一個例項是該範例中的 `table` 變數）。

在字元表的情況下，這些儲存格相當於一行或一個框，您可以在其中
輸入你的角色的名字或他們的力量分數。 EvMenu 還可以輕鬆地允許更新
程式碼中這些欄位的內容（它使用EvTables，因此您在重新傳送之前先重建表
至EvForm）。

EvForm的缺點是它的形狀是靜態的；如果您嘗試在某個區域中放置比該區域更多的文字
調整大小後，文字將被裁剪。同樣，如果您嘗試將 EvTable 例項放入欄位中
對於它來說太小了，EvTable 將盡力嘗試調整大小以適應，但最終會採取
裁剪其資料，如果太小而無法容納任何資料，甚至會給出錯誤。

Python 模組中定義了 EvForm。建立一個新檔案 `mygame/world/charsheetform.py` 並
修改如下：

````python
#coding=utf-8

# in mygame/world/charsheetform.py

FORMCHAR = "x"
TABLECHAR = "c"

FORM = """
.--------------------------------------.
|                                      |
| Name: xxxxxxxxxxxxxx1xxxxxxxxxxxxxxx |
|       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
|                                      |
 >------------------------------------<
|                                      |
| ccccccccccc  Advantages:             |
| ccccccccccc   xxxxxxxxxxxxxxxxxxxxxx |
| ccccccccccc   xxxxxxxxxx3xxxxxxxxxxx |
| ccccccccccc   xxxxxxxxxxxxxxxxxxxxxx |
| ccccc2ccccc  Disadvantages:          |
| ccccccccccc   xxxxxxxxxxxxxxxxxxxxxx |
| ccccccccccc   xxxxxxxxxx4xxxxxxxxxxx |
| ccccccccccc   xxxxxxxxxxxxxxxxxxxxxx |
|                                      |
+--------------------------------------+
"""
````
`#coding` 語句（必須放在第一行才能運作）告訴 Python 使用
檔案的 utf-8 編碼。使用 `FORMCHAR` 和 `TABLECHAR` 我們定義我們要做什麼的單字元
想要用來「標記」分別包含儲存格和表格的字元表區域。
在每個區塊（必須至少用一個非標記字元彼此分隔）內，我們嵌入識別符號 1-4 來標識每個區塊。識別符號可以是除 `FORMCHAR` 和 `TABLECHAR` 之外的任何單個字元

> 您仍然可以在工作表的其他位置使用 `FORMCHAR` 和 `TABLECHAR`，但不能以識別儲存格/表格的方式使用。最小的可識別儲存格/表格區域為 3 個字元寬，包括識別符（例如 `x2x`）。

現在我們將把內容對應到這個表單。

````python
# again, this can be tested in a Python shell

# hard-code this info here, later we'll ask the
# account for this info. We will re-use the 'table'
# variable from the EvTable example.

NAME = "John, the wise old admin with a chip on his shoulder"
ADVANTAGES = "Language-wiz, Intimidation, Firebreathing"
DISADVANTAGES = "Bad body odor, Poor eyesight, Troubled history"

from evennia.utils import evform

# load the form from the module
form = evform.EvForm("world/charsheetform.py")

# map the data to the form
form.map(cells={"1":NAME, "3": ADVANTAGES, "4": DISADVANTAGES},
         tables={"2":table})
````

我們建立一些 RP- 聲音輸入並重新使用先前 `EvTable` 中的 `table` 變數
範例。

> 請注意，如果您不想在單獨的模組中建立表單，您*也可以*將其直接載入到 `EvForm` 呼叫中，如下所示：`EvForm(form={"FORMCHAR":"x", "TABLECHAR":"c", "FORM": formstring})` 其中 `FORM` 以與上面模組中列出的相同方式將表單指定為字串。但請注意，`FORM` 字串的第一行將被忽略，因此以 `\n` 開頭。

然後我們將它們對映到表單的單元格：

````python
print(form)
````
````
.--------------------------------------.
|                                      |
| Name: John, the wise old admin with |
|        a chip on his shoulder        |
|                                      |
 >------------------------------------<
|                                      |
|  Attr|Value  Advantages:             |
| ~~~~~+~~~~~   Language-wiz,          |
|   STR|   12   Intimidation,          |
|   CON|   13   Firebreathing          |
|   DEX|    8  Disadvantages:          |
|   INT|   10   Bad body odor, Poor    |
|   WIS|    9   eyesight, Troubled     |
|   CHA|   13   history                |
|                                      |
+--------------------------------------+
````

如圖所示，文字和表格已放入文字區域，並在需要的地方新增了換行符。我們選擇在此處僅以純字串形式輸入優點/缺點，這意味著長名稱最終會在行之間分割。如果我們想要對顯示進行更多控制，我們可以在每行後面插入 `\n` 換行符，或者使用無邊框 `EvTable` 來顯示這些內容。

(tie-a-character-sheet-to-a-character)=
### 將角色表與角色繫結

我們假設我們採用上面的 `EvForm` 範例。我們現在需要將其附加到角色上，以便可以對其進行修改。為此，我們將稍微修改一下 `Character` 類別：

```python
# mygame/typeclasses/character.py

from evennia.utils import evform, evtable

[...]

class Character(DefaultCharacter):
    [...]
    def at_object_creation(self):
        "called only once, when object is first created"
        # we will use this to stop account from changing sheet
        self.db.sheet_locked = False
        # we store these so we can build these on demand
        self.db.chardata  = {"str": 0,
                             "con": 0,
                             "dex": 0,
                             "int": 0,
                             "wis": 0,
                             "cha": 0,
                             "advantages": "",
                             "disadvantages": ""}
        self.db.charsheet = evform.EvForm("world/charsheetform.py")
        self.update_charsheet()

    def update_charsheet(self):
        """
        Call this to update the sheet after any of the ingoing data
        has changed.
        """
        data = self.db.chardata
        table = evtable.EvTable("Attr", "Value",
                        table = [
                           ["STR", "CON", "DEX", "INT", "WIS", "CHA"],
                           [data["str"], data["con"], data["dex"],
                            data["int"], data["wis"], data["cha"]]],
                           align='r', border="incols")
        self.db.charsheet.map(tables={"2": table},
                              cells={"1":self.key,
                                     "3":data["advantages"],
                                     "4":data["disadvantages"]})

```

使用 `reload` 使此變更適用於所有*新建立的*角色。 *已經存在*
字元將「不」定義字元表，因為 `at_object_creation` 只被呼叫一次。
強制現有角色重新發射其 `at_object_creation` 最簡單的方法是使用
`typeclass` 遊戲中指令：

```
typeclass/force <Character Name>
```

(command-for-account-to-change-character-sheet)=
### 帳戶更改字元表的指令

我們將新增一個指令來編輯角色表的各個部分。開啟
`mygame/commands/command.py`。

```python
# at the end of mygame/commands/command.py

ALLOWED_ATTRS = ("str", "con", "dex", "int", "wis", "cha")
ALLOWED_FIELDNAMES = ALLOWED_ATTRS + \
                     ("name", "advantages", "disadvantages")

def _validate_fieldname(caller, fieldname):
    "Helper function to validate field names."
    if fieldname not in ALLOWED_FIELDNAMES:
        list_of_fieldnames = ", ".join(ALLOWED_FIELDNAMES)
        err = f"Allowed field names: {list_of_fieldnames}"
        caller.msg(err)
        return False
    if fieldname in ALLOWED_ATTRS and not value.isdigit():
        caller.msg(f"{fieldname} must receive a number.")
        return False
    return True

class CmdSheet(MuxCommand):
    """
    Edit a field on the character sheet

    Usage:
      @sheet field value

    Examples:
      @sheet name Ulrik the Warrior
      @sheet dex 12
      @sheet advantages Super strength, Night vision

    If given without arguments, will view the current character sheet.

    Allowed field names are:
       name,
       str, con, dex, int, wis, cha,
       advantages, disadvantages

    """

    key = "sheet"
    aliases = "editsheet"
    locks = "cmd: perm(Players)"
    help_category = "RP"

    def func(self):
        caller = self.caller
        if not self.args or len(self.args) < 2:
            # not enough arguments. Display the sheet
            if sheet:
                caller.msg(caller.db.charsheet)
            else:
                caller.msg("You have no character sheet.")
            return

        # if caller.db.sheet_locked:
            caller.msg("Your character sheet is locked.")
            return

        # split input by whitespace, once
        fieldname, value = self.args.split(None, 1)
        fieldname = fieldname.lower() # ignore case

        if not _validate_fieldnames(caller, fieldname):
            return
        if fieldname == "name":
            self.key = value
        else:
            caller.chardata[fieldname] = value
        caller.update_charsheet()
        caller.msg(f"{fieldname} was set to {value}.")

```

該指令的大部分內容是錯誤檢查，以確保輸入的資料型別正確。請注意 `sheet_locked` Attribute 是如何檢查的，如果未設定，則會返回。

將此指令匯入至 `mygame/commands/default_cmdsets.py` 並新增至 `CharacterCmdSet`，與先前將 `@gm` 指令新增至 `AccountCmdSet` 的方式相同。

(commands-for-gm-to-change-character-sheet)=
### GM 更改字元表的指令

遊戲大師使用與玩家基本相同的輸入來編輯角色表，除了他們可以對自己以外的其他玩家進行編輯。它們也不會被任何 `sheet_locked` 標誌阻止。

```python
# continuing in mygame/commands/command.py

class CmdGMsheet(MuxCommand):
    """
    GM-modification of char sheets

    Usage:
      @gmsheet character [= fieldname value]

    Switches:
      lock - lock the character sheet so the account
             can no longer edit it (GM's still can)
      unlock - unlock character sheet for Account
             editing.

    Examples:
      @gmsheet Tom
      @gmsheet Anna = str 12
      @gmsheet/lock Tom

    """
    key = "gmsheet"
    locks = "cmd: perm(Admins)"
    help_category = "RP"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Usage: @gmsheet character [= fieldname value]")

        if self.rhs:
            # rhs (right-hand-side) is set only if a '='
            # was given.
            if len(self.rhs) < 2:
                caller.msg("You must specify both a fieldname and value.")
                return
            fieldname, value = self.rhs.split(None, 1)
            fieldname = fieldname.lower()
            if not _validate_fieldname(caller, fieldname):
                return
            charname = self.lhs
        else:
            # no '=', so we must be aiming to look at a charsheet
            fieldname, value = None, None
            charname = self.args.strip()

        character = caller.search(charname, global_search=True)
        if not character:
            return

        if "lock" in self.switches:
            if character.db.sheet_locked:
                caller.msg("The character sheet is already locked.")
            else:
                character.db.sheet_locked = True
                caller.msg(f"{character.key} can no longer edit their character sheet.")
        elif "unlock" in self.switches:
            if not character.db.sheet_locked:
                caller.msg("The character sheet is already unlocked.")
            else:
                character.db.sheet_locked = False
                caller.msg(f"{character.key} can now edit their character sheet.")

        if fieldname:
            if fieldname == "name":
                character.key = value
            else:
                character.db.chardata[fieldname] = value
            character.update_charsheet()
            caller.msg(f"You set {character.key}'s {fieldname} to {value}.")
        else:
            # just display
            caller.msg(character.db.charsheet)
```

`gmsheet` 指令需要一個附加引數來指定要編輯哪個角色的字元表。它還需要 `/lock` 和 `/unlock` 開關來阻止玩家調整他們的表。

在使用之前，應以與正常 `sheet` 相同的方式將其新增至預設 `CharacterCmdSet` 中。由於設定了lock，該指令僅對`Admins`（i.e.GMs）或更高許可權等級可用。

(dice-roller)=
## 骰滾筒

Evennia 的 *contrib* 資料夾已附帶完整的骰子滾筒。要將其新增到遊戲中，只需將 `contrib.dice.CmdDice` 匯入 `mygame/commands/default_cmdsets.py` 並將 `CmdDice` 新增到 `CharacterCmdset` 中，就像本教學中的其他指令一樣。 `@reload`之後你將能夠
使用正常的 RPG- 樣式格式擲骰子：

```
roll 2d6 + 3
7
```

使用 `help dice` 檢視支援哪些語法，或檢視 `evennia/contrib/dice.py` 檢視其實作方式。

(rooms)=
## 客房

Evennia 附帶開箱即用的房間，因此不需要額外的工作。 GM 將自動提供所有需要的建置指令。在[建構教學](Beginner-Tutorial/Part1/Beginner-Tutorial-Building-Quickstart.md) 中可以找到更完整的詳細說明。
以下是一些有用的亮點：

* `dig roomname;alias = exit_there;alias, exit_back;alias` - 這是挖掘新房間的基本指令。您可以指定任何出口名稱，只需輸入該出口的名稱即可到達那裡。
* `tunnel direction = roomname` - 這是一個專門的指令，僅接受基本方向（n，ne，e，se，s，sw，w，nw）以及進/出和上/下方向。它還會自動在相反方向建立“匹配”出口。
* `create/drop objectname` - 這將在目前位置建立並刪除一個新的簡單物件。
* `desc obj` - 更改物件的外觀描述。
* `tel object = location` - 將物件傳送到指定位置。
* `search objectname` - 在資料庫中尋找物件。

> TODO：描述如何新增一個日誌記錄室，該日誌記錄並構成一個人們可以在事後存取的日誌檔案。

(channels)=
## 頻道

Evennia 內建[通道](../Components/Channels.md)，並且在檔案中對其進行了完整描述。為了簡潔起見，以下是正常使用的相關指令：

* `channel/create = new_channel;alias;alias = short description` - 建立一個新頻道。
* `channel/sub channel` - 訂閱頻道。
* `channel/unsub channel` - 取消訂閱頻道。
* `channels` 列出所有可用頻道，包括您的訂閱以及您為其設定的任何別名。

您可以讀取頻道歷史記錄：例如，如果您正在 `public` 頻道上聊天，您可以執行以下操作
`public/history` 檢視該頻道的最後 20 條帖子，或 `public/history 32` 檢視 20 條
從倒數第 32 篇文章開始向後倒數。

(pms)=
## 專案經理

要互相傳送私信，玩家可以使用`page`（或`tell`）指令：

```
page recipient = message
page recipient, recipient, ... = message
```

玩家可以單獨使用`page`檢視最新訊息。如果他們不線上，這也適用
訊息傳送時。
