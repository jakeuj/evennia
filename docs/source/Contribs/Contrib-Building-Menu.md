(building-menu)=
# 建築選單

Contrib 作者：文森-LG，2018

建築選單是遊戲中的選單，與 `EvMenu` 不同，儘管使用
不同的方法。建築選單經過特別設計，可以編輯
作為建設者的資訊。在指令中建立建置選單允許
建構者可以快速編輯給定的物件，例如房間。如果您遵循
新增 contrib 的步驟，您將有權存取 `edit` 指令
這將編輯任何預設物件，提供更改其鍵和描述。

(install)=
## 安裝

1. 從此 contrib 匯入 `GenericBuildingCmd` 類
`mygame/commands/default_cmdset.py` 檔案：

    ```python
    from evennia.contrib.base_systems.building_menu import GenericBuildingCmd
    ```

2. 下面，在`CharacterCmdSet`中加入指令：

    ```python
    # ... These lines should exist in the file
    class CharacterCmdSet(default_cmds.CharacterCmdSet):
        key = "DefaultCharacter"

        def at_cmdset_creation(self):
            super().at_cmdset_creation()
            # ... add the line below
            self.add(GenericBuildingCmd())
    ```

(basic-usage)=
## 基本用法

`edit` 指令將允許您編輯任何物件。  您將需要
指定物件名稱或 ID 作為引數。  例如：`edit here`
將編輯當前房間。  然而，建置選單可以執行更多操作
除了這個非常簡單的範例之外，請繼續閱讀以瞭解更多詳細資訊。

建築選單可以設定為編輯任何內容。  這是一個例子
編輯房間時可獲得的輸出：

```
 Editing the room: Limbo(#2)

 [T]itle: the limbo room
 [D]escription
    This is the limbo room.  You can easily change this default description,
    either by using the |y@desc/edit|n command, or simply by entering this
    menu (enter |yd|n).
 [E]xits:
     north to A parking(#4)
 [Q]uit this menu
```

從那裡，您可以按 t 開啟標題選擇。  那你可以
只需輸入文字即可更改房間標題，然後返回
主選單輸入@（所有這些都是可自訂的）。  按 q 退出此選單。

首先要做的是建立一個新模組並放置一個類
繼承自其中的`BuildingMenu`。

```python
from evennia.contrib.base_systems.building_menu import BuildingMenu

class RoomBuildingMenu(BuildingMenu):
    # ...

```

接下來，重寫 `init` 方法（而不是 `__init__`！）。  您可以新增
選擇（如標題、描述和退出選項，如上所示）
`add_choice` 方法。

```python
class RoomBuildingMenu(BuildingMenu):
    def init(self, room):
        self.add_choice("title", "t", attr="key")

```

這將建立第一個選擇，即標題選擇。  如果有人開啟你的選單
然後輸入t，她將出現在標題選擇中。  她可以更改標題
（它會寫在房間的`key` attribute）然後返回
主選單使用`@`。

`add_choice` 有很多論點並提供了大量的
靈活性。  最有用的可能是回呼的使用，
因為您可以將 `add_choice` 中的幾乎任何引數設為回撥，
您在模組中上面定義的函式。  這個函式將是
當選單元素被觸發時呼叫。

請注意，為了編輯描述，最好的呼叫方法不是
`add_choice`，但是`add_choice_edit`。  這是一個方便的捷徑
輸入此選項時可快速開啟`EvEditor`
並在編輯器關閉時返回選單。

```python
class RoomBuildingMenu(BuildingMenu):
    def init(self, room):
        self.add_choice("title", "t", attr="key")
        self.add_choice_edit("description", key="d", attr="db.desc")

```

當您想建立建築選單時，您只需匯入您的
類，建立它並指定您的預期呼叫者和要編輯的物件，
然後呼叫`open`：

```python
from <wherever> import RoomBuildingMenu

class CmdEdit(Command):

    key = "redit"

    def func(self):
        menu = RoomBuildingMenu(self.caller, self.caller.location)
        menu.open()

```


(a-simple-menu-example)=
## 一個簡單的選單範例

在深入之前，有一些事情需要指出：

- 建置選單適用於物件。  該物件將透過選單中的操作進行編輯。  所以
您可以建立一個選單來新增/編輯房間、出口、角色等。
- 建築選單按層層排列進行選擇。  選擇可以存取一個選項或一個子選項
選單。  選擇與指令相關聯（通常很短）。  例如，在所示的範例中
下面，要編輯房間鑰匙，開啟建築選單後，可以輸入`k`。  那會引導你
到鑰匙選擇，您可以在其中輸入房間的新鑰匙。  然後你可以輸入`@`離開這個
選擇並返回整個選單。  （所有這些都可以更改）。
- 要開啟選單，您將需要類似指令的東西。  這個 contrib 提供了一個基本指令
演示，但我們將在本範例中覆寫它，使用具有更大靈活性的相同程式碼。

讓我們先加入一個非常基本的範例。

(a-generic-editing-command)=
### 通用編輯指令

讓我們先新增一個指令。  您可以新增或編輯以下檔案（沒有技巧
在這裡，請隨意以不同的方式組織程式碼）：

