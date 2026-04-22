(code-structure-and-utilities)=
# 程式碼結構和實用程式

在本課中，我們將為 _EvAdventure_ 設定檔案結構。我們會做一些
以後會用到的實用程式。我們也將學習如何寫_測試_。

(folder-structure)=
## 資料夾結構

```{sidebar} 此佈局適用於教學！
我們將 `evadventure` 資料夾設為獨立資料夾只是為了教學的目的。以這種方式隔離程式碼可以清楚地表明我們更改了什麼 –並讓您稍後可以獲得您想要的東西。它還可以更輕鬆地引用 `evennia/contrib/tutorials/evadventure` 中的匹配程式碼。

對於您自己的遊戲，建議您就地修改遊戲目錄（i.e，直接新增到`commands/commands.py`並直接修改`typeclasses/`模組）。事實上，除了 `server/` 資料夾之外，您幾乎可以按照自己的喜好自由地建立遊戲目錄程式碼。
```
在 `mygame` 資料夾下建立一個名為 `evadventure` 的新資料夾。在新資料夾中，建立另一個名為 `tests/` 的資料夾。確保將空的 `__init__.py` 檔案放入兩個新資料夾中。這樣做會將兩個新資料夾轉換為 Python 能夠自動匯入的套件。

```
mygame/
   commands/
   evadventure/         <---
      __init__.py       <---
      tests/            <---
          __init__.py   <---
   __init__.py
   README.md
   server/
   typeclasses/
   web/
   world/

```

從 `mygame` 下的任何其他位置匯入此資料夾內的任何內容將透過以下方式完成

```python
# from anywhere in mygame/
from evadventure.yourmodulename import whatever
```

這是匯入的“絕對路徑”型別。

在 `evadventure/` 中的兩個模組之間，您可以使用 `.` 的「相對」匯入：

```python
# from a module inside mygame/evadventure
from .yourmodulename import whatever
```

來自e.g。在 `mygame/evadventure/tests/` 內，您可以使用 `..` 從上面的一級匯入：

```python
# from mygame/evadventure/tests/
from ..yourmodulename import whatever
```


(enums)=
## 列舉

```{sidebar}
列舉模組的完整範例位於
[evennia/contrib/tutorials/evadventure/enums.py](../../../api/evennia.contrib.tutorials.evadventure.enums.md)。
```
建立一個新檔案`mygame/evadventure/enums.py`。

