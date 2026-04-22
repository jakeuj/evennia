(in-game-rooms)=
# 遊戲內房間

_房間_描述了遊戲世界中的特定位置。作為一個抽象概念，它可以代表遊戲內容的任何易於組合在一起的區域。  在本課中，我們還將建立一個小型的遊戲內自動地圖。

在EvAdventure中，我們將有兩種主要型別的房間：
- 普通的地上房間。基於固定的地圖，這些將被建立一次，然後不會改變。我們將在本課中介紹它們。
- 地牢房間 - 這些將是_程式生成_房間的範例，當玩家探索地下世界時動態建立。作為普通房間的子類，我們將在[地下城生成課程](./Beginner-Tutorial-Dungeon.md)中瞭解它們。

(the-base-room)=
## 基礎房

> 建立一個新模組`evadventure/rooms.py`。

```python
# in evadventure/rooms.py

from evennia import AttributeProperty, DefaultRoom

class EvAdventureRoom(DefaultRoom):
	"""
    Simple room supporting some EvAdventure-specifics.
 
    """
 
    allow_combat = AttributeProperty(False, autocreate=False)
    allow_pvp = AttributeProperty(False, autocreate=False)
    allow_death = AttributeProperty(False, autocreate=False)

``` 

我們的`EvadventureRoom`很簡單。我們使用 Evennia 的 `DefaultRoom` 作為基礎，只增加三個額外的屬性來定義

- 如果允許戰鬥在房間裡開始的話。
- 如果允許戰鬥，如果允許 PvP（玩家對玩家）戰鬥。
- 如果允許戰鬥，如果允許任何一方因此死亡。

稍後我們必須確保我們的戰鬥系統尊重這些價值觀。

(pvp-room)=
## PvP 房間

這是一個允許非致命 PvP（陪練）的房間：

```python
# in evadventure/rooms.py

# ... 

class EvAdventurePvPRoom(EvAdventureRoom):
    """
    Room where PvP can happen, but noone gets killed.
    
    """
    
    allow_combat = AttributeProperty(True, autocreate=False)
    allow_pvp = AttributeProperty(True, autocreate=False)
    
    def get_display_footer(self, looker, **kwargs):
        """
        Customize footer of description.
        """
        return "|yNon-lethal PvP combat is allowed here!|n"
```