```python
# file: commands/building.py
from evennia.contrib.building_menu import BuildingMenu
from commands.command import Command

class EditCmd(Command):

    """
    Editing command.

    Usage:
      @edit [object]

    Open a building menu to edit the specified object.  This menu allows to
    specific information about this object.

    Examples:
      @edit here
      @edit self
      @edit #142

    """

    key = "@edit"
    locks = "cmd:id(1) or perm(Builders)"
    help_category = "Building"

    def func(self):
        if not self.args.strip():
            self.msg("|rYou should provide an argument to this function: the object to edit.|n")
            return

        obj = self.caller.search(self.args.strip(), global_search=True)
        if not obj:
            return

        if obj.typename == "Room":
            Menu = RoomBuildingMenu
        else:
            obj_name = obj.get_display_name(self.caller)
            self.msg(f"|rThe object {obj_name} cannot be edited.|n")
            return

        menu = Menu(self.caller, obj)
        menu.open()
```

這個指令本身相當簡單：

1. 它有一個金鑰 `@edit` 和一個 lock 只允許建構者使用它。
2. 在它的 `func` 方法中，它首先檢查引數，如果沒有引數則傳回錯誤
指定的。
3. 然後它搜尋給定的引數。  我們在全球範圍內進行搜尋。  這裡使用的`search`方法
方式將傳回找到的物件或`None`。  如果出現以下情況，它也會向呼叫者傳送錯誤訊息：
必要的。
4. 假設我們找到了一個物件，我們檢查該物件`typename`。  這個稍後會用到
我們想要顯示幾個建築選單。  目前我們只處理`Room`。  如果
呼叫者指定了其他內容，我們將顯示錯誤。
5. 假設這個對像是 `Room`，我們定義了一個 `Menu` 物件，其中包含我們的類
建築選單。  我們建構這個類別（建立一個例項），給它呼叫者和物件
編輯。
6. 然後我們使用 `open` 方法開啟建置選單。

乍一看，結局可能有點令人驚訝。  但過程還是很簡單：我們
建立我們的建築選單的例項並呼叫其 `open` 方法。  而已。

> 我們的建築選單在哪裡？

如果您繼續新增此指令並測試它，您將收到錯誤。  我們還沒有定義
`RoomBuildingMenu` 還沒有。

若要新增此指令，請編輯 `commands/default_cmdsets.py`。  匯入我們的指令，新增匯入行
在檔案頂部：

```python
"""
...
"""

from evennia import default_cmds

# The following line is to be added
from commands.building import EditCmd
```

在下面的類別中（`CharacterCmdSet`），加入以下程式碼的最後一行：

```python
class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
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
        self.add(EditCmd())
```

(our-first-menu)=
### 我們的第一個選單

到目前為止，我們還不能使用我們的建築選單。  我們的 `@edit` 指令會丟擲錯誤。  我們必須定義
`RoomBuildingMenu` 類。  開啟`commands/building.py`檔案並在檔案末尾新增：

```python
# ... at the end of commands/building.py
# Our building menu

class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.

    For the time being, we have only one choice: key, to edit the room key.

    """

    def init(self, room):
        self.add_choice("key", "k", attr="key")
```

儲存這些更改，重新載入遊戲。  您現在可以使用 `@edit` 指令。  這是我們得到的
（請注意，我們在遊戲中輸入的指令帶有 `> ` 字首，儘管此字首會
可能不會出現在您的 MUD 使用者端）：

```
> look
Limbo(#2)
Welcome to your new Evennia-based game! Visit https://www.evennia.com if you need
help, want to contribute, report issues or just join the community.
As Account #1 you can create a demo/tutorial area with @batchcommand tutorial_world.build.

> @edit here
Building menu: Limbo

 [K]ey: Limbo
 [Q]uit the menu

> q
Closing the building menu.

> @edit here
Building menu: Limbo

 [K]ey: Limbo
 [Q]uit the menu

> k
-------------------------------------------------------------------------------
key for Limbo(#2)

You can change this value simply by entering it.

Use @ to go back to the main menu.

Current value: Limbo

> A beautiful meadow
-------------------------------------------------------------------------------

key for A beautiful meadow(#2)

You can change this value simply by entering it.

Use @ to go back to the main menu.

Current value: A beautiful meadow

> @
Building menu: A beautiful meadow

 [K]ey: A beautiful meadow
 [Q]uit the menu

> q

Closing the building menu.

> look
A beautiful meadow(#2)
Welcome to your new Evennia-based game! Visit https://www.evennia.com if you need
help, want to contribute, report issues or just join the community.
As Account #1 you can create a demo/tutorial area with @batchcommand tutorial_world.build.
```

在深入研究程式碼之前，讓我們先檢查一下我們有什麼：

- 當我們使用`@edit here`指令時，會出現該房間的建築選單。
- 此選單有兩個選擇：
    - 輸入`k`編輯房間鑰匙。  您將進入一個選擇，只需鍵入金鑰即可
房間鑰匙（就像我們在這裡所做的那樣）。  您可以使用 `@` 返回選單。
    - 您可以使用`q` 退出選單。

然後，我們使用 `look` 指令檢查選單是否已修改此房間金鑰。  所以透過新增一個
類，其中有一個方法和一行程式碼，我們新增了一個帶有兩個選項的選單。

(code-explanation)=
### 程式碼解釋

讓我們再次檢查我們的程式碼：

```python
class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.

    For the time being, we have only one choice: key, to edit the room key.

    """

    def init(self, room):
        self.add_choice("key", "k", attr="key")
```

