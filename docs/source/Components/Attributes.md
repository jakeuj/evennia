(attributes)=
# 屬性

```{code-block}
:caption: In-game
> set obj/myattr = "test"
```
```{code-block} python
:caption: In-code, using the .db wrapper
obj.db.foo = [1, 2, 3, "bar"]
value = obj.db.foo
```
```{code-block} python
:caption: In-code, using the .attributes handler
obj.attributes.add("myattr", 1234, category="bar")
value = attributes.get("myattr", category="bar")
```
```{code-block} python
:caption: In-code, using `AttributeProperty` at class level
from evennia import DefaultObject
from evennia import AttributeProperty

class MyObject(DefaultObject):
    foo = AttributeProperty(default=[1, 2, 3, "bar"])
    myattr = AttributeProperty(100, category='bar')

```

_屬性_允許您在物件上儲存任意資料，並確保資料在伺服器重新啟動後仍然存在。 Attribute 可以儲存幾乎任何 Python 資料結構和資料型別，如數字、字串、列表、字典等。您也可以儲存（引用）資料庫物件，如字元和房間。

(working-with-attributes)=
## 使用屬性

屬性通常在程式碼中處理。所有[型別分類](./Typeclasses.md)實體（[帳戶](./Accounts.md)、[物件](./Objects.md)、[Scripts](./Scripts.md)和[通道](./Channels.md))可以（且通常）具有與其關聯的屬性。管理屬性有三種方法，所有這些方法都可以混合使用。

(using-db)=
### 使用.db

取得/設定屬性最簡單的方法是使用 `.db` 捷徑。這允許設定和獲取缺少_category_的屬性（具有類別`None`）

```python
import evennia

obj = evennia.create_object(key="Foo")

obj.db.foo1 = 1234
obj.db.foo2 = [1, 2, 3, 4]
obj.db.weapon = "sword"
obj.db.self_reference = obj   # stores a reference to the obj

# (let's assume a rose exists in-game)
rose = evennia.search_object(key="rose")[0]  # returns a list, grab 0th element
rose.db.has_thorns = True

# retrieving
val1 = obj.db.foo1
val2 = obj.db.foo2
weap = obj.db.weapon
myself = obj.db.self_reference  # retrieve reference from db, get object back

is_ouch = rose.db.has_thorns

# this will return None, not AttributeError!
not_found = obj.db.jiwjpowiwwerw

# returns all Attributes on the object
obj.db.all

# delete an Attribute
del obj.db.foo2
```
嘗試訪問不存在的 Attribute 永遠不會導致 `AttributeError`。相反，您將得到 `None` 返還。特殊的 `.db.all` 將傳回物件上所有屬性的清單。如果需要，您可以將其替換為您自己的 Attribute `all`，它將替換預設的 `all` 功能，直到您再次刪除它。

(using-attributes)=
### 使用.attributes

如果您想將 Attribute 分組到一個類別中，或者事先不知道 Attribute 的名稱，則可以使用 [AttributeHandler](evennia.typeclasses.attributes.AttributeHandler)，它在所有型別分類實體上可用作 `.attributes`。如果沒有額外的關鍵字，這與使用 `.db` 捷徑相同（`.db` 實際上在內部使用 `AttributeHandler`）：

```python
is_ouch = rose.attributes.get("has_thorns")

obj.attributes.add("helmet", "Knight's helmet")
helmet = obj.attributes.get("helmet")

# you can give space-separated Attribute-names (can't do that with .db)
obj.attributes.add("my game log", "long text about ...")
```

透過使用類別，您可以分隔同一物件上的同名屬性以幫助組織。

```python
# store (let's say we have gold_necklace and ringmail_armor from before)
obj.attributes.add("neck", gold_necklace, category="clothing")
obj.attributes.add("neck", ringmail_armor, category="armor")

# retrieve later - we'll get back gold_necklace and ringmail_armor
neck_clothing = obj.attributes.get("neck", category="clothing")
neck_armor = obj.attributes.get("neck", category="armor")
```

如果您不指定類別，Attribute 的 `category` 將是 `None`，因此也可以透過 `.db` 找到。 `None` 被視為自己的類別，因此您不會發現 `None`-類別屬性與具有類別的屬性混合在一起。

