(introduction-to-python-classes-and-objects)=
# Python 類別與物件簡介

我們現在已經學習瞭如何從遊戲伺服器內部（和外部）執行一些簡單的 Python 程式碼。
我們還檢視了我們的遊戲目錄的外觀以及位置。現在我們將開始使用它。

(importing-things)=
## 進口東西

在[上一課](./Beginner-Tutorial-Python-basic-introduction.md#importing-code-from-other-modules)中，我們已經學習如何將資源匯入到我們的程式碼中。現在我們將深入探討一下。

沒有人會在一個巨大的檔案中編寫像線上遊戲這樣大的東西。相反，我們將程式碼分解為單獨的檔案（模組）。每個模組專用於不同的目的。它不僅讓事情變得更乾淨、更有條理、更容易理解。

分割程式碼也可以更輕鬆地重複使用 - 您只需匯入所需的資源，並且知道您只會得到您所要求的內容。這使得更容易發現錯誤並瞭解哪些程式碼是好的，哪些程式碼有問題。

> Evennia 本身以相同的方式使用您的程式碼 - 您只需告訴它特定型別的程式碼在哪裡，
並且它將匯入並使用它（通常而不是預設值）。

這是一個熟悉的例子：

    > py import world.test ; world.test.hello_world(me)
    Hello World!

在此範例中，在您的硬碟上，檔案如下所示：

```
mygame/
    world/
        test.py    <- inside this file is a function hello_world

```
如果您遵循了先前的教學課程，`mygame/world/test.py` 檔案應如下所示（如果
不，就這樣）：

```python
def hello_world(who):
    who.msg("Hello World!")
```

```{sidebar} 空格在 Python 中很重要！

- Python 中縮排很重要
- 大寫也是如此
- 使用 4 `spaces` 縮排，而不是製表符
- 空行就可以了
- `#` 之後的行中的任何內容都是 `comment`，被 Python 忽略
```

重申一下，_python_path_ 描述了 Python 資源之間的關係，包括 Python 模組之間和內部（即以.py 結尾的檔案）。  路徑使用 `.` 並且始終跳過 `.py` 檔案結尾。另外，Evennia 已經知道開始在 `mygame/` 內尋找 python 資源，因此永遠不應該包含它。

    import world.test

`import` Python 指令載入 `world.test`，以便您可以使用它。現在您可以“進入”
這個模組可以達到你想要的功能：

    world.test.hello_world(me)

像這樣使用 `import` 意味著您每次需要時都必須指定完整的 `world.test`
達到你的功能。這是一個替代方案：

    from world.test import hello_world

只要你想得到更長的東西，`from... import...` 就非常非常常見
蟒蛇路徑。它直接匯入`hello_world`，所以你可以立即使用它！

     > py from world.test import hello_world ; hello_world(me)
     Hello World!

假設您的 `test.py` 模組有很多有趣的功能。然後你可以匯入它們
都一一：

    from world.test import hello_world, my_func, awesome_func

如果有_很多_函式，您可以只匯入 `test` 並獲取函式
當您需要時從那裡開始（不必每次都給出完整的`world.test`）：

    > from world import test ; test.hello_world(me)
    Hello World!

您也可以_重新命名_您匯入的內容。舉例來說，您匯入的模組已經具有函式 `hello_world`，但我們也想使用 `world/test.py` 中的函式：

    from world.test import hello_world as test_hello_world

`from... import... as...` 形式重新命名匯入。

    > from world.test import hello_world as hw ; hw(me)
    Hello World!

> 避免重新命名，除非是為了避免像上面那樣的名稱衝突 - 您希望使內容盡可能易於閱讀，而重新命名會增加另一層潛在的混亂。

在[Python基本介紹](./Beginner-Tutorial-Python-basic-introduction.md)中我們學習如何開啟遊戲內
多行直譯器。

    > py
    Evennia Interactive Python mode
    Python 3.7.1 (default, Oct 22 2018, 11:21:55)
    [GCC 8.2.0] on Linux
    [py mode - quit() to exit]

現在，您只需匯入一次即可重複使用匯入的函式。

    > from world.test import hello_world
    > hello_world(me)
    Hello World!
    > hello_world(me)
    Hello World!
    > hello_world(me)
    Hello World!
    > quit()
    Closing the Python console.

```{sidebar} py 的替代品
如果您發現在 `py` 指令中輸入多行很笨拙（傳統的 mud 使用者端對於這種事情非常有限），您也可以 `cd` 到您的 `mygame` 資料夾並執行 `evennia shell`。您最終將進入一個 python shell，其中 Evennia 可用。如果你執行`pip install ipython`，你將獲得一個更現代的 python shell 來使用。這在遊戲外有效，但 `print` 將以相同的方式顯示。
```

在模組中編寫程式碼時也是如此 - 在大多數 Python 模組中，您會在頂部看到一堆匯入，然後模組中的所有程式碼都會使用這些資源。

(on-classes-and-objects)=
## 關於類別和物件

現在我們瞭解了匯入，讓我們來看看真正的 Evennia 模組並嘗試理解它。

在您選擇的文字編輯器中開啟`mygame/typeclasses/scripts.py`。

```python
# mygame/typeclasses/script.py
"""
module docstring
"""
from evennia import DefaultScript

class Script(DefaultScript):
    """
    class docstring
    """
    pass
```

```{sidebar} 檔案字串與註釋

檔案字串與註解（由 `#` 建立）不同。 Python 不會忽略檔案字串，而是它所記錄的內容（在本例中為模組和類別）的組成部分。例如，我們讀取檔案字串來幫助文字 [API 檔案](../../../Evennia-API.md)；我們無法透過評論做到這一點。
```
真實的檔案要長得多，但我們可以忽略多行字串（`"""... """`）。這些用作模組的文件字串或_docstrings_（位於頂部）和下面的`class`。

在模組文件字串下方，我們有 _import_。在本例中，我們正在匯入資源
來自核心 `evennia` 庫本身。我們稍後會深入探討這個問題，現在我們只處理這個
作為一個黑盒子。

名為 `Script` 的 `class` _ 繼承_自 `DefaultScript`。正如你所看到的 `Script` 幾乎是空的。所有有用的程式碼實際上都在 `DefaultScript` 中（`Script`_繼承_該程式碼，除非它用自己的同名程式碼_覆蓋_它）。

我們需要繞一點彎路來理解什麼是「類別」、「物件」或「例項」。在有效使用 Evennia 之前，需要了解這些基本知識。
```{sidebar} OOP

類別、物件、例項和繼承是 Python 的基礎。這個概念和其他一些概念通常在術語「物件導向程式設計」(OOP) 下聚集在一起。
```

(classes-and-instances)=
### 類別和例項

“類別”可以被視為物件“型別”的“模板”。該類別描述了該類別中每個人的基本功能。例如，我們可以有一個類別 `Monster`，它具有用於將自身從一個房間移動到另一個房間的資源。

開啟新檔案`mygame/typeclasses/monsters.py`。新增以下簡單類別：

```python

class Monster:

    key = "Monster"

    def move_around(self):
        print(f"{self.key} is moving!")

```

上面我們定義了一個 `Monster` 類，其中包含一個變數 `key`（即名稱）和一個變數
_方法_就可以了。方法類似函式，只不過它位於類別「之上」。它也始終有
至少一個引數（幾乎總是寫成 `self` 雖然原則上你可以使用
另一個名稱），這是對其自身的引用。因此，當我們列印 `self.key` 時，我們指的是類別上的 `key`。

```{sidebar} 條款

- `class` 是描述某物「型別」的程式碼模板
- `object` 是 `class` 的 `instance`。就像使用模具鑄造錫兵一樣，一個類別可以`instantiated`到任意數量的物件例項中。每個例項不需要完全相同（就像每個錫兵可以被塗成不同的顏色一樣）。

```
類只是一個模板。在使用它之前，我們必須建立該類別的_例項_。如果
`Monster`是一個類，那麼例項就是`Fluffy`，一個特定的龍個體。你例項化
透過_呼叫_類，就像呼叫函式一樣：

    fluffy = Monster()

我們在遊戲中試試看（我們使用`py`多線模式，更簡單）

    > py
    > from typeclasses.monsters import Monster
    > fluffy = Monster()
    > fluffy.move_around()
    Monster is moving!

我們建立了一個 `Monster` 的_例項_，並將其儲存在變數 `fluffy` 中。我們然後
在 fluffy 上呼叫 `move_around` 方法來取得列印輸出。

> 請注意我們_沒有_將該方法呼叫為`fluffy.move_around(self)`。雖然在定義方法時 `self` 必須存在，但我們在呼叫方法時絕對不會明確地新增它（Python 會在幕後自動為我們新增正確的 `self`）。

讓我們創造 Fluffy, Cuddly 的兄弟姊妹：

    > cuddly = Monster()
    > cuddly.move_around()
    Monster is moving!

我們現在有兩個怪物，它們會一直徘徊，直到呼叫 `quit()` 退出這個 Python
例項。我們可以讓它們移動任意多次。但無論我們建立多少個怪物，它們都會顯示相同的列印輸出，因為 `key` 始終固定為「怪物」。

讓我們讓這個類別更靈活一些：

```python

class Monster:

    def __init__(self, key):
        self.key = key

    def move_around(self):
        print(f"{self.key} is moving!")

```

`__init__`是Python辨識的特殊方法。如果給定，當您例項化新的 Monster 時，它將處理額外的引數。我們讓它新增一個引數 `key`，並將其儲存在 `self` 上。

現在，為了讓 Evennia 看到此程式碼更改，我們需要重新載入伺服器。您可以這樣做：

    > quit()
    Python Console is closing.
    > reload

或者您可以使用單獨的終端並從遊戲外部重新啟動：
```{sidebar} 重新載入時

使用 python 模式重新載入有點煩人，因為每次重新載入後都需要重做所有事情。請記住，在常規開發過程中，您不會以這種方式工作。遊戲中的 python 模式對於像這樣的快速修復和實驗來說很實用，但實際的程式碼通常是在外部的 python 模組中編寫的。
```

    $ evennia reload   (or restart)

無論哪種方式，您都需要再次進入 `py`：

    > py
    > from typeclasses.monsters import Monster
    fluffy = Monster("Fluffy")
    fluffy.move_around()
    Fluffy is moving!

現在我們將 `"Fluffy"` 作為引數傳遞給類別。這進入 `__init__` 並設定 `self.key`，我們後來用它來列印正確的名稱！

(whats-so-good-about-objects)=
### 物體有什麼好處？

到目前為止，我們所看到的類別所做的只是表現得像我們的第一個 `hello_world` 函式，但更複雜。我們可以只建立一個函式：

```python
     def monster_move_around(key):
        print(f"{key} is moving!")
```

函式和類別例項（物件）之間的差異在於物件保留_state_。一旦你呼叫了這個函式，它就會忘記你上次呼叫它的所有內容。另一方面，物件會記住改變：

    > fluffy.key = "Fluffy, the red dragon"
    > fluffy.move_around()
    Fluffy, the red dragon is moving!

只要 `fluffy` 物件存在，它的 `key` 就會被改變。這使得物件對於表示和記住資料集合非常有用——其中一些資料又可以是其他物件。一些例子：

- 具有所有統計資料的玩家角色
- 具有HP的怪物
- 一個箱子，裡面有許多金幣
- 裡面有其他物品的房間
- 政黨目前的政策立場
- 包含解決挑戰或擲骰子方法的規則
- 用於複雜經濟模擬的多維資料點
- 還有更多！

(classes-can-have-children)=
### 班級可以有孩子

類別可以相互繼承。 「子」類別將從其「父」類別繼承所有內容。但是，如果子級新增了與其父級同名的內容，它將_覆蓋_從其父級獲得的任何內容。

讓我們用另一個類別來擴充套件`mygame/typeclasses/monsters.py`：

```python

class Monster:
    """
    This is a base class for Monster.
    """

    def __init__(self, key):
        self.key = key

    def move_around(self):
        print(f"{self.key} is moving!")


class Dragon(Monster):
    """
    This is a dragon monster.
    """

    def move_around(self):
        print(f"{self.key} flies through the air high above!")

    def firebreath(self):
        """
        Let our dragon breathe fire.
        """
        print(f"{self.key} breathes fire!")

```

為了清晰起見，我們新增了一些檔案字串。新增檔案字串總是一個好主意；您也可以對方法執行此操作，例如新的 `firebreath` 方法。

我們建立了新類別 `Dragon`，但我們也指定 `Monster` 是 `Dragon` 的_parent_，但在括號中新增了父類別。 `class Classname(Parent)` 是執行此操作的方法。

```{sidebar} 多重繼承

可以在類別中新增更多以逗號分隔的父級。我們在本課最後展示了這種「多重繼承」的範例。在您知道自己在做什麼之前，通常應該避免自己設定多重繼承。單親父母就足以滿足您幾乎所有需要的情況。

```

讓我們嘗試一下我們的新課程。首先 `reload` 伺服器，然後：

    > py
    > from typeclasses.monsters import Dragon
    > smaug = Dragon("Smaug")
    > smaug.move_around()
    Smaug flies through the air high above!
    > smaug.firebreath()
    Smaug breathes fire!

因為我們沒有在 `Dragon` 中（重新）實現 `__init__`，所以我們從 `Monster` 中得到了一個。我們確實在`Dragon`中實現了我們自己的`move_around`，所以它_覆蓋_`Monster`中的那個。且`firebreath`僅適用於`Dragon`s。把它放在`Monster`上沒有多大意義，因為不是每個怪物都能噴火。

即使您覆寫了其中的一些資源，也可以強制一個類別使用父級的資源。這是透過 `super()` 的方法完成。如下修改您的 `Dragon` 類：


```python
# ...

class Dragon(Monster):

    def move_around(self):
        super().move_around()
        print("The world trembles.")

    # ...
```

> 保留`Monster` 和`firebreath` 方法。上面的`#...`表示其餘程式碼不變。

`super().move_around()` 行意味著我們正在類別的父類別上呼叫 `move_around()`。所以在這種情況下，我們會先呼叫`Monster.move_around`，然後再做我們自己的事情。

要檢視 `reload` 伺服器，然後：

    > py
    > from typeclasses.monsters import Dragon
    > smaug = Dragon("Smaug")
    > smaug.move_around()
    Smaug is moving!
    The world trembles.

我們可以看到 `Monster.move_around()` 首先被呼叫並列印“Smaug is moving!”，然後是來自 `Dragon` 類的關於顫抖世界的額外資訊。

繼承是一個強大的概念。它允許您組織和重複使用程式碼，同時僅新增您想要更改的特殊內容。 Evennia 經常使用這個。

(a-look-at-multiple-inheritance)=
### 看看多重繼承

在您選擇的文字編輯器中開啟`mygame/typeclasses/objects.py`。

```python
"""
module docstring
"""
from evennia import DefaultObject

class ObjectParent:
    """
    class docstring 
    """

class Object(ObjectParent, DefaultObject):
    """
    class docstring
    """
    pass
```

在此模組中，我們有一個名為 `ObjectParent` 的空 `class`。它不做任何事情，它唯一的程式碼（除了檔案字串）是 `pass` ，這意味著，好吧，透過並且不做任何事情。由於它也不繼承任何東西，因此它只是一個空容器。

名為 `Object`_ 的 `class`_ 繼承_自 `ObjectParent` 和 `DefaultObject`。通常一個類別只有一個父級，但這裡有兩個。我們已經瞭解到，孩子會繼承父母的一切，除非它覆蓋它。當有多個父母時（“多重繼承”），繼承從左到右發生。

因此，如果 `obj` 是 `Object` 的例項，並且我們嘗試存取 `obj.foo`，Python 將首先檢查 `Object` 類別是否具有屬性/方法 `foo`。接下來它將檢查 `ObjectParent` 是否有它。最後，它將簽入`DefaultObject`。如果兩者都沒有，則會出現錯誤。

為什麼 Evennia 像這樣設定一個空的類別父類別？為了回答這個問題，我們來看看另一個模組，`mygame/typeclasses/rooms.py`：

```python
"""
...
"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent

class Room(ObjectParent, DefaultRoom):
    """
	...
    """
    pass
```

在這裡，我們看到 `Room` 繼承自相同的 `ObjectParent`（從 `objects.py` 匯入）以及來自 `evennia` 庫的 `DefaultRoom` 父級。您會發現 `Character` 和 `Exit` 也是如此。這些都是「遊戲內物件」的範例，因此它們很可能有很多共同點。 `ObjectParent` 的字首為您提供了一種（可選）新增程式碼的方法，該程式碼_對於所有遊戲中的實體都應該相同_。只需將該程式碼放入 `ObjectParent` 中，所有物體、角色、房間和出口都會自動擁有它！

我們將在[下一課](./Beginner-Tutorial-Learning-Typeclasses.md)中回到`objects.py`模組。

(summary)=
## 概括

我們已經從類別中建立了第一條龍。我們已經瞭解如何將類別_例項化_為_物件_的一些知識。我們已經看到了一些_繼承_的範例，並且我們測試瞭如何用子類別中的方法_覆寫_父類別中的方法。我們也使用了`super()`，效果很好。

到目前為止，我們幾乎使用了原始的 Python。在接下來的課程中，我們將開始研究 Evennia 提供的額外位子。但首先我們需要了解在哪裡可以找到所有內容。