- 我們先建立一個繼承自`BuildingMenu`的類別。  當我們想要
用這個contrib創造一個建築選單。
- 在此類中，我們重寫 `init` 方法，該方法在選單開啟時呼叫。
- 在這個`init`方法中，我們呼叫`add_choice`。  這需要幾個引數，但我們只定義了
這裡三個：
    - 選擇名稱。  這是強制性的，建築選單將使用它來瞭解如何
顯示此選擇。
    - 用於存取此選擇的指令鍵。  我們給了一個簡單的`"k"`。  選單指令通常是
相當短（這就是建築選單受到建築商讚賞的部分原因）。  您還可以
指定其他別名，但我們稍後會看到。
    - 我們新增了一個關鍵字引數 `attr`。  這告訴建築選單，當我們在這個
選擇後，我們輸入的文字將進入此 attribute 名稱。  它被稱為`attr`，但它可能是一個房間
attribute 或 typeclass 持久或非持久 attribute （我們也會看到其他範例）。

> 我們在這裡新增了 `key` 的選單選項，為什麼還要為 `quit` 定義另一個選單選項？

如果我們的建置選單是頂級選單（子選單），則它會在選擇清單的末尾建立一個選項
沒有這個功能）。  但是，您可以覆蓋它以提供不同的“退出”訊息或
執行一些操作。

我鼓勵您嘗試這段程式碼。  儘管很簡單，但它已經提供了一些功能。

(customizing-building-menus)=
## 自訂建築選單

這個有點長的部分解釋瞭如何自訂建立選單。  有不同的方法
取決於您想要實現的目標。  我們將在這裡從具體到更高階。

(generic-choices)=
### 通用選擇

在前面的範例中，我們使用了`add_choice`。  這是您可以用來新增的三種方法之一
選擇。  另外兩個用於處理更通用的操作：

- `add_choice_edit`：呼叫此函式是為了新增一個指向`EvEditor`的選擇。  它用於
在大多數情況下編輯描述，儘管您可以編輯其他內容。  我們將看到一個例子
很快。  `add_choice_edit` 使用我們將看到的大部分 `add_choice` 關鍵字引數，但通常
我們只指定兩個（有時三個）：
    - 像往常一樣選擇標題。
    - 選擇鍵（指令鍵）如常。
    - （可選）要編輯的物件的 attribute，帶有 `attr` 關鍵字引數。  經過
預設情況下，`attr` 包含 `db.desc`。  這意味著這個永續性資料attribute會被編輯
`EvEditor`。  不過，您可以將其變更為您想要的任何內容。
- `add_choice_quit`：這允許新增退出編輯器的選項。  最值得推薦！  如果你不這樣做
這樣做，建築選單會自動執行，除非你真的告訴它不要這樣做。  再說一遍，你
可以指定該選單的標題和鍵。  您也可以在此選單關閉時呼叫函式。

這是一個更完整的範例（您可以將 `RoomBuildingMenu` 類別替換為
`commands/building.py` 看到它）：

```python
class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.
    """

    def init(self, room):
        self.add_choice("key", "k", attr="key")
        self.add_choice_edit("description", "d")
        self.add_choice_quit("quit this editor", "q")
```

到目前為止，我們的建築選單類仍然很薄……但我們已經有了一些有趣的功能。
親自檢視以下 MUD 用戶端輸出（同樣，這些指令以 `> ` 為字首
區分它們）：

```
> @reload

> @edit here
Building menu: A beautiful meadow

 [K]ey: A beautiful meadow
 [D]escription:
   Welcome to your new Evennia-based game! Visit https://www.evennia.com if you need
help, want to contribute, report issues or just join the community.
As Account #1 you can create a demo/tutorial area with @batchcommand tutorial_world.build.
 [Q]uit this editor

> d

----------Line Editor [editor]----------------------------------------------------
01| Welcome to your new |wEvennia|n-based game! Visit https://www.evennia.com if you need
02| help, want to contribute, report issues or just join the community.
03| As Account #1 you can create a demo/tutorial area with |w@batchcommand tutorial_world.build|n.

> :DD

----------[l:03 w:034 c:0247]------------(:h for help)----------------------------
Cleared 3 lines from buffer.

> This is a beautiful meadow. But so beautiful I can't describe it.

01| This is a beautiful meadow. But so beautiful I can't describe it.

> :wq
Building menu: A beautiful meadow

 [K]ey: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [Q]uit this editor

> q
Closing the building menu.

> look
A beautiful meadow(#2)
This is a beautiful meadow.  But so beautiful I can't describe it.
```

因此，透過使用建置選單中的 `d` 快捷方式，將開啟 `EvEditor`。  您可以使用`EvEditor`
指令（就像我們在這裡所做的那樣，`:DD` 刪除所有，`:wq` 儲存並退出）。  當你退出編輯器時，
描述已儲存（此處為 `room.db.desc`），然後您將返回建築選單。

請注意，退出的選擇也發生了變化，這是由於我們新增了`add_choice_quit`。  在
大多數情況下，您可能不會使用此方法，因為退出選單是自動新增的。

(add_choice-options)=
### `add_choice`選項

`add_choice`和`add_choice_edit`和`add_choice_quit`這兩種方法需要很多可選
使定製更容易的引數。  其中一些選項可能不適用於 `add_choice_edit`
或 `add_choice_quit` 但是。

