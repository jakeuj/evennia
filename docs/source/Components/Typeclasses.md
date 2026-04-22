(typeclasses)=
# Typeclasses

*Typeclasses*構成Evennia資料儲存的核心。它允許 Evennia 將任意數量的不同遊戲實體表示為 Python 類，而無需為每個新型別修改資料庫架構。

在Evennia中，最重要的遊戲實體，[帳戶](./Accounts.md)、[物件](./Objects.md)、[Scripts](./Scripts.md)和[頻道](./Channels.md)都是從`evennia.typeclasses.models.TypedObject`以不同距離繼承的Python類別。  在檔案中，我們將這些物件稱為「型別分類」甚至「typeclass」。

這是繼承在 Evennia 中找出 typeclasses 的方式：

```
                                  ┌───────────┐
                                  │TypedObject│
                                  └─────▲─────┘
               ┌───────────────┬────────┴──────┬────────────────┐
          ┌────┴────┐     ┌────┴───┐      ┌────┴────┐      ┌────┴───┐
1:        │AccountDB│     │ScriptDB│      │ChannelDB│      │ObjectDB│
          └────▲────┘     └────▲───┘      └────▲────┘      └────▲───┘
       ┌───────┴──────┐ ┌──────┴──────┐ ┌──────┴───────┐ ┌──────┴──────┐
2:     │DefaultAccount│ │DefaultScript│ │DefaultChannel│ │DefaultObject│
       └───────▲──────┘ └──────▲──────┘ └──────▲───────┘ └──────▲──────┘
               │               │               │                │  Evennia
       ────────┼───────────────┼───────────────┼────────────────┼─────────
               │               │               │                │  Gamedir
           ┌───┴───┐       ┌───┴──┐        ┌───┴───┐   ┌──────┐ │
3:         │Account│       │Script│        │Channel│   │Object├─┤
           └───────┘       └──────┘        └───────┘   └──────┘ │
                                                    ┌─────────┐ │
                                                    │Character├─┤
                                                    └─────────┘ │
                                                         ┌────┐ │
                                                         │Room├─┤
                                                         └────┘ │
                                                         ┌────┐ │
                                                         │Exit├─┘
                                                         └────┘
```

