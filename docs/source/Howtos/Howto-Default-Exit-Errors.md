(return-custom-errors-on-missing-exits)=
# 傳回缺少退出時的自訂錯誤


    > north
    Ouch! You bump into a wall!
    > out 
     But you are already outside ...? 
     
Evennia 允許出口具有任何名稱。指令“kitchen”以及“jump out of the window”或“north”都是有效的出口名稱。退出實際上由兩部分組成：[退出物件](../Components/Objects.md) 和
儲存在所述退出物件上的[退出指令](../Components/Commands.md)。該指令與以下指令具有相同的金鑰和別名
exit-object，這就是為什麼你可以看到房間裡的出口，只需寫下它的名字就可以遍歷它。

因此，如果您嘗試輸入不存在的退出的名稱，Evennia 的處理方式與您嘗試使用不存在的指令相同：

     > jump out the window
     Command 'jump out the window' is not available. Type "help" for help.

許多遊戲不需要這種自由。它們僅將基本方向定義為有效的出口名稱（Evennia 的 `tunnel` 指令也提供此功能）。在這種情況下，錯誤開始看起來不那麼合乎邏輯：

     > west
     Command 'west' is not available. Maybe you meant "set" or "reset"?

由於我們對於我們的特定遊戲“知道”西是出口方向，因此如果錯誤訊息只是告訴我們不能去那裡，那就更好了。
    
     > west 
     You cannot move west.

做到這一點的方法是給 Evennia 一個_alternative_ Command，以便在房間中找不到退出指令時使用。有關將新指令新增到 Evennia 的過程的詳細資訊，請參閱[新增指令](Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)。

在這個例子中，我們只會回顯一條錯誤訊息，但你可以做任何事情（如果你撞到牆上，也許你會失去健康？）

```python
# for example in a file mygame/commands/movecommands.py

from evennia import default_cmds, CmdSet

class CmdExitError(default_cmds.MuxCommand):
    """Parent class for all exit-errors."""
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    auto_help = False
    def func(self):
        """Returns error based on key"""
        self.caller.msg(f"You cannot move {self.key}.")

class CmdExitErrorNorth(CmdExitError):
    key = "north"
    aliases = ["n"]

class CmdExitErrorEast(CmdExitError):
    key = "east"
    aliases = ["e"]

class CmdExitErrorSouth(CmdExitError):
    key = "south"
    aliases = ["s"]

class CmdExitErrorWest(CmdExitError):
    key = "west"
    aliases = ["w"]

# you could add each command on its own to the default cmdset,
# but putting them all in a cmdset here allows you to
# just add this and makes it easier to expand with more 
# exit-errors in the future

class MovementFailCmdSet(CmdSet):
    def at_cmdset_creation(self): 
        self.add(CmdExitErrorNorth())
        self.add(CmdExitErrorEast())
        self.add(CmdExitErrorWest())
        self.add(CmdExitErrorSouth()) 
```

我們將指令打包在一個新的小cmdset中；如果我們將其新增至 `CharacterCmdSet` 中，則稍後可以將更多錯誤新增至 `MovementFailCmdSet` 中，而無需在兩個位置變更程式碼。

```python
# in mygame/commands/default_cmdsets.py

from commands import movecommands

# [...]
class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # [...]
    def at_cmdset_creation(self):
        # [...]
        # this adds all the commands at once
        self.add(movecommands.MovementFailCmdSet)
```

`reload` 伺服器。今後發生的情況是，如果您在一個帶有 Exit 物件的房間中（假設它是“北”），正確的退出指令將_overload_您的錯誤指令（也稱為“北”）。但是，如果您輸入方向而沒有符合的出口，您將退回到預設的錯誤指令：

     > east
     You cannot move east.

退出系統的進一步擴充套件（包括操作 Exit 指令本身的建立方式）可以透過直接修改 [Exit typeclass](../Components/Typeclasses.md) 來完成。

(why-not-a-single-command)=
## 為什麼不是一個指令？

那為什麼我們不在上面建立一個錯誤指令呢？像這樣的東西：

```python
class CmdExitError(default_cmds.MuxCommand):
   "Handles all exit-errors."
   key = "error_cmd"
   aliases = ["north", "n", 
              "east", "e",
              "south", "s",
              "west", "w"]
    #[...]
```

這*不會*按照我們想要的方式工作。瞭解原因很重要。

Evennia 的[指令系統](../Components/Commands.md) 按鍵和/或別名比較指令。如果_任何_鍵或別名匹配，則這兩個指令被視為_相同_。當 cmdsets 合併時，優先順序將決定這些「相同」指令中的哪個指令取代哪個指令。

因此，只要房間裡沒有出口，上面的例子就可以正常運作。但當我們進入一個出口為「北」的房間時，它的退出指令（具有更高的優先順序）將覆蓋單一`CmdExitError`及其別名「北」。因此 `CmdExitError` 將消失，而「向北」將起作用，我們將再次收到其他方向的正常「指令無法識別」錯誤。