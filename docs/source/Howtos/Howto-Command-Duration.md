(commands-that-take-time-to-finish)=
# 需要時間才能完成的指令

    > craft fine sword 
    You start crafting a fine sword. 
    > north 
    You are too focused on your crafting, and can't move!
    You create the blade of the sword. 
    You create the pommel of the sword. 
    You finish crafting a Fine Sword.

在某些型別的遊戲中，指令不應立即開始和結束。

裝載十字弓可能需要一些時間 - 你沒有時間
敵人向你衝來。製作盔甲不會立即完成
要麼。對於某些型別的遊戲來說，移動或改變姿勢的行為本身就是
伴隨著與之相關的特定時間。

有兩種主要的合適方法可以在[指令](../Components/Commands.md)的執行中引入「延遲」：

- 在指令的 `func` 方法中使用 `yield`。
- 使用 `evennia.utils.delay` 實用函式。

我們將在下面簡化兩者。

(pause-commands-with-yield)=
## 使用 `yield` 暫停指令

`yield` 關鍵字是 Python 中的保留字。它用於建立[生成器](https://realpython.com/introduction-to-python-generators/)，它們本身就很有趣。不過，出於本指南的目的，我們只需要知道 Evennia 將使用它來「暫停」指令的執行一段時間。

```{sidebar} 這只適用於 Command.func！

此 `yield` 功能*僅*在 `func` 方法中工作
指令。它之所以有效，是因為 Evennia 特別將其作為方便的快捷方式。嘗試在其他地方使用它是行不通的。如果您想在其他地方獲得相同的功能，您應該尋找[互動式裝飾器](../Concepts/Async-Process.md#the-interactive-decorator)。
```

```{code-block} python
:linenos:
:emphasize-lines: 15

class CmdTest(Command):

    """
    A test command just to test waiting.

    Usage:
        test

    """

    key = "test"

    def func(self):
        self.msg("Before ten seconds...")
        yield 10
        self.msg("Afterwards.")
```

- **第 15 行**：這是重要的一行。  `yield 10` 告訴 Evennia「暫停」該指令
並等待 10 秒來執行其餘的操作。  如果新增此指令並且
執行它，您將看到第一條訊息，然後，停頓十秒後，
下一則訊息。  您可以在指令中多次使用 `yield`。

此語法不會“凍結”所有指令。  當指令「暫停」時，您可以執行其他指令（甚至再次呼叫相同指令）。  其他玩家也沒有被凍結。

> 使用 `yield` 是非永續性的。如果您在指令「暫停」時`reload`遊戲，則暫停狀態將會遺失，並且在伺服器重新載入後不會恢復。

(pause-commands-with-utilsdelay)=
## 使用 `utils.delay` 暫停指令

`yield` 文法易於閱讀、易於理解、易於使用。  但如果您想要更高階的選項，它是非永續性的並且不那麼靈活。

`evennia.utils.delay` 代表的是一種更強大的引入延遲的方式。與`yield`不同，它
可以持久化並且也可以在 `Command.func` 之外工作。  然而，寫起來有點麻煩，因為與 `yield` 不同，它實際上不會停在它被呼叫的行處。

```{code-block} python
:linenos:
:emphasize-lines: 14,30

from evennia import default_cmds, utils
    
class CmdEcho(default_cmds.MuxCommand):
    """
    Wait for an echo
    
    Usage: 
      echo <string>
    
    Calls and waits for an echo.
    """
    key = "echo"
    
    def echo(self):
        "Called after 10 seconds."
        shout = self.args
        self.caller.msg(
            "You hear an echo: "
            f"{shout.upper()} ... "
            f"{shout.capitalize()} ... "
            f"{shout.lower()}"
        )
    
    def func(self):
        """
         This is called at the initial shout.            
        """
        self.caller.msg(f"You shout '{self.args}' and wait for an echo ...")
        # this waits non-blocking for 10 seconds, then calls self.echo
        utils.delay(10, self.echo) # call echo after 10 seconds
    
```

將此新的 echo 指令匯入到預設指令集中並重新載入伺服器。你會發現過了10秒你才會看到你的喊聲回來。

- **第 14 行**：我們新增一個新方法 `echo`。這是一個_回撥_ - 我們將在一段時間後呼叫的方法/函式。
- **第 30 行**：這裡我們使用 `utils.delay` 告訴 Evennia：「請等待 10 秒，然後呼叫 `self.echo`。」請注意，我們傳入的是 `self.echo`，而不是 `self.echo()`！如果使用後者，`echo` 就會立刻觸發。相反地，我們讓 Evennia 在十秒後替我們執行這次呼叫。

你還會發現，這是一個*非阻塞*的效果；您可以在此期間發出其他指令，遊戲將照常進行。迴聲會在適當的時間回到你身邊。

`utils.delay` 的呼叫簽名是：

```python
utils.delay(timedelay, callback, persistent=False, *args, **kwargs) 
```

```{sidebar} *args 和 **kwargs

這些用於指示應在此選取任意數量的引數或關鍵字引數。在程式碼中，它們分別被視為 `tuple` 和 `dict`。

Evennia中很多地方都使用了`*args`和`**kwargs`。 [請參閱此處的線上教學](https://realpython.com/python-kwargs-and-args)。
```
如果您設定`persistent=True`，則此延遲將持續`reload`。如果您傳遞 `*args` 和/或 `**kwargs`，它們將傳遞到 `callback` 中。這樣你就可以將更複雜的引數傳遞給延遲函式。

重要的是要記住 `delay()` 呼叫不會在此時“暫停”
呼叫（如上一節 `yield` 的方式）。 `delay()` 呼叫之後的行將
實際上*立即執行*。你必須做的是告訴它在時間之後要呼叫哪個函式
已經過去*（它的“回撥”）。乍聽之下這可能很奇怪，但這是正常做法
非同步系統。您也可以將此類呼叫連結在一起：

```{code-block}
:linenos:
:emphasize-lines: 19,22,28,34

from evennia import default_cmds, utils
    
class CmdEcho(default_cmds.MuxCommand):
    """
    waits for an echo
    
    Usage: 
      echo <string>
    
    Calls and waits for an echo
    """
    key = "echo"
    
    def func(self):
        "This sets off a chain of delayed calls"
        self.caller.msg(f"You shout '{self.args}', waiting for an echo ...")

        # wait 2 seconds before calling self.echo1
        utils.delay(2, self.echo1)
    
    # callback chain, started above
    def echo1(self):
        "First echo"
        self.caller.msg(f"... {self.args.upper()}")
        # wait 2 seconds for the next one
        utils.delay(2, self.echo2)

    def echo2(self):
        "Second echo"
        self.caller.msg(f"... {self.args.capitalize()}")
        # wait another 2 seconds
        utils.delay(2, callback=self.echo3)

    def echo3(self):
        "Last echo"
        self.caller.msg(f"... {self.args.lower()} ...")
```

上面的版本將讓迴聲一個接一個地到達，每個迴聲相隔兩秒
延遲。

- **第 19 行**：這會啟動鏈，告訴 Evennia 在呼叫 `self.echo1` 之前等待 2 秒。
- **第 22 行**：2 秒後呼叫。它告訴 Evennia 在呼叫 `self.echo2` 之前再等待 2 秒。
- **第 28 行**：再過 2 秒（總共 4 秒）後呼叫。它告訴 Evennia 在呼叫 `self.echo3` 之前再等待 2 秒。
- **第 34 行** 再過 2 秒（總共 6 秒）後呼叫。這結束了延遲鏈。

```
> echo Hello!
... HELLO!
... Hello!
... hello! ...
```

```{warning} 那time.sleep呢？

您可能知道 Python 附帶的 `time.sleep` 函式。執行 `time.sleep(10) 會使 Python 暫停 10 秒。 **不要使用這個**，它不能與 Evennia 一起使用。如果您使用它，您將阻止_整個伺服器_（所有人！）十秒鐘！

如果您需要具體資訊，`utils.delay` 是 [Twisted Deferred](https://docs.twisted.org/en/twisted-22.1.0/core/howto/defer.html) 的薄包裝。這是一個[非同步概念](../Concepts/Async-Process.md)。
```

(making-a-blocking-command)=
## 制定阻塞指令

`yield` 或 `utils.delay()` 都會暫停指令，但允許使用者在第一個指令等待完成時使用其他指令。

在某些情況下，您希望讓該指令「阻止」其他指令執行。一個例子是製作頭盔：很可能您不應該能夠同時開始製作盾牌。或甚至走出鐵匠鋪。

實現阻塞最簡單的方法是使用[如何實現指令冷卻](./Howto-Command-Cooldown.md) 教學中介紹的技術。在該教學中，我們透過將當前時間與上次使用該指令的時間進行比較來實現冷卻時間。如果你能逃脫懲罰的話，這是最好的方法。它可以很好地用於我們的製作範例......_如果_您不想自動更新玩家的進度。

簡而言之：
    - 如果您同意玩家主動輸入以檢查其狀態，請按照指令冷卻教學中的方式比較時間戳記。按需是迄今為止最有效的。
    - 如果您希望 Evennia 告訴使用者他們的狀態而不需要他們採取進一步的操作，您需要使用 `yield` 、 `delay` （或其他一些主動計時方法）。

這是一個範例，我們將使用 `utils.delay` 告訴玩家冷卻時間已過：

```python
from evennia import utils, default_cmds
    
class CmdBigSwing(default_cmds.MuxCommand):
    """
    swing your weapon in a big way

    Usage:
      swing <target>
    
    Makes a mighty swing. Doing so will make you vulnerable
    to counter-attacks before you can recover. 
    """
    key = "bigswing"
    locks = "cmd:all()"
    
    def func(self):
        "Makes the swing" 

        if self.caller.ndb.off_balance:
            # we are still off-balance.
            self.caller.msg("You are off balance and need time to recover!")
            return      
      
        # [attack/hit code goes here ...]
        self.caller.msg("You swing big! You are off balance now.")   

        # set the off-balance flag
        self.caller.ndb.off_balance = True
            
        # wait 8 seconds before we can recover. During this time 
        # we won't be able to swing again due to the check at the top.        
        utils.delay(8, self.recover)
    
    def recover(self):
        "This will be called after 8 secs"
        del self.caller.ndb.off_balance            
        self.caller.msg("You regain your balance.")
```    

請注意，冷卻後，使用者將收到一條訊息，告訴他們現在已準備好
另一個揮桿。

透過將 `off_balance` 標誌儲存在角色上（而不是在指令例項上）
本身）它也可以被其他指令存取。當你失去平衡時，其他攻擊也可能不起作用。舉另一個例子，你還可以讓敵人指揮部檢查你的 `off_balance` 狀態以獲得獎勵。

(make-a-command-possible-to-abort)=
## 使指令可以中止

人們可以想像，您希望在長時間執行的指令完成之前中止它。
如果你正在製作你的盔甲，你可能會想停止這樣做，當
怪物進入你的鐵匠鋪。

您可以按照與上面的“阻止”指令相同的方式來實現此操作，只是相反。
以下是一個可以透過開始戰鬥來中止的製作指令的範例：

```python
from evennia import utils, default_cmds
    
class CmdCraftArmour(default_cmds.MuxCommand):
    """
    Craft armour
    
    Usage:
       craft <name of armour>
    
    This will craft a suit of armour, assuming you
    have all the components and tools. Doing some
    other action (such as attacking someone) will 
    abort the crafting process. 
    """
    key = "craft"
    locks = "cmd:all()"
    
    def func(self):
        "starts crafting"

        if self.caller.ndb.is_crafting:
            self.caller.msg("You are already crafting!")
            return 
        if self._is_fighting():
            self.caller.msg("You can't start to craft "
                            "in the middle of a fight!")
            return
            
        # [Crafting code, checking of components, skills etc]          

        # Start crafting
        self.caller.ndb.is_crafting = True
        self.caller.msg("You start crafting ...")
        utils.delay(60, self.step1)
    
    def _is_fighting(self):
        "checks if we are in a fight."
        if self.caller.ndb.is_fighting:                
            del self.caller.ndb.is_crafting 
            return True
      
    def step1(self):
        "first step of armour construction"
        if self._is_fighting(): 
            return
        self.msg("You create the first part of the armour.")
        utils.delay(60, callback=self.step2)

    def step2(self):
        "second step of armour construction"
        if self._is_fighting(): 
            return
        self.msg("You create the second part of the armour.")            
        utils.delay(60, step3)

    def step3(self):
        "last step of armour construction"
        if self._is_fighting():
            return          
    
        # [code for creating the armour object etc]

        del self.caller.ndb.is_crafting
        self.msg("You finalize your armour.")
    
    
# example of a command that aborts crafting
    
class CmdAttack(default_cmds.MuxCommand):
    """
    attack someone
    
    Usage:
        attack <target>
    
    Try to cause harm to someone. This will abort
    eventual crafting you may be currently doing. 
    """
    key = "attack"
    aliases = ["hit", "stab"]
    locks = "cmd:all()"
    
    def func(self):
        "Implements the command"

        self.caller.ndb.is_fighting = True
    
        # [...]
```

上面的程式碼建立了一個延遲的製作指令，它將逐漸建立盔甲。如果
`attack`指令在此過程中發出，它將設定一個標誌，導致製作
下次嘗試更新時悄悄取消。
