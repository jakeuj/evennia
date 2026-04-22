(coding-utils)=
# 編碼工具


Evennia 附帶了許多實用程式來幫助完成常見的程式設計任務。大多數都可以直接訪問
從平面 API 中，否則您可以在 `evennia/utils/` 資料夾中找到它們。

> 這只是 `evennia/utils` 中工具的一小部分。值得直接瀏覽[目錄](evennia.utils)，特別是[evennia/utils/utils.py](evennia.utils.utils)的內容，以找到更多有用的東西。

(searching)=
## 搜尋中

常見的事情是搜尋物件。最簡單的是使用定義的 `search` 方法
在所有物體上。這將搜尋同一位置和 self 物件內部的物件：

```python
     obj = self.search(objname)
```

最常見的情況是在指揮機構內部。 `obj = self.caller.search(objname)` 將在呼叫者（通常是鍵入指令的角色）`.contents`（他們的「庫存」）和`.location`（他們的「房間」）內部進行搜尋。

指定關鍵字 `global_search=True` 將搜尋擴充套件到涵蓋整個資料庫。此搜尋也將符合別名。您將在預設指令集中找到此功能的多個範例。

如果您需要在程式碼模組中搜尋物件，可以使用下列函式
`evennia.utils.search`。您可以透過快捷方式`evennia.search_*` 存取它們。

```python
     from evennia import search_object
     obj = search_object(objname)
```

- [evennia.search_account](evennia.accounts.manager.AccountDBManager.search_account)
- [evennia.search_object](evennia.objects.manager.ObjectDBManager.search_object)
- [evennia.search(物件)_by_tag](evennia.utils.search.search_tag)
- [evennia.search_script](evennia.scripts.manager.ScriptDBManager.search_script)
- [evennia.search_channel](evennia.comms.managers.ChannelDBManager.search_channel)
- [evennia.search_message](evennia.comms.managers.MsgManager.search_message)
- [evennia.search_help](evennia.help.manager.HelpEntryManager.search_help)

請注意，後面這些方法將始終傳回 `list` 的結果，即使清單有一個或零個條目。

(create)=
## 創造

除了遊戲內建立指令（`@create` 等）之外，您還可以直接在程式碼中建立所有 Evennia 的遊戲實體（例如定義新的建立指令時）。

```python
   import evennia

   myobj = evennia.create_objects("game.gamesrc.objects.myobj.MyObj", key="MyObj")
```

- [evennia.create_account](evennia.utils.create.create_account)
- [evennia.create_object](evennia.utils.create.create_object)
- [evennia.create_script](evennia.utils.create.create_script)
- [evennia.create_channel](evennia.utils.create.create_channel)
- [evennia.create_help_entry](evennia.utils.create.create_help_entry)
- [evennia.create_message](evennia.utils.create.create_message)

每個建立函式都有大量引數來進一步自訂建立的實體。有關詳細資訊，請參閱`evennia/utils/create.py`。

(logging)=
## 記錄

通常，您可以使用 Python `print` 語句來檢視終端機/日誌的輸出。 `print`
語句應該只用於除錯。對於生產輸出，使用 `logger` 它將建立正確的日誌到終端或檔案。

```python
     from evennia import logger
     #
     logger.log_err("This is an Error!")
     logger.log_warn("This is a Warning!")
     logger.log_info("This is normal information")
     logger.log_dep("This feature is deprecated")
```

有一種特殊的日誌訊息型別 `log_trace()` 旨在從回溯內部呼叫 - 這對於將回溯訊息中繼回日誌而不需要它非常有用
殺死伺服器。

```python
     try:
       # [some code that may fail...]
     except Exception:
       logger.log_trace("This text will show beneath the traceback itself.")
```

