(xyzgrid)=
# XYZgrid

Gratch 2021 的貢獻

將 Evennia 的遊戲世界放置在 xy（z 是不同的地圖）座標網格上。
網格是透過繪製和解析 2D ASCII 地圖在外部建立和維護的，
包括傳送、地圖轉換和幫助尋路的特殊標記。
支援在每個地圖上非常快速的最短路徑尋路。還包括一個
快速檢視功能，僅檢視距離您有限的步數
目前位置（對於將網格顯示為遊戲中的更新地圖很有用）。

網格管理是在遊戲外使用新的evennia啟動器完成的
選項。

(examples)=
## 範例

<script id="asciicast-Zz36JuVAiPF0fSUR09Ii7lcxc" src="https://asciinema.org/a/Zz36JuVAiPF0fSUR09Ii7lcxc.js" async></script>

```
#-#-#-#   #
|  /      d
#-#       |   #
   \      u   |\
o---#-----#---+-#-#
|         ^   |/
|         |   #
v         |    \
#-#-#-#-#-# #---#
    |x|x|     /
    #-#-#    #-
```

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                     #---#
                                    /
                                   @-
-~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dungeon Entrance
To the east, a narrow opening leads into darkness.
Exits: northeast and east

```

(installation)=
## 安裝

1. XYZGrid 需要 `scipy` 函式庫。最簡單的就是獲得“額外”
Evennia 的依賴關係

       pip install evennia[extra]

如果您使用`git`安裝，還可以

       (cd to evennia/ folder)
       pip install --upgrade -e .[extra]

這將安裝 Evennia 的所有可選要求。
2. 匯入並將 `evennia.contrib.grid.xyzgrid.commands.XYZGridCmdSet` 新增到
`CharacterCmdset` cmdset 在 `mygame/commands.default_cmds.py` 中。重新載入
   伺服器。這使得 `map`、`goto/path` 和修改後的 `teleport` 和
   `open` 遊戲中可用指令。

[add]: ../Components/Command-Sets

3. 編輯`mygame/server/conf/settings.py`並新增

       EXTRA_LAUNCHER_COMMANDS['xyzgrid'] = 'evennia.contrib.grid.xyzgrid.launchcmd.xyzcommand'
       PROTOTYPE_MODULES += ['evennia.contrib.grid.xyzgrid.prototypes']

這將新增在 `evennia xyzgrid <option>` 上輸入的新功能
   指令列。  它還將製作 `xyz_room` 和 `xyz_exit` 原型
   在生成網格時可用作原型父母。

4. 執行 `evennia xyzgrid help` 以獲取可用選項。

5. （可選）：預設情況下，xyzgrid 將僅產生基於模組的
[原型]。這是一種最佳化，通常是有意義的
   因為無論如何，網格完全是在遊戲之外定義的。如果你想
   也利用遊戲中（db-）建立的原型，新增
   `XYZGRID_USE_DB_PROTOTYPES = True` 到設定。

[prototypes]: ../Components/Prototypes

(overview)=
## 概述

網格contrib由多個元件組成。

1. `XYMap` - 該類別使用特殊的 _Map strings_ 解析模組
和 _Map legends_ 到一個 Python 物件中。它有尋路助手和
   視覺範圍處理。
2. `XYZGrid` - 這是一個單例 [Script](../Components/Scripts.md)
儲存遊戲中的所有`XYMaps`。它是管理“網格”的中心點
   遊戲的。
3. `XYZRoom` 和 `XYZExit` 是使用的自訂 typeclasses
[Tags](../Components/Tags.md)
   知道它們位於哪個 X、Y、Z 座標。 `XYZGrid` 是
   抽象化直到它被用來_spawn_這些資料庫實體到
   您可以在遊戲中實際互動的東西。 `XYZRoom`
   typeclass 正在使用其 `return_appearance` 掛鉤來顯示遊戲中的地圖。
4. 已新增自訂_指令_用於與XYZ-感知位置進行互動。
5. 新的自訂_啟動器指令_，`evennia xyzgrid <options>` 用於
從終端管理網格（無需登入遊戲）。

我們將透過一個範例開始探索這些元件。

(first-example-usage)=
## 第一個範例用法

安裝後，從指令列執行以下操作（其中
`evennia` 指令可用）：

    $ evennia xyzgrid init

使用`evennia xyzgrid help`檢視所有選項）
如果尚不存在，這將建立一個新的 `XYZGrid` [Script](../Components/Scripts.md)。
`evennia xyzgrid` 僅為此 contrib 新增的自訂啟動選項。

xyzgrid-contrib 有完整的網格範例。讓我們新增它：

    $ evennia xyzgrid add evennia.contrib.grid.xyzgrid.example

現在您可以在網格上列出地圖：

    $ evennia xyzgrid list

您會發現新增了兩張新地圖。你可以找到很多額外的資訊
使用 `show` 子指令檢視每個地圖：

    $ evennia xyzgrid show "the large tree"
    $ evennia xyzgrid show "the small cave"

如果您想檢視網格的程式碼，請開啟
[evennia/contrib/grid/xyzgrid/example.py](evennia.contrib.grid.xyzgrid.example)。
（我們將在後面的部分中解釋詳細資訊）。

到目前為止，網格是“抽象的”，並且在遊戲中沒有實際存在。讓我們
產生實際的房間/出口。這需要一些時間。

    $ evennia xyzgrid spawn

這將採用與每個地圖的_地圖圖例_一起儲存的原型並使用它
在那裡建造XYZ-感知房間。它還會解析所有連結以做出合適的
在位置之間退出。如果您修改過，您應該重新執行此指令
網格的佈局/原型。多次執行它是安全的。

    $ evennia reload

（如果伺服器未執行，則為 `evennia start`）。這很重要
每次產生操作，因為 `evennia xyzgrid` 在
常規 evennia 程式。重新載入可確保重新整理所有快取。

現在您可以登入伺服器了。您應該可以使用一些新指令。

    teleport (3,0,the large tree)

`teleport` 指令現在接受可選的（X、Y、Z）座標。傳送
房間名稱或 `#dbref` 的作用仍然相同。這會將你傳送到
網格。您應該會看到地圖顯示。嘗試四處走走。

    map

這個新的僅限建構器的指令以完整形式顯示當前地圖（也
顯示使用者通常不可見的「不可見」標記。

    teleport (3, 0)

一旦你進入一個網格房間，你可以傳送到另一個網格房間_在同一房間
map_ 不指定 Z 座標/地圖名稱。

您可以使用 `open` 退出回到“非網格”，但請記住您
不得使用基本方向來執行此操作 - 如果這樣做，`evennia xyzgrid spawn`
下次執行它時可能會刪除它。

    open To limbo;limbo = #2
    limbo

你回到了 Limbo（它不知道關於 XYZ 座標的任何資訊）。你
但是可以將永久連結返回到網格地圖：

    open To grid;grid = (3,0,the large tree)
    grid

這就是將非網格位置和網格位置連結在一起的方式。例如你可以
以這種方式將房屋嵌入網格“內部”。

