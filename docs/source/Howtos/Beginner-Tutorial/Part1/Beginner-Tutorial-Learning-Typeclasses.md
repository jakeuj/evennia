(making-objects-persistent)=
# 使物件持久化

現在我們已經瞭解如何在 Evennia 庫中找到內容，讓我們使用它。

在[Python類別和物件](./Beginner-Tutorial-Python-classes-and-objects.md)課程中，我們建立了毛茸茸的、可愛的龍
和史矛革，讓它們飛起來並噴火。到目前為止，我們的龍是短暫的 - 每當我們 `restart` 伺服器或 `quit()` 退出 python 模式時，它們就會消失。

這是到目前為止您在 `mygame/typeclasses/monsters.py` 中應該得到的內容：


```python

class Monster:
    """
    This is a base class for Monsters.
    """
 
    def __init__(self, key):
        self.key = key 

    def move_around(self):
        print(f"{self.key} is moving!")


class Dragon(Monster):
    """
    This is a dragon-specific monster.
    """

    def move_around(self):
        super().move_around()
        print("The world trembles.")

    def firebreath(self):
        """ 
        Let our dragon breathe fire.
        """
        print(f"{self.key} breathes fire!")

```

(our-first-persistent-object)=
## 我們的第一個持久物件

此時我們應該要夠瞭解`mygame/typeclasses/objects.py`中發生了什麼事。讓我們
開啟它：

```python
"""
module docstring
"""
from evennia import DefaultObject

class ObjectParent:
    """ 
    class docstring 
    """
    pass

class Object(ObjectParent, DefaultObject):
    """
    class docstring
    """
    pass
```

因此，我們有一個類別 `Object`，它繼承自 `ObjectParent`（它是空的）和 `DefaultObject`，我們從 Evennia 匯入了它。 `ObjectParent` 充當放置您希望所有 `Objects` 擁有的程式碼的位置。我們現在將重點放在 `Object` 和 `DefaultObject`。

類別本身不執行任何操作（它只是 `pass`es），但這並不意味著它沒有用。正如我們所看到的，它繼承了其父級的所有功能。事實上，它現在是 `DefaultObject` 的_精確副本_。  一旦我們知道 `DefaultObject` 上有哪些型別的方法和資源可用，我們就可以新增自己的方法和資源並更改其工作方式！

Evennia 類別提供的一件事是普通 Python 類別所沒有的，那就是_永續性_——它們在伺服器重新載入後仍然存在，因為它們儲存在資料庫中。

返回`mygame/typeclasses/monsters.py`。更改如下：

```python

from typeclasses.objects import Object

class Monster(Object):
    """
    This is a base class for Monsters.
    """
    def move_around(self):
        print(f"{self.key} is moving!")


class Dragon(Monster):
    """
    This is a dragon-specific Monster.
    """

    def move_around(self):
        super().move_around()
        print("The world trembles.")

    def firebreath(self):
        """ 
        Let our dragon breathe fire.
        """
        print(f"{self.key} breathes fire!")

```

別忘了儲存。我們刪除了 `Monster.__init__` 並使 `Monster` 繼承自 Evennia 的 `Object`（如我們所見，後者又繼承自 Evennia 的 `DefaultObject`）。推而廣之，這意味著 `Dragon` 也繼承自 `DefaultObject`，只是距離更遠！

(making-a-new-object-by-calling-the-class)=
### 透過呼叫類別建立一個新物件

首先像往常一樣重新載入伺服器。這次我們需要稍微不同地創造龍：

```{sidebar} 關鍵字引數

_關鍵字引數_（如 `db_key="Smaug"`）是一種命名函式或方法的輸入引數的方式。它們使內容更易於閱讀，但也允許方便地為未明確給出的值設定預設值。我們之前看到它們使用了 `.format()`。

```
    > py
    > from typeclasses.monsters import Dragon
    > smaug = Dragon(db_key="Smaug", db_location=here)
    > smaug.save()
    > smaug.move_around()
    Smaug is moving!
    The world trembles.

