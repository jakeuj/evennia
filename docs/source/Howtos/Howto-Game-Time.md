(changing-game-calendar-and-time-speed)=
# 更改比賽日曆和時間速度


許多遊戲使用單獨的時間系統，我們稱之為「遊戲時間」。這與我們通常認為的“實時”並行執行。  遊戲時間可能會以不同的速度執行，使用不同的
其時間單位的名稱，甚至可能使用完全自訂的日曆。您根本不需要依賴遊戲時間系統。但如果您這樣做，Evennia 提供了處理這些不同情況的基本工具。本教學將引導您瞭解這些功能。

(a-game-time-with-a-standard-calendar)=
## 標準日曆的比賽時間

許多遊戲讓他們的遊戲時間比即時執行得更快或更慢，但仍然使用我們的正常時間
現實世界的日曆。這對於以當今為背景的遊戲以及過去的遊戲來說都很常見。
歷史或未來的背景。使用標準日曆有一些優點：

- 處理重複操作要容易得多，因為從即時體驗轉換為即時體驗
遊戲中的感知很容易。
- 現實世界日曆的複雜性，包括閏年和不同長度的月份等
由系統自動處理。

Evennia 的遊戲時間功能採用標準日曆（有關自訂日曆，請參閱下面的相關部分）。

(setting-up-game-time-for-a-standard-calendar)=
### 為標準日曆設定比賽時間

一切都是透過設定完成的。  如果您想玩遊戲，請使用以下設定
標準日曆：

```python
# in a file settings.py in mygame/server/conf
# The time factor dictates if the game world runs faster (timefactor>1)
# or slower (timefactor<1) than the real world.
TIME_FACTOR = 2.0

# The starting point of your game time (the epoch), in seconds.
# In Python a value of 0 means Jan 1 1970 (use negatives for earlier
# start date). This will affect the returns from the utils.gametime
# module.
TIME_GAME_EPOCH = None
```

預設情況下，遊戲時間執行速度是即時時間的兩倍。  您可以將時間係數設為 1（遊戲時間將以與即時完全相同的速度執行）或更低（遊戲時間將比即時慢）。  大多數遊戲選擇讓遊戲時間旋轉得更快（你會發現一些遊戲的時間係數為 60，這意味著遊戲時間比即時時間快 60 倍，即時時間一分鐘將是遊戲時間一小時）。

時代是一個稍微複雜的設定。  它應該包含一些秒數
指示您的遊戲開始的時間。  如前所述，紀元 0 表示 1970 年 1 月 1 日。如果
你想設定未來的時間，你只需要在幾秒鐘內找到起點。  那裡
在 Python 中有多種方法可以實現此目的，此方法將向您展示如何在本機時間執行此操作：

```python
# We're looking for the number of seconds representing
# January 1st, 2020
from datetime import datetime
import time
start = datetime(2020, 1, 1)
time.mktime(start.timetuple())
```

這應該會返回一個巨大的數字 - 自 1970 年 1 月 1 日以來的秒數。將其直接複製到您的設定中（編輯 `server/conf/settings.py`）：

```python
# in a file settings.py in mygame/server/conf
TIME_GAME_EPOCH = 1577865600
```

使用`@reload`重新載入遊戲，然後使用`@time`指令。  你應該會看到類似的東西
這個：

```
+----------------------------+-------------------------------------+
| Server time                |                                     |
+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
| Current uptime             | 20 seconds                          |
| Total runtime              | 1 day, 1 hour, 55 minutes           |
| First start                | 2017-02-12 15:47:50.565000          |
| Current time               | 2017-02-13 17:43:10.760000          |
+----------------------------+-------------------------------------+
| In-Game time               | Real time x 2                       |
+~~~~~~~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
| Epoch (from settings)      | 2020-01-01 00:00:00                 |
| Total time passed:         | 1 day, 17 hours, 34 minutes         |
| Current time               | 2020-01-02 17:34:55.430000          |
+----------------------------+-------------------------------------+
```

