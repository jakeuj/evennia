(searching-for-things)=
# 尋找東西

我們已經瞭解如何在 Evennia 中建立各種實體。但是，如果我們事後無法找到並使用它，那麼創造出來的東西就沒有什麼用處。

```{sidebar} Python 程式碼與使用 py 指令
大多數這些工具旨在在您建立遊戲時在 Python 程式碼中使用。我們
給出如何透過 `py` 指令進行測試的範例，但這只是為了進行實驗，通常不是您編寫遊戲的方式。
```

為了測試本教學中的範例，讓我們建立一些可以在目前位置搜尋的物件。

    > create/drop Rose 
    
(searching-using-objectsearch)=
## 使用 Object.search 進行搜尋

`DefaultObject`上是`.search`的方法，我們在製作指令時已經嘗試過了。要使用此功能，您必須已經有一個可用的物件，如果您使用 `py` 您可以自己使用：

    py self.search("rose")
    Rose

- 這將按物件的 `key` 或 `alias` 進行搜尋。字串始終不區分大小寫，因此搜尋 `"rose"`、`"Rose"` 或 `"rOsE"` 會得到相同的結果。
- 預設情況下，它總是在 `obj.location.contents` 和 `obj.contents` 中搜尋物件（即 obj 的庫存中或同一房間中的東西）。
- 它總是返回恰好一場比賽。如果找到零個或多個符合項，則傳回 `None`。這與 `evennia.search`（見下文）不同，後者總是會傳回一個清單。
- 如果出現不匹配或多重匹配，`.search` 將自動向 `obj` 傳送錯誤訊息。因此，如果結果是`None`，您不必擔心報告訊息。

換句話說，此方法為您處理錯誤訊息。一種非常常見的使用方式是在指令中。您可以將指令放在任何地方，但讓我們嘗試預先填寫的 `mygame/commands/command.py`。

```python
# in for example mygame/commands/command.py

from evennia import Command as BaseCommand

class Command(BaseCommand): 
    # ... 

class CmdQuickFind(Command):
    """ 
    Find an item in your current location.

    Usage: 
        quickfind <query>
        
	"""

    key = "quickfind"

    def func(self):
        query = self.args
        result = self.caller.search(query)
        if not result:
            return
        self.caller.msg(f"Found match for {query}: {result}")
```

如果您想測試此指令，請將其新增到預設的cmdset（有關更多詳細資訊，請參閱[指令教學](./Beginner-Tutorial-Adding-Commands.md)），然後使用`reload`重新載入伺服器：

```python
# in mygame/commands/default_cmdsets.py

# ...

from commands.command import CmdQuickFind    # <-------

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ... 
    def at_cmdset_creation(self): 
        # ... 
        self.add(CmdQuickFind())   # <------

```


請記住，`self.caller` 是呼叫該指令的人。這通常是一個角色，
繼承自 `DefaultObject`。所以它有 `.search()` 可用。

這個簡單的小指令取得其引數並蒐索匹配項。如果找不到，`result` 將是 `None`。該錯誤已報告給 `self.caller`，因此我們僅使用 `return` 中止。

使用 `global_search` 標誌，您可以使用 `.search` 來尋找任何內容，而不僅僅是同一房間中的東西：

```python
volcano = self.caller.search("Vesuvio", global_search=True)
```

您可以將配對限制為特定的typeclasses：

```python
water_glass = self.caller.search("glass", typeclass="typeclasses.objects.WaterGlass")
```

如果您只想搜尋特定的內容列表，您也可以這樣做：

```python
stone = self.caller.search("MyStone", candidates=[obj1, obj2, obj3, obj4])
```

只有當“MyStone”位於房間（或您的庫存中）並且_是提供的四個候選物件之一時，這才會返回匹配項。這非常強大，以下是您如何僅在庫存中找到某些東西的方法：

```python
potion = self.caller.search("Healing potion", candidates=self.caller.contents)
```

您也可以關閉自動錯誤處理：

```python
swords = self.caller.search("Sword", quiet=True)  # returns a list!
```

使用`quiet=True`，使用者將不會收到零個或多匹配錯誤的通知。相反，您應該自己處理這個問題。此外，現在傳回的是零個、一個或多個符合專案的清單！
    
(main-search-functions)=
## 主要搜尋功能

