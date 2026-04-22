(evennia-for-mush-users)=
# Evennia 為 MUSH 使用者

*此頁面改編自最初為 MUSH 社群發布的文章 [此處
musoapbox.net](https://musoapbox.net/topic/1150/evennia-for-mushers).*

[MUSH](https://en.wikipedia.org/wiki/MUSH)es 是傳統上用於
高度重視角色扮演的遊戲風格。他們經常（但並非總是）利用遊戲大師和
人類對程式碼自動化的監督。 MUSHes 傳統上是基於 TinyMUSH 系列遊戲構建的
伺服器，例如 PennMUSH、TinyMUSH、TinyMUX 和 RhostMUSH。還有他們的兄弟姊妹
[MUCK](https://en.wikipedia.org/wiki/TinyMUCK) 和 [MOO](https://en.wikipedia.org/wiki/MOO) 是
經常與 MUSH 一起提及，因為它們都繼承自同一個
[TinyMUD](https://en.wikipedia.org/wiki/MUD_trees#TinyMUD_family_tree) 基礎。一個主要特點是
能夠使用自訂指令碼從遊戲內部修改和程式設計遊戲世界
語言。我們在此將此線上指令碼稱為「軟程式碼」。

Evennia 的工作方式與 MUSH 的整體設計和底層都有很大不同。一樣的
事情是可以實現的，只是方式不同而已。以下是一些需要保留的基本差異
如果你來自 MUSH 世界，請介意。

(developers-vs-players)=
## 開發者 vs 玩家

在MUSH中，使用者傾向於使用軟程式碼從遊戲內部編碼和擴充套件遊戲的各個方面。 MUSH
因此可以說是由具有不同存取等級的「玩家」單獨管理。 Evennia 上
另一方面，區分*玩家*和*開發者*的角色。

- Evennia *開發人員*在遊戲*外部*使用 Python 工作，MUSH 會考慮什麼
「硬編碼」。開發人員實施更大規模的程式碼更改，可以從根本上改變遊戲的方式
作品。然後他們將更改載入到正在執行的 Evennia 伺服器中。這種變化通常不會
刪除所有已連線的玩家。
- Evennia *玩家*在遊戲*內部*操作。一些職員級別的球員可能會加倍
作為開發商。根據訪問級別，玩家可以透過挖掘來修改和擴充套件遊戲世界
新房間、建立新物件、別名指令、客製化體驗等等。值得信賴的員工
可以透過`@py`指令存取Python，但這對普通玩家來說是一個安全風險
使用。所以*玩家*通常會利用玩家為他們準備的工具來操作。
*開發人員* - 工具可以根據開發人員的需求而嚴格或靈活。

(collaborating-on-a-game-python-vs-softcode)=
## 協作開發遊戲 - Python 與 Softcode

對於*玩家*來說，MUSH 和 Evennia 之間的遊戲協作不需要有太大差異。的
遊戲世界的建構和描述仍然可以在遊戲中使用建置指令進行，
使用文字tags和[行內函數](../Components/FuncParser.md)來美化和定製
經驗。 Evennia 提供了建構世界的外部方法，但這些都是可選的。還有
*原則上*沒有什麼可以阻止開發者向玩家提供類似軟程式碼的語言，如果
這被認為是必要的。

對於遊戲的*開發者*來說，差異更大：程式碼主要是在遊戲之外編寫的
Python 模組而不是遊戲中的指令列。 Python 是一種非常流行且得到良好支援的
具有大量檔案和幫助的語言。 Python 標準函式庫也是一個
對於不必重新發明輪子有很大幫助。但話雖如此，雖然 Python 被認為是
更容易學習和使用的語言無疑與MUSH軟程式碼有很大不同。

雖然軟程式碼允許在遊戲中進行協作，但 Evennia 的外部編碼反而開啟了
使用專業版本控制工具進行協作和使用錯誤追蹤的可能性
諸如 github 之類的網站（或用於免費私人儲存庫的 bitbucket）。原始碼可以用適當的方式編寫
文字編輯器和 IDEs 具有重構、語法突出顯示和所有其他便利功能。簡而言之，
Evennia遊戲的協作開發與最專業的協作方式相同
開發是在世界範圍內完成的，這意味著可以使用所有最好的工具。

(parent-vs-typeclass-and-spawn)=
## `@parent` 與 `@typeclass` 及 `@spawn`

繼承在 Python 中的工作方式與在軟程式碼中的工作方式不同。 Evennia沒有「主人」的概念
其他物件繼承自的物件」。事實上根本沒有理由引入“虛擬”
遊戲世界中的「物件」——程式碼和資料彼此分開。

在Python中（這是一個[物件導向](https://en.wikipedia.org/wiki/Object-oriented_programming)
語言）而是建立*類別* - 這些就像您可以從中生成任何數字的藍圖
*物件例項*。 Evennia 還增加了額外的功能，即每個例項都持久存在於
資料庫（這意味著不需要 SQL）。舉個例子，Evennia 中的唯一字元是
類別 `Character` 的例項。

與 MUSH 的 `@parent` 指令並行的一個指令可能是 Evennia 的 `@typeclass` 指令，它改變了
類別是一個已經存在的物件的例項。這樣你就可以真正轉動`Character`
當場變成`Flowerpot`。

如果您是物件導向設計的新手，請務必注意類別的所有物件例項
*不一定*必須相同。如果他們這樣做，所有角色都會被命名為相同。 Evennia 允許
以多種不同的方式自訂單一物件。一種方法是透過*屬性*，它們是
可以連結到任何物件的資料庫繫結屬性。例如，您可以有 `Orc`
定義獸人應該能夠做的所有事情的類別（可能依次繼承自某些
`Monster` 所有怪物共享的等級）。在不同的例項上設定不同的屬性
（不同的力量、裝備、外表等）將使每個獸人獨一無二，儘管他們共享相同的東西
類。

`@spawn` 指令允許人們方便地在不同的屬性「集」之間進行選擇
穿上每個新的獸人（如“戰士”套裝或“薩滿”套裝）。這樣的集合甚至可以繼承一個
另一個至少又讓人想起`@parent`的*效果*和物件-
基於MUSH的繼承。

當然還有其他差異，但這應該能給人一些感覺。夠了
理論。接下來讓我們開始討論更實際的問題。若要安裝，請參閱
[入門說明](../Setup/Installation.md)。

(a-first-step-making-things-more-familiar)=
## 讓事情變得更熟悉的第一步

我們將在這裡給出兩個自訂 Evennia 的範例，以便 MUSH *玩家* 更加熟悉。

(activating-a-multi-descer)=
### 啟動多重解析器

預設情況下，Evennia 的 `desc` 指令會更新您的描述，僅此而已。還有一個特點——
不過`evennia/contrib/multidesc.py`中有豐富的可選「multi-descer」。這種替代方案允許
管理和組合大量的鍵控描述。

要啟動多重解析器，`cd` 到您的遊戲資料夾並進入 `commands` 子資料夾。那裡
你會找到檔案`default_cmdsets.py`。在 Python 術語中，所有 `*.py` 檔案都稱為*模組*。
在文字編輯器中開啟該模組。我們不會討論遊戲中的Evennia*指令*和*指令集*
這裡進一步，但足以說明 Evennia 允許您更改哪些指令（或
指令）根據情況隨時可供玩家使用。

在模組中新增兩行新行，如下所示：

```python
# the file mygame/commands/default_cmdsets.py
# [...] 

from evennia.contrib import multidescer   # <- added now

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The CharacterCmdSet contains general in-game commands like look,
    get etc available on in-game Character objects. It is merged with
    the AccountCmdSet when an Account puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(multidescer.CmdMultiDesc())      # <- added now 
# [...]
```

請注意，Python 關心縮排，因此請確保縮排的空格數與
如上圖所示！

那麼上面會發生什麼事呢？我們[匯入
模組](https://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch28s03.html)
`evennia/contrib/multidescer.py` 在頂部。匯入後我們就可以存取該模組內的內容
使用句號（`.`）。 multidescer 被定義為類別 `CmdMultiDesc` （我們可以發現
透過在文字編輯器中開啟所述模組）。在底部我們建立這個類別的一個新例項並
將其新增到 `CharacterCmdSet` 類別中。為了本教學的目的，我們只需要知道
`CharacterCmdSet` 包含預設情況下 `Character` 可用的所有指令。

當指令集首次建立時，整個事情將被觸發，這發生在伺服器上
開始。因此我們需要用 `@reload` 重新載入 Evennia - 這樣做不會導致任何人斷開連線。如果
一切順利，您現在應該能夠使用`desc`（或`+desc`）並發現您有更多
可能性：

```text
> help +desc                  # get help on the command
> +desc eyes = His eyes are blue. 
> +desc basic = A big guy.
> +desc/set basic + + eyes    # we add an extra space between
> look me
A big guy. His eyes are blue.
```

如果發生錯誤，伺服器日誌中將顯示 *traceback* - 多行文字顯示
發生錯誤的地方。透過尋找與該錯誤相關的行號來尋找錯誤所在
`default_cmdsets.py` 檔案（這是迄今為止您唯一更改過的檔案）。很有可能是你拼字錯誤
某些東西或錯過了縮排。修復它並再次 `@reload` 或執行 `evennia start` 作為
需要。

(customizing-the-multidescer-syntax)=
### 自訂 multidescer 語法

如上所示，multidescer 使用這樣的語法（其中 `|/` 是 Evennia 的 tags 用於換行）
:

```text
> +desc/set basic + |/|/ + cape + footwear + |/|/ + attitude 
``` 

`+ ` 的使用是由編寫此 `+desc` 指令的*開發人員*規定的。如果
*玩家*不喜歡這種文法嗎？玩家需要糾纏開發者來修改嗎？不
必然。而Evennia則不允許玩家在指令上建立自己的多重解析器
行，它確實允許將指令語法“重新對映”為他們喜歡的語法。這是使用以下方法完成的
`nick` 指令。

這是一個改變上面指令輸入方式的暱稱：

```text
> nick setdesc $1 $2 $3 $4 = +desc/set $1 + |/|/ + $2 + $3 + |/|/ + $4
```

左側的字串將與您的輸入進行匹配，如果匹配，它將被替換為
右邊的字串。 `$`-type tags 將儲存空格分隔的引數並將它們放入
替代品。暱稱允許[shell-like萬用字元](http://www.linfo.org/wildcard.html)，所以你
可以使用 `*`、`?`、`[...]`、`[!...]` 等來配對部分輸入。

現在可以將與以前相同的描述設定為

```text
> setdesc basic cape footwear attitude 
```

透過 `nick` 功能，即使沒有
開發人員更改底層 Python 程式碼。

(next-steps)=
## 後續步驟

如果您是*開發人員*並且有興趣製作更像 MUSH 的 Evennia 遊戲，那麼一個好的開始是
檢視Evennia [第一個類似MUSH 的遊戲的教學](./Tutorial-for-basic-MUSH-like-game.md)。
這將逐步從頭開始建立一個簡單的小遊戲，並幫助您熟悉
Evennia的各個角落。還有[執行角色扮演sessions教學](Evennia-
for-roleplaying-sessions)你可能會感興趣。

讓*玩家*更加熟悉的一個重要方面是新增新內容並調整現有內容
指令。 [新增指令教學](Adding-Command-
Tutorial) 介紹如何完成此操作。您可能還會發現透過 `evennia/contrib/` 資料夾進行購物很有用。的
[教學世界](Beginner-Tutorial/Part1/Beginner-Tutorial-Tutorial-World.md)是一個你可以嘗試的小型單人任務（不是很MUSH-
喜歡，但它確實顯示了許多 Evennia 概念的實際應用）。除此之外還有[更多教學](./Howtos-Overview.md)
嘗試一下。如果您覺得想要更直觀的概述，您也可以檢視
[圖片中Evennia](https://evennia.blogspot.se/2016/05/evennia-in-pictures.html)。

…當然，如果您需要進一步的幫助，您可以隨時進入 [Evennia
聊天室](https://webchat.freenode.net/?channels=evennia&uio=MT1mYWxzZSY5PXRydWUmMTE9MTk1JjEyPXRydWUbb)
或在我們的[論壇/郵件列表](https://groups.google.com/forum/#%21forum/evennia) 中發布問題！
