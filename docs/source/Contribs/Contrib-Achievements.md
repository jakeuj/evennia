(achievements)=
# 成就

一個簡單但相當全面的成就追蹤系統。成就是使用普通的 Python 字典定義的，讓人想起核心原型系統，雖然預計您只會在角色或帳戶上使用它，但可以追蹤任何型別分類的物件。

contrib 提供了多種用於追蹤和存取成就的功能，以及用於檢視成就狀態的基本遊戲內指令。

(installation)=
## 安裝

此 contrib 需要建立一個或多個包含成就資料的模組檔案，然後將其新增至設定檔以使其可用。

> 請參閱下面有關「建立成就」的部分，以瞭解此模組中的內容。

```python
# in server/conf/settings.py

ACHIEVEMENT_CONTRIB_MODULES = ["world.achievements"]
```

為了允許玩家檢查他們的成就，您還需要將 `achievements` 指令新增至預設的角色和/或帳戶指令集中。

```python
# in commands/default_cmdsets.py

from evennia.contrib.game_systems.achievements.achievements import CmdAchieve

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        # ...
        self.add(CmdAchieve)
```

**可選** - 成就 contrib 預設將個人進度資料儲存在 `achievements` attribute 上，可透過 `obj.db.achievements` 檢視。您可以透過將 attribute（鍵，類別）元組指派給設定 `ACHIEVEMENT_CONTRIB_ATTRIBUTE` 來變更此設定

例子：
```py
# in settings.py

ACHIEVEMENT_CONTRIB_ATTRIBUTE = ("progress_data", "achievements")
```


(creating-achievements)=
## 創造業績

成就由在成就模組中的模組層級定義的簡單 Python 字典表示。

每個成就都需要定義某些特定的鍵才能正常運作，以及幾個可用於覆蓋預設值的可選鍵。

> 注意：當您透過contrib存取這些成就時，此處未描述的任何其他鍵都包含在成就資料中，因此您可以輕鬆新增自己的擴充功能。

(required-keys)=
#### 所需按鍵

- **名稱** (str)：成就的可搜尋名稱。不需要是唯一的。
- **category** (str)：可以推進該成就的條件類別或一般型別。通常這將是玩家的動作或結果。 e.g。您可以對殺死 10 隻老鼠的成就使用「失敗」類別。
- **追蹤**（字串或清單）：可以推進此成就的特定條件子集。 e.g。您可以在殺死 10 隻老鼠的成就上使用「老鼠」的追蹤值。一項成就還可以追蹤多個事物，例如殺死 10 隻老鼠或蛇。對於這種情況，指定要檢查的所有值的列表，e.g。 `["rat", "snake"]`

(optional-keys)=
#### 可選按鍵

- **key** (str)：*如果未設定，則預設值：變數名稱。 * 標識此成就的唯一、不區分大小寫的鍵。
> 注意：如果任何成就具有相同的唯一鍵，則只會載入*一個*。它不區分大小寫，但尊重標點符號 - “ten_rats”、“Ten_Rats”和“TEN_RATS”會衝突，但“ten_rats”和“十隻老鼠”不會衝突。
- **desc** (str)：成就較長的描述。其常見用途是說明文字或如何完成它的提示。
- **count** (int)：*如果未設定，則預設值：1* 為了完成該成就，該成就的要求需要建立的計數數量。 e.g。殺死 10 隻老鼠的 `"count"` 值為 `10`。對於使用「單獨」追蹤型別的成就，正在追蹤的*每個*專案必須達到此數字才能完成。
- **tracking_type** (str)：*如果未設定則預設值：`"sum"`* 有兩種有效的追蹤型別：「sum」（預設值）和「separate」。每次任何追蹤專案匹配時，`"sum"` 都會增加一個計數器。 `"separate"` 將為追蹤專案中的每個單獨專案提供一個計數器。 （「請參閱範例成就」部分以示範差異。）
- **先決條件**（字串或清單）：任何成就的“關鍵”，必須先完成該成就才能開始追蹤進度。