以下是 `add_choice` 的選項，將它們指定為引數：

- 正如我們所看到的，第一個位置強制引數是選擇標題。  這將
影響選項在選單中的顯示方式。
- 第二個位置強制引數是存取此功能表的指令鍵。  這是最好的
使用關鍵字引數作為其他引數。
- `aliases` 關鍵字引數可以包含可用於此的別名列表
選單。  例如：`add_choice(..., aliases=['t'])`
- 選擇此選項時，`attr` 關鍵字引數包含要編輯的 attribute。  這是一個
字串，它必須是名稱，從物件（在選單建構函式中指定）到達此
attribute。  例如，`"key"` 的 `attr` 將嘗試尋找 `obj.key` 來讀取和寫入
attribute。  您可以指定更複雜的 attribute 名稱，例如 `attr="db.desc"` 來設定
`desc` 永續性 attribute 或 `attr="ndb.something"`，因此請使用非永續性資料 attribute
物件。
- `text` 關鍵字引數用於變更選單選擇時顯示的文字
被選中。  選單選項提供了您可以更改的預設文字。  由於本文篇幅較長，
使用多行字串很有用（請參見下面的範例）。
- `glance` 關鍵字引數用於指定如何顯示當前訊息
選單，當選項尚未開啟時。  如果你檢查前面的例子，你會看到
目前（`key` 或`db.desc`）顯示在指令鍵旁邊的選單中。  這是
對於一目瞭然地檢視當前值（因此得名）很有用。  同樣，選單選項將提供
如果您未指定，則為預設一目瞭然。
- `on_enter` 關鍵字引數允許新增在開啟選單選項時使用的回呼。
這是更高階的，但有時很有用。
- 當呼叫者在選單中輸入一些文字時，呼叫 `on_nomatch` 關鍵字引數
不符合任何指令（包括 `@` 指令）。  預設情況下，這將編輯
指定`attr`。
- `on_leave` 關鍵字引數允許指定呼叫者離開選單時使用的回撥
選擇。  這對於清理也很有用。

這些可能性有很多，但大多數時候您並不需要全部。  這是一個簡短的
使用其中一些引數的範例（再次，替換 `RoomBuildingMenu` 類
`commands/building.py` 使用以下程式碼檢視其工作狀況）：

```python
class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.

    For the time being, we have only one choice: key, to edit the room key.

    """

    def init(self, room):
        self.add_choice("title", key="t", attr="key", glance="{obj.key}", text="""
                -------------------------------------------------------------------------------
                Editing the title of {{obj.key}}(#{{obj.id}})

                You can change the title simply by entering it.
                Use |y{back}|n to go back to the main menu.

                Current title: |c{{obj.key}}|n
        """.format(back="|n or |y".join(self.keys_go_back)))
        self.add_choice_edit("description", "d")
```

重新載入您的遊戲並檢視它的執行情況：

```
> @edit here
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [Q]uit the menu

> t
-------------------------------------------------------------------------------

Editing the title of A beautiful meadow(#2)

You can change the title simply by entering it.
Use @ to go back to the main menu.

Current title: A beautiful meadow

> @

Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [Q]uit the menu

> q
Closing the building menu.
```

最令人驚訝的部分無疑是文字。  我們使用多行語法（帶有`"""`）。
每行左側多餘的空格將自動刪除。  我們指定一些
大括號之間的資訊...有時使用雙大括號。  可能有點奇怪：

- `{back}` 是我們將使用的直接格式引數（請參閱 `.format` 說明符）。
- `{{obj...}}` 指的是正在編輯的物件。  我們使用兩個大括號，因為 `.format` 會刪除它們。

在`glance`中，我們也使用`{obj.key}`來表示我們要顯示房間的鑰匙。

(everything-can-be-a-function)=
### 一切都可以是個函式

`add_choice` 的關鍵字引數通常是字串（型別 `str`）。  但這些論點中的每一個
也可以是一個函式。  這允許大量定製，因為我們定義了回撥
將被執行以實現這樣那樣的操作。

為了進行演示，我們將嘗試新增一個新功能。  我們的房間建設選單還不錯，但是
如果能夠編輯出口就太好了。  所以我們可以在下面新增一個新的選單選項
描述...但是如何實際編輯出口？  退出不僅僅是設定的attribute：退出是
位於兩個房間之間的物件（預設型別為 `Exit`）（型別為 `Room` 的物件）。  那麼如何
我們可以證明這一點嗎？

首先讓我們加入幾個懸而未決的出口，這樣我們就有了一些東西可以處理：

```
@tunnel n
@tunnel s
```

這應該會建立兩個新房間，以及通往地獄邊緣和返回地獄邊緣的出口。

```
> look
A beautiful meadow(#2)
This is a beautiful meadow.  But so beautiful I can't describe it.
Exits: north(#4) and south(#7)
```

我們可以使用 `exits` 屬性來存取房間出口：

```
> @py here.exits
[<Exit: north>, <Exit: south>]
```

所以我們需要的是在我們的建築選單中顯示這個清單......並允許編輯它
太棒了。  也許甚至增加新的出口？

首先，讓我們寫一個函式來顯示現有出口上的`glance`。  這是程式碼，
解釋如下：

