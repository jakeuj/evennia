(show-a-dynamic-map-of-rooms)=
# 顯示房間的動態地圖

```{sidebar}
另請參閱 [Mapbuilder](../Contribs/Contrib-Mapbuilder.md) 和 [XYZGrid](../Contribs/Contrib-XYZGrid.md) contribs，它們提供了建立和顯示房間地圖的替代方法。 [實施 Evadventure 房間的初學者教學課程](https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Part3/Beginner-Tutorial-Rooms.html#adding-a-room-map) 也說明如何新增（更簡單的）自動地圖。
```
MUD 中經常需要的功能是顯示遊戲內地圖以幫助導航。

```
Forest path

         [.]   [.]
[.][.][@][.][.][.]
         [.]   [.][.][.]

The trees are looming over the narrow forest path.

Exits: East, West
```

(the-grid-of-rooms)=
## 房間網格

本教學的執行至少需要滿足兩個要求。

1. 泥漿的結構必須遵循邏輯佈局。 Evennia 支援你的世界的佈局在「邏輯上」是不可能的，房間迴圈到自己或出口通往地圖的另一邊。出口也可以被命名為任何名稱，從「跳出窗外」到「進入第五次元」。本教學假設您只能沿著基本方向（N、E、S 和 W）移動。
2. 房間必須連線並連結在一起才能正確產生地圖。 Vanilla Evennia 附帶一個管理指令 [tunnel](evennia.commands.default.building.CmdTunnel)，允許使用者在基本方向上建立房間，但需要額外的工作來確保房間已連線。例如，如果您`tunnel east`，然後立即執行`tunnel west`，您會發現您已經建立了兩個完全獨立的房間。因此，如果您想建立“邏輯”佈局，則需要小心。在本教學中，我們假設您有這樣一個房間網格，我們可以從中產生地圖。

(concept)=
## 概念

在進入程式碼之前，理解和概念化它是如何運作的是有益的。這個想法類似於從您目前位置開始的蠕蟲。它選擇一個方向並從該方向向外“行走”，並在行走過程中繪製出其路線。一旦它行駛了預設的距離，它就會停下來並從另一個方向重新開始。需要注意的是，我們想要一個易於呼叫且不太複雜的系統。因此，我們將把整個程式碼包裝到一個自訂 Python 類別中（不是 typeclass，因為它不使用 evennia 本身的任何核心物件）。  我們將建立當您輸入“look”時顯示如下的內容：

```
Hallway

      [.]   [.]
      [@][.][.][.][.]
      [.]   [.]   [.]

The distant echoes of the forgotten
wail throughout the empty halls.

Exits: North, East, South
```

您目前的位置由 `[@]` 定義，而 `[.]`s 是「蠕蟲」見過的其他房間
自從離開您所在的位置後。

(setting-up-the-map-display)=
## 設定地圖顯示

首先我們必須定義用於顯示地圖的元件。為了讓「蠕蟲」知道在地圖上繪製什麼符號，我們將讓它檢查它訪問的名為 `sector_type` 的房間上的 Attribute。在本教學中，我們瞭解兩個符號 - 一個普通的房間和我們所在的房間。我們也為沒有說 Attribute 的房間定義了一個後備符號 - 這樣即使我們沒有正確準備房間，地圖仍然可以工作。假設您的遊戲資料夾名為`mygame`，我們在`mygame/world/map.py.`中建立此程式碼

```python
# in mygame/world/map.py

# the symbol is identified with a key "sector_type" on the
# Room. Keys None and "you" must always exist.
SYMBOLS = { None : ' . ', # for rooms without sector_type Attribute
            'you' : '[@]',
            'SECT_INSIDE': '[.]' }
```

由於嘗試造訪未設定的 Attribute 返回 `None`，這意味著沒有 `sector_type` 的房間
屬性將顯示為`. `。接下來我們開始建立自訂類別`Map`。它將容納所有
我們需要的方法。

```python
# in mygame/world/map.py

class Map(object):

    def __init__(self, caller, max_width=9, max_length=9):
        self.caller = caller
        self.max_width = max_width
        self.max_length = max_length
        self.worm_has_mapped = {}
        self.curX = None
        self.curY = None
```

