(implementing-a-game-rule-system)=
# 實施遊戲規則系統


建立線上角色扮演遊戲的最簡單方法（至少從程式碼角度來看）是
只要拿一本平裝本RPG規則書，召集一群遊戲高手並開始執行場景
與任何登入者一起。遊戲大師可以在計算機前擲骰子並告訴玩家
玩家的結果。這與傳統的桌上遊戲僅一步之遙，並且投入了大量的精力
對員工的要求－員工不太可能全天候工作，即使他們
非常敬業。

因此，許多遊戲，甚至是最專注於角色扮演的遊戲，都傾向於允許玩家自行調解
在某種程度上。做到這一點的一種常見方法是引入*編碼系統* - 也就是說，讓
計算機承擔一些繁重的工作。最基本的事情是增加一個線上擲骰子，這樣每個人都可以
製作麵包卷並確保沒有人作弊。在這個關卡的某個地方，您會發現最簡單的內容
角色扮演MUSHes。

編碼系統的優點是，只要規則是公平的，電腦也是公平的——它使得
沒有任何判斷力，也沒有個人恩怨（也不能被指控持有任何個人恩怨）。另外，
計算機不需要睡眠，無論玩家何時登入，都可以始終線上。的
缺點是編碼系統不靈活，無法適應人類未程式設計的行為
玩家可能會在角色扮演中想出。基於這個原因，許多角色扮演重的MUDs會混合使用
變化 - 他們使用編碼系統進行戰鬥和技能進步等，但保留角色扮演
大部分是自由形式，由工作人員遊戲大師監督。

最後，天平的另一端是角色扮演較少或沒有的遊戲，其中游戲機制（和
因此玩家公平性）是最重要的方面。在此類遊戲中，唯一具有遊戲內價值的事件
是由程式碼產生的結果。此類遊戲非常常見，包括砍殺等各種遊戲
MUDs各種戰術模擬。

因此，您的第一個決定需要確定您的目標是什麼型別的系統。此頁面將嘗試
給出一些關於如何組織系統的「編碼」部分的想法，無論它有多大。

(overall-system-infrastructure)=
## 整體系統基礎架構

我們強烈建議您盡可能獨立編碼規則系統。也就是說，不要
傳播你的技能檢定程式碼、種族獎金計算、骰子修改器或你擁有的東西
遊戲。

