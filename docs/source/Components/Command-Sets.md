(command-sets)=
# 指令集


指令集與[指令](./Commands.md)密切相關，您應該熟悉
閱讀本頁之前的指令。為了方便閱讀，兩頁被分開。

*指令集*（通常稱為 CmdSet 或 cmdset）是儲存一個或多個指令的基本單位
*指令*。給定的指令可以進入任意數量的不同指令集。儲存指令
指令集中的類別是使指令可在遊戲中使用的方法。

當在物件上儲存 CmdSet 時，您將使該指令集中的指令可供
物件。一個例子是儲存在新角色上的預設指令集。該指令集包含
所有有用的指令，從`look`和`inventory`到`@dig`和`@reload`
([許可權](./Permissions.md) 然後限制哪些玩家可以使用它們，但這是一個單獨的
主題）。

當帳戶輸入指令時，cmdsets 來自帳戶、角色、其位置和其他地方
被拉到一個*合併堆疊*中。該堆疊按特定順序合併在一起
建立一個“合併”cmdset，代表當時可用的指令池。

一個例子是一個 `Window` 物件，它有一個 cmdset，其中有兩個指令：`look through
視窗` and `開啟視窗`。有窗戶的房間裡的玩家可以看到指令集，
允許他們只在那裡使用這些指令。你可以想像它的各種巧妙用途，
就像一個 `Television` 物件，它有多個指令用於檢視它、切換通道等等
上。 Evennia 包含的教學世界展示了一個暗室，它取代了某些關鍵的房間
指令有自己的版本，因為角色看不到。

如果您想快速開始定義第一個指令並將它們與指令集一起使用，您可以
可以轉到[新增指令教學](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)，它會逐步完成所有操作
沒有解釋。

(defining-command-sets)=
## 定義指令集

與 Evennia 中的大多數內容一樣，CmdSet 被定義為從正確的父類繼承的 Python 類
（`evennia.CmdSet`，這是 `evennia.commands.cmdset.CmdSet` 的捷徑）。僅限 CmdSet 類
需要定義一種方法，稱為`at_cmdset_creation()`。所有其他類別引數都是可選的，
但用於更進階的集合運算和編碼（請參閱[合併規則](Command-
Sets#merge-rules)部分）。

```python
# file mygame/commands/mycmdset.py

from evennia import CmdSet

# this is a theoretical custom module with commands we
# created previously: mygame/commands/mycommands.py
from commands import mycommands

class MyCmdSet(CmdSet):
    def at_cmdset_creation(self):
        """
        The only thing this method should need
        to do is to add commands to the set.
        """
        self.add(mycommands.MyCommand1())
        self.add(mycommands.MyCommand2())
        self.add(mycommands.MyCommand3())
```

CmdSet 的 `add()` 方法還可以採用另一個 CmdSet 作為輸入。在這種情況下所有指令
從那 CmdSet 將被附加到這一個，就像你逐行新增它們一樣：

```python
    def at_cmdset_creation():
        ...
        self.add(AdditionalCmdSet) # adds all command from this set
        ...
```

如果您將指令新增至現有的 cmdset（如預設的 cmdset），則該集已經是
載入到記憶體中。您需要讓伺服器知道程式碼變更：

```
@reload
```

您現在應該能夠使用該指令。

如果您建立了一個新的cmdset，則必須將其新增至物件才能執行指令
可用範圍內。臨時測試自己的 cmdset 的簡單方法是使用 `@py` 指令
執行一個Python片段：

```python
@py self.cmdset.add('commands.mycmdset.MyCmdSet')
```

這將伴隨您，直到您 `@reset` 或 `@shutdown` 伺服器，或者您執行

```python
@py self.cmdset.delete('commands.mycmdset.MyCmdSet')
```

在上面的範例中，刪除了特定的 Cmdset 類別。不帶引數呼叫 `delete` 將
刪除最新新增的cmdset。

> 注意：預設情況下，使用 `cmdset.add` 新增的指令集*不會*持久保留在資料庫中。

如果您希望 cmdset 在重新載入後仍然存在，您可以執行以下操作：

```
@py self.cmdset.add(commands.mycmdset.MyCmdSet, persistent=True)
```

或者您可以新增 cmdset 作為*預設*cmdset：

```
@py self.cmdset.add_default(commands.mycmdset.MyCmdSet)
```

一個物件只能有一個「預設」cmdset（但也可以沒有）。這意味著安全墜落-
即使所有其他 cmdsets 失敗或被刪除，也會返回。始終堅持，不會受到影響
`cmdset.delete()`。要刪除預設的 cmdset，您必須明確呼叫 `cmdset.remove_default()`。

指令集通常透過 `at_object_creation` 方法新增到物件中。有關更多範例
新增指令，請閱讀[逐步教學](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)。一般情況下你可以
使用 `self.cmdset.add()` 或自訂將哪些指令集新增至您的物件
`self.cmdset.add_default()`。

> 重要提示：指令由鍵*或*別名唯一標識（請參閱[指令](./Commands.md)）。如果有的話
存在重疊，兩個指令被認為是相同的。將指令加入到指令集中
已經有一個相同的指令將*替換*之前的指令。這非常重要。你
嘗試使用以下指令過載任何預設 Evennia 指令時必須考慮此行為
你自己的。否則，您在新增指令時可能會不小心在指令集中「隱藏」自己的指令
具有匹配別名的新名稱。

(properties-on-command-sets)=
### 指令集的屬性

您可以在 CmdSets 上設定幾個額外的標誌，以修改它們的工作方式。全部都是
可選，否則將設定為預設值。  由於其中許多與*合併*cmdsets有關，
您可能需要閱讀[新增和合併指令集](./Command-Sets.md#adding-and-merging-
command-sets) 部分，以瞭解其中的一些內容。

- `key`（字串）- cmdset 的識別碼。這是可選的，但應該是唯一的。它被用來
用於在清單中顯示，也可以使用 `key_mergetype` 識別特殊合併行為
字典如下。
- `mergetype`（字串）- 允許使用下列字串值之一：「*Union*」、「*Intersect*」、
“*替換*”或“*刪除*”。
- `priority` (int) - 這定義了合併堆疊的合併順序 - cmdsets 將按升序合併
優先順序最高的集合最後合併。在合併期間，來自的指令
具有較高優先順序的設定將具有優先權（發生的情況取決於 [merge
型別](./Command-Sets.md#adding-and-merging-command-sets))。如果優先權相同，則順序
合併堆疊決定偏好。優先值必須大於或等於`-100`。大多數在-
遊戲集的優先順序通常應在 `0` 和 `100` 之間。 Evennia預設集有優先權
如下（如果您想要不同的分佈，可以更改這些）：
    - EmptySet：`-101`（應低於所有其他集合）
    - SessionCmdSet: `-20`
    - AccountCmdSet: `-10`
    - CharacterCmdSet: `0`
    - ExitCmdSet：` 101`（通常應該始終可用）
    - ChannelCmdSet：`101`（通常應該始終可用）-因為退出從不接受
引數，即使指令與頻道名稱相同，出口之間也不會發生衝突
「碰撞」。
- `key_mergetype` (dict) - `key:mergetype` 對的字典。這允許 cmdset 合併
與某些命名的 cmdsets 不同。如果要合併的 cmdset 有 `key` 與中的條目匹配
`key_mergetype`，不會依照`mergetype`中的設定合併，而是依照
這個字典中的模式。請注意，由於 [merge
指令集的順序](./Command-Sets.md#adding-and-merging-command-sets)。  請檢視該部分
在使用`key_mergetype`之前。
- `duplicates` (bool/None default `None`) - 這決定了合併相同優先順序時會發生什麼
cmdsets 包含相同鍵的指令。 `dupicate` 選項*僅*合併時適用
將具有此選項的 cmdset 轉移到具有相同優先順序的其他 cmdset 上。結果 cmdset 將
*不*保留此 `duplicate` 設定。
    - `None`（預設）：不允許重複，cmdset 被合併到舊的“上”
將優先。結果將是獨特的指令。 *但是*，系統會假設這一點
物件上 cmdsets 的值為 `True`，以避免危險的衝突。這通常是安全的選擇。
    - `False`：與 `None` 類似，但係統不會自動採用定義於 cmdsets 的任何值
物件。
    - `True`：同名、同優先權的指令將合併到同一個cmdset中。  這將導致
多重匹配錯誤（使用者將獲得一個可能性列表，以便指定他們使用哪個指令
的意思）。這很有用e.g。對於物件上的cmdsets（例如：有一個`red button`和一個“綠色”
按鈕` in the room. Both have a `按下按鈕`指令，與cmdsets具有相同的優先權。這個
標誌確保僅寫入 `press button` 將強制玩家定義哪個物件
指令的目的）。
- `no_objs` 這是 cmdhandler 的一個標誌，用於建立每次可用的指令集
片刻。它告訴處理程式不要包含來自帳戶周圍物件的cmdsets（也不包含來自房間的cmdsets）
或庫存）建構合併集時。退出指令仍將包含在內。該選項可以
有三個值：
    - `None`（預設）：傳遞合併堆疊中先前明確設定的任何值。如果從來沒有
明確設定，這相當於 `False`。
    - `True`/`False`：明確開啟/關閉。如果合併兩個具有明確 `no_objs` 的集合，
優先順序決定使用什麼。
- `no_exits` - 這是 cmdhandler 的一個標誌，用於建立每次可用的指令集
片刻。它告訴處理程式不要在退出時包含 cmdsets。此標誌可以有三個值：
    - `None`（預設）：傳遞合併堆疊中先前明確設定的任何值。如果
從未明確設定，這充當 `False`。
    - `True`/`False`：明確開啟/關閉。如果合併兩個具有明確 `no_exits` 的集合，
優先順序決定使用什麼。
- `no_channels` (bool) - 這是建立可用指令集的 cmdhandler 的標誌
每時每刻。它告訴處理程式不要包含來自可用遊戲內頻道的cmdsets。這個
flag 可以有三個值：
    - `None`（預設）：傳遞合併堆疊中先前明確設定的任何值。如果
從未明確設定，這充當 `False`。
    - `True`/`False`：明確開啟/關閉。如果合併兩個具有明確 `no_channels` 的集合，
優先順序決定使用什麼。

(command-sets-searched)=
## 搜尋的指令集

當使用者發出指令時，它會與玩家目前可用的[合併](./Command-Sets.md#adding-and-merging-
command-sets)指令集進行比對。這些可能隨時改變
時間（例如玩家帶著前面描述的 `Window` 物件走進房間時）。

目前有效的指令集是從以下來源收集的：

- cmdsets 儲存在目前活動的 [Session](./Sessions.md) 上。預設為空
`SessionCmdSet`，合併優先順序為`-20`。
- [帳戶](./Accounts.md) 上定義的 cmdsets。預設為AccountCmdSet，合併優先順序
`-10`.
- 角色/物件上的所有cmdsets（假設該帳戶目前正在操縱這樣一個
角色/物件）。合併優先順序`0`。
- 木偶角色攜帶的所有物體的cmdsets（檢查`call` lock）。不會
如果 `no_objs` 選項在合併堆疊中處於活動狀態，則包含在內。
- 角色目前位置的cmdsets（檢查`call` lock）。不會被包括在內，如果
`no_objs` 選項在合併堆疊中處於活動狀態。
- 目前位置中的 cmdsets 物件（檢查 `call` lock）。不會被包括在內，如果
`no_objs` 選項在合併堆疊中處於活動狀態。
- 該位置的 cmdsets 個出口。合併優先順序`+101`。如果 `no_exits` 將不包括在內
*或* `no_objs` 選項在合併堆疊中處於活動狀態。
- [頻道](./Channels.md) cmdset 包含將帳戶釋出到所有頻道的指令
或當前連線的角色。合併優先順序`+101`。如果 `no_channels` 將不包括在內
選項在合併堆疊中處於活動狀態。

請注意，物件「沒有」與周圍環境共享其指令。一個角色的
例如，cmdsets 不應共享，否則所有其他角色都會出現多重匹配錯誤
透過在同一個房間裡。物件共享其 cmdsets 的能力由其 `call` 管理
[lock](./Locks.md)。例如，[字元物件](./Objects.md) 預設為 `call:false()`，以便任何
它們上的 cmdsets 只能被它們自己訪問，不能被它們周圍的其他物件訪問。另一個
範例可能是 lock 具有 `call:inside()` 的物件，僅使其指令可用於
它們內部的物件，或 `cmd:holds()` 以使它們的指令僅在它們被持有時才可用。

(adding-and-merging-command-sets)=
## 新增和合併指令集

*注意：這是一個高階主題。瞭解它非常有用，但如果出現以下情況，您可能想跳過它：
這是您第一次學習指令。 *

CmdSets 具有特殊能力，可以將它們「合併」到新的集合中。哪一個
最終出現在合併集中的傳入指令由*合併規則*和相對的定義
兩組的*優先順序*。  刪除最新新增的集將使事情恢復到原來的樣子
是在新增之前。

CmdSets 非破壞性地儲存在物件的 cmdset 處理程式內的堆疊中。這個堆疊
被解析以建立目前處於活動狀態的「組合」cmdset。 CmdSets也來自其他來源
包含在合併中，例如同一房間中的物體（例如要按下的按鈕）或那些
由狀態變化引入（例如進入選單時）。 cmdsets 都是在之後訂購的
優先順序，然後以*相反的順序*合併在一起。即優先順序高的會被合併
「到」較低優先順序的。透過定義 cmdset ，其合併優先順序介於其他兩個集合之間，
您將確保它將合併在它們之間。
此堆疊中的第一個 cmdset 稱為*預設 cmdset*，並且受到保護，不會受到意外影響
刪除。執行 `obj.cmdset.delete()` 永遠不會刪除預設集。相反，應該新增
在預設值之上新增新的 cmdsets 以「隱藏」它，如下所述。  使用特殊的
`obj.cmdset.delete_default()` 僅當您真正知道自己在做什麼時。

CmdSet合併是一項進階功能，可用於實現強大的遊戲效果。想像一下
例如，玩家進入黑暗的房間。您不希望玩家能夠找到其中的所有內容
房間一目瞭然 - 也許您甚至希望他們很難在揹包裡找到東西！
然後，您可以使用覆蓋正常指令的指令定義不同的 CmdSet。雖然他們是
在黑暗的房間裡，也許 `look` 和 `inv` 指令現在只是告訴玩家他們看不到
任何東西！另一個例子是僅當玩家處於戰鬥狀態時才提供特殊的戰鬥指令
戰鬥。或是在船上的時候。或在獲得超級能量時。這一切都可以在
透過合併指令集進行飛行。

(merge-rules)=
### 合併規則

基本規則是指令集以*相反的優先順序*合併。也就是說，較低優先順序的集合是
合併的第一個和更高的prio集合被合併在它們的“頂部”。把它想像成一個分層蛋糕
最高優先權在上面。

為了進一步理解集合如何合併，我們需要定義一些例子。讓我們呼叫第一個指令
設定 **A** 和第二個 **B**。我們假設 **B** 是我們物件上已經啟動的指令集，並且
我們將 **A** 合併到 **B** 上。用程式碼術語來說，這將由 `object.cdmset.add(A)` 完成。
請記住，B 之前已經在 `object` 上處於活動狀態。

我們讓 **A** 集具有比 **B** 更高的優先權。優先順序只是一個整數。作為
從上面的列表中可以看出，Evennia 的預設cmdsets 的優先範圍在`-101` 到`120` 之間。你
對於大多數遊戲效果，通常可以安全地使用 `0` 或 `1` 優先順序。

在我們的範例中，這兩個集合都包含許多指令，我們將透過數字來標識這些指令，例如“A1”
A2` for set **A** and `B1、B2、B3、B4` 代表 **B**。因此對於該範例，兩組都包含指令
使用相同的鍵（或別名）“1”和“2”（例如，這可能是真實中的“look”和“get”
遊戲），而指令 3 和 4 是 **B** 獨有的。為了描述這些集合之間的合併，我們
會寫 `A1,A2 + B1,B2,B3,B4 =?` 其中 `?` 是依賴哪個合併的指令列表
型別 **A** 具有，以及兩個集合具有哪些相對優先權。按照慣例，我們讀到這個
語句為「新指令集**A**合併到舊指令集**B**以形成**？**」。

以下是可用的合併型別及其工作原理。名字部分借用自[Set
理論](https://en.wikipedia.org/wiki/Set_theory)。

- **聯合**（預設）- 兩個 cmdsets 被合併，以便每個中的指令數量盡可能多
cmdset 最終出現在合併的 cmdset 中。相同鍵的指令按優先權合併。

         # Union
         A1,A2 + B1,B2,B3,B4 = A1,A2,B3,B4

- **相交** - 僅在*兩個* cmdsets（i.e。具有相同鍵）中找到的指令最終會出現在
合併的 cmdset，其中優先順序較高的 cmdset 替換優先順序較低的指令。

         # Intersect
         A1,A3,A5 + B1,B2,B4,B5 = A1,A5

- **替換** - 高優先權cmdset的指令完全替換低優先權的指令
cmdset 的指令，不論是否有同鍵指令。

         # Replace
         A1,A3 + B1,B2,B4,B5 = A1,A3

- **刪除** - 高優先指令集從低優先指令集中刪除相同鍵的指令
cmdset。它們不會被任何東西替換，所以這是一種過濾器，可以修剪低優先順序的內容
使用高優先順序作為模板進行設定。

         # Remove
         A1,A3 + B1,B2,B3,B4,B5 = B2,B4,B5

除了 `priority` 和 `mergetype` 之外，指令集還需要一些其他變數來控制
他們合併：

- `duplicates` (bool) - 確定當兩組相同優先合併時會發生什麼。預設為
合併中的新集（上面的i.e。**A**）自動優先。但如果
*duplicates* 為 true，結果將是每個名稱符合多個的合併。  這將
通常會導致玩家在更高的道路上收到多場比賽錯誤，但可能有利於
諸如 cmdsets 之類的東西放在房間中的非玩家對像上，以允許系統警告多個物件
房間中的“球”具有相同的“踢”指令，並提供選擇哪個指令的機會
踢球...允許重複僅對 *Union* 和 *Intersect* 有意義，設定為
對於其他合併型別被忽略。
- `key_mergetypes` (dict) - 允許 cmdset 為特定的 cmdsets 定義唯一的合併型別，
由cmdset `key` 標識。  格式為`{CmdSetkey:mergetype}`。範例：
`{'Myevilcmdset','Replace'}` 這將確保該集始終使用“替換”
cmdset 僅與金鑰 `Myevilcmdset` 無關，無論主 `mergetype` 設定為何。

> 警告：`key_mergetypes` 字典*只能在我們合併到的cmdset 上工作*。使用時
`key_mergetypes` 因此，考慮合併優先順序很重要 - 您必須確保
在您要偵測的 cmdset 和下一個較高的優先權（如果有）之間選擇一個優先順序。也就是說，如果
我們定義了一個具有高優先權的cmdset，並將其設為影響合併中較靠後的cmdset
堆疊，當我們需要合併時，我們不會「看到」該集合。範例：合併堆疊是
`A(prio=-10), B(prio=-5), C(prio=0), D(prio=5)`。我們現在將 cmdset `E(prio=10)` 合併到這個堆疊上，
與`key_mergetype={"B":"Replace"}`。但優先順序決定了我們不會被合併到B上，我們
將被合併到 E（這是此時較低優先權集的合併）。既然我們正在合併
到 E 而不是 B，我們的 `key_mergetype` 指令將不會觸發。為了確保它有效，我們必須
確保我們合併到 B。將 E 的優先權設為 -4 將確保將其合併到 B 並影響
適當地。

更高階的cmdset範例：

```python
from commands import mycommands

class MyCmdSet(CmdSet):

    key = "MyCmdSet"
    priority = 4
    mergetype = "Replace"
    key_mergetypes = {'MyOtherCmdSet':'Union'}

    def at_cmdset_creation(self):
        """
        The only thing this method should need
        to do is to add commands to the set.
        """
        self.add(mycommands.MyCommand1())
        self.add(mycommands.MyCommand2())
        self.add(mycommands.MyCommand3())
```

(assorted-notes)=
### 什錦筆記

請務必記住，兩個指令都是透過其 `key` 屬性進行比較的
*和*透過它們的 `aliases` 屬性。如果任一鍵或其別名之一匹配，則這兩個指令
被認為是*相同*。所以考慮這兩個指令：

 - 帶有鍵“kick”和別名“fight”的指令
 - 帶有鍵“punch”的指令也帶有別名“fight”

在 cmdset 合併期間（這種情況一直在發生，因為通道指令和
退出合併），這兩個指令將被視為*相同*，因為它們共享別名。它
意味著合併後只剩下其中一個。每個也將與所有其他進行比較
具有按鍵和/或別名“kick”、“punch”或“fight”的任意組合的指令。

……所以避免重複的別名，它只會造成混亂。