以下是`AttributeHandler`的方法。有關詳細資訊，請參閱 [AttributeHandler API](evennia.typeclasses.attributes.AttributeHandler)。

- `has(...)` - 檢查物件是否有帶有此鍵的 Attribute。這相當於執行 `obj.db.attrname`，只不過您還可以檢查特定的「類別」。
- `get(...)` - 這將檢索給定的 Attribute。如果未定義 Attribute（而不是「無」），您也可以提供要傳回的 `default` 值。透過向呼叫提供`accessing_object`，還可以確保在修改任何內容之前檢查許可權。當您訪問不存在的 `Attribute` 時，`raise_exception` kwarg 允許您提高 `AttributeError` 而不是返回 `None`。 `strattr` kwarg 告訴系統將 Attribute 儲存為原始字串而不是對其進行 pickle。雖然最佳化通常不應該使用，除非 Attribute 用於某些特定的、有限的目的。
- `add(...)` - 這會為物件新增新的 Attribute。可以在此處提供可選的 [lockstring](./Locks.md) 以限制將來的訪問，並且還可以檢查呼叫本身是否已鎖定。
- `remove(...)` - 刪除給定的Attribute。可以選擇在執行刪除之前檢查許可權。  - `clear(...)` - 從物件中刪除所有屬性。
- `all(category=None)` - 傳回附加到該物件的所有屬性（給定類別）。

範例：

```python
try:
  # raise error if Attribute foo does not exist
  val = obj.attributes.get("foo", raise_exception=True):
except AttributeError:
   # ...

# return default value if foo2 doesn't exist
val2 = obj.attributes.get("foo2", default=[1, 2, 3, "bar"])

# delete foo if it exists (will silently fail if unset, unless
# raise_exception is set)
obj.attributes.remove("foo")

# view all clothes on obj
all_clothes = obj.attributes.all(category="clothes")
```

(using-attributeproperty)=
### 使用AttributeProperty

設定 Attribute 的第三種方法是使用 `AttributeProperty`。這是在 typeclass 的_類別層級_上完成的，並允許您像 Django 資料庫欄位一樣對待屬性。與使用 `.db` 和 `.attributes` 不同，`AttributeProperty` 不能動態建立，您必須在類別程式碼中分配它。

```python
# mygame/typeclasses/characters.py

from evennia import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty

class Character(DefaultCharacter):

    strength = AttributeProperty(10, category='stat')
    constitution = AttributeProperty(11, category='stat')
    agility = AttributeProperty(12, category='stat')
    magic = AttributeProperty(13, category='stat')

    sleepy = AttributeProperty(False, autocreate=False)
    poisoned = AttributeProperty(False, autocreate=False)

    def at_object_creation(self):
      # ...
```

當建立該類別的新例項時，將使用給定的值和類別建立新的`Attributes`。

透過像這樣設定 `AttributeProperty`，人們可以像建立物件上的常規屬性一樣存取底層 `Attribute`：

```python
char = create_object(Character)

char.strength   # returns 10
char.agility = 15  # assign a new value (category remains 'stat')

char.db.magic  # returns None (wrong category)
char.attributes.get("agility", category="stat")  # returns 15

char.db.sleepy # returns None because autocreate=False (see below)

```

```{warning}
請小心，不要將 AttributeProperty 分配給類別中已存在的屬性和方法的名稱，例如“key”或“at_object_creation”。這可能會導致非常令人困惑的錯誤。
```

用於 `sleepy` 和 `poisoned` 的 `autocreate=False`（預設為 `True`）值得更詳細的解釋。當 `False` 時，_no_ Attribute 將為這些 AttributProperties 自動建立，除非它們是_明確_設定的。

不建立 Attribute 的優點是傳回給 `AttributeProperty` 的預設值，除非您變更它，否則不會存取資料庫。這也意味著，如果您想稍後更改預設值，則先前建立的所有實體都將繼承新的預設值。

缺點是，如果沒有資料庫前置，您無法透過 `.db` 和 `.attributes.get` 找到 Attribute （或透過在資料庫中以其他方式查詢它）：

