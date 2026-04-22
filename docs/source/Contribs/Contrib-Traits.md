(traits)=
# 性狀

Griatch 2020 貢獻，基於 Whitenoise 和 Ainneve contribs 的程式碼，2014 年

`Trait` 代表（通常）角色的可修改屬性。他們可以
用來表示從屬性（力量、敏捷等）到技能的一切
（狩獵 10，劍 14 等）和動態變化的東西，如 HP、XP 等。
特徵與普通屬性的不同之處在於它們追蹤其變化和限制
自己到特定的值範圍。人們可以輕鬆地新增/減去它們，並且
它們甚至可以以特定的速率動態變化（例如你中毒了或
痊癒了）。

特徵在幕後使用 Evennia 屬性，使它們持久化（它們能夠生存
伺服器重新載入/重新啟動）。

(installation)=
## 安裝

Traits 總是會新增到 typeclass 中，例如 Character 類別。

有兩種方法可以在 typeclass 上設定 Traits。第一個設定`TraitHandler`
作為類別上的屬性 `.traits`，然後您可以將特徵作為 e.g 存取。 `.traits.strength`。
另一種選擇使用 `TraitProperty`，這使得特徵可以直接使用
為e.g。 `.strength`。此解決方案也使用 `TraitHandler`，但您不需要
明確定義它。如果您願意，可以將兩種風格結合起來。

(traits-with-traithandler)=
### 具有 TraitHandler 的特徵

以下是將 TraitHandler 新增至 Character 類別的範例：

```python
# mygame/typeclasses/objects.py

from evennia import DefaultCharacter
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler

# ...

class Character(DefaultCharacter):
    ...
    @lazy_property
    def traits(self):
        # this adds the handler as .traits
        return TraitHandler(self)


    def at_object_creation(self):
        # (or wherever you want)
        self.traits.add("str", "Strength", trait_type="static", base=10, mod=2)
        self.traits.add("hp", "Health", trait_type="gauge", min=0, max=100)
        self.traits.add("hunting", "Hunting Skill", trait_type="counter",
                        base=10, mod=1, min=0, max=100)
```
新增特徵時，您可以提供屬性名稱 (`hunting`)
有了一個更人性化的名字（“狩獵技能”）。後者將顯示如果您
列印特徵等。 `trait_type` 很重要，這指定了哪種型別
這就是特徵（見下文）。

(traitproperties)=
### TraitProperties

使用 `TraitProperties` 使特徵可以直接在類別上可用，就像 Django 模型一樣
欄位。缺點是你必須確保你的特質名稱不會與任何特質相衝突。
您班級的其他屬性/方法。

```python
# mygame/typeclasses/objects.py

from evennia import DefaultObject
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitProperty

# ...

class Object(DefaultObject):
    ...
    strength = TraitProperty("Strength", trait_type="static", base=10, mod=2)
    health = TraitProperty("Health", trait_type="gauge", min=0, base=100, mod=2)
    hunting = TraitProperty("Hunting Skill", trait_type="counter", base=10, mod=1, min=0, max=100)
```

> 請注意，屬性名稱將成為特徵的名稱，並且您不提供`trait_key`
> 分別地。

> `.traits` TraitHandler 仍將被建立（它在
> 兜帽。但只有當 TraitProperty 至少被訪問一次時才會建立，
> 所以混合兩種風格時要小心。如果您想確保 `.traits` 始終可用，
> 如前所示手動新增 `TraitHandler` - 預設將使用 `TraitProperty`
> 相同的處理程式 (`.traits`)。

(using-traits)=
## 使用特質

特徵是新增到特徵處理程式中的實體（如果您使用`TraitProperty`，則處理程式剛剛在下面建立
引擎蓋），之後可以將其作為處理程式上的屬性進行存取（類似於您可以執行的操作）
.db.attrname 表示 Evennia 中的屬性）。