- `self.caller` 通常是您的角色物件，也就是使用地圖的角色物件。
- `self.max_width/length` 確定將產生的地圖的最大寬度和長度。請注意，將這些變數設為“奇數”非常重要，以確保顯示區域具有中心點。
- ` self.worm_has_mapped` 是基於上面的蠕蟲類比建構的。該字典將儲存「蠕蟲」對映的所有房間及其在網格內的相對位置。這是最重要的變數，因為它充當“檢查器”和“地址簿”，能夠告訴我們蠕蟲病毒去過哪裡以及到目前為止它所對映的內容。
- `self.curX/Y` 是代表蠕蟲在網格上目前位置的座標。

在實際完成任何型別的對應之前，我們需要建立一個空的顯示區域，並使用以下方法對其進行一些健全性檢查。

```python
# in mygame/world/map.py

class Map(object):
    # [... continued]

    def create_grid(self):
        # This method simply creates an empty grid/display area
        # with the specified variables from __init__(self):
        board = []
        for row in range(self.max_width):
            board.append([])
            for column in range(self.max_length):
                board[row].append('   ')
        return board

    def check_grid(self):
        # this method simply checks the grid to make sure
        # that both max_l and max_w are odd numbers.
        return True if self.max_length % 2 != 0 or self.max_width % 2 != 0\
            else False
```

在我們讓蠕蟲病毒繼續傳播之前，我們需要了解這一切背後的一些電腦科學，即「圖遍歷」。在偽程式碼中，我們試圖完成的是：

```python
# pseudo code

def draw_room_on_map(room, max_distance):
    self.draw(room)

    if max_distance == 0:
        return

    for exit in room.exits:
        if self.has_drawn(exit.destination):
            # skip drawing if we already visited the destination
            continue
        else:
            # first time here!
            self.draw_room_on_map(exit.destination, max_distance - 1)
```

Python 的美妙之處在於我們執行此操作的實際程式碼與此沒有太大區別
偽程式碼範例。

- `max_distance` 是一個變數，向我們的蠕蟲指示它將對映距離您當前位置有多少個房間 AWAY。顯然，如果您當前位置周圍有很多房間，則數字越大，所需的時間就越長。

這裡的第一個障礙是「max_distance」使用什麼值。蠕蟲沒有理由傳播得比實際顯示給您的距離更遠。例如，如果您的目前位置位於大小為`max_length = max_width = 9`的顯示區域的中心，那麼蠕蟲只需要
向任一方向走 `4` 空格：

```
[.][.][.][.][@][.][.][.][.]
 4  3  2  1  0  1  2  3  4
```

`max_distance`可以根據顯示區域的大小動態設定。當寬度/長度改變時，它會變成簡單的代數線性關係，即 `max_distance = (min(max_width, max_length) -1) / 2`。

(building-the-mapper)=
## 建構對映器

現在我們可以開始用一些方法填入我們的 Map 物件。我們還缺少一些非常重要的方法：

* `self.draw(self, room)` - 負責實際繪製房間到網格。
* `self.has_drawn(self, room)` - 檢查房間是否已被對映並且蠕蟲是否已經在這裡。
* `self.median(self, number)` - 一種簡單的實用方法，可從 `0, n` 中找到中位數（中點）
* `self.update_pos(self, room, exit_name)` - 透過相應地重新分配`self.curX/Y`來更新蠕蟲的物理位置。
* `self.start_loc_on_grid(self)` - 網格上的第一個初始繪製代表您在網格中間的位置。
* `self.show_map` - 一切完成後將地圖轉換為可讀字串
* `self.draw_room_on_map(self, room, max_distance)` - 將它們聯絡在一起的主要方法。


現在我們知道我們需要哪些方法，讓我們改進最初的 `__init__(self)` 以傳遞一些
條件語句並設定它以開始建立顯示。

```python
#mygame/world/map.py

class Map(object):

    def __init__(self, caller, max_width=9, max_length=9):
        self.caller = caller
        self.max_width = max_width
        self.max_length = max_length
        self.worm_has_mapped = {}
        self.curX = None
        self.curY = None

        if self.check_grid():
            # we have to store the grid into a variable
            self.grid = self.create_grid()
            # we use the algebraic relationship
            self.draw_room_on_map(caller.location,
                                  ((min(max_width, max_length) -1 ) / 2)

```

在這裡，我們檢查網格引數是否正確，然後建立一個空畫布並將我們的初始位置對應為第一個房間！

如上所述，`self.draw_room_on_map()` 的程式碼與偽程式碼沒有太大區別。方法如下圖所示：

