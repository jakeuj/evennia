(random-name-generator)=
# 隨機名稱產生器

貢獻者InspectorCaracal (2022)

用於產生隨機名稱的模組，包括現實世界和幻想世界。現實世界
名稱可以產生為名字、姓氏或
全名（名字、可選的中間名和姓氏）。姓名資料來自[姓名背後](https://www.behindthename.com/)
並在 [CC BY-SA 4.0 許可證](https://creativecommons.org/licenses/by-sa/4.0/) 下使用。

幻想名稱是根據基本語音規則使用 CVC 音節語法產生的。

現實世界和幻想名稱的生成都可以擴充套件以包括額外的
透過您的遊戲的 `settings.py` 獲取資訊

(installation)=
## 安裝

這是一個獨立的實用程式。只需匯入此模組（`from evennia.contrib.utils import name_generator`）並在任何您喜歡的地方使用它的功能即可。

(usage)=
## 用法

使用以下指令將模組匯入到需要的地方：
```py
from evennia.contrib.utils.name_generator import namegen
```

預設情況下，所有函式都將傳回具有一個生成名稱的字串。
如果指定多個，或傳遞 `return_list=True` 作為關鍵字引數，則傳回值將是字串清單。

此模組對於命名新建立的 NPCs 特別有用，如下所示：
```py
npc_name = namegen.full_name()
npc_obj = create_object(key=npc_name, typeclass="typeclasses.characters.NPC")
```

(available-settings)=
## 可用設定

這些設定都可以在遊戲的 `server/conf/settings.py` 檔案中定義。

- `NAMEGEN_FIRST_NAMES` 新增新的名字清單。
- `NAMEGEN_LAST_NAMES` 新增新的姓氏清單。
- `NAMEGEN_REPLACE_LISTS` - 如果您只想使用設定中定義的名稱，請設定為 `True`。
- `NAMEGEN_FANTASY_RULES` 允許您新增新的語音規則來產生完全虛構的名稱。有關外觀的詳細資訊，請參閱“自訂幻想名稱樣式規則”部分。

範例：
```py
NAMEGEN_FIRST_NAMES = [
		("Evennia", 'mf'),
		("Green Tea", 'f'),
	]

NAMEGEN_LAST_NAMES = [ "Beeblebrox", "Son of Odin" ]

NAMEGEN_FANTASY_RULES = {
  "example_style": {
			"syllable": "(C)VC",
			"consonants": [ 'z','z','ph','sh','r','n' ],
			"start": ['m'],
			"end": ['x','n'],
			"vowels": [ "e","e","e","a","i","i","u","o", ],
			"length": (2,4),
	}
}
```


(generating-real-names)=
## 產生真實姓名

contrib 提供了三個用於產生隨機真實世界名稱的函式：
`first_name()`、`last_name()` 和 `full_name()`。如果您想要多個名字
一次生成，可以使用`num`關鍵字引數來指定多少。

例子：
```
>>> namegen.first_name(num=5)
['Genesis', 'Tali', 'Budur', 'Dominykas', 'Kamau']
>>> namegen.first_name(gender='m')
'Blanchard'
```

`first_name` 函式也採用 `gender` 關鍵字引數來篩選名稱
由性別協會。 「f」代表女性，「m」代表男性，「mf」代表女性
_and_ 男性，或預設 `None` 以符合任何性別。

`full_name` 函式也採用 `gender` 關鍵字，以及 `parts`
定義有多少個名字組成全名。最少有兩個：名字和
一個姓氏。您也可以透過設定先生成姓氏的名稱
關鍵字引數 `surname_first` 到 `True`

例子：
```
>>> namegen.full_name()
'Keeva Bernat'
>>> namegen.full_name(parts=4)
'Suzu Shabnam Kafka Baier'
>>> namegen.full_name(parts=3, surname_first=True)
'Ó Muircheartach Torunn Dyson'
>>> namegen.full_name(gender='f')
'Wikolia Ó Deasmhumhnaigh'
```

(adding-your-own-names)=
### 新增您自己的名字

您可以使用設定 `NAMEGEN_FIRST_NAMES` 新增其他名稱，並且
`NAMEGEN_LAST_NAMES`

`NAMEGEN_FIRST_NAMES` 應該是元組列表，其中第一個值是名稱
第二個值是性別標誌 - 'm' 表示僅限男性，'f' 表示女性 -
僅，“mf”代表其中之一。

`NAMEGEN_LAST_NAMES` 應該是字串列表，其中每個專案都是可用的
姓氏。

範例：
```py
NAMEGEN_FIRST_NAMES = [
		("Evennia", 'mf'),
		("Green Tea", 'f'),
	]

NAMEGEN_LAST_NAMES = [ "Beeblebrox", "Son of Odin" ]
```

如果您希望上面的自訂清單完全替換內建清單而不是擴充套件它們，請設定`NAMEGEN_REPLACE_LISTS = True`。

(generating-fantasy-names)=
## 產生幻想名稱

產生完全虛構的名稱是使用 `fantasy_name` 函式完成的。的
contrib 帶有三種內建的名稱樣式，您可以使用它們，或者您也可以
將自訂名稱規則的字典放入`settings.py`

產生幻想名稱以規則集鍵為「style」關鍵字，可以
傳回單一名稱或多個名稱。預設情況下，它會回傳一個
內建「嚴厲」風格的單一名稱。 contrib 還帶有“流體”和“外星人”風格。

```py
>>> namegen.fantasy_name()
'Vhon'
>>> namegen.fantasy_name(num=3, style="harsh")
['Kha', 'Kizdhu', 'Godögäk']
>>> namegen.fantasy_name(num=3, style="fluid")
['Aewalisash', 'Ayi', 'Iaa']
>>> namegen.fantasy_name(num=5, style="alien")
["Qz'vko'", "Xv'w'hk'hxyxyz", "Wxqv'hv'k", "Wh'k", "Xbx'qk'vz"]
```

(multi-word-fantasy-names)=
### 多字幻想名稱

`fantasy_name` 函式一次只會產生一個名稱-單字，因此對於多單字名稱
你需要將各個部分組合在一起。根據您想要什麼樣的最終結果，有
幾種方法。


(the-simple-approach)=
#### 簡單的方法

如果您只需要它具有多個部分，您可以一次產生多個名稱並`join`它們。

```py
>>> name = " ".join(namegen.fantasy_name(num=2))
>>> name
'Dezhvözh Khäk'
```

如果您希望名字/姓氏之間有更多變化，您也可以為
不同的風格，然後將它們組合起來。

```py
>>> first = namegen.fantasy_name(style="fluid")
>>> last = namegen.fantasy_name(style="harsh")
>>> name = f"{first} {last}"
>>> name
'Ofasa Käkudhu'
```

(nakku-silversmith)=
#### 《納庫銀匠》

一種常見的幻想名字實踐是基於職業或頭銜的姓氏。為了達到這個效果，
您可以將 `last_name` 函式與自訂姓氏清單結合使用，並將其與產生的
幻想的名字。

例子：
```py
NAMEGEN_LAST_NAMES = [ "Silversmith", "the Traveller", "Destroyer of Worlds" ]
NAMEGEN_REPLACE_LISTS = True

>>> first = namegen.fantasy_name()
>>> last = namegen.last_name()
>>> name = f"{first} {last}"
>>> name
'Tözhkheko the Traveller'
```

(elarion-dyrinea-thror-obinson)=
#### 埃拉里昂·迪里尼亞，索羅·奧賓森

幻想名字的另一種常見風格是使用姓氏字尾或字首。為此，你將
需要自行增加額外的位元。

範例：
```py
>>> names = namegen.fantasy_name(num=2)
>>> name = f"{names[0]} za'{names[1]}"
>>> name
"Tithe za'Dhudozkok"

>>> names = namegen.fantasy_name(num=2)
>>> name = f"{names[0]} {names[1]}son"
>>> name
'Kön Ködhöddoson'
```


(custom-fantasy-name-style-rules)=
### 自訂幻想名稱樣式規則

樣式規則包含在字典的字典中，其中樣式名稱
是鍵，樣式規則是字典值。

以下是將自訂樣式新增至 `settings.py` 的方法：
```py
NAMEGEN_FANTASY_RULES = {
  "example_style": {
			"syllable": "(C)VC",
			"consonants": [ 'z','z','ph','sh','r','n' ],
			"start": ['m'],
			"end": ['x','n'],
			"vowels": [ "e","e","e","a","i","i","u","o", ],
			"length": (2,4),
	}
}
```

然後您可以使用 `namegen.fantasy_name(style="example_style")` 產生遵循該規則集的名稱。

鍵 `syllable`、`consonants`、`vowels` 和 `length` 必須存在，且 `length` 必須是最小和最大音節數。 `start` 和 `end` 是可選的。


(syllable)=
#### 音節
“音節”欄位定義每個音節的結構。 C是子音，V是母音，
和括號表示它是可選的。所以，例子`(C)VC`意味著每個音節
總是有一個母音後面跟著一個子音，並且*有時*會有另一個
開頭是子音。 e.g。 `en`、`bak`

*注意：* 雖然它不是標準的，但 contrib 允許您在每一層中巢狀括號
不太可能出現。此外，放入音節中的任何其他字元
結構 - e.g。撇號 - 將以書寫方式讀取和插入。的
模組中的「alien」樣式規則給了兩者的範例：音節結構為`C(C(V))(')(C)`
這會導致 `khq`、`xho'q` 和 `q'` 等音節的母音頻率比
`C(C)(V)(')(C)` 會給出。

(consonants)=
#### 子音
可供選擇的子音音素的簡單清單。多字元字串是
完全可以接受，例如“th”，但每個都將被視為單一子音。

該函式使用一種簡單的加權形式，使音素更有可能
透過將更多副本放入清單中來發生。

(start-and-end)=
#### 開始和結束
這些是音節第一個和最後一個字母的**可選**列表（如果它們是）
一個子音。您可以新增只能出現在開頭的附加子音
或音節末尾，或者您可以新增已定義子音的額外副本
增加音節開頭/結尾處的頻率。

例如，在上面的`example_style`中，我們有m的`start`，x和n的`end`。
與其餘子音/母音一起使用，這意味著您可以擁有 `mez` 的音節
但不能有 `zem`，並且可以有 `phex` 或 `phen`，但不能有 `xeph` 或 `neph`。

它們可以完全排除在自訂規則集中。

(vowels)=
#### 母音
母音是母音音素的簡單列表 - 與子音完全相同，但用於表示
母音選擇。單字元或多字元字串同樣可以。它使用相同的簡單加權系統
作為子音 - 您可以透過多次將任何給定母音放入清單中來增加其頻率。

(length)=
#### 長度
具有名稱可以具有的最小和最大音節數的元組。

設定此值時，請記住您的音節可以持續多久！ 4個音節可以
看起來不是很多，但如果你有一個 (C)(V)VC 結構，其中一個和
兩個字母的音素，每個音節最多可以包含八個字元。

----

<small>此檔案頁面是從`evennia\contrib\utils\name_generator\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
