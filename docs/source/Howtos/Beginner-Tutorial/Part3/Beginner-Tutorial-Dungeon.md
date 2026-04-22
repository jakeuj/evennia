(procedurally-generated-dungeon)=
# 程式生成的地下城

我們在[關於房間的課程](./Beginner-Tutorial-Rooms.md)中討論的房間都是_手動_生成的。也就是說，人類建造者必須坐下來手動產生每個房間，無論是在遊戲中還是使用程式碼。

在本課中，我們將探索構成遊戲地下城的房間的_程式_生成。程式性意味著它的房間會在玩家探索時自動和半隨機地生成，每次都會建立不同的地下城佈局。

(design-concept)=
## 設計理念

這描述了程式生成應該如何在高階別上工作。在我們開始編寫程式碼之前理解這一點很重要。

我們假設我們的地下城存在於 2D 平面上（x，y，無 z 方向）。我們只會使用 N、E、S、W 羅盤方向，但這種設計沒有理由不能與 SE、NW 等一起使用，除了這可能會讓玩家更難想像。更多可能的方向也使其更有可能產生碰撞和單向出口（見下文）。

這個設計非常簡單，但僅僅透過一些設定，它就可以產生非常不同感覺的地下城系統。

(the-starting-room)=
### 起始房間

這個想法是所有玩家都會從井裡下降到地牢的起點。井的底部是一個靜態建立的房間，不會改變。

```{code-block}
:caption: Starting room
            
                 Branch N                
                    ▲                    
                    │                    
           ┌────────┼────────┐           
           │        │n       │           
           │        ▼        │           
           │                 │           
           │                e│           
Branch W ◄─┼─►     up▲     ◄─┼─► Branch E1
           │w                │           
           │                 │           
           │        ▲        │           
           │        │s       │           
           └────────┼────────┘           
                    │                    
                    ▼                    
                 Branch S               
```

當你選擇這個房間的出口之一（除了帶你回到地面的出口）時，奇蹟就會發生。我們假設 PC 下降到起始房間並移動 `east`：

- 第一個向東走的人會產生一個新的「地下城分支」（圖中的分支E1）。與穿過任何其他出口時生成的地下城相比，這是一個單獨的地下城「例項」。在一個地下城分支內生成的房間永遠不會與另一個地下城分支的房間重疊。
- 計時器啟動。當此計時器處於活動狀態時，前往 `east` 的每個人最終都會到達分支 E1。這允許玩家組隊並協作來佔領一個分支。
- 計時器耗盡後，前往 `east` 的每個人都將進入_new_分支 E2。這是一個與分支 E1 沒有重疊的新分支。
- 分支 E1 和 E2 中的 PC 始終可以`west` 撤退到起始房間，但在計時器耗儘後，這現在是單向出口 - 如果他們這樣做，他們將無法返回到原來的分支。

(generating-new-branch-rooms)=
### 產生新的分支房間

每個地下城分支本身都會在（X，Y）座標網格上追蹤屬於該分支的房間佈局。

```{code-block}
:caption: Creating the eastern branch and its first room
                   ?         
                   ▲         
                   │         
┌─────────┐   ┌────┼────┐    
│         │   │A   │    │    
│         │   │   PC    │    
│  start◄─┼───┼─► is  ──┼──►?
│         │   │   here  │    
│         │   │    │    │    
└─────────┘   └────┼────┘    
                   │         
                   ▼         
```

起始房間始終位於座標`(0, 0)`。

地牢房間只有在實際移動到它時才會建立。在上面的例子中，PC從起始房間移動了`east`，這啟動了一個新的地下城分支。該分支機構還在坐標`(1,0)`處建立了一個新房間（房間`A`）。在本例中，它（隨機）在該房間中播種了三個出口 `north`、`east` 和 `south`。
由於這個分支剛剛建立，回到起始房間的出口仍然是雙向的。

這是地牢分支在生成新房間時遵循的程式：

- 它總是建立一個返回我們原來房間的出口。
- 它檢查目前地牢中有多少個未探索的出口。也就是說，我們還沒有走過多少個出口。這個數字絕對不能為零，除非我們想要一個可以「完成」的地下城。在任何給定時間開啟的未探索出口的最大數量是我們可以嘗試的設定。較小的最大數字會導致線性地牢，較大的數字會使地牢蔓延且像迷宮一樣。
- 外出出口（不返回我們來的地方的出口）是根據以下規則產生的：
    - 隨機建立 0 到房間允許的傳出出口數量以及分支目前允許開啟的未探索出口的預算。
    - 只有當這會在地牢分支中的某處留下至少一個未探索的出口時，才建立 0 個傳出出口（死衚衕）。
    - 不要建立一個將出口連線到先前生成的房間的出口（因此我們更喜歡通往新地點的出口而不是返回舊地點）
    - 如果先前建立的出口最終指向新建立的房間，則這是允許的，並且是唯一一次發生單向出口（如下例）。所有其他出口始終是雙向出口。這也提供了關閉地牢的唯一小機會，除了返回起點之外無法繼續。
    - 切勿建立返回起始房間的出口（e.g.從另一個方向）。返回起始房間的唯一方法是回溯。