```python
# in mygame/world/map.py, in the Map class

def draw_room_on_map(self, room, max_distance):
    self.draw(room)

    if max_distance == 0:
        return

    for exit in room.exits:
        if exit.name not in ("north", "east", "west", "south"):
            # we only map in the cardinal directions. Mapping up/down would be
            # an interesting learning project for someone who wanted to try it.
            continue
        if self.has_drawn(exit.destination):
            # we've been to the destination already, skip ahead.
            continue

        self.update_pos(room, exit.name.lower())
        self.draw_room_on_map(exit.destination, max_distance - 1)
```

「蠕蟲」做的第一件事就是在`self.draw`中繪製你目前的位置。讓我們定義一下...

```python
#in mygame/word/map.py, in the Map class

def draw(self, room):
    # draw initial ch location on map first!
    if room == self.caller.location:
        self.start_loc_on_grid()
        self.worm_has_mapped[room] = [self.curX, self.curY]
    else:
        # map all other rooms
        self.worm_has_mapped[room] = [self.curX, self.curY]
        # this will use the sector_type Attribute or None if not set.
        self.grid[self.curX][self.curY] = SYMBOLS[room.db.sector_type]
```

在`self.start_loc_on_grid()`中：

```python
def median(self, num):
    lst = sorted(range(0, num))
    n = len(lst)
    m = n -1
    return (lst[n//2] + lst[m//2]) / 2.0

def start_loc_on_grid(self):
    x = self.median(self.max_width)
    y = self.median(self.max_length)
    # x and y are floats by default, can't index lists with float types
    x, y = int(x), int(y)

    self.grid[x][y] = SYMBOLS['you']
    self.curX, self.curY = x, y # updating worms current location
```

系統繪製完目前地圖後，會檢查 `max_distance` 是否為 `0`（因為此
是初始開始階段，但不是）。現在，一旦我們有每個單獨的出口，我們就處理迭代
在房間裡。它做的第一件事是檢查蠕蟲所在的房間是否已經被對映。
讓我們定義...


```python
def has_drawn(self, room):
    return True if room in self.worm_has_mapped.keys() else False
```

如果`has_drawn`回傳`False`，這表示蠕蟲已經找到了一個尚未對映的房間。它
然後會「移動」到那裡。 self.curX/Y 有點滯後，所以我們必須確保跟蹤
蠕蟲的位置；我們在下面的 `self.update_pos()` 中執行此操作。

```python
def update_pos(self, room, exit_name):
    # this ensures the coordinates stays up to date
    # to where the worm is currently at.
    self.curX, self.curY = \
      self.worm_has_mapped[room][0], self.worm_has_mapped[room][1]

    # now we have to actually move the pointer
    # variables depending on which 'exit' it found
    if exit_name == 'east':
        self.curY += 1
    elif exit_name == 'west':
        self.curY -= 1
    elif exit_name == 'north':
        self.curX -= 1
    elif exit_name == 'south':
        self.curX += 1
```

一旦系統更新了蠕蟲的位置，它就會將新房間回饋給原來的房間
`draw_room_on_map()` 並重新開始該過程..

這基本上就是整件事情了。最後的方法是將它們組合在一起並製作一個漂亮的
使用 `self.show_map()` 方法從中提取表示性字串。

```python
def show_map(self):
    map_string = ""
    for row in self.grid:
        map_string += " ".join(row)
        map_string += "\n"

    return map_string
```

(using-the-map)=
## 使用地圖

為了觸發地圖，我們將其儲存在房間 typeclass 上。如果我們把它放進去
`return_appearance`我們每次看房間都會拿回地圖。

> `return_appearance` 是所有物件上可用的預設 Evennia 掛鉤；它被稱為e.g。由
`look` 指令取得某事物的描述（本例中為房間）。

```python
# in mygame/typeclasses/rooms.py

from evennia import DefaultRoom
from world.map import Map

class Room(DefaultRoom):

    def return_appearance(self, looker):
        # [...]
        string = f"{Map(looker).show_map()}\n"
        # Add all the normal stuff like room description,
        # contents, exits etc.
        string += "\n" + super().return_appearance(looker)
        return string
```

顯然，這種生成地圖的方法沒有考慮任何隱藏的門或出口…等等，但希望它可以作為一個良好的基礎。如前所述，在實施此操作之前，為房間打下堅實的基礎非常重要。您可以透過使用 @tunnel 在原版 evennia 上嘗試此操作，本質上您可以建立一個長直/前衛的非迴圈房間，該房間將顯示在您的遊戲地圖上。

