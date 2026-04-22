(scripts)=
# Scripts

[Script API參考](evennia.scripts.scripts)

*Scripts* 是字元內[物件](./Objects.md) 的非字元同級。 Scripts 是如此靈活，以至於名稱「Script」本身就有點限制 - 但我們必須選擇_一些東西_來命名它們。其他可能的名稱（取決於您的用途）為 `OOBObjects`、`StorageContainers` 或 `TimerObjects`。

如果您曾經考慮建立一個帶有 `None` 位置的 [物件](./Objects.md) 只是為了儲存一些遊戲資料，那麼您確實應該使用 Script。

- Scripts 是完整的[型別分類](./Typeclasses.md) 實體 - 它們具有[屬性](./Attributes.md) 並且可以以相同的方式進行修改。但它們_在遊戲中不存在_，因此沒有像[物件](./Objects.md)這樣的位置或指令執行，也沒有像[帳號](./Accounts.md)那樣與特定玩家/session的連線。這意味著它們非常適合充當遊戲_系統_的資料庫儲存後端：儲存當前的經濟狀態、誰參與了當前的戰鬥、追蹤正在進行的以物易物等等。它們非常適合作為持久系統處理程式。
- Scripts 有一個可選的_計時器元件_。這意味著你可以設定script以一定的時間間隔勾選Script上的`at_repeat`鉤子。定時器可以根據需要獨立於script的其餘部分進行控制。該元件是可選的，並且是 Evennia 中其他計時函式的補充，例如 [evennia.utils.delay](evennia.utils.utils.delay) 和 [evennia.utils.repeat](evennia.utils.utils.repeat)。
- Scripts 可以透過 e.g_附加_到物件和帳戶。 `obj.scripts.add/remove`。在 script 中，您可以以 `self.obj` 或 `self.account` 的身分存取物件/帳戶。這可以用來動態擴充其他typeclasses，也可以使用計時器元件以各種方式影響父物件。由於歷史原因，未附加到物件的 Script 稱為_Global_ Script。

```{versionchanged} 1.0
   In previous Evennia versions, stopping the Script's timer also meant deleting the Script object.
   Starting with this version, the timer can be start/stopped separately and `.delete()` must be called
   on the Script explicitly to delete it.

```

(working-with-scripts)=
## 與 Scripts 一起工作

有兩個主要指令控制預設cmdset中的scripts：

`addscript` 指令用於將 scripts 附加到現有物件：

    > addscript obj = bodyfunctions.BodyFunctions

`scripts`指令用於檢視所有scripts並對其進行操作：

    > scripts
    > scripts/stop bodyfunctions.BodyFunctions
    > scripts/start #244
    > scripts/pause #11
    > scripts/delete #566

```{versionchanged} 1.0
The `addscript` command used to be only `script` which was easy to confuse with `scripts`.
```

(code-examples)=
### 程式碼範例

以下是在程式碼中使用 Scripts 的一些範例（稍後將詳細介紹
部分）。

創造一個新的script：
```python
new_script = evennia.create_script(key="myscript", typeclass=...)
```

使用計時器元件建立 script：

```python
# (note that this will call `timed_script.at_repeat` which is empty by default)
timed_script = evennia.create_script(key="Timed script",
                                     interval=34,  # seconds <=0 means off
                                     start_delay=True,  # wait interval before first call
                                     autostart=True)  # start timer (else needing .start() )

# manipulate the script's timer
timed_script.stop()
timed_script.start()
timed_script.pause()
timed_script.unpause()
```

將script附加到另一個物件：

```python
myobj.scripts.add(new_script)
myobj.scripts.add(evennia.DefaultScript)
all_scripts_on_obj = myobj.scripts.all()
```

以各種方式搜尋/尋找 scripts：

```python
# regular search (this is always a list, also if there is only one match)
list_of_myscripts = evennia.search_script("myscript")

# search through Evennia's GLOBAL_SCRIPTS container (based on
# script's key only)
from evennia import GLOBAL_SCRIPTS

myscript = GLOBAL_SCRIPTS.myscript
GLOBAL_SCRIPTS.get("Timed script").db.foo = "bar"
```

刪除Script（這也會停止其計時器）：

```python
new_script.delete()
timed_script.delete()
```

(defining-new-scripts)=
### 定義新的Scripts

Script 被定義為一個類，其建立方式與其他類相同
[型分類](./Typeclasses.md) 個實體。父類是`evennia.DefaultScript`。