```python
char.sleepy   # returns False, no db access

char.db.sleepy   # returns None - no Attribute exists
char.attributes.get("sleepy")  # returns None too

char.sleepy = True  # now an Attribute is created
char.db.sleepy   # now returns True!
char.attributes.get("sleepy")  # now returns True

char.sleepy  # now returns True, involves db access
```

你可以e.g。 `del char.strength` 將值設定回預設值（`AttributeProperty` 中定義的值）。

有關如何使用特殊選項（例如提供訪問限制）建立它的更多詳細資訊，請參閱 [AttributeProperty API](evennia.typeclasses.attributes.AttributeProperty)。

```{warning}
雖然 `AttributeProperty` 在幕後使用了 `AttributeHandler` (`.attributes`)，但反之則不然。 `AttributeProperty` 有輔助方法，如 `at_get` 和 `at_set`。如果您使用該屬性存取 Attribute，這些將_僅_被呼叫。

也就是說，如果您執行`obj.yourattribute = 1`，則會呼叫`AttributeProperty.at_set`。但是在執行`obj.db.yourattribute = 1`時，會導致儲存相同的Attribute，這是「繞過」`AttributeProperty`並直接使用`AttributeHandler`。因此在這種情況下 `AttributeProperty.at_set` 將_不會_被呼叫。如果您在 `at_get` 中新增了一些特殊功能，這可能會令人困惑。

為了避免混淆，您應該在存取屬性方面保持一致 - 如果您使用 `AttributeProperty` 來定義它，稍後也可以使用它來存取和修改 Attribute。
```


(properties-of-attributes)=
### 屬性的特性

`Attribute` 物件儲存在資料庫中。它具有以下屬性：

