(ondemandhandler)=
# OnDemandHandler

此處理程式為實現按需狀態變更提供協助。按需意味著在玩家_實際查詢_之前不會計算狀態。在他們這樣做之前，什麼事也不會發生。這是處理系統時計算效率最高的方法，您應該盡可能考慮使用這種型別的系統。

以園藝系統為例。玩家進入一個房間並種下一顆種子。一段時間後，該植物將經歷一系列階段；它將從“幼苗”到“發芽”，再到“開花”，然後“枯萎”，最後“死亡”。

現在，您可以使用 `utils.delay` 來追蹤每個階段，或使用 [TickerHandler](./TickerHandler.md) 來勾選花朵。你甚至可以在花上使用[Script](./Scripts.md)。這會像這樣工作：

1. 程式碼/任務/Script 會定期自動觸發，以更新工廠的各個階段。
2. 每當玩家來到房間時，花上的狀態已經更新，因此他們只需讀取狀態即可。

這會運作得很好，但如果沒有人回到那個房間，那就是沒有人會看到的大量更新。雖然對於單一玩家來說可能沒什麼大不了的，但如果你在數千個房間裡都有鮮花，並且全部獨立生長怎麼辦？或者一些更複雜的系統需要對每個狀態變化進行計算。您應該避免將計算花在不會為玩家群帶來任何額外好處的事情上。

使用按需風格，花會像這樣工作：

1. 當玩家種植種子時，我們會註冊_當前時間戳_ - 植物開始生長的時間。我們將其與 `OnDemandHandler` 一起儲存（如下）。
2. 當玩家進入房間和/或檢視植物時（或程式碼系統需要知道植物的狀態），_然後_（只有那時）我們檢查_當前時間_以找出花現在必須處於的狀態（`OnDemandHandler` 為我們記帳）。關鍵是_直到我們檢查_，花物件完全不活動並且不使用任何計算資源。

(a-blooming-flower-using-the-ondemandhandler)=
## 使用OnDemandHandler盛開的花朵

該處理程式被發現為 `evennia.ON_DEMAND_HANDLER`。它旨在整合到您的其他程式碼中。以下是一朵花在 12 小時內經歷其生命階段的例子。

```python
# e.g. in mygame/typeclasses/objects.py

from evennia import ON_DEMAND_HANDLER 

# ... 

class Flower(Object): 

    def at_object_creation(self):

        minute = 60
        hour = minute * 60

        ON_DEMAND_HANDLER.add(
            self,
            category="plantgrowth"
            stages={
                0: "seedling",
                10 * minute: "sprout",
                5 * hour: "flowering",
                10 * hour: "wilting",
                12 * hour: "dead"
            })

    def at_desc(self, looker):
        """
        Called whenever someone looks at this object
        """ 
        stage = ON_DEMAND_HANDLER.get_state(self, category="plantgrowth")

        match stage: 
            case "seedling": 
                return "There's nothing to see. Nothing has grown yet."
            case "sprout": 
                return "A small delicate sprout has emerged!"
            case "flowering": 
                return f"A beautiful {self.name}!"
            case "wilting": 
                return f"This {self.name} has seen better days."
            case "dead": 
                # it's dead and gone. Stop and delete 
                ON_DEMAND_HANDLER.remove(self, category="plantgrowth")
                self.delete()
```


`get_state(key, category=None, **kwargs)` 方法用於取得當前階段。 `get_dt(key, category=None, **kwargs)` 方法而是檢索目前經過的時間。

現在您可以建立玫瑰，只有當您實際觀察它時，它才會弄清楚它的狀態。在發芽之前，它會在幼苗中停留 10 分鐘（遊戲中的實時時間）。 12小時內它就會再次死亡。

如果您的遊戲中有 `harvest` 指令，您同樣可以讓它檢查開花階段，並根據您是否在正確的時間採摘玫瑰給出不同的結果。

按需處理程式的任務在重新載入後仍然存在，並將正確考慮停機時間。

(more-usage-examples)=
## 更多使用範例

[OnDemandHandler API](evennia.scripts.ondemandhandler.OnDemandHandler) 詳細描述如何使用處理程式。雖然它以 `evennia.ON_DEMAND_HANDLER` 的形式提供，但其程式碼位於 `evennia.scripts.ondemandhandler.py` 中。

