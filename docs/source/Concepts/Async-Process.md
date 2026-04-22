(async-process)=
# 非同步程式


```{important}
這被認為是一個高階主題。
```

(synchronous-versus-asynchronous)=
## 同步與非同步

```{sidebar}
[指令持續時間教學](../Howtos/Howto-Command-Duration.md) 中也對此進行了探討。
```

大多數程式碼*同步*執行。這意味著程式碼中的每個語句都會在下一個語句開始之前處理並完成。這使得程式碼易於理解。在許多情況下，這也是一個*要求* - 後續的程式碼通常取決於先前語句中計算或定義的內容。

考慮傳統 Python 程式中的這段程式碼：

```python
    print("before call ...")
    long_running_function()
    print("after call ...")
```

執行時，將列印 `"before call..."`，之後 `long_running_function` 開始工作
無論多久。完成後，系統才會列印 `"after call..."`。簡單且合乎邏輯。 Evennia 中的大多數都以這種方式工作，並且通常重要的是指令得到
按照與編碼相同的嚴格順序執行。

Evennia，來自 Twisted，是一個單程式多使用者伺服器。簡單來說，這意味著它在處理玩家輸入之間快速切換，速度如此之快，以至於每個玩家都感覺自己在同時做事。  然而，這是一個聰明的錯覺：如果一個使用者執行一個包含`long_running_function`的指令，*所有*其他玩家實際上被迫等待直到它完成。

現在，應該說在現代電腦系統上這很少是一個問題。很少有指令執行時間長到其他使用者註意到的程度。  如前所述，大多數時候您「希望」強制所有指令按嚴格的順序發生。

(utilsdelay)=
## `utils.delay`

```{sidebar} 延遲（）與time.sleep（）
這相當於 `time.sleep()` ，除了 `delay` 是非同步的，而 `sleep` 會在睡眠期間 lock 整個伺服器。
```
`delay` 函式是 `run_async` 的同級函式，要簡單得多。事實上，這只是將指令的執行延遲到未來某個時間的一種方法。

```python
     from evennia.utils import delay

     # [...]
     # e.g. inside a Command, where `self.caller` is available
     def callback(obj):
        obj.msg("Returning!")
     delay(10, callback, self.caller)
```

這會將回呼的執行延遲 10 秒。提供 `persistent=True` 以使延遲在伺服器 `reload` 中倖存。等待期間可以正常輸入指令。

您也可以嘗試以下程式碼片段，看看它是如何運作的：

    py from evennia.utils import delay; delay(10, lambda who: who.msg("Test!"), self)

等待 10 秒鐘，然後「測試！」應該會回覆給你。


(utilsinteractive-decorator)=
## `@utils.interactive` 裝飾器

