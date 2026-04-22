(debugging)=
# 偵錯

有時，解決錯誤並不容易。一些簡單的 `print` 語句不足以找到問題的原因。回溯沒有提供任何訊息，甚至不存在。

執行*偵錯程式*會非常有幫助並且可以節省大量時間。除錯意味著在特殊*偵錯程式*程式的控制下執行Evennia。這允許您在給定點停止操作，檢視當前狀態並逐步執行程式以檢視其邏輯如何運作。

Evennia 本機支援這些偵錯程式：

- [Pdb](https://docs.python.org/2/library/pdb.html) 是 Python 發行版的一部分，並且
開箱即用。
- [PuDB](https://pypi.org/project/pudb/) 是一個第三方偵錯程式，功能稍多一些
'圖形'，基於curses的使用者介面而不是pdb。它是用`pip install pudb`安裝的。

(debugging-evennia)=
## 除錯Evennia

若要使用偵錯器執行 Evennia，請依照下列步驟操作：

1. 在程式碼中找到您想要獲得更多見解的點。在該處新增以下行
觀點。
    ```python
    from evennia import set_trace;set_trace()
    ```
2. 使用 `evennia istart` 以互動（前臺）模式（重新）啟動 Evennia。這很重要 - 如果沒有這一步，偵錯器將無法正確啟動 - 它將在此互動終端中啟動。
3. 執行將觸發您新增 `set_trace()` 呼叫的行的步驟。偵錯程式將在互動式啟動 Evennia 的終端中啟動。

`evennia.set_trace` 函式採用下列引數：


```python
    evennia.set_trace(debugger='auto', term_size=(140, 40))
```

這裡，`debugger`是`pdb`、`pudb`或`auto`之一。如果 `auto`，則使用 `pudb`（如果可用），否則使用 `pdb`。 `term_size` 元組僅設定 `pudb` 的視口大小（它被 `pdb` 忽略）。


(a-simple-example-using-pdb)=
## 使用 pdb 的簡單範例

偵錯程式在不同的情況下很有用，但首先，讓我們看看它在指令中的工作情況。
新增以下測試指令（其中有一系列故意錯誤）並將其新增到您的
預設cmdset。然後以互動模式與 `evennia istart` 重新啟動 Evennia。


```python
# In file commands/command.py


class CmdTest(Command):

    """
    A test command just to test pdb.

    Usage:
        test

    """

    key = "test"

    def func(self):
        from evennia import set_trace; set_trace()   # <--- start of debugger
        obj = self.search(self.args)
        self.msg("You've found {}.".format(obj.get_display_name()))

```

如果您在遊戲中輸入`test`，一切都會凍結。  您不會從遊戲中獲得任何回饋，也無法輸入任何指令（也無法輸入其他任何人）。  這是因為偵錯程式已在您的控制檯中啟動，您將在此處找到它。下面是一個帶有 `pdb` 的範例。

```
...
> .../mygame/commands/command.py(79)func()
-> obj = self.search(self.args)
(Pdb)

```

`pdb` 記錄它在哪裡停止執行以及將要執行哪一行（在我們的例子中，`obj = self.search(self.args)`），並詢問您想要做什麼。

(listing-surrounding-lines-of-code)=
### 列出周圍的程式碼行

當出現 `pdb` 提示字元 `(Pdb)` 時，您可以鍵入不同的指令來探索程式碼。  您應該知道的第一個是 `list`（您可以簡稱為 `l`）：

```
(Pdb) l
 43
 44         key = "test"
 45
 46         def func(self):
 47             from evennia import set_trace; set_trace()   # <--- start of debugger
 48  ->         obj = self.search(self.args)
 49             self.msg("You've found {}.".format(obj.get_display_name()))
 50
 51     # -------------------------------------------------------------
 52     #
 53     # The default commands inherit from
(Pdb)
```

好吧，這並沒有做任何引人注目的事情，但是當您對 `pdb` 更加自信並發現自己處於許多不同的檔案中時，您有時需要檢視程式碼中的內容。  請注意，在即將執行的行之前有一個小箭頭 (`->`)。

這很重要：**即將**，而不是**剛剛**。  您需要告訴 `pdb` 繼續（我們很快就會看到如何進行）。

(examining-variables)=
### 檢查變數

`pdb` 允許您檢查變數（或實際上，執行任何 Python 指令）。  瞭解特定行的變數值非常有用。  要檢視變數，只需鍵入其名稱（就像在 Python 直譯器中一樣：

```
(Pdb) self
<commands.command.CmdTest object at 0x045A0990>
(Pdb) self.args
u''
(Pdb) self.caller
<Character: XXX>
(Pdb)
```

如果您嘗試檢視變數 `obj`，您將收到錯誤：

```
(Pdb) obj
*** NameError: name 'obj' is not defined
(Pdb)
```

這個數字是這樣的，因為此時我們還沒有建立變數。

> 以這種方式檢查變數是非常強大的。  您甚至可以執行 Python 程式碼並繼續
> 執行，當您識別出問題時，這可以幫助檢查您的修復是否確實有效
> 錯誤。  如果您的變數名稱將與 `pdb` 指令衝突（例如 `list`
> 變數），您可以在變數前加上 `!` 字首，以告訴 `pdb` 接下來是 Python 程式碼。

(executing-the-current-line)=
### 執行目前行

現在是我們要求 `pdb` 執行目前行的時候了。為此，請使用 `next` 指令。  你可以
只需輸入 `n` 即可縮短它：

```
(Pdb) n
AttributeError: "'CmdTest' object has no attribute 'search'"
> .../mygame/commands/command.py(79)func()
-> obj = self.search(self.args)
(Pdb)
```

`Pdb` 抱怨您嘗試在指令上呼叫 `search` 方法...而指令上沒有 `search` 方法。  執行指令的字元位於 `self.caller` 中，因此我們可以更改行：

```python
obj = self.caller.search(self.args)
```

(letting-the-program-run)=
### 讓程式執行

`pdb` 正在等待執行相同的指令...它引發了錯誤，但已準備好重試，以防萬一。  理論上我們已經修復了，但是需要重新載入，所以需要輸入指令。  要告訴 `pdb` 終止並繼續執行程式，請使用 `continue`（或 `c`）指令：

```
(Pdb) c
...
```

您看到一個錯誤被捕獲，這就是我們已經修復的錯誤......或者希望有的錯誤。  讓我們重新載入遊戲並重試。您需要再次執行 `evennia istart`，然後執行 `test` 才能再次進入該指令。

```
> .../mygame/commands/command.py(79)func()
-> obj = self.caller.search(self.args)
(Pdb)

```

`pdb` 即將再次執行該線路。

```
(Pdb) n
> .../mygame/commands/command.py(80)func()
-> self.msg("You've found {}.".format(obj.get_display_name()))
(Pdb)
```

這次線路執行沒有錯誤。  讓我們看看 `obj` 變數中有什麼：

```
(Pdb) obj
(Pdb) print obj
None
(Pdb)
```

我們輸入了不含引數的`test`指令，所以在搜尋中找不到物件
（`self.args` 是空字串）。

讓我們允許指令繼續並嘗試使用物件名稱作為引數（儘管我們應該
也修復這個錯誤，那就更好了）：

```
(Pdb) c
...
```

請注意，這次您將在遊戲中遇到錯誤。  讓我們嘗試使用有效的引數。  我在這個房間裡還有另一個角色，`barkeep`：

```test barkeep```

And again, the command freezes, and we have the debugger opened in the console. 

Let's execute this line right away:

```
> .../mygame/commands/command.py(79)func()
-> 物件 = self.caller.search(self.args)
(Pdb) n
> .../mygame/commands/command.py(80)func()
-> self.msg("您已找到 {}。".format(obj.get_display_name()))
(Pdb) 物件
<Character: barkeep>
（資料庫）
```

At least this time we have found the object.  Let's process...

```
(Pdb) n
TypeError: 'get_display_name() 恰好需要 2 個引數（給定 1 個）'
> .../mygame/commands/command.py(80)func()
-> self.msg("您找到了 {}。".format(obj.get_display_name()))
（資料庫）
```

As an exercise, fix this error, reload and run the debugger again.  Nothing better than some experimenting!

Your debugging will often follow the same strategy:

1. Receive an error you don't understand.
2. Put a breaking point **BEFORE** the error occurs.
3. Run `evennia istart`
4. Run the code again and see the debugger open.
5. Run the program line by line, examining variables, checking the logic of instructions.
6. Continue and try again, each step a bit further toward the truth and the working feature.

## Cheat-sheet of pdb/pudb commands

PuDB and Pdb share the same commands. The only real difference is how it's presented. The `look`
command is not needed much in `pudb` since it displays the code directly in its user interface.

| Pdb/PuDB command | To do what |
| ----------- | ---------- |
| list (or l) | List the lines around the point of execution (not needed for `pudb`, it will show
this directly). |
| print (or p) | Display one or several variables. |
| `!` | Run Python code (using a `!` is often optional). |
| continue (or c) | Continue execution and terminate the debugger for this time. |
| next (or n) | Execute the current line and goes to the next one. |
| step (or s) | Step inside of a function or method to examine it. |
| `<RETURN>` | Repeat the last command (don't type `n` repeatedly, just type it once and then press
`<RETURN>` to repeat it). |

If you want to learn more about debugging with Pdb, you will find an [interesting tutorial on that topic here](https://pymotw.com/3/pdb/).

## Debugging with debugpy

If you use Visual Studio Code and would like to debug Evennia using a graphical debugger, please follow the instructions here:

[debugpy contrib](https://github.com/evennia/evennia/tree/main/evennia/contrib/utils/debugpy)