```python
class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.

    """

    def init(self, room):
        self.add_choice("title", key="t", attr="key", glance="{obj.key}", text="""
                -------------------------------------------------------------------------------
                Editing the title of {{obj.key}}(#{{obj.id}})

                You can change the title simply by entering it.
                Use |y{back}|n to go back to the main menu.

                Current title: |c{{obj.key}}|n
        """.format(back="|n or |y".join(self.keys_go_back)))
        self.add_choice_edit("description", "d")
        self.add_choice("exits", "e", glance=glance_exits, attr="exits")


# Menu functions
def glance_exits(room):
    """Show the room exits."""
    if room.exits:
        glance = ""
        for exit in room.exits:
            glance += f"\n  |y{exit.key}|n"

        return glance

    return "\n  |gNo exit yet|n"
```

當建築選單開啟時，它會向呼叫者顯示每個選項。  將顯示一個選項及其
標題（渲染得很好，也顯示了關鍵）和一目瞭然。  在`exits`的情況下
選擇，一目瞭然是一個函式，因此建築選單呼叫此函式並為其提供物件
正在編輯（這裡的房間）。  該函式應該傳回要檢視的文字。

```
> @edit here
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  north
  south
 [Q]uit the menu

> q
Closing the editor.
```

> 我如何知道要給的函式的引數？

您提供的函式可以接受很多不同的引數。  這允許採取靈活的方法
但一開始可能看起來很複雜。  基本上，你的函式可以接受任何引數，並且
建立選單將僅根據其名稱傳送引數。  如果你的函式定義了一個
例如名為 `caller` 的引數（如 `def func(caller):`），那麼建立選單就知道
第一個引數應包含建築選單的呼叫者。  這是論據，你
不必指定它們（如果指定，它們需要具有相同的名稱）：

- `menu`：如果你的函式定義了一個名為`menu`的引數，它將包含建置選單
本身。
- `choice`：如果你的函式定義了一個名為`choice`的引數，它將包含`Choice`物件
代表此選單選項。
- `string`：如果你的函式定義了一個名為`string`的引數，它將包含使用者輸入
到達此選單選項。  這不是很有用，除了我們將看到的 `nomatch` 回撥
稍後。
- `obj`：如果你的函式定義了一個名為`obj`的引數，它將包含編輯的建置選單
目的。
- `caller`：如果你的函式定義了一個名為`caller`的引數，它將包含該函式的呼叫者
建築選單。
- 任何其他：任何其他引數將包含正在由建築選單編輯的物件。

所以在我們的例子中：

```python
def glance_exits(room):
```

我們唯一需要的引數是 `room`。  它不存在於可能的引數列表中，因此
給出了建築選單的編輯物件（此處為房間）。

> 為什麼取得選單或選擇物件很有用？

大多數時候，您不需要這些引數。  在極少數情況下，您將使用它們來獲取
特定資料（如設定的預設attribute）。  本教學不會詳細闡述這些
的可能性。  只要知道它們存在即可。

我們還應該定義一個文字回撥，以便我們可以進入選單來檢視房間出口。  我們會
請參閱下一節中如何編輯它們，但這是展示更完整的內容的好機會
回撥。  要檢視它的實際效果，像往常一樣，替換 `commands/building.py` 中的類別和函式：

```python
# Our building menu

class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.

    """

    def init(self, room):
        self.add_choice("title", key="t", attr="key", glance="{obj.key}", text="""
                -------------------------------------------------------------------------------
                Editing the title of {{obj.key}}(#{{obj.id}})

                You can change the title simply by entering it.
                Use |y{back}|n to go back to the main menu.

                Current title: |c{{obj.key}}|n
        """.format(back="|n or |y".join(self.keys_go_back)))
        self.add_choice_edit("description", "d")
        self.add_choice("exits", "e", glance=glance_exits, attr="exits", text=text_exits)


# Menu functions
def glance_exits(room):
    """Show the room exits."""
    if room.exits:
        glance = ""
        for exit in room.exits:
            glance += f"\n  |y{exit.key}|n"

        return glance

    return "\n  |gNo exit yet|n"

def text_exits(caller, room):
    """Show the room exits in the choice itself."""
    text = "-" * 79
    text += "\n\nRoom exits:"
    text += "\n Use |y@c|n to create a new exit."
    text += "\n\nExisting exits:"
    if room.exits:
        for exit in room.exits:
            text += f"\n  |y@e {exit.key}|n"
            if exit.aliases.all():
                text += " (|y{aliases}|n)".format(aliases="|n, |y".join(
                    alias for alias in exit.aliases.all()
                ))
            if exit.destination:
                text += f" toward {exit.get_display_name(caller)}"
    else:
        text += "\n\n |gNo exit has yet been defined.|n"

    return text
```

特別看第二個回撥。  它需要一個額外的引數，即呼叫者（記住，
引數名稱很重要，它們的順序不相關）。  這對於顯示很有用
準確出口目的地。  這是該選單的示範：

```
> @edit here
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  north
  south
 [Q]uit the menu

> e
-------------------------------------------------------------------------------

Room exits:
 Use @c to create a new exit.

Existing exits:
  @e north (n) toward north(#4)
  @e south (s) toward south(#7)

> @
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  north
  south
 [Q]uit the menu

> q
Closing the building menu.
```

使用回撥可以提供很大的靈活性。  現在我們將瞭解如何處理子選單。

(sub-menus-for-complex-menus)=
### 複雜選單的子選單