所有特徵都有一個_唯讀_欄位`.value`。這僅用於讀出結果，您永遠不會
直接操作它（如果你嘗試，它只會保持不變）。 `.value` 的計算依據
關於組合欄位，例如 `.base` 和 `.mod` - 哪些欄位可用以及它們如何關聯
彼此取決於特質型別。

```python
> obj.traits.strength.value
12                                  # base + mod

> obj.traits.strength.base += 5
obj.traits.strength.value
17

> obj.traits.hp.value
102                                 # base + mod

> obj.traits.hp.base -= 200
> obj.traits.hp.value
0                                   # min of 0

> obj.traits.hp.reset()
> obj.traits.hp.value
100

# you can also access properties like a dict
> obj.traits.hp["value"]
100

# you can store arbitrary data persistently for easy reference
> obj.traits.hp.effect = "poisoned!"
> obj.traits.hp.effect
"poisoned!"

# with TraitProperties:

> obj.hunting.value
12

> obj.strength.value += 5
> obj.strength.value
17
```

(relating-traits-to-one-another)=
### 將特徵彼此關聯

從特徵中，您可以透過 `.traithandler` 存取自己的 Traithandler。你可以
也可以使用以下方法在同一處理程式上找到另一個特徵
`Trait.get_trait("traitname")`方法。

```python
> obj.strength.get_trait("hp").value
100
```

這對於預設特徵型別來說不太有用——它們都在執行
彼此獨立。但如果你創造自己的特質類別，你
可以用它來創造相互依賴的特徵。

例如，您可以想像建立一個 Trait，它是以下值的總和
其他兩個特徵並受到第三個特徵的值的限制。如此複雜
互動在RPG規則系統中很常見，但根據定義是特定於遊戲的。

