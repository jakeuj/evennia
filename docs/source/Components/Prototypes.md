(spawner-and-prototypes)=
# 生成器和原型

```shell
> spawn goblin

Spawned Goblin Grunt(#45)
```

*spawner* 是一個用於從稱為「原型」的基本模板定義和建立單個物件的系統。它僅設計用於遊戲中的[物件](./Objects.md)，而不是任何其他型別的實體。

在 Evennia 中建立自訂物件的正常方法是建立 [Typeclass](./Typeclasses.md)。如果您還沒有閱讀 Typeclasses ，請將它們視為在背景儲存到資料庫的普通 Python 類別。假設您想建立一個“妖精”敵人。常見的方法是先建立一個 `Mobile` typeclass，其中包含遊戲中行動裝置常見的所有內容，例如通用 AI、戰鬥程式碼和各種行動方法。然後，`Goblin` 子類別將從 `Mobile` 繼承。 `Goblin` 類別新增了妖精獨有的東西，例如基於群體的 AI（因為妖精在群體中更聰明）、驚慌失措的能力、挖掘黃金等。

但現在是時候真正開始創造一些妖精並將它們放入世界中了。如果我們希望這些妖精看起來不一樣呢？也許我們想要灰皮膚和綠皮膚的妖精，或者一些可以施法或使用不同武器的妖精？我們*可以*建立`Goblin`的子類，例如`GreySkinnedGoblin`和`GoblinWieldingClub`。但這似乎有點過分（而且每件小事都有大量的 Python 程式碼）。當想要組合類別時，使用類別也可能變得不切實際——如果我們想要一個揮舞著長矛的灰皮膚妖精薩滿怎麼辦——建立一個透過多重繼承相互繼承的類別網路可能會很棘手。

這就是*原型*的用途。它是一個 Python 字典，描述了物件的這些每個例項的變更。該原型還具有允許遊戲內建構者自訂物件而無需存取 Python 後端的優點。 Evennia 還允許儲存和搜尋原型，以便其他建構者稍後可以找到和使用（和調整）它們。擁有有趣的原型庫對於建構者來說是一個很好的資源。 OLC 系統允許使用選單系統建立、儲存、載入和操作原型。

*spawner* 採用原型並使用它來建立（產生）新的自訂物件。

(working-with-prototypes)=
## 使用原型

(using-the-olc)=
### 使用OLC

輸入`olc`指令或`spawn/olc`進入原型精靈。這是一個用於建立、載入、儲存和操作原型的選單系統。它旨在供遊戲內構建者使用，並且總體上可以更好地理解原型。在選單的每個節點上使用 `help` 以獲取更多資訊。以下是有關原型如何運作及其使用方式的更多詳細資訊。

(the-prototype)=
### 原型機

原型字典可以由OLC為您建立（見上文），在Python模組中手動編寫（然後由`spawn`指令/OLC引用），或者即時建立並手動載入到spawner函式或`spawn`指令中。

該字典定義了物件的所有可能的資料庫屬性。它有一組固定的允許鍵。當準備將原型儲存在資料庫中時（或使用OLC時），其中一些鍵是必需的。當僅將一次性原型字典傳遞給生成器時，系統更加寬鬆，並且將使用未明確提供的鍵的預設值。

在字典形式中，原型可以如下所示：

```python
{
   "prototype_key": "house"
   "key": "Large house"
   "typeclass": "typeclasses.rooms.house.House"
 }
```
如果您想將其載入到遊戲中的生成器中，您可以將所有內容放在一行上：

    spawn {"prototype_key"="house", "key": "Large house", ...}