Evennia的基本搜尋工具是`evennia.search_*`功能，例如`evennia.search_object`。這些通常在您的程式碼中使用，但您也可以使用 `py` 在遊戲中嘗試它們：

     > py evennia.search_object("rose")
     <Queryset [Rose]>

```{sidebar} 查詢集

主搜尋函式傳回的實際上是`queryset`。它們可以像列表一樣對待，只是它們不能就地修改。我們將在[下一課]中討論查詢集(./Beginner-Tutorial-Django-queries.md)

```
這將根據 `key` 或 `alias` 搜尋物件。  我們在上一節中討論的 `.search` 方法實際上包裝了 `evennia.search_object` 並以各種方式處理其輸出。這是 Python 程式碼中的相同範例，例如作為指令或編碼系統的一部分：

```python
import evennia 

roses = evennia.search_object("rose")
accts = evennia.search_account("YourName")
```

在上面我們先找到玫瑰，然後找到一個帳戶。您可以使用 `py` 嘗試兩者：

    > py evennia.search_object("rose")[0]
    Rose
    > py evennia.search_account("YourName")[0]
    <Player: YourName>

`search_object/account` 傳回所有符合專案。我們使用 `[0]` 僅取得查詢集的第一個符合項，在本例中分別為我們提供了玫瑰和您的帳戶。請注意，如果找不到任何匹配項，像這樣使用 `[0]` 會導致錯誤，因此它對於偵錯最有用。

在其他情況下，零個或多個匹配項表示存在問題，您需要自行處理這種情況。對於僅使用 `py` 進行測試來說這太詳細了，但是如果您想建立自己的搜尋方法，那麼瞭解一下是很不錯的：

```python
    the_one_ring = evennia.search_object("The one Ring")
    if not the_one_ring:
        # handle not finding the ring at all
    elif len(the_one_ring) > 1:
        # handle finding more than one ring
    else:
        # ok - exactly one ring found
        the_one_ring = the_one_ring[0]
```

所有主要資源都有等效的搜尋功能。您可以在[API首頁的搜尋功能部分](../../../Evennia-API.md)找到它們的清單。

(understanding-object-relationships)=
## 理解物件關係

搜尋時瞭解物件之間的相互關係非常重要。

讓我們考慮一個 `chest` ，裡面有一個 `coin` 。箱子位於`dungeon`的房間。地牢裡還有一個`door`（通往外面的出口）。

```
┌───────────────────────┐
│dungeon                │
│    ┌─────────┐        │
│    │chest    │ ┌────┐ │
│    │  ┌────┐ │ │door│ │
│    │  │coin│ │ └────┘ │
│    │  └────┘ │        │
│    │         │        │
│    └─────────┘        │
│                       │
└───────────────────────┘
```

如果您有權存取任何遊戲內物件，則可以透過使用其 `.location` 和 `.contents` 屬性來尋找相關物件。

- `coin.location` 是 `chest`。
- `chest.location` 是 `dungeon`。
- `door.location` 是 `dungeon`。
- `room.location` 是 `None` 因為它不在其他東西裡面。

人們可以用它來找出裡面有什麼。例如，`coin.location.location` 就是 `dungeon`。

- `room.contents` 是 `[chest, door]`
- `chest.contents` 是 `[coin]`
- `coin.contents` 是 `[]`，空列表，因為硬幣「內部」沒有任何內容。
- `door.contents` 也是`[]`。

一個方便的助手是 `.contents_get` - 這允許限制返回的內容：

- `room.contents_get(exclude=chest)` - 這將返回房間中除箱子之外的所有東西（也許它是隱藏的？）

有一個特殊的屬性用來尋找出口：

- `room.exits` 是 `[door]`
- `coin.exits` 是 `[]`，因為它沒有出口（所有其他物件相同）

有一個屬性 `.destination` 僅由出口使用：

- `door.destination`是`outside`（或門通往的任何地方）
- `room.destination` 是 `None`（對於所有其他非退出物件相同）

(what-can-be-searched-for)=
## 可以搜尋什麼

這些是人們可以搜尋的主要資料庫實體：

- [物件](../../../Components/Objects.md)
- [帳戶](../../../Components/Accounts.md)
- [Scripts](../../../Components/Scripts.md),
- [頻道](../../../Components/Channels.md)
- [訊息](../../../Components/Msg.md)（預設由 `page` 指令使用）
- [幫助條目](../../../Components/Help-System.md)（手動建立的幫助條目）

