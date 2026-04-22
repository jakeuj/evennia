(adding-room-coordinates-to-your-game)=
# 將房間座標新增到您的遊戲中

```{sidebar} XYZGrid
另請參閱 [XYZGrid contrib](../Contribs/Contrib-XYZGrid.md)，它新增了座標支援和尋路。
```
本教學的內容難度適中。  您可能希望熟悉並輕鬆瞭解一些 Python 概念（如屬性）和可能的 Django 概念（如查詢），儘管本教學將嘗試引導您完成整個過程並每次都給出足夠的解釋。  如果您對數學不太有信心，請立即暫停，轉到範例部分，其中顯示了一張小地圖，並嘗試瀏覽程式碼或閱讀說明。

Evennia 預設沒有座標系。  房間和其他物件透過位置和內容連結：

- 一個物件可以位於一個位置，即另一個物件。  就像房間裡的出口一樣。
- 物件可以存取其內容。  房間可以看到哪些物件使用它作為位置（這將
包括出口、房間、角色等）。

該系統具有很大的靈活性，幸運的是，可以透過其他系統進行擴充套件。
在這裡，我為您提供一種以最符合Evennia的方式為每個房間新增座標的方法
設計。  這也將向您展示如何使用座標，尋找給定點周圍的房間
例項。

(coordinates-as-tags)=
## 座標為tags

第一個概念乍看之下可能是最令人驚訝的：我們將建立坐標為
[tags](../Components/Tags.md)。

那麼，為什麼不使用屬性，這不是更容易嗎？  會的。  我們可以做類似 `room.db.x = 3` 的事。  使用tags的好處是搜尋起來既簡單又有效。  雖然現在這看起來並不是一個巨大的優勢，但對於擁有數千個房間的資料庫來說，它可能會產生影響，特別是如果你有很多基於座標的東西。

我們不會向您提供逐步過程，而是向您展示程式碼。  請注意，我們使用
屬性以輕鬆存取和更新座標。  這是一種 Pythonic 方法。  這是我們的第一個
`Room` 類，您可以在 `typeclasses/rooms.py` 中修改：

```python
# in typeclasses/rooms.py

from evennia import DefaultRoom

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    
    @property
    def x(self):
        """Return the X coordinate or None."""
        x = self.tags.get(category="coordx")
        return int(x) if isinstance(x, str) else None

    @x.setter
    def x(self, x):
        """Change the X coordinate."""
        old = self.tags.get(category="coordx")
        if old is not None:
            self.tags.remove(old, category="coordx")
        if x is not None:
            self.tags.add(str(x), category="coordx")

    @property
    def y(self):
        """Return the Y coordinate or None."""
        y = self.tags.get(category="coordy")
        return int(y) if isinstance(y, str) else None
    
    @y.setter
    def y(self, y):
        """Change the Y coordinate."""
        old = self.tags.get(category="coordy")
        if old is not None:
            self.tags.remove(old, category="coordy")
        if y is not None:
            self.tags.add(str(y), category="coordy")

    @property
    def z(self):
        """Return the Z coordinate or None."""
        z = self.tags.get(category="coordz")
        return int(z) if isinstance(z, str) else None
    
    @z.setter
    def z(self, z):
        """Change the Z coordinate."""
        old = self.tags.get(category="coordz")
        if old is not None:
            self.tags.remove(old, category="coordz")
        if z is not None:
            self.tags.add(str(z), category="coordz")
```

如果您不熟悉 Python 中的屬性概念，我鼓勵您閱讀一本好書
關於該主題的教學。  [這篇關於Python屬性的文章](https://www.programiz.com/python-
programming/property)
解釋得很清楚，應該可以幫助您理解這個想法。

讓我們看看 `x` 的屬性。  首先是讀取屬性。

```python
    @property
    def x(self):
        """Return the X coordinate or None."""
        x = self.tags.get(category="coordx")
        return int(x) if isinstance(x, str) else None
```

它的作用非常簡單：

1. 它獲取類別 `"coordx"` 的 tag。  這是我們儲存 X 座標的 tag 類別。
如果找不到 tag，`tags.get` 方法將回傳 `None`。
2. 如果該值是 `str`，我們會將其轉換為整數。  請記住tags只能包含`str`，
所以我們需要轉換它。

