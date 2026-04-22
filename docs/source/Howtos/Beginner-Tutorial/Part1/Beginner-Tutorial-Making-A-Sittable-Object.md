(building-a-chair-you-can-sit-on)=
# 建造一張可以坐的椅子

在本課中，我們將利用所學來創造一個新的遊戲物件：一張可以坐的椅子。

我們的目標是：

- 我們想要一個新的「可坐」物件，特別是 `Chair`。
- 我們希望能夠使用指令坐在椅子上。
- 一旦我們坐在椅子上，它就會以某種方式影響我們。為了展示這家店
當前主席在 attribute `is_sitting`。其他系統可以檢查這一點並以不同的方式影響我們。
- 角色應該能夠站起來並離開椅子。
- 當您坐下時，如果沒有先站起來，您不應該能夠走到另一個房間。

(make-us-not-able-to-move-while-sitting)=
## 讓我們坐著時無法動彈

當你坐在椅子上時，你不能不先站起來就走開。
這需要改變我們的角色typeclass。開啟`mygame/typeclasses/characters.py`：

```python
# in mygame/typeclasses/characters.py

# ...

class Character(DefaultCharacter):
    # ...

    def at_pre_move(self, destination, **kwargs):
       """
       Called by self.move_to when trying to move somewhere. If this returns
       False, the move is immediately cancelled.
       """
       if self.db.is_sitting:
           self.msg("You need to stand up first.")
           return False
       return True

```

當移動到某個地方時，會呼叫[character.move_to](evennia.objects.objects.DefaultObject.move_to)。這反過來
將呼叫`character.at_pre_move`。  如果返回 `False`，則移動將中止。

在這裡，我們尋找 Attribute `is_sitting`（我們將在下面分配）來確定我們是否被困在椅子上。

(making-the-chair-itself)=
## 自己製作椅子

接下來我們需要椅子本身，或者更確切地說是一整套“你可以坐的東西”，我們稱之為_sittables_。我們不能只使用預設物件，因為我們想要一個可坐的東西包含一些自訂程式碼。我們需要一個新的自訂Typeclass。建立一個新模組 `mygame/typeclasses/sittables.py` 並包含以下內容：

```{code-block} python
:linenos:
:emphasize-lines: 3,7,15,16,23,24,25

# in mygame/typeclasses/sittables.py

from typeclasses.objects import Object

class Sittable(Object):

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.

        Args:
            sitter (Object): The one trying to sit down.

        """
        current = self.db.sitter
        if current:
            if current == sitter:
                sitter.msg(f"You are already sitting on {self.key}.")
            else:
                sitter.msg(f"You can't sit on {self.key} "
                        f"- {current.key} is already sitting there!")
            return
        self.db.sitter = sitter
        sitter.db.is_sitting = self
        sitter.msg(f"You sit on {self.key}")
```

這處理了某人坐在椅子上的邏輯。

- **第3行**：我們從`mygame/typeclasses/objects.py`中的空`Object`類別繼承。這意味著我們理論上可以在未來修改它，並使這些變化也影響到可坐的東西。
- **第 7 行**：`do_sit` 方法期望使用引數 `sitter` 進行呼叫，該引數是 `Object`（最有可能是 `Character`）。這是那個想坐下來的人。
-  **第 15 行**：請注意，如果椅子上未定義 [Attribute](../../../Components/Attributes.md) `sitter`（因為這是有人第一次坐在椅子上），則只會返回 `None`，這很好。
- **第 16-22 行** 我們檢查是否有人已經坐在椅子上，並根據是您還是其他人返回相應的錯誤訊息。我們使用 `return` 來中止靜坐動作。
- **第 23 行**：如果我們到達這一點，`sitter` 就可以坐下了。我們將它們存放在椅子上的`sitter` Attribute 中。
- **第 24 行**：`self.obj` 是指令所附加的椅子。我們將其儲存在 `sitter` 本身的 `is_sitting` Attribute 中。
- **第 25 行**：最後我們告訴保母他們可以坐下了。

我們繼續：

```{code-block} python 
:linenos: 
:emphasize-lines: 12,15,16,17

# add this right after the `do_sit method` in the same class 

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.

        """
        current = self.db.sitter
        if not stander == current:
            stander.msg(f"You are not sitting on {self.key}.")
        else:
            self.db.sitter = None
            del stander.db.is_sitting
            stander.msg(f"You stand up from {self.key}.")
```

