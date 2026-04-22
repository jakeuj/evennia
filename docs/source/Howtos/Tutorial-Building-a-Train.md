(building-a-train-that-moves)=
# 建造一列可以移動的火車

> TODO：這應該更新為最新的 Evennia 使用。

車輛是您可以進入然後在遊戲世界中移動的東西。在這裡我們將解釋如何建立火車，但這同樣可以應用於建立其他型別的車輛
（汽車、飛機、船、太空船、潛水艇…）。

Evennia 中的物件有一個有趣的屬性：您可以將任何物件放入另一個物件中。這在房間中最為明顯：Evennia 中的房間就像任何其他遊戲物件一樣（除了房間本身往往不在其他任何物體內）。

我們的火車將是類似的：它將是一個其他物體可以進入的物體。然後我們簡單地
移動火車，將所有人帶到車內。

(creating-our-train-object)=
## 建立我們的火車物件

我們需要做的第一步是建立火車物件，包括一個新的typeclass。  為此，
建立一個新檔案，例如在 `mygame/typeclasses/train.py` 中包含以下內容：

```python
# in mygame/typeclasses/train.py

from evennia import DefaultObject

class TrainObject(DefaultObject):

    def at_object_creation(self):
        # We'll add in code here later.
        pass

```

現在我們可以在遊戲中建立火車：

```
create/drop train:train.TrainObject
```

現在這只是一個還沒有做太多事情的物件......但我們已經可以強行進入它內部
然後返回（假設我們在不確定的情況下建立了它）。

```
tel train 
tel limbo
```

(entering-and-leaving-the-train)=
## 進入和離開火車

使用如上所示的`tel`指令顯然不是我們想要的。 `@tel`是管理員指令，普通玩家將永遠無法進入火車！

