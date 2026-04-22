(extended-room)=
# 擴充房

貢獻 - Griatch 2012、vincent-lg 2019、Griatch 2023

這擴充套件了正常的 `Room` typeclass 以允許其描述隨
一天中的時間和/或季節以及任何其他狀態（如洪水或黑暗）。
在描述中嵌入 `$state(burning, This place is on fire!)` 將
允許根據房間狀態變更描述。房間還支援
`details` 供玩家在房間中檢視（無需建立新的
每個的遊戲內物件），以及對隨機迴聲的支援。房間
附帶一組用於 `look` 和 `@desc` 的備用指令，以及新指令
指令`detail`、`roomstate` 和`time`。

(installation)=
## 安裝

將`ExtendedRoomCmdset`新增到預設字元cmdset將新增所有
新的使用指令。

更詳細地說，在`mygame/commands/default_cmdsets.py`中：

```python
...
from evennia.contrib.grid import extended_room   # <---

class CharacterCmdset(default_cmds.CharacterCmdSet):
    ...
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        ...
        self.add(extended_room.ExtendedRoomCmdSet)  # <---

```

然後重新載入以使新指令可用。請注意，它們僅起作用
在有 typeclass `ExtendedRoom` 的房間。使用許可權建立新房間
typeclass或使用`typeclass`指令交換現有房間。請注意，自從
此 contrib 覆蓋 `look` 和 `@desc` 指令，您將需要新增
`extended_room.ExtendedRoomCmdSet` 到預設字元 cmdset *之後*
`super().at_cmdset_creation()`，否則它們將被預設外觀覆蓋。

挖掘一個新的擴充套件房間：

    dig myroom:evennia.contrib.grid.extended_room.ExtendedRoom = north,south

要使所有新房間 ExtendedRooms 而不必指定它，請使您的
`Room` typeclass 繼承自 `ExtendedRoom` 然後重新載入：

```python
# in mygame/typeclasses/rooms.py

from evennia.contrib.grid.extended_room import ExtendedRoom

# ...

class Room(ObjectParent, ExtendedRoom):
    # ...

```

(features)=
## 特徵

(state-dependent-description-slots)=
### 狀態相關的描述槽

預設情況下，使用正常的 `room.db.desc` 描述。不過你可以
新增的有狀態描述 `room.add_desc(description,
room_state=roomstate)`或使用遊戲內指令

```
@desc/roomstate [<description>]
```

例如

```
@desc/dark This room is pitch black.`.

```


這些將儲存在屬性`desc_<roomstate>`中。要設定預設值，
後備描述，只需使用`@desc <description>`。
要啟動房間的狀態，請使用 `room.add/remove_state(*roomstate)` 或遊戲中的
指令
```
roomstate <state>      (use it again to toggle the state off)
```
例如
```
roomstate dark
```
有一個內建的、基於時間的狀態`season`。預設情況下這些是“spring”，
「夏天」、「秋天」和「冬天」。 `room.get_season()` 方法返回
當前賽季基於比賽時間。預設情況下，它們會在 12 個月內更改
遊戲內的時間安排。你可以用以下指令控制它們
```
ExtendedRoom.months_per_year      # default 12
ExtendedRoom.seasons_per year     # a dict of {"season": (start, end), ...} where
                                  # start/end are given in fractions of the whole year
```
要設定季節描述，只需將其設為正常，使用 `room.add_desc` 或
遊戲中與

```
@desc/winter This room is filled with snow.
@desc/autumn Red and yellow leaves cover the ground.
```

通常季節會隨著遊戲時間的變化而變化，您也可以「強制」給定
透過設定季節的狀態
```
roomstate winter
```
如果你像這樣手動設定季節，它不會再次自動更改
直到您取消設定。

您可以使用`room.get_stateful_desc()`從房間取得狀態描述。

(changing-parts-of-description-based-on-state)=
### 根據狀態變更部分描述

所有描述都可以嵌入`$state(roomstate, description)`
[FuncParser tags](../Components/FuncParser.md) 嵌入其中。這是一個例子：

```py
room.add_desc("This a nice beach. "
              "$state(empty, It is completely empty)"
              "$state(full, It is full of people).", room_state="summer")
```

這是帶有特殊嵌入字串的夏季描述。如果你定了房間
與

    > room.add_room_state("summer", "empty")
    > room.get_stateful_desc()

    This is a nice beach. It is completely empty.

    > room.remove_room_state("empty")
    > room.add_room_state("full")
    > room.get_stateful_desc()

    This is a nice beach. It is full of people.

有四種預設的時間狀態應與這些 tags 一起使用。的
room 會自動追蹤並更改這些內容。預設情況下它們是“早上”，
「下午」、「晚上」和「晚上」。您可以透過以下方式取得目前時段
`room.get_time_of_day`。你可以用以下指令控制它們

```
ExtendedRoom.hours_per_day    # default 24
ExtendedRoom.times_of_day     # dict of {season: (start, end), ...} where
                              # the start/end are given as fractions of the day.
```

您可以像平常一樣使用這些內部描述：

    "A glade. $(morning, The morning sun shines down through the branches)."

(details)=
### 細節

_Details_ 是在房間中檢視的「虛擬」目標，無需建立
每件事的新資料庫例項。最好新增更多資訊
位置。詳細資訊以字串形式儲存在字典中。

    detail window = There is a window leading out.
    detail rock = The rock has a text written on it: 'Do not dare lift me'.

當你在房間裡時，你可以執行 `look window` 或 `look rock` 並獲得
匹配的詳細描述。這需要新的自訂 `look` 指令。

(random-echoes)=
### 隨機迴聲

`ExtendedRoom` 支援隨機迴聲。只需將它們設定為 Attribute 列表
`room_messages`：

```
room.room_message_rate = 120   # in seconds. 0 to disable
room.db.room_messages = ["A car passes by.", "You hear the sound of car horns."]
room.start_repeat_broadcast_messages()   # also a server reload works
```

這些聲音將每隔 120 秒開始隨機迴響到房間。


(extra-commands)=
### 額外指令

- `CmdExtendedRoomLook` (`look`) - 檢視支援房間詳細資訊的指令
- `CmdExtendedRoomDesc` (`@desc`) - desc 指令允許新增狀態 desc，
- `CmdExtendeRoomState` (`roomstate`) - 切換房間狀態
- `CmdExtendedRoomDetail` (`detail`) - 列出和操作房間詳細資訊
- `CmdExtendedRoomGameTime` (`time`) - 顯示房間中的當前時間和季節。


----

<small>此檔案頁面是從`evennia\contrib\grid\extended_room\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
