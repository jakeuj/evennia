(tags)=
# Tags

_標籤_是一種簡短的文字標籤，人們可以將其「附加」到物體上，以便對其進行組織、分組和快速查詢其屬性，類似於將標籤附加到行李上的方式。

```{code-block}
:caption: In game 
> tag obj = tagname
```
```{code-block} python 
:caption: In code, using .tags (TagHandler)

obj.tags.add("mytag", category="foo")
obj.tags.get("mytag", category="foo")
```

```{code-block} python
:caption: In code, using TagProperty or TagCategoryProperty

from evennia import DefaultObject
from evennia import TagProperty, TagCategoryProperty

class Sword(DefaultObject): 
    # name of property is the tagkey, category as argument
    can_be_wielded = TagProperty(category='combat')
    has_sharp_edge = TagProperty(category='combat')

    # name of property is the category, tag-keys are arguments
    damage_type = TagCategoryProperty("piercing", "slashing")
    crafting_element = TagCategoryProperty("blade", "hilt", "pommel") 
        
```

在遊戲中，tags 由預設的 `tag` 指令控制：

     > tag Chair = furniture
     > tag Chair = furniture
     > tag Table = furniture
     
     > tag/search furniture 
     Chair, Sofa, Table
     

Evennia 實體可以由任意數量的 tags 標記。 Tags 比 [屬性](./Attributes.md) 更有效，因為在資料庫端，Tags 在具有該特定 tag 的所有物件之間_共享_。 tag 本身不具有值；相反，檢查的內容是 tag 本身是否存在 - 給定的對像要麼具有給定的 tag，要麼沒有。

在程式碼中，您可以使用型別分類實體上的 `TagHandler` (`.tags`) 來管理 Tags。您也可以透過 `TagProperty`（一個 tag，每行一個類別）或 `TagCategoryProperty`（一個類別，每行多個 tags）在類別層級上分配 Tags。這兩個都在底層使用了 `TagHandler`，它們只是在定義類別時新增 tags 的便捷方法。

上面的tags告訴我們`Sword`既鋒利又可以使用。如果這就是他們所做的一切，那麼他們可能只是一個普通的 Python 標誌。當tags變得重要時，如果有很多物件具有不同的tags組合。也許你有一個魔法咒語，可以讓城堡中所有鋒利的物體變鈍——無論是劍、匕首、矛還是菜刀！然後，您可以使用 `has_sharp_edge` tag 抓取所有物件。 
另一個例子是天氣 script 影響所有標記為 `outdoors` 的房間或尋找標記為 `belongs_to_fighter_guild` tag 的所有字元。

在Evennia中，Tags在技術上也用於實現`Aliases`（物件的替代名稱）和`Permissions`（[Locks](./Locks.md)檢查的簡單字串）。


(working-with-tags)=
## 與 Tags 一起工作

(searching-for-tags)=
### 正在搜尋 tags

使用 tags （一旦設定）的常見方法是尋找用特定 tag 組合標記的所有物件：

    objs = evennia.search_tag(key=("foo", "bar"), category='mycategory')

如上所示，您還可以有 tags 不含類別（`None` 的類別）。

```python
     import evennia
     
     # all methods return Querysets

     # search for objects 
     objs = evennia.search_tag("furniture")
     objs2 = evennia.search_tag("furniture", category="luxurious")
     dungeon = evennia.search_tag("dungeon#01")
     forest_rooms = evennia.search_tag(category="forest") 
     forest_meadows = evennia.search_tag("meadow", category="forest")
     magic_meadows = evennia.search_tag("meadow", category="magical")

     # search for scripts
     weather = evennia.search_tag_script("weather")
     climates = evennia.search_tag_script(category="climate")

     # search for accounts
     accounts = evennia.search_tag_account("guestaccount")          
```

> 請注意，僅搜尋「傢俱」將僅傳回帶有「傢俱」tag 標記且類別為 `None` 的物件。我們必須明確給出類別才能獲得“豪華”傢俱。