在以下範例中，我們假設任何時間允許開啟的未探索出口的最大數量設定為 4。

```{code-block}
:caption: After four steps in the eastern dungeon branch
                    ?                                 
                   ▲                                 
                   │                                 
┌─────────┐   ┌────┼────┐                            
│         │   │A   │    │                            
│         │   │         │                            
│  start◄─┼───┼─      ──┼─►?                         
│         │   │    ▲    │                            
│         │   │    │    │                            
└─────────┘   └────┼────┘                            
                   │                                 
              ┌────┼────┐   ┌─────────┐   ┌─────────┐
              │B   │    │   │C        │   │D        │
              │    ▼    │   │         │   │   PC    │
          ?◄──┼─      ◄─┼───┼─►     ◄─┼───┼─► is    │
              │         │   │         │   │   here  │
              │         │   │         │   │         │
              └─────────┘   └─────────┘   └─────────┘
```

1. PC 從起始房間移動 `east`。建立一個新房間 `A` （座標 `(1, 0)`）。一段時間後，返回起始房間的出口變成單向出口。該分支最多可以有4個未探索的出口，並且地下城分支在房間`A`之外隨機新增三個額外的出口。
2. PC移動`south`。建立一個新房間 `B` (`(1,-1)`)，有兩個隨機出口，這是編排器此時允許建立的數量（現在開啟了 4 個）。它還總是建立返回前一個房間的出口 (`A`)
3. PC移動`east`（座標（`(2, -1)`）。一個新房間`C`被建立。地下城分支已經有3個出口未探索，所以只能在這個房間增加一個出口。
4. PC 移動 `east` (`(3, -1)`)。雖然地下城分支仍然有一個出口的預算，但它知道其他地方有其他未探索的出口，並且允許隨機建立 0 個出口。這是一個死衚衕。 PC必須回去探索另一個方向。

讓我們稍微改變一下地牢來做另一個例子：

```{code-block}
:caption: Looping around
                   ?                   
                   ▲                   
                   │                   
┌─────────┐   ┌────┼────┐              
│         │   │A   │    │              
│         │   │         │              
│  start◄─┼───┼─      ──┼──►?           
│         │   │    ▲    │              
│         │   │    │    │        ?     
└─────────┘   └────┼────┘        ▲     
                   │             │     
              ┌────┼────┐   ┌────┼────┐
              │B   │    │   │C   │    │
              │    ▼    │   │   PC    │
          ?◄──┼─      ◄─┼───┼─► is    │
              │         │   │   here  │
              │         │   │         │
              └─────────┘   └─────────┘

```

在此範例中，PC 移動了 `east`、`south`、`east`，但房間 `C` 的出口朝北，進入 `A` 已經有出口指向的座標。在這裡使用 `north` 會導致以下結果：

```{code-block}
:caption: Creation of a one-way exit
                   ?                   
                   ▲                   
                   │                   
┌─────────┐   ┌────┼────┐   ┌─────────┐
│         │   │A   │    │   │D   PC   │
│         │   │         │   │    is   │
│  start◄─┼───┼─      ──┼───┼─►  here │
│         │   │    ▲    │   │    ▲    │
│         │   │    │    │   │    │    │
└─────────┘   └────┼────┘   └────┼────┘
                   │             │     
              ┌────┼────┐   ┌────┼────┐
              │B   │    │   │C   │    │
              │    ▼    │   │    ▼    │
          ?◄──┼─      ◄─┼───┼─►       │
              │         │   │         │
              │         │   │         │
              └─────────┘   └─────────┘
```

當 PC 移動 `north` 時，在 `(2,0)` 建立房間 `D`。

雖然 `C` 到 `D` 正常情況下會獲得雙向出口，但這會建立從 `A` 到 `D` 的單向出口。

無論哪個出口導致實際建立房間，都會獲得雙向出口，因此，如果 PC 從 `C` 返回並透過從房間 `A` 前往 `east` 建立了房間 `D`，則單向出口將從房間 `C` 開始。

> 如果開放的未探索出口的最大允許數量很小，則這種情況是唯一可以「完成」地牢的情況（沒有更多未探索的出口可跟隨）。我們接受這種情況，因為玩家只需要返回並嘗試另一個地下城分支。

```{code-block}
:caption: Never link back to start room
                   ?                   
                   ▲                   
                   │                   
┌─────────┐   ┌────┼────┐   ┌─────────┐
│         │   │A   │    │   │D        │
│         │   │         │   │         │
│  start◄─┼───┼─      ──┼───┼─►       │
│         │   │    ▲    │   │    ▲    │
│         │   │    │    │   │    │    │
└─────────┘   └────┼────┘   └────┼────┘
                   │             │     
┌─────────┐   ┌────┼────┐   ┌────┼────┐
│E        │   │B   │    │   │C   │    │
│  PC     │   │    ▼    │   │    ▼    │
│  is   ◄─┼───┼─►     ◄─┼───┼─►       │
│  here   │   │         │   │         │
│         │   │         │   │         │
└─────────┘   └─────────┘   └─────────┘
```

這裡PC從房間`B`移動了`west`，在`(0, -1)`建立了房間`E`。