使用 [Exits](../Components/Objects.md#exits) 進出火車也不是一個好主意 - 出口也是（至少預設）物件。  它們指向一個特定的目的地。如果我們在這個房間放一個出口，通往火車內部，當火車開走時，它會留在這裡（仍然通往火車，就像一個神奇的portal！）。同樣，如果我們將 Exit 物件放在火車內，它總是指向這個房間，無論火車移動到哪裡。

現在，*可以*定義隨火車移動的自訂出口型別或以正確的方式更改目的地 - 但這似乎是一個相當麻煩的解決方案。

相反，我們要做的是建立一些新的[指令](../Components/Commands.md)：一個用於進入火車並
另一個是再次離開它。這些將被存放在*火車物件*上，因此將被製作
任何在火車內或與火車在同一房間的人都可以使用。

讓我們建立一個新的指令模組作為`mygame/commands/train.py`：

```python
# mygame/commands/train.py

from evennia import Command, CmdSet

class CmdEnterTrain(Command):
    """
    entering the train
    
    Usage:
      enter train

    This will be available to players in the same location
    as the train and allows them to embark. 
    """

    key = "enter train"

    def func(self):
        train = self.obj
        self.caller.msg("You board the train.")
        self.caller.move_to(train, move_type="board")


class CmdLeaveTrain(Command):
    """
    leaving the train 
 
    Usage:
      leave train

    This will be available to everyone inside the 
    train. It allows them to exit to the train's
    current location. 
    """

    key = "leave train"

    def func(self):
        train = self.obj
        parent = train.location
        self.caller.move_to(parent, move_type="disembark")


class CmdSetTrain(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEnterTrain())
        self.add(CmdLeaveTrain())
```
請注意，雖然這看起來有很多文字，但這裡的大部分行都是由
文件。

這些指令的工作方式非常簡單：`CmdEnterTrain` 將玩家的位置移到火車內部，`CmdLeaveTrain` 則相反：它將玩家移回火車內部。
火車的目前位置（返回目前位置）。我們將它們堆疊在 [cmdset](../Components/Command-Sets.md) `CmdSetTrain` 中，以便可以使用它們。

為了使指令起作用，我們需要將此 cmdset 新增到我們的訓練 typeclass 中：

```python
# file mygame/typeclasses/train.py

from commands.train import CmdSetTrain
from typeclasses.objects import Object

class TrainObject(Object):

    def at_object_creation(self):        
        self.cmdset.add_default(CmdSetTrain)

```

如果我們現在`reload`我們的遊戲並重置我們的火車，這些指令應該會起作用，我們現在可以進入和離開火車：

```
reload
typeclass/force/reset train = train.TrainObject
enter train
leave train
```

請注意與 `typeclass` 指令一起使用的開關：`/force` 開關對於為我們的物件分配與我們已有的相同的 typeclass 是必需的。 `/reset` 重新觸發 typeclass' `at_object_creation()` 掛鉤（否則僅在建立第一個例項時呼叫）。
如上所示，當在我們的火車上呼叫此鉤子時，我們的新 cmdset 將被載入。

(locking-down-the-commands)=
## 鎖定指令

如果您玩過一些，您可能已經發現可以在以下情況下使用 `leave train`
火車外時為`enter train`，車內時為`enter train`。這沒有任何意義……所以我們繼續吧
並解決這個問題。  我們需要告訴Evennia，當你已經在車內時，你不能進入火車
或在外出時離開火車。解決這個問題的一種方法是[鎖定](../Components/Locks.md)：我們將lock下調指令，這樣只有當玩家位於正確的位置時才能呼叫它們。

由於我們沒有在指令上設定 `lock` 屬性，因此它預設為 `cmd:all()`。這意味著只要在同一個房間_或火車內_，每個人都可以使用該指令。

首先我們需要建立一個新的 lock 函式。 Evennia 帶有許多內建的 lock 函式
已經存在，但在這種特殊情況下我們無法使用它來鎖定指令。在 `mygame/server/conf/lockfuncs.py` 中建立一個新條目：

```python

# file mygame/server/conf/lockfuncs.py

def cmdinside(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage: cmdinside() 
    Used to lock commands and only allows access if the command
    is defined on an object which accessing_obj is inside of.     
    """
    return accessed_obj.obj == accessing_obj.location

```
如果您不知道，Evennia 預設為使用此模組中的所有函式作為 lock
函式（有一個指向它的設定變數）。

我們的新 lock 函式 `cmdinside` 將由指令使用。  `accessed_obj` 是 Command 物件（在我們的例子中，這將是 `CmdEnterTrain` 和 `CmdLeaveTrain`） — 每個指令都有一個 `obj` 屬性：這是指令「所在」的物件。  由於我們將這些指令新增到了火車物件中，因此 `.obj` 屬性將設定為火車物件。相反，`accessing_obj` 是呼叫指令的物件：在我們的例子中，它是嘗試進入或離開火車的角色。

此函式的作用是檢查玩家的位置是否與火車物件相同。如果
是的，這意味著玩家在火車內。否則就意味著玩家在其他地方並且
檢查將會失敗。

下一步是實際使用這個新的 lock 函式來建立 `cmd` 型別的 lock：

```python
# file commands/train.py
...
class CmdEnterTrain(Command):
    key = "enter train"
    locks = "cmd:not cmdinside()"
    # ...

class CmdLeaveTrain(Command):
    key = "leave train"
    locks = "cmd:cmdinside()"
    # ...
```

注意我們如何在這裡使用`not`，以便我們可以使用相同的`cmdinside`來檢查我們是否在裡面
和外部，無需建立兩個單獨的 lock 函式。 `@reload` 之後我們的指令
應適當鎖定，並且您應該只能在正確的地方使用它們。

> 注意：如果您以超級使用者（使用者`#1`）登入，則此lock將無法運作：超級使用者
使用者忽略lock功能。為了使用此功能，您需要先`@quell`。

(making-our-train-move)=
## 讓我們的火車開動

現在我們可以正確地進出火車了，是時候讓它移動了。  有不同的
為此我們需要考慮的事情：

* 誰可以控制您的車輛？第一個進入的玩家，只有具有一定「駕駛」技能的玩家，自動？
* 它應該去哪裡？玩家可以駕駛車輛前往其他地方還是會始終遵循相同的路線？

對於我們的範例火車，我們將透過預先定義的路線（其軌道）自動移動。火車會在路線的起點和終點停留一段時間，以便玩家可以進出。

繼續為我們的火車建立一些房間。列出沿途的房間 ID（使用 `xe` 指令）。

```
> dig/tel South station
> ex              # note the id of the station
> tunnel/tel n = Following a railroad
> ex              # note the id of the track
> tunnel/tel n = Following a railroad
> ...
> tunnel/tel n = North Station
```

將火車放到鐵軌上：

```
tel south station
tel train = here
```

接下來我們將告訴火車如何移動以及走哪條路線。

```python
# file typeclasses/train.py

from evennia import DefaultObject, search_object

from commands.train import CmdSetTrain

class TrainObject(DefaultObject):

    def at_object_creation(self):
        self.cmdset.add_default(CmdSetTrain)
        self.db.driving = False
        # The direction our train is driving (1 for forward, -1 for backwards)
        self.db.direction = 1
        # The rooms our train will pass through (change to fit your game)
        self.db.rooms = ["#2", "#47", "#50", "#53", "#56", "#59"]

    def start_driving(self):
        self.db.driving = True

    def stop_driving(self):
        self.db.driving = False

    def goto_next_room(self):
        currentroom = self.location.dbref
        idx = self.db.rooms.index(currentroom) + self.db.direction

        if idx < 0 or idx >= len(self.db.rooms):
            # We reached the end of our path
            self.stop_driving()
            # Reverse the direction of the train
            self.db.direction *= -1
        else:
            roomref = self.db.rooms[idx]
            room = search_object(roomref)[0]
            self.move_to(room)
            self.msg_contents(f"The train is moving forward to {room.name}.")
```

我們在這裡新增了很多程式碼。由於我們更改了 `at_object_creation` 以新增變數，因此我們必須像以前一樣重置火車物件（使用 `@typeclass/force/reset` 指令）。

我們現在正在追蹤一些不同的事情：火車是在移動還是靜止不動，
火車開往哪個方向以及經過哪些房間。

我們還新增了一些方法：一個開始移動火車，另一個停止，第三個將火車實際移動到清單中的下一個房間。或在到達最後一站時使其停止行駛。

讓我們嘗試一下，使用 `py` 呼叫新的火車功能：

```
> reload
> typeclass/force/reset train = train.TrainObject
> enter train
> py here.goto_next_room()
```

您應該看到火車沿著鐵路向前移動了一步。

(adding-in-scripts)=
## 新增scripts

如果我們想要完全控制火車，我們現在只需新增一個指令即可在需要時沿著軌道行駛。不過，我們希望火車自行移動，而不必透過手動呼叫 `goto_next_room` 方法來強制它。

為此，我們將建立兩個 [scripts](../Components/Scripts.md)：一個 script 在火車停在
一個車站，負責在一段時間後再次啟動火車。其餘script將佔用
照顧駕駛。

讓我們在`mygame/typeclasses/trainscript.py`中建立一個新檔案

```python
# file mygame/typeclasses/trainscript.py

from evennia import DefaultScript

class TrainStoppedScript(DefaultScript):

    def at_script_creation(self):
        self.key = "trainstopped"
        self.interval = 30
        self.persistent = True
        self.repeats = 1
        self.start_delay = True

    def at_repeat(self):
        self.obj.start_driving()        

    def at_stop(self):
        self.obj.scripts.add(TrainDrivingScript)


class TrainDrivingScript(DefaultScript):

    def at_script_creation(self):
        self.key = "traindriving"
        self.interval = 1
        self.persistent = True

    def is_valid(self):
        return self.obj.db.driving

    def at_repeat(self):
        if not self.obj.db.driving:
            self.stop()
        else:
            self.obj.goto_next_room()

    def at_stop(self):
        self.obj.scripts.add(TrainStoppedScript)
```

那些 scripts 作為狀態系統工作：當火車停止時，它會等待 30 秒，然後
再次開始。火車行駛時，每秒鐘都會移動到下一個房間。火車總是
在這兩種狀態之一 - scripts 完成後都會再增加一種狀態。

最後一步，我們需要將停止狀態 script 連線到我們的火車，重新載入遊戲並重置我們的
再次訓練，我們已經準備好騎它到處跑了！

```python
# file typeclasses/train.py

from typeclasses.trainscript import TrainStoppedScript

class TrainObject(DefaultObject):

    def at_object_creation(self):
        # ...
        self.scripts.add(TrainStoppedScript)
```

```
> reload
> typeclass/force/reset train = train.TrainObject
> enter train

# output:
< The train is moving forward to Following a railroad.
< The train is moving forward to Following a railroad.
< The train is moving forward to Following a railroad.
...
< The train is moving forward to Following a railroad.
< The train is moving forward to North station.

leave train
```

我們的火車將在每個終點站停靠 30 秒，然後掉頭返回另一端。

(expanding)=
## 擴充

這列火車非常基礎，但仍存在一些缺陷。還有一些事情要做：

* 讓它看起來像一列火車。
* 使乘客無法在中途退出和進入火車。這可以透過檢查進入/退出指令來實現，以便在允許呼叫者繼續之前火車不會移動。
* 擁有可以覆蓋自動啟動/停止的列車售票員指令。
* 允許在起點站和終點站之間進行中途停靠
* 擁有鐵路軌道，而不是對火車物件中的房間進行硬編碼。例如，這可以是隻能由火車穿過的自訂[出口](../Components/Objects.md#exits)。火車將沿著軌道行駛。有些軌道段可以分開，通往兩個不同的房間，玩家可以切換方向到哪個房間。
* 創造另一種車輛！