選單相對扁平：它有一個根（您可以在其中看到所有選單選項）和單獨的選項
您可以使用選單選擇鍵進入。  一旦做出選擇，您可以輸入一些內容或返回
透過輸入返回指令（通常是`@`）返回根選單。

為什麼各個出口不應該有自己的選單呢？  假設您編輯一個出口並可以更改其
鍵、描述或別名...甚至可能是目的地？  為什麼從來沒有？  這將使建築變得更加
更容易！

建築選單系統提供了兩種方法來做到這一點。  第一個是巢狀鍵：巢狀鍵允許
超越只有一個選單/選項，擁有更多層的選單。  使用它們很快，但可能會感覺
一開始有點違反直覺。  另一種選擇是建立不同的選單類別並重定向
從第一個到第二個。  此選項可能需要更多行，但更明確並且可以
重新用於多個選單。  根據您的口味採用其中之一。

(nested-menu-keys)=
#### 巢狀選單鍵

到目前為止，我們只使用了帶有一個字母的選單鍵。  當然，我們可以新增更多，但選單鍵
它們簡單的形狀只是指令鍵。  按“e”轉到“退出”選項。

但選單鍵可以巢狀。  巢狀鍵允許新增帶有子選單的選項。  例如，輸入
“e”轉到“出口”選項，然後您可以鍵入“c”開啟選單以建立新出口，或者
“d”開啟選單以刪除出口。  第一個選單將有“e.c”鍵（先是 e，然後是 c），
第二個選單的鍵為「e.d」。

這是更高階的，如果以下程式碼對您來說聽起來不太友好，請嘗試下一個
部分提供了同一問題的不同方法。

所以我們想編輯出口。  也就是可以輸入「e」進入選擇退出，然後
輸入 `@e` 後跟退出名稱進行編輯...這將開啟另一個選單。  在此子選單中
您可以變更退出鍵或說明。

所以我們有一個類似的選單層次結構：

```
t                       Change the room title
d                       Change the room description
e                       Access the room exits
  [exit name]           Access the exit name sub-menu
                 [text] Change the exit key
```

或者，如果您喜歡範例輸出：

```
> look
A beautiful meadow(#2)
This is a beautiful meadow.  But so beautiful I can't describe it.
Exits: north(#4) and south(#7)

> @edit here
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  north
  south
 [Q]uit the menu

> e
-------------------------------------------------------------------------------

Room exits :
 Use @c to create a new exit.

Existing exits:
  @e north (n) toward north(#4)
  @e south (s) toward south(#7)

> @e north
Editing: north
Exit north:
Enter the exit key to change it, or @ to go back.

New exit key:

> door

Exit door:
Enter the exit key to change it, or @ to go back.

New exit key:

> @

-------------------------------------------------------------------------------

Room exits :
 Use @c to create a new exit.

Existing exits:
  @e door (n) toward door(#4)
  @e south (s) toward south(#7)

> @
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  door
  south
 [Q]uit the menu

> q
Closing the building menu.
```

這需要一些程式碼和一些解釋。  所以我們開始...首先是程式碼，
接下來進行解釋！

```python
# ... from commands/building.py
# Our building menu

class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.

    For the time being, we have only one choice: key, to edit the room key.

    """

    def init(self, room):
        self.add_choice("title", key="t", attr="key", glance="{obj.key}", text="""
                -------------------------------------------------------------------------------
                Editing the title of {{obj.key}}(#{{obj.id}})

                You can change the title simply by entering it.
                Use |y{back}|n to go back to the main menu.

                Current title: |c{{obj.key}}|n
        """.format(back="|n or |y".join(self.keys_go_back)))
        self.add_choice_edit("description", "d")
        self.add_choice("exits", "e", glance=glance_exits, text=text_exits, on_nomatch=nomatch_exits)

        # Exit sub-menu
        self.add_choice("exit", "e.*", text=text_single_exit, on_nomatch=nomatch_single_exit)


# Menu functions
def glance_exits(room):
    """Show the room exits."""
    if room.exits:
        glance = ""
        for exit in room.exits:
            glance += f"\n  |y{exit.key}|n"

        return glance

    return "\n  |gNo exit yet|n"

def text_exits(caller, room):
    """Show the room exits in the choice itself."""
    text = "-" * 79
    text += "\n\nRoom exits:"
    text += "\n Use |y@c|n to create a new exit."
    text += "\n\nExisting exits:"
    if room.exits:
        for exit in room.exits:
            text += f"\n  |y@e {exit.key}|n"
            if exit.aliases.all():
                text += " (|y{aliases}|n)".format(aliases="|n, |y".join(
                    alias for alias in exit.aliases.all()
                ))
            if exit.destination:
                text += f" toward {exit.get_display_name(caller)}"
    else:
        text += "\n\n |gNo exit has yet been defined.|n"

    return text

def nomatch_exits(menu, caller, room, string):
    """
    The user typed something in the list of exits.  Maybe an exit name?
    """
    string = string[3:]
    exit = caller.search(string, candidates=room.exits)
    if exit is None:
        return

    # Open a sub-menu, using nested keys
    caller.msg(f"Editing: {exit.key}")
    menu.move(exit)
    return False

# Exit sub-menu
def text_single_exit(menu, caller):
    """Show the text to edit single exits."""
    exit = menu.keys[1]
    if exit is None:
        return ""

    return f"""
        Exit {exit.key}:

        Enter the exit key to change it, or |y@|n to go back.

        New exit key:
    """

def nomatch_single_exit(menu, caller, room, string):
    """The user entered something in the exit sub-menu.  Replace the exit key."""
    # exit is the second key element: keys should contain ['e', <Exit object>]
    exit = menu.keys[1]
    if exit is None:
        caller.msg("|rCannot find the exit.|n")
        menu.move(back=True)
        return False

    exit.key = string
    return True
```