地牢分支永遠不會建立返回起始房間的連結，但它_可能_建立最多兩個新出口`west`和/或`south`。由於房間 `A` 仍有一個未探索的出口 `north`，因此分支也可以隨機分配 0 個出口，這就是它在這裡所做的。

PC需要從`A`原路返回並前往`north`才能繼續探索這個地下城分支。

(making-the-dungeon-dangerous)=
### 讓地牢變得危險

如果沒有危險，地牢就不會有趣！需要有怪物要殺死，需要解決謎題，需要有寶藏。

當電腦第一次進入房間時，房間被標記為`not clear`。當房間未被清理時，電腦_不能使用該房間的任何未探索的出口_。  他們仍然可以原路撤退，除非他們陷入戰鬥，在這種情況下他們必須先逃離。

一旦電腦克服了房間的挑戰（並可能獲得了一些獎勵），它會變成 `clear` 。  如果房間是空的或沒有旨在阻止 PC 的挑戰（例如其他地方的謎題的書面提示），則房間可以自動清除。

請注意，清晰/不清晰僅與與該房間相關的挑戰有關。漫遊怪物（參見 [AI 教學](./Beginner-Tutorial-AI.md)）可能會導致戰鬥發生在先前「清理」的房間中。

(difficulty-scaling)=
### 擴充難度

```{sidebar} 風險與報酬
地牢深度/難度的概念與有限的資源配合得很好。如果治療僅限於可攜帶的東西，這會導致玩家必須決定是要冒險深入，還是拿走當前的戰利品並撤退到地表恢復。
```