使用任何 `search_tag` 變體都會傳回 [Django 查詢集](https://docs.djangoproject.com/en/4.1/ref/models/querysets/)，包括如果您只有一個符合專案。您可以將查詢集視為列表並對其進行迭代，或者繼續使用它們來建立搜尋查詢。

請記住，在搜尋時，不設定類別意味著將其設為 `None` - 這並不意味著類別未定義，而是 `None` 被視為預設的未命名類別。

```python
import evennia 

myobj1.tags.add("foo")  # implies category=None
myobj2.tags.add("foo", category="bar")

# this returns a queryset with *only* myobj1 
objs = evennia.search_tag("foo")

# these return a queryset with *only* myobj2
objs = evennia.search_tag("foo", category="bar")
# or
objs = evennia.search_tag(category="bar")
```

還有一個遊戲內指令處理分配和使用 ([Object-](./Objects.md)) tags：

     tag/search furniture


(taghandler)=
### TagHandler

當您已經有了條目時，這是使用 tags 的主要方法。該處理程式作為 `.tags` 位於所有型別分類實體上，並且您使用 `.tags.add()`、`.tags.remove()` 和 `.tags.has()` 來管理物件上的 Tags。 [請參閱 api 檔案](evennia.typeclasses.tags.TagHandler) 以瞭解更多有用的方法。

TagHandler 可以在任何基本 *typeclassed* 物件上找到，分別是 [Objects](./Objects.md)、[Accounts](./Accounts.md)、[Scripts](./Scripts.md) 和 [Channels](./Channels.md)（及其子項）。以下是一些使用範例：

```python
     mychair.tags.add("furniture")
     mychair.tags.add("furniture", category="luxurious")
     myroom.tags.add("dungeon#01")
     myscript.tags.add("weather", category="climate")
     myaccount.tags.add("guestaccount")

     mychair.tags.all()  # returns a list of Tags
     mychair.tags.remove("furniture") 
     mychair.tags.clear()    
```

新增的 tag 將建立新的 Tag 或重新使用已存在的Tag。請注意，有兩件「傢俱」tags，一件屬於 `None` 類別，一件屬於「豪華」類別。

使用 `remove` 時，`Tag` 不會被刪除，而只是與標記物件斷開連線。這使得操作非常快速。 `clear` 方法從物件中刪除（斷開）所有 Tags。


(tagproperty)=
### TagProperty

當您建立新類別時，這將用作屬性：

```python
from evennia import TagProperty 
from typeclasses import Object 

class MyClass(Object):
    mytag = TagProperty(tagcategory)
```

這將在資料庫中建立一個名為 `mytag` 和類別 `tagcategory` 的 Tag。您將能夠透過 `obj.mytag` 找到它，但更有用的是，您可以使用資料庫中正常的 Tag 搜尋方法找到它。

請注意，如果您要使用 `obj.tags.remove("mytag", "tagcategory")` 刪除此 tag，則下次造訪此屬性時，tag 將_重新新增_到物件中！

(tagcategoryproperty)=
### TagCategoryProperty

這是 `TagProperty` 的逆：

```python
from evennia import TagCategoryProperty 
from typeclasses import Object 

class MyClass(Object): 
    tagcategory = TagCategroyProperty(tagkey1, tagkey2)
```

上面的範例意味著您將有兩個 tags（`tagkey1` 和 `tagkey2`）分配給該物件，每個都有 `tagcategory` 類別。

請注意，與 `TagProperty` 的工作方式類似，如果您要從具有 `TagHandler`（`obj.tags.remove("tagkey1", "tagcategory")`）的物件中刪除這些 tags（`obj.tags.remove("tagkey1", "tagcategory")`），那麼這些 tags 將在下次造訪該屬性時自動_重新新增_。

但反之則不然：如果您要透過 `TagHandler` 將相同類別的新 tag 新增至物件，則此屬性將把它包含在傳回的 tags 清單中。

如果您想將屬性中的 tags 與資料庫中的“重新同步”，可以對其使用 `del` 操作 - 下次訪問該屬性時，它將僅顯示您在其中指定的預設鍵。它的工作原理如下：

```python
>>> obj.tagcategory 
["tagkey1", "tagkey2"]

# remove one of the default tags outside the property
>>> obj.tags.remove("tagkey1", "tagcategory")
>>> obj.tagcategory 
["tagkey1", "tagkey2"]   # missing tag is auto-created! 

# add a new tag from outside the property 
>>> obj.tags.add("tagkey3", "tagcategory")
>>> obj.tagcategory 
["tagkey1", "tagkey2", "tagkey3"]  # includes the new tag! 

# sync property with datbase 
>>> del obj.tagcategory 
>>> obj.tagcategory 
["tagkey1", "tagkey2"]   # property/database now in sync 
```

(properties-of-tags-and-aliases-and-permissions)=
## Tags 的屬性（以及別名和許可權）

Tags 是*獨特的*。這意味著只有一個 Tag 物件具有給定的鍵和類別。

```{important}
不指定類別（預設）會為 tag 提供 `None` 的類別，這也被視為唯一按鍵 + 類別組合。您不能使用 `TagCategoryProperty` 來設定 `None` 類別的 Tags，因為屬性名稱可能不是 `None`。為此，請使用`TagHandler`（或`TagProperty`）。

```
當Tags被分配給遊戲實體時，這些實體實際上共享相同的Tag。這意味著 Tags 不適合儲存有關單一物件的資訊 - 使用
[Attribute](./Attributes.md) 為此。 Tags 比屬性限制得多，但這也
使它們能夠非常快速地在資料庫中找到 - 這就是重點。

Tags 具有以下屬性，儲存在資料庫中：

- **key** - Tag 的名稱。這是尋找 Tag 時要搜尋的主要屬性。
- **類別** - 此類別僅允許擷取用於不同目的的 tags 的特定子集。例如，您可以將 tags 的一個類別用於“區域”，另一個類別用於“室外位置”。如果未給出，類別將為 `None`，這也被視為單獨的預設類別。
- **資料** - 這是一個可選文字欄位，其中包含有關 tag 的資訊。請記住，Tags 在實體之間共享，因此該欄位不能儲存任何特定於物件的資訊。通常，它將用於儲存有關 Tag 所標記的實體群組的資訊 - 可能用於上下文幫助，例如工具提示。預設不使用它。

還有兩個特殊屬性。這些通常不需要更改或設定，Evennia 在內部使用它來實現 `Tag` 物件的各種其他用途：

- **模型** - 這包含tag 處理的模型物件的*自然鍵* 描述，格式為*application.modelclass*，例如`objects.objectdb`。它被每種實體型別的 TagHandler 用於在幕後正確儲存資料。
- **tagtype** - 這是 Tags 的內建子級的“頂級類別”，即 *別名* 和 *許可權*。使用此特殊欄位的標記處理程式特別旨在釋放 *category* 屬性以供您想要的任何用途。

(aliases-and-permissions)=
## 別名和許可權

別名和許可權是使用正常的 TagHandlers 實現的，只需使用 a 即可節省 Tags
不同`tagtype`。這些處理程式在所有物件上都被命名為 `aliases` 和 `permissions`。他們是
使用方式與上面Tags相同：

```python
    boy.aliases.add("rascal")
    boy.permissions.add("Builders")
    boy.permissions.remove("Builders")

    all_aliases = boy.aliases.all()
```

等等。與 `tag` 在遊戲中的工作方式類似，還有用於分配許可權的 `perm` 指令和用於別名的 `@alias` 指令。