`(3,0,the large tree)` 是「地下城入口」。如果你向東走你會
_過渡_進入「小洞穴」地圖。這是一個小型的地下迷宮
能見度有限。再次回到外面（回到「大樹」地圖）。

    path view

這找到了通往“A beautiful view”房間的最短路徑，該房間位於大房間的高處
樹。如果你的用戶端有顏色，你應該會看到路徑的起點
以黃色顯示。

    goto view

這將開始自動帶您前往檢視。在路上你們都會進步
進入樹並穿越地圖內的傳送器。單獨使用 `goto`
中止自動行走。

完成探索後，再次開啟終端（在遊戲外）並
刪除所有內容：

    $ evennia xyzgrid delete

系統將要求您確認刪除網格並解除安裝
XYZGrid Script。之後重新載入伺服器。如果你在一張地圖上
刪除後，您將被移回您的家庭位置。

(defining-an-xymap)=
## 定義XYMap

對於適合傳遞到 `evennia xyzgrid add <module>` 的模組，
模組必須包含以下變數之一：

- `XYMAP_DATA` - 包含完全定義 XYMap 的資料的字典
- `XYMAP_DATA_LIST` - `XYMAP_DATA` 字典的列表。如果存在，則需要
優先。這允許在一個模組中儲存多個地圖。


`XYMAP_DATA` 字典有以下形式：

```
XYMAP_DATA = {
    "zcoord": <str>
    "map": <str>,
    "legend": <dict, optional>,
    "prototypes": <dict, optional>
    "options": <dict, optional>
}

```

- `"zcoord"` (str)：地圖的 Z 座標/地圖名稱。
- `"map"` (str)：描述地圖拓樸的_地圖字串_。
- `"legend"`（字典，可選）：將地圖上的每個符號對應到Python程式碼。這
dict 可以省略或僅部分填充 - 任何未指定的符號都會
  而是使用 contrib 中的預設圖例。
- `"prototypes"`（字典，可選）：這是對映地圖座標的字典
自訂原型覆蓋。當地圖生成到
  實際的房間/出口。
- `"options"`（字典，可選）：這些被傳遞到`return_appearance`
房間的掛鉤並允許自訂地圖的顯示方式，
  尋路應該如何進行等等。

這是整個設定的最小範例：

```
# In, say, a module gamedir/world/mymap.py

MAPSTR = r"""

+ 0 1 2

2 #-#-#
     /
1 #-#
  |  \
0 #---#

+ 0 1 2


"""
# use only defaults
LEGEND = {}

# tweak only one room. The 'xyz_room/exit' parents are made available
# by adding the xyzgrid prototypes to settings during installation.
# the '*' are wildcards and allows for giving defaults on this map.
PROTOTYPES = {
    (0, 0): {
        "prototype_parent": "xyz_room",
        "key": "A nice glade",
        "desc": "Sun shines through the branches above.",
    },
    (0, 0, 'e'): {
        "prototype_parent": "xyz_exit",
        "desc": "A quiet path through the foilage",
    },
    ('*', '*'): {
        "prototype_parent": "xyz_room",
        "key": "In a bright forest",
        "desc": "There is green all around.",
    },
    ('*', '*', '*'): {
        "prototype_parent": "xyz_exit",
        "desc": "The path leads further into the forest.",
    },
}

# collect all info for this one map
XYMAP_DATA = {
    "zcoord": "mymap",  # important!
    "map": MAPSTR,
    "legend": LEGEND,
    "prototypes": PROTOTYPES,
    "options": {}
}

# this can be skipped if there is only one map in module
XYMAP_DATA_LIST = [
    XYMAP_DATA
]
```

上面的地圖將會被加入到網格中

    $ evennia xyzgrid add world.mymap

在下面的部分中，我們將依次討論每個元件。

(the-zcoord)=
### Z座標

網格上的每個 XYMap 都有一個 Z 座標，通常可以視為
地圖的名稱。 Z 座標可以是字串或整數，且必須
在整個網格中是唯一的。它作為鍵“zcoord”新增到`XYMAP_DATA`。

大多數使用者只想將每張地圖視為一個位置，並為其命名
“Z 座標”，例如 `Dungeon of Doom`、`The ice queen's palace` 或“城市”
布萊克黑文`。但如果您願意，也可以將其命名為 -1, 0, 1, 2, 3。

> 請注意，在中搜尋 Zcoord *不區分大小寫*

尋路僅在每個 XYMap 內發生（上/下通常是透過移動來「偽造」的）
橫向到 XY 平面的新區域）。

(a-true-3d-map)=
#### 真正的 3D 地圖

即使是最硬派的科幻太空遊戲，也可以考慮堅持 2D
運動。對玩家來說，用圖形來視覺化 3D 體積已經夠困難的了。
在文字中就更難了。

也就是說，如果您想建立一個真正的 X、Y、Z 3D 座標系（其中
您可以從每個點向上/向下移動），您也可以這樣做。

這contrib提供了一個範例指令`commands.CmdFlyAndDive`，該指令為玩家提供了
能夠使用 `fly` 和 `dive` 在 Z 之間直接向上/向下移動
座標。只需將其（或其 cmdset `commands.XYZGridFlyDiveCmdSet`）新增到您的
角色cmdset並重新載入來嘗試。

為了使飛行/潛水工作，您需要將網格建構成 XY-網格地圖的“堆疊”
並透過它們的 Z 座標作為整數命名它們。飛行/俯衝動作將
僅當上方/下方確實有匹配的房間時才有效。

> 請注意，由於尋路僅在每個 XY 地圖內有效，因此玩家不會
> 能夠在自動行走中包含飛行/潛水 - 這始終是手冊
> 行動。

作為範例，我們假設座標 `(1, 1, -3)`
是通往地面的深井底部（0 級）

```
LEVEL_MINUS_3 = r"""
+ 0 1

1   #
    |
0 #-#

+ 0 1
"""

LEVEL_MINUS_2 = r"""
+ 0 1

1   #

0

+ 0 1
"""

LEVEL_MINUS_1 = r"""
+ 0 1

1   #

0

+ 0 1
"""

LEVEL_0 = r"""
+ 0 1

1 #-#
  |x|
0 #-#

+ 0 1
"""

XYMAP_DATA_LIST = [
    {"zcoord": -3, "map": LEVEL_MINUS_3},
    {"zcoord": -2, "map": LEVEL_MINUS_2},
    {"zcoord": -1, "map": LEVEL_MINUS_1},
    {"zcoord": 0, "map": LEVEL_0},
]
```

在此範例中，如果我們在 `(1, 1, -3)` 到達井底，我們
`fly` 直上三層，直到到達轉角處的 `(1, 1, 0)`
某種開放領域。

我們可以從`(1, 1, 0)`跳下去。在預設實作中，您必須 `dive` 3 次
追根究底。如果你願意，你可以調整指令，這樣你
自動落到底部並受到傷害等。

我們無法從任何其他 XY 位置飛行/俯衝/俯衝，因為該位置沒有開放房間
相鄰的 Z 座標。


(map-string)=
### 地圖字串

新地圖的建立從_地圖字串_開始。這可以讓你“畫畫”
您的地圖，描述房間在 X、Y 座標系中的位置。
它透過鍵“map”新增到`XYMAP_DATA`。

```
MAPSTR = r"""

+ 0 1 2

2 #-#-#
     /
1 #-#
  |  \
0 #---#

+ 0 1 2

"""