那麼Tags可以包含數值嗎？好吧，從技術上講，他們不能：他們要麼在這裡，要麼不在這裡。  但使用 tag 類別，就像我們所做的那樣，我們得到 tag，只知道它的類別。  這是本教學中座標的基本方法。

現在，讓我們看看當我們希望在房間中設定 `x` 時將呼叫的方法：

```python
    @x.setter
    def x(self, x):
        """Change the X coordinate."""
        old = self.tags.get(category="coordx")
        if old is not None:
            self.tags.remove(old, category="coordx")
        if x is not None:
            self.tags.add(str(x), category="coordx")
```

1. 首先，我們刪除舊的 X 座標（如果存在）。  否則，我們最終會得到兩個 tags
房間以“coordx”為類別，這根本行不通。
2. 然後我們新增新的 tag，為其指定正確的類別。

如果您新增此程式碼並重新載入遊戲，一旦您使用房間中的角色登入
位置，你可以玩：

```
py here.x
py here.x = 0
py here.y = 3
py here.z = -2
py here.z = None
```

(some-additional-searches)=
## 一些額外的搜尋

擁有座標很有用，原因如下：

1. 它可以幫助塑造一個真正邏輯的世界，至少在地理上是如此。
2. 它可以允許在給定座標處尋找特定房間。
3. 它可以很好地快速找到某個位置周圍的房間。
4. 它甚至在尋路（找到兩個房間之間的最短路徑）方面也很有用。

到目前為止，我們的座標係可以幫助解決 1. 問題，但除此之外就沒有什麼幫助了。  以下是我們所採用的一些方法
可以加到`Room` typeclass。  這些方法只是搜尋方法。  請注意，他們是
類別方法，因為我們想要獲得房間。

(finding-one-room)=
### 尋找一間房間

首先，一個簡單的問題：如何在給定座標處找到房間？  比如說，X=0、Y=0 處的房間是多少，
Z=0？

```python
class Room(DefaultRoom):
    # ...
    @classmethod
    def get_room_at(cls, x, y, z):
        """
        Return the room at the given location or None if not found.

        Args:
            x (int): the X coord.
            y (int): the Y coord.
            z (int): the Z coord.

        Return:
            The room at this location (Room) or None if not found.

        """
        rooms = cls.objects.filter(
                db_tags__db_key=str(x), db_tags__db_category="coordx").filter(
                db_tags__db_key=str(y), db_tags__db_category="coordy").filter(
                db_tags__db_key=str(z), db_tags__db_category="coordz")
        if rooms:
            return rooms[0]

        return None
```

此解決方案包括一些[Django查詢](Basic-Tutorial-Django-queries)。  基本上，我們所做的就是存取物件管理器並搜尋具有匹配 tags 的物件。再次強調，不要花太多時間擔心機制，這個方法非常容易使用：

```
Room.get_room_at(5, 2, -3)
```

請注意，這是一個類別方法：您將從 `Room` （類別）而不是例項呼叫它。儘管你仍然可以：

    py here.get_room_at(3, 8, 0)

(finding-several-rooms)=
### 找幾個房間

這是另一種有用的方法，它允許我們尋找給定座標周圍的房間。  這是更高階的搜尋並進行一些計算，請注意！  如果您是，請檢視以下部分
丟失了。