(simple-storage-script)=
#### 簡單儲存script

`mygame/typeclasses/scripts.py` 中是已設定的空 `Script` 類。你
可以使用它作為您自己的 scripts 的基礎。

```python
# in mygame/typeclasses/scripts.py

from evennia import DefaultScript

class Script(DefaultScript):
    # stuff common for all your scripts goes here

class MyScript(Script):
    def at_script_creation(self):
        """Called once, when script is first created"""
        self.key = "myscript"
        self.db.foo = "bar"

```

建立後，這個簡單的 Script 可以充當全域儲存：

```python
evennia.create_script('typeclasses.scripts.MyScript')

# from somewhere else

myscript = evennia.search_script("myscript").first()
bar = myscript.db.foo
myscript.db.something_else = 1000

```

請注意，如果將關鍵字引數指定為 `create_script`，則可以覆寫這些值
您在 `at_script_creation` 中設定：

```python

evennia.create_script('typeclasses.scripts.MyScript', key="another name",
                      attributes=[("foo", "bar-alternative")])


```

有關建立和尋找 Scripts 的更多選項，請參閱 [create_script](evennia.utils.create.create_script) 和 [search_script](evennia.utils.search.search_script) API 檔案。

(timed-script)=
#### 定時Script

可以在 Script 上設定多個屬性來控制其計時器元件。

```python
# in mygame/typeclasses/scripts.py

class TimerScript(Script):

    def at_script_creation(self):
        self.key = "myscript"
        self.desc = "An example script"
        self.interval = 60  # 1 min repeat

    def at_repeat(self):
        # do stuff every minute

```

此範例將每分鐘呼叫 `at_repeat`。 `create_script` 函式有 `autostart=True` 關鍵字
預設設定 - 這表示 script 的計時器元件將自動啟動。否則
`.start()` 必須單獨呼叫。

支援的屬性有：

- `key` (str)：script 的名稱。這樣以後要查詢起來就更容易了。如果是script
附加到另一個物件上，也可以從該物件上取得所有 scripts 並以這種方式取得 script。
- `desc` (str)：注意 - 不是 `.db.desc`！這是 script 清單中顯示的 Script 上的資料庫欄位
幫助辨識什麼作用。
- `interval` (int)：計時器每次「滴答」之間的時間量（以秒為單位）。注意
在文字遊戲中使用亞秒計時器通常是不好的做法 - 玩家會
  無法欣賞其精確度（如果您列印它，它只會在螢幕上產生垃圾郵件）。對於
  你幾乎總是可以按需進行計算，或者以更慢的時間間隔進行計算，而玩家並不知情。
- `start_delay` (bool)：計時器是否應立即啟動或先等待 `interval` 秒。
- `repeats` (int)：如果>0，計時器在停止之前只會運作這麼多次。否則
重複次數是無限的。如果設定為 1，Script 會模仿 `delay` 操作。
- `persistent` (bool)：預設為 `True`，表示計時器將在伺服器重新載入/重新啟動後繼續存在。
如果沒有，重新載入將使計時器回到停止狀態。將其設為 `False` _不會_
  刪除 Script 物件本身（為此使用 `.delete()`）。

計時器元件由 Script 類別上的方法控制：

- `.at_repeat()` - 當計時器啟動時，此方法每 `interval` 秒呼叫一次
積極的。
- `.is_valid()` - 此方法由計時器在 `at_repeat()` 之前呼叫。如果返回`False`
計時器立即停止。
- `.start()` - 啟動/更新計時器。如果給予關鍵字引數，它們可用於
動態變更 `interval`、`start_delay` 等。這呼叫 `.at_start()` 鉤子。
  假設計時器之前沒有停止，這也會在伺服器重新載入後呼叫。
- `.update()` - `.start` 的舊別名。
- `.stop()` - 停止並重設計時器。這呼叫了 `.at_stop()` 鉤子。
- `.pause()` - 將計時器暫停在目前位置，儲存其目前位置。這呼叫
`.at_pause(manual_pause=True)` 鉤子。這也在伺服器重新載入/重新啟動時呼叫，
  此時`manual_pause` 將變為`False`。