```

在座標軸上，只有兩個 `+` 是有意義的 - 數字是
_可選_，所以這是等效的：

```
MAPSTR = r"""

+

  #-#-#
     /
  #-#
  | \
  #---#

+

"""
```
> 儘管它是可選的，但強烈建議您新增數字
> 你的斧頭——如果只是為了你自己的理智。

座標區開始_向右兩格_和_兩格
下面/上面_強制`+`標誌（標記地圖區域的角落）。
Origo `(0,0)` 位於左下角（因此 X 座標向右增加，
Y 座標向頂部增加）。高度/寬度沒有限制
地圖可以，但是將一個大世界分成多個地圖可以更容易
組織。

網格上的位置很重要。每隔_秒_放置完整座標
沿所有軸的空間。這些「完整」座標之間是 `.5` 座標。
請注意，遊戲中產生了 _no_ `.5` 座標；它們只被使用
在地圖字串中留出空間來描述房間/節點如何相互連結。

    + 0 1 2 3 4 5

    4           E
       B
    3

    2         D

    1    C

    0 A

    + 0 1 2 3 4 5

- `A` 位於原點，`(0, 0)`（「完整」座標）
- `B` 位於 `(0.5, 3.5)`
- `C` 位於 `(1.5, 1)`
- `D` 位於 `(4, 2)`（「完整」座標）。
- `E` 是地圖的右上角，位於 `(5, 4)`（「完整」座標）

地圖字串由兩個主要的實體類別組成 - _nodes_ 和 _links_。
- _node_ 通常代表遊戲中的_room_（但並非總是如此）。節點必須
_始終_放置在「完整」座標上。
- _link_ 描述兩個節點之間的連線。在遊戲中，連結通常是
由_exits_表示。可以放一個連結
  座標空間中的任何位置（全座標和 0.5 座標）。多個
  連結通常「連結」在一起，但鏈必須始終以節點結束
  兩側。

> 即使連結鏈可能由多個步驟組成，例如 `#-----#`，
> 在遊戲中它仍然只代表一個「步驟」（e.g。你只往「東」走一次
> 從最左邊移動到最右邊的節點/房間）。


(map-legend)=
### 地圖圖例

可以有許多不同型別的_節點_和_連結_。而地圖
字串描述它們所在的位置，_地圖圖例_連線每個符號
在Python程式碼的地圖上。

```

LEGEND = {
    '#': xymap_legend.MapNode,
    '-': xymap_legende.EWMapLink
}

# added to XYMAP_DATA dict as 'legend': LEGEND below

```