- 將您需要在規則手冊中查詢的所有內容放入 `mygame/world` 中的模組中。躲起來
盡你所能。  將其視為一個黑盒子（或可能是全知的程式碼表示）
遊戲大師）。遊戲的其餘部分將詢問這個黑盒子問題並獲得答案。正是如此
不需要在盒子外面知道它是如何得出這些結果的。  這樣做
讓以後更容易在一個地方更改和更新內容。
- 僅儲存每個遊戲物件所需的最少內容。也就是說，如果你的角色需要
健康值、技能清單等，將這些東西儲存在角色上 - 不要儲存如何
滾動或更改它們。
- 接下來是確定您希望如何在物件和角色上儲存內容。你可以
選擇將事物儲存為單獨的[屬性](../Components/Attributes.md)，例如`character.db.STR=34` 和
`character.db.Hunting_skill=20`。但您也可以使用一些自訂儲存方法，例如字典 `character.db.skills = {"Hunting":34, "Fishing":20,...}`。一個更奇特的解決方案是檢視 [Trait handler contrib](../Contribs/Contrib-Traits.md)。最後你甚至可以使用[自訂 django 型號](../Concepts/Models.md)。哪個更好取決於您的遊戲和系統的複雜性。
- 在您的規則中明確[API](https://en.wikipedia.org/wiki/Application_programming_interface)。也就是說，建立您提供的方法/函式，例如您的角色和您想要檢查的技能。也就是說，您想要類似的東西：

    ```python
        from world import rules
        result = rules.roll_skill(character, "hunting")
        result = rules.roll_challenge(character1, character2, "swords")
    ```

您可能需要根據您的遊戲使這些函式變得或多或少複雜。例如，房間的屬性可能會對擲骰子的結果產生影響（如果房間是黑暗的、燃燒的等）。確定需要傳送到遊戲機制模組中的內容是瞭解需要新增到引擎中的內容的好方法。

(coded-systems)=
## 編碼系統

受桌上角色扮演遊戲的啟發，大多數遊戲系統都會模仿某種骰子機制。為此Evennia提供了完整的[骰子貢獻](../Contribs/Contrib-Dice.md)。對於自訂實現，Python 提供了多種使用其內建 `random` 模組來隨機化結果的方法。不管它是如何實現的，我們在本文中將確定結果的動作稱為「擲骰」。

在自由形式的系統中，擲骰的結果只是與價值觀和人（或遊戲）進行比較
大師）只是同意它的意思。在編碼系統中，現在需要以某種方式處理結果。規則執行可能會發生很多事情：

- 健康值可以增加或減少。這可以透過多種方式影響角色。
- 可能需要新增經驗，並且如果使用基於級別的系統，則可能需要通知玩家他們已經提高了等級。
- 房間範圍內的影響需要報告給房間，可能會影響房間中的每個人。

還有許多其他東西屬於“編碼系統”，包括諸如
天氣、NPC人工智慧和遊戲經濟。基本上，遊戲大師在桌上角色扮演遊戲中控制的世界的一切都可以透過編碼系統在某種程度上進行模仿。


(example-of-rule-module)=
## 規則模組範例

這是規則模組的一個簡單範例。這是我們對簡單範例遊戲的假設：
- 字元只有四個數值：
    - 他們的`level`，從1開始。
    - 技能`combat`，決定了他們擊打物體的能力。從 5 點到 10 點開始。
    - 他們的力量，`STR`，決定了他們造成的傷害有多大。從 1 到 10 之間開始。
    - 他們的生命值`HP`，從 100 開始。
- 當角色達到`HP = 0`時，他們被視為「失敗」。他們的 HP 被重置，並且他們收到一條失敗訊息（作為死亡程式碼的替代）。
- 能力作為角色的簡單屬性儲存。
- 「滾」是透過滾動 100 面的骰子來完成的。如果結果低於 `combat` 值，則成功並滾動傷害。傷害以六面骰 + `STR` 的值進行滾動（在本例中，我們忽略武器並假設 `STR` 是最重要的）。
- 每次成功的 `attack` 擲骰都會獲得 1-3 點經驗值 (`XP`)。每當`XP`的數量達到`(level + 1) ** 2`時，角色就會升級。升級時，角色的 `combat` 值增加 2 點，`STR` 增加 1 點（這是真實進度系統的替代）。

(character)=
### 特點

字元 typeclass 很簡單。它進入`mygame/typeclasses/characters.py`。那裡已經有一個空的 `Character` 類，Evennia 將查詢並使用該類。

```python
from random import randint
from evennia import DefaultCharacter

class Character(DefaultCharacter):
    """
    Custom rule-restricted character. We randomize
    the initial skill and ability values bettween 1-10.
    """
    def at_object_creation(self):
        "Called only when first created"
        self.db.level = 1
        self.db.HP = 100
        self.db.XP = 0
        self.db.STR = randint(1, 10)
        self.db.combat = randint(5, 10)
```

`@reload` 伺服器載入新程式碼。然而，執行 `examine self` 將*不會*顯示新的
對自己的屬性。這是因為 `at_object_creation` 鉤子僅在 *new* 上呼叫
人物。您的角色已經建立，因此不會擁有它們。若要強制重新載入，請使用
以下指令：

```
@typeclass/force/reset self
```

`examine self` 指令現在將顯示新屬性。

(rule-module)=
### 規則模組

這是一個模組`mygame/world/rules.py`。

```python
from random import randint

def roll_hit():
    "Roll 1d100"
    return randint(1, 100)

def roll_dmg():
    "Roll 1d6"
    return randint(1, 6)

def check_defeat(character):
    "Checks if a character is 'defeated'."
    if character.db.HP <= 0:
       character.msg("You fall down, defeated!")
       character.db.HP = 100   # reset

def add_XP(character, amount):
    "Add XP to character, tracking level increases."
    character.db.XP += amount
    if character.db.XP >= (character.db.level + 1) ** 2:
        character.db.level += 1
        character.db.STR += 1
        character.db.combat += 2
        character.msg(f"You are now level {character.db.level}!")

def skill_combat(*args):
    """
    This determines outcome of combat. The one who
    rolls under their combat skill AND higher than
    their opponent's roll hits.
    """
    char1, char2 = args
    roll1, roll2 = roll_hit(), roll_hit()
    failtext_template = "You are hit by {attacker} for {dmg} damage!"
    wintext_template = "You hit {target} for {dmg} damage!"
    xp_gain = randint(1, 3)
    if char1.db.combat >= roll1 > roll2:
        # char 1 hits
        dmg = roll_dmg() + char1.db.STR
        char1.msg(wintext_template.format(target=char2, dmg=dmg))
        add_XP(char1, xp_gain)
        char2.msg(failtext_template.format(attacker=char1, dmg=dmg))
        char2.db.HP -= dmg
        check_defeat(char2)
    elif char2.db.combat >= roll2 > roll1:
        # char 2 hits
        dmg = roll_dmg() + char2.db.STR
        char1.msg(failtext_template.format(attacker=char2, dmg=dmg))
        char1.db.HP -= dmg
        check_defeat(char1)
        char2.msg(wintext_template.format(target=char1, dmg=dmg))
        add_XP(char2, xp_gain)
    else:
        # a draw
        drawtext = "Neither of you can find an opening."
        char1.msg(drawtext)
        char2.msg(drawtext)

SKILLS = {"combat": skill_combat}

def roll_challenge(character1, character2, skillname):
    """
    Determine the outcome of a skill challenge between
    two characters based on the skillname given.
    """
    if skillname in SKILLS:
        SKILLS[skillname](character1, character2)
    else:
        raise RunTimeError(f"Skillname {skillname} not found.")
```

這幾個函式實作了我們整個簡單的規則系統。  我們有一個函式可以檢查
「失敗」條件並將`HP`再次重回100。我們定義一個通用的「技能」函式。
多個技能都可以用同一個簽名新增；我們的 `SKILLS` 字典可以輕鬆
尋找技能，無論其實際功能為何。最後，訪問
函式 `roll_challenge` 只是選擇技能並獲得結果。

在這個例子中，技能函式實際上做了很多事情 - 它不僅滾動結果，還通知
每個人的結果都是透過 `character.msg()` 電話獲得的。

以下是遊戲指令中的用法範例：

```python
from evennia import Command
from world import rules

class CmdAttack(Command):
    """
    attack an opponent

    Usage:
      attack <target>

    This will attack a target in the same room, dealing
    damage with your bare hands.
    """
    def func(self):
        "Implementing combat"

        caller = self.caller
        if not self.args:
            caller.msg("You need to pick a target to attack.")
            return

        target = caller.search(self.args)
        if target:
            rules.roll_challenge(caller, target, "combat")
```

請注意該指令變得多麼簡單以及您可以使其變得多麼通用。  提供任何服務都變得簡單
只需擴充套件此功能即可增加戰鬥指令的數量 - 您可以輕鬆地進行挑戰並
選擇不同的技能來檢查。如果你決定改變決定命中率的方式
您不必更改每個指令，而只需更改其中的單個 `roll_hit` 函式
你的`rules`模組。
