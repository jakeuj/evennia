(wilderness-system)=
# 荒野系統

titeuf87 的貢獻，2017 年

這contrib提供了荒野地圖，而沒有實際建立大量
房間數 - 當您移動時，您最終會回到同一個房間，但其描述
變化。這意味著您可以使用很少的資料庫來建立巨大的區域，例如
只要房間相對相似（e.g。僅名稱/描述發生變化）。

(installation)=
## 安裝

此contrib不提供任何新指令。而是預設的 `py` 指令
用於直接呼叫這contrib中的函式/類別。

(usage)=
## 用法

首先需要建立荒野地圖。可以有不同的地圖，全部
與他們自己的名字。如果未提供名稱，則使用預設名稱。在內部，
荒野儲存為 Script 並具有您指定的名稱。如果你不這樣做
指定名稱，將建立並使用名為“default”的script。

    py from evennia.contrib.grid import wilderness; wilderness.create_wilderness()

建立後，就可以進入該荒野地圖：

    py from evennia.contrib.grid import wilderness; wilderness.enter_wilderness(me)

荒野地圖所使用的所有座標均採用`(x, y)`格式
元組。 x 從左到右，y 從下到上。所以`(0, 0)`
是地圖的左下角。

> 您也可以透過在 GLOBAL_SCRIPT 中定義 WildernessScript 來新增荒野
> 設定.如果這樣做，請確保定義地圖提供者。

(customisation)=
## 客製化

預設值雖然可用，但可以自訂。當建立一個
新的荒野地圖可以提供“地圖提供者”：這是一個
python 物件足夠聰明來建立地圖。

預設提供者 `WildernessMapProvider` 只是建立一個網格區域
大小不受限制。

`WildernessMapProvider` 可以被子類化以建立更有趣的
地圖，還可以自訂使用的房間/出口 typeclass。

`WildernessScript` 還有一個可選的 `preserve_items` 屬性，該屬性
當設定為 `True` 時，將不會回收包含任何物件的房間。預設情況下，
當荒野房間中沒有玩家時，就會被回收。

也沒有允許玩家進入荒野的指令。這個
還需要補充：可以是指令，也可以是退出，取決於你的
需要。

(example)=
## 例子

為了給出一個如何自訂的例子，我們將建立一個非常簡單的（並且
小）形狀像金字塔的荒野地圖。地圖將是
以字串形式提供：「.」符號是我們可以行走的位置。

讓我們建立一個檔案`world/pyramid.py`：

```python
# mygame/world/pyramid.py

map_str = '''
     .
    ...
   .....
  .......
'''

from evennia.contrib.grid import wilderness

class PyramidMapProvider(wilderness.WildernessMapProvider):

    def is_valid_coordinates(self, wilderness, coordinates):
        "Validates if these coordinates are inside the map"
        x, y = coordinates
        try:
            lines = map_str.split("\n")
            # The reverse is needed because otherwise the pyramid will be
            # upside down
            lines.reverse()
            line = lines[y]
            column = line[x]
            return column == "."
        except IndexError:
            return False

    def get_location_name(self, coordinates):
        "Set the location name"
        x, y = coordinates
        if y == 3:
            return "Atop the pyramid."
        else:
            return "Inside a pyramid."

    def at_prepare_room(self, coordinates, caller, room):
        "Any other changes done to the room before showing it"
        x, y = coordinates
        desc = "This is a room in the pyramid."
        if y == 3 :
            desc = "You can see far and wide from the top of the pyramid."
        room.ndb.active_desc = desc
```

請注意，目前活動描述儲存為 `.ndb.active_desc`。當
看看房間，這就是將被拉出並顯示的內容。

> 房間的出口總是存在的，但鎖隱藏了那些不用於房間的出口。
> 地點。因此，如果您是超級使用者，請確保`quell`（因為超級使用者忽略
> 鎖，否則這些出口將不會被隱藏）

現在我們可以使用新的金字塔形荒野地圖了。從內部Evennia我們
建立一個新的荒野（名稱為“default”），但使用我們的新地圖提供者：

    py from world import pyramid as p; p.wilderness.create_wilderness(mapprovider=p.PyramidMapProvider())
    py from evennia.contrib.grid import wilderness; wilderness.enter_wilderness(me, coordinates=(4, 1))

(implementation-details)=
## 實施細節

當角色進入荒野時，他們會得到自己的房間。如果
他們移動，而不是移動角色，房間會改變以匹配
新座標。

如果一個角色在荒野中遇到另一個角色，那麼他們的房間
合併。當其中一個角色再次離開時，他們每個人都會得到自己的
單獨的房間。

房間是根據需要建立的。不需要的房間會被存放起來，以避免
未來再次建立新房間的間接費用。


----

<small>此檔案頁面是從`evennia\contrib\grid\wilderness\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