圖例是可選的，圖例中未明確給出的任何符號都將
回退到預設圖例中的值[如下所述](#default-legend)。

- [MapNode](evennia.contrib.grid.xyzgrid.xymap_legend.MapNode)
是所有節點的基底類別。
- [MapLink](evennia.contrib.grid.xyzgrid.xymap_legend.MapLink)
是所有連結的基底類別。

當解析 _Map String_ 時，會在圖例中尋找每個找到的符號並
初始化到對應的MapNode/Link例項。

(important-nodelink-properties)=
#### 重要的節點/連結屬性

如果您想自訂地圖，這些都是相關的。 contrib已經來了
具有以各種方式使用這些屬性的全套地圖元素
（在下一節中描述）。

的一些有用的屬性
[MapNode](evennia.contrib.grid.xyzgrid.xymap_legend.MapNode)
類別（有關鉤子方法，請參閱類別檔案）：

- `symbol` (str) - 要從對映解析到此節點的字元。預設情況下這個
是 `'#'` 並且_必須_是單一字元（`\\` 除外，它必須
  被轉義以供使用）。無論這個值預設是什麼，它都會被替換為
  執行時由 legend-dict 中使用的符號執行。
- `display_symbol`（str 或 `None`）- 用於視覺化此節點
遊戲中。該符號的視覺大小仍然只能為 1，但您可以e.g。
  使用一些奇特的 unicode 字元（注意不同用戶端的編碼
  不過），或通常在其周圍新增顏色tags。 `.get_display_symbol`
  可以自訂該類別以動態產生該類別；預設情況下
  只回`.display_symbol`。如果設定為 `None`（預設），則 `symbol` 為
  使用過。
- `interrupt_path` (bool): 如果設定了此項，最短路徑演演算法將
正常包含該節點，但自動步進器在到達該節點時將停止，
  即使還沒有達到目標。這對於標記“點”很有用
  沿途或您預計無法到達的地方的興趣
  繼續沒有一些
  地圖未涵蓋的其他遊戲內動作（例如守衛或上鎖的門）
  等）。
- `prototype` (dict) - 用於重現此內容的預設 `prototype` dict
遊戲網格上的地圖元件。如果沒有專門覆蓋，則使用此值
  對於 `XYMAP_DATA` 的“原型”字典中的這個座標..如果不是
  給定，該座標不會產生任何內容（“虛擬”節點可以是
  由於各種原因很有用，主要是地圖轉換）。

的一些有用的屬性
[MapLink](evennia.contrib.grid.xyzgrid.xymap_legend.MapLink)
類別（有關鉤子方法，請參閱類別檔案）：

- `symbol` (str) - 要從對映解析到此節點的字元。這必須
可以是單一字元，`\\` 除外。這將被替換
  在執行時透過 legend-dict 中使用的符號。
- `display_symbol`（str 或 None）- 用於視覺化該節點
之後。此符號的視覺大小仍必須僅為 1，但您可以e.g。
  使用一些奇特的 unicode 字元（注意不同用戶端的編碼
  不過），或通常在其周圍新增顏色 tags 。為了進一步定製，
  可以使用`.get_display_symbol`。
- `default_weight` (int) - 此連結所涵蓋的每個連結方向都可以有其
單獨的重量（用於尋路）。如果沒有特定重量，則使用此
  在特定的連結方向上指定。  該值必須 >= 1，並且可以
  如果連結不那麼受歡迎，則應高於 1。
- `directions` (dict) - 這指定從哪條連結邊緣到哪條其他邊緣
link-edge 此連結已連線；將連結的 sw 邊緣連線到其
  東邊將寫為 `{'sw': 'e'}` 並讀取“從西南連線”
  向東' 這個 ONLY 採用基本方向（不是向上/向下）。請注意，如果您
  想要雙向連結，也必須反向（東向西南）
  補充道。
- `weights (dict)` 這將連結的起始方向對應到權重。所以對於
`{'sw': 'e'}` 連結，權重將指定為 `{'sw': 2}`。如果沒有給出，則
  連結將使用`default_weight`。
- `average_long_link_weights` (bool)：這適用於某個連結中的*第一個*連結
僅節點。  當追蹤到另一個節點的連結時，可能會出現多個連結
  涉及其中，各有分量。  因此對於具有預設權重的連結鏈，`#---#`
  則總權重為 3。使用此設定（預設），權重將
  為 (1+1+1) / 3 = 1。也就是說，對於均勻加權的連結，
  連結鏈並不重要（這通常是最有意義的）。
- `direction_aliases` (dict): 尋路時顯示方向時，
人們可能想要顯示與地圖上主要方向不同的「方向」。
  例如，“向上”可能在地圖上視覺化為“n”運動，但找到的
  此連結的路徑應顯示為“u”。在這種情況下，別名將是
  `{'n': 'u'}`。
- `multilink` (bool)：如果設定，此連結接受來自所有方向的連結。它
通常會使用自訂 `.get_direction` 方法來確定這些是什麼
  基於周圍的拓撲。此設定對於避免無限
  當此類多重連結彼此相鄰時會發生迴圈。
- `interrupt_path` (bool)：如果設定，最短路徑解決方案將包含此
連結正常，但自動步進器將停止實際移動超過此
  連結。
- `prototype` (dict) - 用於重現此內容的預設 `prototype` dict
遊戲網格上的地圖元件。這僅與*第一個*連結輸出相關
  節點的（連結的延續僅用於確定其
  目的地）。這可以在每個方向的基礎上被覆蓋。
- `spawn_aliases`（字典）：對映 `{direction: (key, alias, alias,...),}` 到
從此連結產生實際退出時使用。如果沒有給出，則提供一組健全的
  將使用預設值（`n=(north, n)` 等）。如果您使用任何一個，則這是必需的
  基本方向+上/下之外的自訂方向。出口的鑰匙
  （對於自動行走很有用）通常透過呼叫來檢索
  `node.get_exit_spawn_name(direction)`

下面是一個將地圖節點更改為紅色的範例
（也許是熔岩地圖？）：

```
from evennia.contrib.grid.xyzgrid import xymap_legend

class RedMapNode(xymap_legend.MapNode):
    display_symbol = "|r#|n"


LEGEND = {
   '#': RedMapNode
}

```

(default-legend)=
#### 預設圖例


下面是預設的地圖圖例。 `symbol` 是應該放在地圖中的內容
字串。它必須始終是單一字元。 `display-symbol` 是什麼
在遊戲中向玩家顯示地圖時實際上是視覺化的。這可能有
顏色等。所有類別都可以在 `evennia.contrib.grid.xyzgrid.xymap_legend` 中找到並且
包含它們的名稱是為了方便了解要涵蓋的內容。

```{eval-rst}
=============  ==============  ====  ===================  =========================================
symbol         display-symbol  type  class                description
=============  ==============  ====  ===================  =========================================
#              #               node  `BasicMapNode`       A basic node/room.
T                              node  `MapTransitionNode`  Transition-target for links between maps
                                                          (see below)
I (letter I)   #               node  `InterruptMapNode`   Point of interest, auto-step will always
                                                          stop here (see below).
\|             \|              link  `NSMapLink`          North-South two-way
\-             \-              link  `EWMapLink`          East-West two-way
/              /               link  `NESWMapLink`        NorthEast-SouthWest two-way
\\             \\              link  `SENWMapLink`        NorthWest two-way
u              u               link  `UpMapLink`          Up, one or two-way (see below)
d              d               link  `DownMapLink`        Down, one or two-way (see below)
x              x               link  `CrossMapLink`       SW-NE and SE-NW two-way
\+             \+              link  `PlusMapLink`        Crossing N-S and E-W two-way
v              v               link  `NSOneWayMapLink`    North-South one-way
^              ^               link  `SNOneWayMapLink`    South-North one-way
<              <               link  `EWOneWayMapLink`    East-West one-way
>              >               link  `WEOneWayMapLink`    West-East one-way
o              o               link  `RouterMapLink`      Routerlink, used for making link 'knees'
                                                          and non-orthogonal crosses (see below)
b              (varies)        link  `BlockedMapLink`     Block pathfinder from using this link.
                                                          Will appear as logically placed normal
                                                          link (see below).
i              (varies)        link  `InterruptMapLink`   Interrupt-link; auto-step will never
                                                          cross this link (must move manually, see
                                                          below)
t                              link  `TeleporterMapLink`  Inter-map teleporter; will teleport to
                                                          same-symbol teleporter on the same map.
                                                          (see below)
=============  ==============  ====  ===================  =========================================

```



(map-nodes)=
#### 地圖節點

基本地圖節點（`#`）通常代表遊戲世界中的一個「房間」。友情連結
可以從 8 個基本方向中的任何一個連線到節點，但由於節點
必須_僅_存在於完整座標上，它們永遠不能直接出現在
彼此。

    \|/
    -#-
    /|\

    ##     invalid!

所有連結或連結鏈_必須_以兩側的節點結束。


    #-#-----#

    #-#-----   invalid!

(one-way-links)=
#### 單向連結

`>`、`<`、`v`、`^` 用於表示單向連結。這些指標應該
可以是連結鏈中的_first_或_last_（將它們視為箭頭）：

    #----->#
    #>-----#

這兩個是等效的，但第一個可以說更容易閱讀。這也是
解析速度更快，因為最右邊節點上的解析器立即看到
那個方向的連結是無法從那個方向透過的。

> 請注意，`\` 和 `/` 方向沒有單向等效項。這
> 不是因為做不到而是因為沒有明顯的ASCII
> 表示對角箭頭的字元。如果你想要它們，很容易
> 子類化現有的單向地圖圖例以新增對角線的單向版本
> 運動也是如此。

(up-and-down-links)=
#### 上行鏈路和下行鏈路

像 `u` 和 `d` 這樣的連結沒有明確的指示它們的方向
連線（與 e.g、`|` 和 `-` 不同）。

因此，放置它們（以及許多類似型別的地圖元素）需要
方向視覺上清晰。例如，多個連結無法連線到
上下連結（不清楚哪個通往哪裡），如果與一個節點相鄰，則
link 將優先連線到該節點。以下是一些範例：

        #
        u    - moving up in BOTH directions will bring you to the other node (two-way)
        #

        #
        |    - one-way up from the lower node to the upper, south to go back
        u
        #

        #
        ^    - true one-way up movement, combined with a one-way 'n' link
        u
        #

        #
        d    - one-way up, one-way down again (standard up/down behavior)
        u
        #

        #u#
        u    - invalid since top-left node has two 'up' directions to go to
        #

        #     |
        u# or u-   - invalid since the direction of u is unclear
        #     |


(interrupt-nodes)=
#### 中斷節點

中斷節點（`I`、`InterruptMapNode`）是像其他節點一樣運作的節點。
節點，除非它被認為是“興趣點”並且該節點的自動行走
`goto` 指令將始終在此位置停止自動步進。

＃-＃-我-＃-＃

因此，如果從左到右自動行走，自動行走將正確地繪製路徑
到最後的房間，但總是停在`I`節點。如果使用者_開始_於
`I` 房間，他們會不間斷地離開它（所以你可以
再次手動執行 `goto` 以恢復自動步驟）。

這個房間的用途是預測地圖未涵蓋的街區。例如
這個房間裡可能有一名警衛會逮捕你，除非你
向他們展示正確的檔案——試圖自動走過他們是很糟糕的！

預設情況下，這個節點對玩家來說就像一個普通的`#`。

(interrupt-links)=
#### 中斷連結

中斷連結（`i`，`InterruptMapLink`）相當於
`InterruptMapNode`，但它適用於連結。雖然探路者將
正確地追蹤到另一側的路徑，自動步進器將永遠不會穿過
中斷連結 - 您必須「手動」執行此操作。與上/下連結類似，
InterruptMapLink 的放置必須確保其方向明確（使用
連結到附近節點的優先權）。

＃-＃-＃我＃-＃

當從左向右尋路時，尋路者會剛好找到最後一個房間
可以，但是自動步進時，它總是停在左邊的節點處
`i` 連結的。重新執行 `goto` 並不重要。

這對於自動處理不屬於地圖的遊戲內區塊很有用。
一個例子是鎖著的門 - 而不是讓自動步進器嘗試
要穿過門出口（並且失敗），它應該停下來讓使用者
在他們可以繼續之前手動跨越閾值。

與中斷節點相同，中斷連結看起來像是使用者預期的連結
（所以在上面的例子中，它將顯示為`-`）。

(blocked-links)=
#### 被阻止的連結

攔截者（`b`、`BlockedMapLink`）表示探路者不應使用的路線。的
探路者會將其視為不可通行，即使它將作為一個生成
遊戲中正常退出。


#-#-#b#-#

無法從左到右自動步進，因為探路器會
將`b`（塊）視為那裡沒有連結（從技術上講，它設定了
連結的 `weight` 到非常高的數字）。玩家需要自動走到
房間就在街區左側，手動跨過街區，然後
從那裡繼續。

這對於實際的街區（也許房間裡充滿了瓦礫？）和在
為了避免玩家自動走進隱藏區域或找到出去的路
迷宮等。只需將迷宮的出口隱藏在方塊後面即可`goto exit`
將無法運作（誠然，人們可能想完全關閉尋路功能
此類地圖）。


(router-links)=
#### 路由器連結

路由器（`o`、`RouterMapLink`）允許透過連結連線節點
透過創造「膝蓋」來調整角度。

#----o
	| \
	#-#-# o
	       |
#-o

在上面，您可以從左上角的房間和最底部的房間之間向東移動
房間。請記住，連結的長度並不重要，因此在遊戲中這將
僅一步（兩個房間各有一個出口 `east`）。

路由器可以連結多個連線，只要有盡可能多的連線
「傳入」因為有「傳出」連結。如果有疑問，系統將假定
連結將繼續到路由器另一側的傳出連結。

          /
        -o    - this is ok, there can only be one path, w-ne

         |
        -o-   - equivalent to '+': one n-s and one w-e link crossing
         |

        \|/
        -o-   - all links are passing straight through
        /|\

        -o-   - w-e link pass straight through, other link is sw-s
        /|

        -o    - invalid; impossible to know which input goes to which output
        /|


(teleporter-links)=
#### 傳送器連結

傳送器 (`TeleportMapLink`) 總是成對使用相同的地圖符號
（預設為`'t'`）。  當移動到一個連結時，移動會繼續進行
匹配傳送連結。該對必須位於同一 XYMap 且兩側
必須連線/連結到一個節點（像所有連結一樣）。只有單一連結（或節點）可以
連線到傳送連結。

尋路也會在傳送過程中正常運作。

#-t t-#

從最左邊的節點向東移動將使您出現在最右邊的節點
反之亦然（將兩個 `t` 視為認為它們位於同一位置）。

傳送運動始終是雙向的，但您可以使用單向連結
建立單向傳送的效果：

#-tt>#

在此範例中，您可以透過傳送向東移動，但不能向西移動，因為
傳送連結隱藏在單向出口後面。

#-t#（無效！）

上述內容無效，因為只有一個連結/節點可以連線到傳送點
時間。

您可以在同一張地圖上擁有多個傳送，透過為每一對分配一個
地圖圖例中不同的（未使用的）獨特符號：


```python
# in your map definition module

from evennia.contrib.grid.xyzgrid import xymap_legend

MAPSTR = r"""

+ 0 1 2 3 4

2 t q #   q
  | v/ \  |
1 #-#-p #-#
  |       |
0 #-t p>#-#

+ 0 1 2 3 4

"""

LEGEND = {
    't': xymap_legend.TeleporterMapLink,
    'p': xymap_legend.TeleporterMapLink,
    'q': xymap_legend.TeleportermapLink,
}


```

(map-transition-nodes)=
#### 地圖轉換節點

地圖轉換 (`MapTransitionNode`) 在 XYMaps（a
Z 座標過渡，如果你願意的話），就像從「Dungeon」地圖步行到
「城堡」地圖。與其他節點不同，MapTransitionNode 永遠不會生成
進入一個實際的房間（它沒有原型）。它只持有XYZ
座標指向另一張地圖上的某個位置。通往 _to_ 的連結
節點將使用這些座標來建立指向那裡的出口。只有一張
連結可能會導致這種型別的節點。

與 `TeleporterMapLink` 不同，不需要匹配
`MapTransitionNode` 在另一張地圖上 - 過渡可以選擇傳送
玩家到另一張地圖上的_任何_有效座標。

每個 MapTransitionNode 都有一個屬性 `target_map_xyz` 儲存 XYZ
玩家走向這個節點時應該到達的座標。這個
必須在子類別中為每次轉換進行自訂。

如果有多個轉換，則應設定單獨的轉換類
新增了不同的地圖圖例符號：


```python
# in your map definition module (let's say this is mapB)

from evennia.contrib.grid.xyzgrid import xymap_legend

MAPSTR = r"""

+ 0 1 2

2   #-C
    |
1 #-#-#
     \
0 A-#-#

+ 0 1 2


"""

class TransitionToMapA(xymap_legend.MapTransitionNode):
    """Transition to MapA"""
    target_map_xyz = (1, 4, "mapA")

class TransitionToMapC(xymap_legend.MapTransitionNode):
    """Transition to MapB"""
    target_map_xyz = (12, 14, "mapC")

LEGEND = {
    'A': TransitionToMapA
    'C': TransitionToMapC

}

XYMAP_DATA = {
    # ...
    "map": MAPSTR,
    "legend": LEGEND
    # ...
}

```

從 `(1,0)` 向西移動將到達 MapA 的 `(1,4)`，從
`(1,2)` 會將您帶到 MapC 上的 `(12,14)`（假設這些地圖存在）。

地圖轉換總是單向的，並且可以導致 _any_ 的座標
另一張地圖上的現有節點：

地圖1 地圖2

#-T#-#---#-#-#-#

例如，向東向 `T` 移動的玩家最終可能會到達從 `#` 開始的第 4 個位置
如果需要的話，可以在map2的左邊（即使它在視覺上沒有意義）。
無法從那裡返回map1。

若要創造雙向過渡的效果，可以設定映象
另一張地圖上的轉換節點：

城市地圖 地下城地圖

#-T T-#


上面每張地圖的轉換節點都有 `target_map_xyz` 指向
其他地圖的 `#` 節點的座標（_不是_其他 `T`，即不是
產生並導致出口找不到目的地！）。結果是
可以向東進入地牢，然後立即向西返回城市
跨越地圖邊界。

(prototypes)=
### 原型

[原型](../Components/Prototypes.md) 是描述如何_產生_新例項的字典
一個物體的。上面的每個_節點_和_連結_都有一個預設原型
允許 `evennia xyzgrid spawn` 指令將它們轉換為
[XYZRoom](evennia.contrib.grid.xyzgrid.xyzroom.XYZRoom)
或分別為 [XYZExit](evennia.contrib.grid.xyzgrid.xyzroom.XYZRoom)。

預設原型位於`evennia.contrib.grid.xyzgrid.prototypes`（已新增
在安裝此 contrib) 期間，`prototype_key`s `"xyz_room"` 和
`"xyz_exit"` - 使用這些作為 `prototype_parent` 新增您自己的自訂原型。

