(advanced-searching-django-database-queries)=
# 進階搜尋 - Django 資料庫查詢

```{important} 更高階的課程！

一旦您開始做更多事情，瞭解 Django 的查詢語言將非常有用
Evennia 中的高階內容。但它並不是嚴格需要開箱即用的，而且可以
第一次閱讀時有點不知所措。因此，如果您是 Python 新手並且
Evennia，請隨意瀏覽本課程，稍後再參考
你獲得了更多的經驗。
```

我們在上一課中使用的搜尋功能和方法足以滿足大多數情況。
但有時你需要更具體：

- 你想找到所有`Characters`...
- ……誰在標記為 `moonlit` 的房間中...
- ....並且_誰的 Attribute `lycanthropy` 等級等於 2...
- ……因為他們應該立刻變身為狼人！

原則上，您可以透過現有的搜尋功能結合大量迴圈來實現這一點
和 if 語句。但對於像這樣的非標準的東西，直接查詢資料庫將是
效率更高。

Evennia 使用 [Django](https://www.djangoproject.com/) 處理其與資料庫的連線。
一個 [django queryset](https://docs.djangoproject.com/en/3.0/ref/models/querysets/) 代表一個資料庫查詢。人們可以將查詢集新增在一起來建立更複雜的查詢。只有當您嘗試使用查詢集的結果時，它才會真正呼叫資料庫。

建立查詢集的正常方法是透過取得其 `.objects` 資源來定義要搜尋的實體類，然後對其呼叫各種方法。我們之前見過這種情況的變體：

    all_weapons = Weapon.objects.all()

現在這是一個表示 `Weapon` 的所有例項的查詢集。如果 `Weapon` 有一個子類別 `Cannon` 並且我們只想要大砲，我們會這樣做

    all_cannons = Cannon.objects.all()

請注意，`Weapon` 和 `Cannon` _不同_typeclasses。這意味著您在 `all_cannons` 中找不到任何 `Weapon` 型別分類的結果。反之亦然，您不會在 `all_weapons` 中找到任何 `Cannon` 型別分類的結果。這可能不是您所期望的。

如果您想要取得具有 typeclass `Weapon` 的所有實體以及 `Weapon` 的所有子類，例如 `Cannon`，則需要使用 `_family` 型別的查詢：

```{sidebar} _家庭

`all_family` 和 `filter_family`（以及用於獲得恰好一個結果的 `get_family`）是 Evennia 特定的。它們不是常規 Django 的一部分。
```

    really_all_weapons = Weapon.objects.all_family()

此結果現在包含 `Weapon` 和 `Cannon` 例項（以及任何其他
typeclasses 從 `Weapon` 任意距離繼承的實體，例如 `Musket` 或
`Sword`）。

要透過 Typeclass 以外的其他條件限制搜尋，您需要使用 `.filter`
（或 `.filter_family`）：

    roses = Flower.objects.filter(db_key="rose")

這是一個表示 `db_key` 等於 `"rose"` 的所有花的查詢集。
由於這是一個查詢集，您可以繼續新增它；這將充當 `AND` 條件。

    local_roses = roses.filter(db_location=myroom)

我們也可以在一份宣告中寫下這一點：

    local_roses = Flower.objects.filter(db_key="rose", db_location=myroom)

我們也可以從結果中`.exclude`得到一些東西

    local_non_red_roses = local_roses.exclude(db_key="red_rose")

需要注意的是，我們還沒有呼叫資料庫！直到我們
實際上嘗試檢查資料庫是否會被呼叫。這裡的
當我們嘗試迴圈資料庫時，它會被呼叫（因為現在我們實際上需要
從中取得結果以便能夠迴圈）：

    for rose in local_non_red_roses:
        print(rose)

從現在開始，查詢集是_evaluated_，我們不能繼續向其中新增更多查詢 - 如果我們想找到其他結果，我們需要建立一個新的查詢集。評估查詢集的其他方法是列印它，將其轉換為帶有 `list()` 的列表，或嘗試存取其結果。

```{sidebar} 資料庫欄位
每個資料庫表只有幾個欄位。對於`DefaultObject`，最常見的是`db_key`、`db_location` 和`db_destination`。當它們被訪問時，它們通常被訪問為 `obj.key`、`obj.location` 和 `obj.destination`。  在資料庫查詢中使用它們時，您只需要記住 `db_` 即可。物件描述，`obj.db.desc` 不是這樣一個硬編碼欄位，而是許多欄位之一
附加到物件的屬性。
```
注意我們如何使用 `db_key` 和 `db_location`。這是這些資料庫欄位的實際名稱。依照約定，Evennia 在每個資料庫欄位前面使用 `db_`。當您使用普通的 Evennia 搜尋幫助程式和物件時，您可以跳過 `db_` 但這裡我們直接呼叫資料庫並且需要使用「真實」名稱。


以下是 `objects` 管理器最常用的方法：

- `filter` - 根據搜尋條件查詢物件清單。如果沒有則給予空查詢集
被發現。
- `get` - 查詢單一符合專案 - 如果未找到或找到多個符合項，則會引發異常
成立。
- `all` - 取得特定型別的所有例項。
- `filter_family` - 與 `filter` 類似，但也搜尋所有子類別。
- `get_family` - 與 `get` 類似，但也搜尋所有子類別。
- `all_family` - 與 `all` 類似，但也傳回所有子類別的實體。

> 所有 Evennia 搜尋函式都在底層使用查詢集。 `evennia.search_*` 函式實際上會傳回查詢集（到目前為止我們只是將它們視為列表）。這意味著原則上您可以將 `.filter` 查詢新增到 `evennia.search_object` 的結果中以進一步細化搜尋。


(queryset-field-lookups)=
## 查詢集欄位查詢

上面我們發現了玫瑰的`db_key` `"rose"`。這是一個_大小寫敏感_的_精確_匹配，因此它不會找到`"Rose"`。

```python
# this is case-sensitive and the same as =
roses = Flower.objects.filter(db_key__exact="rose"

# the i means it's case-insensitive
roses = Flower.objects.filter(db_key__iexact="rose")
```
Django 欄位查詢語言使用 `__` 類似於 Python 使用 `.` 存取資源。這是因為函式關鍵字中不允許使用 `.`。

```python
roses = Flower.objects.filter(db_key__icontains="rose")
```

這將找到名稱中包含字串 `"rose"` 的所有花，例如 `"roses"`、`"wild rose"` 等。開頭的 `i` 使搜尋不區分大小寫。其他有用的變體有 `__istartswith` 和 `__iendswith`。您也可以使用 `__gt`、`__ge` 進行「大於」/「大於或等於」比較（`__lt` 和 `__le` 相同）。還有`__in`：

```python
swords = Weapons.objects.filter(db_key__in=("rapier", "two-hander", "shortsword"))
```

也可以使用 `__` 來存取外部物件，例如 Tags。例如，我們假設
這就是我們辨識法師的方式：

```python
char.tags.add("mage", category="profession")
```

現在，在這種情況下，我們已經有一個 Evennia 助手來執行此搜尋：

```python
mages = evennia.search_tags("mage", category="profession")
```

如果您只尋找吸血鬼法師，那麼查詢的內容如下：

```{sidebar} 打破程式碼行
在 Python 中，您可以將程式碼包裝在 `(...)` 中以將其分成多行。這樣做不會影響功能，但可以使其更易於閱讀。
```

```python
sparkly_mages = (
	Vampire.objects.filter(									   
           db_tags__db_key="mage", 
           db_tags__db_category="profession")
    )
```

這將檢視 `Vampire` 上的 `db_tags` 欄位並過濾每個 tag 的值
`db_key` 和 `db_category` 在一起。

有關更多欄位查詢，請參閱有關該主題的 [django 檔案](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#field-lookups)。

(lets-get-that-werewolf)=
## 讓我們抓住那個狼人...

我們來看看能不能查詢一開始提到的月光下的狼人
本課的。

首先，我們讓自己和目前位置符合標準，這樣我們就可以測試：

    > py here.tags.add("moonlit")
    > py me.db.lycanthropy = 2

這是更複雜查詢的範例。我們將把它視為一個例子
可能的。

```{code-block} python
:linenos:
:emphasize-lines: 4,6,7,8

from typeclasses.characters import Character

will_transform = (
    Character.objects
    .filter(
        db_location__db_tags__db_key__iexact="moonlit",
        db_attributes__db_key__iexact="lycanthropy",
        db_attributes__db_value=2
    )
)
```

```{sidebar} 屬性與資料庫欄位
不要將資料庫欄位與您透過`obj.db.attr = 'foo'`或`obj.attributes.add()`設定的[屬性](../../../Components/Attributes.md)混淆。屬性是「連結」到物件的自訂資料庫實體。它們不是像 `db_key` 或 `db_location` 這樣的物件*上的單獨欄位。

雖然 Attribute 的 `db_key` 只是一個普通字串，但 `db_value` 實際上是一個序列化的資料。  這意味著無法使用其他運運算元查詢此內容。所以如果你使用e.g。 `db_attributes__db_value__iexact=2`，你會得到一個錯誤。雖然屬性非常靈活，但這是它們的缺點 - 除了找到精確匹配之外，無法使用高階查詢方法直接查詢它們的儲存值。
```
- **第 4 行** 我們想要找到 `Character`s，因此我們訪問 `Character` typeclass 上的 `.objects`。
- 我們開始篩選...
    - **第 6 行**：...透過存取 `db_location` 欄位（通常這是一個房間）
	    - ……在該位置，我們得到 `db_tags` 的值（這是一個 _many-to-many_ 資料庫欄位
        that we can treat like an object for this purpose; it references all Tags on the location)
	    - ... and from those `Tags`, we looking for `Tags` whose `db_key` is "monlit" (non-case sensitive).
     - **Line 7**: ... We also want only Characters with `Attributes` whose `db_key` is exactly `"lycanthropy"`
    - **Line 8** :... at the same time as the `Attribute`'s `db_value` is 2.

執行此查詢會使我們新的狼人角色出現在 `will_transform` 中，因此我們知道要對其進行轉換。成功！

```{important}
您無法像其他資料型別一樣自由地查詢 Attribute `db_value`。這是因為 Attributes 可以儲存任何 Python 實體，並且實際上在資料庫端儲存為 _strings_ 。因此，雖然您可以在上面的範例中使用 `db_value=2`，但您將無法使用 `dbvalue__eq=2` 或 `__lt=2`。有關處理屬性的更多資訊，請參閱[屬性](../../../Components/Attributes.md#querying-by-attribute)。
```

(queries-with-or-or-not)=
## 使用 OR 或 NOT 的查詢

到目前為止，所有範例都使用 `AND` 關係。 `.filter` 的引數與 `AND` 一起新增
（「我們希望 tag 的空間是「monlit」_並且_狼性> 2」）。

對於使用`OR`和`NOT`的查詢，我們需要Django的[Q物件](https://docs.djangoproject.com/en/4.1/topics/db/queries/#complex-lookups-with-q-objects)。它是直接從 Django 匯入的：

    from django.db.models import Q

例如，`Q` 是使用與 `.filter` 相同的引數建立的物件

    Q(db_key="foo")

然後，您可以使用此 `Q` 例項作為 `filter` 中的引數：

    q1 = Q(db_key="foo")
    Character.objects.filter(q1)
	# this is the same as 
	Character.objects.filter(db_key="foo")

`Q` 的有用之處在於，這些物件可以用特殊符號（位元運運算元）連結在一起：`|` 對應 `OR`，`&` 對應 `AND`。前面的波形符 `~` 否定 `Q` 內的表示式，因此
工作原理類似於 `NOT`。

    q1 = Q(db_key="Dalton")
    q2 = Q(db_location=prison)
    Character.objects.filter(q1 | ~q2)

將獲得所有名為“道爾頓”或_不在監獄中的角色。結果是混合的
道爾頓和非囚犯。

讓我們擴充套件原來的狼人查詢。我們不僅想找到月光下的房間中具有一定等級`lycanthropy`的所有角色 - 我們決定，如果他們被_新近咬傷_，他們也應該轉身，_無論_他們的狼人等級如何（這樣更戲劇化！）。

假設被咬意味著你將被分配Tag `recently_bitten`。

這就是我們更改查詢的方式：

```python
from django.db.models import Q

will_transform = (
    Character.objects
    .filter(
        Q(db_location__db_tags__db_key__iexact="moonlit")
        & (
          Q(db_attributes__db_key="lycanthropy",
            db_attributes__db_value=2)
          | Q(db_tags__db_key__iexact="recently_bitten")
        ))
    .distinct()
)
```

這是相當緊湊的。如果這樣寫，可能會更容易看出發生了什麼事：

```python
from django.db.models import Q

q_moonlit = Q(db_location__db_tags__db_key__iexact="moonlit")
q_lycanthropic = Q(db_attributes__db_key="lycanthropy", db_attributes__db_value=2)
q_recently_bitten = Q(db_tags__db_key__iexact="recently_bitten")

will_transform = (
    Character.objects
    .filter(q_moonlit & (q_lycanthropic | q_recently_bitten))
    .distinct()
)
```

```{sidebar} SQL

這些Python結構在內部轉換為SQL，即本機語言
資料庫。  如果您熟悉SQL，這些是多對多表
使用 `LEFT OUTER JOIN` 連線，這可能會導致多個合併行合併
同一物件具有不同的關係。

```

這讀作「在月光照射的房間裡找到所有具有以下特徵的角色」：
Attribute `lycanthropy` 等於二，_或_ 其中有 Tag
`recently_bitten`」。使用這樣的 OR- 查詢，可以找到相同的內容
字元透過不同的路徑，所以我們在末尾新增`.distinct()`。這使得
確保結果中每個角色只有一個例項。

(annotations)=
## 註解

如果我們想過濾某些不能輕易表示的條件該怎麼辦
物體上的場？一個例子是想要找到只包含_五個或更多物體_的房間。

我們*可以*這樣做（實際上不要這樣做！）：

```python
from typeclasses.rooms import Room

  all_rooms = Rooms.objects.all()

  rooms_with_five_objects = []
  for room in all_rooms:
      if len(room.contents) >= 5:
          rooms_with_five_objects.append(room)
```

```{sidebar} list.append，擴充套件並.pop

使用 `mylist.append(obj)` 將新專案新增至清單。使用 `mylist.extend(another_list))` 或 `list1 + list2` 將兩個清單合併在一起。使用 `mylist.pop()` 從清單末端刪除專案，或使用 `.pop(0)` 從清單開頭刪除專案。請記住，Python 中所有索引都是從 `0` 開始的。
```

上面我們得到_all_房間，然後使用`list.append()`繼續增加正確的房間
房間數量不斷增加。這不是一個好主意，一旦你的資料庫
隨著增長，這將產生不必要的計算密集型。最好查詢一下
直接資料庫

_Annotations_ 允許您在查詢中設定一個“變數”，然後您可以
從查詢的其他部分存取。讓我們像之前一樣做同樣的例子
直接在資料庫中：

```{code-block} python
:linenos:
:emphasize-lines: 6,8

from typeclasses.rooms import Room
from django.db.models import Count

rooms = (
    Room.objects
    .annotate(
        num_objects=Count('locations_set'))
    .filter(num_objects__gte=5)
)
```

```{sidebar} locations_set
請注意 `Count` 中 `locations_set` 的使用。 `*s_set` 是 Django 自動建立的反向引用。在這種情況下，它允許您查詢*以當前物件作為位置*的所有物件。
```

`Count` 是一個 Django 類，用於計算資料庫中的事物數量。

- **第6-7行**：這裡我們先建立一個型別為`Count`的註解`num_objects`。它會建立一個資料庫內函式來計算資料庫內的結果數量。事實註釋意味著現在 `num_objects` 可用於查詢的其他部分。
- **第 8 行** 我們對此註解進行過濾，使用名稱 `num_objects` 作為我們的名稱
可以過濾。我們使用`num_objects__gte=5`，這意味著`num_objects`
應大於或等於5。

註釋可能有點難以理解，但比遍歷 Python 中的所有物件要有效得多。

(f-objects)=
## F 物件

如果我們想在一個模型中比較兩個動態引數呢？
查詢？例如，如果我們不想要 5 個或更多物件，而只想
庫存比 tags 更大的物件（愚蠢的例子，但...）？

這可以使用 Django 的 [F 物件](https://docs.djangoproject.com/en/4.1/ref/models/expressions/#f-expressions)。所謂的 F 表示式允許您執行檢視資料庫中每個物件的值的查詢。

```python
from django.db.models import Count, F
from typeclasses.rooms import Room

result = (
    Room.objects
    .annotate(
        num_objects=Count('locations_set'),
        num_tags=Count('db_tags'))
    .filter(num_objects__gt=F('num_tags'))
)
```

這裡我們使用 `.annotate` 建立兩個查詢內「變數」`num_objects` 和 `num_tags`。然後我們直接在過濾器中使用這些結果。使用 `F()` 還可以完全在資料庫內即時計算過濾條件的右側。

(grouping-and-returning-only-certain-properties)=
## 僅分組並傳回某些屬性

假設您使用 tags 來標記屬於某個組織的某人。現在您想要製作一個列表，並且需要一次獲取每個組織的成員數量。

`.annotate`、`.values_list` 和 `.order_by` 查詢集方法對此很有用。通常，當您執行 `.filter` 時，您傳回的是一堆完整的 typeclass 例項，例如玫瑰或劍。使用 `.values_list` 您可以選擇僅取回物件的某些屬性。 `.order_by` 方法最終允許根據某些標準對結果進行排序：


```{code-block} python 
:linenos:
:emphasize-lines: 6,7,8,9 

from django.db.models import Count
from typeclasses.rooms import Room

result = (
    Character.objects
    .filter(db_tags__db_category="organization")
    .annotate(tagcount=Count('id'))
    .order_by('-tagcount'))
    .values_list('db_tags__db_key', "tagcount")
```

在這裡我們獲取所有的角色...
- **第 6 行**：...有 tag 類別“組織”
- **第7行**：...一路上我們計算為每個組織找到多少個不同的字元（每個`id`都是唯一的），並使用`.annotate`和`Count`將其儲存在「變數」`tagcount`中
- **第 8 行**：...我們使用此計數按 `tagcount` 的降序對結果進行排序（降序是因為有一個減號，預設是升序，但我們希望最受歡迎的組織排在第一位）。
- **第 9 行**：...最後，我們確保只返回我們想要的屬性，即組織 tag 的名稱以及我們為該組織找到的匹配項數量。為此，我們在查詢集上使用 `values_list` 方法。這將立即評估查詢集。

結果將是按匹配數降序排列的元組列表，
格式如下：
```
[
 ('Griatch's poets society', 3872),
 ("Chainsol's Ainneve Testers", 2076),
 ("Blaufeuer's Whitespace Fixers", 1903),
 ("Volund's Bikeshed Design Crew", 1764),
 ("Tehom's Glorious Misanthropes", 1763)
]
```

(conclusions)=
## 結論

我們在本課程中涵蓋了許多基礎知識，並涵蓋了幾個更複雜的主題。瞭解如何使用 Django 進行查詢是一項強大的技能。