這裡最相關的行是遊戲時間紀元。  您會看到它顯示於 2020-01-01。  來自
至此，比賽時間不斷增加。  如果你繼續輸入`@time`，你會看到遊戲
時間更新正確......並且（預設）速度是即時的兩倍。

(time-related-events)=
### 與時間相關的事件

`gametime` 實用程式還有一種方法來安排與遊戲相關的事件，考慮到您的遊戲時間，並假設標準日曆（請參閱下面的自訂日曆的相同功能）。  例如，它可用於在每天（遊戲內）的 6:00 AM 傳送特定訊息，顯示太陽如何升起。

這裡應該使用函式`schedule()`。  它將建立一個具有一些附加功能的 [script](../Components/Scripts.md)，以確保當遊戲時間與給定引數匹配時始終執行 script。

`schedule` 函式採用下列引數：

- *回撥*，時間到時呼叫的函式。
- 關鍵字`repeat`（預設為`False`）指示是否應重複呼叫此函式。
- 其他關鍵字引數 `sec`、`min`、`hour`、`day`、`month` 和 `year` 用於描述計畫時間。  如果未給予該引數，則假定該特定單位的目前時間值。

這是讓太陽每天升起的一個簡短範例：

```python
# in a file ingame_time.py in mygame/world/

from evennia.utils import gametime
from typeclasses.rooms import Room

def at_sunrise():
    """When the sun rises, display a message in every room."""
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("The sun rises from the eastern horizon.")

def start_sunrise_event():
    """Schedule an sunrise event to happen every day at 6 AM."""
    script = gametime.schedule(at_sunrise, repeat=True, hour=6, min=0, sec=0)
    script.key = "at sunrise"
```

如果你想測試這個功能，你可以輕鬆地執行以下操作：

```
@py from world import ingame_time; ingame_time.start_sunrise_event()
```

script 將被靜默建立。 `at_sunrise` 函式現在將在遊戲中的每個日呼叫
6AM。可以使用`@scripts`指令來檢視。您可以使用 `@scripts/stop` 來停止它。如果
我們沒有設定`repeat`，太陽只會升起一次，然後就不會再升起。

我們在這裡使用了 `@py` 指令：沒有什麼可以阻止您將系統新增到遊戲程式碼中。但請記住，不要在啟動時新增每個事件，否則在太陽升起時會安排許多重疊的事件。

當使用設定為 `True` 的 `repeat` 時，`schedule` 函式適用於較高的、未指定的單位。
在我們的範例中，我們指定了小時、分鐘和秒。  我們沒有指定的較高單位是
day: `schedule` 假設我們的意思是「每天在指定時間執行回呼」。  因此，你
可以有一個每小時 HH:30 執行的事件，或每月第 3 天執行的事件。

> 請注意每月或每年重複 scripts：由於
現實生活中的日曆在安排月末或年末的活動時需要小心。
例如，如果您將 script 設定為每月 31 號執行，它將在一月執行，但找不到
二月、四月等的這一天。同樣，閏年可能會改變一年中的天數。

(a-game-time-with-a-custom-calendar)=
### 帶有自訂日曆的遊戲時間

如果您想將遊戲置於虛構的宇宙中，有時需要使用自訂日曆來處理遊戲時間。  例如，您可能想要建立託爾金所描述的夏爾曆，有 12 個月，每個月 30 天。這樣一來，一年只有 360 天（大概哈比人並不真正喜歡遵循天文日曆的麻煩）。  另一個例子是在不同的太陽系中創造一顆行星，例如，白天長 29 小時，月份只有 18 天。

Evennia 透過選購的 *contrib* 模組（稱為 `custom_gametime`）處理自訂日曆。
與上述正常的 `gametime` 模組相反，它預設不處於活動狀態。

(setting-up-the-custom-calendar)=
### 設定自訂日曆

在託爾金書中哈比人使用的夏爾日曆的第一個例子中，我們實際上並不需要周的概念……但我們需要有 30 天而不是 28 天的月份的概念。

自訂日曆是透過將 `TIME_UNITS` 設定新增至您的設定檔來定義的。它是一個字典，其中包含單位名稱作為鍵，以及該單位中的秒數（我們的最小單位）作為值。它的鍵必須從以下選項中選擇：“秒”、“分鐘”、“小時”、“日”、“週”、“月”和“年”，但不必全部包含。  以下是 Shire 日曆的設定：