(example-achievements)=
### 成就範例

第一次登入即可獲得的簡單成就。該成就沒有任何先決條件，只需要完成一次即可完成。
```python
# This achievement has the unique key of "first_login_achieve"
FIRST_LOGIN_ACHIEVE = {
    "name": "Welcome!", # the searchable, player-friendly display name
    "desc": "We're glad to have you here.", # the longer description
    "category": "login", # the type of action this tracks
    "tracking": "first", # the specific login action
}
```

一個成就是總共殺死 10 隻老鼠，另一個是殺死 10 隻「可怕」老鼠，這需要先完成「殺死 10 隻老鼠」成就。在第一個成就完成之前，可怕的老鼠成就不會開始追蹤*任何*進度。
```python
# This achievement has the unique key of "ten_rats" instead of "achieve_ten_rats"
ACHIEVE_TEN_RATS = {
    "key": "ten_rats",
    "name": "The Usual",
    "desc": "Why do all these inns have rat problems?",
    "category": "defeat",
    "tracking": "rat",
    "count": 10,
}

ACHIEVE_DIRE_RATS = {
    "name": "Once More, But Bigger",
    "desc": "Somehow, normal rats just aren't enough any more.",
    "category": "defeat",
    "tracking": "dire rat",
    "count": 10,
    "prereqs": "ACHIEVE_TEN_RATS",
}
```

總共購買 5 個蘋果、橘子、*或*梨的成就。 「總和」追蹤型別意味著所有物品都統計在一起 - 因此可以透過購買 5 個蘋果、5 個梨、3 個蘋果、1 個柳橙和 1 個梨，或這三種水果的任何其他組合（總計為 5）來完成。

```python
FRUIT_FAN_ACHIEVEMENT = {
    "name": "A Fan of Fruit", # note, there is no desc here - that's allowed!
    "category": "buy",
    "tracking": ("apple", "orange", "pear"),
    "count": 5,
    "tracking_type": "sum", # this is the default, but it's included here for clarity
}
```

購買 5 個蘋果、柳橙和梨*各*即可獲得成就。 「單獨」追蹤型別意味著每個追蹤的專案都獨立於其他專案進行計數 - 因此您將需要 5 個蘋果、5 個橙子和 5 個梨子。
```python
FRUIT_BASKET_ACHIEVEMENT = {
    "name": "Fruit Basket",
    "desc": "One kind of fruit just isn't enough.",
    "category": "buy",
    "tracking": ("apple", "orange", "pear"),
    "count": 5,
    "tracking_type": "separate",
}
```


(usage)=
## 用法

為了在遊戲中使用成就contrib，您需要做的兩件主要事情是**追蹤成就**和**獲取成就資訊**。第一個是用函式 `track_achievements` 完成的；第二個可以用 `search_achievement` 或 `get_achievement` 完成。

(tracking-achievements)=
### 追蹤成就

(track_achievements)=
#### `track_achievements`

在您可能想要在成就中追蹤的遊戲機制中的任何操作或功能中，新增對 `track_achievements` 的呼叫以更新該玩家的成就進度。

使用先前的「殺死 10 隻老鼠」範例成就，您可能有一些在角色被擊敗時觸發的程式碼：為了舉例，我們假設我們在基本 Object 類別上有一個 `at_defeated` 方法，當物件被擊敗時會呼叫該方法。

新增成就追蹤可能看起來像這樣：

```python
# in typeclasses/objects.py

from contrib.game_systems.achievements import track_achievements

class Object(ObjectParent, DefaultObject):
    # ....

    def at_defeated(self, victor):
        """called when this object is defeated in combat"""
        # we'll use the "mob_type" tag-category as the tracked info
        # this way we can have rats named "black rat" and "brown rat" that are both rats
        mob_type = self.tags.get(category="mob_type")
        # only one mob was defeated, so we include a count of 1
        track_achievements(victor, category="defeated", tracking=mob_type, count=1)
```