地下城的「難度」是透過玩家探索的「深度」來衡量的。這是從起始房間開始的_徑向距離_，向下捨入，由古老的[畢達哥拉斯定理](https://en.wikipedia.org/wiki/Pythagorean_theorem) 得出：

    depth = int(math.sqrt(x**2 + y**2))

因此，如果您在房間 `(1, 1)` 中，您的難度為 1。相反，在房間座標 `(4,-5)` 中，難度為 6。增加深度應該會帶來更艱鉅的挑戰，但也會帶來更大的回報。

(start-implementation)=
## 開始實施

現在就讓我們來實現設計吧！

```{sidebar}
您也可以在 `evennia/contrib/tutorials` 的 [evadventure/dungeon.py](evennia.contrib.tutorials.evadventure.dungeon) 中找到地下城產生器的程式碼範例。
```
> 建立一個新模組`evadventure/dungeon.py`。

(basic-dungeon-rooms)=
## 基本地城房間

這是設計的基本元素，所以讓我們從這裡開始。

回到[關於房間的課程](./Beginner-Tutorial-Rooms.md)，我們建立了一個基本的`EvAdventureRoom` typeclass。 
我們將在地牢房間中對此進行擴充套件。

```{code-block} python
:linenos: 
:emphasize-lines: 13-14,29,32,36, 38
# in evadventure/dungeon.py 

from evennia import AttributeProperty
from .rooms import EvAdventureRoom 


class EvAdventureDungeonRoom(EvAdventureRoom):
    """
    Dangerous dungeon room.

    """

    allow_combat = AttributeProperty(True, autocreate=False)
    allow_death = AttributeProperty(True, autocreate=False)

    # dungeon generation attributes; set when room is created
    dungeon_branch = AttributeProperty(None, autocreate=False)
    xy_coords = AttributeProperty(None, autocreate=False)

    def at_object_creation(self):
        """
        Set the `not_clear` tag on the room. This is removed when the room is
        'cleared', whatever that means for each room.

        We put this here rather than in the room-creation code so we can override
        easier (for example we may want an empty room which auto-clears).

        """
        self.tags.add("not_clear", category="dungeon_room")
    
    def clear_room(self):
        self.tags.remove("not_clear", category="dungeon_room")
    
    @property
    def is_room_clear(self):
        return not bool(self.tags.get("not_clear", category="dungeon_room"))

    def get_display_footer(self, looker, **kwargs):
        """
        Show if the room is 'cleared' or not as part of its description.

        """
        if self.is_room_clear:
            return ""
        else:
            return "|rThe path forwards is blocked!|n"
```

```{sidebar} 儲藏室typeclass
在本教學中，我們將所有與地下城相關的程式碼保留在一個模組中。但也可以認為它們與其他房間一起屬於`evadventure/rooms.py`。這只是您想要如何組織事物的問題。您可以隨意組織自己的遊戲。
```

- **第 14-15 行**：地牢房間很危險，因此與基礎 EvAdventure 房間不同，我們允許戰鬥和死亡在其中發生。
- **第 17 行**：我們儲存對地下城分支的引用，以便我們可以在房間建立期間存取它（如果需要）。如果我們想了解有關地下城分支的資訊作為建立房間的一部分，這可能是相關的。
- **第 18 行**：xy 座標將簡單地儲存為房間中的元組 `(x,y)`。

所有其他功能都是為了管理房間的「乾淨」狀態而建造的。

- **第29行**：當我們建立房間Evennia時，總是會呼叫它的`at_object_creation`鉤子。我們確保為其新增 [Tag](../../../Components/Tags.md) `not_clear`（類別「dungeon_room」以避免與其他系統發生衝突）。
- **第 32 行**：一旦克服了房間的挑戰，我們將使用 `.clear_room()` 方法刪除此 Tag。
- **第 36 行** `.is_room_clear` 是檢查 tag 的便捷屬性。這隱藏了Tag，所以我們不需要擔心我們追蹤乾淨的房間狀態。
- **第 38 行** `get_display_footer` 是一個標準的 Evennia 掛鉤，用於自訂房間的頁尾顯示。

(dungeon-exits)=
## 地牢出口

地牢出口的特殊之處在於，我們希望透過穿越它們的行為來創造另一側的房間。

```python
# in evadventure/dungeon.py 

# ...

from evennia import DefaultExit

# ... 

class EvAdventureDungeonExit(DefaultExit):
    """
    Dungeon exit. This will not create the target room until it's traversed.

    """

    def at_object_creation(self):
        """
        We want to block progressing forward unless the room is clear.

        """
        self.locks.add("traverse:not objloctag(not_clear, dungeon_room)")

    def at_traverse(self, traversing_object, target_location, **kwargs):
        pass  # to be implemented! 

    def at_failed_traverse(self, traversing_object, **kwargs):
        """
        Called when failing to traverse.

        """
        traversing_object.msg("You can't get through this way yet!")

```

目前，我們還沒有實際建立在分支中建立新房間的程式碼，因此我們暫時保留 `at_traverse` 方法未實現。這個鉤子是Evennia在遍歷出口時所呼叫的。

在`at_object_creation`方法中，我們確保增加一個「traverse」型別的[Lock](../../../Components/Locks.md)，這將限制誰可以透過這個出口。我們使用 [objlocktag](evennia.locks.lockfuncs.objloctag) Lock 函式lock 它。這會檢查訪問物件（此出口）的位置（地牢房間）是否有 tag“not_clear”，其類別為“dungeon_room”。如果是，則遍歷_失敗_。也就是說，在房間沒有清理乾淨的情況下，這種出口不會讓任何人透過。

如果 PC 在房間被清理之前嘗試使用出口，`at_failed_traverse` 鉤子允許我們自訂錯誤訊息。

(dungeon-branch-and-the-xy-grid)=
## 地下城分支和 xy 網格

地牢分支負責地牢的一個例項的結構。

(grid-coordinates-and-exit-mappings)=
### 網格座標和退出對映

在開始之前，我們需要建立一些關於網格的常數 - 我們將放置房間的 xy 平面。

```python
# in evadventure/dungeon.py 

# ... 

# cardinal directions
_AVAILABLE_DIRECTIONS = [
    "north",
    "east",
    "south",
    "west",
]

_EXIT_ALIASES = {
    "north": ("n",),
    "east": ("e",),
    "south": ("s",),
    "west": ("w",),
}
# finding the reverse cardinal direction
_EXIT_REVERSE_MAPPING = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east",
}

# how xy coordinate shifts by going in direction
_EXIT_GRID_SHIFT = {
    "north": (0, 1),
    "east": (1, 0),
    "south": (0, -1),
    "west": (-1, 0),
}
```

在本教學中，我們僅允許 NESW 移動。如果您願意，您也可以輕鬆增加 NE、SE、SW、NW 方向。我們為出口別名進行對映（這裡只有一個，但每個方向也可以有多個）。我們還找出“反向”方向，以便稍後能夠輕鬆建立“後退”。

`_EXIT_GRID_SHIFT` 對映指示如果您朝指定方向移動，(x,y) 座標如何移動。因此，如果您站在 `(4,2)` 並移動 `south`，您最終將處於 `(4,1)`。

(base-structure-of-the-dungeon-branch-script)=
#### 地下城分支的基礎結構script

我們將這個元件基於 Evennia [Script](../../../Components/Scripts.md) - 這些可以被認為是在世界上沒有物理存在的遊戲實體。 Scripts 還具有計時屬性。

```{code-block} 
:linenos: 
:emphasize-lines: 
# in evadventure/dungeon.py 

from evennia.utils import create
from evennia import DefaultScript

# ... 

class EvAdventureDungeonBranch(DefaultScript):
    """
    One script is created for every dungeon 'instance' created. The branch is
    responsible for determining what is created next when a character enters an
    exit within the dungeon.

    """
    # this determines how branching the dungeon will be
    max_unexplored_exits = 2
    max_new_exits_per_room = 2

    rooms = AttributeProperty(list())
    unvisited_exits = AttributeProperty(list())

    last_updated = AttributeProperty(datetime.utcnow())

    # the room-generator function; copied from the same-name value on the
    # start-room when the branch is first created
    room_generator = AttributeProperty(None, autocreate=False)

    # (x,y): room coordinates used up by the branch
    xy_grid = AttributeProperty(dict())
    start_room = AttributeProperty(None, autocreate=False)


    def register_exit_traversed(self, exit):
        """
        Tell the system the given exit was traversed. This allows us to track
        how many unvisited paths we have so as to not have it grow
        exponentially.

        """
        if exit.id in self.unvisited_exits:
            self.unvisited_exits.remove(exit.id)

    def create_out_exit(self, location, exit_direction="north"):
        """
        Create outgoing exit from a room. The target room is not yet created.

        """
        out_exit = create.create_object(
            EvAdventureDungeonExit,
            key=exit_direction,
            location=location,
            aliases=_EXIT_ALIASES[exit_direction],
        )
        self.unvisited_exits.append(out_exit.id)
        
    def delete(self):
        """
        Clean up the dungeon branch.

        """
        pass  # to be implemented
        
    def new_room(self, from_exit):
        """
        Create a new Dungeon room leading from the provided exit.

        Args:
            from_exit (Exit): The exit leading to this new room.

        """
        pass  # to be implemented
```

這設定了分支所需的有用屬性，並概述了我們將在下面實現的一些方法。

分支機構有幾項主要職責：
- 追蹤有多少個未探索的出口可用（確保不超過允許的最大數量）。當 PC 穿過這些出口時，我們必須進行適當的更新。
- 當穿過未探索的出口時建立新房間。這個房間又可以有出口。我們還必須追蹤這些房間和出口，以便稍後在清理分支時刪除它們。
- 分支也必須能夠刪除自身，清理其所有資源和房間。

由於 `register_exit_traversed` 和 `create_out_exit` 很簡單，我們立即實施它們。關於出口建立的唯一額外的事情是，它必須確保將新出口註冊為“未訪問”，以便分支可以追蹤它。

(a-note-about-the-room-generator)=
### 關於房間生成器的注意事項

特別值得注意的是 `EvAdventureDungeonBranch` 的 `room_generator` 屬性。這將指向一個函式。我們將其作為一個外掛，因為生成房間是我們在建立遊戲內容時可能需要大量自訂的內容 - 這是我們生成挑戰、房間描述等的地方。

房間生成器必須具有到地下城分支、當前預期難度（在我們的例子中為深度）以及建立房間的 xy 坐標的連結，這是有道理的。

這是一個非常基本的房間生成器的範例，它僅將深度對映到不同的房間描述：

```
# in evadventure/dungeon.py (could also be put with game content files)

# ... 

def room_generator(dungeon_branch, depth, coords):
    """
    Plugin room generator

    This default one returns the same empty room but with different descriptions.

    Args:
        dungeon_branch (EvAdventureDungeonBranch): The current dungeon branch.
        depth (int): The 'depth' of the dungeon (radial distance from start room) this
            new room will be placed at.
        coords (tuple): The `(x,y)` coords that the new room will be created at.

    """
    room_typeclass = EvAdventureDungeonRoom

    # simple map of depth to name and desc of room
    name_depth_map = {
        1: ("Water-logged passage", "This earth-walled passage is dripping of water."),
        2: ("Passage with roots", "Roots are pushing through the earth walls."),
        3: ("Hardened clay passage", "The walls of this passage is of hardened clay."),
        4: ("Clay with stones", "This passage has clay with pieces of stone embedded."),
        5: ("Stone passage", "Walls are crumbling stone, with roots passing through it."),
        6: ("Stone hallway", "Walls are cut from rough stone."),
        7: ("Stone rooms", "A stone room, built from crude and heavy blocks."),
        8: ("Granite hall", "The walls are of well-fitted granite blocks."),
        9: ("Marble passages", "The walls are blank and shiny marble."),
        10: ("Furnished rooms", "The marble walls have tapestries and furnishings."),
    }
    key, desc = name_depth_map.get(depth, ("Dark rooms", "There is very dark here."))

    new_room = create.create_object(
        room_typeclass,
        key=key,
        attributes=(
            ("desc", desc),
            ("xy_coords", coords),
            ("dungeon_branch", dungeon_branch),
        ),
    )
    return new_room

```

這個函式可以包含大量邏輯 - 根據深度、座標或隨機機會，我們可以產生各種不同的房間，並用小怪、謎題或其他東西填充它。由於我們可以存取地牢分支物件，我們甚至可以更改其他房間中的東西以實現真正複雜的互動（多房間謎題，有人嗎？）。

這將在[本教學的第 4 部分](../Part4/Beginner-Tutorial-Part4-Overview.md) 中發揮作用，我們將利用我們在這裡建立的工具來實際建立遊戲世界。

(deleting-a-dungeon-branch)=
### 刪除地下城分支

我們希望能夠清理一個分支。造成這種情況的原因有很多：
- 一旦每個 PC 離開分支，他們就無法返回，因此所有資料現在只是佔用空間。
- 分支機構並不意味著是永久性的。因此，如果玩家停止探索並在樹枝上呆了很長時間，我們應該有辦法迫使他們退出。

為了正確清理該地下城內的角色，我們做了一些假設：
- 當我們建立地下城分支時，我們給它的script一個唯一的識別碼（e.g。涉及當前時間的東西）。
- 當我們啟動地下城分支時，我們tag 該角色具有分支的唯一識別碼。
- 同樣，當我們在該分支內建立房間時，我們使用分支的識別碼tag它們。

如果這樣做了，將很容易找到與分支關聯的所有角色和房間，以便執行此清理操作。

```python
# in evadventure/dungeon.py 

from evennia import search

# ... 

class EvAdventureDungeonBranch(DefaultScript):

    # ...

    def delete(self):
        """
        Clean up the dungeon branch, removing players safely

        """
        # first secure all characters in this branch back to the start room
        characters = search.search_object_by_tag(self.key, category="dungeon_character")
        start_room = self.start_room
        for character in characters:
            start_room.msg_contents(
                "Suddenly someone stumbles out of a dark exit, covered in dust!"
            )
            character.location = start_room
            character.msg(
                "|rAfter a long time of silence, the room suddenly rumbles and then collapses! "
                "All turns dark ...|n\n\nThen you realize you are back where you started."
            )
            character.tags.remove(self.key, category="dungeon_character")
        # next delete all rooms in the dungeon (this will also delete exits)
        rooms = search.search_object_by_tag(self.key, category="dungeon_room")
        for room in rooms:
            room.delete()
        # finally delete the branch itself
        super().delete()

    # ...

```

`evennia.search.search_object_by_tag` 是內建的 Evennia 實用程式，用於尋找以特定 tag+類別組合標記的物件。

1. 首先，我們取得角色並將它們安全地移動到起始房間，並附上相關訊息。
2. 然後我們獲取分支中的所有房間並將其刪除（出口將自動刪除）。
3. 最後我們刪除分支本身。

(creating-a-new-dungeon-room)=
### 建立一個新的地牢房間

這是地下城分支的主要職責。在這種方法中，我們建立新房間，但還需要建立返回我們來自的地方的出口，以及（隨機）產生通往地牢其他部分的出口。


```{code-block}
:linenos: 
:emphasize-lines: 20,23,31,37,44,58,67,72,77
# in evadventure/dungeon.py 

from datetime import datetime
from random import shuffle

# ... 

class EvAdventureDungeonBranch(DefaultScript):

    # ...

    def new_room(self, from_exit):
        """
        Create a new Dungeon room leading from the provided exit.

        Args:
            from_exit (Exit): The exit leading to this new room.

        """
        self.last_updated = datetime.utcnow()
        # figure out coordinate of old room and figure out what coord the
        # new one would get
        source_location = from_exit.location
        x, y = source_location.attributes.get("xy_coords", default=(0, 0))
        dx, dy = _EXIT_GRID_SHIFT.get(from_exit.key, (0, 1))
        new_x, new_y = (x + dx, y + dy)

        # the dungeon's depth acts as a measure of the current difficulty level. This is the radial
        # distance from the (0, 0) (the entrance). The branch also tracks the highest
        # depth achieved.
        depth = int(sqrt(new_x**2 + new_y**2))

        new_room = self.room_generator(self, depth, (new_x, new_y))

        self.xy_grid[(new_x, new_y)] = new_room

        # always make a return exit back to where we came from
        back_exit_key = _EXIT_REVERSE_MAPPING.get(from_exit.key, "back")
        create.create_object(
            EvAdventureDungeonExit,
            key=back_exit_key,
            aliases=_EXIT_ALIASES.get(back_exit_key, ()),
            location=new_room,
            destination=from_exit.location,
            attributes=(
                (
                    "desc",
                    "A dark passage.",
                ),
            ),
            # we default to allowing back-tracking (also used for fleeing)
            locks=("traverse: true()",),
        )

        # figure out what other exits should be here, if any
        n_unexplored = len(self.unvisited_exits)

        if n_unexplored < self.max_unexplored_exits:
            # we have a budget of unexplored exits to open
            n_exits = min(self.max_new_exits_per_room, self.max_unexplored_exits)
            if n_exits > 1:
                n_exits = randint(1, n_exits)
            available_directions = [
                direction for direction in _AVAILABLE_DIRECTIONS if direction != back_exit_key
            ]
            # randomize order of exits
            shuffle(available_directions)
            for _ in range(n_exits):
                while available_directions:
                    # get a random direction and check so there isn't a room already
                    # created in that direction
                    direction = available_directions.pop(0)
                    dx, dy = _EXIT_GRID_SHIFT[direction]
                    target_coord = (new_x + dx, new_y + dy)
                    if target_coord not in self.xy_grid and target_coord != (0, 0):
                        # no room there (and not back to start room) - make an exit to it
                        self.create_out_exit(new_room, direction)
                        # we create this to avoid other rooms linking here, but don't create the
                        # room yet
                        self.xy_grid[target_coord] = None
                        break

        return new_room
```

這裡有很多東西要解壓縮！

- **第 17 行**：我們將「上次更新」時間儲存為目前 UTC 時間戳記。正如我們在上面的刪除部分中討論的那樣，我們需要知道分支是否已經「空閒」很長時間，這有助於追蹤。
- **第 20 行**：`from_exit` 輸入是一個 Exit 物件（可能是 `EvAdventureDungeonExit)` 它位於「來源」位置（我們開始移動的位置）。在後續行中，我們計算出來源的座標以及按照建議的方向移動最終到達的位置
- **第 28 行**：畢達哥拉斯定理！
- **第30行**：這裡我們呼叫上面範例的`room_generator`外掛函式來取得新房間。
- **第 34 行**：我們總是按照來時的方式建立一個後退出口。這_覆蓋_預設的地下城出口lock為`"traverse:true()"`，這意味著PC將始終能夠返回它們來時的方式。
- **第 44 行**：我們可以將 `destination` 欄位留空，但 Evennia 假設出口在顯示房間等中的東西時設定了 `destination` 欄位。因此，為了避免必須更改房間顯示東西的方式，該值應設為 _something_。  由於我們不想建立實際的目的地，所以我們改為將 `destination` 指向當前房間。也就是說，如果你能透過這個出口，你最終會到達同一個地方。我們將在下面使用它來識別未探索的出口。
- **第 55 行**：我們僅在未探索出口的「預算」允許的情況下建立新出口。
- **第 64 行**：在上面的行中，我們建立了房間可以擁有的所有可能出口方向的新清單（不包括必須有的後退出口）。在這裡，我們以隨機順序打亂此列表。
- **第 69 行**：在此迴圈中，我們彈出打亂列表的第一個元素（因此這是一個隨機方向）。在接下來的幾行中，我們檢查該方向是否指向已經存在的地牢房間，也不指向起始房間。如果一切順利，我們將在**第 74 行**呼叫我們的退出建立方法。

最後的結果是一個新房間，至少有一個後退出口和 0 個或更多未探索的出口。

(back-to-the-dungeon-exit-class)=
## 回到地牢出口等級

現在我們有了工具，我們可以回到 `EvAdventureDungeonExit` 類別來實現我們之前跳過的 `at_traverse` 方法。

```python
# in evadventure/dungeon.py 

# ... 

class EvAdventureDungeonExit(DefaultExit):

# ...
    def at_traverse(self, traversing_object, target_location, **kwargs):
        """
        Called when traversing. `target_location` will be pointing back to
        ourselves if the target was not yet created. It checks the current
        location to get the dungeon-branch in use.

        """
        dungeon_branch = self.location.db.dungeon_branch
        if target_location == self.location:
            # destination points back to us - create a new room
            self.destination = target_location = dungeon_branch.new_room(
                self
            )
            dungeon_branch.register_exit_traversed(self)

        super().at_traverse(traversing_object, target_location, **kwargs)

```

我們取得 `EvAdventureDungeonBranch` 例項並檢查目前出口是否指向目前房間。如果您閱讀了上一節中的第 44 行，您會注意到這是在尋找此出口之前是否未探索過的方法！

如果是這樣，我們呼叫地牢分支的`new_room`來產生一個新房間，並將這個出口的`destination`更改為它。我們還確保呼叫 `.register_exit_traversed` 以表明現在已「探索」出口。

我們還必須使用 `super()` 呼叫父類別'`at_traverse`，因為這實際上是將 PC 移至新建立的位置。

(starting-room-exits)=
## 起始房間出口

我們現在擁有了在建立程式地下城分支後實際執行它的所有部分。缺少的是所有分支起源的起始房間。

如設計中所描述的，房間的出口會產生新的分支，但也應該有一個時間段，PC最終都會出現在同一個分支中。因此，我們需要一種特殊型別的出口來處理從起始房間出來的出口。

```{code-block} python
:linenos:
:emphasize-lines: 12,19,22,32
# in evennia/dungeon.py

# ... 

class EvAdventureDungeonStartRoomExit(DefaultExit):

    def reset_exit(self):
        """
        Flush the exit, so next traversal creates a new dungeon branch.

        """
        self.destination = self.location

    def at_traverse(self, traversing_object, target_location, **kwargs):
        """
        When traversing create a new branch if one is not already assigned.

        """
        if target_location == self.location:
            # make a global branch script for this dungeon branch
            self.location.room_generator
            dungeon_branch = create.create_script(
                EvAdventureDungeonBranch,
                key=f"dungeon_branch_{self.key}_{datetime.utcnow()}",
                attributes=(
                    ("start_room", self.location),
                    ("room_generator", self.location.room_generator),
                ),
            )
            self.destination = target_location = dungeon_branch.new_room(self)
            # make sure to tag character when entering so we can find them again later
            traversing_object.tags.add(dungeon_branch.key, category="dungeon_character")

        super().at_traverse(traversing_object, target_location, **kwargs)
```

這個出口擁有創造新的地下城分支所需的一切。

- **第 12 行**：斷開出口與其所連線的任何連線，並將其連結回當前房間（迴圈、無價值的出口）。
- **第 19 行**：當有人穿過此出口時，將呼叫 `at_traverse`。我們偵測到上面的特殊條件（目的地等於當前位置）以確定該出口目前無處可去，我們應該建立一個新分支。
- **第 22 行**：我們建立一個新的 `EvAdventureDungeonBranch` 並確保根據當前時間為其賦予唯一的 `key`。我們還確保設定其起始屬性。
- **第 32 行**：當玩家穿過此出口時，角色會被標記為該地下城分支的相應 tag。這可以被稍後的刪除機制使用。

(utility-scripts)=
## 效用scripts

在建立起始房間之前，我們需要最後兩個實用程式：

- 用於定期重置退出起始房間的計時器（因此它們會建立新的分支）。
- 清理舊/閒置地牢分支的重複任務。

這兩個 scripts 預計都會在起始房間「上」建立，因此 `self.obj` 將是起始房間。

```python
# in evadventure/dungeon.py

from evennia.utils.utils import inherits_from

# ... 

class EvAdventureStartRoomResetter(DefaultScript):
    """
    Simple ticker-script. Introduces a chance of the room's exits cycling every
    interval.

    """

    def at_script_creation(self):
        self.key = "evadventure_dungeon_startroom_resetter"

    def at_repeat(self):
        """
        Called every time the script repeats.

        """
        room = self.obj
        for exi in room.exits:
            if inherits_from(exi, EvAdventureDungeonStartRoomExit) and random() < 0.5:
                exi.reset_exit()
```

這個 script 非常簡單 - 它只是迴圈所有起始房間出口並重置每個出口 50% 的時間。

```python
# in evadventure/dungeon.py

# ... 

class EvAdventureDungeonBranchDeleter(DefaultScript):
    """
    Cleanup script. After some time a dungeon branch will 'collapse', forcing all players in it
    back to the start room.

    """

    # set at creation time when the start room is created
    branch_max_life = AttributeProperty(0, autocreate=False)

    def at_script_creation(self):
        self.key = "evadventure_dungeon_branch_deleter"

    def at_repeat(self):
        """
        Go through all dungeon-branchs and find which ones are too old.

        """
        max_dt = timedelta(seconds=self.branch_max_life)
        max_allowed_date = datetime.utcnow() - max_dt

        for branch in EvAdventureDungeonBranch.objects.all():
            if branch.last_updated < max_allowed_date:
                # branch is too old; tell it to clean up and delete itself
                branch.delete()

```

這個 script 檢查所有分支並檢視自上次更新以來已經過去了多長時間（即在其中建立了一個新房間）。如果時間太長，分支將被刪除（這會將所有玩家轉回起始房間）。

(starting-room)=
## 起始房間

最後，我們需要為起始房間建立一個類別。此房間需要手動建立，之後分支應自動建立。

```python
# in evadventure/dungeon.py

# ... 

class EvAdventureDungeonStartRoom(EvAdventureDungeonRoom):

    recycle_time = 60 * 5  # 5 mins
    branch_check_time = 60 * 60  # one hour
    branch_max_life = 60 * 60 * 24 * 7  # 1 week

    # allow for a custom room_generator function
    room_generator = AttributeProperty(lambda: room_generator, autocreate=False)

    def get_display_footer(self, looker, **kwargs):
        return (
            "|yYou sense that if you want to team up, "
            "you must all pick the same path from here ... or you'll quickly get separated.|n"
        )

    def at_object_creation(self):
        # want to set the script interval on creation time, so we use create_script with obj=self
        # instead of self.scripts.add() here
        create.create_script(
            EvAdventureStartRoomResetter, obj=self, interval=self.recycle_time, autostart=True
        )
        create.create_script(
            EvAdventureDungeonBranchDeleter,
            obj=self,
            interval=self.branch_check_time,
            autostart=True,
            attributes=(("branch_max_life", self.branch_max_life),),
        )

    def at_object_receive(self, obj, source_location, **kwargs):
        """
        Make sure to clean the dungeon branch-tag from characters when leaving a dungeon branch.

        """
        obj.tags.remove(category="dungeon_character")



```

這個房間剩下要做的就是設定我們建立的scripts，並確保清除從分支返回到這個房間的任何物件的分支tags。所有其他工作均由出口和地牢分支處理。

(testing)=
## 測試

```{sidebar}
單元測試檔案的範例位於 [evadventure/tests/test_dungeon.py](evennia.contrib.tutorials.evadventure.tests.test_dungeon) 中的`evennia/contrib/tutorials/`。
```

> 建立`evadventure/tests/test_dungeon.py`。

測試程式地下城最好透過單元測試和手動來完成。

要手動測試，在遊戲中進行很簡單

```shell
> dig well:evadventure.dungeon.EvAdventureDungeonStartRoom = down,up
> down 
> create/drop north;n:evadventure.dungeon.EvAdventureDungeonStartRoomExit
> create/drop east;e:evadventure.dungeon.EvAdventureDungeonStartRoomExit
> create/drop south;s:evadventure.dungeon.EvAdventureDungeonStartRoomExit
> create/drop west;w:evadventure.dungeon.EvAdventureDungeonStartRoomExit
```
    
現在您應該能夠走出其中一個出口並開始探索地牢！一旦一切正常，這尤其有用

為了進行單元測試，您需要在程式碼中建立一個起始房間和出口，然後模擬一個角色穿過出口，確保結果符合預期。  我們將這個練習留給讀者。

(conclusions)=
## 結論

這只是程式生成可能性的表面，但透過相對簡單的方法，我們可以建立一個無限增長的地下城供玩家探索。

值得一提的是，這僅涉及如何按程式生成地牢結構。它還沒有太多_內容_來填滿地牢。我們將在[第 4 部分](../Part4/Beginner-Tutorial-Part4-Overview.md) 中回到這一點，我們將利用我們建立的程式碼來建立遊戲內容。