XYMap-data 字典的 `"prototypes"` 鍵可讓您自訂
原型用於 XYMap 中的每個座標。坐標給出為
`(X, Y)` 用於節點/房間，`(X, Y, direction)` 用於連結/出口，其中
方向是「n」、「ne」、「e」、「se」、「s」、「sw」、「w」、「nw」、「u」或「d」之一。對於
退出，建議_不_設定 `key`，因為這是產生的
自動由網格產生器按預期進行（“north”，別名“n”，對於
範例）。

特殊座標是`*`。這充當該座標的萬用字元並且
允許您新增用於房間的“預設”原型。


```python

MAPSTR = r"""

+ 0 1

1 #-#
   \
0 #-#

+ 0 1


"""


PROTOTYPES = {
    (0,0): {
	"prototype_parent": "xyz_room",
	"key": "End of a the tunnel",
	"desc": "This is is the end of the dark tunnel. It smells of sewage."
    },
    (0,0, 'e') : {
	"prototype_parent": "xyz_exit",
	"desc": "The tunnel continues into darkness to the east"
    },
    (1,1): {
	"prototype_parent": "xyz_room",
	"key": "Other end of the tunnel",
	"desc": The other end of the dark tunnel. It smells better here."
    }
    # defaults
    ('*', '*'): {
    	"prototype_parent": "xyz_room",
	"key": "A dark tunnel",
	"desc": "It is dark here."
    },
    ('*', '*', '*'): {
	"prototype_parent": "xyz_exit",
	"desc": "The tunnel stretches into darkness."
    }
}

XYMAP_DATA = {
    # ...
    "map": MAPSTR,
    "prototypes": PROTOTYPES
    # ...
}

```