Smaug 的工作方式與以前相同，但我們以不同的方式建立了他：首先我們使用
`Dragon(db_key="Smaug", db_location=here)` 建立物件，然後我們使用 `smaug.save()` 之後。

```{sidebar} 這裡
`db_location=here` 中使用的 `here` 是您目前位置的捷徑。此 `here`（類似 `me`）_僅_可在 `py` 指令中使用；你不能在你寫的其他Python程式碼中使用它，除非你自己定義它。
```

    > quit()
    Python Console is closing.
    > look 
    
你現在應該看到史矛革_和你在房間裡_。哇哦！

    > reload 
    > look 
    
_他還在那裡_...我們剛剛所做的是在資料庫中為 Smaug 建立一個新條目。我們為該物件指定了名稱（鍵）並將其位置設為我們目前的位置。

要在程式碼中使用 Smaug，我們必須先在資料庫中找到他。對於當前位置的物件，我們可以透過使用 `me.search()` 輕鬆地在 `py` 中執行此操作：

    > py smaug = me.search("Smaug") ; smaug.firebreath()
    Smaug breathes fire!  

(creating-using-create_object)=
### 使用 create_object 建立

像上面那樣建立 Smaug 很好，因為它與我們之前建立非資料庫繫結 Python 例項的方式類似。但是你需要使用 `db_key` 而不是 `key` 並且你還必須記住之後呼叫 `.save()` 。 Evennia 有一個更常用的輔助函式，稱為 `create_object`。這次讓我們重新建立 Cuddly：

    > py evennia.create_object('typeclasses.monsters.Monster', key="Cuddly", location=here)
    > look 
    
嘭，卡德利現在應該跟你在房間裡了，比史矛革沒那麼可怕。您指定所需程式碼的 python 路徑，然後設定鍵和位置（如果您已經匯入了 `Monster` 類，您也可以透過它）。 Evennia 為您設定並儲存。

如果你想從任何地方（不僅僅是在同一個房間）找到 Cuddly，你可以使用 Evennia 的 `search_object` 函式：

    > py cuddly = evennia.search_object("Cuddly")[0] ; cuddly.move_around()
    Cuddly is moving!

> `[0]` 是因為 `search_object` 總是傳回一個由零個、一個或多個找到的物件組成的清單。 `[0]` 意味著我們想要這個清單的第一個元素（Python 中計數總是從 0 開始）。如果有多個可愛寶寶，我們可以用 `[1]` 獲得第二個。

(creating-using-create-command)=
### 使用create指令建立

最後，您也可以使用我們在前幾課中探討過的熟悉的建構器指令來建立一條新龍：

    > create/drop Fluffy:typeclasses.monsters.Dragon

蓬鬆現在在房間裡。在瞭解了物件的建立方式之後，您將意識到該指令真正所做的只是解析您的輸入，找出 `/drop` 的意思是“為物件提供與呼叫者相同的位置”，然後執行與以下類似的呼叫

    evennia.create_object("typeclasses.monsters.Dragon", key="Cuddly", location=here)

這幾乎就是強大的 `create` 指令的全部了！剩下的只是解析指令以瞭解使用者想要建立的內容。

(typeclasses)=
## Typeclasses

`Object`（以及我們從上面繼承的`DefafultObject`類別就是我們所說的_Typeclass_。這是一個Evennia的東西。typeclass的例項在建立時會將自身儲存到資料庫中，之後您只需搜尋它即可將其取回。

我們使用術語 _typeclass_ 或 _typeclassed_ 來區分這些型別的類別和物件與普通的 Python 類，後者的例項會在重新載入時消失。

Evennia中typeclasses的數量很少，可以背下來：

