(help-system)=
# 幫助系統


```shell
> help theatre
```

```shell
------------------------------------------------------------------------------
Help for The theatre (aliases: the hub, curtains)

The theatre is at the centre of the city, both literally and figuratively ...
(A lot more text about it follows ...)

Subtopics:
  theatre/lore
  theatre/layout
  theatre/dramatis personae
------------------------------------------------------------------------------
```

```shell
> help evennia
```

```shell
------------------------------------------------------------------------------
No help found

There is no help topic matching 'evennia'.
... But matches where found within the help texts of the suggestions below.

Suggestions:
  grapevine2chan, about, irc2chan
-----------------------------------------------------------------------------
```

Evennia 擁有廣泛的幫助系統，涵蓋指令幫助和常規自由格式幫助檔案。它支援子主題，如果找不到匹配項，它將首先從替代主題中提供建議，然後透過在幫助條目中查詢搜尋字詞的提及來提供建議。

在遊戲中使用 `help` 指令存取幫助系統：

    help <topic>

子主題以 `help <topic>/<subtopic>/...` 的形式存取。

(working-with-three-types-of-help-entries)=
## 使用三種型別的說明條目

產生幫助條目的方法有以下三種：

- 在資料庫中
- 作為 Python 模組
- 來自指令檔案字串

(database-stored-help-entries)=
### 資料庫儲存的幫助條目

從遊戲中建立新的幫助條目是透過

    sethelp <topic>[;aliases] [,category] [,lockstring] = <text>

例如

    sethelp The Gods;pantheon, Lore = In the beginning all was dark ...

這將在資料庫中建立一個新的幫助條目。使用 `/edit` 開關開啟 EvEditor 以便更方便地在遊戲中編寫（但請注意，開發人員也可以使用常規程式碼編輯器在遊戲外建立說明條目，請參見下文）。

[HelpEntry](evennia.help.models.HelpEntry) 儲存資料庫協助。它_不是_型別分類實體，並且不能使用 typeclass 機制進行擴充。

以下是如何在程式碼中建立資料庫幫助條目：
```python
from evennia import create_help_entry
entry = create_help_entry("emote",
                "Emoting is important because ...",
                category="Roleplaying", locks="view:all()")
```

(file-stored-help-entries)=
### 檔案儲存的說明條目

```{versionadded} 1.0
```

檔案幫助條目由遊戲開發團隊在遊戲之外建立。幫助條目在普通 Python 模組（`.py` 檔案結尾）中定義，包含 `dict` 來表示每個條目。在應用任何變更之前，它們需要伺服器 `reload`。

- Evennia 將檢視由以下給出的所有模組
`settings.FILE_HELP_ENTRY_MODULES`。這應該是 python 路徑列表
  Evennia 匯入。
- 如果該模組包含頂級變數`HELP_ENTRY_DICTS`，則這將是
已匯入，並且必須是 `list` 的幫助輸入字典。
- 如果沒有找到 `HELP_ENTRY_DICTS` 列表，則_every_中的頂級變數
`dict` 的模組將被讀取為幫助條目。變數名稱將
  在這種情況下可以忽略。

如果您新增多個要閱讀的模組，則稍後新增相同按鍵的說明條目
該列表將覆蓋先前的列表。

每個條目字典必須定義鍵以符合所有幫助條目所需的鍵。
這是幫助模組的範例：

```python

# in a module pointed to by settings.FILE_HELP_ENTRY_MODULES

HELP_ENTRY_DICTS = [
  {
    "key": "The Gods",   # case-insensitive, can be searched by 'gods' too
    "aliases": ['pantheon', 'religion']
    "category": "Lore",
    "locks": "read:all()",  # optional
    "text": '''
        The gods formed the world ...

        # Subtopics

        ## Pantheon

        The pantheon consists of 40 gods that ...

        ### God of love

        The most prominent god is ...

        ### God of war

        Also known as 'the angry god', this god is known to ...

    '''
  },
  {
    "key": "The mortals",

  }
]

```

幫助條目文字將減少縮排並保留段落。你應該嘗試
保持字串合理的寬度（看起來會更好）。只需重新載入
伺服器和基於檔案的幫助條目將可供檢視。

(command-help-entries)=
### 指令幫助條目

[指令類別](./Commands.md) 的 `__docstring__` 會自動擷取到說明條目中。您直接在類上設定`help_category`。

```python
from evennia import Command

class MyCommand(Command): 
    """ 
    This command is great! 

    Usage: 
      mycommand [argument]

    When this command is called, great things happen. If you 
    pass an argument, even GREATER things HAPPEN!

    """

    key = "mycommand"

    locks: "cmd:all();read:all()"   # default 
    help_category = "General"       # default
    auto_help = True                # default 

    # ...
```

當您更新程式碼時，指令的幫助將隨之而來。這個想法是，如果開發人員可以在編寫程式碼的同時更改指令文件，那麼指令文件就更容易維護並保持最新。

(locking-help-entries)=
### 鎖定幫助條目

預設`help`指令收集所有可用指令和說明條目
在一起，以便可以搜尋或列出它們。透過在指令/幫助上設定鎖定
條目可以限制誰可以閱讀有關它的幫助。

- 未透過正常 `cmd`-lock 的指令將在獲得之前被刪除
到幫助指令。在這種情況下，下面的其他兩個 lock 型別將被忽略。
- `view` 存取型別決定指令/幫助條目是否應在以下位置可見
主要幫助索引。如果沒有給出，則假設每個人都可以檢視。
- `read` 存取型別決定是否可以實際讀取指令/幫助條目。
如果給出了 `read` lock 而未給出 `view`，則假定 `read`-lock
  也適用於`view`-訪問（因此，如果您無法閱讀幫助條目，它將
  也沒有出現在索引中）。如果未給出`read`-lock，則假設
  每個人都可以閱讀幫助條目。