- 上面的**等級 1** 是「資料庫模型」等級。這描述了資料庫表和欄位（從技術上講，這是一個 [Django 模型](https://docs.djangoproject.com/en/4.1/topics/db/models/)）。
- **等級 2** 是我們在資料庫頂部找到 Evennia 各種遊戲實體的預設實現的地方。這些類別定義了Evennia在各種情況下呼叫的所有鉤子方法。 `DefaultObject` 有點特殊，因為它是 `DefaultCharacter`、`DefaultRoom` 和 `DefaultExit` 的父級。它們都被分組在等級 2 下，因為它們都代表建置的預設值。
- 最後，**第 3 級**包含在遊戲目錄中建立的空白模板類別。這是您應該根據需要修改和調整的級別，過載預設值以適合您的遊戲。模板直接從其預設值繼承，因此 `Object` 從 `DefaultObject` 繼承，`Room` 從 `DefaultRoom` 繼承。

> 此圖不包括 `Object`、`Character`、`Room` 和 `Exit` 的 `ObjectParent` mixin。這為這些類建立了一個共同的父類，用於共享屬性。有關詳細資訊，請參閱[物件](./Objects.md)。

`typeclass/list` 指令將提供Evennia 已知的所有typeclasses 的清單。這對於瞭解可用的內容很有用。但請注意，如果您新增一個包含類別的新模組，但不從任何地方匯入該模組，則 `typeclass/list` 將找不到它。為了讓 Evennia 知道它，您必須從某個地方匯入該模組。


(difference-between-typeclasses-and-classes)=
## typeclasses 和類別之間的差異

從上表中的類別繼承的所有 Evennia 類別都有一個重要的特性和兩個重要的限制。這就是為什麼我們不簡單地稱它們為「類」而是「typeclasses」。

 1. typeclass 可以將自身儲存到資料庫中。這意味著類別上的某些屬性（實際上不是很多）實際上代表資料庫欄位，並且只能儲存非常特定的資料型別。
 1. 由於它與資料庫的連線，typeclass' 名稱在整個伺服器名稱空間中必須是*唯一的*。也就是說，任何地方都不能定義兩個同名的類別。因此，下面的程式碼會給出錯誤（因為 `DefaultObject` 現在在此模組和預設庫中全域找到）：

    ```python
    from evennia import DefaultObject as BaseObject
    class DefaultObject(BaseObject):
         pass
    ```

 1. typeclass' `__init__` 方法通常不應過載。這主要與 `__init__` 方法沒有以可預測的方式呼叫有關。相反，Evennia 建議您使用 `at_*_creation` 掛鉤（如物件的 `at_object_creation`）在第一次將 typeclass 儲存到資料庫時進行設定，或每次將物件快取到記憶體時呼叫 `at_init` 掛鉤。如果您知道自己在做什麼並且想要使用 `__init__`，它*必須*既接受任意關鍵字引數並使用 `super` 呼叫其父級：
 
    ```python
    def __init__(self, **kwargs):
        # my content
        super().__init__(**kwargs)
        # my content
    ```

除此之外，typeclass 的工作方式與任何普通的 Python 類別一樣，您可以這樣對待它。

(working-with-typeclasses)=
## 與 typeclasses 一起工作

(creating-a-new-typeclass)=
### 創造一個新的typeclass

使用 Typeclasses 很容易工作。您可以使用現有的typeclass，也可以建立一個繼承現有typeclass 的新Python 類別。這是建立新型別物件的範例：
 
```python
    from evennia import DefaultObject

    class Furniture(DefaultObject):
        # this defines what 'furniture' is, like
        # storing who sits on it or something.
        pass

```

現在您可以透過兩種方式建立新的 `Furniture` 物件。  首先（通常不是最
方便）的方法是建立該類別的例項，然後手動將其儲存到資料庫中：

```python
chair = Furniture(db_key="Chair")
chair.save()

```

要使用此功能，您必須將資料庫欄位名稱作為呼叫的關鍵字。哪些可用取決於您要建立的實體，但全部以 Evennia 中的 `db_*` 開頭。如果您以前瞭解過 Django，那麼您可能會熟悉這種方法。

建議您改用 `create_*` 函式來建立型別分類實體：


```python
from evennia import create_object

chair = create_object(Furniture, key="Chair")
# or (if your typeclass is in a module furniture.py)
chair = create_object("furniture.Furniture", key="Chair")
```

`create_object`（`create_account`、`create_script` 等）將 typeclass 作為其第一個引數；這可以是實際的類，也可以是在遊戲目錄下找到的 typeclass 的 python 路徑。因此，如果您的 `Furniture` typeclass 位於 `mygame/typeclasses/furniture.py`，您可以將其指向 `typeclasses.furniture.Furniture`。由於 Evennia 本身會出現在 `mygame/typeclasses` 中，因此您可以進一步縮短為 `furniture.Furniture`。建立函式需要很多額外的關鍵字，允許您一次設定 [屬性](./Attributes.md) 和 [Tags](./Tags.md) 等內容。這些關鍵字不使用 `db_*` 字首。這也會自動將新執行個體儲存到資料庫，因此您不需要明確呼叫 `save()`。

資料庫欄位的範例是 `db_key`。它儲存您正在修改的實體的“名稱”，因此只能儲存一個字串。這是確保更新 `db_key` 的一種方法：

```python
chair.db_key = "Table"
chair.save()

print(chair.db_key)
<<< Table
```

也就是說，我們將椅子物件更改為具有`db_key`“桌子”，然後將其儲存到資料庫中。然而，你幾乎從來不會這樣做； Evennia 定義所有資料庫欄位的屬性包裝器。它們的命名與欄位相同，但沒有 `db_` 部分：

```python
chair.key = "Table"

print(chair.key)
<<< Table

```

`key` 包裝器不僅編寫起來更短，它還可以確保為您儲存該欄位，並且透過在後臺利用 sql 更新機制來更有效地完成此操作。因此，雖然最好知道該欄位名為 `db_key`，但您應該盡可能多地使用 `key`。

每個 typeclass 實體都有一些與該型別相關的唯一欄位。  但所有人也共享
以下欄位（給出不含 `db_` 的包裝器名稱）：

 - `key` (str)：實體的主要識別符號，例如「Rose」、「myscript」或「Paul」。 `name` 是別名。
 - `date_created` (datetime)：建立此物件時的時間戳記。
 - `typeclass_path` (str)：指向該（型別）類別位置的Python路徑

有一個特殊欄位不使用 `db_` 字首（它是由 Django 定義的）：

 - `id` (int): 物件的資料庫 ID (database ref)。這是一個不斷增加的唯一整數。它也可以作為`dbid`（資料庫ID）或`pk`（主鍵）進行存取。 `dbref` 屬性傳回字串形式「#id」。

型別分類實體有幾個常見的處理程式：

 - `tags` - 處理標記的 [TagHandler](./Tags.md)。使用 `tags.add()` 、 `tags.get()` 等。
 - `locks` - 管理存取限制的 [LockHandler](./Locks.md)。使用`locks.add()`、`locks.get()`等。
 - `attributes` - 管理物件屬性的 [AttributeHandler](./Attributes.md)。使用`attributes.add()`
ETC。
 - `db` (DataBase) - AttributeHandler 的捷徑屬性；允許`obj.db.attrname = value`
 - `nattributes` - 未儲存在屬性中的 [非持久 AttributeHandler](./Attributes.md)
資料庫.
 - `ndb` (NotDataBase) - 非持久 AttributeHandler 的捷徑屬性。允許`obj.ndb.attrname = value`


然後，每個型別分類的實體都會用自己的屬性擴充套件此列表。請前往[物件](./Objects.md)、[Scripts](./Scripts.md)、[帳號](./Accounts.md) 和[頻道](./Channels.md) 的對應頁面瞭解更多資訊。也建議您使用 [Evennia 的平面 API](../Evennia-API.md) 來探索可用實體，以探索它們具有哪些可用屬性和方法。

(overloading-hooks)=
### 超載吊鉤

自訂 typeclasses 的方法通常是在它們上過載 *hook 方法*。鉤子是Evennia在各種情況下呼叫的方法。一個範例是 `Objects` 上的 `at_object_creation` 掛鉤，僅在第一次將此物件儲存到資料庫時呼叫一次。  其他範例包括 Accounts 的 `at_login` 掛鉤和 Scripts 的 `at_repeat` 掛鉤。

(querying-for-typeclasses)=
### 查詢 typeclasses

大多數時候，您可以使用 [指令](./Commands.md) 的 `caller.search()` 等便捷方法或 `evennia.search_objects` 等搜尋功能來搜尋資料庫中的物件。

不過，您也可以直接使用[Django 的查詢語言](https://docs.djangoproject.com/en/4.1/topics/db/queries/) 來查詢它們。這利用了位於所有 typeclasses 上的_資料庫管理器_，名為 `objects`。此管理器擁有允許針對特定型別的物件進行資料庫搜尋的方法（這也是 Django 通常的工作方式）。使用 Django 查詢時，需要使用完整的欄位名稱（如 `db_key`）進行搜尋：

```python
matches = Furniture.objects.get(db_key="Chair")

```

重要的是，這將「僅」查詢直接從資料庫中的 `Furniture` 繼承的物件。如果 `Furniture` 有一個名為 `Sitables` 的子類，則使用此查詢將找不到任何從 `Sitables` 派生的椅子（這不是 Django 功能，而是 Evennia 所特有的）。若要從子類別 Evennia 尋找物件，請使用 `get_family` 和 `filter_family` 查詢方法：

```python
# search for all furnitures and subclasses of furnitures
# whose names starts with "Chair"
matches = Furniture.objects.filter_family(db_key__startswith="Chair")

```

為了確保搜尋，例如，所有 `Scripts` *不管* typeclass，您需要從資料庫模型本身進行查詢。因此對於物件來說，這將是上圖中的`ObjectDB`。以下是 Scripts 的範例：

```python
from evennia import ScriptDB
matches = ScriptDB.objects.filter(db_key__contains="Combat")
```

從資料庫模型父級查詢時，不需要使用 `filter_family` 或 `get_family` - 您將始終查詢資料庫模型上的所有子級。

(updating-existing-typeclass-instances)=
### 正在更新現有 typeclass 例項

如果您已經建立了 Typeclasses 的例項，則可以隨時修改 *Python 程式碼* - 由於 Python 繼承的工作原理，一旦您重新載入伺服器，您的變更將自動套用至所有子層級。然而，資料庫儲存的資料，如 `db_*` 欄位、[屬性](./Attributes.md)、[Tags](./Tags.md) 等，本身並未嵌入到類別中，且不會自動更新。您需要透過搜尋所有相關物件並更新或新增資料來自行管理：

```python
# add a worth Attribute to all existing Furniture
for obj in Furniture.objects.all():
    # this will loop over all Furniture instances
    obj.db.worth = 100
```

一個常見的用例是將所有屬性放入實體的 `at_*_creation` 掛鉤中，例如 `at_object_creation` 對應 `Objects`。每次建立物件時都會呼叫此方法 - 並且只有在那時。這通常是您想要的，但它確實意味著如果您稍後更改 `at_object_creation` 的內容，則現有物件將不會更新。您可以透過與上面類似的方式修復此問題（手動設定每個 Attribute）或使用類似以下內容：

```python
# Re-run at_object_creation only on those objects not having the new Attribute
for obj in Furniture.objects.all():
    if not obj.db.worth:
        obj.at_object_creation()
```

上面的範例可以在`evennia shell`建立的指令提示字元下執行。您還可以使用 `@py` 在遊戲中執行它。然而，這需要您使用 `;` 和 [列表推導式](http://www.secnetix.de/olli/Python/list_comprehensions.hawk) 將程式碼（包括匯入）作為一行，如下所示（忽略換行符，這只是為了 wiki 中的可讀性）：

```
py from typeclasses.furniture import Furniture;
[obj.at_object_creation() for obj in Furniture.objects.all() if not obj.db.worth]
```

建議您在開始建造之前正確規劃遊戲，以避免不必要地追溯更新物件。

(swap-typeclass)=
### 交換typeclass

如果您想交換已經存在的 typeclass，有兩種方法可以實現：從遊戲內和透過程式碼。在遊戲內部，您可以使用預設的 `@typeclass` 指令：

```
typeclass objname = path.to.new.typeclass
```

此指令有兩個重要的開關：
- `/reset` - 這將清除物件上的所有現有屬性並重新執行建立掛鉤（如物件的 `at_object_creation`）。這可以確保您獲得純粹屬於這個新類別的物件。
- `/force` - 如果您要將類別變更為物件已有的「相同」類，則這是必需的 - 這是避免使用者錯誤的安全檢查。這通常與 `/reset` 一起使用以在現有類別上重新執行建立掛鉤。

在程式碼中，您可以使用 `swap_typeclass` 方法，您可以在所有型別分類的實體上找到該方法：

```python
obj_to_change.swap_typeclass(new_typeclass_path, clean_attributes=False,
                   run_start_hooks="all", no_default=True, clean_cmdsets=False)
```

此方法的引數在[此處的 API 檔案中](github:evennia.typeclasses.models#typedobjectswap_typeclass) 中進行了描述。


(how-typeclasses-actually-work)=
## typeclasses 實際工作原理

*這被認為是高階部分。 *

從技術上講，typeclasses 是 [Django 代理模型](https://docs.djangoproject.com/en/4.1/topics/db/models/#proxy-models)。  typeclass 系統中唯一「真實」的資料庫模型（即由資料庫中的實際表表示）是 `AccountDB`、`ObjectDB`、`ScriptDB` 和 `ChannelDB`（還有 [屬性](./Attributes.md) 和 [Tags](./Tags.md)，但它們本身不是 typeclasses）。它們的所有子類別都是“代理”，用 Python 程式碼擴充套件它們，而無需實際修改資料庫佈局。

Evennia 以各種方式修改 Django 的代理模型，以允許它們在沒有任何樣板的情況下工作（例如，您不需要在模型 `Meta` 子類中設定 Django「代理」屬性，Evennia 使用元類為您處理此問題）。 Evennia 還確保您可以查詢子類別以及修補 Django 以允許從同一基底類別進行多重繼承。

(caveats)=
### 注意事項

Evennia 使用 *idmapper* 將其 typeclasses （Django 代理模型）快取在記憶體中。 idmapper 允許將物件處理程式和屬性等內容儲存在 typeclass 例項上，只要伺服器正在執行，就不會遺失（它們只會在伺服器重新載入時清除）。 Django 預設不是這樣運作的；預設情況下，每次在資料庫中搜尋物件時，您都會得到該物件的「不同」例項，並且儲存在該物件上的任何不在資料庫中的內容都會遺失。最重要的是，Evennia 的 Typeclass 例項在記憶體中的存在時間比普通 Django 模型例項長很多。

對此需要考慮一個警告，這與[製作自己的模型](New-
Models)有關：與typeclasses的外部關係由Django快取，這意味著如果您要透過該關係以外的其他方式更改外部關係中的物件，看到該關係的物件可能無法可靠地更新，但仍會看到其舊的快取版本。由於 typeclasses 在記憶體中保留了很長時間，此類關係的過時快取可能比 Django 中常見的快取更明顯。請參閱[已關閉的問題 #1098 及其評論](https://github.com/evennia/evennia/issues/1098) 以取得範例和解決方案。

(will-i-run-out-of-dbrefs)=
## 我會用完 dbrefs 嗎？

Evennia 不會重複使用其 `#dbrefs`。這表示即使您刪除舊物件，新對像也會持續增加 `#dbref`。這有技術和安全方面的原因。但您可能想知道這是否意味著您必須擔心大型遊戲最終會「耗盡」 dbref 整數。

答案很簡單：**不**。

例如，預設 sqlite3 資料庫的最大 dbref 值為 `2**64`。如果您*一年中的每一天、每一分鐘、每一秒都建立 10 000 個新物件，那麼您將需要大約 **6000 萬年**才能用完 dbref 數字*。這是一個 140TeraBytes 的資料庫，僅用於儲存 dbrefs，沒有其他資料。

如果此時您仍在使用 Evennia 並有此擔憂，請回覆我們，我們可以討論新增 dbref 重複使用。