- `.unpause()` - 取消暫停前暫停的script。這將呼叫 `at_start` 掛鉤。
- `.time_until_next_repeat()` - 取得計時器下次觸發之前的時間。
- `.remaining_repeats()` - 取得剩餘的重複次數，如果重複次數無限，則取得 `None`。
- `.reset_callcount()` - 這會將重複計數器重設為從 0 開始。僅在 `repeats>0` 時有用。
- `.force_repeat()` - 這會過早強制立即呼叫 `at_repeat`。這樣做將重置倒數計時，以便下一次呼叫將在 `interval` 秒後再次發生。

(script-timers-vs-delayrepeat)=
### Script計時器與延遲/重複

如果_only_目標是獲得重複/延遲效果，則通常應先考慮 [evennia.utils.delay](evennia.utils.utils.delay) 和 [evennia.utils.repeat](evennia.utils.utils.repeat) 函式。 Script 對於動態建立/刪除來說「更重」。事實上，對於進行單一延遲呼叫 (`script.repeats==1`)，`utils.delay` 呼叫可能始終是更好的選擇。

對於重複任務，`utils.repeat` 針對快速重複大量物件進行了最佳化。它在底層使用了TickerHandler。其基於訂閱的模型使得啟動/停止物件的重複操作變得非常有效。然而，副作用是所有設定為以給定時間間隔滴答的物件都會_全部同時這樣做_。根據具體情況，這在遊戲中可能看起來很奇怪，也可能不奇怪。相比之下，Script 使用自己的股票程式碼，該股票程式碼將獨立於所有其他 Scripts 的股票程式碼執行。

另外值得注意的是，一旦 script 物件已_已建立_，啟動/停止/暫停/取消暫停計時器的開銷非常小。 script 的暫停/取消暫停和更新方法也提供了比使用 `utils.delays/repeat` 更精細的控制。

(script-attached-to-another-object)=
### Script 附加到另一個物件

Scripts 可以附加到[帳戶](./Accounts.md) 或（更常見）[物件](./Objects.md)。
如果是這樣，「父物件」將作為 `.obj` 或 `.account` 可供 script 使用。


```python
    # mygame/typeclasses/scripts.py
    # Script class is defined at the top of this module

    import random

    class Weather(Script):
        """
        A timer script that displays weather info. Meant to
        be attached to a room.

        """
        def at_script_creation(self):
            self.key = "weather_script"
            self.desc = "Gives random weather messages."
            self.interval = 60 * 5  # every 5 minutes

        def at_repeat(self):
            "called every self.interval seconds."
            rand = random.random()
            if rand < 0.5:
                weather = "A faint breeze is felt."
            elif rand < 0.7:
                weather = "Clouds sweep across the sky."
            else:
                weather = "There is a light drizzle of rain."
            # send this message to everyone inside the object this
            # script is attached to (likely a room)
            self.obj.msg_contents(weather)
```

如果連線到一個房間，這個Script會隨機報告一些天氣
每 5 分鐘向房間中的每個人傳送一次。

```python
    myroom.scripts.add(scripts.Weather)
```

> 請注意，您的遊戲目錄中的 `typeclasses` 將新增到設定 `TYPECLASS_PATHS` 中。
> 因此我們不需要給出完整路徑（`typeclasses.scripts.Weather`
> 但上面只有`scripts.Weather`。

您還可以在建立它時附加 script：

```python
    create_script('typeclasses.weather.Weather', obj=myroom)
```

(other-script-methods)=
### 其他Script方法

Script 具有型別分類物件的所有屬性，例如 `db` 和 `ndb`（請參閱
[Typeclasses](./Typeclasses.md))。設定 `key` 對於管理 scripts 很有用（按名稱刪除它們）
等）。這些通常設定在 Script 的 typeclass 中，但也可以動態分配為
`evennia.create_script` 的關鍵字引數。

- `at_script_creation()` - 僅在首次建立 script 時呼叫一次。
- `at_server_reload()` - 每當伺服器熱重啟時都會呼叫此函式（e.g。使用 `reload` 指令）。這是儲存您可能希望在重新載入後繼續存在的非永續性資料的好地方。
- `at_server_shutdown()` - 當呼叫系統重設或系統關閉時呼叫此函式。
- `at_server_start()` - 當伺服器返回時（從重新載入/關閉/重新啟動），將呼叫此函式。當啟動 script 的功能時，它對於非永續性資料的初始化和快取非常有用。
- `at_repeat()`
- `at_start()`
- `at_pause()`
- `at_stop()`
- `delete()` - 與其他型別分類實體相同，這將刪除 Script。值得注意的是
它還會停止計時器（如果它執行），導致呼叫 `at_stop` 鉤子。

