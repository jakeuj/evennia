(map-builder)=
# 地圖產生器

Cloud_Keeper 2016 的貢獻

根據 2D ASCII 地圖的繪製建立遊戲地圖。

這是一個需要兩個輸入的指令：

    ≈≈≈≈≈
    ≈♣n♣≈   MAP_LEGEND = {("♣", "♠"): build_forest,
    ≈∩▲∩≈                 ("∩", "n"): build_mountains,
    ≈♠n♠≈                 ("▲"): build_temple}
    ≈≈≈≈≈

由 ASCII 個字元組成的字串，表示函式的對應和字典
包含建置指令。地圖的字元被迭代並
與觸發字元列表相比。當找到匹配項時
執行對應的函式，產生房間、出口和物件：
由使用者建構指令定義。如果一個字元不匹配
提供的觸發字元（包括空格）它會被簡單地跳過並且
過程仍在繼續。

例如，上面的地圖代表了山脈 (n,∩) 中的一座寺廟 (▲)
位於四面環水 (≈) 的島嶼上的森林 (♣,♠) 中。上的每個字元
第一行被迭代，但由於與我們的 `MAP_LEGEND` 不匹配，所以它
被跳過。在第二行，它找到“♣”，這是一個匹配項，因此
`build_forest` 函式被呼叫。接下來 `build_mountains` 函式是
呼叫等等，直到地圖完成。建築指令已透過
以下論點：

    x         - The rooms position on the maps x axis
    y         - The rooms position on the maps y axis
    caller    - The account calling the command
    iteration - The current iterations number (0, 1 or 2)
    room_dict - A dictionary containing room references returned by build
                functions where tuple coordinates are the keys (x, y).
                ie room_dict[(2, 2)] will return the temple room above.

建築功能應該返回它們建立的房間。預設這些房間
用於在北、南的有效相鄰房間之間建立出口，
東、西兩個方向。可以使用開關關閉此行為
論據。除了關閉自動退出產生之外，開關
允許地圖迭代多次。這對於
像是自訂出口建築之類的東西。退出需要引用兩個
退出位置和退出目的地。在第一次迭代期間是
可能會建立一個指向目的地的出口
尚未建立，導致錯誤。透過迭代地圖兩次
房間可以在第一次迭代時建立，並且房間相關的程式碼可以
在第二次迭代時使用。迭代次數和字典
對先前建立的房間的引用將傳遞給建置指令。

然後，您可以使用 MAP 和 MAP_LEGEND 變數的路徑在遊戲中呼叫該指令
您提供的路徑是相對於 evennia 或 mygame 資料夾的。

另請參閱[檔案中的單獨教學](./Contrib-Mapbuilder-Tutorial.md)。

(installation)=
## 安裝

透過將指令匯入並包含在您的 default_cmdsets 模組中來使用。
例如：

```python
    # mygame/commands/default_cmdsets.py

    from evennia.contrib.grid import mapbuilder

    ...

    self.add(mapbuilder.CmdMapBuilder())
```


(usage)=
## 用法：

    mapbuilder[/switch] <path.to.file.MAPNAME> <path.to.file.MAP_LEGEND>

    one - execute build instructions once without automatic exit creation.
    two - execute build instructions twice without automatic exit creation.

(examples)=
## 範例

    mapbuilder world.gamemap.MAP world.maplegend.MAP_LEGEND
    mapbuilder evennia.contrib.grid.mapbuilder.EXAMPLE1_MAP EXAMPLE1_LEGEND
    mapbuilder/two evennia.contrib.grid.mapbuilder.EXAMPLE2_MAP EXAMPLE2_LEGEND
            (Legend path defaults to map path)

以下是兩個範例，展示了自動退出產生和
自訂退出生成。雖然可以從該模組找到並使用
方便 下面的範例程式碼應該位於 mygame/world 的 `mymap.py` 中。

(example-one)=
### 例項一