這是坐下的逆過程；我們需要做一些清理工作。

- **第12行**：如果我們沒有坐在椅子上，那麼從椅子上站起來就沒有意義。
- **15號線**：如果我們到了這裡，我們就可以站起來了。我們確保取消設定 `sitter` Attribute，以便其他人稍後可以使用椅子。
- **第16行**：角色不再坐著，所以我們刪除他們的`is_sitting` Attribute。我們也可以在這裡完成 `stander.db.is_sitting = None`，但刪除 Attribute 感覺更乾淨。
- **第17行**：最後，我們通知他們站起來成功了。

人們可以想像，可以使用未來的 `sit` 指令（我們尚未建立）來檢查是否有人已經坐在椅子上。這也可以，但是讓 `Sittable` 類處理誰可以坐在上面的邏輯是有意義的。

我們讓 typeclass 處理邏輯，並讓它處理所有回傳訊息。這樣就可以很容易地製作出一堆椅子供人坐。

(sitting-on-or-in)=
### 坐在上面還是裡面？

坐在椅子上很好。但如果我們的坐桌是一張扶手椅呢？

```
> py evennia.create_object("typeclasses.sittables.Sittable", key="armchair", location=here)
> py self.search("armchair").do_sit(me)
You sit on armchair.
```

這在語法上是不正確的，你實際上是坐在扶手椅“裡面”，而不是“坐在”扶手椅上。椅子的型別很重要（英語很奇怪）。我們希望能夠控制這一點。

我們_可以_建立一個名為 `SittableIn` 的 `Sittable` 子類別來進行此更改，但這感覺有點過分了。相反，我們將修改我們所擁有的：

```{code-block} python 
:linenos:
:emphasize-lines: 15,19,22,27,39,43

# in mygame/typeclasses/sittables.py

from typeclasses.objects import Object

class Sittable(Object):

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.

        Args:
            sitter (Object): The one trying to sit down.

        """
        preposition = self.db.preposition or "on"
        current = self.db.sitter
        if current:
            if current == sitter:
                sitter.msg(f"You are already sitting {preposition} {self.key}.")
            else:
                sitter.msg(
                    f"You can't sit {preposition} {self.key} "
                    f"- {current.key} is already sitting there!")
            return
        self.db.sitter = sitter
        sitter.db.is_sitting = self
        sitter.msg(f"You sit {preposition} {self.key}")

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.

        """
        current = self.db.sitter
        if not stander == current:
            stander.msg(f"You are not sitting {self.db.preposition} {self.key}.")
        else:
            self.db.sitter = None
            del stander.db.is_sitting
            stander.msg(f"You stand up from {self.key}.")
```