> 這是很多程式碼！  我們只處理編輯退出鍵！

這就是為什麼在某些時候您可能想要編寫一個真正的子選單，而不是使用簡單的巢狀
鍵。  但您可能也需要兩者來建立漂亮的選單！

1. 第一個新的東西是我們的選單類別。  為退出建立 `on_nomatch` 回撥後
選單（這不應該令人驚訝），我們需要新增一個巢狀鍵。  我們給這個選單一個鍵
`"e.*"`。  這有點奇怪！  “e”是退出選單的鍵。是表示一個的分隔符
巢狀選單，* 表示任何內容。  所以基本上，我們建立一個巢狀選單，其中包含
退出選單和任何東西。  我們將在實踐中看看這個「任何東西」是什麼。
2. `glance_exits`和`text_exits`基本上相同。
3. `nomatch_exits` 很短但很有趣。  當我們在“出口”中輸入一些文字時會呼叫它
選單（即在出口清單中）。  我們說過使用者應該輸入 `@e` 後跟
退出名稱進行編輯。  因此，在 `nomatch_exits` 回撥中，我們檢查該輸入。  如果輸入的
文字從`@e`開始，我們嘗試在房間裡找到出口。  如果我們這樣做...
4. 我們稱之為`menu.move`方法。  這就是巢狀選單的事情變得有點複雜的地方：我們
需要使用`menu.move`從一層到另一層進行更改。  在這裡，我們正在選擇退出（
退出選單，按“e”鍵）。  我們需要下一層來編輯出口。  所以我們呼叫 `menu.move` 並且
給它一個退出物件。  選單系統根據使用者按下的按鍵記住使用者所在的位置。
已進入：當使用者開啟選單時，沒有按鍵。  如果她選擇退出選項，
選單鍵為“e”，使用者的位置為`["e"]`（有選單鍵的清單）。  如果我們打電話
`menu.move`，我們給這個方法的任何內容都會被附加到鍵列表中，以便使用者
位置變為`["e", <Exit object>]`。
5. 在選單類別中，我們定義了選單`"e.*"`，意思是「出口處包含的選單
選擇加任何內容」。這裡的「任何內容」是一個退出：我們呼叫了`menu.move(exit)`，所以
已選擇 `"e.*"` 選單選項。
6. 在此選單中，文字設定為回撥。  還有一個 `on_nomatch` 回撥，即
每當使用者輸入一些文字時呼叫。  如果是這樣，我們更改出口名稱。

像這樣使用 `menu.move` 起初有點令人困惑。  有時它很有用。  在這種情況下，如果
我們想要一個更複雜的退出選單，使用真正的子選單是有意義的，而不是像這樣的巢狀鍵
這個。  但有時，您會發現自己不需要完整的選單即可
處理一個選擇。

(full-sub-menu-as-separate-classes)=
## 完整的子選單作為單獨的類

處理單獨退出的最佳方法是建立兩個單獨的類別：

- 一份用於房間選單。
- 一個用於單獨的退出選單。

第一個必須重新導向到第二個。  這可能更直覺、更靈活，
取決於您想要實現的目標。  那麼讓我們來建立兩個選單：

```python
# Still in commands/building.py, replace the menu class and functions by...
# Our building menus

class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.
    """

    def init(self, room):
        self.add_choice("title", key="t", attr="key", glance="{obj.key}", text="""
                -------------------------------------------------------------------------------
                Editing the title of {{obj.key}}(#{{obj.id}})

                You can change the title simply by entering it.
                Use |y{back}|n to go back to the main menu.

                Current title: |c{{obj.key}}|n
        """.format(back="|n or |y".join(self.keys_go_back)))
        self.add_choice_edit("description", "d")
        self.add_choice("exits", "e", glance=glance_exits, text=text_exits,
on_nomatch=nomatch_exits)


# Menu functions
def glance_exits(room):
    """Show the room exits."""
    if room.exits:
        glance = ""
        for exit in room.exits:
            glance += f"\n  |y{exit.key}|n"

        return glance

    return "\n  |gNo exit yet|n"

def text_exits(caller, room):
    """Show the room exits in the choice itself."""
    text = "-" * 79
    text += "\n\nRoom exits:"
    text += "\n Use |y@c|n to create a new exit."
    text += "\n\nExisting exits:"
    if room.exits:
        for exit in room.exits:
            text += f"\n  |y@e {exit.key}|n"
            if exit.aliases.all():
                text += " (|y{aliases}|n)".format(aliases="|n, |y".join(
                    alias for alias in exit.aliases.all()
                ))
            if exit.destination:
                text += f" toward {exit.get_display_name(caller)}"
    else:
        text += "\n\n |gNo exit has yet been defined.|n"

    return text

def nomatch_exits(menu, caller, room, string):
    """
    The user typed something in the list of exits.  Maybe an exit name?
    """
    string = string[3:]
    exit = caller.search(string, candidates=room.exits)
    if exit is None:
        return

    # Open a sub-menu, using nested keys
    caller.msg(f"Editing: {exit.key}")
    menu.open_submenu("commands.building.ExitBuildingMenu", exit, parent_keys=["e"])
    return False

class ExitBuildingMenu(BuildingMenu):

    """
    Building menu to edit an exit.

    """

    def init(self, exit):
        self.add_choice("key", key="k", attr="key", glance="{obj.key}")
        self.add_choice_edit("description", "d")
```