[主房間描述](../../../Components/Objects.md#changing-an-objects-appearance)後會顯示`get_display_footer`的返回，表示該房間為陪練室。這意味著當玩家跌至 0 HP 時，他們將輸掉戰鬥，但不會面臨任何死亡風險（儘管武器在陪練過程中通常會磨損）。

(adding-a-room-map)=
## 新增房間地圖

我們想要一個動態地圖，可以直觀地顯示您可以隨時使用的出口。以下是我們的房間的顯示方式：

```shell
  o o o
   \|/
  o-@-o
    | 
    o
The crossroads 
A place where many roads meet. 
Exits: north, northeast, south, west, and northwest
```

> 檔案不顯示 ansi 顏色。

讓我們用地圖擴充套件基地`EvAdventureRoom`。

```{code-block} python
:linenos: 
:emphasize-lines: 12,19,51,52,58,67

# in evadventyre/rooms.py

# ... 

from copy import deepcopy
from evennia import DefaultCharacter
from evennia.utils.utils import inherits_from

CHAR_SYMBOL = "|w@|n"
CHAR_ALT_SYMBOL = "|w>|n"
ROOM_SYMBOL = "|bo|n"
LINK_COLOR = "|B"

_MAP_GRID = [
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", "@", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
]
_EXIT_GRID_SHIFT = {
    "north": (0, 1, "||"),
    "east": (1, 0, "-"),
    "south": (0, -1, "||"),
    "west": (-1, 0, "-"),
    "northeast": (1, 1, "/"),
    "southeast": (1, -1, "\\"),
    "southwest": (-1, -1, "/"),
    "northwest": (-1, 1, "\\"),
}

class EvAdventureRoom(DefaultRoom): 

    # ... 

    def format_appearance(self, appearance, looker, **kwargs):
        """Don't left-strip the appearance string"""
        return appearance.rstrip()
 
    def get_display_header(self, looker, **kwargs):
        """
        Display the current location as a mini-map.
 
        """
        # make sure to not show make a map for users of screenreaders.
        # for optimization we also don't show it to npcs/mobs
        if not inherits_from(looker, DefaultCharacter) or (
            looker.account and looker.account.uses_screenreader()
        ):
            return ""
 
        # build a map
        map_grid = deepcopy(_MAP_GRID)
        dx0, dy0 = 2, 2
        map_grid[dy0][dx0] = CHAR_SYMBOL
        for exi in self.exits:
            dx, dy, symbol = _EXIT_GRID_SHIFT.get(exi.key, (None, None, None))
            if symbol is None:
                # we have a non-cardinal direction to go to - indicate this
                map_grid[dy0][dx0] = CHAR_ALT_SYMBOL
                continue
            map_grid[dy0 + dy][dx0 + dx] = f"{LINK_COLOR}{symbol}|n"
            if exi.destination != self:
                map_grid[dy0 + dy + dy][dx0 + dx + dx] = ROOM_SYMBOL
 
        # Note that on the grid, dy is really going *downwards* (origo is
        # in the top left), so we need to reverse the order at the end to mirror it
        # vertically and have it come out right.
        return "  " + "\n  ".join("".join(line) for line in reversed(map_grid))
```

從`get_display_header`傳回的字串將最終出現在[房間描述](../../../Components/Objects.md#changing-an-objects-description)的頂部，這是顯示地圖的好地方！

- **第 12 行**：地圖本身由 2D 矩陣 `_MAP_GRID` 組成。這是一個由 Python 清單描述的 2D 區域。要查詢列表中的給定位置，首先需要找到要使用哪個巢狀列表，然後找到要在該列表中使用哪個元素。 Python 中的索引從 0 開始。因此，要為最南端的房間繪製 `o` 符號，您需要在 `_MAP_GRID[4][2]` 處繪製。
- **第 19 行**：`_EXIT_GRID_SHIFT` 指示每個主要出口的方向，以及在該點繪製的地圖符號。因此 `"east": (1, 0, "-")` 表示東出口將沿著正 x 方向（向右）繪製一步，使用「-」符號。對於像 `|` 和“\\”這樣的符號，我們需要使用雙符號進行轉義，因為否則它們會被解釋為其他格式的一部分。
- **第 51 行**：我們先製作 `_MAP_GRID` 的 `deepcopy`。這樣我們就不會修改原始模板，但總是有一個空模板可供使用。
- **第52行**：我們使用`@`來指示玩家的位置（在座標`(2, 2)`處）。然後，我們從房間的實際出口處使用它們的名稱來找出要從中心繪製的符號。
- **第 58 行**：如果需要，我們希望能夠上/下電網。因此，如果房間中有非主要出口（例如「後退」或上/下），我們將透過在目前房間中顯示 `>` 符號而不是 `@` 來表示這一點。
- **第 67 行**：將所有出口和房間符號放置在網格中後，我們將它們全部合併到一個字串中。最後我們使用Python的標準[join](https://www.w3schools.com/python/ref_string_join.asp)將網格轉換為單一字串。為此，我們必須將網格顛倒過來（反轉最外面的清單）。這是為什麼呢？如果您考慮 MUD 遊戲如何顯示其資料 - 透過在底部列印然後向上滾動 - 您會意識到 Evennia 必須先傳送地圖的頂部並_最後_傳送地圖的底部，才能正確顯示給使用者。

(adding-life-to-a-room)=
## 為房間增添生氣

通常情況下，房間是靜態的，直到你在裡面做某事。但假設您身處一個被描述為熙熙攘攘的市場的房間裡。偶爾收到一些隨機訊息不是很好嗎？

"You hear a merchant calling out his wares."
	“音樂聲從敞開的酒館門中飄過廣場。”
	“商業聲音以穩定的節奏起伏。”

以下是如何實現此目的的範例：

```{code-block} python 
:linenos:
:emphasize-lines: 22,25

# in evadventure/rooms.py 

# ... 

from random import choice, random
from evennia import TICKER_HANDLER

# ... 

class EchoingRoom(EvAdventureRoom):
    """A room that randomly echoes messages to everyone inside it"""

    echoes = AttributeProperty(list, autocreate=False)
	echo_rate = AttributeProperty(60 * 2, autocreate=False)
	echo_chance = AttributeProperty(0.1, autocreate=False)

	def send_echo(self): 
		if self.echoes and random() < self.echo_chance: 
			self.msg_contents(choice(self.echoes))

	def start_echo(self): 
		TICKER_HANDLER.add(self.echo_rate, self.send_echo)

	def stop_echo(self): 
		TICKER_HANDLER.remove(self.echo_rate, self.send_echo)
```

[TickerHandler](../../../Components/TickerHandler.md)。這相當於“請勾選我 - 訂閱服務”。在**第 22 行**，我們告訴將 `.send_echo` 方法新增至處理程式，並告訴 TickerHandler 每 `.echo_rate` 秒呼叫該方法。

當 `.send_echo` 方法被呼叫時，它將使用 `random.random()` 來檢查我們是否應該_實際上_做任何事情。在我們的範例中，我們僅在 10% 的時間內顯示訊息。在這種情況下，我們使用 Python 的 `random.choice()` 從 `.echoes` 清單中抓取隨機文字字串，傳送給這個房間內的每個人。

以下是您在遊戲中使用這個房間的方法：

    > dig market:evadventure.rooms.EchoingRoom = market,back 
    > market 
    > set here/echoes = ["You hear a merchant shouting", "You hear the clatter of coins"]
    > py here.start_echo() 

如果您等待一段時間，您最終會看到兩個迴聲之一出現。如果需要，可以使用 `py here.stop_echo()`。

如果沒有別的辦法的話，能夠隨意開啟/關閉迴聲是個好主意，因為如果它們顯示得太頻繁，您會驚訝地發現它們會多麼煩人。

在這個例子中，我們不得不求助於 `py` 來啟用/停用回顯，但是您可以輕鬆地建立一些實用程式 [指令](../Part1/Beginner-Tutorial-Adding-Commands.md) `startecho` 和 `stopecho` 來為您完成此操作。我們將此作為獎勵練習。

(testing)=
## 測試

> 建立一個新模組`evadventure/tests/test_rooms.py`。

```{sidebar} 
您可以在[教學資料夾中](evennia.contrib.tutorials.evadventure.tests.test_rooms)找到現成的測試模組。
```
我們的新房間要測試的主要內容是地圖。以下是如何進行此測試的基本原則：

```python
# in evadventure/tests/test_rooms.py

from evennia import DefaultExit, create_object
from evennia.utils.test_resources import EvenniaTestCase
from ..characters import EvAdventureCharacter 
from ..rooms import EvAdventureRoom

class EvAdventureRoomTest(EvenniaTestCase): 

    def test_map(self): 
        center_room = create_object(EvAdventureRoom, key="room_center")
        
        n_room = create_object(EvAdventureRoom, key="room_n)
        create_object(DefaultExit, 
                      key="north", location=center_room, destination=n_room)
        ne_room = create_object(EvAdventureRoom, key="room=ne")
        create_object(DefaultExit,
			          key="northeast", location=center_room, destination=ne_room)
        # ... etc for all cardinal directions 
        
        char = create_object(EvAdventureCharacter, 
					         key="TestChar", location=center_room)					        
		desc = center_room.return_appearance(char)

        # compare the desc we got with the expected description here

```


因此，我們建立了一堆房間，將它們連結到一個中心房間，然後確保房間中的地圖看起來像我們期望的那樣。

(conclusion)=
## 結論

在本課中，我們操作字串並製作了地圖。更改物件的描述是更改基於文字的遊戲的「圖形」的一個重要部分，因此檢查[組成物件描述的部分](../../../Components/Objects.md#changing-an-objects-description) 是很好的額外閱讀。