- `key` - Attribute 的名稱。當做e.g時。 `obj.db.attrname = value`，此屬性設定為 `attrname`。
- `value` - 這是Attribute 的值。該值可以是任何可以醃製的內容 - 物件、列表、數字或您擁有的任何內容（有關詳細資訊，請參閱[本節](./Attributes.md#what-types-of-data-can-i-save-in-an-attribute)）。在範例中
`obj.db.attrname = value`，`value` 儲存在這裡。
- `category` - 這是一個可選屬性，對於大多數屬性設定為“無”。設定此項允許使用屬性來實現不同的功能。這通常是不需要的，除非您想將屬性用於非常不同的功能（[Nicks](./Nicks.md) 是使用的範例
屬性以這種方式）。要修改此屬性，您需要使用 [Attribute 處理程式](#attributes)
- `strvalue` - 這是一個單獨的值欄位，僅接受字串。這嚴重限制了可儲存的資料，但允許更輕鬆的資料庫查詢。通常不使用此屬性，除非出於其他目的而重新使用屬性（[Nicks](./Nicks.md) 使用它）。它只能透過 [Attribute 處理程式](#attributes) 存取。

還有兩個特殊屬性：

- `attrtype` - Evennia 在內部使用它來將 [Nicks](./Nicks.md) 與屬性分開（Nicks 在幕後使用屬性）。
- `model` - 這是一個*自然鍵*，描述了 Attribute 所附加到的模型。其格式為 *appname.modelclass*，如 `objects.objectdb`。 Attribute 和 NickHandler 使用它來快速對資料庫中的匹配項進行排序。  通常不需要修改此值或 `attrtype`。

非資料庫屬性不儲存在資料庫中，且不等於`category`、`strvalue`、`attrtype` 或`model`。


(managing-attributes-in-game)=
### 管理遊戲中的屬性

屬性主要由程式碼使用。但也可以允許建造者使用屬性在遊戲中「轉動旋鈕」。例如，建造者可能想要手動調整敵人 NPC 的「等級」Attribute 以降低其難度。

以這種方式設定屬性時，可以儲存的內容會受到嚴重限制 - 這是因為讓玩家（甚至建構者）能夠儲存任意 Python 將是一個嚴重的安全問題。

在遊戲中你可以像這樣設定Attribute：

    set myobj/foo = "bar"

若要檢視，請執行以下操作

    set myobj/foo

或將它們與所有物件資訊一起檢視

    examine myobj

第一個 `set`-範例將在物件 `myobj` 上儲存新的 Attribute `foo` 並為其賦予值「bar」。您可以透過這種方式儲存數字、布林值、字串、元組、列表和字典。但是，如果您儲存清單/元組/字典，它們必須是正確的 Python 結構，並且可能_僅_包含字串
或數字。如果您嘗試插入不支援的結構，輸入將轉換為
字串。

    set myobj/mybool = True
    set myobj/mybool = True
    set myobj/mytuple = (1, 2, 3, "foo")
    set myobj/mylist = ["foo", "bar", 2]
    set myobj/mydict = {"a": 1, "b": 2, 3: 4}
    set mypobj/mystring = [1, 2, foo]   # foo is invalid Python (no quotes)

對於最後一行，您將收到警告，並且該值將被儲存為字串 `"[1, 2, foo]"`。

(locking-and-checking-attributes)=
### 鎖定和檢查屬性

雖然 `set` 指令僅限於建置者，但單一屬性通常不會被鎖定。您可能需要lock某些敏感屬性，特別是對於允許玩家建造的遊戲。您可以透過將 [lock 字串](./Locks.md) 新增至 Attribute 來新增此類限制。 A NAttribute 沒有鎖。

相關的 lock 型別是

- `attrread` - 限制誰可以讀取 Attribute 的值
- `attredit` - 限制誰可以設定/更改此Attribute

您必須使用 `AttributeHandler` 將鎖定字串分配給 Attribute：

```python
lockstring = "attread:all();attredit:perm(Admins)"
obj.attributes.add("myattr", "bar", lockstring=lockstring)"
```

如果您已經有 Attribute 並想要就地新增 lock，您可以透過讓 `AttributeHandler` 返回 `Attribute` 物件本身（而不是其值），然後直接將 lock 分配給它來實現：

```python
     lockstring = "attread:all();attredit:perm(Admins)"
     obj.attributes.get("myattr", return_obj=True).locks.add(lockstring)
```

請注意 `return_obj` 關鍵字，它確保返回 `Attribute` 物件，以便可以存取其 LockHandler。

如果沒有任何東西檢查它，lock 是沒有用的——並且預設情況下 Evennia 不檢查屬性上的鎖。要檢查您提供的 `lockstring`，請確保在進行 `get` 呼叫時包含 `accessing_obj` 並設定 `default_access=False`。

```python
    # in some command code where we want to limit
    # setting of a given attribute name on an object
    attr = obj.attributes.get(attrname,
                              return_obj=True,
                              accessing_obj=caller,
                              default=None,
                              default_access=False)
    if not attr:
        caller.msg("You cannot edit that Attribute!")
        return
    # edit the Attribute here
```

相同的關鍵字可與 `obj.attributes.set()` 和 `obj.attributes.remove()` 一起使用，它們將檢查 `attredit` lock 型別。

(querying-by-attribute)=
## 按Attribute查詢

雖然您可以使用 `obj.attributes.get` 處理程式來取得屬性，但您也可以透過每個型別分類實體上可用的 `db_attributes` 多對多欄位根據物件具有的屬性來尋找物件：

```python
# find objects by attribue assigned (regardless of value)
objs = evennia.ObjectDB.objects.filter(db_attributes__db_key="foo")
# find objects with attribute of particular value assigned to them
objs = evennia.ObjectDB.objects.filter(db_attributes__db_key="foo", db_attributes__db_value="bar")
```

```{important}
在內部，Attribute 值儲存為_pickled strings_（請參閱下一節）。查詢時，您的搜尋字串將轉換為相同的格式並以該形式進行比對。雖然這意味著屬性可以儲存任意 Python 結構，但缺點是您無法對它們進行更高階的資料庫比較。例如，執行 `db_attributes__db__value__lt=4` 或 `__gt=0` 將不起作用，因為小於和大於不會在字串之間執行您想要的操作。
```

(what-types-of-data-can-i-save-in-an-attribute)=
## Attribute 中可以儲存哪些型別的資料？

資料庫對 Python 物件一無所知，因此 Evennia 必須將 Attribute 值序列化為字串表示形式，然後再儲存到資料庫中。這是使用 Python 的 [pickle](https://docs.python.org/library/pickle.html) 模組完成的。

> 唯一的例外是，如果您使用 `AttributeHandler` 的 `strattr` 關鍵字儲存到 Attribute 的 `strvalue` 欄位。在這種情況下，您可以_僅_儲存*字串*，並且這些字串不會被醃製）。

(storing-single-objects)=
### 儲存單一物件

對於單一物件，我們指的是任何「不可迭代」的東西，例如數字、字串或不帶 `__iter__` 方法的自訂類別例項。

* 您通常可以儲存任何可以_pickled_的不可迭代的Python實體。
* 可以儲存單一資料庫物件/typeclasses，儘管它們通常無法進行pickle。 Evennia 將使用類別名稱、資料庫 ID 和建立日期以微秒精度將它們轉換為內部表示形式。檢索時，將使用此資訊從資料庫重新取得物件例項。
* 如果您將 db-obj 作為自訂類別的屬性“隱藏”，Evennia 將無法找到它來序列化它。為此，您需要提供協助（請參閱下文）。

```{code-block} python
:caption: Valid assignments

# Examples of valid single-value  attribute data:
obj.db.test1 = 23
obj.db.test1 = False
# a database object (will be stored as an internal representation)
obj.db.test2 = myobj
```

如前所述，Evennia 將無法自動序列化物件上任意屬性中「隱藏」的資料庫物件。這將導致儲存Attribute時出錯。

```{code-block} python
:caption: Invalid, 'hidden' dbobject
# example of storing an invalid, "hidden" dbobject in Attribute
class Container:
    def __init__(self, mydbobj):
        # no way for Evennia to know this is a database object!
        self.mydbobj = mydbobj

# let's assume myobj is a db-object
container = Container(myobj)
obj.db.mydata = container  # will raise error!

```

透過為要儲存的物件新增兩個方法 `__serialize_dbobjs__` 和 `__deserialize_dbobjs__` ，您可以在 Evennia 的主序列化程式開始工作之前對所有「隱藏」物件進行預序列化和後反序列化。在這些方法中，使用 Evennia 的 [evennia.utils.dbserialize.dbserialize](evennia.utils.dbserialize.dbserialize) 和 [dbunserialize](evennia.utils.dbserialize.dbunserialize) 函式來安全地序列化要儲存的資料庫物件。

```{code-block} python
:caption: Fixing an invalid 'hidden' dbobj for storing in Attribute

from evennia.utils import dbserialize  # important

class Container:
    def __init__(self, mydbobj):
        # A 'hidden' db-object
        self.mydbobj = mydbobj

    def __serialize_dbobjs__(self):
        """This is called before serialization and allows
        us to custom-handle those 'hidden' dbobjs"""
        self.mydbobj = dbserialize.dbserialize(self.mydbobj

    def __deserialize_dbobjs__(self):
        """This is called after deserialization and allows you to
        restore the 'hidden' dbobjs you serialized before"""
        if isinstance(self.mydbobj, bytes):
            # make sure to check if it's bytes before trying dbunserialize
            self.mydbobj = dbserialize.dbunserialize(self.mydbobj)

# let's assume myobj is a db-object
container = Container(myobj)
obj.db.mydata = container  # will now work fine!
```

> 請注意 `__deserialize_dbobjs__` 中的額外檢查，以確保您要反序列化的物件是 `bytes` 物件。這是必要的，因為在某些情況下，當資料已經反序列化一次時，Attribute 的快取會重新執行反序列化。如果您在日誌中看到錯誤，顯示`Could not unpickle data for storage:...`，原因可能是您忘記新增此檢查。


(storing-multiple-objects)=
### 儲存多個物件

這意味著將物件儲存在某種型別的集合中，並且是 *iterables* 的範例，可以在 for 迴圈中迴圈的可pickle 實體。 Attribute- saving 支援以下迭代：

* [元組](https://docs.python.org/3/library/functions.html#tuple)，如`(1,2,"test", <dbobj>)`。
* [列表](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)，例如`[1,2,"test", <dbobj>]`。
* [字典](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)，例如`{1:2, "test":<dbobj>]`。
* [集](https://docs.python.org/2/tutorial/datastructures.html#sets)，如`{1,2,"test",<dbobj>}`。
* [收藏。 OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict),
比如`OrderedDict((1,2), ("test", <dbobj>))`。
* [collections.Deque](https://docs.python.org/3/library/collections.html#collections.deque)，如`deque((1,2,"test",<dbobj>))`。
* [收藏。 DefaultDict](https://docs.python.org/3/library/collections.html#collections.defaultdict) 就像`defaultdict(list)`。
* 上述任意組合的*巢狀*，例如字典中的列表或 OrderedDict 元組，每個都包含字典等。
* 所有其他可迭代物件（i.e。具有 `__iter__` 方法的實體）將轉換為*列表*。由於您可以使用上述迭代的任意組合，因此這通常不是太大的限制。

上面的[單一物件](./Attributes.md#storing-single-objects)部分中列出的任何實體都可以儲存在可迭代物件中。

> 如上一節所述，資料庫實體（又稱 typeclasses）無法進行 pickle。因此，在儲存可迭代物件時，Evennia 必須遞迴遍歷可迭代物件*及其所有巢狀的子可迭代物件*，以便找到最終要轉換的資料庫物件。這是一個非常快速的過程，但為了提高效率，您可能希望盡可能避免巢狀太深的結構。

```python
# examples of valid iterables to store
obj.db.test3 = [obj1, 45, obj2, 67]
# a dictionary
obj.db.test4 = {'str':34, 'dex':56, 'agi':22, 'int':77}
# a mixed dictionary/list
obj.db.test5 = {'members': [obj1,obj2,obj3], 'enemies':[obj4,obj5]}
# a tuple with a list in it
obj.db.test6 = (1, 3, 4, 8, ["test", "test2"], 9)
# a set
obj.db.test7 = set([1, 2, 3, 4, 5])
# in-situ manipulation
obj.db.test8 = [1, 2, {"test":1}]
obj.db.test8[0] = 4
obj.db.test8[2]["test"] = 5
# test8 is now [4,2,{"test":5}]
```

請注意，如果建立一些高階可迭代物件，並以某種方式儲存資料庫物件，使其不會透過迭代返回，那麼您就建立了一個「隱藏」資料庫物件。請參閱[上一節](#storing-single-objects) 以瞭解如何告訴 Evennia 如何安全地序列化此類隱藏物件。


(retrieving-mutable-objects)=
### 檢索可變物件

Evennia 儲存屬性的方式的一個副作用是 *mutable* 可迭代物件（可在建立後就地修改的可迭代物件，除了元組之外的所有內容）由稱為 `_SaverList`、`_SaverDict` 等的自訂物件處理。這些 `_Saver...` 類別的行為就像正常變體一樣，只是它們知道資料庫並在分配新資料時儲存到資料庫。這允許您執行 `self.db.mylist[7] = val` 之類的操作，並確保儲存新版本的清單。如果沒有這個，您必須將清單載入到臨時變數中，更改它，然後將其重新分配給 Attribute 才能儲存。

然而，有一件重要的事情要記住。如果將可變迭代檢索到另一個變數中，e.g。 `mylist2 = obj.db.mylist`，您的新變數 (`mylist2`) *仍然*是 `_SaverList`。這意味著每當更新時它都會繼續將自身儲存到資料庫中！

```python
obj.db.mylist = [1, 2, 3, 4]
mylist = obj.db.mylist

mylist[3] = 5  # this will also update database

print(mylist)  # this is now [1, 2, 3, 5]
print(obj.db.mylist)  # now also [1, 2, 3, 5]
```

當您將可變的 Attribute 資料提取到像 `mylist` 這樣的變數中時，可以將其視為獲取該變數的_快照_。如果您更新快照，它將儲存到資料庫，但此變更_不會傳播到您之前可能已完成的任何其他快照_。

```python
obj.db.mylist = [1, 2, 3, 4]
mylist1 = obj.db.mylist
mylist2 = obj.db.mylist
mylist1[3] = 5

print(mylist1)  # this is now [1, 2, 3, 5]
print(obj.db.mylist)  # also updated to [1, 2, 3, 5]

print(mylist2)  # still [1, 2, 3, 4]  !

```

```{sidebar}
請記住，本節的複雜性僅與*可變*迭代相關 - 您可以更新的東西
就地，如列表和字典。 [不可變](https://en.wikipedia.org/wiki/Immutable) 物件（字串、
數字、元組等）從一開始就已經與資料庫斷開連線。
```

為了避免與可變屬性混淆，一次僅使用一個變數（快照）並根據需要儲存結果。

您還可以選擇完全“斷開”Attribute 與
藉助 `.deserialize()` 方法的資料庫：

```python
obj.db.mylist = [1, 2, 3, 4, {1: 2}]
mylist = obj.db.mylist.deserialize()
```

此操作的結果將是僅由普通 Python 可變變陣列成的結構（`list` 而不是 `_SaverList`，`dict` 而不是 `_SaverDict` 等等）。如果更新，則需要明確將其儲存回Attribute才能儲存。


(in-memory-attributes-nattributes)=
## 記憶體中屬性 (NAttributes)

_NAttributes_（非資料庫屬性的縮寫）在大多數事物中模仿屬性，除了它們
**非永續性** - 它們不會在伺服器重新載入後倖存下來。

- 使用 `.ndb` 而不是 `.db`。
- 使用 `.nattributes` 代替 `.attributes`
- 使用 `NAttributeProperty`，而不是 `AttributeProperty`。

```python
    rose.ndb.has_thorns = True
    is_ouch = rose.ndb.has_thorns

    rose.nattributes.add("has_thorns", True)
    is_ouch = rose.nattributes.get("has_thorns")
```

`Attributes` 和 `NAttributes` 之間的差異：

- `NAttribute`s 總是在伺服器重新載入時被擦除。
- 它們只存在於記憶體中，根本不涉及資料庫，這使得它們可以更快地被呼叫。
訪問和編輯次數超過 `Attribute`s。
- `NAttribute`s 可以無限制地儲存_any_ Python 結構（和資料庫物件）。但是，如果您要_刪除_之前儲存在 `NAttribute` 中的資料庫物件，`NAttribute` 將不知道這一點，並且可能會為您提供一個沒有匹配資料庫條目的 python 物件。相比之下，`Attribute` 總是檢查這一點）。如果這是一個問題，請在儲存之前使用 `Attribute` 或檢查物件的 `.pk` 屬性不是 `None`。
- 它們_不能_使用標準 `set` 指令設定（但使用 `examine` 可見）

我們建議使用 `ndb` 來儲存臨時資料，而不是直接在物件上儲存變數的簡單替代方案，有一些重要原因：
[]()
- NAttributes 由 Evennia 跟蹤，並且不會在伺服器可能執行的各種快取清理操作中被清除。因此，使用它們可以保證它們至少在伺服器存在期間保持可用。
- 這是一種一致的風格 - `.db/.attributes` 和 `.ndb/.nattributes` 使得程式碼看起來很乾淨，很清楚你的資料的壽命（或壽命）有多長。

(persistent-vs-non-persistent)=
### 永續性與非永續性

因此，*持久*資料意味著您的資料將在伺服器重新啟動後繼續存在，而
*非永續性*資料不會...

……那麼您為什麼要使用非永續性資料呢？答案是，你不必這樣做。大部分
您真正想盡可能節省的時間。非永續性資料可能
但在某些情況下很有用。

- 您擔心資料庫效能。由於 Evennia 非常積極地快取屬性，因此這不是問題，除非您非常頻繁地讀取*和*寫入您的 Attribute（例如每秒多次）。從已快取的 Attribute 讀取與讀取任何 Python 屬性一樣快。但即便如此，這也不太可能是值得擔心的：除了 Evennia 自己的快取之外，現代資料庫系統本身也非常有效地快取資料以提高速度。如果可能的話，我們的預設資料庫甚至完全在 RAM 中執行，從而減輕了在重負載期間寫入磁碟的大部分需求。
- 使用非永續性資料的一個更有效的原因是您「希望」在登出時遺失狀態。也許您正在儲存伺服器啟動時重新初始化的廢棄資料。也許您正在實施一些自己的快取。或者您可能正在測試一個錯誤 [Script](./Scripts.md)，它會對您的角色物件執行潛在有害的操作。使用非持久儲存，您可以確保無論出現什麼問題，伺服器重新啟動都可以解決。
- `NAttribute`s 對它們可以儲存的內容沒有任何限制，因為它們不需要擔心被儲存到資料庫中 - 它們非常適合臨時儲存。
- 您想要實現一個完全或部分*非持久世界*。我們有什麼資格去爭論你的宏偉願景！