對於指令，您可以像設定任何 lock 一樣設定與幫助相關的鎖定：

```python
class MyCommand(Command):
    """
    <docstring for command>
    """
    key = "mycommand"
    # everyone can use the command, builders can view it in the help index
    # but only devs can actually read the help (a weird setup for sure!)
    locks = "cmd:all();view:perm(Builders);read:perm(Developers)

```

Db-help 條目和 File-Help 條目的運作方式相同（`cmd` 型別除外）
lock 未使用。檔案幫助範例：

```python
help_entry = {
    # ...
    locks = "read:perm(Developer)",
    # ...
}

```

```{versionchanged} 1.0
   Changed the old 'view' lock to control the help-index inclusion and added
   the new 'read' lock-type to control access to the entry itself.
```

(customizing-the-look-of-the-help-system)=
### 自訂幫助系統的外觀

這幾乎完全是透過覆蓋 `help` 指令 [evennia.commands.default.help.CmdHelp](evennia.commands.default.help.CmdHelp) 來完成的。

由於可用的指令可能隨時變化，`help` 負責將幫助條目的三個來源（指令/資料庫/檔案）整理在一起並動態搜尋它們。它還對輸出進行所有格式化。

為了更容易調整外觀，更改視覺呈現和實體搜尋的程式碼部分已分解為指令類別上的單獨方法。在您的 `help` 版本中覆寫這些內容，以根據需要變更顯示或調整。有關詳細資訊，請參閱上面的 api 連結。

(subtopics)=
## 副主題

```{versionadded} 1.0
```

`text` 也可以分為_子主題_，而不是製作很長的幫助條目。下一層子主題的清單顯示在主要幫助文字下方，並允許使用者閱讀有關主要文字中不適合的某些特定細節的更多資訊。

子主題使用與 Markdown 標題稍微相似的標記。頂級標題必須命名為 `# subtopics`（不區分大小寫），且以下標題必須是該標題的子標題（例如 `## subtopic name` 等）。所有標題都不區分大小寫（幫助指令將格式化它們）。主題最多可以巢狀 5 層（這可能已經太多了）。解析器使用模糊匹配來尋找副主題，因此不必完全準確地輸入所有內容。

以下是帶有子主題的 `text` 的範例。

```
The theatre is the heart of the city, here you can find ...
(This is the main help text, what you get with `help theatre`)

# subtopics

## lore

The theatre holds many mysterious things...
(`help theatre/lore`)

### the grand opening

The grand opening is the name for a mysterious event where ghosts appeared ...
(`this is a subsub-topic to lore, accessible as `help theatre/lore/grand` or
any other partial match).

### the Phantom

Deep under the theatre, rumors has it a monster hides ...
(another subsubtopic, accessible as `help theatre/lore/phantom`)

## layout

The theatre is a two-story building situated at ...
(`help theatre/layout`)

## dramatis personae

There are many interesting people prowling the halls of the theatre ...
(`help theatre/dramatis` or `help theathre/drama` or `help theatre/personae` would work)

### Primadonna Ada

Everyone knows the primadonna! She is ...
(A subtopic under dramatis personae, accessible as `help theatre/drama/ada` etc)

### The gatekeeper

He always keeps an eye on the door and ...
(`help theatre/drama/gate`)

```


(technical-notes)=
## 技術說明

(help-entry-clashes)=
#### 幫助輸入衝突

如果三種型別的可用條目之間存在衝突的說明條目（同名），則優先順序是

    Command-auto-help > Db-help > File-help
    
如果新的說明條目可能被相同/相似名稱的指令或基於檔案的說明條目隱藏/被隱藏，`sethelp` 指令（僅處理建立基於資料庫的說明條目）將警告您。

(the-help-entry-container)=
#### 幫助條目容器

所有幫助條目（無論來源）都被解析為具有以下屬性的物件：

- `key` - 這是主要主題名稱。對於指令，這實際上是指令的`key`。
- `aliases` - Alternate names for the help entry.如果主要名稱很難記住，這可能很有用。
- `help_category` - 條目的一般分組。這是可選的。如果沒有給出，它將使用 `settings.COMMAND_DEFAULT_HELP_CATEGORY` 給出的預設類別作為指令和
`settings.DEFAULT_HELP_CATEGORY` 用於檔案+資料庫幫助條目。
- `locks` - Lock 字串（對於指令）或 LockHandler（所有幫助條目）。這定義了誰可以閱讀此條目。請參閱下一節。
- `tags` - 預設不使用，但可用於進一步組織幫助條目。
- `text` - 實際的幫助條目文字。這將在開頭和結尾處縮排並去除多餘的空間。

(help-pagination)=
#### 幫助分頁

滾出螢幕的 `text` 將自動由 [EvMore](./EvMore.md) 尋呼機分頁（您可以使用 `settings.HELP_MORE_ENABLED=False` 控制它）。如果您使用 EvMore 並希望準確控制分頁器應在何處分頁，請使用控製字元 `\f` 標記分頁。

(search-engine)=
#### 搜尋引擎

由於需要搜尋如此不同型別的資料，因此幫助系統必須在搜尋整個資料集之前收集記憶體中的所有可能性。它使用 [Lunr](https://github.com/yeraydiazdiaz/lunr.py) 搜尋引擎來搜尋主要的幫助條目。 Lunr 是一個用於網頁的成熟引擎，比以前的解決方案產生更合理的結果。

一旦找到主條目，就會使用簡單的 `==`、`startswith` 和 `in` 匹配來搜尋子主題（此時它們相對較少）。

```{versionchanged} 1.0
  Replaced the old bag-of-words algorithm with lunr package.

```