請參閱有關[建立您自己的 Trait 類別](#expanding-with-your-own-traits) 部分中的範例。


(trait-types)=
## 性狀型別

所有預設特徵都有一個唯讀 `.value` 屬性，顯示相關或
特徵的“當前”值。這到底意味著什麼取決於特質的型別。

特徵也可以組合起來用它們的.value 進行算術運算，如果兩者都有
相容型別。

```python
> trait1 + trait2
54

> trait1.value
3

> trait1 + 2
> trait1.value
5
```

也可以比較兩個數字特徵（大於等），這在以下方面很有用
各種規則解析。

```python

if trait1 > trait2:
    # do stuff
```

(trait)=
### 特徵

任何型別的單一值。

這是「基礎」特徵，如果你想發明就必須繼承
從頭開始的特質型別（大多時候你可能會繼承一些
不過更高階的特質型別類別）。

與其他 Trait-types 不同，基礎 `Trait` 的單一 `.value` 屬性可以
被編輯。該值可以儲存可以儲存在 Attribute 中的任何資料。如果
它是一個整數/浮點數，你可以用它來做算術，但否則這只是
就像一個榮耀的Attribute。


```python
> obj.traits.add("mytrait", "My Trait", trait_type="trait", value=30)
> obj.traits.mytrait.value
30

> obj.traits.mytrait.value = "stringvalue"
> obj.traits.mytrait.value
"stringvalue"
```

(static-trait)=
### 靜態特質

`value = base + mod`

靜態特徵具有 `base` 值和可選的 `mod`-ifier。典型用途
靜態特徵的屬性是力量統計或技能值。也就是說，某物
變化緩慢或根本不變化，可以就地修改。

```python
> obj.traits.add("str", "Strength", trait_type="static", base=10, mod=2)
> obj.traits.mytrait.value

12   # base + mod
> obj.traits.mytrait.base += 2
> obj.traits.mytrait.mod += 1
> obj.traits.mytrait.value
15

> obj.traits.mytrait.mod = 0
> obj.traits.mytrait.value
12
```

(counter)=
### 櫃檯


    min/unset     base    base+mod                       max/unset
    |--------------|--------|---------X--------X------------|
                                  current    value
                                             = current
                                             + mod

計數器描述了可以從基數開始移動的值。 `.current` 屬性
是通常修改的東西。它從 `.base` 開始。還可以新增一個
修飾符，它將被新增到基礎和當前（形成
`.value`）。  範圍的最小/最大是可選的，將邊界設為“無”將
刪除它。反特徵的建議用途是追蹤技能值。

```python
> obj.traits.add("hunting", "Hunting Skill", trait_type="counter",
                   base=10, mod=1, min=0, max=100)
> obj.traits.hunting.value
11  # current starts at base + mod

> obj.traits.hunting.current += 10
> obj.traits.hunting.value
21

# reset back to base+mod by deleting current
> del obj.traits.hunting.current
> obj.traits.hunting.value
11
> obj.traits.hunting.max = None  # removing upper bound

# for TraitProperties, pass the args/kwargs of traits.add() to the
# TraitProperty constructor instead.
```

計數器有一些額外的屬性：

(descs)=
#### .descs

`descs` 屬性是一個字典 `{upper_bound:text_description}`。這允許輕鬆地
在中儲存當前值的更人性化的描述
間隔。以下是技能值介於 0 到 10 之間的範例：

    {0: "unskilled", 1: "neophyte", 5: "trained", 7: "expert", 9: "master"}

必須按照從最小到最大的順序提供金鑰。低於最低值和高於最低值的任何值
最高的描述將被視為包含在最接近的描述槽中。
透過在計數器上呼叫`.desc()`，您將獲得與當前`value`相符的文字。

```python
# (could also have passed descs= to traits.add())
> obj.traits.hunting.descs = {
    0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"}
> obj.traits.hunting.value
11

> obj.traits.hunting.desc()
"neophyte"
> obj.traits.hunting.current += 60
> obj.traits.hunting.value
71

> obj.traits.hunting.desc()
"expert"
```

(rate)=
#### 。速度

`rate` 屬性預設為 0。如果設定為不同於 0 的值，則
允許特徵動態改變值。這可以用於例如
對於暫時降低但會逐漸（或突然）的 attribute
一定時間後恢復。速率作為電流的變化給出
每秒`.value`，這仍然受到最小/最大邊界的限制，
如果設定了這些。

還可以設定 `.ratetarget`，以便自動變更停止於
（而不是在最小/最大邊界）。這允許值返回到
先前的值。

```python

> obj.traits.hunting.value
71

> obj.traits.hunting.ratetarget = 71
# debuff hunting for some reason
> obj.traits.hunting.current -= 30
> obj.traits.hunting.value
41

> obj.traits.hunting.rate = 1  # 1/s increase
# Waiting 5s
> obj.traits.hunting.value
46

# Waiting 8s
> obj.traits.hunting.value
54

# Waiting 100s
> obj.traits.hunting.value
71    # we have stopped at the ratetarget

> obj.traits.hunting.rate = 0  # disable auto-change
```
請注意，檢索 `current` 時，結果將始終相同
鍵入 `.base` 甚至 `rate` 都是非整數值。所以如果 `base` 是 `int`
（預設），`current` 值也將四捨五入為最接近的完整整數。
如果您想檢視確切的 `current` 值，請將 `base` 設定為浮點數 - 您
如果您想要整數，則需要自己在結果上使用 `round()` 。

(percent)=
#### .percent()

如果同時定義了 min 和 max，則特徵的 `.percent()` 方法將
以百分比形式傳回值。

```python
> obj.traits.hunting.percent()
"71.0%"

> obj.traits.hunting.percent(formatting=None)
71.0
```

(gauge)=
### 測量

這模擬了從基本+mod值清空的[fuel-]儀表。

    min/0                                            max=base+mod
     |-----------------------X---------------------------|
                           value
                          = current

`.current` 值將從滿量規開始。.max 屬性是
只讀，由 `.base` + `.mod` 設定。因此與 `Counter` 相反，
`.mod`修飾符僅適用於儀表的最大值，不適用於目前值
值。如果未明確設定，最小界限預設為 0。

此特徵對於顯示通常會耗盡的資源（例如健康、
體力之類的。

```python
> obj.traits.add("hp", "Health", trait_type="gauge", base=100)
> obj.traits.hp.value  # (or .current)
100

> obj.traits.hp.mod = 10
> obj.traits.hp.value
110

> obj.traits.hp.current -= 30
> obj.traits.hp.value
80
```

Gauge 特徵是 Counter 的子類，因此您可以存取相同的
有意義的方法和屬性。所以儀表也可以有一個
`.descs` dict 來描述文字中的間隔，並且可以使用 `.percent()` 來
取得它的填充程度（百分比等）。

`.rate` 與儀表特別相關 - 對一切都很有用
從毒藥慢慢耗盡你的生命值，到休息後逐漸增加你的生命值。

(expanding-with-your-own-traits)=
## 根據自己的特質進行擴充套件

Trait 是繼承自 `evennia.contrib.rpg.traits.Trait` （或繼承自以下之一的類別）
現有的 Trait 類）。

```python
# in a file, say, 'mygame/world/traits.py'

from evennia.contrib.rpg.traits import StaticTrait

class RageTrait(StaticTrait):

    trait_type = "rage"
    default_keys = {
        "rage": 0
    }

    def berserk(self):
        self.mod = 100

    def sedate(self):
        self.mod = 0
```

上面是一個自訂特徵類別「rage」的範例，它將屬性「rage」儲存在
本身，預設值為 0。這具有 Trait 的所有功能 -
例如，如果您對 `rage` 屬性執行 del 操作，它將被設定回原來的狀態
預設 (0)。上面我們也加入了一些輔助方法。

若要將自訂 RageTrait 新增至 Evennia，請將以下內容新增至您的設定檔中
（假設你的班級在mygame/world/traits.py）：

    TRAIT_CLASS_PATHS = ["world.traits.RageTrait"]

重新載入伺服器，您現在應該可以使用您的特徵：

```python
> obj.traits.add("mood", "A dark mood", rage=30, trait_type='rage')
> obj.traits.mood.rage
30
```

請記住，您可以使用 `.get_trait("name")` 來訪問
相同的處理程式。  假設怒氣修正值實際上受到以下限制
字元的目前 STR 值乘以 3，最大值為 100：

```python
class RageTrait(StaticTrait):
    #...
    def berserk(self):
        self.mod = min(100, self.get_trait("STR").value * 3)
```

(as-traitproperty)=
# 如TraitProperty

```
class Character(DefaultCharacter):
    rage = TraitProperty("A dark mood", rage=30, trait_type='rage')
```

(adding-additional-traithandlers)=
## 增加額外的TraitHandlers

有時，對特徵進行頂層分類更容易，例如統計資料、技能或您想要彼此獨立處理的其他類別的特徵。以下範例顯示了物件 typeclass 上的範例，擴充套件了第一個安裝範例：

```python
# mygame/typeclasses/objects.py

from evennia import DefaultCharacter
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler

# ...

class Character(DefaultCharacter):
    ...
    @lazy_property
    def traits(self):
        # this adds the handler as .traits
        return TraitHandler(self)

    @lazy_property
    def stats(self):
        # this adds the handler as .stats
        return TraitHandler(self, db_attribute_key="stats")

    @lazy_property
    def skills(self):
        # this adds the handler as .skills
        return TraitHandler(self, db_attribute_key="skills")


    def at_object_creation(self):
        # (or wherever you want)
        self.stats.add("str", "Strength", trait_type="static", base=10, mod=2)
        self.traits.add("hp", "Health", trait_type="gauge", min=0, max=100)
        self.skills.add("hunting", "Hunting Skill", trait_type="counter",
                        base=10, mod=1, min=0, max=100)
```

> 請記住，`.get_traits()` 方法僅適用於訪問
_相同_TraitHandler。


----

<small>此檔案頁面是從`evennia\contrib\rpg\traits\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