```python

from django.conf import settings
from evennia.utils import utils

# mapbuilder evennia.contrib.grid.mapbuilder.EXAMPLE1_MAP EXAMPLE1_LEGEND

# -*- coding: utf-8 -*-

# Add the necessary imports for your instructions here.
from evennia import create_object
from typeclasses import rooms, exits
from random import randint
import random


# A map with a temple (▲) amongst mountains (n,∩) in a forest (♣,♠) on an
# island surrounded by water (≈). By giving no instructions for the water
# characters we effectively skip it and create no rooms for those squares.
EXAMPLE1_MAP = '''
≈≈≈≈≈
≈♣n♣≈
≈∩▲∩≈
≈♠n♠≈
≈≈≈≈≈
'''

def example1_build_forest(x, y, **kwargs):
    '''A basic example of build instructions. Make sure to include **kwargs
    in the arguments and return an instance of the room for exit generation.'''

    # Create a room and provide a basic description.
    room = create_object(rooms.Room, key="forest" + str(x) + str(y))
    room.db.desc = "Basic forest room."

    # Send a message to the account
    kwargs["caller"].msg(room.key + " " + room.dbref)

    # This is generally mandatory.
    return room


def example1_build_mountains(x, y, **kwargs):
    '''A room that is a little more advanced'''

    # Create the room.
    room = create_object(rooms.Room, key="mountains" + str(x) + str(y))

    # Generate a description by randomly selecting an entry from a list.
    room_desc = [
        "Mountains as far as the eye can see",
        "Your path is surrounded by sheer cliffs",
        "Haven't you seen that rock before?",
    ]
    room.db.desc = random.choice(room_desc)

    # Create a random number of objects to populate the room.
    for i in range(randint(0, 3)):
        rock = create_object(key="Rock", location=room)
        rock.db.desc = "An ordinary rock."

    # Send a message to the account
    kwargs["caller"].msg(room.key + " " + room.dbref)

    # This is generally mandatory.
    return room


def example1_build_temple(x, y, **kwargs):
    '''A unique room that does not need to be as general'''

    # Create the room.
    room = create_object(rooms.Room, key="temple" + str(x) + str(y))

    # Set the description.
    room.db.desc = (
        "In what, from the outside, appeared to be a grand and "
        "ancient temple you've somehow found yourself in the the "
        "Evennia Inn! It consists of one large room filled with "
        "tables. The bardisk extends along the east wall, where "
        "multiple barrels and bottles line the shelves. The "
        "barkeep seems busy handing out ale and chatting with "
        "the patrons, which are a rowdy and cheerful lot, "
        "keeping the sound level only just below thunderous. "
        "This is a rare spot of mirth on this dread moor."
    )

    # Send a message to the account
    kwargs["caller"].msg(room.key + " " + room.dbref)

    # This is generally mandatory.
    return room


# Include your trigger characters and build functions in a legend dict.
EXAMPLE1_LEGEND = {
    ("♣", "♠"): example1_build_forest,
    ("∩", "n"): example1_build_mountains,
    ("▲"): example1_build_temple,
}
```

(example-two)=
### 範例二

```python
# @mapbuilder/two evennia.contrib.grid.mapbuilder.EXAMPLE2_MAP EXAMPLE2_LEGEND

# -*- coding: utf-8 -*-

# Add the necessary imports for your instructions here.
# from evennia import create_object
# from typeclasses import rooms, exits
# from evennia.utils import utils
# from random import randint
# import random

# This is the same layout as Example 1 but included are characters for exits.
# We can use these characters to determine which rooms should be connected.
EXAMPLE2_MAP = '''
≈ ≈ ≈ ≈ ≈

≈ ♣-♣-♣ ≈
  |   |
≈ ♣ ♣ ♣ ≈
  | | |
≈ ♣-♣-♣ ≈

≈ ≈ ≈ ≈ ≈
'''

def example2_build_forest(x, y, **kwargs):
    '''A basic room'''
    # If on anything other than the first iteration - Do nothing.
    if kwargs["iteration"] > 0:
        return None

    room = create_object(rooms.Room, key="forest" + str(x) + str(y))
    room.db.desc = "Basic forest room."

    kwargs["caller"].msg(room.key + " " + room.dbref)

    return room

def example2_build_verticle_exit(x, y, **kwargs):
    '''Creates two exits to and from the two rooms north and south.'''
    # If on the first iteration - Do nothing.
    if kwargs["iteration"] == 0:
        return

    north_room = kwargs["room_dict"][(x, y - 1)]
    south_room = kwargs["room_dict"][(x, y + 1)]

    # create exits in the rooms
    create_object(
        exits.Exit, key="south", aliases=["s"], location=north_room, destination=south_room
    )

    create_object(
        exits.Exit, key="north", aliases=["n"], location=south_room, destination=north_room
    )

    kwargs["caller"].msg("Connected: " + north_room.key + " & " + south_room.key)


def example2_build_horizontal_exit(x, y, **kwargs):
    '''Creates two exits to and from the two rooms east and west.'''
    # If on the first iteration - Do nothing.
    if kwargs["iteration"] == 0:
        return

    west_room = kwargs["room_dict"][(x - 1, y)]
    east_room = kwargs["room_dict"][(x + 1, y)]

    create_object(exits.Exit, key="east", aliases=["e"], location=west_room, destination=east_room)

    create_object(exits.Exit, key="west", aliases=["w"], location=east_room, destination=west_room)

    kwargs["caller"].msg("Connected: " + west_room.key + " & " + east_room.key)


# Include your trigger characters and build functions in a legend dict.
EXAMPLE2_LEGEND = {
    ("♣", "♠"): example2_build_forest,
    ("|"): example2_build_verticle_exit,
    ("-"): example2_build_horizontal_exit,
}

```

```{toctree}
:hidden:
Contrib-Mapbuilder-Tutorial
```


----

<small>此檔案頁面是從`evennia\contrib\grid\mapbuilder\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