如果玩家擊敗了標記為 `rat` 且 tag 類別為 `mob_type` 的東西，它現在將計入滅鼠成就。

您還可以將追蹤資訊硬編碼到您的遊戲中，以應對特殊或獨特的情況。例如，前面描述的成就 `FIRST_LOGIN_ACHIEVE` 將按如下方式追蹤：

```py
# in typeclasses/accounts.py
from contrib.game_systems.achievements import track_achievements

class Account(DefaultAccount):
    # ...

    def at_first_login(self, **kwargs):
        # this function is only called on the first time the account logs in
        # so we already know and can just tell the tracker that this is the first
        track_achievements(self, category="login", tracking="first")
```

`track_achievements` 函式也傳回一個值：該更新新完成的任何成就的可迭代鍵。您可以忽略該值，也可以將其用於e.g。向玩家傳送最新成就的訊息。

(getting-achievements)=
### 取得成就

取得特定成就資訊的主要方法是`get_achievement`，它採用已知的成就金鑰並傳回該成就的資料。

然而，為了處理更多變數和玩家友好的輸入，還有`search_achievement`，它不僅對按鍵進行部分匹配，還對成就的顯示名稱和描述進行部分匹配。

(get_achievement)=
#### `get_achievement`

用於從成就的唯一鍵檢索特定成就的資料的實用函式。它不能用於搜尋，但如果您已經擁有成就的金鑰 - 例如，從 `track_achievements` 的結果中 - 您可以透過這種方式檢索其資料。

(example)=
#### 例子：

```py
from evennia.contrib.game_systems.achievements import get_achievement

def toast(achiever, completed_list):
    if completed_list:
        # `completed_data` will be a list of dictionaries - unrecognized keys return empty dictionaries
        completed_data = [get_achievement(key) for key in args]
        names = [data.get('name') for data in completed]
        achiever.msg(f"|wAchievement Get!|n {iter_to_str(name for name in names if name)}"))
```

(search_achievement)=
#### `search_achievement`

用於按名稱或描述搜尋成就的實用功能。它處理部分匹配並返回匹配成就的字典。遊戲中提供的 `achievement` 指令使用此函式從使用者輸入中尋找匹配的成就。

(example-1)=
#### 例子：

第一個範例搜尋“fruit”，它會傳回水果混合成就，因為它的鍵和名稱中包含“fruit”。

第二個範例搜尋“usual”，它會根據其顯示名稱傳回十隻老鼠的成就。

```py
>>> from evennia.contrib.game_systems.achievements import search_achievement
>>> search_achievement("fruit")
{'fruit_basket_achievement': {'name': 'Fruit Basket', 'desc': "One kind of fruit just isn't enough.", 'category': 'buy', 'tracking': ('apple', 'orange', 'pear'), 'count': 5, 'tracking_type': 'separate'}}
>>> search_achievement("usual")
{'ten_rats': {'key': 'ten_rats', 'name': 'The Usual', 'desc': 'Why do all these inns have rat problems?', 'category': 'defeat', 'tracking': 'rat', 'count': 10}}
```

(the-achievements-command)=
### `achievements`指令

contrib 提供的指令 `CmdAchieve` 旨在按原樣使用，具有多個開關以按各種進度狀態過濾成就以及按成就名稱搜尋的能力。

為了更輕鬆地針對您自己的遊戲進行自訂（e.g。顯示您可能新增的一些額外成就資料），格式和樣式程式碼從指令邏輯中拆分為 `format_achievement` 方法和 `template` attribute，兩者都在 `CmdAchieve` 上

(example-output)=
#### 輸出範例

```
> achievements
The Usual
Why do all these inns have rat problems?
70% complete
A Fan of Fruit

Not Started
```
```
> achievements/progress
The Usual
Why do all these inns have rat problems?
70% complete
```
```
> achievements/done
There are no matching achievements.
```


----

<small>此檔案頁面是從`evennia\contrib\game_systems\achievements\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