大多數時候，您可能會花時間搜尋物件和偶爾的帳戶。

大多數搜尋方法可直接從 `evennia` 取得。但也可以透過 `evennia.search` 找到很多有用的搜尋助手。

那麼要找到一個實體，可以搜尋什麼？

(search-by-key)=
### 按鍵搜尋

`key` 是實體的名稱。搜尋此內容始終不區分大小寫。

(search-by-aliases)=
### 按別名搜尋

物件和帳戶可以有任意數量的別名。當搜尋 `key` 時，這些也會被搜尋，您不能輕鬆地只搜尋別名。讓我們使用預設的`alias`指令為rose新增一個別名：

    > alias rose = flower

或者，您可以手動實現相同的操作（這是 `alias` 指令自動為您執行的操作）：

    > py self.search("rose").aliases.add("flower")

如果上面的範例 `rose` 有 `key` `"Rose"`，現在也可以透過搜尋其別名 `flower` 找到它。

    > py self.search("flower")
    Rose 

> 所有預設指令都使用相同的搜尋功能，因此您現在也可以執行 `look flower` 來檢視玫瑰。

(search-by-location)=
### 按地點搜尋

只有物件（從 `evennia.DefaultObject` 繼承的事物）具有 `.location` 屬性。

`Object.search` 方法將自動根據物件的位置限制其搜尋，因此假設您與玫瑰在同一個房間中，這將起作用：

    > py self.search("rose")
    Rose

讓我們建立另一個位置並移動到它 - 你將不再找到玫瑰：

    > tunnel n = kitchen
    north 
    > py self.search("rose")
    Could not find "rose"

但是，使用 `search_object` 將會找到玫瑰，無論它位於何處：

     > py evennia.search_object("rose") 
     <QuerySet [Rose]> 

`evennia.search_object` 方法沒有 `location` 引數。相反，您所做的是將其 `candidates` 關鍵字設為當前位置的 `.contents` 來限制搜尋。這與位置搜尋相同，因為它只接受房間內的匹配項。在這個例子中，我們將（正確地）發現玫瑰不在房間裡。

    > py evennia.search_object("rose", candidate=here.contents)
    <QuerySet []>

一般來說，`Object.search` 是在同一位置進行非常常見的搜尋的快捷方式，而 `search_object` 可以在任何地方找到物件。

(search-by-tags)=
### 按Tags搜尋

將 [Tag](../../../Components/Tags.md) 視為機場在飛行時貼在您行李上的標籤。乘坐同一架飛機的每個人都會得到 tag，將它們分組在一起，以便機場可以知道什麼應該去哪架飛機。 Evennia中的實體可以用同樣的方式分組。每個物件可以附加任意數量的 tags。

返回 `rose` 的位置，讓我們再建立一些植物：

    > create/drop Daffodil
    > create/drop Tulip
    > create/drop Cactus

然後讓我們新增“有刺”和“花朵”tags 作為根據它們是否是花朵和/或有刺進行分組的方法：

    py self.search("rose").tags.add("flowers")
	py self.search("rose").tags.add("thorny")
    py self.search("daffodil").tags.add("flowers")
    py self.search("tulip").tags.add("flowers")
    py self.search("cactus").tags.add("flowers")
    py self.search("cactus").tags.add("thorny")	

現在您可以使用 `search_tag` 函式來尋找所有花：

    py evennia.search_tag("flowers")
    <QuerySet [Rose, Daffodil, Tulip, Cactus]>
    py evennia.search_tag("thorny")
    <QuerySet [Rose, Cactus]>

Tags也可以有類別。預設情況下，此類別是 `None` ，它被視為自己的類別。  以下是在純 Python 程式碼中使用類別的一些範例（如果您想先建立物件，也可以使用 `py` 進行嘗試）：

    silmarillion.tags.add("fantasy", category="books")
    ice_and_fire.tags.add("fantasy", category="books")
    mona_lisa_overdrive.tags.add("cyberpunk", category="books")

請注意，如果您指定 tag 為類別，則在搜尋時_必須_還包括其類別，否則將搜尋 `None` 的 tag-類別。

    all_fantasy_books = evennia.search_tag("fantasy")  # no matches!
    all_fantasy_books = evennia.search_tag("fantasy", category="books")

只有上面的第二行返回兩本幻想書。

    all_books = evennia.search_tag(category="books")