```python
from math import sqrt

class Room(DefaultRoom):

    # ...

    @classmethod
    def get_rooms_around(cls, x, y, z, distance):
        """
        Return the list of rooms around the given coordinates.

        This method returns a list of tuples (distance, room) that
        can easily be browsed.  This list is sorted by distance (the
        closest room to the specified position is always at the top
        of the list).

        Args:
            x (int): the X coord.
            y (int): the Y coord.
            z (int): the Z coord.
            distance (int): the maximum distance to the specified position.

        Returns:
            A list of tuples containing the distance to the specified
            position and the room at this distance.  Several rooms
            can be at equal distance from the position.

        """
        # Performs a quick search to only get rooms in a square
        x_r = list(reversed([str(x - i) for i in range(0, distance + 1)]))
        x_r += [str(x + i) for i in range(1, distance + 1)]
        y_r = list(reversed([str(y - i) for i in range(0, distance + 1)]))
        y_r += [str(y + i) for i in range(1, distance + 1)]
        z_r = list(reversed([str(z - i) for i in range(0, distance + 1)]))
        z_r += [str(z + i) for i in range(1, distance + 1)]
        wide = cls.objects.filter(
                db_tags__db_key__in=x_r, db_tags__db_category="coordx").filter(
                db_tags__db_key__in=y_r, db_tags__db_category="coordy").filter(
                db_tags__db_key__in=z_r, db_tags__db_category="coordz")

        # We now need to filter down this list to find out whether
        # these rooms are really close enough, and at what distance
        # In short: we change the square to a circle.
        rooms = []
        for room in wide:
            x2 = int(room.tags.get(category="coordx"))
            y2 = int(room.tags.get(category="coordy"))
            z2 = int(room.tags.get(category="coordz"))
            distance_to_room = sqrt(
                    (x2 - x) ** 2 + (y2 - y) ** 2 + (z2 - z) ** 2)
            if distance_to_room <= distance:
                rooms.append((distance_to_room, room))

        # Finally sort the rooms by distance
        rooms.sort(key=lambda tup: tup[0])
        return rooms
```

這變得更加嚴重。

1. 我們指定了座標作為引數。  我們使用距離來確定一個廣泛的範圍。
也就是說，對於每個座標，我們建立一個可能匹配的清單。  請參閱下面的範例。
2. 然後我們在這個更廣泛的範圍內搜尋房間。  它在我們的位置周圍提供了一個正方形。  有些房間絕對不在範圍內。  再次，請參閱下面的範例以遵循邏輯。
3. 我們過濾列表並按指定座標的距離對其進行排序。

請注意，我們僅從步驟 2 開始搜尋。因此，Django 搜尋不會尋找並快取所有內容
物件，只是比真正需要的範圍更廣泛。  該方法傳回一個圓
圍繞指定點的座標。  姜戈尋找一個正方形。  什麼不適合圈子
在步驟3中被刪除，這是唯一包含系統計算的部分。  這個方法是
最佳化以快速且有效率。

(an-example)=
### 一個例子

一個例子可能會有所幫助。  考慮這個非常簡單的地圖（下面有文字描述）：

```
4 A B C D
3 E F G H
2 I J K L
1 M N O P
  1 2 3 4
```

X 座標如下。  Y 座標在左側給出。  這是一個簡單的正方形，有 16 個房間：每行 4 個，共 4 行。  在此範例中，所有房間均由字母標識：頂部第一行為房間 A 至 D，第二行為房間 A 至 D，第二行為房間 E 至 H，第三行為房間 I 至 L，第四行為 M 至 P。左下房間 X=1 和 Y=1 為 M。右上房間 X=4 且 Y=4 為 D。 
假設我們想要找出所有距房間 J 的鄰居，距離為 1。 J 位於 X=2，Y=2 處。

所以我們使用：

    Room.get_rooms_around(x=2, y=2, z=0, distance=1)
    # we'll assume a z coordinate of 0 for simplicity

1. 首先，此方法取得 J 周圍正方形中的所有房間。因此它得到 E F G、I J K、M N O。如果需要，可以在這些座標周圍繪製正方形以檢視發生了什麼。
2. 接下來，我們瀏覽此清單並檢查 J（X=2，Y=2）與房間之間的實際距離。正方形的四個角不在這個圓內。  例如，J 和 M 之間的距離不是 1。如果您畫一個以 J 為中心、半徑為 1 的圓，您會注意到正方形的四個角（E、G、M 和 O）不在該圓內。所以我們刪除它們。 3.我們按照與J的距離排序。

所以最終我們可能會得到這樣的結果：

```
[
    (0, J), # yes, J is part of this circle after all, with a distance of 0
    (1, F),
    (1, I),
    (1, K),
    (1, N),
]
```

如果您想檢視實際效果，可以嘗試更多範例。

(to-conclude)=
## 總結一下

您還可以使用該系統來對映其他物件，而不僅僅是房間。  您可以輕鬆刪除
`Z` 座標，如果您只需要 `X` 和 `Y`。