上面的範例將在房間描述上方顯示地圖。您也可以使用 [EvTable](github:evennia.utils.evtable) 將描述和地圖放在一起。您可以做的其他一些事情是讓 [Command](../Components/Commands.md) 以更大的半徑顯示，也許帶有圖例和其他功能。

以下是全部`map.py`供您參考。您需要更新您的`Room` typeclass（請參閱上文）才能實際呼叫它。請記住，要檢視某個位置的不同符號，您還需要將房間上的 `sector_type` Attribute 設定為 `SYMBOLS` 字典中的按鍵之一。因此，在此範例中，要使房間對應為 `[.]`，您需要將該房間的 `sector_type` 設為 `"SECT_INSIDE"`。用`@set here/sector_type = "SECT_INSIDE"`試試。如果您希望所有新房間都有給定的扇區符號，您可以更改下面 `SYMBOLS` 字典中的預設值，或者您可以在房間的 `at_object_creation` 方法中新增 Attribute。

```python
# mygame/world/map.py

# These are keys set with the Attribute sector_type on the room.
# The keys None and "you" must always exist.
SYMBOLS = { None : ' . ',  # for rooms without a sector_type attr
            'you' : '[@]',
            'SECT_INSIDE': '[.]' }

class Map(object):

    def __init__(self, caller, max_width=9, max_length=9):
        self.caller = caller
        self.max_width = max_width
        self.max_length = max_length
        self.worm_has_mapped = {}
        self.curX = None
        self.curY = None

        if self.check_grid():
            # we actually have to store the grid into a variable
            self.grid = self.create_grid()
            self.draw_room_on_map(caller.location,
                                 ((min(max_width, max_length) -1 ) / 2))

    def update_pos(self, room, exit_name):
        # this ensures the pointer variables always
        # stays up to date to where the worm is currently at.
        self.curX, self.curY = \
           self.worm_has_mapped[room][0], self.worm_has_mapped[room][1]

        # now we have to actually move the pointer
        # variables depending on which 'exit' it found
        if exit_name == 'east':
            self.curY += 1
        elif exit_name == 'west':
            self.curY -= 1
        elif exit_name == 'north':
            self.curX -= 1
        elif exit_name == 'south':
            self.curX += 1

    def draw_room_on_map(self, room, max_distance):
        self.draw(room)

        if max_distance == 0:
            return

        for exit in room.exits:
            if exit.name not in ("north", "east", "west", "south"):
                # we only map in the cardinal directions. Mapping up/down would be
                # an interesting learning project for someone who wanted to try it.
                continue
            if self.has_drawn(exit.destination):
                # we've been to the destination already, skip ahead.
                continue

            self.update_pos(room, exit.name.lower())
            self.draw_room_on_map(exit.destination, max_distance - 1)

    def draw(self, room):
        # draw initial caller location on map first!
        if room == self.caller.location:
            self.start_loc_on_grid()
            self.worm_has_mapped[room] = [self.curX, self.curY]
        else:
            # map all other rooms
            self.worm_has_mapped[room] = [self.curX, self.curY]
            # this will use the sector_type Attribute or None if not set.
            self.grid[self.curX][self.curY] = SYMBOLS[room.db.sector_type]

    def median(self, num):
        lst = sorted(range(0, num))
        n = len(lst)
        m = n -1
        return (lst[n//2] + lst[m//2]) / 2.0

    def start_loc_on_grid(self):
        x = self.median(self.max_width)
        y = self.median(self.max_length)
        # x and y are floats by default, can't index lists with float types
        x, y = int(x), int(y)

        self.grid[x][y] = SYMBOLS['you']
        self.curX, self.curY = x, y # updating worms current location


    def has_drawn(self, room):
        return True if room in self.worm_has_mapped.keys() else False


    def create_grid(self):
        # This method simply creates an empty grid
        # with the specified variables from __init__(self):
        board = []
        for row in range(self.max_width):
            board.append([])
            for column in range(self.max_length):
                board[row].append('   ')
        return board

    def check_grid(self):
        # this method simply checks the grid to make sure
        # both max_l and max_w are odd numbers
        return True if self.max_length % 2 != 0 or \
                    self.max_width % 2 != 0 else False

    def show_map(self):
        map_string = ""
        for row in self.grid:
            map_string += " ".join(row)
            map_string += "\n"

        return map_string
```

(final-comments)=
## 最終意見

動態地圖可以透過更多功能進行擴充。例如，它可以標記退出或
也允許 NE、SE 等方向。它可以有適合不同地形型別的顏色。一個可以
也要研究上/下方向並找出如何以良好的方式顯示它。