`@interactive` [裝飾器](https://realpython.com/primer-on-python- decorators/) 使任何函式或方法都可以以互動方式「暫停」和/或等待玩家輸入。

```python
    from evennia.utils import interactive

    @interactive
    def myfunc(caller):
        
      while True:
          caller.msg("Getting ready to wait ...")
          yield(5)
          caller.msg("Now 5 seconds have passed.")

          response = yield("Do you want to wait another 5 secs?")  

          if response.lower() not in ("yes", "y"):
              break 
```

`@interactive` 裝飾器賦予函式暫停的能力。使用 `yield(seconds)` 就可以做到這一點 - 它將非同步暫停指定的秒數，然後再繼續。從技術上講，這相當於使用 `call_async` 和 5 秒後繼續的回撥。但是帶有 `@interactive` 的程式碼更容易理解一些。

在 `@interactive` 函式中，`response = yield("question")` 問題允許您要求使用者輸入。然後，您可以處理輸入，就像使用 Python `input` 函式一樣。

所有這些使得 `@interactive` 裝飾器非常有用。但它有一些警告。

- 修飾函式/方法/可呼叫函式必須有一個名為 `caller` 的引數。 Evennia 將尋找具有此名稱的引數並將其視為輸入來源。
- 以這種方式裝飾函式會將其變成 Python [生成器](https://wiki.python.org/moin/Generators)。這意味著
    - 您不能使用生成器中的 `return <value>`（只需使用空的 `return` 即可）。要從 `@interactive` 修飾的函式/方法傳回值，您必須使用特殊的 Twisted 函式 `twisted.internet.defer.returnValue`。 Evennia 還可以從 `evennia.utils` 方便使用此功能：
    
    ```python
    from evennia.utils import interactive, returnValue
    
    @interactive
    def myfunc():
    
        # ... 
        result = 10
    
        # this must be used instead of `return result`
        returnValue(result)
    ```


(utilsrun_async)=
## `utils.run_async`

```{warning}
除非你心裡有一個非常明確的目的，否則你不太可能從`run_async`得到預期的結果。值得注意的是，它仍然會與伺服器的其餘部分在同一個執行緒中執行長時間執行的函式。因此，雖然它確實執行非同步，但非常繁重和 CPU- 繁重的操作仍然會阻塞伺服器。因此，不要認為這是一種在不影響伺服器其餘部分的情況下解除安裝繁重操作的方法。
```

當您不關心指令實際完成的順序時，您可以「非同步」執行它。這利用了 `src/utils/utils.py` 中的 `run_async()` 函式：

```python
    run_async(function, *args, **kwargs)
```

其中`function`將與`*args`和`**kwargs`非同步呼叫。例子：

```python
    from evennia import utils
    print("before call ...")
    utils.run_async(long_running_function)
    print("after call ...")
```

現在，執行此程式時，您會發現程式不會等待 `long_running_function` 完成。事實上，您會立即看到 `"before call..."` 和 `"after call..."` 列印出來。長時間執行的函式將在背景執行，您（和其他使用者）可以正常執行。

使用非同步呼叫的一個複雜問題是如何處理該呼叫的結果。如果
`long_running_function` 傳回您需要的值？放置任何行都沒有任何實際意義
呼叫後的程式碼嘗試處理上面 `long_running_function` 的結果 - 正如我們所看到的
`"after call..."` 早在 `long_running_function` 完成之前就已經列印出來了，使得
行對於處理函式中的任何資料毫無意義。相反，人們必須使用*回撥*。

`utils.run_async` 採用不會傳遞到長時間執行的函式中的保留 kwargs：

- `at_return(r)`（*回呼*）在非同步函式（`long_running_function`
上）成功完成。引數 `r` 將是該函式的回傳值（或
  `None`）。

    ```python
        def at_return(r):
            print(r)
    ```

- `at_return_kwargs` - 一個可選字典，將作為關鍵字引數提供給 `at_return` 回呼。
- 如果非同步函式失敗並引發異常，則呼叫 `at_err(e)`（*errback*）。
此異常會傳遞到包裝在 *Failure* 物件 `e` 中的 errback。如果您不提供
  您自己的 errback，Evennia 會自動新增一個，默默地將錯誤寫入 evennia
  日誌。下面是一個 errback 的範例：

```python
        def at_err(e):
            print("There was an error:", str(e))
```

- `at_err_kwargs` - 一個可選字典，將作為關鍵字引數提供給 `at_err`
出錯了。

從 [Command](../Components/Commands.md) 定義內部進行非同步呼叫的範例：

```python
    from evennia import utils, Command

    class CmdAsync(Command):

       key = "asynccommand"
    
       def func(self):     
           
           def long_running_function():  
               #[... lots of time-consuming code  ...]
               return final_value
           
           def at_return_function(r):
               self.caller.msg(f"The final value is {r}")
    
           def at_err_function(e):
               self.caller.msg(f"There was an error: {e}")

           # do the async call, setting all callbacks
           utils.run_async(long_running_function, at_return=at_return_function,
at_err=at_err_function)
```

就是這樣 - 從這裡開始我們可以忘記 `long_running_function` 並繼續做其他需要做的事情。 *每當*完成時，`at_return_function` 函式將被呼叫，最終值將彈出供我們檢視。如果沒有，我們將看到一條錯誤訊息。

> 從技術上講，`run_async` 只是一個圍繞 [Twisted Deferred](https://twistedmatrix.com/documents/9.0.0/core/howto/defer.html) 物件的非常薄且簡化的包裝器；如果沒有提供，包裝器也會設定預設的錯誤回傳。如果您知道自己在做什麼，就沒有什麼可以阻止您繞過實用函式，根據自己的喜好建立更複雜的回撥鏈。