此外，Scripts 像其他型別分類實體一樣支援[屬性](./Attributes.md)、[Tags](./Tags.md) 和[鎖定](./Locks.md) 等。

另請參閱上面控制[定時Script](#timed-script)所涉及的方法。

(dealing-with-script-errors)=
### 處理 Script 錯誤

定時執行 script 內的錯誤有時可能相當簡潔，或指向難以解釋的執行機制部分。更容易偵錯 scripts 的一種方法是匯入 Evennia 的本機記錄器並將函式包裝在 try/catch 區塊中。 Evennia 的記錄器可以向您顯示 script 中回溯發生的位置。

```python

from evennia.utils import logger

class Weather(Script):

    # [...]

    def at_repeat(self):

        try:
            # [...]
        except Exception:
            logger.log_trace()
```


(using-global_scripts)=
## 使用GLOBAL_SCRIPTS

未附加到另一個實體的 Script 通常稱為 _Global_ script，因為它不可用
從任何地方訪問。這意味著需要搜尋它們才能使用。

Evennia提供了一個方便的「容器」`evennia.GLOBAL_SCRIPTS`來幫助組織你的全域性
scripts。您所需要的只是 Script 的 `key`。

```python
from evennia import GLOBAL_SCRIPTS

# access as a property on the container, named the same as the key
my_script = GLOBAL_SCRIPTS.my_script
# needed if there are spaces in name or name determined on the fly
another_script = GLOBAL_SCRIPTS.get("another script")
# get all global scripts (this returns a Django Queryset)
all_scripts = GLOBAL_SCRIPTS.all()
# you can operate directly on the script
GLOBAL_SCRIPTS.weather.db.current_weather = "Cloudy"

```

```{warning}
請注意，全域 scripts 根據其 `key` 顯示為 `GLOBAL_SCRIPTS` 上的屬性。如果您要建立兩個具有相同 `key` 的全域 scripts（即使具有不同的 typeclasses），則 `GLOBAL_SCRIPTS` 容器將只傳回其中之一（哪一個取決於資料庫中的順序）。最好的方法是組織好你的scripts，這樣就不會發生這種情況。否則，使用 `evennia.search_script` 來準確獲得您想要的 script。
```

有兩種方法可以使 script 顯示為 `GLOBAL_SCRIPTS` 上的屬性：

1. 使用 `create_script` 手動建立一個新的全域 script 和 `key`。
2. 在 `GLOBAL_SCRIPTS` 設定變數中定義 script 的屬性。這告訴Evennia
它應該檢查帶有 `key` 的 script 是否存在，如果不存在，則為您建立它。
   這對於必須始終存在和/或應該自動建立的 scripts 非常有用
   當你的伺服器重新啟動時。如果您使用此方法，您必須確保所有
   script 鍵是全域唯一的。

以下是告訴 Evennia 管理設定中的 script 的方法：

```python
# in mygame/server/conf/settings.py

GLOBAL_SCRIPTS = {
    "my_script": {
        "typeclass": "typeclasses.scripts.Weather",
        "repeats": -1,
        "interval": 50,
        "desc": "Weather script"
    },
    "storagescript": {}
}
```

上面我們加了兩個scripts，鍵分別為`myscript`和`storagescript`。以下字典可以為空 - 然後將使用 `settings.BASE_SCRIPT_TYPECLASS`。在底層，提供的字典（以及`key`）將自動傳遞到`create_script`，因此這裡支援所有[與create_script相同的關鍵字引數]（evennia.utils.create.create_script）。
```{warning}

在像這樣設定 Evennia 來管理您的 script 之前，請確保您的 Script typeclass 沒有任何嚴重錯誤（單獨測試）。如果有，您將在日誌中看到錯誤，並且 Script 將暫時回退為 `DefaultScript` 型別。
```

此外，當您嘗試訪問它時，以這種方式定義的script*保證*存在：

```python
from evennia import GLOBAL_SCRIPTS
# Delete the script
GLOBAL_SCRIPTS.storagescript.delete()
# running the `scripts` command now will show no storagescript
# but below it's automatically recreated again!
storage = GLOBAL_SCRIPTS.storagescript
```

也就是說，如果script被刪除，下次從`GLOBAL_SCRIPTS`取得它時，Evennia會使用
設定中的資訊以便您即時重新建立它。


