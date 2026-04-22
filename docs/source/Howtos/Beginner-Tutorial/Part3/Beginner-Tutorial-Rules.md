(rules-and-dice-rolling)=
# 規則和骰子滾動

在_EvAdventure_中我們決定使用[Knave](https://www.drivethrurpg.com/product/250888/Knave)
RPG 規則集。這是商業性的，但在 Creative Commons 4.0 下發布，這意味著可以分享和
使_Knave_適應任何目的，甚至商業用途。如果你不想買但仍關注
另外，您可以在這裡找到[免費粉絲版本](http://abominablefancy.blogspot.com/2018/10/knaves-fancypants.html)。

(summary-of-_knave_-rules)=
## _Knave_ 規則摘要

Knave 受到早期龍與地下城的啟發，非常簡單。

- 它使用六種能力獎勵
_力量_ (STR)、_敏捷_ (DEX)、_體質_ (CON)、_智力_ (INT)、_智慧_ (WIS)
和_魅力_ (CHA)。這些評級從 `+1` 到 `+10`。
- 骰子是用二十面骰子（`1d20`）製成的，通常會為骰子新增適當的能力加值。
- 如果你投_有優勢_，你投 `2d20` 並選擇
_最高_值，如果你投擲_有劣勢_，你投擲`2d20`並選擇_最低_。
- 滾動自然的 `1` 是_嚴重失敗_。自然的 `20` 是_關鍵的成功_。滾動這樣的
在戰鬥中意味著你的武器或盔甲失去質量，最終會摧毀它。
- _saving throw_（試圖在環境中取得成功）意味著進行一次擲骰以擊敗`15`（總是）。
因此，如果您舉起一塊重石並且有 `STR +2`，您會滾動 `1d20 + 2` 並希望結果
高於`15`。
- _對抗豁免_意味著擊敗敵人合適的能力“防禦”，這始終是他們的
`Ability bonus + 10`。因此，如果你有 `STR +1` 並且正在和有 `STR +2` 的人扳手腕，你會擲骰子
`1d20 + 1`並希望滾動高於`2 + 10 = 12`。
- 特殊加成是`Armor`，`+1`是無甲的，額外的甲值是由裝備賦予的。近戰攻擊
測試 `STR` 與 `Armor` 防禦值，而遠端攻擊使用 `WIS` 與 `Armor`。
- _Knave_沒有技能或職業。每個人都可以使用所有物品，並且使用魔法意味著擁有特殊的
你手中的『符文石』；每石頭一天一個咒語。
- 一個字元有 `CON + 10` 帶有“槽”。大多數普通物品使用一個插槽，盔甲和大型武器使用
兩個或三個。
- 治療是隨機的，食物和睡眠後`1d8 + CON`的健康得到治癒。
- 怪物難度按他們擁有的眾多1d8 HP列出；這被稱為「擊中骰子」或HD。如果
需要測試能力，怪物每項能力都有HD加成。
- 怪物有_士氣等級_。當事情變壞時，他們有機會驚慌並逃跑，如果
士氣評級滾動`2d6`。
- _Knave_ 中的所有角色大多是隨機產生的。 HP 是 `<level>d8` 但我們給每一個
新角色最多 HP 開始。
- _Knave_也有隨機表，例如用於啟動裝置以及檢視何時死亡
擊中 0。死亡，如果發生，是永久性的。


(making-a-rule-module)=
## 製作規則模組

> 建立一個新模組mygame/evadventure/rules.py

```{sidebar}
規則模組的完整版本位於
[evennia/contrib/tutorials/evadventure/rules.py](../../../api/evennia.contrib.tutorials.evadventure.rules.md)。
```
對於大多數 RPGS 來說，有三組廣泛的規則：

- 角色生成規則，通常僅在角色建立過程中使用
- 常規遊戲規則 - 擲骰子並解決遊戲狀況
- 角色提升 - 獲取並花費經驗來提升角色

我們希望我們的 `rules` 模組能夠涵蓋我們原本必須查詢的盡可能多的方面
在規則手冊中。


(rolling-dice)=
## 擲骰子

我們將從製作一個骰子開始。讓我們將所有骰子組合成這樣的結構
（還不是功能程式碼）：

```python 
class EvAdventureRollEngine:

   def roll(...):
       # get result of one generic roll, for any type and number of dice
       
   def roll_with_advantage_or_disadvantage(...)
       # get result of normal d20 roll, with advantage/disadvantage (or not)
       
   def saving_throw(...):
       # do a saving throw against a specific target number
       
   def opposed_saving_throw(...):
       # do an opposed saving throw against a target's defense

   def roll_random_table(...):
       # make a roll against a random table (loaded elsewere)
  
   def morale_check(...):
       # roll a 2d6 morale check for a target
      
   def heal_from_rest(...):
       # heal 1d8 when resting+eating, but not more than max value.
       
   def roll_death(...):
       # roll to determine penalty when hitting 0 HP. 
       
       
dice = EvAdventureRollEngine() 
       
```
```{sidebar}
這會將所有與骰子相關的程式碼分組到一個易於匯入的「容器」中。但這主要是一個問題
的味道。您也_可以_將類別的方法分解為頂層的普通函式
模組，如果你想要的話。
```

這種結構（稱為 _singleton_）意味著我們將所有骰子分為一個類，然後啟動該類
到模組末尾的變數 `dice` 中。這意味著我們可以從其他地方做以下事情
模組：

```python
    from .rules import dice 

    dice.roll("1d8")
```

(generic-dice-roller)=
### 通用骰子滾輪

我們希望能夠執行 `roll("1d20")` 並從擲骰中獲得隨機結果。

```python
# in mygame/evadventure/rules.py 

from random import randint

class EvAdventureRollEngine:
    
    def roll(self, roll_string):
        """ 
        Roll XdY dice, where X is the number of dice 
        and Y the number of sides per die. 
        
        Args:
            roll_string (str): A dice string on the form XdY.
        Returns:
            int: The result of the roll. 
            
        """ 
        
        # split the XdY input on the 'd' one time
        number, diesize = roll_string.split("d", 1)     
        
        # convert from string to integers
        number = int(number) 
        diesize = int(diesize)
            
        # make the roll
        return sum(randint(1, diesize) for _ in range(number))
```

```{sidebar}
對於本教學，我們選擇不使用任何 contribs，因此我們建立
我們自己的骰子滾輪。但通常你可以用[骰子](../../../Contribs/Contrib-Dice.md)contrib來代替。 
當我們繼續進行時，我們將在側邊欄中指出可能有幫助的contribs。
```

`randint` 標準 Python 函式庫模組產生一個隨機整數
在特定範圍內。線路

```python 
sum(randint(1, diesize) for _ in range(number))
```
工作原理如下：

- 對於特定的 `number` 次...
- ....建立 `1` 和 `diesize` 之間的隨機整數...
- ...和 ​​`sum` 所有這些整數在一起。

您可以像這樣不那麼緊湊地編寫相同的內容：

```python 
rolls = []
for _ in range(number): 
   random_result = randint(1, diesize)
   rolls.append(random_result)
return sum(rolls)
```

```{sidebar}
請注意，`range` 產生值 `0...number-1`。我們在 `for` 迴圈中使用 `_` 來
表明我們並不真正關心這個值是什麼 - 我們只是想重複迴圈
一定次數。
```

我們不希望終端使用者呼叫此方法；如果我們這樣做，我們將必須驗證輸入
更多 - 我們必須確保 `number` 或 `diesize` 是有效輸入，而不是
太瘋狂了，所以迴圈需要永遠！

(rolling-with-advantage)=
### 滾動優勢

現在我們有了通用滾筒，我們可以開始使用它來進行更複雜的滾動。

```python
# in mygame/evadventure/rules.py 

# ... 

class EvAdventureRollEngine:

    def roll(roll_string):
        # ... 
    
    def roll_with_advantage_or_disadvantage(self, advantage=False, disadvantage=False):
        
        if not (advantage or disadvantage) or (advantage and disadvantage):
            # normal roll - advantage/disadvantage not set or they cancel 
            # each other out 
            return self.roll("1d20")
        elif advantage:
             # highest of two d20 rolls
             return max(self.roll("1d20"), self.roll("1d20"))
        else:
             # disadvantage - lowest of two d20 rolls 
             return min(self.roll("1d20"), self.roll("1d20"))
```

`min()` 和 `max()` 函式是取得最大/最小的標準 Python 函式
兩個引數。

(saving-throws)=
### 豁免檢定

我們希望豁免檢定本身能夠確定它是否成功。這意味著它需要知道
能力加值（如STR `+1`）。如果我們可以直接傳遞實體的話會很方便
對此方法進行儲存丟擲，告訴它需要什麼型別的儲存，然後
讓它弄清楚事情：

```python 
result, quality = dice.saving_throw(character, Ability.STR)
```
如果透過，返回值將是布林值 `True/False`，以及告訴我們是否透過的 `quality`
是否有完美的失敗/成功。

為了使儲存方法變得如此聰明，我們需要更多地考慮如何儲存我們的
有關角色的資料。

就我們的目的而言，我們將使用 [屬性](../../../Components/Attributes.md) 來儲存聽起來很合理
能力得分。為了方便起見，我們將它們命名為與
我們在上一課中設定的[列舉值](./Beginner-Tutorial-Utilities.md#enums)。所以如果我們有
列舉 `STR = "strength"`，我們希望將角色的能力儲存為 Attribute `strength`。

從Attribute檔案中，我們可以看到我們可以使用`AttributeProperty`來使其
Attribute 可用作 `character.strength`，這就是我們要做的。

因此，簡而言之，我們將建立儲存丟擲方法，假設我們能夠執行以下操作
`character.strength`、`character.constitution`、`character.charisma` 等以獲得相關能力。

```python 
# in mygame/evadventure/rules.py 
# ...
from .enums import Ability

class EvAdventureRollEngine: 

    def roll(...)
        # ...
   
    def roll_with_advantage_or_disadvantage(...)
        # ...
       
    def saving_throw(self, character, bonus_type=Ability.STR, target=15, 
                     advantage=False, disadvantage=False):
        """ 
        Do a saving throw, trying to beat a target.
       
        Args:
           character (Character): A character (assumed to have Ability bonuses
               stored on itself as Attributes).
           bonus_type (Ability): A valid Ability bonus enum.
           target (int): The target number to beat. Always 15 in Knave.
           advantage (bool): If character has advantage on this roll.
           disadvantage (bool): If character has disadvantage on this roll.
          
        Returns:
            tuple: A tuple (bool, Ability), showing if the throw succeeded and 
                the quality is one of None or Ability.CRITICAL_FAILURE/SUCCESS
               
        """
                    
        # make a roll 
        dice_roll = self.roll_with_advantage_or_disadvantage(advantage, disadvantage)
       
        # figure out if we had critical failure/success
        quality = None
        if dice_roll == 1:
            quality = Ability.CRITICAL_FAILURE
        elif dice_roll == 20:
            quality = Ability.CRITICAL_SUCCESS 

        # figure out bonus
        bonus = getattr(character, bonus_type.value, 1) 

        # return a tuple (bool, quality)
        return (dice_roll + bonus) > target, quality
```

`getattr(obj, attrname, default)` 函式是一個非常有用的 Python 工具，用於取得 attribute
如果未定義 attribute，則關閉物件並取得預設值。

(opposed-saving-throw)=
### 反對豁免

使用我們已經建立的建置區塊，此方法很簡單。請記住，你擁有的防禦力
在_Knave_中擊敗始終是相關獎金+10。所以如果敵人用`STR +3`防禦，你必須
滾動高於`13`。

```python
# in mygame/evadventure/rules.py 

from .enums import Ability

class EvAdventureRollEngine:
    
    def roll(...):
        # ... 

    def roll_with_advantage_or_disadvantage(...):
        # ... 

    def saving_throw(...):
        # ... 

    def opposed_saving_throw(self, attacker, defender, 
                             attack_type=Ability.STR, defense_type=Ability.ARMOR,
                             advantage=False, disadvantage=False):
        defender_defense = getattr(defender, defense_type.value, 1) + 10 
        result, quality = self.saving_throw(attacker, bonus_type=attack_type,
                                            target=defender_defense, 
                                            advantage=advantage, disadvantage=disadvantage)
        
        return result, quality 
```

(morale-check)=
### 士氣檢查

我們將假設 `morale` 值可以從生物中簡單地獲得
`monster.morale` - 我們需要記住稍後再做！

在_Knave_中，生物的`2d6`士氣等於或低於其士氣時，不會逃跑或投降
當事情向南發展時。標準士氣值為 9。

```python 
# in mygame/evadventure/rules.py 

class EvAdventureRollEngine:

    # ...
    
    def morale_check(self, defender): 
        return self.roll("2d6") <= getattr(defender, "morale", 9)
    
```

(roll-for-healing)=
### 滾動治療

為了能夠處理治癒，我們需要對如何儲存做出更多假設
遊戲實體的健康狀況。我們將需要`hp_max`（可用總量HP）和`hp`
（當前健康值）。我們再次假設這些將作為 `obj.hp` 和 `obj.hp_max` 提供。

根據規則，角色在吃完口糧並睡了一整夜後，會恢復
`1d8 + CON` HP。

```python 
# in mygame/evadventure/rules.py 

from .enums import Ability

class EvAdventureRollEngine: 

    # ... 
    
    def heal_from_rest(self, character): 
        """ 
        A night's rest retains 1d8 + CON HP  
        
        """
        con_bonus = getattr(character, Ability.CON.value, 1)
        character.heal(self.roll("1d8") + con_bonus)
```

我們在這裡做出另一個假設 - `character.heal()` 是一個東西。我們告訴這個函式如何
角色應該要治癒很多，並且它會這樣做，並確保治癒的量不會超過其最大值
HP數量

> 知道角色上有什麼可用的以及我們需要什麼規則，這有點像先有雞還是先有蛋的問題
> 問題。我們將確保下一課實現匹配的 _Character_ 類別。


(rolling-on-a-table)=
### 在桌子上打滾

我們有時需要在“桌子”上滾動——一系列選擇。有兩種主要的表型別
我們需要支援：

只需表格的每一行一個元素（獲得每個結果的機率相同）。

| 結果 |
|:------:|
| 專案1  |
| 專案2  | 
| 專案3  | 
| 專案4  | 

我們將簡單地表示為一個簡單的列表
    
```python
["item1", "item2", "item3", "item4"]
```

每個專案的範圍（每個結果的賠率不同）：

| 範圍 | 結果 | 
|:-----:|:------:|
|  1-5  | 專案1  |
| 6-15  | 專案2  |
| 16-19 | 專案3  |
|  20   | 專案4  |

我們將其表示為元組列表：

```python
[("1-5", "item1"), ("6-15", "item2"), ("16-19", "item4"), ("20", "item5")]
```

我們還需要知道要擲什麼骰子才能得到結果（可能並非總是如此）
顯而易見，在某些遊戲中，您可能會被要求擲較低的骰子才能獲得
例如，早期的表格結果）。

```python
# in mygame/evadventure/rules.py 

from random import randint, choice

class EvAdventureRollEngine:
    
    # ... 

    def roll_random_table(self, dieroll, table_choices): 
        """ 
        Args: 
             dieroll (str): A die roll string, like "1d20".
             table_choices (iterable): A list of either single elements or 
                of tuples.
        Returns: 
            Any: A random result from the given list of choices.
            
        Raises:
            RuntimeError: If rolling dice giving results outside the table.
            
        """
        roll_result = self.roll(dieroll) 
        
        if isinstance(table_choices[0], (tuple, list)):
            # the first element is a tuple/list; treat as on the form [("1-5", "item"),...]
            for (valrange, choice) in table_choices:
                minval, *maxval = valrange.split("-", 1)
                minval = abs(int(minval))
                maxval = abs(int(maxval[0]) if maxval else minval)
                
                if minval <= roll_result <= maxval:
                    return choice 
                
            # if we get here we must have set a dieroll producing a value 
            # outside of the table boundaries - raise error
            raise RuntimeError("roll_random_table: Invalid die roll")
        else:
            # a simple regular list
            roll_result = max(1, min(len(table_choices), roll_result))
            return table_choices[roll_result - 1]
```
檢查您是否理解它的作用。

這可能會令人困惑：
```python
minval, *maxval = valrange.split("-", 1)
minval = abs(int(minval))
maxval = abs(int(maxval[0]) if maxval else minval)
```

如果 `valrange` 是字串 `1-5`，則 `valrange.split("-", 1)` 將產生元組 `("1", "5")`。 
但如果字串實際上只是 `"20"`（可能是 RPG 表中的單一條目），這將
導致錯誤，因為它只會分裂出一個元素 - 而我們期望兩個。

透過使用 `*maxval` （與 `*` 一起），`maxval` 被告知元組中需要 _0 個或更多_ 元素。 
因此 `1-5` 的結果將是 `("1", ("5",))`，而 `20` 的結果將變為 `("20", ())`。在行

```python
maxval = abs(int(maxval[0]) if maxval else minval)
```

我們檢查 `maxval` 實際上是否有值 `("5",)` 或它是否為空 `()`。結果是
`"5"` 或 `minval` 的值。


(roll-for-death)=
### 滾動死亡

雖然原始的無賴建議擊中 0 HP 意味著立即死亡，但我們將從“美化”無賴的可選規則中獲取可選的“死亡表”，以使其懲罰減輕一些。我們還將 `2` 的結果更改為“死亡”，因為我們在本教學中不模擬“肢解”：

| 卷 |  結果  | -1d4 喪失能力 | 
|:---: |:--------:|:--------------------:|
| 1-2 | 1-2 死了| -
| 3 | 削弱 |         STR          | 
|4 | 不穩定的 |         DEX          | 
| 5 | 病態的 |         CON          | 
| 6 | 糊塗的 |         INT          | 
| 7 | 驚慌的 |         WIS          | 
| 8 | 毀容的 |         CHA          |

所有非死亡值都對映到六種能力之一的 1d4 損失（但你會得到 HP 恢復）。我們需要從上表中對映回這一點。一個人的能力加值也不能低於-10，如果這樣做，你也會死。

```python 
# in mygame/evadventure/rules.py 

death_table = (
    ("1-2", "dead"),
    ("3", "strength"),
    ("4", "dexterity"),
    ("5", "constitution"),
    ("6", "intelligence"),
    ("7", "wisdom"),
    ("8", "charisma"),
)
    
    
class EvAdventureRollEngine:
    
    # ... 

    def roll_random_table(...)
        # ... 
        
    def roll_death(self, character): 
        ability_name = self.roll_random_table("1d8", death_table)

        if ability_name == "dead":
            # TODO - kill the character! 
            pass 
        else: 
            loss = self.roll("1d4")
            
            current_ability = getattr(character, ability_name)
            current_ability -= loss
            
            if current_ability < -10: 
                # TODO - kill the character!
                pass 
            else:
                # refresh 1d4 health, but suffer 1d4 ability loss
                self.heal(character, self.roll("1d4"))
                setattr(character, ability_name, current_ability)
                
                character.msg(
                    "You survive your brush with death, and while you recover "
                    f"some health, you permanently lose {loss} {ability_name} instead."
                )
                
dice = EvAdventureRollEngine()
```

在這裡，我們根據規則滾動“死亡表”，看看會發生什麼。我們賦予角色
如果他們倖存，就會收到一條訊息，讓他們知道發生了什麼事。

我們還不知道「殺死角色」在技術上意味著什麼，所以我們將其標記為 `TODO` 並在後面的課程中返回它。我們只知道我們需要在這裡做點什麼來殺死這個角色！

(testing)=
## 測試

> 建立一個新模組`mygame/evadventure/tests/test_rules.py`

測試`rules`模組也會在測試時展示一些非常有用的工具。

```python 
# mygame/evadventure/tests/test_rules.py 

from unittest.mock import patch 
from evennia.utils.test_resources import BaseEvenniaTest
from .. import rules 

class TestEvAdventureRuleEngine(BaseEvenniaTest):
   
    def setUp(self):
        """Called before every test method"""
        super().setUp()
        self.roll_engine = rules.EvAdventureRollEngine()
    
    @patch("evadventure.rules.randint")
    def test_roll(self, mock_randint):
        mock_randint.return_value = 4 
        self.assertEqual(self.roll_engine.roll("1d6"), 4)     
        self.assertEqual(self.roll_engine.roll("2d6"), 2 * 4)     
        
    # test of the other rule methods below ...
```

和以前一樣，執行特定測試

    evennia test --settings settings.py evadventure.tests.test_rules

(mocking-and-patching)=
### 模擬和修補

```{sidebar}
在[evennia/contrib/tutorials/evadventure/tests/test_rules.py](../../../api/evennia.contrib.tutorials.evadventure.tests.test_rules.md)中
有一個完整的規則測試範例。
```
`setUp`方法是測試類別的特殊方法。 It will be run before every
測試方法。我們使用 `super().setUp()` 來確定該方法的父類別版本
總是火。 Then we create a fresh `EvAdventureRollEngine` we can test with.

在我們的測試中，我們從 `unittest.mock` 庫匯入 `patch`。這是一個非常有用的測試工具。 
通常我們在`rules`中匯入的`randint`函式會傳回一個隨機值。這很難測試，因為每次測試的值都會不同。

使用`@patch`（這稱為_decorator_），我們暫時用「模擬」（虛擬實體）取代`rules.randint`。該模擬被傳遞到測試方法中。然後我們將`mock_randint`設定為`.return_value = 4`。

將 `return_value` 新增到模擬中意味著每次呼叫此模擬時，它將返回 4。在測試期間，我們現在可以使用 `self.assertEqual` 檢查我們的 `roll` 方法是否始終傳回結果，就好像隨機結果是 4 一樣。

有【很多瞭解mock的資源】(https://realpython.com/python-mock-library/)，參考
他們尋求進一步的幫助。

> `EvAdventureRollEngine`有很多方法可以測試。我們將此作為額外練習！

(summary)=
## 概括

這總結了 _Knave_ 的所有核心規則機制 - 遊戲過程中使用的規則。我們在這裡注意到，我們很快就需要確定我們的 _Character_ 實際上如何儲存資料。所以我們接下來會解決這個問題。