程式碼可能更容易閱讀。  但在詳細介紹它之前，讓我們看看它在
遊戲：

```
> @edit here
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  door
  south
 [Q]uit the menu

> e
-------------------------------------------------------------------------------

Room exits:
 Use @c to create a new exit.

Existing exits:
  @e door (n) toward door(#4)
  @e south (s) toward south(#7)

Editing: door

> @e door
Building menu: door

 [K]ey: door
 [D]escription:
   None

> k
-------------------------------------------------------------------------------
key for door(#4)

You can change this value simply by entering it.

Use @ to go back to the main menu.

Current value: door

> north

-------------------------------------------------------------------------------
key for north(#4)

You can change this value simply by entering it.

Use @ to go back to the main menu.

Current value: north

> @
Building menu: north

 [K]ey: north
 [D]escription:
   None

> d
----------Line Editor [editor]----------------------------------------------------
01| None
----------[l:01 w:001 c:0004]------------(:h for help)----------------------------

> :DD
Cleared 1 lines from buffer.

> This is the northern exit. Cool huh?
01| This is the northern exit. Cool huh?

> :wq
Building menu: north
 [K]ey: north
 [D]escription:
   This is the northern exit.  Cool huh?

> @
-------------------------------------------------------------------------------
Room exits:
 Use @c to create a new exit.

Existing exits:
  @e north (n) toward north(#4)
  @e south (s) toward south(#7)

> @
Building menu: A beautiful meadow

 [T]itle: A beautiful meadow
 [D]escription:
   This is a beautiful meadow.  But so beautiful I can't describe it.
 [E]xits:
  north
  south
 [Q]uit the menu

> q
Closing the building menu.

> look
A beautiful meadow(#2)
This is a beautiful meadow.  But so beautiful I can't describe it.
Exits: north(#4) and south(#7)
> @py here.exits[0]
>>> here.exits[0]
north
> @py here.exits[0].db.desc
>>> here.exits[0].db.desc
This is the northern exit.  Cool huh?
```

非常簡單，我們建立了兩個選單並將它們橋接在一起。  這需要更少的回撥。  那裡
只需在`nomatch_exits`中新增一行：

```python
    menu.open_submenu("commands.building.ExitBuildingMenu", exit, parent_keys=["e"])
```

我們必須在選單物件上呼叫`open_submenu`（顧名思義，它開啟一個子選單）
有三個引數：

- 要建立的選單類別的路徑。  它是通往選單的 Python 類別（注意
點）。
- 將由選單編輯的物件。  在這裡，這是我們的出口，所以我們把它交給子選單。
- 子選單關閉時開啟的父級按鍵。  基本上，當我們處於根部時
子選單並按`@`，我們將使用父鍵開啟父選單。  所以我們指定`["e"]`，
因為父選單是「退出」選擇。

就是這樣。  新班級將自動建立。  正如你所看到的，我們必須建立一個
`on_nomatch` 回呼開啟子選單，但一旦開啟，需要時就會自動關閉。

(generic-menu-options)=
### 通用選單選項

有一些選項可以在任何選單類別上設定。  這些選項允許更大的
定製。  它們是類別屬性（請參閱下面的範例），因此只需在類別中設定它們即可
身體：

- `keys_go_back`（預設為`["@"]`）：用於返回選單層次結構的鍵，可以選擇
到根選單，從子選單到父選單。  預設情況下，僅使用 `@`。  你可以改變這個
一個選單或所有選單的鍵。  如果需要，您可以定義多個返回指令。
- `sep_keys`（預設`"."`）：這是巢狀鍵的分隔符號。  沒有真正的必要
重新定義它，除非您確實需要點作為鍵，並且需要在選單中巢狀鍵。
- `joker_key`（預設為`"*"`）：用於巢狀鍵，表示「任意鍵」。  再說一遍，你不應該
需要更改它，除非您希望能夠在指令鍵中使用 `@*@`，並且還需要巢狀
選單中的按鍵。
- `min_shortcut`（預設為`1`）：雖然我們在這裡沒有看到它，但可以建立一個選單選項
而不給它鑰匙。  如果是這樣，選單系統將嘗試「猜測」該鍵。  該選項允許
出於安全原因更改任何金鑰的最小長度。

要設定其中之一，只需在選單類別中執行以下操作：

```python
class RoomBuildingMenu(BuildingMenu):
    keys_go_back = ["/"]
    min_shortcut = 2
```

(conclusion)=
## 結論

建立選單意味著節省您的時間並建立豐富而簡單的介面。  但他們可以是
學習起來很複雜，需要閱讀原始碼才能找出如何做這樣或那樣的事情
事。  該檔案無論有多長，都是為了描述該系統，但很可能
讀完之後你仍然會有疑問，特別是如果你嘗試將這個系統推向
在很大程度上。  不要猶豫，閱讀這個 contrib 的文件，它的意思是
詳盡但使用者友好。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\building_menu\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