```python
from evennia import ON_DEMAND_HANDLER 

ON_DEMAND_HANDLER.add("key", category=None, stages=None)
time_passed = ON_DEMAND_HANDLER.get_dt("key", category=None)
current_state = ON_DEMAND_HANDLER.get_stage("key", category=None)

# remove things 
ON_DEMAND_HANDLER.remove("key", category=None)
ON_DEMAND_HANDLER.clear(cateogory="category")  #clear all with category
```

```{sidebar} 並非所有階段都可能發生火災！
這很重要。如果在花朵已經枯萎之前沒有人檢查花朵，它會簡單地跳過所有先前的階段，直接進入「枯萎」階段。因此，不要為假設先前階段對物件進行了特定更改的階段編寫程式碼 - 這些更改可能不會發生，因為這些階段可能已完全跳過！
```
- `key` 可以是字串，也可以是型別分類物件（將使用其字串表示形式，通常包括其 `#dbref`）。您還可以傳遞 `callable` - 這將在不帶引數的情況下呼叫，並預計將返回用於 `key` 的字串。最後，您也可以傳遞 [OnDemandTask](evennia.scripts.ondemandhandler.OnDemandTask) 實體 - 這些是處理程式在幕後使用的物件來表示每個任務。
- `category` 允許您進一步對需求處理程式任務進行分類，以確保它們是唯一的。由於處理程式是全域的，因此您需要確保 `key` + `category` 是唯一的。雖然 `category` 是可選的，但如果您使用它，則以後也必須使用它來檢索您的狀態。
- `stages` 是 `dict` `{dt: statename}` 或 `{dt: (statename, callable)}` ，表示從_任務開始_開始該階段所需的時間（以秒為單位）。在上面的花範例中，距離 `wilting` 狀態開始還有 10 個小時。如果包含可呼叫物件，它將在第一次到達該階段時觸發。此可呼叫函式將目前的 `OnDemandTask` 和 `**kwargs` 作為引數；關鍵字從 `get_stages/dt` 方法傳遞。 [請參閱下文](#stage-callables) 以瞭解有關允許的可呼叫專案的資訊。 `stages` 是可選的 - 有時您只想知道已經過去了多少時間。
- `.get_dt()` - 取得自任務開始以來的當前時間（以秒為單位）。這是`float`。
- `.get_stage()` - 取得目前狀態名稱，例如「開花」或「幼苗」。如果您沒有指定任何`stages`，這將返回`None`，並且您需要自己解釋`dt`以確定您處於哪種狀態。

在底層，處理程式使用 [OnDemandTask](evennia.scripts.ondemandhandler.OnDemandTask) 物件。有時直接使用這些建立任務並將它們批次傳遞給處理程式是很實用的：

```python
from evennia import ON_DEMAND_HANDLER, OnDemandTask 

task1 = OnDemandTask("key1", {0: "state1", 100: ("state2", my_callable)})
task2 = OnDemandTask("key2", category="state-category")

# batch-start on-demand tasks
ON_DEMAND_HANDLER.batch_add(task1, task2)

# get the tasks back later 
task1 = ON_DEMAND_HANDLER.get("key1")
task2 = ON_DEMAND_HANDLER.get("key1", category="state-category")

# batch-deactivate tasks you have available
ON_DEMAND_HANDLER.batch_remove(task1, task2)
```

(stage-callables)=
### 階段可呼叫物件

如果您將一個或多個 `stages` 字典鍵定義為 `{dt: (statename, callable)}`，則第一次檢查該階段時將呼叫此可呼叫函式。這個「可呼叫階段」有一些要求：

- 可呼叫的階段必須[可能進行pickle](https://docs.python.org/3/library/pickle.html#pickle-picklable)，因為它將被儲存到資料庫中。這基本上意味著您的可​​呼叫函式需要是獨立函式或以 `@staticmethod` 修飾的方法。您將無法直接從這樣的方法或函式存取物件例項作為 `self` - 您需要明確傳遞它。
- 可呼叫物件必須始終將 `task` 作為其第一個元素。這是觸發此可呼叫的 `OnDemandTask` 物件。
- 它可以選擇採用 `**kwargs` 。這將從您的 `get_dt` 或 `get_stages` 呼叫中傳遞下來。

這是一個例子：

```python
from evennia DefaultObject, ON_DEMAND_HANDLER

def mycallable(task, **kwargs)
	# this function is outside the class and is pickleable just fine
    obj = kwargs.get("obj")
    # do something with the object

class SomeObject(DefaultObject):

    def at_object_creation(self):
        ON_DEMAND_HANDLER.add(
	        "key1", 
	        stages={0: "new", 10: ("old", mycallable)}
	    )

	def do_something(self):
	    # pass obj=self into the handler; to be passed into
	    # mycallable if we are in the 'old' stage.
		state = ON_DEMAND_HANDLER.get_state("key1", obj=self)

```

上面，一旦我們達到「舊」狀態，`obj=self` 將傳遞到 `mycallable`。如果我們不處於「舊」階段，多餘的 kwargs 將無處可去。透過這種方式，函式可以知道呼叫它的物件，同時仍然可以進行 pickle。您也可以透過這種方式將任何其他資訊傳遞到可呼叫物件中。

> 如果您不想處理可呼叫物件的複雜性，您也可以只讀取當前階段並在處理程式之外執行所有邏輯。這通常更容易閱讀和維護。


(looping-repeatedly)=
### 反覆迴圈

通常，當迴圈完`stages`的序列後，任務將無限期地停止在最後一個階段。

`evennia.OnDemandTask.stagefunc_loop` 是一個包含的可呼叫靜態方法階段，可用來使任務迴圈。以下是如何使用它的範例：

```python
from evennia import ON_DEMAND_HANDLER, OnDemandTask 

ON_DEMAND_HANDLER.add(
    "trap_state", 
    stages={
        0: "harmless",
        50: "solvable",
        100: "primed",
        200: "deadly",
        250: ("_reset", OnDemandTask.stagefunc_loop)
    }
)
```

這是一個陷阱狀態，根據時間迴圈其狀態。請注意，迴圈助手可呼叫將立即將迴圈重置回第一階段，因此最後一個階段永遠不會對玩家/遊戲系統可見。因此，用 `_*` 命名它是一個好主意（如果可選），以記住這是一個「虛擬」階段。在上面的例子中，「致命」狀態將直接迴圈到「無害」狀態。

`OnDemandTask` 任務例項有一個 `.iterations` 變數，每次迴圈該變數都會加一。

如果長時間沒有檢查狀態，迴圈函式將正確更新迄今為止使用的任務的 `.iterations` 屬性，並找出它現在在迴圈中的位置。

(bouncing-back-and-forth)=
### 來回彈跳

`evennia.OnDemandTask.stagefunc_bounce` 是一個包含的可呼叫靜態方法，您可以使用它來「反彈」階段序列。也就是說，它將迴圈到迴圈結束，然後反轉方向並反向迴圈序列，保持每個階段之間的時間間隔相同。

要使其無限重複，您需要將這些可呼叫物件放在清單的兩端：

```python 
from evennia import ON_DEMAND_HANDLER, OnDemandTask 

ON_DEMAND_HANDLER.add(
    "cycling reactor",
    "nuclear",
    stages={
        0: ("cold", OnDemandTask.stagefunc_bounce),
        150: "luke warm",
        300: "warm", 
        450: "hot"
        600: ("HOT!", OnDemandTask.stagefunc_bounce)    
    }
)
```

這樣會迴圈
    
        cold -> luke warm -> warm -> hot -> HOT! 

在反轉和返回之前（一遍又一遍）：

        HOT! -> hot -> warm -> luke warm -> cold 

與 `stagefunc_loop` 可呼叫不同，彈跳階段_將_明顯停留在第一個和最後一個階段，直到它更改為序列中的下一個階段。  `OnDemandTask` 例項有一個 `.iterations` 屬性，每次序列反轉時該屬性都會加一。

如果長時間未檢查狀態，則彈跳函式將正確地將 `.iterations` 屬性更新為該時間段內將完成的迭代次數，並找出它現在處於迴圈中的位置。

(when-is-it-not-suitable-to-do-things-on-demand)=
## 什麼時候不適合按需做事？

如果您下定決心，您可能可以按需製作遊戲。玩家不會變得更聰明。

實際上只有一種情況點播不起作用，那就是如果應該向玩家通知某些內容_而不先提供任何輸入_。

如果玩家必須執行 `check health` 指令來檢視他們有多少生命值，這可能會按需發生。同樣，可以設定提示以在您每次移動時更新。但是，如果你想讓一個閒置的玩家突然收到一條訊息，說“你感覺餓了”，或者在靜止不動時看到一些HP儀表在視覺上增加，那麼某種計時器/自動收報機將需要啟動輪子。

但請記住，在文字媒體中（尤其是傳統的逐行 MUD 使用者端），在玩家被淹沒之前，你只能向他們推送這麼多垃圾訊息。