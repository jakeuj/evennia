(creating-rooms-from-an-ascii-map)=
# 從 ASCII 對映建立房間

本教學描述了基於預先繪製的地圖建立遊戲內地圖顯示。  它與[Mapbuilder contrib](./Contrib-Mapbuilder.md)一起使用。   它還詳細介紹如何使用[批次程式碼處理器](../Components/Batch-Code-Processor.md) 進行進階建置。

Evennia 不要求其房間以「邏輯」方式定位。您的出口可以被命名
任何東西。你可以從「西」出口通往一個被描述為位於遙遠北方的房間。你
可以有一個房間在另一個房間內，出口通往同一個房間或描述空間
現實世界中不可能的幾何形狀。

也就是說，大多數遊戲*確實*以邏輯方式組織房間，如果沒有其他方法來保留房間
他們球員的理智。當他們這樣做時，遊戲就可以繪製地圖了。本教學將給出
一個簡單但靈活的遊戲內地圖系統範例，可進一步幫助玩家導航。我們將

為了簡化開發和錯誤檢查，我們將把工作分解為小塊，每個塊
建立在之前的基礎上。為此，我們將廣泛使用[批次程式碼處理器](Batch-
Code-Processor)，因此您可能需要熟悉一下。

1. **規劃地圖** - 在這裡我們將提供一個小範例地圖以用於其餘部分
教學。
2. **製作地圖物件** - 這將展示如何製作靜態遊戲內「地圖」物件
人物可以拿起來看。
3. **構建地圖區域** - 這裡我們實際上將根據
我們之前設計的地圖。
4. **地圖程式碼** - 這會將地圖連結到該位置，因此我們的輸出如下所示：

    ```
    crossroads(#3)
    ↑╚∞╝↑
    ≈↑│↑∩  The merger of two roads. To the north looms a mighty castle.
    O─O─O  To the south, the glow of a campfire can be seen. To the east lie
    ≈↑│↑∩  the vast mountains and to the west is heard the waves of the sea.
    ↑▲O▲↑
    
    Exits: north(#8), east(#9), south(#10), west(#11)
    ```

今後我們將假設您的遊戲資料夾名稱為 `mygame` 並且您尚未修改
dkefault 指令。我們也不會在我們的地圖中使用[顏色](../Concepts/Colors.md)，因為它們
不顯示在檔案 wiki 中。

(planning-the-map)=
## 規劃地圖

讓我們從有趣的部分開始吧！ MUDs 中的地圖有許多不同的[形狀和
尺寸](http://journal.imaginary-realities.com/volume-05/issue-01/modern-interface-modern-
mud/index.html)。有些看起來只是由線連線的盒子。其他人則有複雜的圖形
遊戲本身的外部。