當產生上面的地圖時，位於地圖左下角和右上角的房間
地圖將獲得自訂描述和名稱，而其他地圖將具有預設描述和名稱
價值觀。一個出口（左下房間的東出口會有一個
自訂描述。

> 如果您習慣使用原型，您可能會注意到我們沒有新增
> `prototype_key` 對於上述原型。這通常是每個人都需要的
> 原型。這是為了方便 - 如果
> 你不加`prototype_key`，網格會自動產生一個
> you - 基於要產生的節點/連結的當前 XYZ（+ 方向）的雜湊值。

如果您發現自己在生成後更改了原型
網格/地圖，您可以再次重新執行`evennia xyzgrid spawn`；變化將是
拾取並應用於現有物件。

(extending-the-base-prototypes)=
#### 擴充套件基礎原型

預設原型位於 `evennia.contrib.grid.xyzgrid.prototypes` 和
對於地圖上的原型，應包含為 `prototype_parents`。會嗎
能夠更改這些並將更改應用到所有
網格？您可以透過將以下內容新增至 `mygame/server/conf/settings.py` ：

    XYZROOM_PROTOTYPE_OVERRIDE = {"typeclass": "myxyzroom.MyXYZRoom"}
    XYZEXIT_PROTOTYPE_OVERRIDE = {...}


> 如果您涵蓋原型中的 typeclass，則 typeclass 使用 **MUST**
> 從 `XYZRoom` 和/或 `XYZExit` 繼承。 `BASE_ROOM_TYPECLASS` 和
> `BASE_EXIT_TYPECLASS` 設定不會有幫助 - 這些仍然有用
> 但非 xyzgrid 房間/出口。

僅新增您想要更改的內容 - 這些字典將_擴充套件_預設父級
原型而不是取代它們。只要您定義地圖的原型
要使用 `"xyz_room"` 和/或 `"xyz_exit"` 的 `prototype_parent`，您的更改
現在將被應用。您可能需要重新生成網格並重新載入伺服器
經過這樣的改變之後。

(options)=
### 選項

例如，`XYMAP_DATA` 字典的最後一個元素是 `"options"`

```
XYMAP_DATA = {
    # ...
    "options": {
	"map_visual_range": 2
    }
}

```

`options` 字典作為 `**kwargs` 傳遞到 `XYZRoom.return_appearance`
在遊戲中視覺化地圖時。它允許顯示不同的地圖
彼此不同（請注意，雖然這些選項很方便，但
當然也可以透過繼承來完全涵蓋 `return_appearance`
`XYZRoom` 然後在你的原型中指向它）。

預設的視覺化是這樣的：

```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                     #---#
                                    /
                                   @-
-~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dungeon Entrance
To the east, a narrow opening leads into darkness.
Exits: northeast and east

```

- `map_display`（布林值）：這將完全關閉該地圖的顯示。
- `map_character_symbol` (str)：用於在地圖上顯示「您」的符號。它可以
有顏色，但只能佔用一個字元空間。預設情況下這是一個
  綠色`@`。
- `map_visual_range` (int): 這是距離你目前位置的距離
看。
- `map_mode` (str)：這是“節點”或“掃描”，影響視覺效果
計算範圍。
  在「節點」模式下，範圍顯示距離您可以看到的_節點_數量。在“掃描”中
  在模式下，您可以看到許多_螢幕上的角色_遠離您的角色。
  為了視覺化，假設這是完整的地圖（其中“@”是字元位置）：

      #----------------#
      |                |
      |                |
      # @------------#-#
      |                |
      #----------------#

這是玩家在「節點」模式下看到的 `map_visual_range=2` 的內容：

      @------------#-#

....並且在“掃描”模式下：

      |
      |
      # @--
      |
      #----

“節點”模式的優點是僅顯示連線的連結，並且
  非常適合導航，但根據地圖，它可以包含相當多的節點
  視覺上離你很遠。 「掃描」模式可能會意外顯示未連線的情況
  地圖的一部分（請參閱上面的範例），但限制範圍可以用作
  隱藏訊息的方式。

這是玩家在「節點」模式下看到的 `map_visual_range=1` 的內容：

      @------------#

....並且在“掃描”模式下：

      @-

