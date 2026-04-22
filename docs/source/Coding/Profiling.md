(profiling)=
# 分析

```{important}
這被認為是一個高階主題。它主要是伺服器開發人員感興趣的。
```

有時，嘗試確定特定程式碼的效率，或弄清楚是否可以比實際速度更快，可能會很有用。有很多方法可以測試Python和執行伺服器的效能。

在深入研究本節之前，請記住 Donald Knuth 的[智慧之言](https://en.wikipedia.org/wiki/Program_optimization#When_to_optimize)：

> *[...]大約 97% 的時間：過早的最佳化是萬惡之源*。

也就是說，在您真正確定需要這樣做之前，不要開始嘗試最佳化程式碼。這意味著在開始考慮最佳化之前，您的程式碼必須實際執行。  最佳化通常還會使您的程式碼變得更加複雜且難以閱讀。考慮可讀性和可維護性，您可能會發現速度的微小提升是不值得的。

(simple-timer-tests)=
## 簡單的定時器測試

Python 的 `timeit` 模組非常適合測試小東西。例如，在
為了測試使用 `for` 迴圈或清單理解是否更快
可以使用以下程式碼：

```python
    import timeit
    # Time to do 1000000 for loops
    timeit.timeit("for i in range(100):\n    a.append(i)", setup="a = []")
   <<< 10.70982813835144
    # Time to do 1000000 list comprehensions
    timeit.timeit("a = [i for i in range(100)]")
   <<<  5.358283996582031
```

`setup` 關鍵字用於設定不應包含在時間測量中的內容，例如第一次呼叫中的`a = []`。

預設情況下，`timeit` 函式將重新執行給定測試 1000000 次並傳回執行此操作的*總時間*（因此*不是*每個測試的平均值）。提示是不要使用此預設值來測試包含資料庫寫入的內容 - 為此，您可能想要使用 `number=100` 關鍵字來使用較少的重複次數（例如 100 或 1000）。

在上面的範例中，我們看到使用清單理解的呼叫次數大約是使用 `.append()` 建立清單的兩倍。

(using-cprofile)=
## 使用cProfile

Python 附帶自己的分析器，名為 cProfile（這是針對 cPython 的，目前尚未使用 `pypy` 進行任何測試）。由於 Evennia 程式的處理方式，使用正常方式啟動探查器 (`python -m cProfile evennia.py`) 是沒有意義的。相反，您可以透過啟動器啟動分析器：

    evennia --profiler start

這將啟動 Evennia，伺服器元件在 cProfile 下運作（以守護程式模式）。您可以嘗試使用 `--profile` 和 `portal` 引數來分析 Portal（然後您需要[單獨啟動伺服器](../Setup/Running-Evennia.md)）。

請注意，當分析器執行時，您的程式將使用比平常更多的記憶體。  隨著時間的推移，記憶體使用量甚至可能會攀升。因此，不要讓它永久執行，而是要仔細監視它（例如在 Linux 上使用 `top` 指令或在 Windows 上使用工作管理員的記憶體顯示）。

一旦您執行伺服器一段時間，您需要停止它，以便探查器可以提供其報告。  請勿從工作管理員終止程式或透過向其傳送終止訊號來終止程式 -​​ 這很可能也會擾亂分析器。相反，可以使用 `evennia.py stop` 或（這可能更好），在遊戲內部使用 `@shutdown`。

一旦伺服器完全關閉（這可能比平常慢很多），您會發現探查器建立了一個新檔案`mygame/server/logs/server.prof`。

(analyzing-the-profile)=
### 分析個人資料

`server.prof` 檔案是二進位檔案。有許多方法可以分析和顯示其內容，所有這些方法僅在 Linux 中進行了測試（如果您是 Windows/Mac 使用者，請告訴我們哪些方法有效）。

您可以在 evennia shell 中使用 Python 內建的 `pstats` 模組檢視設定檔的內容（建議您先在 virtualenv 中安裝 `ipython` 和 `pip install ipython`，以獲得更漂亮的輸出）：

    evennia shell

然後在殼裡

```python
import pstats
from pstats import SortKey

p = pstats.Stats('server/log/server.prof')
p.strip_dirs().sort_stats(-1).print_stats()

```

有關詳細資訊，請參閱[Python 分析檔案](https://docs.python.org/3/library/profile.html#instant-user-s-manual)。

您也可以透過多種方式視覺化資料。
- [Runsnake](https://pypi.org/project/RunSnakeRun/) 將設定檔視覺化
給出一個很好的概述。使用 `pip install runsnakerun` 安裝。請注意，這
  可能需要 C 編譯器且安裝速度相當慢。
- 如需更詳細的使用時間列表，您可以使用
[KCachegrind](http://kcachegrind.sourceforge.net/html/Home.html)。使
  KCachegrind 使用 Python 設定檔案，您還需要包裝器 script
  [pyprof2calltree](https://pypi.python.org/pypi/pyprof2calltree/)。你可以獲得
  `pyprof2calltree` 透過 `pip` 而 KCacheGrind 是你需要得到的東西
  透過您的套件管理器或其主頁。

如何分析和解釋分析資料並不是一個小問題，這取決於您分析的目的。 Evennia 作為非同步伺服器也會使分析變得混亂。在郵件清單中詢問您是否需要協助，並準備好提供您的 `server.prof` 檔案以供比較，以及取得該檔案的確切條件。

(the-dummyrunner)=
## 假跑者

如果遊戲中沒有玩家，則很難測試「實際」遊戲效能。因此 Evennia 隨 *Dummyrunner* 系統一起提供。 Dummyrunner 是一個壓力測試系統：一個單獨的程式，可以使用模擬玩家（又稱「機器人」或「假人」）登入您的遊戲。連線後，這些假人將半隨機地從可能的操作清單中執行各種任務。  使用 `Ctrl-C` 停止 Dummyrunner。

```{warning}

    You should not run the Dummyrunner on a production database. It
    will spawn many objects and also needs to run with general permissions.

這是使用虛擬跑步者的推薦流程：
```

1. 使用 `evennia stop` 完全停止你的伺服器。
1. 在 `mygame/server/conf.settings.py` 檔案的末尾新增以下行

        from evennia.server.profiling.settings_mixin import *

這將覆蓋您的設定並停用 Evennia 的速率限制器和 DoS 保護，否則將阻止來自 1IP 的大量連線使用者端。值得注意的是，它還將更改為不同的（更快的）密碼雜湊器。
1. （建議）：建立一個新的資料庫。如果您使用預設的 Sqlite3 並且想要
保留現有資料庫，只需將 `mygame/server/evennia.db3` 重新命名為
   `mygame/server/evennia.db3_backup` 並執行 `evennia migrate` 和 `evennia
   start` 像往常一樣建立一個新的超級使用者。
1. （推薦）以超級使用者登入遊戲。這正是你
可以手動檢查響應。如果您保留舊資料庫，您將_不會_
   由於密碼雜湊器更改，能夠與_現有_使用者連線！
1. 從終端啟動 10 個虛擬使用者的 dummyrunner

        evennia --dummyrunner 10

使用`Ctrl-C`（或`Cmd-C`）來停止它。

如果您想檢視虛擬機器實際上在做什麼，您可以使用單一虛擬機器執行：

    evennia --dummyrunner 1

然後將列印虛擬機器的輸入/輸出。預設情況下，跑步者使用“looker”設定檔案，該設定檔案僅登入並一遍又一遍地傳送“look”指令。要更改設定，請將檔案 `evennia/server/profiling/dummyrunner_settings.py` 複製到您的 `mygame/server/conf/` 目錄，然後將此行新增到您的設定檔案中以在新位置使用它：

    DUMMYRUNNER_SETTINGS_MODULE = "server/conf/dummyrunner_settings.py"

dummyrunner 設定檔本身就是一個 Python 程式碼模組 - 它定義了傻瓜可用的操作。這些只是指令字串的元組（例如“看這裡”），供虛擬物件傳送到伺服器以及它們發生的機率。 dummyrunner 尋找全域變數 `ACTIONS`，這是一個元組列表，其中前兩個元素定義用於登入/登出伺服器的指令。

以下是簡化的最小設定（預設設定檔新增了更多功能和資訊）：

```python
# minimal dummyrunner setup file

# Time between each dummyrunner "tick", in seconds. Each dummy will be called
# with this frequency.
TIMESTEP = 1

# Chance of a dummy actually performing an action on a given tick. This
# spreads out usage randomly, like it would be in reality.
CHANCE_OF_ACTION = 0.5

# Chance of a currently unlogged-in dummy performing its login action every
# tick. This emulates not all accounts logging in at exactly the same time.
CHANCE_OF_LOGIN = 0.01

# Which telnet port to connect to. If set to None, uses the first default
# telnet port of the running server.
TELNET_PORT = None

# actions

def c_login(client):
    name = f"Character-{client.gid}"
    pwd = f"23fwsf23sdfw23wef23"
    return (
        f"create {name} {pwd}"
        f"connect {name} {pwd}"
    )

def c_logout(client):
    return ("quit", )

def c_look(client):
    return ("look here", "look me")

# this is read by dummyrunner.
ACTIONS = (
    c_login,
    c_logout,
    (1.0, c_look)   # (probability, command-generator)
)

```

預設檔案的底部是一些預設設定檔案，您只需將 `PROFILE` 變數設定為選項之一即可測試。

(dummyrunner-hints)=
### 虛擬跑者提示

- 不要從太多的假人開始。 Dummyrunner 對伺服器的負擔更大
比「真實」使用者傾向於做的事情。從 10-100 開始。
- 壓力測試可能很有趣，但也要考慮「現實」的數量
使用者會喜歡你的遊戲。
- 請注意 dummyrunner 輸出中有多少指令被傳送到
伺服器由所有傻瓜組成。這通常比你想要的要高得多
  實際上期望看到相同數量的使用者。
- 預設設定設定“滯後”測量來測量迂迴
留言時間。平均每 30 秒更新一次。值得
  在新增之前，在一個終端機中為少量虛擬機器執行此程式
  更多透過在另一個終端啟動另一個 dummyrunner - 第一個將
  衡量滯後如何隨不同負載變化。還要驗證
  透過在遊戲中手動輸入指令來減少延遲時間。
- 使用 `top/htop` (linux) 檢查伺服器的 CPU 使用情況。在遊戲中，使用
`server`指令。
- 您可以使用 `--profiler start` 執行伺服器來使用虛擬機器進行測試。筆記
分析器本身會影響伺服器效能，尤其是記憶體
  消費。
- 一般來說，dummyrunner 系統可以對一般的測試進行不錯的測試
表現;但實際上模仿人類使用者的行為當然很難。
  為此，需要進行實際的真實遊戲測試。