- **第 15 行**：我們抓取 `preposition` Attribute。此處使用 `self.db.preposition or "on"` 意味著如果未設定 Attribute（是 `None`/falsy），則將採用預設的「on」字串。這是因為 `or` 關係將傳回第一個 true 條件。更明確的編寫方法是使用 [三元運運算元](https://www.dataquest.io/blog/python-ternary-operator/) `self.db.preposition if self.db.preposition else "on"`。
- **第 19、22、27、39 和 43 行**：我們使用此介詞來修改我們看到的回傳文字。

`reload` 伺服器。使用這樣的屬性的一個優點是它們可以在遊戲中動態修改。讓我們看看建構器如何將其與普通建置指令一起使用（不需要 `py`）：

```
> set armchair/preposition = in 
```

由於我們還沒有新增`sit`指令，所以我們仍然必須使用`py`來測試：

```
> py self.search("armchair").do_sit(me)
You sit in armchair.
```

(extra-credits)=
### 額外學分

當您坐在某些椅子上時，如果我們想要一些更戲劇性的天賦怎麼辦？

    You sit down and a whoopie cushion makes a loud fart noise!

您可以透過調整 `Sittable` 類別來實現這一點，使回傳訊息可由您在建立的物件上設定的 `Attributes` 取代。你想要這樣的東西：

```
> py 
> chair = evennia.create_object("typeclasses.sittables.Sittable", key="pallet", location=here)
> chair.do_sit(me)
You sit down on pallet.
> chair.do_stand(me)
You stand up from pallet.
> chair.db.msg_sitting_down = "You sit down and a whoopie cushion makes a loud fart noise!"
> chair.do_sit(me)
You sit down and a whoopie cushion makes a loud fart noise!
```

也就是說，如果您沒有設定Attribute，您應該獲得預設值。 
我們將這個實作留給讀者。

(adding-commands)=
## 新增指令

正如我們在[關於新增指令的課程](./Beginner-Tutorial-More-on-Commands.md)中討論的，設計坐下和站立指令的主要方法有兩種：
- 您可以將指令存放在椅子上，這樣只有當房間裡有椅子時它們才可用
- 您可以將指令儲存在角色上，以便它們始終可用，並且您必須始終指定坐在哪張椅子上。

瞭解這兩者都非常有用，因此在本課中我們將嘗試兩者。

(command-variant-1-commands-on-the-chair)=
### 指令變體 1：在椅子上發出指令

這種實現`sit`和`stand`的方法將新的cmdsets放在Sittable本身上。
正如我們之前所瞭解的，房間中的其他人可以使用物件上的指令。
這使得指令變得簡單，但反而增加了 CmdSet 管理的複雜度。

如果 `armchair` 在房間裡，情況如下（附加積分：更改扶手椅上的坐訊息以匹配此輸出，而不是獲取預設的 `You sit in armchair`！）：

    > sit
    As you sit down in armchair, life feels easier.

如果房間裡還有可坐的 `sofa` 和 `barstool` 會怎麼樣？ Evennia 將會
自動為我們處理這個問題，並允許我們指定我們想要哪一個：

    > sit
    More than one match for 'sit' (please narrow target):
     sit-1 (armchair)
     sit-2 (sofa)
     sit-3 (barstool)
    > sit-1
    As you sit down in armchair, life feels easier.

為了保持分離，我們將建立一個新模組`mygame/commands/sittables.py`：

```{sidebar} 單獨的指令和Typeclasses？

您可以根據自己的喜好組織這些內容。如果您願意，可以將坐指令 + cmdset 與 `Sittable` typeclass 放在 `mygame/typeclasses/sittables.py` 中。這樣做的好處是可以將與坐相關的所有事情集中在一個地方。但是，像我們在這裡所做的那樣，將所有指令保留在一個地方也有一些組織上的優點。
```

```{code-block} python
:linenos: 
:emphasize-lines: 11,19,23

# in mygame/commands/sittables.py 

from evennia import Command, CmdSet

class CmdSit(Command):
    """
    Sit down.
    """
    key = "sit"
    def func(self):
        self.obj.do_sit(self.caller)

class CmdStand(Command):
     """
     Stand up.
     """
     key = "stand"
     def func(self):
         self.obj.do_stand(self.caller)


class CmdSetSit(CmdSet):
    priority = 1
    def at_cmdset_creation(self):
        self.add(CmdSit)
        self.add(CmdStand)

```

如所見，這些指令幾乎是微不足道的。

- **第 11 行和第 19 行**：`self.obj` 是我們使用此指令新增 cmdset 的物件（因此是椅子）。我們只需呼叫該物件的 `do_sit/stand` 並傳遞 `caller`（坐下的人）。 `Sittable` 將完成剩下的工作。
- **第 23 行**：`CmdSetSit` 上的 `priority = 1` 表示來自此 cmdset 的同名指令合併的優先順序比來自角色上的指令 -cmdset（具有 `priority = 0`）的優先順序稍高。這意味著，如果您的角色有 `sit` 指令並進入有椅子的房間，則椅子上的 `sit` 指令將優先。

我們還需要對 `Sittable` typeclass 進行更改。開啟`mygame/typeclasses/sittables.py`：

```{code-block} python 
:linenos: 
:emphasize-lines: 4,10,11

# in mygame/typeclasses/sittables.py

from typeclasses.objects import Object
from commands.sittables import CmdSetSit 

class Sittable(Object):
    """
    (docstring)
    """
    def at_object_creation(self):
        self.cmdset.add_default(CmdSetSit)
    # ... 
```

- **第 4 行**：我們必須安裝 `CmdSetSit` 。
- **第 10 行**：`at_object_creation` 方法只會在第一次建立物件時呼叫一次。
- **第 11 行**：我們將指令集新增為「預設」cmdset 和 `add_default`。這使其持久化，並防止在新增另一個 cmdset 時被刪除。有關詳細資訊，請參閱[指令集](../../../Components/Command-Sets.md)。

確保 `reload` 使程式碼變更可用。
	
所有_新_Sittables 現在都將擁有您的`sit` 指令。但你現有的 `armchair` 不會。這是因為 `at_object_creation` 不會針對已存在的物件重新執行。我們可以手動更新：

    > update armchair

我們也可以更新所有現有的可坐桌（全部在一行上）：

```{sidebar} 列表推導式
`[obj for obj in iterator]` 是_列表理解_的範例。將其視為在一行中建立新清單的有效方法。您可以[在 Python 檔案中](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) 閱讀更多關於清單推導式的資訊。
```

    > py from typeclasses.sittables import Sittable ;
           [sittable.at_object_creation() for sittable in Sittable.objects.all()]

我們現在應該能夠在有扶手椅的房間裡使用`sit`。

    > sit
    As you sit down in armchair, life feels easier.
    > stand
    You stand up from armchair.

將 `sit`（或 `stand`）指令放置在椅子「上」的一個問題是，當房間裡沒有可坐的物體時，該指令將不可用：

    > sit
    Command 'sit' is not available. ...

這個很實用，但是不太好看；它使使用者更難知道 `sit` 操作是否可行。這是解決這個問題的技巧。讓我們在底部加上_another_指令
`mygame/commands/sittables.py`：

```{code-block} python 
:linenos: 
:emphasize-lines: 9,12

# after the other commands in mygame/commands/sittables.py
# ...

class CmdNoSitStand(Command):
    """
    Sit down or Stand up
    """
    key = "sit"
    aliases = ["stand"]

    def func(self):
        if self.cmdname == "sit":
            self.msg("You have nothing to sit on.")
        else:
            self.msg("You are not sitting down.")

```

- **第 9 行**：此指令同時回應 `sit` 和 `stand`，因為我們將 `stand` 新增至其 `aliases` 清單中。指令別名與指令的 `key` 具有相同的“權重”，兩者同等地標識指令。
- **第 12 行**：`Command` 的 `.cmdname` 儲存實際用來呼叫它的名稱。這將是 `"sit"` 或 `"stand"` 之一。  這會導致不同的返回訊息。

為此，我們不需要新的CmdSet，而是將其新增到預設字元cmdset。開啟`mygame/commands/default_cmdsets.py`：

```python
# in mygame/commands/default_cmdsets.py

# ...
from commands import sittables

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    (docstring)
    """
    def at_cmdset_creation(self):
        # ...
        self.add(sittables.CmdNoSitStand)

```

與往常一樣，請確保`reload`伺服器能夠識別新程式碼。

為了進行測試，我們將建立一個沒有任何舒適扶手椅的新位置，然後前往那裡：

    > tunnel n = kitchen
    north
    > sit
    You have nothing to sit on.
    > south
    sit
    As you sit down in armchair, life feels easier.

現在我們有了一個功能齊全的 `sit` 動作，它包含在椅子本身中。當周圍沒有椅子時，會顯示預設錯誤訊息。

這是如何運作的？有兩個 cmdsets 在玩，兩個都有 `sit/stand` 指令 - 一個在 `Sittable`（扶手椅）上，另一個在我們身上（透過 `CharacterCmdSet`）。由於我們在椅子的cmdset上設定了`priority=1`（並且`CharacterCmdSet`有`priority=0`），因此不會有指令衝突：椅子的`sit`優先於我們定義的`sit`......直到周圍沒有椅子。

所以這處理`sit`。那`stand`呢？那會工作得很好：

    > stand
    You stand up from armchair.
    > north
    > stand
    You are not sitting down.

不過，我們還有一個關於 `stand` 的問題 - 當你坐下來嘗試在一個有多個 `Sittable` 的房間裡進行 `stand` 時會發生什麼：

    > stand
    More than one match for 'stand' (please narrow target):
     stand-1 (armchair)
     stand-2 (sofa)
     stand-3 (barstool)

由於所有的可坐桌都有 `stand` 指令，因此您將收到多重匹配錯誤。這_有效_......但是你可以選擇_任何_這些坐墊來「站起來」。這真的很奇怪。

對於 `sit` 來說，有一個選擇是可以的 - Evennia 不知道我們打算坐在哪張椅子上。但一旦我們坐下來，我們就知道該從哪張椅子上站起來！我們必須確保我們只從我們實際坐的椅子上得到指令。

我們將使用 [Lock](../../../Components/Locks.md) 和自訂 `lock function` 來修復此問題。我們希望 `stand` 指令上有 lock，僅當呼叫者實際坐在特定 `stand` 指令所連線的椅子上時才可用。

首先讓我們加入lock，這樣我們就可以看到我們想要的內容。開啟`mygame/commands/sittables.py`：

```{code-block} python 
:linenos:
:emphasize-lines: 10

# in mygame/commands/sittables.py

# ...

class CmdStand(Command):
     """
     Stand up.
     """
     key = "stand"
     locks = "cmd:sitsonthis()"

     def func(self):
         self.obj.do_stand(self.caller)
# ...
```

- **第 10 行**：這是 lock 定義。其格式為 `condition:lockfunc`。在確定使用者是否有權存取指令時，Evennia 將檢查 `cmd:` 型別 lock。如果此指令位於呼叫者所坐的椅子上，我們希望 lock 函式只傳回 `True`。
將檢查的是 `sitsonthis` _lock function_ 尚不存在。

開啟`mygame/server/conf/lockfuncs.py`新增！

```python
# mygame/server/conf/lockfuncs.py

"""
(module lockstring)
"""
# ...

def sitsonthis(accessing_obj, accessed_obj, *args, **kwargs):
    """
    True if accessing_obj is sitting on/in the accessed_obj.
    """
    return accessed_obj.obj.db.sitter == accessing_obj

# ...
```

Evennia 知道 `mygame/server/conf/lockfuncs` 中的 _all_ 函式應該可以在 lock 定義中使用。

所有 lock 函式必須接受相同的引數。引數是必需的，Evennia 將根據需要傳遞所有相關物件。

```{sidebar} Lockfuncs

Evennia提供了大量的預設lockfuncs，例如檢查許可權級別，是否攜帶或在存取物件內部等。但是預設Evennia中沒有「坐」的概念，所以這個需要我們自己指定。
```

- `accessing_obj` 是嘗試訪問lock 的人。在這種情況下，我們也是如此。
- `accessed_obj` 是我們試圖取得特定型別存取許可權的實體。由於我們在 `CmdStand` 類別上定義了 lock，因此這是_指令例項_。然而，我們對此不感興趣，而是指令分配給的物件（椅子）。該物件在指令上可用為 `.obj`。所以在這裡，`accessed_obj.obj` 是椅子。
- `args` 是一個元組，儲存傳遞給 lockfunc 的任何引數。由於我們使用 `sitsondthis()` 這將是空的（如果我們新增任何內容，它將被忽略）。
- `kwargs` 是傳遞給 lockfuncs 的關鍵字引數的元組。在我們的範例中，這也將是空的。

確保你`reload`。

如果您是超級使用者，那麼在嘗試此操作之前您自己 `quell` 很重要。這是因為超級使用者繞過所有鎖 - 它永遠不會被鎖定，但這意味著它也不會看到像這樣的 lock 的效果。

    > quell
    > stand
    You stand up from armchair

其他 sattables 的 `stand` 指令都沒有透過 lock，只有我們實際坐的那個指令透過了！現在這是一張功能齊全的椅子！

像這樣為椅子物件新增指令非常強大，也是一項值得了解的好技術。但正如我們所見，它確實有一些警告。

我們現在將嘗試另一種方法來新增 `sit/stand` 指令。

(command-variant-2-command-on-character)=
### 指令變體 2：對角色的指令

在我們開始之前，請刪除您建立的椅子：

	> 德爾扶手椅
	> 德爾沙發
	> （ETC）

進行以下更改：

- 在`mygame/typeclasses/sittables.py`中，註解掉整個`at_object_creation`方法。
- 在`mygame/commands/default_cmdsets.py`中，註解掉`self.add(sittables.CmdNoSitStand)`行。

這會禁用物件上指令解決方案，因此我們可以嘗試替代方案。確保 `reload` 以便 Evennia 知道更改。

在此變體中，我們將把 `sit` 和 `stand` 指令放在 `Character` 而不是椅子上。這使得一些事情變得更容易，但也使指令本身變得更加複雜，因為他們不知道該坐在哪張椅子上。我們不能再只做`sit`了。其工作原理如下：

    > sit <chair>
    You sit on chair.
    > stand
    You stand up from chair.

再次開啟`mygame/commands/sittables.py`。我們將新增一個新的坐指令。我們將類別命名為 `CmdSit2`，因為我們已經從上一個範例中獲得了 `CmdSit`。我們將所有內容放在模組的末尾以使其保持獨立。

```{code-block} python 
:linenos:
:emphasize-lines: 4,27,32,35

# in mygame/commands/sittables.py

from evennia import Command, CmdSet
from evennia import InterruptCommand

class CmdSit(Command):
    # ...

# ...

# new from here

class CmdSit2(Command):
    """
    Sit down.

    Usage:
        sit <sittable>

    """
    key = "sit"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Sit on what?")
            raise InterruptCommand

    def func(self):

        # self.search handles all error messages etc.
        sittable = self.caller.search(self.args)
        if not sittable:
            return
        try:
            sittable.do_sit(self.caller)
        except AttributeError:
            self.caller.msg("You can't sit on that!")

```

```{sidebar} 引發例外

引發異常可以立即中斷目前的程式流程。當偵測到程式碼問題時，Python 會自動引發錯誤異常。它將透過被呼叫程式碼的序列（「堆疊」）向上提升，直到它達到帶有 `try... except` 的 `caught` 或到達將記錄或顯示的最外層範圍。在這種情況下，Evennia 知道捕獲 `InterruptCommand` 異常並提前停止指令執行。
```

- **第 4 行**：我們需要 `InterruptCommand` 才能提前中止指令解析（見下文）。
- **第 27 行**：`parse` 方法在 `Command` 上的 `func` 方法之前執行。如果沒有向指令提供引數，我們希望儘早失敗，已經在 `parse` 中，因此 `func` 永遠不會觸發。僅 `return` 還不夠，我們需要 `raise InterruptCommand`。 Evennia 將看到一個凸起的 `InterruptCommand` 作為一個標誌，它應該立即中止指令執行。
- **第 32 行**：我們使用解析後的指令引數作為要搜尋的目標主席。正如[搜尋教學](./Beginner-Tutorial-Searching-Things.md) 中所討論的，`self.caller.search()` 將自行處理錯誤訊息。因此，如果它返回`None`，我們就可以`return`。
- **第 35-38 行**：`try...except` 區塊「捕獲」異常並處理它。在本例中，我們嘗試在物件上執行 `do_sit`。如果我們找到的物件不是 `Sittable`，它可能沒有 `do_sit` 方法，並且會引發 `AttributeError`。我們應該優雅地處理這個案子。

讓我們執行 `stand` 指令。由於指令位於椅子外部，因此我們需要確定我們是否坐下。

```{code-block} python 
:linenos:
:emphasize-lines: 17,21

# end of mygame/commands/sittables.py

class CmdStand2(Command):
    """
    Stand up.

    Usage:
        stand

    """
    key = "stand"

    def func(self):
        caller = self.caller
        # if we are sitting, this should be set on us
        sittable = caller.db.is_sitting
        if not sittable:
            caller.msg("You are not sitting down.")
        else:
            sittable.do_stand(caller)

```

- **第 17 行**：對於這些指令的第一個版本，我們不需要 `is_sitting` Attribute，但我們現在確實需要它。有了這個，我們就不需要搜尋並知道我們坐在哪張椅子上。如果我們沒有設定Attribute，我們就不會坐在任何地方。
- **第 21 行**：我們使用找到的可坐桌站起來。


現在剩下的就是讓 `sit` 和 `stand` 可供我們使用。這種型別的指令應該始終可供我們使用，因此我們可以將其放在角色的預設 Cmdset 中。開啟`mygame/commands/default_cmdsets.py`。


```python
# in mygame/commands/default_cmdsets.py

# ...
from commands import sittables

class CharacterCmdSet(CmdSet):
    """
    (docstring)
    """
    def at_cmdset_creation(self):
        # ...
        self.add(sittables.CmdSit2)
        self.add(sittables.CmdStand2)

```

確保`reload`。

現在我們來嘗試一下：

    > create/drop sofa : sittables.Sittable
    > sit sofa
    You sit down on sofa.
    > stand
    You stand up from sofa.
    > north 
    > sit sofa 
    > You can't find 'sofa'.

在角色上儲存指令可以集中它們，但您必須搜尋或儲存您希望該指令與之互動的任何外部物件。

(conclusions)=
## 結論

在本課中，我們為自己製作了一張椅子，甚至一張沙發！

- 我們修改了 `Character` 類以避免坐下時移動。
- 我們做了一個新的`Sittable` typeclass
- 我們嘗試了兩種方法來允許使用者使用`sit`和`stand`指令與sittables互動。

目光敏銳的讀者會注意到，坐在椅子「上」的 `stand` 指令（變體 1）可以與坐在角色「上」的 `sit` 指令（變體 2）一起工作。沒有什麼可以阻止您混合它們，甚至嘗試更適合您想法的第三種解決方案。

初學者教學的第一部分到此結束！