例如，可以使用“節點”來繪製戶外/城鎮地圖，並使用“掃描”來繪製
  探索地牢。

- `map_align` (str)：「r」、「c」或「l」之一。這會相對於地圖移動
房間文字。預設情況下它是居中的。
- `map_target_path_style`：如何視覺化到達目標的路徑。這是一個
採用 `{display_symbol}` 格式 tag 的字串。這將被替換
  路徑中每個地圖元素的`display_symbol`。預設情況下這是
  `"|y{display_symbol}|n"`，即路徑為黃色。
- `map_fill_all` (bool): 地圖區域是否應填滿整個用戶端寬度
（預設）或變更為始終僅與房間描述一樣寬。注意事項
  在後一種情況下，地圖最終可能會在用戶端視窗中“跳舞”
  如果描述的寬度差異很大。
- `map_separator_char` (str)：用於地圖之間分隔線的字元
以及房間描述。預設為 `"|x~|n"` - 深灰色波浪線。


更改已生成的地圖的選項不需要重新生成
地圖，但你_確實_需要重新載入伺服器！

(about-the-pathfinder)=
### 關於探路者

新的 `goto` 指令舉例說明瞭 _Pathfinder_ 的使用。這個
是一種計算節點（房間）之間最短路徑的演演算法
XY-任意大小和複雜度的地圖。可以讓玩家快速移動到
某個位置（如果他們知道該位置的名稱）。以下是一些有關的詳細資訊

- 探路器解析節點和連結以建立距離矩陣
從每個節點移動到 XYMap 上的_所有_其他節點。路徑
  使用以下方法解決
  [Dijkstra演演算法](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)。
- 對於非常大的地圖，探路者的矩陣可能需要很長時間才能建造。
因此它們被快取為 pickled 二進位檔案
  `mygame/server/.cache/` 並且僅在地圖更改時才重建。他們可以安全地
  刪除（您也可以使用 `evennia xyzgrid initpath` 強制建立/重建快取檔案）。
- 一旦被快取，探路器就會很快（在上面找到 500 步的最短路徑）
20 000 個節點/房間耗時低於 0.1 秒）。
- 重要的是要記住，探路器只能在 _one_ XYMap 內工作。
它不會找到跨越地圖轉換的路徑。如果這是一個問題，可以考慮
  使遊戲的所有區域成為一個XYMap。這可能工作得很好，但使它
  更難向網格新增新地圖或從網格中刪除新地圖。
- 探路器實際上會總結每個連結的「權重」來確定哪個是
「最便宜」（最短）的路線。預設情況下，除阻止連結之外的每個連結都有
  成本為 1（因此成本等於在節點之間移動的步數）。
  然而，單一連結可以將其更改為更高/更低的權重（必須 >=1）。
  權重越高意味著探路者使用該路線的可能性就越小
  與其他相比（這也可能讓使用者感到困惑，因此請小心使用）。
- 探路者將_平均_長鏈條的重量。由於所有連結
預設具有相同的權重 (=1)，這意味著
  `#-#` 與 `#----#` 具有相同的移動成本，儘管它在視覺上「更短」。
  可以透過使用連結來更改每個連結的此行為
`average_long_link_weights = False`。


(xyzgrid-1)=
## XYZGrid

`XYZGrid` 是一個 [全域 Script](../Components/Scripts.md)，它儲存了所有 `XYMap` 物件
網格。任何時候都只能創造一個 XYZGrid。

要在程式碼中存取網格，有多種方法：

- 您可以像搜尋其他Script 一樣搜尋網格。它被命名為“XYZGrid”。

網格 = evennia.search_script("XYZGrid")[0]

（`search_script` 總是回傳一個清單）
- 你可以用`evennia.contrib.grid.xyzgrid.xyzgrid.get_xyzgrid`得到它

從evennia.contrib.grid.xyzgrid.xyzgrid匯入get_xyzgrid
	網格=get_xyzgrid()

這將“總是”返回一個網格，如果沒有，則建立一個空網格
  以前存在。所以這也是建立新網格的建議方法
  在程式碼中。
- 您可以透過造訪現有的 XYZRoom/Exit 的 `.xyzgrid` 來取得它
財產

grid = self.caller.location.xyzgrid # 如果目前在網格房間

網格類別上的大多數工具都與載入/新增和刪除地圖有關，
您應該使用 `evennia xyzgrid` 指令來執行某些操作。但有
還有幾種普遍有用的方法：

- `.get_room(xyz)` - 在特定座標`(X, Y, Z)`處取得房間。這將
僅當地圖實際上首先生成時才有效。例如
  `.get_room((0,4,"the dark castle))`。使用 `'*'` 作為萬用字元，所以
  `.get_room(('*','*',"the dark castle))` 會讓你在黑暗中產生所有房間
 城堡地圖。
- `.get_exit(xyz, name)` - 獲得特定出口，e.g。
`.get_exit((0,4,"the dark castle", "north")`。您也可以使用 `'*'` 作為
  萬用字元。

也可以直接存取 `XYZGrid` 上特定的已解析 `XYMap` 物件：

- `.grid` - 這是所有 XYMaps 的實際（快取）儲存，如 `{zcoord: XYMap,...}`
- `.get_map(zcoord)` - 取得特定的XYMap。
- `.all_maps()` - 取得所有 XYMaps 的清單。

除非您想大幅改變地圖的工作方式（或瞭解它的作用），否則您
可能永遠不需要修改 `XYZMap` 物件本身。你可能想要
但知道如何呼叫 find 探路者：

- `xymap.get_shortest_path(start_xy, end_xy)`
- `xymap.get_visual_range(xy, dist=2, **kwargs)`

請參閱 [XYMap](xymap) 檔案瞭解
詳細資訊。


(xyzroom-and-xyzexit)=
## XYZRoom 和 XYZExit

這些是新的自訂 [Typeclasses](../Components/Typeclasses.md)，位於
`evennia.contrib.xyzgrid.xyzroom`。他們擴充套件了基礎`DefaultRoom`並且
`DefaultExit` 瞭解它們的 `X`、`Y` 和 `Z` 座標。

```{warning}

    You should usually **not** create XYZRooms/Exits manually. They are intended
    to be created/deleted based on the layout of the grid. So to add a new room, add
    a new node to your map. To delete it, you remove it. Then rerun
    **evennia xyzgrid spawn**. Having manually created XYZRooms/exits in the mix
    can lead to them getting deleted or the system getting confused.

    If you **still** want to create XYZRoom/Exits manually (don't say we didn't
    warn you!), you should do it with their `XYZRoom.create()` and
    `XYZExit.create()` methods. This makes sure the XYZ they use are unique.

```

`XYZRoom`、`XYZExit` 上有用的（額外）屬性：

- `xyz` 實體的`(X, Y, Z)`座標，例如`(23, 1, "greenforest")`
- `xyzmap` 這屬於`XYMap`。
- `get_display_name(looker)` - 這已修改為顯示座標
如果您具有 Builder 或更高許可權，則實體以及 `#dbref`。
- `return_appearance(looker, **kwargs)` - 這已被廣泛修改為
`XYZRoom`，顯示地圖。將出現 `XYMAP_DATA` 中給出的 `options`
  作為此方法的`**kwargs`，如果您覆寫此方法，您可以自訂
  深度地圖顯示。
