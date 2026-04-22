(eveditor)=
# EvEditor


Evennia 在 `evennia.utils.eveditor.EvEditor` 中提供了強大的遊戲內線路編輯器。這位編輯，
模仿著名的 VI 行編輯器。它提供逐行編輯、撤銷/重做、行刪除、
搜尋/取代、填入、縮排等。

(launching-the-editor)=
## 啟動編輯器

編輯器建立如下：

```python
from evennia.utils.eveditor import EvEditor

EvEditor(caller,
         loadfunc=None, savefunc=None, quitfunc=None,
         key="")
```

 - `caller`（物件或帳號）：編輯器的使用者。
 - `loadfunc`（可呼叫，可選）：這是編輯器首次啟動時呼叫的函式。它
以 `caller` 作為唯一引數呼叫。該函式的傳回值用作
編輯器緩衝區中的起始文字。
 - `savefunc`（可呼叫，可選）：當使用者將緩衝區儲存在編輯器中時呼叫
使用兩個引數 `caller` 和 `buffer` 呼叫，其中 `buffer` 是當前緩衝區。
 - `quitfunc`（可呼叫，可選）：當使用者退出編輯器時呼叫。如果給定，所有
向使用者傳送的清理和退出訊息必須由該函式處理。
 - `key`（str，可選）：此文字將在編輯時顯示為識別碼和提醒。
它沒有其他機械功能。
 - `persistent`（預設`False`）：如果設定為`True`，編輯器將在重新啟動後繼續存在。

(working-with-eveditor)=
## 與 EvEditor 一起工作

這是使用編輯器設定特定 Attribute 的範例指令。

```python
from evennia import Command
from evennia.utils import eveditor

class CmdSetTestAttr(Command):
    """
    Set the "test" Attribute using
    the line editor.

    Usage:
       settestattr

    """
    key = "settestattr"
    def func(self):
        "Set up the callbacks and launch the editor"
        def load(caller):
            "get the current value"
            return caller.attributes.get("test")
        def save(caller, buffer):
            "save the buffer"
            caller.attributes.add("test", buffer)
        def quit(caller):
            "Since we define it, we must handle messages"
            caller.msg("Editor exited")
        key = f"{self.caller}/test"
        # launch the editor
        eveditor.EvEditor(self.caller,
                          loadfunc=load, savefunc=save, quitfunc=quit,
                          key=key)
```

(persistent-editor)=
### 持久編輯器

如果您在建立編輯器時將`persistent`關鍵字設為`True`，即使
重新載入遊戲時。  為了持久化，編輯器需要有回撥函式
（`loadfunc`、`savefunc` 和 `quitfunc`）作為模組中定義的頂級函式。  由於這些
函式將被儲存，Python 將需要找到它們。

```python
from evennia import Command
from evennia.utils import eveditor

def load(caller):
    "get the current value"
    return caller.attributes.get("test")

def save(caller, buffer):
    "save the buffer"
    caller.attributes.add("test", buffer)

def quit(caller):
    "Since we define it, we must handle messages"
    caller.msg("Editor exited")

class CmdSetTestAttr(Command):
    """
    Set the "test" Attribute using
    the line editor.

    Usage:
       settestattr

    """
    key = "settestattr"
    def func(self):
        "Set up the callbacks and launch the editor"
        key = f"{self.caller}/test"
        # launch the editor
        eveditor.EvEditor(self.caller,
                          loadfunc=load, savefunc=save, quitfunc=quit,
                          key=key, persistent=True)
```

(line-editor-usage)=
### 行編輯器的使用

此編輯器盡可能模仿 `VIM` 編輯器。以下是回傳的摘錄
編輯器內幫助指令 (`:h`)。

```
 <txt>  - any non-command is appended to the end of the buffer.
 :  <l> - view buffer or only line <l>
 :: <l> - view buffer without line numbers or other parsing
 :::    - print a ':' as the only character on the line...
 :h     - this help.

 :w     - save the buffer (don't quit)
 :wq    - save buffer and quit
 :q     - quit (will be asked to save if buffer was changed)
 :q!    - quit without saving, no questions asked

 :u     - (undo) step backwards in undo history
 :uu    - (redo) step forward in undo history
 :UU    - reset all changes back to initial state

 :dd <l>     - delete line <n>
 :dw <l> <w> - delete word or regex <w> in entire buffer or on line <l>
 :DD         - clear buffer

 :y  <l>        - yank (copy) line <l> to the copy buffer
 :x  <l>        - cut line <l> and store it in the copy buffer
 :p  <l>        - put (paste) previously copied line directly before <l>
 :i  <l> <txt>  - insert new text <txt> at line <l>. Old line will move down
 :r  <l> <txt>  - replace line <l> with text <txt>
 :I  <l> <txt>  - insert text at the beginning of line <l>
 :A  <l> <txt>  - append text after the end of line <l>

 :s <l> <w> <txt> - search/replace word or regex <w> in buffer or on line <l>

 :f <l>    - flood-fill entire buffer or line <l>
 :fi <l>   - indent entire buffer or line <l>
 :fd <l>   - de-indent entire buffer or line <l>

 :echo - turn echoing of the input on/off (helpful for some clients)

    Legend:
    <l> - line numbers, or range lstart:lend, e.g. '3:7'.
    <w> - one word or several enclosed in quotes.
    <txt> - longer string, usually not needed to be enclosed in quotes.
```

(the-eveditor-to-edit-code)=
### EvEditor編輯程式碼

`EvEditor`也用於編輯Evennia中的一些Python程式碼。  `py` 指令支援 `/edit` 開關，該開關將在程式碼模式下開啟 EvEditor。  此模式與標準模式沒有顯著不同，只是它處理區塊的自動縮排以及一些控制此行為的選項。

- `:<` 刪除未來行的縮排等級。
- `:+` 為未來的行新增縮排等級。
- `:=` 完全停用自動縮排。

自動縮排可以使程式碼編輯更加簡單。  Python 需要正確的縮排，不是為了美觀，而是為了確定區塊的開頭和結尾。  EvEditor 將嘗試猜測下一個縮排等級。  例如，如果您鍵入「if」區塊，EvEditor 將建議您在下一行進行額外的縮排。  然而，此功能並不完美，有時，您必須使用上述選項來處理縮排。

`:=` 可用於完全關閉自動縮排。  這在嘗試時非常有用
例如，貼上幾行已經正確縮排的程式碼。

要在程式碼模式下檢視EvEditor，可以使用`@py/edit`指令。  輸入您的程式碼（一行或多行）。  然後您可以使用 `:w` 選項（儲存而不退出）和您擁有的程式碼
輸入的內容將會被執行。  `:!` 也會做同樣的事情。  在不關閉的情況下執行程式碼
如果您想測試已鍵入的程式碼但在測試後新增行，編輯器可能會很有用。
