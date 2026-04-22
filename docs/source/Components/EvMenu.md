(evmenu)=
# EvMenu

```shell
Is your answer yes or no?
_________________________________________
[Y]es! - Answer yes.
[N]o! - Answer no.
[A]bort - Answer neither, and abort.

> Y
You chose yes!

Thanks for your answer. Goodbye!
```

_EvMenu_ 用於產生分支多選選單。每個選單“節點”可以
接受特定選項作為輸入或自由格式輸入。取決於玩家甚麼
選擇後，它們將被轉發到選單中的不同節點。

`EvMenu` 實用程式類別位於 [evennia/utils/evmenu.py](evennia.utils.evmenu)。
它允許輕鬆地向遊戲新增互動式選單；例如，實現角色建立、建立指令或類似指令。下面是提供 NPC 對話選項的範例：

這是本頁頂部的範例選單在程式碼中的外觀：

```python
from evennia.utils import evmenu

def _handle_answer(caller, raw_input, **kwargs):
    answer = kwargs.get("answer")
    caller.msg(f"You chose {answer}!")
    return "end"  # name of next node

def node_question(caller, raw_input, **kwargs):
    text = "Is your answer yes or no?"
    options = (
        {"key": ("[Y]es!", "yes", "y"),
         "desc": Answer yes.",
         "goto": _handle_answer, {"answer": "yes"}},
        {"key": ("[N]o!", "no", "n"),
         "desc": "Answer no.",
         "goto": _handle_answer, {"answer": "no"}},
        {"key": ("[A]bort", "abort", "a"),
         "desc": "Answer neither, and abort.",
         "goto": "end"}
    )
    return text, options

def node_end(caller, raw_input, **kwargs):
    text "Thanks for your answer. Goodbye!"
    return text, None  # empty options ends the menu

evmenu.EvMenu(caller, {"start": node_question, "end": node_end})

```

注意最後對`EvMenu`的呼叫；這會立即建立選單
`caller`。它還將兩個節點功能分配給選單節點名稱 `start` 和
`end`，這是選單用來引用節點的內容。

選單的每個節點都是一個傳迴文字和字典列表的函式
描述您可以在該節點上做出的選擇。

每個選項都詳細說明瞭應顯示的內容（鍵/描述）以及要顯示的節點
到（轉到）下一個。 「goto」應該是下一個要轉到的節點的名稱（如果`None`，
同一節點將再次重新執行）。

上面，`Abort` 選項給出了“結束”節點名稱作為字串，而
yes/no 選項改為使用可呼叫 `_handle_answer` 但傳遞不同的
對此的論據。 `_handle_answer` 然後返回下一個節點的名稱（這
允許您在進行選擇之前執行操作
選單的下一個節點）。請注意，`_handle_answer` 不是選單中的節點，
它只是一個輔助函式。

當選擇“是”（或“否”）時，會發生 `_handle_answer` 得到
在定向到退出的「結束」節點之前呼叫並回顯您的選擇
選單（因為它不返回任何選項）。