| Evennia基礎typeclass | mygame.typeclasses 孩子 | 描述 |  
| --------------- |  --------------| ------------- | 
| `evennia.DefaultObject` | `typeclasses.objects.Object` | 一切都有位置 |
| `evennia.DefaultCharacter`（`DefaultObject` 的子級） | `typeclasses.characters.Character` | 玩家頭像 |
| `evennia.DefaultRoom`（`DefaultObject` 的子級） | `typeclasses.rooms.Room` | 遊戲內地點 | 
| `evennia.DefaultExit`（`DefaultObject` 的子代） | `typeclasses.exits.Exit` | 房間之間的連結 | 
| `evennia.DefaultAccount` | `typeclasses.accounts.Account` | 一個玩家帳號 | 
| `evennia.DefaultChannel` | `typeclasses.channels.Channel` | 遊戲內通訊 | 
|  `evennia.DefaultScript` | `typeclasses.scripts.Script` | 沒有位置的實體 | 

`mygame/typeclasses/` 下的子類別是為了方便您修改和使用。  從 Evennia 基 typeclass 繼承（任意距離）的每個類別也被視為 typeclass。

```
from somewhere import Something 
from evennia import DefaultScript 

class MyOwnClass(Something): 
    # not inheriting from an Evennia core typeclass, so this 
    # is just a 'normal' Python class inheriting from somewhere
    pass 

class MyOwnClass2(DefaultScript):
    # inherits from one of the core Evennia typeclasses, so 
    # this is also considered a 'typeclass'.
    pass

```

```{sidebar} 為什麼發明「typeclass」這個名字？
我們將「常規類別」與「typeclasses」分開，因為雖然 typeclasses 的行為幾乎與普通 Python 類別一樣，但[存在一些差異](../../../Components/Typeclasses.md)。我們現在將掩蓋這些差異，但當您稍後想做更高階的事情時，它們值得閱讀。
```

請注意，`mygame/typeclasses/` 中的類別_不是相互繼承的_。例如，`Character` 繼承自 `evennia.DefaultCharacter`，而不是繼承自 `typeclasses.objects.Object`。  因此，如果您更改 `Object`，則不會導致 `Character` 類別發生任何變更。如果您願意，您可以輕鬆地將子類別變更為以這種方式繼承； Evennia 不在乎。

正如我們的 `Dragon` 示例所示，您不必_必須_直接修改這些模組。您可以建立自己的模組並匯入基底類別。

(examining-objects)=
### 檢查物體

當你這樣做時

    > create/drop giantess:typeclasses.monsters.Monster
    You create a new Monster: giantess.
    
或者

    > py evennia.create_object("typeclasses.monsters.Monster", key="Giantess", location=here)
    