[enum](https://docs.python.org/3/library/enum.html)（列舉）是 Python 中建立常數的一種方法。例如：

```python
# in a file mygame/evadventure/enums.py

from enum import Enum

class Ability(Enum):

    STR = "strength"

```

然後您可以像這樣存取列舉：

```
# from another module in mygame/evadventure

from .enums import Ability

Ability.STR   # the enum itself
Ability.STR.value  # this is the string "strength"

```

使用列舉是建議的做法。設定列舉後，我們可以確保每次都引用相同的常數或變數。將所有列舉儲存在一個位置也意味著我們可以很好地瞭解正在處理的常數。

例如，列舉的替代方法是傳遞名為 `"constitution"` 的字串。如果您將其錯誤拼寫為 `"consitution"`，您不一定會立即知道它，因為稍後當無法識別字串時會發生錯誤。透過使用列舉實踐，如果您輸入錯誤，得到 `Ability.COM` 而不是 `Ability.CON`，Python 將立即引發錯誤，因為該錯誤的列舉將無法被識別。

使用列舉，您還可以進行很好的直接比較，例如 `if ability is Ability.WIS: <do stuff>`。

請注意，`Ability.STR` 列舉沒有實際的_值_，例如你的力量。 `Ability.STR`只是力量能力的固定標籤。

下面是_Knave_所需的`enum.py`模組。它涵蓋了我們需要追蹤的規則系統的基本方面。 （請參閱 _Knave_ 規則。）如果您稍後使用另一個規則系統，當您弄清楚您需要什麼時，您可能會逐漸擴充套件您的列舉。

```python
# mygame/evadventure/enums.py

class Ability(Enum):
    """
    The six base ability-bonuses and other
    abilities

    """

    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHA = "charisma"

    ARMOR = "armor"

    CRITICAL_FAILURE = "critical_failure"
    CRITICAL_SUCCESS = "critical_success"

    ALLEGIANCE_HOSTILE = "hostile"
    ALLEGIANCE_NEUTRAL = "neutral"
    ALLEGIANCE_FRIENDLY = "friendly"


ABILITY_REVERSE_MAP =  {
    "str": Ability.STR,
    "dex": Ability.DEX,
    "con": Ability.CON,
    "int": Ability.INT,
    "wis": Ability.WIS,
    "cha": Ability.CHA
}

```

上面，`Ability` 類別儲存了字元表的一些基本屬性。

`ABILITY_REVERSE_MAP` 是將字串轉換為列舉的便捷對映。最常見的用法是在指令中；玩家對列舉一無所知，他們只能傳送字串。所以我們只能得到字串“cha”。使用這個 `ABILITY_REVERSE_MAP` 我們可以輕鬆地將此輸入轉換為 `Ability.CHA` 列舉，然後您可以在程式碼中傳遞

    ability = ABILITY_REVERSE_MAP.get(user_input)


(utility-module)=
## 實用模組

> 建立一個新模組`mygame/evadventure/utils.py`

```{sidebar}
實用程式模組的範例位於
[evennia/contrib/tutorials/evadventure/utils.py](../../../api/evennia.contrib.tutorials.evadventure.utils.md)
```

實用程式模組用於包含我們可能需要從各種其他模組重複呼叫的通用函式。在本教學範例中，我們只建立一個實用程式：一個函式，它可以為我們傳遞給它的任何物件產生漂亮的顯示。

它看起來是這樣的：

```python
# in mygame/evadventure/utils.py

_OBJ_STATS = """
|c{key}|n
Value: ~|y{value}|n coins{carried}

{desc}

Slots: |w{size}|n, Used from: |w{use_slot_name}|n
Quality: |w{quality}|n, Uses: |w{uses}|n
Attacks using |w{attack_type_name}|n against |w{defense_type_name}|n
Damage roll: |w{damage_roll}|n
""".strip()


def get_obj_stats(obj, owner=None):
    """
    Get a string of stats about the object.

    Args:
        obj (Object): The object to get stats for.
        owner (Object): The one currently owning/carrying `obj`, if any. Can be
            used to show e.g. where they are wielding it.
    Returns:
        str: A nice info string to display about the object.

    """
    return _OBJ_STATS.format(
        key=obj.key,
        value=10,
        carried="[Not carried]",
        desc=obj.db.desc,
        size=1,
        quality=3,
        uses="infinite",
        use_slot_name="backpack",
        attack_type_name="strength",
        defense_type_name="armor",
        damage_roll="1d6"
    )
```

在先前的教學課程中，我們已經看到 `"""... """` 多行字串主要用於函式幫助字串，但 Python 中的三引號字串可用於任何多行字串。

上面，我們設定了一個字串模板 (`_OBJ_STATS`)，其中包含佔位符 (`{...}`)，用於表示統計資訊的每個元素應存放的位置。然後，在 `_OBJ_STATS.format(...)` 呼叫中，我們用傳遞到 `get_obj_stats` 的物件中的資料動態填入這些佔位符。

如果您將一把「缺口劍」傳遞給 `get_obj_stats`，您會得到以下結果（請注意，這些檔案不顯示文字顏色）：

```
Chipped Sword
Value: ~10 coins [wielded in Weapon hand]

A simple sword used by mercenaries all over
the world.

Slots: 1, Used from: weapon hand
Quality: 3, Uses: None
Attacks using strength against armor.
Damage roll: 1d6
```

稍後我們將使用它來讓玩家檢查任何物件，而無需為每種物件型別建立一個新的實用程式。

研究 `_OBJ_STATS` 模板字串，以便了解它的作用。 `|c`、`|y`、`|w` 和 `|n` 標記是 [Evennia 顏色標記](../../../Concepts/Colors.md)，分別用於使文字變為青色、黃色、白色和中性色。

在上面的程式碼中很容易識別一些統計元素。例如，`obj.key` 是物件的名稱，`obj.db.desc` 將儲存物件的描述 -這也是預設 Evennia 的工作原理。

到目前為止，在我們的教學中，我們尚未確定如何獲得任何其他屬性，例如 `size`、`damage_roll` 或 `attack_type_name`。出於我們目前的目的，我們只需將它們設定為固定的虛擬值，以便它們可以運作。當我們有更多程式碼時，我們需要稍後重新訪問它們！

(testing)=
## 測試

Evennia 具有豐富的功能來幫助您測試程式碼。 _單元測試_允許您設定程式碼的自動化測試。編寫測試後，您可以一遍又一遍地執行它，以確保以後對程式碼的更改不會因引入錯誤而破壞事物。

> 建立一個新模組`mygame/evadventure/tests/test_utils.py`

您怎麼知道上面的程式碼中是否有拼字錯誤？您可以透過重新載入 Evennia 伺服器並發出以下遊戲內 python 指令來_手動_測試它：

    py from evadventure.utils import get_obj_stats;print(get_obj_stats(self))

這樣做應該會回傳一些關於你自己的字串輸出！如果有效的話，那就太好了！但是，當您稍後更改程式碼時，您需要記住手動重新執行該測試。

```{sidebar}
在[evennia/contrib/tutorials/evadventure/tests/test_utils.py](evennia.contrib.tutorials.evadventure.tests.test_utils)中
是測試模組的一個範例。若要深入瞭解 Evennia 中的單元測試，請參閱[單元測試](../../../Coding/Unit-Testing.md) 檔案。
```

在本教學的特定情況下，當 `get_obj_stats` 程式碼變得更加完整並傳回更多相關資料時，我們應該_期望_需要稍後更新測試。

這是用於測試`get_obj_stats`的模組。

```python
# mygame/evadventure/tests/test_utils.py

from evennia.utils import create
from evennia.utils.test_resources import EvenniaTest

from ..import utils

class TestUtils(EvenniaTest):
    def test_get_obj_stats(self):
        # make a simple object to test with
        obj = create.create_object(
            key="testobj",
            attributes=(("desc", "A test object"),)
        )
        # run it through the function
        result = utils.get_obj_stats(obj)
        # check that the result is what we expected
        self.assertEqual(
            result,
            """
|ctestobj|n
Value: ~|y10|n coins[Not carried]

A test object

Slots: |w1|n, Used from: |wbackpack|n
Quality: |w3|n, Uses: |winfinite|n
Attacks using |wstrength|n against |warmor|n
Damage roll: |w1d6|n
""".strip()
)

```

上面程式碼中發生的情況是，我們建立了一個名為 `TestUtils` 的新測試類，它繼承自 `EvenniaTest`。正是這種繼承使其成為測試類別。


```{important}
對於任何遊戲開發人員來說，瞭解如何有效地測試他們的程式碼都是很有用的。因此，我們將嘗試在本教學中的每個實施課程的末尾新增*測試*部分。

為程式碼編寫測試是可選的，但強烈建議這樣做。最初，單元測試可能會感覺有點麻煩或耗時……但稍後您會感謝自己。
```

我們可以在這個類別上呼叫任意數量的方法。要讓 Evennia 自動將方法識別為包含要測試的程式碼的方法，其名稱_必須_以 `test_` 字首開頭。我們這裡有一個 `test_get_obj_stats`。

在我們的 `test_get_obj_stats` 方法中，我們建立一個虛擬 `obj` 並為其分配一個 `key`「testobj」。請注意，我們透過將 attribute 指定為元組 `(name, value)`，直接在 `create_object` 呼叫中加入`desc` [Attribute](../../../Components/Attributes.md)！

然後，我們可以得到透過我們先前匯入的 `get_obj_stats` 函式傳遞這個虛擬物件的結果。

`assertEqual` 方法可用於所有測試類，並檢查 `result` 是否等於我們指定的字串。如果它們相同，則測試_透過_。否則，它就會_失敗_，我們需要調查出了什麼問題。

(running-your-test)=
### 執行你的測試

要執行我們的實用程式模組測試，我們需要直接從 `mygame` 資料夾發出以下指令：

    evennia test --settings settings.py evadventure.tests

上述指令將執行在 `mygame/evadventure/tests` 資料夾中找到的所有 `evadventure` 測試。要僅執行我們的實用程式測試，我們可以單獨指定測試：

    evennia test --settings settings.py evadventure.tests.test_utils

如果一切順利，上述實用程式測試應該會產生以 `OK` 結尾的輸出，表示我們的程式碼已透過測試。

但是，如果我們的返回字串與我們的預期不完全匹配，則測試將失敗。然後我們需要開始檢查失敗的程式碼並排除故障。

> 提示：上面的範例單元測試程式碼包含故意的大小寫錯誤。看看是否可以檢查輸出來解釋故意的錯誤，然後修復它！

(summary)=
## 概括

瞭解如何在 Python 的模組之間匯入程式碼非常重要。如果從 Python 模組匯入仍然讓您感到困惑，那麼值得閱讀更多關於該主題的內容。

也就是說，許多新手對如何處理這些概念感到困惑。在本課程中，透過建立資料夾結構、兩個小模組，甚至進行我們的第一個單元測試，您將有一個良好的開始！