```python
# in a file settings.py in mygame/server/conf
TIME_UNITS = {"sec": 1,
              "min": 60,
              "hour": 60 * 60,
              "day": 60 * 60 * 24,
              "month": 60 * 60 * 24 * 30,
              "year": 60 * 60 * 24 * 30 * 12 }
```

我們將我們想要的每個單位作為金鑰。  值表示該單位的秒數。  小時設定為60 * 60（即每小時3600秒）。  請注意，我們在此設定中沒有指定週單位：相反，我們直接從天跳到月。

為了使此設定正常工作，請記住所有單位都必須是先前單位的倍數。  例如，如果您建立“日”，則它需要是多個小時。

因此，對於我們的範例，我們的設定可能如下所示：

```python
# in a file settings.py in mygame/server/conf
# Time factor
TIME_FACTOR = 4

# Game time epoch
TIME_GAME_EPOCH = 0

# Units
TIME_UNITS = {
        "sec": 1,
        "min": 60,
        "hour": 60 * 60,
        "day": 60 * 60 * 24,
        "month": 60 * 60 * 24 * 30,
        "year": 60 * 60 * 24 * 30 * 12,
}
```

請注意，我們已將時間紀元設定為 0。使用自訂日曆，我們將自己設計出漂亮的時間顯示。在我們的例子中，遊戲時間從第 0 年、第 1 月、第 1 天和午夜開始。

> 年、時、分、秒從0開始，月、週、日從1開始，這使得它們
> 行為與標準時間一致。

請注意，雖然我們在設定中使用「月」、「週」等，但您的遊戲可能不會在遊戲中使用這些術語，而是將它們稱為「週期」、「月亮」、「沙落」等。這只是您的問題
以不同的方式顯示它們。請參閱下一節。

(a-command-to-display-the-current-game-time)=
#### 顯示當前遊戲時間的指令

如前所述，`@time` 指令旨在與標準日曆一起使用，而不是與自訂日曆一起使用。  不過我們可以輕鬆建立一個新指令。  我們稱之為`time`，就像通常的情況一樣
其他MU*。  這是我們如何編寫它的範例（例如，您可以建立一個檔案
`gametime.py` 在您的 `commands` 目錄中並將此程式碼貼到其中）：

```python
# in a file mygame/commands/gametime.py

from evennia.contrib.base_systems import custom_gametime

from commands.command import Command

class CmdTime(Command):

    """
    Display the time.

    Syntax:
        time

    """

    key = "time"
    locks = "cmd:all()"

    def func(self):
        """Execute the time command."""
        # Get the absolute game time
        year, month, day, hour, mins, secs = custom_gametime.custom_gametime(absolute=True)
        time_string = f"We are in year {year}, day {day}, month {month}."
        time_string += f"\nIt's {hour:02}:{mins:02}:{secs:02}."
        self.msg(time_string)
```

不要忘記將其新增到您的 CharacterCmdSet 中以檢視此指令：

```python
# in mygame/commands/default_cmdset.py

from commands.gametime import CmdTime   # <-- Add

# ...

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        # ...
        self.add(CmdTime())   # <- Add
```

使用 `@reload` 指令重新載入遊戲。  您現在應該看到 `time` 指令。  如果您輸入它，您可能會看到類似以下內容：

    We are in year 0, day 0, month 0.
    It's 00:52:17.

如果您願意，您可以更漂亮地顯示幾個月甚至幾天的名稱。
如果“月份”在您的遊戲中被稱為“月亮”，那麼您就需要在此處新增它。

(time-related-events-in-custom-gametime)=
## 自訂遊戲時間中與時間相關的事件

`custom_gametime` 模組還可以考慮您的遊戲時間（以及您的自訂日曆）來安排與遊戲相關的事件。  它可用於每天 6:00 AM 傳送特定訊息，例如顯示太陽升起。 `custom_gametime.schedule` 函式的工作方式與上述預設函式的工作方式相同。