您正在準確指定要使用哪個 typeclass 來建立女巨人。讓我們檢查一下結果：

    > examine giantess
    ------------------------------------------------------------------------------- 
    Name/key: Giantess (#14)
    Typeclass: Monster (typeclasses.monsters.Monster)
    Location: Limbo (#2)
    Home: Limbo (#2)
    Permissions: <None>
    Locks: call:true(); control:id(1) or perm(Admin); delete:id(1) or perm(Admin);
       drop:holds(); edit:perm(Admin); examine:perm(Builder); get:all();
       puppet:pperm(Developer); tell:perm(Admin); view:all()
    Persistent attributes:
     desc = You see nothing special. 
    ------------------------------------------------------------------------------- 

我們在[關於遊戲內構建的課程](./Beginner-Tutorial-Building-Quickstart.md)中簡要使用了`examine`指令。現在這些行可能對我們更有用：
- **名稱/鍵** - 這個東西的名稱。值 `(#14)` 對您來說可能不同。這是
    unique 'primary key' or _dbref_ for this entity in the database.
- **Typeclass**：這顯示了我們指定的typeclass，以及它的路徑。
- **地點**：我們在地獄邊境。如果您搬到其他地方，您會看到這一點。也顯示了 Limbo 的 `#dbref`。
- **Home**：所有具有位置的物件（繼承自 `DefaultObject`）都必須有一個 home 位置。這是在物件目前位置被刪除時將物件移動到的備份。
- **許可權**：_許可權_就像_鎖_的反面－它們就像解鎖對其他事物的存取的鑰匙。女巨人沒有這樣的鑰匙（也許幸運）。 [許可權](../../../Components/Permissions.md) 有更多資訊。
- **鎖定**：鎖定與_許可權_相反 - 指定_其他_物件必須滿足什麼條件才能存取`giantess`物件。這使用了非常靈活的迷你語言。對於檢查，`examine:perm(Builders)` 行被解讀為「只有具有 _Builder_ 或更高許可權的人才能_檢查_此物件」。由於我們是超級使用者，因此我們可以輕鬆地透過（甚至繞過）此類鎖。有關詳細資訊，請參閱[鎖](../../../Components/Locks.md) 檔案。
- **持久屬性**：這允許在型別分類實體上儲存任意的永續性資料。我們將在下一節中討論這些內容。
  
請注意 **Typeclass** 行如何準確描述在哪裡可以找到該物件的程式碼？這對於理解 Evennia 中的任何物件如何運作非常有用。


(default-typeclasses)=
### 預設typeclasses

如果我們建立一個物件並且_不_指定它的typeclass，會發生什麼事？

    > create/drop box 
    You create a new Object: box.
    
或者

    > py create.create_object(None, key="box", location=here)
    
現在檢查一下：
    
    > examine box  
    
您會發現 **Typeclass** 行現在顯示為

    Typeclass: Object (typeclasses.objects.Object) 
    
因此，當您未指定 typeclass 時，Evennia 使用預設值，更具體地說，`mygame/typeclasses/objects.py` 中的（到目前為止）空 `Object` 類別。這通常是您想要的，特別是因為您可以根據需要調整該類別。

但 Evennia 知道回退到此類的原因並不是硬編碼的 - 這是一個設定。預設位於 [evennia/settings_default.py](../../../Setup/Settings-Default.md) 中，名稱為 `BASE_OBJECT_TYPECLASS`，設定為 `typeclasses.objects.Object`。

```{sidebar} 改變事物

雖然根據自己的喜好更改資料夾很誘人，但這可能會使遵循教學變得更加困難，並且在您向其他人尋求幫助時可能會感到困惑。因此，除非您真正知道自己在做什麼，否則不要做得太過分。
```

因此，如果您希望建立指令和方法預設為其他類，您可以將自己的 `BASE_OBJECT_TYPECLASS` 行新增至 `mygame/server/conf/settings.py`。對於所有其他型別類別（例如角色、房間和帳戶）也是如此。這樣，如果您願意，您可以顯著更改遊戲目錄的佈局。你只需要告訴Evennia所有東西在哪裡。
    
(modifying-ourselves)=
## 改變自己

讓我們試著稍微改變一下自己。開啟`mygame/typeclasses/characters.py`。

```python
"""
(module docstring)
"""
from evennia import DefaultCharacter
from .objects import ObjectParent

class Character(ObjectParent, DefaultCharacter):
    """
    (class docstring)
    """
    pass
```

現在看起來很熟悉 - 一個繼承自 Evennia 基底型別classObjectParent 的空類別。 `ObjectParent`（預設為空）也用於新增所有型別的物件共享的任何功能。正如您所期望的，如果您不指定的話，這也是用於建立角色的預設typeclass。您可以驗證一下：


    > examine me
    ------------------------------------------------------------------------------
    Name/key: YourName (#1)
    Session id(s): #1
    Account: YourName
    Account Perms: <Superuser> (quelled)
    Typeclass: Character (typeclasses.characters.Character)
    Location: Limbo (#2)
    Home: Limbo (#2)
    Permissions: developer, player
    Locks:      boot:false(); call:false(); control:perm(Developer); delete:false();
          drop:holds(); edit:false(); examine:perm(Developer); get:false();
          msg:all(); puppet:false(); tell:perm(Admin); view:all()
    Stored Cmdset(s):
     commands.default_cmdsets.CharacterCmdSet [DefaultCharacter] (Union, prio 0)
    Merged Cmdset(s):
       ...
    Commands available to YourName (result of Merged CmdSets):
       ...
    Persistent attributes:
     desc = This is User #1.
     prelogout_location = Limbo
    Non-Persistent attributes:
     last_cmd = None
    ------------------------------------------------------------------------------
    
是的，`examine` 指令可以理解 `me`。這次你得到了更長的輸出。除了一個簡單的物件之外，還有更多的事情要做。以下是一些值得注意的新欄位：

- **Session id(s)**：這標識_Session_（即與玩家遊戲使用者端的單獨連線）。
- **帳戶** 顯示與此角色關聯的 `Account` 物件和 Session。
- **儲存/合併Cmdsets**和**可用指令**與儲存在您身上的_指令_相關。我們將在[下一課](./Beginner-Tutorial-Adding-Commands.md)中介紹它們。現在，知道這些構成了您在給定時刻可用的所有指令就足夠了。
- **非永續性屬性**是僅暫時儲存的屬性，並將在下次重新載入時消失。

檢視 **Typeclass** 欄位，您會發現它按預期指向 `typeclasses.character.Character`。因此，如果我們修改這個類，我們也會修改我們自己。

(a-method-on-ourselves)=
### 一個針對我們自己的方法

讓我們先嘗試一些簡單的事情。回到`mygame/typeclasses/characters.py`：

```python
# in mygame/typeclasses/characters.py

# ...

class Character(ObjectParent, DefaultCharacter):
    """
    (class docstring)
    """

    strength = 10
    dexterity = 12
    intelligence = 15

    def get_stats(self):
        """
        Get the main stats of this character
        """
        return self.strength, self.dexterity, self.intelligence

```

    > reload 
    > py self.get_stats()
    (10, 12, 15)
    
```{sidebar} 元組和列表

- `list` 寫為 `[a, b, c, d,...]`。建立後可以修改。
- `tuple` 寫為 `(a, b, c,...)`。一旦建立就無法修改。
```
我們建立了一個新方法，給它一個檔案字串，並讓它 `return` 我們設定的 RP-esque 值。它以 _tuple_ `(10, 12, 15)` 的形式傳回。若要取得特定值，您可以指定所需值的_index_，從零開始：

    > py stats = self.get_stats() ; print(f"Strength is {stats[0]}.")
    Strength is 10.

(attributes)=
### 屬性

那麼當我們增強實力時會發生什麼事呢？這是一種方式：

    > py self.strength = self.strength + 1
    > py self.strength
    11
    
這裡我們將強度設定為等於其先前的值 + 1。更短的編寫方法是使用 Python 的 `+=` 運運算元：

    > py self.strength += 1
    > py self.strength
    12     
    > py self.get_stats()
    (12, 12, 15)
    
這看起來是正確的！也嘗試更改 dex 和 int 的值；效果很好。然而：

    > reload 
    > py self.get_stats()
    (10, 12, 15)
    
重新載入後，我們所有的更改都被忘記了。當我們像這樣更改屬性時，它只會在記憶體中更改，而不是在資料庫中更改（我們也不會修改 python 模組的程式碼）。因此，當我們重新載入時，載入了“新鮮”`Character` 類，並且它仍然具有我們在其中寫入的原始統計資料。
 
原則上我們可以更改 python 程式碼。但我們不想每次都手動執行此操作。更重要的是，由於我們在類別中硬編碼了統計資料，所以遊戲中的_每個_角色例項現在都將具有完全相同的`str`、`dex` 和 `int`！這顯然不是我們想要的。

Evennia 為此提供了一種特殊的、持久的屬性型別，稱為 `Attribute`。像這樣修改你的`mygame/typeclasses/characters.py`：
    
```python
# in mygame/typeclasses/characters.py

# ...

class Character(ObjectParent, DefaultCharacter):
    """
    (class docstring)
    """

    def get_stats(self):
        """
        Get the main stats of this character
        """
        return self.db.strength, self.db.dexterity, self.db.intelligence
```

```{sidebar} Attribute 名稱中有空格嗎？

如果您希望 Attribute 名稱中包含空格怎麼辦？或者您想動態分配 Attribute 的名稱？然後您可以使用 `.attributes.add(name, value)` 代替，例如 `self.attributes.add("emotional intelligence", 10)`。你用`self.attributes.get("emotional intelligence"`再次讀出它。

```

我們刪除了硬編碼的統計資料，並為每個統計資料新增了`.db`。 `.db` 處理程式將統計資料變為 Evennia [Attribute](../../../Components/Attributes.md)。

    > reload 
    > py self.get_stats()
    (None, None, None) 
    
由於我們刪除了硬編碼值，Evennia 還不知道它們應該是什麼。所以我們得到的只是 `None`，這是一個 Python 保留字，代表什麼都沒有，一個無值。這與普通的 python 屬性不同：

    > py me.strength
    AttributeError: 'Character' object has no attribute 'strength'
    > py me.db.strength
    (nothing will be displayed, because it's None)

嘗試取得未知的普通 Python 屬性將給出錯誤。獲取未知的 Evennia `Attribute` 永遠不會給出錯誤，而只會導致返回 `None`。這通常非常實用。

接下來，讓我們測試分配這些屬性

    > py me.db.strength, me.db.dexterity, me.db.intelligence = 10, 12, 15
    > py me.get_stats()
    (10, 12, 15)
    > reload 
    > py me.get_stats()
    (10, 12, 15)
    
現在我們將屬性設定為正確的值，它們在伺服器重新載入後仍然存在！ Let's modify the strength:
    
    > py self.db.strength += 2 
    > py self.get_stats()
    (12, 12, 15)
    > reload 
    > py self.get_stats()
    (12, 12, 15)
    
此外，我們的變更現在可以在重新載入後繼續存在，因為 Evennia 會自動為我們將 Attribute 儲存到資料庫中。

(setting-things-on-new-characters)=
### 對新角色進行設定

情況看起來好多了，但有一件事仍然很奇怪 - 統計資料一開始的值是 `None`，我們必須手動將它們設定為合理的值。在後面的課程中，我們將更詳細地研究角色建立。現在，讓我們為每個新角色提供一些隨機統計資料作為開始。

我們希望這些統計資料僅在第一次建立物件時設定一次。對於角色來說，這個方法稱為`at_object_creation`。


```python
# in mygame/typeclasses/characters.py

# ...
import random 

class Character(ObjectParent, DefaultCharacter):
    """
    (class docstring)
    """

    def at_object_creation(self):       
        self.db.strength = random.randint(3, 18)
        self.db.dexterity = random.randint(3, 18)
        self.db.intelligence = random.randint(3, 18)
    
    def get_stats(self):
        """
        Get the main stats of this character
        """
        return self.db.strength, self.db.dexterity, self.db.intelligence
```

我們匯入了一個新模組，`random`。這是Python 標準函式庫的一部分。我們使用 `random.randint` 為每個統計資料設定一個從 3 到 18 的隨機值。很簡單，但是對於一些經典的RPGs來說，這就是你所需要的！

    > reload 
    > py self.get_stats()
    (12, 12, 15)
    
```{sidebar} __init__ 與 at_object_creation

對於 `Monster` 類，我們使用 `__init__` 來設定類別。我們不能將其用於 typeclass，因為它會被多次呼叫，至少在每次重新載入後，可能更多取決於快取。即使你熟悉Python，避免為typeclasses碰觸`__init__`，結果也不會是你所期望的。

```
嗯，這與我們之前設定的值相同。它們不是隨機的。原因當然是，如前所述，`at_object_creation` 僅執行_一次_，即第一次建立角色時。我們的角色物件很早之前就已經建立了，所以不會再呼叫它。
    
不過手動執行它很簡單：

    > py self.at_object_creation()
    > py self.get_stats()
    (5, 4, 8)
    
在這個例子中，幸運女神並沒有對我們微笑。也許你會過得更好。 Evennia 有一個輔助指令 `update`，它重新執行建立掛鉤，並清除 `at_object_creation` 未重新建立的任何其他屬性：

    > update self
    > py self.get_stats()
    (8, 16, 14)

   
(updating-all-characters-in-a-loop)=
### 迴圈更新所有字元
    
```{sidebar} AttributeProperties
還有另一種方法可以在類別上定義屬性，稱為 [AttributeProperties](../../../Components/Attributes.md#using-attributeproperty)。它們可以更輕鬆地維護 typeclass 上的靜態預設 Attribute 值。當我們在本教學系列後面製作遊戲時，我們將展示它們。
```

不用說，在建立大量物件（在本例中為字元）之前，明智的做法是先了解要進入 `at_object_creation` 鉤子的內容。

幸運的是，您只需要更新物件一次，並且不必手動對每個人重新執行 `at_object_creation` 方法。為此，我們將嘗試使用 Python _loop_。讓我們進入多行Python模式：

    > py
    > for a in [1, 2, "foo"]:   
    >     print(a)
    1
    2
    foo
    
python _for-loop_ 允許我們迴圈某些東西。上面，我們建立了一個由兩個數字和一個字串組成的清單。在迴圈的每次迭代中，變數 `a` 依次成為元素，然後我們列印它。
    
對於我們的列表，我們想要迴圈所有字元，並且想要對每個字元呼叫 `.at_object_creation`。這是如何完成的（仍然處於 python 多行模式）：

    > from typeclasses.characters import Character
    > for char in Character.objects.all():
    >     char.at_object_creation()
    
```{sidebar} 資料庫查詢

`Character.objects.all()` 是用 Python 表達的資料庫查詢的範例。這將在後臺轉換為資料庫查詢。此語法是[Django 查詢語言](https://docs.djangoproject.com/en/4.1/topics/db/queries/) 的一部分。您不需要了解 Django 即可使用 Evennia，但如果您需要更具體的資料庫查詢，那麼在您需要時它始終可用。我們將在後面的課程中回到資料庫查詢。
``` 
我們匯入 `Character` 類，然後使用 `.objects.all()` 來取得所有 `Character` 例項。簡單來說，`.objects` 是一種資源，可以從中查詢所有 `Characters`。使用 `.all()` 可以獲得所有這些的列表，然後我們立即迴圈遍歷。繁榮，我們剛剛更新了所有角色，包括我們自己：

    > quit()
    Closing the Python console.
    > py self.get_stats()
    (3, 18, 10)

(extra-credits)=
## 額外學分

這個原理對於其他typeclasses也是一樣的。因此，使用本課程中探討的工具，嘗試使用 `is_dark` 標誌擴充套件預設房間。它可以是 `True` 或 `False`。  讓所有新房間都以 `is_dark = False` 開頭，並確保一旦您更改它，它就可以在重新載入後倖存下來。  哦，如果您之前建立了任何其他房間，請確保它們也獲得新標誌！

(conclusions)=
## 結論

在本課中，我們透過讓龍的類別繼承於 `Object`（Evennia 的 _typeclasses_ 之一）來建立資料庫持久龍。我們探索如果我們沒有明確指定路徑，Evennia 會在哪裡找到 typeclasses。然後我們修改自己 - 透過 `Character` 類 - 給我們一些簡單的 RPG 統計資料。這導致需要使用 Evennia 的 _Attributes_（可透過 `.db` 設定）並使用 for 迴圈來更新自己。

Typeclasses 是 Evennia 的基本部分，我們將在本教學中看到它們的更多用途。但現在已經足夠了。是時候採取一些行動了。讓我們瞭解_指令_。