> 請注意，指令列上給出的原型字典必須是有效的 Python 結構 - 因此您需要在字串等處加上引號。出於安全原因，從遊戲內插入的字典不能具有任何其他高階 Python 功能，例如可執行程式碼、`lambda` 等。如果建構器應該能夠使用此類功能，您需要透過 [$protfuncs](Spawner-and- Prototypes#protfuncs) 提供它們，嵌入式可執行函式您可以完全控制在執行之前進行檢查和審查。

(prototype-keys)=
### 原型鑰匙

所有以`prototype_`開頭的鍵都是用來記帳的。

 - `prototype_key` - 原型的“名稱”，用於引用原型
    when spawning and inheritance. If defining a prototype in a module and this
    not set, it will be auto-set to the name of the prototype's variable in the module.
 - `prototype_parent` - 如果給出，這應該是系統中儲存或模組中可用的另一個原型的 `prototype_key`。這使得這個原型*繼承*來自
    parent and only override what is needed. Give a tuple `(parent1, parent2, ...)` for multiple left-right inheritance. If this is not given, a `typeclass` should usually be defined (below).
 - `prototype_desc` - 這是可選的，在遊戲內列表中列出原型時使用。
 - `protototype_tags` - 這是可選的，允許標記原型以便找到它
稍後會更容易。
 - `prototype_locks` - 支援兩種 lock 型別：`edit` 和 `spawn`。第一個lock限制透過OLC載入時原型的複製和編輯。第二個決定誰可以使用原型來建立新物件。


其餘的鍵確定從此原型生成的物件的實際方面：

 - `key` - 主要物件識別碼。預設為“產生的物件 *X*”，其中 *X* 是隨機整數。
 - `typeclass` - 到你想要使用的 typeclass 的完整 python 路徑（從你的遊戲目錄）。如果未設定，則應定義 `prototype_parent`，並在父鏈中的某處定義 `typeclass`。當建立一個僅用於生成的一次性原型字典時，可以忽略這一點 - 將使用 `settings.BASE_OBJECT_TYPECLASS` 代替。
 - `location` - 這應該是 `#dbref`。
 - `home` - 有效的 `#dbref`。如果位置不存在，則預設為 `location` 或 `settings.DEFAULT_HOME`。
 - `destination` - 有效的 `#dbref`。僅供出口使用。
 - `permissions` - 許可權字串列表，例如 `["Accounts", "may_use_red_door"]`
 - `locks` - [lock-字串](./Locks.md) 就像 `"edit:all();control:perm(Builder)"`
 - `aliases` - 用作別名的字串列表
 - `tags` - 列出 [Tags](./Tags.md)。這些以元組 `(tag, category, data)` 的形式給出。
 - `attrs` - [屬性]列表(./Attributes.md)。這些以元組形式給出 `(attrname, value, category, lockstring)`
 - 任何其他關鍵字都被解釋為非類別[屬性](./Attributes.md) 及其值。這對於簡單屬性來說很方便 - 使用 `attrs` 來完全控制屬性。

(more-on-prototype-inheritance)=
#### 有關原型繼承的更多資訊

- 原型可以透過定義指向名稱（另一個原型的`prototype_key`）的`prototype_parent`來繼承。如果清單為 `prototype_keys`，則將從左到右逐步執行，優先考慮清單中的第一個而不是後面出現的清單。也就是說，如果您的繼承是 `prototype_parent = ('A', 'B,' 'C')`，並且所有父級都包含衝突鍵，則 `A` 中的繼承將適用。
- 以 `prototype_*` 開頭的原型鍵對於每個原型都是唯一的。它們永遠不會從父母遺傳給孩子。
- 原型欄位 `'attr': [(key, value, category, lockstring),...]` 和 `'tags': [(key, category, data),...]` 以_complementary_ 方式繼承。這意味著只有衝突的鍵+類別匹配才會被替換，而不是整個列表。請記住，類別 `None` 也被視為有效類別！
- 新增 Attribute 作為簡單的 `key:value` 將在底層轉換為 Attribute 元組 `(key, value, None, '')`，並且如果它具有相同的鍵和 `None` 類別，則可以替換父級中的 Attribute。
- 所有其他鍵（`permissions`、`destination`、`aliases` 等）將完全被子項的值（如果給定）_替換_。為了保留父級的值，子級根本不能定義這些鍵。

(prototype-values)=
### 原型值

此原型支援多種不同型別的值。

它可以是一個硬編碼值：

```python
    {"key": "An ugly goblin", ...}

```

它也可以是*可呼叫*。每當使用原型產生新物件時，都會不帶引數地呼叫此可呼叫物件：

```python
    {"key": _get_a_random_goblin_name, ...}

```

透過使用 Python `lambda` 可以包裝可呼叫物件，以便在原型中立即進行設定：

```python
    {"key": lambda: random.choice(("Urfgar", "Rick the smelly", "Blargh the foul", ...)), ...}

```

(protfuncs)=
#### 產品功能

最後，該值可以是*原型函式* (*Protfunc*)。這些看起來像是嵌入在字串中的簡單函式呼叫，並且前面有一個 `$`，例如

```python
    {"key": "$choice(Urfgar, Rick the smelly, Blargh the foul)",
     "attrs": {"desc": "This is a large $red(and very red) demon. "
                       "He has $randint(2,5) skulls in a chain around his neck."}
```

> 如果要轉義 protfunc 並使其逐字顯示，請使用 `$$funcname()`。

在產生時，protfunc 的位置將會被呼叫該 protfunc 的結果取代（這總是一個字串）。 protfunc 是每次使用原型產生新物件時執行的 [FuncParser 函式](./FuncParser.md)。請參閱 FuncParse 以瞭解更多資訊。

以下是 protfunc 的定義方式（與其他 funcparser 函式相同）。

```python
# this is a silly example, you can just color the text red with |r directly!
def red(*args, **kwargs):
   """
   Usage: $red(<text>)
   Returns the same text you entered, but red.
   """
   if not args or len(args) > 1:
      raise ValueError("Must have one argument, the text to color red!")
   return f"|r{args[0]}|n"
```

> 請注意，我們必須確保驗證輸入並在失敗時引發 `ValueError`。

解析器將始終包含以下保留的`kwargs`：
- `session` - 目前執行產生的 [Session](evennia.server.ServerSession)。
- `prototype` - 函式所屬的原型字典。這是_唯讀_使用的。從函式內部修改這樣的可變結構時要小心—這可能會導致很難發現的錯誤。
- `current_key` - 執行此 protfunc 的 `prototype` 字典的目前鍵。

要讓這個 protfunc 可供遊戲中的建構者使用，請將其新增至新模組並將該模組的路徑新增至 `settings.PROT_FUNC_MODULES`：

```python
# in mygame/server/conf/settings.py

PROT_FUNC_MODULES += ["world.myprotfuncs"]

```
您新增的模組中的所有*全域可呼叫物件*都將被視為新的 protfunc。為了避免這種情況（e.g。擁有本身不是 protfuncs 的輔助函式），請將函式命名為以 `_` 開頭的名稱。

開箱即用的預設 protfunc 在 `evennia/prototypes/profuncs.py` 中定義。要覆寫可用的函式，只需在您自己的 protfunc 模組中新增同名函式即可。

| 普羅特函式 | 描述 |
| --- | --- |
| `$random()` | 傳回 `[0, 1)` 範圍內的隨機值 |
|  `$randint(start, end)` |  傳回範圍 [start, end] 內的隨機值  |
| `$left_justify(<text>)` | 左對齊文字 |
|  `$right_justify(<text>)` | 將文字右對齊到螢幕寬度 |
|  `$center_justify(<text>)` | 將文字置中對齊到螢幕寬度 |
|  `$full_justify(<text>)` | 透過新增空格將文字分散到螢幕寬度上 |
|  `$protkey(<name>)` | 傳回此原型中另一個鍵的值（自引用） |
|  `$add(<value1>, <value2>)` | 傳回值 1 + 值 2。也可以是列表、字典等 |
|  `$sub(<value1>, <value2>)` | 傳回值 1 - 值 2 |
|  `$mult(<value1>, <value2>)` | 傳回值1 * 值2 |
|  `$div(<value1>, <value2>)` | 傳回值 2 / 值 1 |
|  `$toint(<value>)` | 傳回轉換為整數的值（如果不可能，則傳回值） |
|  `$eval(<code>)` | 傳回程式碼字串的 [literal-eval](https://docs.python.org/2/library/ast.html#ast.literal_eval) 的結果。只有簡單的Python表示式。 |
| `$obj(<query>)` | 傳回按鍵、tag 或#dbref 全域搜尋的物件。需要 `spawner.spawn()` 中的 `caller` kwarg 進行訪問檢查。請參閱[搜尋可呼叫物件](./FuncParser.md#evenniautilsfuncparsersearching_callables)。  （$dbref(<query>) 是個別名，作用相同） |
| `$objlist(<query>)` | 與 `$obj` 類似， except 總是傳回零、一個或多個結果的清單。需要 `spawner.spawn()` 中的 `caller` kwarg 進行訪問檢查。請參閱[搜尋可呼叫物件](./FuncParser.md#evenniautilsfuncparsersearching_callables)。 |

對於能夠使用 Python 的開發人員來說，在原型中使用 protfuncs 通常沒有什麼用處。傳遞真正的 Python 函式更加強大和靈活。它們的主要用途是允許遊戲內構建者為其原型進行有限的編碼/指令碼編寫，而無需直接訪問原始 Python。

(database-prototypes)=
## 資料庫原型

在資料庫中儲存為 [Scripts](./Scripts.md)。這些有時被稱為“資料庫原型”，這是遊戲內建構者修改和新增原型的唯一方法。它們的優點是可以在建造者之間輕鬆修改和共享，但您需要使用遊戲內工具來使用它們。

(module-based-prototypes)=
## 基於模組的原型

這些原型被定義為分配給 `settings.PROTOTYPE_MODULES` 中定義的模組之一中的全域變數的字典。它們只能從遊戲外部修改，因此它們在遊戲中必然是「只讀」的並且不能被修改（但它們的副本可以製作成資料庫原型）。這些是 Evennia 0.8 之前唯一可用的原型。基於模組的原型對於開發人員提供唯讀的「起始」或「基礎」原型非常有用，或者如果他們只是喜歡在外部程式碼編輯器中離線工作的話。

預設設定`mygame/world/prototypes.py`供您新增自己的原型。 *全球所有
該模組中的 dicts* 將被 Evennia 視為原型。你也可以告訴Evennia
如果您願意，可以在更多模組中尋找原型：

```python
# in mygame/server/conf.py

PROTOTYPE_MODULES = += ["world.myownprototypes", "combat.prototypes"]

```

以下是模組中定義的原型範例：

    ```python
    # in a module Evennia looks at for prototypes,
    # (like mygame/world/prototypes.py)

    ORC_SHAMAN = {"key":"Orc shaman",
		  "typeclass": "typeclasses.monsters.Orc",
		  "weapon": "wooden staff",
		  "health": 20}
    ```

> 請注意，在上面的範例中，`"ORC_SHAMAN"` 將成為該原型的`prototype_key`。這是原型中唯一可以跳過 `prototype_key` 的情況。但是，如果明確給出 `prototype_key`，則該值優先。這是一個遺留行為，建議您始終新增 `prototype_key` 以保持一致。


(spawning)=
## 產卵

可以透過僅建構器的 `@spawn` 指令在遊戲內部使用生成器。假設「妖精」typeclass 可用於系統（作為資料庫原型或從模組讀取），您可以使用以下指令產生一個新的妖精

    spawn goblin

您也可以直接將原型指定為有效的 Python 字典：

    spawn {"prototype_key": "shaman", \
	    "key":"Orc shaman", \
            "prototype_parent": "goblin", \
            "weapon": "wooden staff", \
            "health": 20}

> 注意：`spawn` 指令對於原型字典比此處顯示的更寬鬆。因此，如果您只是測試一次性原型，則可以跳過 `prototype_key`。將使用隨機雜湊來進行驗證。您也可以跳過`prototype_parent/typeclass` - 然後將使用`settings.BASE_OBJECT_TYPECLASS` 給出的typeclass。

(using-evenniaprototypesspawner)=
### 使用evennia.prototypes.spawner()

在程式碼中，您可以直接透過呼叫存取生成器機制

```python
    new_objects = evennia.prototypes.spawner.spawn(*prototypes)
```

所有引數都是原型字典。該函式將傳回一個
已建立物件的匹配清單。例子：

```python
    obj1, obj2 = evennia.prototypes.spawner.spawn({"key": "Obj1", "desc": "A test"},
                                                  {"key": "Obj2", "desc": "Another test"})
```

> 提示：與使用 `spawn` 時相同，當從像這樣的一次性原型字典產生時，您可以跳過其他必需的鍵，例如 `prototype_key` 或 `typeclass`/`prototype_parent`。將使用預設值。

請注意，使用 `evennia.prototypes.spawner.spawn()` 時不會自動設定 `location`，您必須在原型字典中明確指定 `location`。  如果您提供的原型使用 `prototype_parent` 關鍵字，則生成器將從 `settings.PROTOTYPE_MODULES` 中的模組以及儲存到資料庫的原型中讀取原型，以確定可用父級的主體。 `spawn` 指令帶有許多可選關鍵字，您可以在[api 檔案中]找到它的定義(https://www.evennia.com/docs/latest/api/evennia.prototypes.spawner.html#evennia.prototypes.spawner.spawn)