最後，`log_file` 記錄器是一個非常有用的記錄器，用於輸出任意日誌訊息。這是一種高度最佳化的非同步日誌機制，使用[執行緒](https://en.wikipedia.org/wiki/Thread_%28computing%29)來避免開銷。您應該能夠將它用於非常繁重的自訂日誌記錄，而不必擔心磁碟寫入延遲。

```python
 logger.log_file(message, filename="mylog.log")
```

如果未給予絕對路徑，則日誌檔案將出現在 `mygame/server/logs/` 目錄中。如果該檔案已存在，則會將其追加到其中。與正常 Evennia 日誌格式相同的時間戳記將自動新增至每個條目。  如果未指定檔案名，輸出將寫入檔案 `game/logs/game.log`。

另請參閱[偵錯](../Coding/Debugging.md) 檔案以協助尋找難以捉摸的錯誤。

(time-utilities)=
## 時間公用事業

(game-time)=
### 比賽時間

Evennia 追蹤當前伺服器時間。您可以透過 `evennia.gametime` 快捷方式存取此時間：

```python
from evennia import gametime

# all the functions below return times in seconds).

# total running time of the server
runtime = gametime.runtime()
# time since latest hard reboot (not including reloads)
uptime = gametime.uptime()
# server epoch (its start time)
server_epoch = gametime.server_epoch()

# in-game epoch (this can be set by `settings.TIME_GAME_EPOCH`.
# If not, the server epoch is used.
game_epoch = gametime.game_epoch()
# in-game time passed since time started running
gametime = gametime.gametime()
# in-game time plus game epoch (i.e. the current in-game
# time stamp)
gametime = gametime.gametime(absolute=True)
# reset the game time (back to game epoch)
gametime.reset_gametime()

```

設定 `TIME_FACTOR` 決定了遊戲時間與現實世界相比的快/慢。設定 `TIME_GAME_EPOCH` 設定開始遊戲紀元（以秒為單位）。 `gametime` 模組中的函式均以秒為單位傳回其時間。您可以將其轉換為您想要的遊戲時間單位。您可以使用`@time`指令檢視伺服器時間資訊。 
您也可以使用 [gametime.schedule](evennia.utils.gametime.schedule) 函式*安排*在遊戲中的特定時間發生的事情：

```python
import evennia

def church_clock:
    limbo = evennia.search_object(key="Limbo")
    limbo.msg_contents("The church clock chimes two.")

gametime.schedule(church_clock, hour=2)
```

(utilstime_format)=
### utils.time_format()

此函式需要幾秒鐘的時間作為輸入（e.g。來自上面的`gametime` 模組），並將其轉換為以天、小時等為單位的漂亮文字輸出。當您想要顯示某些內容有多舊時，它非常有用。它使用 *style* 關鍵字轉換為四種不同樣式的輸出：

- 樣式 0 - `5d:45m:12s`（標準冒號輸出）
- 樣式1 - `5d`（僅顯示最長的時間單位）
- 樣式 2 - `5 days, 45 minutes`（完整格式，忽略秒）
- 樣式 3 - `5 days, 45 minutes, 12 seconds`（完整格式，附秒）

(utilsdelay)=
### utils.delay()

這允許延遲呼叫。

```python
from evennia import utils

def _callback(obj, text):
    obj.msg(text)

# wait 10 seconds before sending "Echo!" to obj (which we assume is defined)
utils.delay(10, _callback, obj, "Echo!", persistent=False)

# code here will run immediately, not waiting for the delay to fire!

```

有關詳細資訊，請參閱[非同步程式](../Concepts/Async-Process.md#delay)。

(finding-classes)=
## 尋找課程

(utilsinherits_from)=
### utils.inherits_from()

這個有用的函式有兩個引數 - 一個要檢查的物件和一個父物件。如果物件以任意距離*從父物件繼承，它會傳回 `True`（與 Python 內建的 `is_instance()` 相反，
只會捕獲直接依賴）。此函式也接受以下任意組合作為輸入
類別、例項或 python 類別路徑。

請注意，Python 程式碼通常應與 [鴨子型別](https://en.wikipedia.org/wiki/Duck_typing) 一起使用。但在 Evennia 的情況下，檢查物件是否繼承給定的 [Typeclass](./Typeclasses.md) 作為一種識別方式有時會很有用。舉例來說，我們有一個 typeclass *動物*。它有一個子類別 *Felines*，而它又有一個子類別 *HouseCat*。也許還有許多其他動物型別，例如馬和狗。使用 `inherits_from` 可以讓你一次檢查所有動物：

```python
     from evennia import utils
     if (utils.inherits_from(obj, "typeclasses.objects.animals.Animal"):
        obj.msg("The bouncer stops you in the door. He says: 'No talking animals allowed.'")
```

(text-utilities)=
## 文字實用程式

在文字遊戲中，您自然會做很多來回移動文字的工作。這是一個*非-
`evennia/utils/utils.py` 中找到的完整*文字實用程式選擇（捷徑 `evennia.utils`）。
如果不出意外的話，在開始開發自己的解決方案之前先看看這裡可能會很好。

(utilsfill)=
### utils.fill()

這種洪水將文字填充到給定的寬度（打亂單字以使每行寬度均勻）。它還根據需要縮排。

```python
     outtxt = fill(intxt, width=78, indent=4)
```

(utilscrop)=
### utils.crop()

此函式將裁剪一條很長的線，並新增字尾以顯示該線實際上是連續的。這個
當顯示多行會使事情變得混亂時，在清單中可能很有用。

```python
     intxt = "This is a long text that we want to crop."
     outtxt = crop(intxt, width=19, suffix="[...]")
     # outtxt is now "This is a long text[...]"
```

(utilsdedent)=
### utils.dedent()

這解決了乍看之下似乎是一個微不足道的文字問題——刪除縮排。它用於將整個段落向左移動，而不影響它們可能具有的任何進一步的格式。常見的情況是在程式碼中使用 Python 三引號字串時 - 它們將保留程式碼中的任何縮排，並且為了使原始程式碼易於閱讀，人們通常不希望將字串移動到左邊緣。

```python
    #python code is entered at a given indentation
          intxt = """
          This is an example text that will end
          up with a lot of whitespace on the left.
                    It also has indentations of
                    its own."""
          outtxt = dedent(intxt)
          # outtxt will now retain all internal indentation
          # but be shifted all the way to the left.
```

通常，您會在顯示程式碼中執行縮排（例如，這就是幫助系統同質化的方式）
幫助條目）。

(to_str-and-to_bytes)=
### to_str() 和 to_bytes()

Evennia 提供兩個實用函式來將文字轉換為正確的編碼。 `to_str()` 和 `to_bytes()`。除非您要新增自訂協定並且需要透過線路傳送位元組資料，否則 `to_str` 是您唯一需要的協定。

與 Python 內建 `str()` 和 `bytes()` 運運算元的差異在於 Evennia 使用 `ENCODINGS` 設定，並且會盡力不引發回溯，而是透過日誌記錄回顯錯誤。請參閱[此處](../Concepts/Text-Encodings.md) 以瞭解更多資訊。