您也可以使用[EvMenu 範本語言](#evmenu-templating-language) 編寫選單。這個
允許您使用文字字串產生更簡單的選單和更少的鍋爐
板。讓我們使用模板語言來建立完全相同的選單：

```python
from evennia.utils import evmenu

def _handle_answer(caller, raw_input, **kwargs):
    answer = kwargs.get("answer")
    caller.msg(f"You chose {answer}!")
    return "end"  # name of next node

menu_template = """

## node start

Is your answer yes or no?

## options

[Y]es!;yes;y: Answer yes. -> handle_answer(answer=yes)
[N]o!;no;n: Answer no. -> handle_answer(answer=no)
[A]bort;abort;a: Answer neither, and abort. -> end

## node end

Thanks for your answer. Goodbye!

"""

evmenu.template2menu(caller, menu_template, {"handle_answer": _handle_answer})

```

如圖所示，`_handle_answer` 是相同的，但選單結構是
`menu_template` 字串中描述。 `template2menu` 助手
使用模板字串和可呼叫物件的對映（我們必須新增
`_handle_answer` 此處）為我們建立完整的 EvMenu。

這是另一個選單範例，我們可以在其中選擇如何與 NPC 互動：

```
The guard looks at you suspiciously.
"No one is supposed to be in here ..."
he says, a hand on his weapon.
_______________________________________________
 1. Try to bribe him [Cha + 10 gold]
 2. Convince him you work here [Int]
 3. Appeal to his vanity [Cha]
 4. Try to knock him out [Luck + Dex]
 5. Try to run away [Dex]
```

```python

def _skill_check(caller, raw_string, **kwargs):
    skills = kwargs.get("skills", [])
    gold = kwargs.get("gold", 0)

    # perform skill check here, decide if check passed or not
    # then decide which node-name to return based on
    # the result ...

    return next_node_name

def node_guard(caller, raw_string, **kwarg):
    text = (
        'The guard looks at you suspiciously.\n'
        '"No one is supposed to be in here ..."\n'
        'he says, a hand on his weapon.'
    options = (
        {"desc": "Try to bribe on [Cha + 10 gold]",
         "goto": (_skill_check, {"skills": ["Cha"], "gold": 10})},
        {"desc": "Convince him you work here [Int].",
         "goto": (_skill_check, {"skills": ["Int"]})},
        {"desc": "Appeal to his vanity [Cha]",
         "goto": (_skill_check, {"skills": ["Cha"]})},
        {"desc": "Try to knock him out [Luck + Dex]",
         "goto": (_skill_check, {"skills"" ["Luck", "Dex"]})},
        {"desc": "Try to run away [Dex]",
         "goto": (_skill_check, {"skills": ["Dex"]})}
    return text, options
    )

# EvMenu called below, with all the nodes ...

```

請注意，透過跳過選項的`key`，我們會得到一個
（自動產生）可供選擇的編號選項清單。

這裡 `_skill_check` 助理將檢查（滾動你的統計資料，這到底是什麼
方法取決於您的遊戲）來決定您的方法是否成功。那麼可能
選擇將您指向繼續對話的節點，或者可能轉儲您
投入戰鬥！


(launching-the-menu)=
## 啟動選單

初始化選單是透過呼叫 `evennia.utils.evmenu.EvMenu` 類別來完成的。這是最常見的方法 - 從 [Command](./Commands.md) 內部：

```python
# in, for example gamedir/commands/command.py

from evennia.utils.evmenu import EvMenu

class CmdTestMenu(Command):

    key = "testcommand"

    def func(self):

	EvMenu(self.caller, "world.mymenu")

```

執行此指令時，選單將開始使用從載入的選單節點
`mygame/world/mymenu.py`。請參閱下一節，瞭解如何定義選單節點。

`EvMenu` 有以下可選呼號：

```python
EvMenu(caller, menu_data,
       startnode="start",
       cmdset_mergetype="Replace", cmdset_priority=1,
       auto_quit=True, auto_look=True, auto_help=True,
       cmd_on_exit="look",
       persistent=False,
       startnode_input="",
       session=None,
       debug=False,
       **kwargs)

```

 - `caller`（物件或帳戶）：是使用選單對物件的引用。該物件將獲得分配給它的新的 [CmdSet](./Command-Sets.md)，用於處理選單。
 - `menu_data`（str、module 或 dict）：是一個模組或模組的 python 路徑，其中全域級函式將被視為選單節點。它們在模組中的名稱將是在模組中引用它們的名稱。重要的是，以下劃線 `_` 開頭的函式名稱將被載入程式忽略。或者，這可以是直接對映
`{"nodename":function,...}`。
 - `startnode` (str)：是啟動選單的選單節點的名稱。更改此設定意味著您可以根據情況跳到不同位置的選單樹，從而可能重新使用選單專案。
 - `cmdset_mergetype` (str)：這通常是「替換」或「聯合」之一（請參閱 [CmdSets](Command- Sets)。第一個表示選單是獨佔的 - 使用者在選單中無法存取任何其他指令。聯合合併型別表示選單與先前的指令共存（並且可能會使它們過載，因此在這種情況下要小心命名專案的名稱）。
 - `cmdset_priority` (int)：在選單 cmdset 中合併的優先順序。這允許高階使用。
 - `auto_quit`、`auto_look`、`auto_help`（布林值）：如果其中任何一個是 `True`，則選單會自動向使用者提供 `quit`、`look` 或 `help` 指令。您想要關閉此功能的主要原因是您想在選單中使用別名“q”、“l”或“h”。 `auto_help` 也會啟動在選單節點中具有任意「工具提示」的功能（見下文），強烈建議至少使用 `quit` - 如果 `False`，則選單 *必須* 本身提供一個「退出節點」（沒有任何選項的節點），否則使用者將卡在選單中，直到伺服器重新載入選單（或如果選單是 `persistent`，選單中！
 - `cmd_on_exit` (str)：此指令字串將在選單關閉後立即執行。根據經驗，觸發「檢視」指令以確保使用者意識到狀態的變化很有用；但可以使用任何指令。如果設定為`None`，則退出選單後不會觸發任何指令。
 - `persistent` (bool) - 如果`True`，選單將在重新載入後繼續存在（因此使用者不會被踢
透過重新載入退出 - 確保他們可以自行退出！）
 - `startnode_input` (str or (str, dict) tuple): 將輸入文字或輸入文字 + kwargs 傳遞給
啟動節點，就好像它是在虛構的前一個節點上輸入的。這非常有用，以便
   根據初始化選單的指令引數，以不同的方式啟動選單。
 - `session` (Session): 當從[帳號](./Accounts.md)呼叫選單時有用
`MULTISESSION_MODE` 高於 2，以確保只有正確的 Session 才能看到選單輸出。
 - `debug`（布林）：如果設定，`menudebug` 指令將在選單中可用。用它來
列出選單的目前狀態並使用 `menudebug <variable>` 檢查特定狀態
   列表中的變數。
 - 所有其他關鍵字引數將可用作節點的初始資料。它們將作為 `caller.ndb._evmenu` 上的屬性在所有節點中可用（見下文）。如果選單是`persistent`，這些也將保留`reload`。

您不需要將 EvMenu 例項儲存在任何地方 - 初始化它的行為本身就會儲存它
作為 `caller` 上的 `caller.ndb._evmenu`。當選單出現時，該物件將自動刪除
退出後，您還可以使用它來儲存自己的臨時變數，以便在整個過程中訪問
選單。當它執行時，您儲存在永續性`_evmenu`上的臨時變數將
*不會*在 `@reload` 中倖存，只有那些您設定為原始 `EvMenu` 呼叫一部分的內容。

(the-menu-nodes)=
## 選單節點

EvMenu 節點由這些表單之一上的函式組成。

```python
def menunodename1(caller):
    # code
    return text, options

def menunodename2(caller, raw_string):
    # code
    return text, options

def menunodename3(caller, raw_string, **kwargs):
    # code
    return text, options

```

> 雖然上述所有形式都可以，但建議堅持使用第三種也是最後一種形式，因為它提供了最大的靈活性。以前的形式主要是為了向後相容現有的選單，當時 EvMenu 的能力較差，並且可能在將來的某個時候被棄用。


(input-arguments-to-the-node)=
### 節點的輸入引數

 - `caller`（物件或帳戶）：使用選單的物件 - 通常是角色，但也可以是 Session 或帳戶，取決於使用選單的位置。
 - `raw_string` (str)：如果給出了該值，它將被設定為使用者在
*前一個*節點（即為到達此節點而輸入的指令）。在選單的起始節點上，這將是一個空字串，除非設定了`startnode_input`。
 - `kwargs` (dict)：這些額外的關鍵字引數是當使用者在*前一個*節點上做出選擇時傳遞給節點的額外可選引數。這可能包括狀態標誌和有關選擇哪個確切選項的詳細資訊（這可能無法從
`raw_string` 單獨）。 `kwargs` 中傳遞的內容取決於您建立前一個節點時的情況。

(return-values-from-the-node)=
### 從節點傳回值

每個節點函式必須傳回兩個變數，`text` 和 `options`。


(text)=
#### 文字

`text` 變數是字串或元組。這是最簡單的形式：

```python
text = "Node text"
```

這是進入選單節點時將顯示為文字的內容。如果需要，您可以在節點中動態修改它。允許返回 `None` 節點文字文字 - 這會導致節點沒有文字而只有選項。

```python
text = ("Node text", "help text to show with h|elp")
```

在這種形式中，我們還新增了可選的幫助文字。如果`auto_help=True`在初始化EvMenu時，使用者在檢視此節點時將能夠使用`h`或`help`看到此文字。如果使用者要提供覆蓋 `h` 或 `help` 的自訂選項，則會顯示該選項。

如果 `auto_help=True` 且未提供幫助文字，則使用 `h|elp` 將給出一般錯誤訊息。

```python
text = ("Node text", {"help topic 1": "Help 1", 
                      ("help topic 2", "alias1", ...): "Help 2", ...})
```

這是「工具提示」或「多重幫助類別」模式。這在初始化EvMenu時也需要`auto_help=True`。透過提供 `dict` 作為 `text` 元組的第二個元素，使用者將能夠就這些主題中的任何主題提供協助。使用元組作為鍵將多個別名新增至相同幫助條目。這允許使用者在不離開給定節點的情況下獲得更詳細的幫助文字。

請注意，在「工具提示」模式下，正常的 `h|elp` 指令將無法運作。 `h|elp` 條目必須手動新增到字典中。例如，這將重現正常的幫助功能：

```python
text = ("Node text", {("help", "h"): "Help entry...", ...})
```

(options)=
#### 選項

`options` 清單描述了使用者在檢視此節點時可用的所有選擇。如果 `options` 作為 `None` 返回，則表示該節點是*退出節點* - 顯示任何文字，然後選單立即退出，執行 `exit_cmd`（如果給定）。

否則，`options` 應該是一個字典列表（或元組），每個選項一個。如果只有一個選項可用，也可以傳回單一字典。它看起來是這樣的：


```python
def node_test(caller, raw_string, **kwargs):

    text = "A goblin attacks you!"

    options = (
	{"key": ("Attack", "a", "att"),
         "desc": "Strike the enemy with all your might",
         "goto": "node_attack"},
	{"key": ("Defend", "d", "def"),
         "desc": "Hold back and defend yourself",
         "goto": (_defend, {"str": 10, "enemyname": "Goblin"})})

    return text, options

```

這將產生一個如下所示的選單節點：


```
A goblin attacks you!
________________________________

Attack: Strike the enemy with all your might
Defend: Hold back and defend yourself

```

(option-key-key)=
##### 選項鍵 'key'

此選項的 `key` 是使用者應該輸入的內容才能選擇該選項。如果以元組形式給出，則該元組的第一個字串將是螢幕上顯示的內容，而其餘字串是用於選擇該選項的別名。在上面的例子中，使用者可以輸入“Attack”（或“attack”，不區分大小寫）、“a”或“att”來攻擊妖精。別名對於向選擇新增自訂顏色很有用。別名元組的第一個元素應該是彩色版本，後面是沒有顏色的版本 - 否則使用者將必須輸入顏色程式碼才能選擇該選項。

請注意，`key` 是*可選*。如果沒有給出金鑰，它將自動被替換
流水號從 `1` 開始。如果刪除每個選項的 `key` 部分，則結果
選單節點將如下所示：


```
A goblin attacks you!
________________________________

1: Strike the enemy with all your might
2: Hold back and defend yourself

```

無論您想使用按鍵還是依賴數字，主要取決於選單的風格和型別。

EvMenu 接受僅作為 `"_default"` 給出的一個重要特殊 `key`。當使用者輸入與任何其他固定鍵不符的內容時，將使用此鍵。它對於獲取使用者輸入特別有用：

```python
def node_readuser(caller, raw_string, **kwargs):
    text = "Please enter your name"

    options = {"key": "_default",
               "goto": "node_parse_input"}

    return text, options

```

`"_default"` 選項不會出現在選單中，因此上面只是一個節點
`"Please enter your name"`。他們輸入的名稱將在下一個節點中顯示為 `raw_string`。


(option-key-desc)=
#### 選項鍵“desc”

這僅包含有關選擇選單選項時發生的情況的描述。對於 `"_default"` 選項或如果 `key` 已經很長或具有描述性，則不是嚴格需要的。但通常最好保持 `key` 簡短並在 `desc` 中放置更多細節。


(option-key-goto)=
#### 選項鍵“轉到”

這是選項的操作部分，僅當使用者選擇所述選項時才會觸發。這裡有三種寫法

```python

def _action_two(caller, raw_string, **kwargs):
    # do things ...
    return "calculated_node_to_go_to"

def _action_three(caller, raw_string, **kwargs):
    # do things ...
    return "node_four", {"mode": 4}

def node_select(caller, raw_string, **kwargs):

    text = ("select one",
            "help - they all do different things ...")

    options = ({"desc": "Option one",
		            "goto": "node_one"},
	             {"desc": "Option two",
		            "goto": _action_two},
	             {"desc": "Option three",
		            "goto": (_action_three, {"key": 1, "key2": 2})}
              )

    return text, options

```

如上所示，`goto` 可能只是指向單一 `nodename` 字串 - 要轉到的節點的名稱。當像這樣給出時， EvMenu 將尋找這樣命名的節點並呼叫其關聯函式：

```python
    nodename(caller, raw_string, **kwargs)
```

這裡，`raw_string` 始終是使用者在做出選擇時輸入的輸入，`kwargs` 與已經進入 *目前* 節點的 `kwargs` 相同（它們被傳遞）。

或者，`goto` 可以指向「goto-callable」。此類可呼叫專案通常在與選單節點相同的模組中定義，並給出以 `_` 開頭的名稱（以避免被解析為節點本身）。這些可呼叫函式的呼叫方式與節點函式相同 - `callable(caller, raw_string, **kwargs)`，其中 `raw_string` 是使用者在此節點上輸入的內容，`**kwargs` 是從節點自己的輸入轉發的。

`goto` 選項鍵也可以指向元組 `(callable, kwargs)` - 這允許自訂傳遞到 goto-callable 的 kwargs，例如，您可以使用相同的可呼叫函式，但根據實際選擇的選項變更傳遞到其中的 kwargs。

「goto callable」必須傳回字串 `"nodename"` 或元組 `("nodename", mykwargs)`。這將導致下一個節點被稱為 `nodename(caller, raw_string, **kwargs)` 或 `nodename(caller, raw_string, **mykwargs)` - 因此這允許根據選擇的選項更改（或替換）進入下一個節點的選項。

有一個重要的情況 - 如果 goto-callable 對於 `nodename` 返回 `None`，*當前節點將再次執行*，可能會使用不同的 kwargs。這使得一遍又一遍地重複使用節點變得非常容易，例如允許不同的選項來更新每次迭代傳遞和操作的某些文字表單。


(temporary-storage)=
### 暫存

當選單啟動時，EvMenu 例項在呼叫方上儲存為 `caller.ndb._evmenu`。如果您知道自己在做什麼，則原則上可以透過此物件到達選單的內部狀態。這也是儲存臨時的、更多全域變數的好地方，這些變數透過 `**kwargs` 在節點之間傳遞可能會很麻煩。選單關閉時，`_evmnenu` 將自動刪除，這表示您無需擔心清理任何內容。

如果您想要*永久*狀態儲存，最好在 `caller` 上使用 Attribute。請記住，選單關閉後它將保留，因此您需要自己處理任何所需的清理工作。


(customizing-menu-formatting)=
### 自訂選單格式

`EvMenu` 節點、選項等的顯示由 `EvMenu` 類別上的一系列格式化方法控制。要自訂這些，只需建立 `EvMenu` 的新子類別並根據需要進行覆蓋即可。這是一個例子：

```python
from evennia.utils.evmenu import EvMenu

class MyEvMenu(EvMenu):

    def nodetext_formatter(self, nodetext):
        """
        Format the node text itself.

        Args:
            nodetext (str): The full node text (the text describing the node).

        Returns:
            nodetext (str): The formatted node text.

        """

    def helptext_formatter(self, helptext):
        """
        Format the node's help text

        Args:
            helptext (str): The unformatted help text for the node.

        Returns:
            helptext (str): The formatted help text.

        """

    def options_formatter(self, optionlist):
        """
        Formats the option block.

        Args:
            optionlist (list): List of (key, description) tuples for every
                option related to this node.
            caller (Object, Account or None, optional): The caller of the node.

        Returns:
            options (str): The formatted option display.

        """

    def node_formatter(self, nodetext, optionstext):
        """
        Formats the entirety of the node.

        Args:
            nodetext (str): The node text as returned by `self.nodetext_formatter`.
            optionstext (str): The options display as returned by `self.options_formatter`.
            caller (Object, Account or None, optional): The caller of the node.

        Returns:
            node (str): The formatted node to display.

        """

```
有關其預設實現的詳細資訊，請參閱 `evennia/utils/evmenu.py`。

(evmenu-templating-language)=
## EvMenu 範本語言

`evmenu.py` 中有兩個輔助函式 `parse_menu_template` 和 `template2menu`，用於將 _menu template_ 字串解析為 EvMenu：

    evmenu.template2menu(caller, menu_template, goto_callables)

也可以分兩步完成，產生一個選單樹並使用它來呼叫
EvMenu 通常：

    menutree = evmenu.parse_menu_template(caller, menu_template, goto_callables)
    EvMenu(caller, menutree)

使用後一種解決方案，可以混合和匹配正常建立的選單節點
與模板引擎生成的那些。

`goto_callables` 是一個對映 `{"funcname": callable,...}`，其中每個
callable 必須是表單上的模組全域函式
`funcname(caller, raw_string, **kwargs)`（就像任何 goto-callable 一樣）。的
`menu_template` 是以下形式的多行字串：

```python
menu_template = """

## node node1

Text for node

## options

key1: desc1 -> node2
key2: desc2 -> node3
key3: desc3 -> node4
"""
```

每個選單節點由包含該節點文字的 `## node <name>` 定義，
其次是`## options` `## NODE` 和`## OPTIONS` 也有效。沒有Python程式碼
模板中允許使用邏輯，該程式碼不會被評估，而是會被解析。更多
進階動態使用需要完整的節點功能。

除了定義節點/選項之外，`#` 充當註釋 - 以下內容
將被模板解析器忽略。

(template-options)=
### 模板選項

選項語法是

    <key>: [desc ->] nodename or function-call

'desc' 部分是可選的，如果未給出，則可以跳過 `->`
太：

    key: nodename

鍵可以是字串和數字。以 `;` 分隔別名。

    key: node1
    1: node2
    key;k: node3
    foobar;foo;bar;f;b: node4

以特殊字母`>`開頭的鍵表示後面是
glob/正規表示式匹配器。

    >: node1          - matches empty input
    > foo*: node1     - everything starting with foo
    > *foo: node3     - everything ending with foo
    > [0-9]+?: node4  - regex (all numbers)
    > *: node5        - catches everything else (put as last option)

以下是從選項呼叫 goto 函式的方法：

    key: desc -> myfunc(foo=bar)

為此，必須給 `template2menu` 或 `parse_menu_template` 一個字典
其中包括`{"myfunc": _actual_myfunc_callable}`。所有可呼叫物件都是
模板中可用的內容必須以這種方式對應。 Goto 可呼叫的行為就像
正常的 EvMenu goto-callables 並且應該有一個呼號
`_actual_myfunc_callable(caller, raw_string, **kwargs)`並回傳下一個節點
（將動態 kwargs 傳遞到下一個節點不適用於模板
- 如果您想要進階動態資料傳遞，請使用完整的EvMenu）。

這些可呼叫物件中只允許不使用或命名關鍵字。所以

    myfunc()         # OK
    myfunc(foo=bar)  # OK
    myfunc(foo)      # error!

這是因為這些屬性作為 `**kwargs` 傳遞到 goto 可呼叫函式。

(templating-example)=
### 模板化範例

```python
from random import random
from evennia.utils import evmenu

def _gamble(caller, raw_string, **kwargs):

    caller.msg("You roll the dice ...")
    if random() < 0.5:
        return "loose"
    else:
        return "win"

template_string = """

## node start

Death patiently holds out a set of bone dice to you.

"ROLL"

he says.

## options

1: Roll the dice -> gamble()
2: Try to talk yourself out of rolling -> start

## node win

The dice clatter over the stones.

"LOOKS LIKE YOU WIN THIS TIME"

says Death.

# (this ends the menu since there are no options)

## node loose

The dice clatter over the stones.

"YOUR LUCK RAN OUT"

says Death.

"YOU ARE COMING WITH ME."

# (this ends the menu, but what happens next - who knows!)

"""

# map the in-template callable-name to real python code
goto_callables = {"gamble": _gamble}
# this starts the evmenu for the caller
evmenu.template2menu(caller, template_string, goto_callables)

```

(asking-for-one-line-input)=
## 要求單行輸入

這描述了向使用者詢問簡單問題的兩種方法。使用Python的`input`
在 Evennia 中*不起作用*。 `input` 將為*所有人**阻止*整個伺服器，直到那個人
玩家已輸入他們的文字，這不是您想要的。

(the-yield-way)=
### `yield`方式

在指令的 `func` 方法中（僅），您可以使用 Python 的內建 `yield` 指令來
以與 `input` 類似的方式請求輸入。它看起來像這樣：

```python
result = yield("Please enter your answer:")
```

這會將「請輸入您的答案」傳送到指令的 `self.caller`，然後在此暫停
點。伺服器上的所有其他玩家將不受影響。一旦呼叫者輸入回覆，程式碼
執行將繼續，您可以使用 `result` 執行操作。這是一個例子：

```python
from evennia import Command
class CmdTestInput(Command):
    key = "test"
    def func(self):
        result = yield("Please enter something:")
        self.caller.msg(f"You entered {result}.")
        result2 = yield("Now enter something else:")
        self.caller.msg(f"You now entered {result2}.")
```

使用 `yield` 簡單直觀，但它只能存取來自 `self.caller` 的輸入，並且您
在玩家做出回應之前，無法中止或逾時暫停。在幕後，它實際上是
只是一個呼叫下一節中描述的 `get_input` 的包裝器。

> 重要提示：在 Python 中，您*無法在相同方法中混合 `yield` 和 `return <value>`*。它有
> 與 `yield` 將方法變成
> [發電機](https://www.learnpython.org/en/Generators)。不含引數的 `return` 可以工作，你
> 不能做`return <value>`。無論如何，這通常不是你需要在 `func()` 中做的事情，
> 但值得記住。

(the-get_input-way)=
### `get_input`方式

evmenu 模組提供了一個名為 `get_input` 的輔助函式。這是由 `yield` 包裹的
語句使用起來通常更容易、更直覺。但 `get_input` 提供了更大的靈活性
和電源（如果您需要的話）。雖然與 `EvMenu` 位於同一模組中，但 `get_input` 在技術上不相關
到它。 `get_input` 允許您詢問並接收使用者的簡單一行輸入，而無需
啟動選單的全部功能來執行此操作。要使用，請像這樣呼叫 `get_input`：

```python
get_input(caller, prompt, callback)
```

這裡 `caller` 是應該接收 `prompt` 輸入提示的實體。的
`callback` 是您定義用來處理答案的可呼叫 `function(caller, prompt, user_input)`
來自使用者。執行時，呼叫者將看到 `prompt` 出現在他們的螢幕上以及他們的*任何*文字
Enter 將被傳送到回呼中以進行您想要的任何處理。

以下是完整解釋的回撥和範例呼叫：

```python
from evennia import Command
from evennia.utils.evmenu import get_input

def callback(caller, prompt, user_input):
    """
    This is a callback you define yourself.

    Args:
        caller (Account or Object): The one being asked
          for input
        prompt (str): A copy of the current prompt
        user_input (str): The input from the account.

    Returns:
        repeat (bool): If not set or False, exit the
          input prompt and clean up. If returning anything
          True, stay in the prompt, which means this callback
          will be called again with the next user input.
    """
    caller.msg(f"When asked '{prompt}', you answered '{user_input}'.")

get_input(caller, "Write something! ", callback)
```

這將顯示為

```
Write something!
> Hello
When asked 'Write something!', you answered 'Hello'.

```

通常， `get_input` 函式在任何輸入後都會退出，但如範例檔案所示，您可以
從回撥中返回 True 以重複提示，直到透過您想要的任何檢查。

> 注意：您*不能*透過在問題中新增新的`get_input` 呼叫來連結連續的問題
> 回撥 如果您希望您應該使用 EvMenu 代替（請參閱[重複相同
> 節點](./EvMenu.md#example-repeating-the-same-node) 上面的範例）。否則您可以檢視
> `get_input` 的實現並實現你自己的機制（它只是使用 cmdset 巢狀）或
> 你可以看看[郵件中建議的這個擴充套件
> 列表](https://groups.google.com/forum/#!category-topic/evennia/evennia-questions/16pi0SfMO5U)。


(example-yesno-prompt)=
#### 範例：是/否提示

以下是使用 `get_input` 函式的「是/否」提示的範例：

```python
def yesno(caller, prompt, result):
    if result.lower() in ("y", "yes", "n", "no"):
        # do stuff to handle the yes/no answer
        # ...
        # if we return None/False the prompt state
        # will quit after this
    else:
        # the answer is not on the right yes/no form
        caller.msg("Please answer Yes or No. \n{prompt}")
@        # returning True will make sure the prompt state is not exited
        return True

# ask the question
get_input(caller, "Is Evennia great (Yes/No)?", yesno)
```

(the-list_node-decorator)=
## `@list_node` 裝飾器

`evennia.utils.evmenu.list_node` 是與 `EvMenu` 節點函式一起使用的高階裝飾器。
它用於快速建立用於操作大量專案的選單。


```
text here
______________________________________________

1. option1     7. option7      13. option13
2. option2     8. option8      14. option14
3. option3     9. option9      [p]revius page
4. option4    10. option10      page 2
5. option5    11. option11     [n]ext page
6. option6    12. option12

```

此選單將自動建立一個可以翻閱的多頁選項清單。一個可以
檢查每個條目，然後使用上一個/下一個選擇它們。它的使用方式如下：


```python
from evennia.utils.evmenu import list_node


...

_options(caller):
    return ['option1', 'option2', ... 'option100']

_select(caller, menuchoice, available_choices):
    # analyze choice
    return "next_node"

@list_node(options, select=_select, pagesize=10)
def node_mylist(caller, raw_string, **kwargs):
    ...

    return text, options

```

`list_node` 的 `options` 引數是清單、產生器或傳回清單的可呼叫函式
應在節點中顯示的每個選項的字串。

`select` 在上面的範例中是可呼叫的，但也可以是選單節點的名稱。如果一個
可呼叫，`menuchoice` 引數儲存已完成的選擇，`available_choices` 儲存所有
可用選項。可呼叫物件應根據選擇返回要轉到的選單（或
`None` 重新執行相同節點）。如果是選單節點的名稱，則選擇將作為
`selection` kwarg 到該節點。

裝飾節點本身應該會傳回 `text` 以顯示在節點中。它必須至少返回一個
其選項為空字典。它會返回選項，這些選項將補充選項
由 `list_node` 裝飾器自動建立。

(example-menus)=
## 選單範例

這是一個圖表，可協助視覺化從節點到節點的資料流，包括中間的 goto-callables：

```
        ┌─
        │  def nodeA(caller, raw_string, **kwargs):
        │      text = "Choose how to operate on 2 and 3."
        │      options = (
        │          {
        │              "key": "A",
        │              "desc": "Multiply 2 with 3",
        │              "goto": (_callback, {"type": "mult", "a": 2, "b": 3})
        │          },                      ───────────────────┬────────────
        │          {                                          │
        │              "key": "B",                            └───────────────┐
        │              "desc": "Add 2 and 3",                                 │
  Node A│              "goto": (_callback, {"type": "add", "a": 2, "b": 3})   │
        │          },                      ─────────────────┬─────────────    │
        │          {                                        │                 │
        │              "key": "C",                          │                 │
        │              "desc": "Show the value 5",          │                 │
        │              "goto": ("node_B", {"c": 5})         │                 │
        │          }                      ───────┐          │                 │
        │      )                                 └──────────┼─────────────────┼───┐
        │      return text, options                         │                 │   │
        └─                                       ┌──────────┘                 │   │
                                                 │                            │   │
                                                 │ ┌──────────────────────────┘   │
        ┌─                                       ▼ ▼                              │
        │  def _callback(caller, raw_string, **kwargs):                           │
        │      if kwargs["type"] == "mult":                                       │
        │          return "node_B", {"c": kwargs["a"] * kwargs["b"]}              │
Goto-   │                           ───────────────┬────────────────              │
callable│                                          │                              │
        │                                          └───────────────────┐          │
        │                                                              │          │
        │      elif kwargs["type"] == "add":                           │          │
        │          return "node_B", {"c": kwargs["a"] + kwargs["b"]}   │          │
        └─                          ────────┬───────────────────────   │          │
                                            │                          │          │
                                            │ ┌────────────────────────┼──────────┘
                                            │ │                        │
                                            │ │ ┌──────────────────────┘
        ┌─                                  ▼ ▼ ▼
        │  def nodeB(caller, raw_string, **kwargs):
  Node B│      text = "Result of operation: " + kwargs["c"]
        │      return text, {}
        └─

        ┌─
   Menu │  EvMenu(caller, {"node_A": nodeA, "node_B": nodeB}, startnode="node_A")
   Start│
        └─
```

上面我們建立了一個非常簡單/愚蠢的選單（在最後的 `EvMenu` 呼叫中），我們將節點識別符號 `"node_A"` 對映到 Python 函式 `nodeA` 並將 `"node_B"` 對映到函式 `nodeB`。

我們從 `"node_A"` 開始選單，我們得到三個選項 A、B 和 C。選項 A 和 B 將透過一個可呼叫的 `_callback` 進行路由，在繼續到 `"node_B"` 之前將數字 2 和 3 相乘或相加。選項 C 直接路由到 `"node_B"`，傳遞數字 5。

在每一步中，我們都會傳遞一個字典，該字典將在下一步中成為傳入的 `**kwargs` 。如果我們沒有傳遞任何內容（它是可選的），下一步的 `**kwargs` 將是空的。

更多範例：

- **[簡單分支選單](./EvMenu.md#example-simple-branching-menu)** - 從選項中選擇
- **[動態跳轉](./EvMenu.md#example-dynamic-goto)** - 根據回應跳到不同節點
- **[設定呼叫者屬性](./EvMenu.md#example-set-caller-properties)** - 可以更改內容的選單
- **[取得任意輸入](./EvMenu.md#example-get-arbitrary-input)** - 輸入文字
- **[在節點之間儲存資料](./EvMenu.md#example-storing-data-between-nodes)** - 保持狀態和
選單中的資訊
- **[重複相同節點](./EvMenu.md#example-repeating-the-same-node)** - 在節點內驗證
在進入下一個之前
- **[是/否提示](#example-yesno-prompt)** - 輸入可能回應有限的文字
（這*不是*使用EvMenu，而是概念上相似但技術上不相關的`get_input`
輔助函式以 `evennia.utils.evmenu.get_input` 的形式存取）。


(example-simple-branching-menu)=
### 範例：簡單的分支選單

以下是一個簡單的分支選單節點的範例，根據選擇導致不同的其他節點：

```python
# in mygame/world/mychargen.py

def define_character(caller):
    text = \
    """
    What aspect of your character do you want
    to change next?
    """
    options = ({"desc": "Change the name",
                "goto": "set_name"},
               {"desc": "Change the description",
                "goto": "set_description"})
    return text, options

EvMenu(caller, "world.mychargen", startnode="define_character")

```

這將導致以下節點顯示：

```
What aspect of your character do you want
to change next?
_________________________
1: Change the name
2: Change the description
```

請注意，由於我們沒有指定「name」鍵，EvMenu 將讓使用者輸入數字。在
在下面的範例中，我們將不包含 `EvMenu` 呼叫，而僅顯示在
選單。另外，由於 `EvMenu` 也使用字典來描述選單，因此我們可以將其稱為
在範例中就像這樣：

```python
EvMenu(caller, {"define_character": define_character}, startnode="define_character")

```

(example-dynamic-goto)=
### 範例：動態跳轉

```python

def _is_in_mage_guild(caller, raw_string, **kwargs):
    if caller.tags.get('mage', category="guild_member"):
        return "mage_guild_welcome"
    else:
        return "mage_guild_blocked"

def enter_guild:
    text = 'You say to the mage guard:'
    options ({'desc': 'I need to get in there.',
              'goto': _is_in_mage_guild},
             {'desc': 'Never mind',
              'goto': 'end_conversation'})
    return text, options
```

這個簡單的可呼叫 goto 將根據 `caller` 是誰來分析發生的情況。  的
`enter_guild`節點會讓你選擇對守衛說些什麼。如果您嘗試進入，您將
最終會出現在不同的節點中，這取決於（在本例中）您是否設定了正確的 [Tag](./Tags.md)
無論你自己與否。請注意，由於我們在選項字典中不包含任何“鍵”，因此您只需
可以在數字之間進行選擇。

(example-set-caller-properties)=
### 範例：設定呼叫者屬性

這是將引數傳遞到 `goto` 可呼叫函式並使用它來影響的範例
下一個應該轉到哪個節點：

```python

def _set_attribute(caller, raw_string, **kwargs):
    "Get which attribute to modify and set it"

    attrname, value = kwargs.get("attr", (None, None))
    next_node = kwargs.get("next_node")

    caller.attributes.add(attrname, attrvalue)

    return next_node


def node_background(caller):
    text = \
    f"""
    {caller.key} experienced a traumatic event
    in their childhood. What was it?
    """

    options = ({"key": "death",
                "desc": "A violent death in the family",
                "goto": (_set_attribute, {"attr": ("experienced_violence", True),
					  "next_node": "node_violent_background"})},
               {"key": "betrayal",
                "desc": "The betrayal of a trusted grown-up",
                "goto": (_set_attribute, {"attr": ("experienced_betrayal", True),
					  "next_node": "node_betrayal_background"})})
    return text, options
```

這將給出以下輸出：

```
Kovash the magnificent experienced a traumatic event
in their childhood. What was it?
____________________________________________________
death: A violent death in the family
betrayal: The betrayal of a trusted grown-up

```

請注意上面我們如何使用 `_set_attribute` 輔助函式來設定 attribute 根據
使用者的選擇。在這種情況下，輔助函式不知道任何關於哪個節點呼叫它的資訊 - 我們
甚至告訴它應該返回哪個節點名，因此選擇會導致選單中的不同路徑。
我們還可以想像輔助函式分析哪些其他選擇


(example-get-arbitrary-input)=
### 範例：取得任意輸入

詢問使用者輸入的選單範例 - 任何輸入。

```python

def _set_name(caller, raw_string, **kwargs):

    inp = raw_string.strip()

    prev_entry = kwargs.get("prev_entry")

    if not inp:
        # a blank input either means OK or Abort
        if prev_entry:
            caller.key = prev_entry
            caller.msg(f"Set name to {prev_entry}.")
            return "node_background"
        else:
	    caller.msg("Aborted.")
	    return "node_exit"
    else:
        # re-run old node, but pass in the name given
        return None, {"prev_entry": inp}


def enter_name(caller, raw_string, **kwargs):

    # check if we already entered a name before
    prev_entry = kwargs.get("prev_entry")

    if prev_entry:
	text = "Current name: {}.\nEnter another name or <return> to accept."
    else:
	text = "Enter your character's name or <return> to abort."

    options = {"key": "_default",
               "goto": (_set_name, {"prev_entry": prev_entry})}

    return text, options

```

這將顯示為

```
Enter your character's name or <return> to abort.

> Gandalf

Current name: Gandalf
Enter another name or <return> to accept.

>

Set name to Gandalf.

```

在這裡，我們重複使用同一節點兩次來讀取使用者的輸入資料。無論我們輸入什麼都會
被 `_default` 選項捕獲並傳遞到輔助函式。我們也傳遞一切
我們之前輸入過的名稱。這使我們能夠對“空”輸入做出正確反應 - 繼續
如果我們接受輸入，則名為 `"node_background"` 的節點；如果按 Return 鍵，則轉到退出節點
無需輸入任何內容。透過從輔助函式返回`None`，我們自動重新執行
前一個節點，但更新其傳入的 kwargs 以告訴它顯示不同的文字。



(example-storing-data-between-nodes)=
### 範例：在節點之間儲存資料

儲存資料的一種便捷方法是將其儲存在您可以存取的`caller.ndb._evmenu`上
每個節點。這樣做的好處是 `_evmenu` NAttribute 將被刪除
退出選單時自動。

```python

def _set_name(caller, raw_string, **kwargs):

    caller.ndb._evmenu.charactersheet = {}
    caller.ndb._evmenu.charactersheet['name'] = raw_string
    caller.msg(f"You set your name to {raw_string}")
    return "background"

def node_set_name(caller):
    text = 'Enter your name:'
    options = {'key': '_default',
               'goto': _set_name}

    return text, options

...


def node_view_sheet(caller):
    text = f"Character sheet:\n {self.ndb._evmenu.charactersheet}"

    options = ({"key": "Accept",
                "goto": "finish_chargen"},
	       {"key": "Decline",
                "goto": "start_over"})

    return text, options

```

我們不是透過 `kwargs` 將字元表從一個節點傳遞到另一個節點，而是
暫時設定在`caller.ndb._evmenu.charactersheet`。這使得您可以輕鬆地從
所有節點。最後我們檢視它，如果我們接受該字元，選單可能會儲存
結果永久儲存並退出。

> 但要記住的一點是 `caller.ndb._evmenu` 上的儲存不會持久存在
> `@reloads`。如果您使用持久選單（使用 `EvMenu(..., persistent=True)` 您應該
使用
> `caller.db` 也可以像這樣儲存選單內資料。然後你必須自己確保清潔它
> 當使用者退出選單時。


(example-repeating-the-same-node)=
### 範例：重複相同的節點

有時您想要一個接一個地建立一系列選單節點，但您不希望使用者能夠繼續到下一個節點，直到您驗證他們在前一個節點中輸入的內容正確為止。一個常見的例子是登入選單：


```python

def _check_username(caller, raw_string, **kwargs):
    # we assume lookup_username() exists
    if not lookup_username(raw_string):
	# re-run current node by returning `None`
	caller.msg("|rUsername not found. Try again.")
	return None
    else:
	# username ok - continue to next node
	return "node_password"


def node_username(caller):
    text = "Please enter your user name."
    options = {"key": "_default",
               "goto": _check_username}
    return text, options


def _check_password(caller, raw_string, **kwargs):

    nattempts = kwargs.get("nattempts", 0)
    if nattempts > 3:
	caller.msg("Too many failed attempts. Logging out")
	return "node_abort"
    elif not validate_password(raw_string):
        caller.msg("Password error. Try again.")
	return None, {"nattempts", nattempts + 1}
    else:
	# password accepted
	return "node_login"

def node_password(caller, raw_string, **kwargs):
    text = "Enter your password."
    options = {"key": "_default",
	       "goto": _check_password}
    return text, options

```

這將顯示類似的內容


```
---------------------------
Please enter your username.
---------------------------

> Fo

------------------------------
Username not found. Try again.
______________________________
abort: (back to start)
------------------------------

> Foo

---------------------------
Please enter your password.
---------------------------

> Bar

--------------------------
Password error. Try again.
--------------------------
```

等等。

如果發生錯誤，goto-callables 將會回到前一個節點。如果是
密碼嘗試，這將勾選將從迭代中傳遞的 `nattempts` 引數
迭代，直到進行了太多次嘗試。


(defining-nodes-in-a-dictionary)=
### 定義字典中的節點

您也可以直接在字典中定義節點以饋送到 `EvMenu` 建立者。

```python
def mynode(caller):
   # a normal menu node function
   return text, options

menu_data = {"node1": mynode,
             "node2": lambda caller: (
                      "This is the node text",
                     ({"key": "lambda node 1",
                       "desc": "go to node 1 (mynode)",
                       "goto": "node1"},
                      {"key": "lambda node 2",
                       "desc": "go to thirdnode",
                       "goto": "node3"})),
             "node3": lambda caller, raw_string: (
                       # ... etc ) }

# start menu, assuming 'caller' is available from earlier
EvMenu(caller, menu_data, startnode="node1")

```

字典的鍵成為節點識別符號。您可以在正確的表單上使用任何可呼叫的
來描述每個節點。如果您使用 Python `lambda` 表示式，您可以真正動態地建立節點。
如果這樣做，則 lambda 表示式必須接受一個或兩個引數，並且始終傳回一個包含兩個引數的元組
元素（節點的文字及其選項），與任何選單節點功能相同。

建立這樣的選單是呈現隨情況變化的選單的一種方法 - 您
例如，可以根據某些條件在啟動功能表之前刪除或新增節點。的
缺點是 `lambda` 表示式 [ 更
有限](https://docs.python.org/2/tutorial/controlflow.html#lambda-expressions) 比完整
函式 - 例如，您不能在函式體內使用其他 Python 關鍵字，例如 `if`
`lambda`。

除非您正在處理相對簡單的動態選單，否則使用 lambda 定義選單是
可能比其價值更多的工作：您可以透過建立每個節點來建立動態選單
功能更加巧妙。有關範例，請參閱 [NPC 商店教學](../Howtos/Tutorial-NPC-Merchants.md)。