這得到了所有三本書。

(search-by-attribute)=
### 按Attribute搜尋

我們也可以透過與實體關聯的[屬性](../../../Components/Attributes.md)來搜尋。

例如，假設我們的植物有一個“生長狀態”，隨著它的生長而更新：

    > py self.search("rose").db.growth_state = "blooming"
    > py self.search("daffodil").db.growth_state = "withering"

現在我們可以找到具有給定生長狀態的事物：

    > py evennia.search_object("withering", attribute_name="growth_state")
    <QuerySet [Rose]> 

> 以 Attribute 搜尋非常實用。但如果您想要經常對實體進行分組或搜尋，則使用 Tags 並按 Tags 進行搜尋會更快且更節省資源。

(search-by-typeclass)=
### 按Typeclass搜尋

有時，限制搜尋的 Typeclass 很有用。

假設您在 `mygame/typeclasses.flowers.py` 下定義了兩種型別的花，`CursedFlower` 和 `BlessedFlower`。每個類別都包含分別授予詛咒和祝福的自訂程式碼。你可能有兩個`rose`的物體，而玩家不知道哪一個是壞的還是好的。要在搜尋中將它們分開，您可以確保獲得正確的搜尋結果（在 Python 程式碼中）

```python
cursed_roses = evennia.search_object("rose", typeclass="typeclasses.flowers.CursedFlower")
```

如果你e.g。已經匯入了 `BlessedRose` 類，你也可以直接傳遞它：

```python
from typeclasses.flowers import BlessedFlower
blessed_roses = evennia.search_object("rose", typeclass=BlessedFlower)
```

一個常見的用例是尋找給定 typeclass 的_所有_ 項，無論它們的名稱是什麼。為此，您不使用 `search_object`，而是直接使用 typeclass 進行搜尋：

```python
from typeclasses.objects.flowers import Rose
all_roses = Rose.objects.all()
```

最後一種搜尋方式是 Django _query_ 的簡單形式。這是一種使用 Python 表達 SQL 查詢的方法。請參閱[下一課](./Beginner-Tutorial-Django-queries.md)，我們將在其中更詳細地探討這種搜尋方式。

(search-by-dbref)=
### 按資料庫引用搜尋

```{sidebar} 我會用完 dbrefs 嗎？

由於 dbref 不被重複使用，您是否需要擔心您的資料庫 ID 將來「用完」？ [不，原因如下](../../../Components/Typeclasses.md#will-i-run-out-of-dbrefs)。
```
資料庫 ID 或 `#dbref` 是唯一的，並且在每個資料庫表中不會重複使用。在搜尋方法中，您可以將 `key` 的搜尋替換為要搜尋的 dbref。這必須寫成字串`#dbref`：

    the_answer = self.caller.search("#42")
    eightball = evennia.search_object("#8")

由於 `#dbref` 始終是唯一的，因此此搜尋始終是全域的。

```{warning} 依賴#dbrefs

在遺留程式碼庫中，您可能習慣於大量依賴#dbrefs來尋找和追蹤事物。如果偶爾使用的話，透過 #dbref 查詢內容可能很實用。然而，「依賴」Evennia 中的硬編碼 #dbrefs 被認為是「不好的做法」。特別是期望終端使用者瞭解它們。它使您的程式碼脆弱且難以維護，同時將您的程式碼與資料庫的確切佈局連結在一起。在 99% 的用例中，您應該組織程式碼，以便傳遞實際物件並按鍵/tags/attribute 進行搜尋。
```


(summary)=
## 概括

瞭解如何找到內容很重要，本節中的工具將為您提供很好的幫助。這些工具將滿足您大部分的日常需求。

但並不總是如此。如果我們回到之前箱子裡有硬幣的例子，你_可以_使用以下程式碼動態地找出房間裡是否有裝有硬幣的箱子：

```python 
from evennia import search_object

# we assume only one match of each 
dungeons = search_object("dungeon", typeclass="typeclasses.rooms.Room")
chests = search_object("chest", location=dungeons[0])
# find out how much coin are in the chest 
coins = search_object("coin", candidates=chests[0].contents)
```

這可行，但效率很低、脆弱且需要輸入大量內容。這種事情最好透過*直接查詢資料庫*來完成。我們將在下一課中討論這一點。在那裡，我們將使用 Django 資料庫查詢和查詢集深入研究更複雜的搜尋。