- `xyz_destination`（僅適用於`XYZExits`） - 這給出了 xyz 座標
出口的目的地。

座標儲存為 [Tags](../Components/Tags.md)，其中房間和出口均為 tag
類別 `room_x_coordinate`、`room_y_coordinate` 和 `room_z_coordinate`
而出口除了 tags 之外還使用相同的內容作為其目的地，並使用 tag
類別 `exit_dest_x_coordinate`、`exit_dest_y_coordinate` 和
`exit_dest_z_coordinate`。

這使得透過座標查詢資料庫變得更容易，每個typeclass提供
自訂管理器方法。過濾器方法允許使用 `'*'` 作為萬用字元。

```python

# find a list of all rooms in map foo
rooms = XYZRoom.objects.filter_xyz(('*', '*', 'foo'))

# find list of all rooms with name "Tunnel" on map foo
rooms = XYZRoom.objects.filter_xyz(('*', '*', 'foo'), db_key="Tunnel")

# find all rooms in the first column of map footer
rooms = XYZRoom.objects.filter_xyz((0, '*', 'foo'))

# find exactly one room at given coordinate (no wildcards allowed)
room = XYZRoom.objects.get_xyz((13, 2, foo))

# find all exits in a given room
exits = XYZExit.objects.filter_xyz((10, 4, foo))

# find all exits pointing to a specific destination (from all maps)
exits = XYZExit.objects.filter_xyz_exit(xyz_destination=(13,5,'bar'))

# find exits from a room to anywhere on another map
exits = XYZExit.objects.filter_xyz_exit(xyz=(1, 5, 'foo'), xyz_destination=('*', '*', 'bar'))

# find exactly one exit to specific destination (no wildcards allowed)
exit = XYZExit.objects.get_xyz_exit(xyz=(0, 12, 'foo'), xyz_destination=(5, 2, 'foo'))

```

您可以透過讓網格產生您自己的子類別來自訂 XYZRoom/Exit
其中。為此，您需要覆蓋用於生成房間的原型
網格。最簡單的方法是修改設定中的基本原型父母（請參閱
[XYZRoom 和 XYZExit](#xyzroom-and-xyzexit) 以上部分）。

(working-with-the-grid)=
## 使用網格

使用網格的工作流程通常如下：

1. 準備一個有_Map String_、_Map Legend_、_Prototypes_和的模組
_Options_ 打包成字典`XYMAP_DATA`。每個模組包含多個地圖
   透過將幾個 `XYMAP_DATA` 加到變數 `XYMAP_DATA_LIST` 來代替。
2. 如果您的地圖包含`TransitionMapNodes`，則目標地圖也必須是
新增或已存在於網格中。如果沒有，您應該跳過該節點
   現在（否則在生成時你會遇到錯誤，因為退出目的地
   不存在）。
2. 執行 `evennia xyzgrid add <module>` 將地圖註冊到網格中。如果沒有
網格已經存在，它將由此建立。修復報告的任何錯誤
   解析器。
3. 使用 `evennia xyzgrid show <zcoord>` 檢查已解析的對映並確保
他們看起來還不錯。
4. 執行 `evennia xyzgrid spawn` 將地圖產生/更新為實際的 `XYZRoom`s 並且
`XYZExit`s。
5. 如果您願意，現在可以透過常用的建置指令手動調整網格。
您可以在網格原型中執行_未_指定的任何操作
   在遊戲中本地修改 - 只要整個房間/出口不被刪除，
   `evennia xyzgrid spawn` 不會影響這些。  您也可以挖掘/開啟
   退出到「嵌入」網格中的其他房間。這些出口不得命名
   網格方向之一（北、東北等，也不是上/下）或網格
   將在下一次 `evennia xyzgrid spawn` 執行中刪除它（因為它不在地圖上）。
6. 如果您想新增新的網格房間/出口，您應該_始終_這樣做
修改 _Map String_ 然後重新執行 `evennia xyzgrid spawn` 到
   應用更改。

(details)=
## 細節

預設 Evennia 的房間是非歐幾裡得的 - 他們可以連線
彼此之間可以有任何型別的退出，而不必有明確的
相對於彼此的位置。這提供了最大的靈活性，但許多遊戲
想要使用基本運動（向北、向東等）以及尋找等功能
兩點之間的最短路徑。

這 contrib 強制每個房間存在於 3 維 XYZ 網格上，並且
實現非常有效率的尋路以及顯示工具
您目前的視覺範圍和許多相關功能。

網格的房間完全由遊戲外部控制，使用
python 模組，帶有定義遊戲地圖的字串和字典。這是
可以將網格房間與非網格房間結合起來，並且您可以裝飾
網格房間在遊戲中隨心所欲，但不能產生新的網格
房間，無需在遊戲外編輯地圖檔。

(installation-1)=
## 安裝

1. 如果您以前沒有安裝過，請安裝額外的 contrib 要求。
您可以透過執行 `pip install evennia[extra]` 來執行此操作，或者如果您使用 `git` 來執行此操作
   安裝，從 `evennia/` 儲存庫執行 `pip install --upgrade -e.[extra]`
   資料夾。
2. 匯入並將 `evennia.contrib.grid.xyzgrid.commands.XYZGridCmdSet` 新增到
`CharacterCmdset` cmdset 在 `mygame/commands.default_cmds.py` 中。重新載入
   伺服器。這使得 `map`、`goto/path` 和修改後的 `teleport` 和
   `open` 遊戲中可用指令。
3. 編輯`mygame/server/conf/settings.py`並設定

        EXTRA_LAUNCHER_COMMANDS['xyzgrid'] = 'evennia.contrib.grid.xyzgrid.launchcmd.xyzcommand'

4. 執行新的 `evennia xyzgrid help` 以取得有關如何產生網格的說明。

(example-usage)=
## 用法範例

安裝後，執行以下操作（從指令列，其中
`evennia` 指令可用）來安裝範例網格：

    evennia xyzgrid init
    evennia xyzgrid add evennia.contrib.grid.xyzgrid.example
    evennia xyzgrid list
    evennia xyzgrid show "the large tree"
    evennia xyzgrid show "the small cave"
    evennia xyzgrid spawn
    evennia reload

（記住在生成操作後重新載入伺服器）。

現在您可以登入
伺服器並執行 `teleport (3,0,the large tree)` 傳送到地圖中。

您可以使用`open togrid = (3, 0, the large tree)`開啟永久（單向）
從目前位置退出到網格中。回到無網格狀態
位置只需站在網格房間中並開啟一個新的出口即可：
`open tolimbo = #2`。

嘗試 `goto view` 到樹頂，`goto dungeon` 到樹下
地牢入口在樹的底部。


----

<small>此檔案頁面是從`evennia\contrib\grid\xyzgrid\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
