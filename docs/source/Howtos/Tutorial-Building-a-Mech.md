(building-a-giant-mech)=
# 建造巨型機甲

讓我們在Evennia中創造一個運作良好的巨型機甲。每個人都喜歡巨型機甲，對吧？以具有建置許可權的角色（或超級使用者）開始遊戲。

    create/drop Giant Mech ; mech

繁榮。我們建立了一個巨型機甲物體並將其扔到房間裡。我們也給它取了一個別名*mech*。
我們來描述一下。

    desc mech = This is a huge mech. It has missiles and stuff.

接下來我們定義誰可以「操縱」機甲物件。

    lock mech = puppet:all()

這使得每個人都可以控制機甲。為人民提供更多機甲！ （請注意，雖然 Evennia 的預設指令可能看起來有點像 MUX-，但您可以更改語法以使其看起來像您喜歡的任何介面風格。）

在繼續之前，讓我們先繞一下。 Evennia 對於它的物件非常靈活，對於使用和向這些物件新增指令甚至更加靈活。對於本文的其餘部分，以下是一些值得記住的基本規則：

- [帳號](../Components/Accounts.md)代表真人登入，不存在遊戲世界。
- 任何[物件](../Components/Objects.md) 都可以被帳號操縱（具有適當的許可權）。
- [字元](../Components/Objects.md#characters)、[房間](../Components/Objects.md#rooms) 和[出口](../Components/Objects.md#exits) 只是普通物件的子物件。
- 任何物件都可以位於另一個物件內部（除非它建立了迴圈）。
- 任何物件都可以在其上儲存自訂指令集。這些指令可以：
    - 可供木偶操縱者（帳號）使用，
    - 可供與物件位於同一位置的任何人使用，且
    - 可供物件「內部」的任何人使用
    - 帳戶還可以儲存自己的指令。帳戶指令始終可用，除非傀儡物件上的指令明確覆蓋它們。

在 Evennia 中，使用 `ic` 指令將允許您操縱給定的物件（假設您具有操縱許可權來執行此操作）。如上所述，沼澤標準的角色類別實際上就像任何物件一樣：它在登入時會自動傀儡，並且只有一個指令集，其中包含正常的遊戲內指令，例如檢視、庫存、獲取等。

    ic mech

你剛剛跳出了你的角色，現在*是*機甲了！如果人們在遊戲中看著你，他們
會看機甲。此時的問題是機械物件沒有自己的指令。
常見的事情，例如檢視、庫存和坐在角色物件上，還記得嗎？所以在
此刻，機甲並沒有想像中那麼酷。

    ic <Your old Character>

你剛剛又跳回傀儡你正常的、平凡的角色。一切都很好。

> 如果機甲上沒有指令，那麼 `ic` 指令從何而來？這
答案是它來自`Account`的指令集。這很重要。如果該帳戶不是使用 `ic` 指令的帳戶，我們將無法再次登出我們的機甲。

(make-a-mech-that-can-shoot)=
## 製作一個可以射擊的機甲

讓我們讓機甲變得更有趣一點。在我們最喜歡的文字編輯器中，我們將建立一些新的
適合機甲的指令。在Evennia中，指令被定義為Python類別。

```python
# in a new file mygame/commands/mechcommands.py

from evennia import Command

class CmdShoot(Command):
    """
    Firing the mech’s gun

    Usage:
      shoot [target]

    This will fire your mech’s main gun. If no
    target is given, you will shoot in the air.
    """
    key = "shoot"
    aliases = ["fire", "fire!"]

    def func(self):
        "This actually does the shooting"

        caller = self.caller
        location = caller.location

        if not self.args:
            # no argument given to command - shoot in the air
            message = "BOOM! The mech fires its gun in the air!"
            location.msg_contents(message)
            return

        # we have an argument, search for target
        target = caller.search(self.args.strip())
        if target:
            location.msg_contents(
                f"BOOM! The mech fires its gun at {target.key}"
            )

class CmdLaunch(Command):
    # make your own 'launch'-command here as an exercise!
    # (it's very similar to the 'shoot' command above).

```

這被儲存為普通的 Python 模組（我們稱之為 `mechcommands.py`），在 Evennia 的地方查詢此類模組（`mygame/commands/`）。當玩家發出「射擊」、「開火」甚至「開火！」指令時，該指令就會觸發。帶有感嘆號。如果你有的話，機甲可以在空中或目標上射擊。在真實的遊戲中，槍可能有機會擊中並給予
對目標造成傷害，但這已經足夠了。

我們也發出了第二個發射飛彈的指令（`CmdLaunch`）。為了節省篇幅，這裡不再描述；它看起來相同，只是它返回有關正在發射的導彈的文字並且具有不同的 `key` 和 `aliases`。我們將其留給您來建立作為練習。例如，您可以讓它列印`"WOOSH! The mech launches missiles against <target>!`。

現在我們將指令放入指令集中。 [指令集](../Components/Command-Sets.md) (CmdSet) 是容納任意數量指令的容器。指令集是我們將儲存在機械上的內容。

```python
# in the same file mygame/commands/mechcommands.py

from evennia import CmdSet
from evennia import default_cmds

class MechCmdSet(CmdSet):
    """
    This allows mechs to do do mech stuff.
    """
    key = "mechcmdset"

    def at_cmdset_creation(self):
        "Called once, when cmdset is first created"
        self.add(CmdShoot())
        self.add(CmdLaunch())
```

這只是將我們想要的所有指令分組。我們新增了新的射擊/發射指令。讓我們回到遊戲中。為了進行測試，我們將手動將新的CmdSet附加到機械上。

    py self.search("mech").cmdset.add("commands.mechcommands.MechCmdSet")

這是一個小的 Python 片段，用於搜尋目前位置的機甲並將新的 MechCmdSet 附加到它。我們新增的實際上是 cmdset 類別的 Python 路徑。 Evennia 將在幕後匯入並初始化它。

    ic mech

我們作為機甲回來了！讓我們進行一些拍攝吧！

    fire!
    BOOM! The mech fires its gun in the air!

就這樣，一臺正常運轉的機甲。嘗試您自己的 `launch` 指令，看看它是否也有效。我們不僅可以作為機甲四處走動——因為CharacterCmdSet包含在我們的MechCmdSet中，所以機甲還可以做角色可以做的所有事情，比如環顧四周，撿起東西，並擁有庫存。我們現在可以用槍射擊目標或嘗試導彈發射指令。一旦你擁有了自己的機甲，你還需要什麼？

> 你會發現，只要站在同一個地方，就可以使用機甲的指令
位置（不僅僅是透過操縱它）。我們將在下一節中使用 *lock* 來解決這個問題。

(making-an-army-of-mechs)=
## 組一支機甲軍隊

到目前為止我們所做的只是建立一個普通的物件，描述它並在它上面放置一些指令。
這對於測試來說非常有用。按照我們新增的方式，如果我們重新載入，MechCmdSet 甚至會消失
伺服器。現在我們想讓機甲成為一個實際的物件“型別”，這樣我們就可以建立機甲而無需這些額外的步驟。為此，我們需要建立一個新的Typeclass。

[Typeclass](../Components/Typeclasses.md) 是一個接近普通的 Python 類，它將其存在儲存到資料庫中
在幕後。在普通的 Python 原始檔中建立 Typeclass：

```python
# in the new file mygame/typeclasses/mech.py

from typeclasses.objects import Object
from commands.mechcommands import MechCmdSet
from evennia import default_cmds

class Mech(Object):
    """
    This typeclass describes an armed Mech.
    """
    def at_object_creation(self):
        "This is called only when object is first created"
        self.cmdset.add_default(default_cmds.CharacterCmdSet)
        self.cmdset.add(MechCmdSet, persistent=True)
        self.locks.add("puppet:all();call:false()")
        self.db.desc = "This is a huge mech. It has missiles and stuff."
```

為了方便起見，我們在其中包含預設 `CharacterCmdSet` 的完整內容。這將使角色的正常指令可供機甲使用。我們還新增了先前的機械指令，確保它們持久地儲存在資料庫中。這些鎖規定任何人都可以操縱機甲，並且沒有人可以從機甲的“外部”“呼叫”機甲的指令 - 你必須操縱它才能射擊。

就是這樣。當建立這種型別的物件時，它們總是以機甲的指令集和正確的lock開始。我們設定了預設描述，但您可能會使用 `desc` 更改此描述，以便在建立機甲時個性化您的機甲。

回到遊戲，只需退出舊機甲（`@ic`回到你的舊角色）然後執行

    create/drop The Bigger Mech ; bigmech : mech.Mech

我們建立了一個新的、更大的機甲，別名為 bigmech。注意我們如何將 python-path 提供給我們的
Typeclass 最後 - 這告訴 Evennia 基於該類別建立新物件（我們不
必須提供我們遊戲目錄 `typeclasses.mech.Mech` 中的完整路徑，因為 Evennia 已經知道要查詢 `typeclasses` 資料夾）。一個閃亮的新機甲將出現在房間裡！只需使用

    ic bigmech

試駕一下。

(future-mechs)=
### 未來機甲

直接操縱機甲物件只是在 Evennia 中實現巨型機甲的一種方法。

例如，您可以將機甲想像成您正常“進入”的“車輛”
角色（因為任何物件都可以在另一個物件內部移動）。在這種情況下，機甲物體的「內部」可能是「駕駛艙」。駕駛艙本身會存放`MechCommandSet`，只有當你進入駕駛艙時，所有的射擊技巧才會提供給你。

要對此進行擴充套件，您可以向機甲新增更多指令並刪除其他指令。也許機甲畢竟不該像角色一樣運作。

也許它每次從一個房間經過另一個房間時都會發出很大的噪音。也許它無法在不壓碎東西的情況下撿起它們。也許它需要燃料、彈藥和修理。也許你會lock把它放下，這樣它就只能被情緒化的青少年操縱。

當然，你可以在上面放更多的槍。並讓它飛起來。