我們的地圖將是遊戲中的文字，但這並不意味著我們僅限於普通字母表！如果
您曾在 Microsoft Word 中選擇過 [Wingdings 字型](https://en.wikipedia.org/wiki/Wingdings)
您會知道還有許多其他字元可供使用。建立遊戲時
Evennia 您有權存取 [UTF-8 字元編碼](https://en.wikipedia.org/wiki/UTF-8)
供您使用[數千個字母、數字和幾何形狀](https://mcdlr.com/utf-8/#1)。

對於本練習，我們從以下位置使用的特殊字元託盤複製並貼上
[矮人要塞](https://dwarffortresswiki.org/index.php/Character_table)創造希望的東西
令人愉悅且易於理解的景觀：

```
≈≈↑↑↑↑↑∩∩
≈≈↑╔═╗↑∩∩   Places the account can visit are indicated by "O".
≈≈↑║O║↑∩∩   Up the top is a castle visitable by the account.
≈≈↑╚∞╝↑∩∩   To the right is a cottage and to the left the beach.
≈≈≈↑│↑∩∩∩   And down the bottom is a camp site with tents.
≈≈O─O─O⌂∩   In the center is the starting location, a crossroads
≈≈≈↑│↑∩∩∩   which connect the four other areas.
≈≈↑▲O▲↑∩∩   
≈≈↑↑▲↑↑∩∩
≈≈↑↑↑↑↑∩∩
```
根據遊戲風格和要求，製作遊戲地圖時需要考慮許多因素
你打算實施。在這裡，我們將顯示 5x5 周圍區域的字元圖
帳戶。這意味著確保每個可訪問位置周圍都有 2 個字元。好
這個階段的計劃可以在許多問題發生之前解決它們。

(creating-a-map-object)=
## 建立地圖物件

在本節中，我們將嘗試建立一個帳戶可以擷取並檢視的實際「地圖」物件
在。

Evennia 提供一系列[預設指令](../Components/Default-Commands.md)
[在遊戲中創造物件和房間](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Building-Quickstart.md)。雖然易於訪問，但這些指令的用途非常廣泛
具體的、受限制的事物，因此不會提供盡可能多的實驗彈性（對於
進階異常請參閱[FuncParser](../Components/FuncParser.md))。此外，輸入長
遊戲使用者端中一遍又一遍的描述和屬性可能會變得乏味；尤其是當
測試時，您可能想要一遍又一遍地刪除和重新建立內容。

為了克服這個問題，Evennia 提供了作為輸入檔的[批次處理器](../Components/Batch-Processors.md)
遊戲外建立的。在本教學中，我們將使用兩個可用批次中更強大的一個
處理器，[批次程式碼處理器](../Components/Batch-Code-Processor.md)，使用 `@batchcode` 指令呼叫。
這是一個非常強大的工具。它允許您製作 Python 檔案作為您的藍圖
整個遊戲世界。這些檔案可以直接使用Evennia的Python API。批次程式碼允許
可以在您喜歡的任何文字編輯器中輕鬆編輯和建立，避免手動構建
遊戲內的世界線。

> 重要警告：`@batchcode` 的威力只能與 `@py` 指令相提並論。批次碼是這樣的
功能強大，應該僅為[超級使用者](../Concepts/Building-Permissions.md)保留。仔細想想
在讓其他人（例如 `Developer`-級別的員工）自己執行 `@batchcode` 之前 - 確保
你可以接受他們在你的伺服器上執行*任意Python程式碼*。

雖然是一個簡單的範例，但地圖物件是嘗試 `@batchcode` 的好方法。前往
`mygame/world` 並在其中建立一個名為 `batchcode_map.py` 的新檔案：

```Python
# mygame/world/batchcode_map.py

from evennia import create_object
from evennia import DefaultObject

# We use the create_object function to call into existence a 
# DefaultObject named "Map" wherever you are standing.

map = create_object(DefaultObject, key="Map", location=caller.location)

# We then access its description directly to make it our map.

map.db.desc = """
≈≈↑↑↑↑↑∩∩
≈≈↑╔═╗↑∩∩
≈≈↑║O║↑∩∩
≈≈↑╚∞╝↑∩∩
≈≈≈↑│↑∩∩∩
≈≈O─O─O⌂∩
≈≈≈↑│↑∩∩∩
≈≈↑▲O▲↑∩∩
≈≈↑↑▲↑↑∩∩
≈≈↑↑↑↑↑∩∩
"""

# This message lets us know our map was created successfully.
caller.msg("A map appears out of thin air and falls to the ground.")
```

以超級使用者登入您的遊戲專案並執行指令

```
@batchcode batchcode_map
```

這將載入您的 `batchcode_map.py` 檔案並執行程式碼（Evennia 將在您的 `world/` 中查詢
自動資料夾，因此您無需指定它）。

地面上應該會出現一個新的地圖物件。您可以使用`look map`檢視地圖。讓我們
使用 `get map` 指令獲取它。萬一我們迷路了，我們就需要它！

(building-the-map-areas)=
## 建構地圖區域

我們剛剛使用批次程式碼建立了一個對我們的冒險有用的物件。但那上面的位置
地圖實際上還不存在——我們都被繪製好了無處可去！讓我們使用批次程式碼
根據我們的地圖建構一個遊戲區域。我們概述了五個區域：城堡、小屋、露營地、
沿海海灘和連線它們的十字路口。為此建立一個新的批次程式碼檔案
`mygame/world`，名為`batchcode_world.py`。

```Python
# mygame/world/batchcode_world.py

from evennia import create_object, search_object
from typeclasses import rooms, exits

# We begin by creating our rooms so we can detail them later.

centre = create_object(rooms.Room, key="crossroads")
north = create_object(rooms.Room, key="castle")
east = create_object(rooms.Room, key="cottage")
south = create_object(rooms.Room, key="camp")
west = create_object(rooms.Room, key="coast")

# This is where we set up the cross roads.
# The rooms description is what we see with the 'look' command.

centre.db.desc = """
The merger of two roads. A single lamp post dimly illuminates the lonely crossroads.
To the north looms a mighty castle. To the south the glow of a campfire can be seen.
To the east lie a wall of mountains and to the west the dull roar of the open sea.
"""

# Here we are creating exits from the centre "crossroads" location to 
# destinations to the north, east, south, and west. We will be able 
# to use the exit by typing it's key e.g. "north" or an alias e.g. "n".

centre_north = create_object(exits.Exit, key="north", 
                            aliases=["n"], location=centre, destination=north)
centre_east = create_object(exits.Exit, key="east", 
                            aliases=["e"], location=centre, destination=east)
centre_south = create_object(exits.Exit, key="south", 
                            aliases=["s"], location=centre, destination=south)
centre_west = create_object(exits.Exit, key="west", 
                            aliases=["w"], location=centre, destination=west)

# Now we repeat this for the other rooms we'll be implementing.
# This is where we set up the northern castle.

north.db.desc = "An impressive castle surrounds you. " \
                "There might be a princess in one of these towers."
north_south = create_object(exits.Exit, key="south", 
                            aliases=["s"], location=north, destination=centre)

# This is where we set up the eastern cottage.

east.db.desc = "A cosy cottage nestled among mountains " \
               "stretching east as far as the eye can see."
east_west = create_object(exits.Exit, key="west", 
                            aliases=["w"], location=east, destination=centre)

# This is where we set up the southern camp.

south.db.desc = "Surrounding a clearing are a number of " \
                "tribal tents and at their centre a roaring fire."
south_north = create_object(exits.Exit, key="north", 
                            aliases=["n"], location=south, destination=centre)

# This is where we set up the western coast.

west.db.desc = "The dark forest halts to a sandy beach. " \
               "The sound of crashing waves calms the soul."
west_east = create_object(exits.Exit, key="east", 
                            aliases=["e"], location=west, destination=centre)

# Lastly, lets make an entrance to our world from the default Limbo room.

limbo = search_object('Limbo')[0]
limbo_exit = create_object(exits.Exit, key="enter world", 
                            aliases=["enter"], location=limbo, destination=centre)

```

使用 `@batchcode batchcode_world` 應用這個新的批次程式碼。如果程式碼沒有錯誤我們
現在有一個漂亮的迷你世界可供探索。請記住，如果您迷路了，可以檢視我們的地圖
建立了！

(in-game-minimap)=
## 遊戲內小地圖

現在我們有了一個風景和匹配的地圖，但我們真正想要的是一個顯示的迷你地圖
每當我們移動到一個房間或使用`look`指令時。

我們 *可以* 手動將地圖的一部分輸入到每個房間的描述中，就像我們製作地圖一樣
物件描述。但有些MUDs有幾萬個房間！此外，如果我們改變了我們的
在地圖上，我們可能必須手動更改許多房間描述以匹配
改變。因此，我們將製作一個中央模組來儲存我們的地圖。房間會參考這個
建立時的中心位置和地圖更改將在下次執行我們的時生效
批次程式碼。

為了製作我們的迷你地圖，我們需要能夠將完整地圖切割成多個部分。為此，我們需要將其
以一種允許我們輕鬆做到這一點的格式。幸運的是，Python 允許我們將字串視為列表
字元允許我們挑選出我們需要的字元。

`mygame/world/map_module.py`
```Python
# We place our map into a sting here.
world_map = """\
≈≈↑↑↑↑↑∩∩
≈≈↑╔═╗↑∩∩
≈≈↑║O║↑∩∩
≈≈↑╚∞╝↑∩∩
≈≈≈↑│↑∩∩∩
≈≈O─O─O⌂∩
≈≈≈↑│↑∩∩∩
≈≈↑▲O▲↑∩∩
≈≈↑↑▲↑↑∩∩
≈≈↑↑↑↑↑∩∩
"""

# This turns our map string into a list of rows. Because python 
# allows us to treat strings as a list of characters, we can access 
# those characters with world_map[5][5] where world_map[row][column].
world_map = world_map.split('\n')

def return_map():
    """
    This function returns the whole map
    """
    map = ""
    
    #For each row in our map, add it to map
    for valuey in world_map:
        map += valuey
        map += "\n"
    
    return map

def return_minimap(x, y, radius = 2):
    """
    This function returns only part of the map.
    Returning all chars in a 2 char radius from (x,y)
    """
    map = ""
    
    #For each row we need, add the characters we need.
    for valuey in world_map[y-radius:y+radius+1]:         for valuex in valuey[x-radius:x+radius+1]:
            map += valuex
        map += "\n"
    
    return map
```

設定完 map_module 後，讓我們將 `mygame/world/batchcode_map.py` 中的硬編碼地圖替換為
對我們的地圖模組的引用。確保匯入我們的map_module！

```python
# mygame/world/batchcode_map.py

from evennia import create_object
from evennia import DefaultObject
from world import map_module

map = create_object(DefaultObject, key="Map", location=caller.location)

map.db.desc = map_module.return_map()

caller.msg("A map appears out of thin air and falls to the ground.")
```

以超級使用者登入 Evennia 並執行此批次程式碼。如果一切正常，我們的新地圖應該
看起來和舊地圖一模一樣 - 你可以使用 `@delete` 刪除舊地圖（使用數字來刪除舊地圖）
選擇要刪除的）。

現在，讓我們將注意力轉向我們的遊戲房間。讓我們使用 `return_minimap` 方法
上面建立的目的是為了在我們的房間描述中包含小地圖。這個有點多
複雜。

就其本身而言，我們必須滿足於地圖「高於」描述
`room.db.desc = map_string + description_string`，或透過顛倒順序來*下面*的地圖。
這兩個選項都不太令人滿意——我們希望在文字旁邊有地圖！為此
在解決方案中，我們將探索 Evennia 附帶的實用程式。藏在`evennia\evennia\utils`中
是一個名為 [EvTable](github:evennia.utils.evtable) 的小模組。這是一個高階ASCII表
建立者供您在遊戲中使用。我們將透過建立一個包含 1 行和 2 行的基本表來使用它
列（一列用於我們的地圖，一列用於我們的文字），同時也隱藏了邊框。開啟批次檔案
再次

```python
# mygame\world\batchcode_world.py

# Add to imports
from evennia.utils import evtable
from world import map_module

# [...]

# Replace the descriptions with the below code.

# The cross roads.
# We pass what we want in our table and EvTable does the rest.
# Passing two arguments will create two columns but we could add more.
# We also specify no border.
centre.db.desc = evtable.EvTable(map_module.return_minimap(4,5), 
                 "The merger of two roads. A single lamp post dimly " \
                 "illuminates the lonely crossroads. To the north " \
                 "looms a mighty castle. To the south the glow of " \
                 "a campfire can be seen. To the east lie a wall of " \
                 "mountains and to the west the dull roar of the open sea.", 
                 border=None)
# EvTable allows formatting individual columns and cells. We use that here
# to set a maximum width for our description, but letting the map fill
# whatever space it needs. 
centre.db.desc.reformat_column(1, width=70)

# [...]

# The northern castle.
north.db.desc = evtable.EvTable(map_module.return_minimap(4,2), 
                "An impressive castle surrounds you. There might be " \
                "a princess in one of these towers.", 
                border=None)
north.db.desc.reformat_column(1, width=70)   

# [...]

# The eastern cottage.
east.db.desc = evtable.EvTable(map_module.return_minimap(6,5), 
               "A cosy cottage nestled among mountains stretching " \
               "east as far as the eye can see.", 
               border=None)
east.db.desc.reformat_column(1, width=70)

# [...]

# The southern camp.
south.db.desc = evtable.EvTable(map_module.return_minimap(4,7), 
                "Surrounding a clearing are a number of tribal tents " \
                "and at their centre a roaring fire.", 
                border=None)
south.db.desc.reformat_column(1, width=70)

# [...]

# The western coast.
west.db.desc = evtable.EvTable(map_module.return_minimap(2,5), 
               "The dark forest halts to a sandy beach. The sound of " \
               "crashing waves calms the soul.", 
               border=None)
west.db.desc.reformat_column(1, width=70)
```

在我們執行新的批次程式碼之前，如果您像我一樣，您將擁有大約 100 張地圖
周圍有 3-4 個不同版本的房間，從地獄邊緣延伸出來。讓我們把它全部擦掉
從頭開始。在指令提示字元中，您可以執行 `evennia flush` 來清除資料庫並
重新開始。但是，它不會重設 dbref 值，因此如果您位於 #100，它將從那裡開始。
或者，您可以導航至 `mygame/server` 並刪除 `evennia.db3` 檔案。現在指揮
提示使用`evennia migrate`擁有一個全新製作的資料庫。

登入evennia並執行`@batchcode batchcode_world`，您將有一個小世界可供探索。

(conclusions)=
## 結論

現在您應該有一個對映的小世界，並對批次程式碼、EvTable 以及如何進行基本瞭解
可以輕鬆地將新的遊戲定義功能新增到Evennia。

您可以透過擴充套件地圖並建立更多房間來探索，輕鬆地根據本教學進行構建。為什麼
不要透過嘗試其他教學來為您的遊戲新增更多功能：[為您的世界新增天氣](Weather-
Tutorial)、[用 NPC 填充您的世界](../Howtos/Tutorial-NPC-Reacting.md) 或
[實施戰鬥系統](../Howtos/Turn-based-Combat-System.md)。
