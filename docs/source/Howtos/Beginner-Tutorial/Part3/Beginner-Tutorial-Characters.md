(player-characters)=
# 玩家角色

在[上一課關於規則和骰子滾動](./Beginner-Tutorial-Rules.md)中，我們對「玩家角色」實體做了一些假設：

- 它應該將自身的能力儲存為 `character.strength`、`character.constitution` 等。
- 它應該有一個 `.heal(amount)` 方法。

所以我們有一些關於它的外觀的指導方針！字元是一個資料庫實體，其值應該能夠隨著時間的推移而變更。以 Evennia 為基礎是有意義的
[DefaultCharacter Typeclass](../../../Components/Typeclasses.md)。 Character 類別就像桌面上的“字元表”
RPG，它將儲存與PC相關的所有內容。

(inheritance-structure)=
## 繼承結構

玩家角色（PC）並不是我們世界上唯一「有生命」的東西。我們還有_NPC_
（如店家和其他友軍）以及可以攻擊我們的_怪物_（小怪）。

在程式碼中，我們可以透過幾種方法來建構它。如果 NPCs/monsters 只是 PC 的特殊情況，我們可以使用這樣的類別繼承：

```python
from evennia import DefaultCharacter

class EvAdventureCharacter(DefaultCharacter):
    # stuff

class EvAdventureNPC(EvAdventureCharacter):
    # more stuff

class EvAdventureMob(EvAdventureNPC):
    # more stuff
```

我們放在 `Character` 類別上的所有程式碼現在都將自動繼承到 `NPC` 和 `Mob` 。

然而，在_Knave_中，NPCs，尤其是怪物_不_使用與PC相同的規則——它們被簡化為使用Hit-Die (HD)概念。因此，雖然仍然像字元一樣，NPCs 應該與 PC 分開，如下所示：

```python
from evennia import DefaultCharacter

class EvAdventureCharacter(DefaultCharacter):
    # stuff

class EvAdventureNPC(DefaultCharacter):
    # separate stuff

class EvAdventureMob(EvadventureNPC):
    # more separate stuff
```

儘管如此，有些事情應該是所有「生物」所共有的：

- 所有人都會受到傷害。
- 所有人都會死。
- 一切都可以治癒
- 所有人都可以持有和丟失硬幣
- 所有人都可以掠奪倒下的敵人。
- 被擊敗後所有人都可能被掠奪。

我們不想為每個類別單獨編碼，但我們不再有一個公共的父類別來放置它。因此，我們將使用 _mixin_ 類別的概念：

```python
from evennia import DefaultCharacter

class LivingMixin:
    # stuff common for all living things

class EvAdventureCharacter(LivingMixin, DefaultCharacter):
    # stuff

class EvAdventureNPC(LivingMixin, DefaultCharacter):
    # stuff

class EvAdventureMob(LivingMixin, EvadventureNPC):
    # more stuff
```

```{sidebar}
在[evennia/contrib/tutorials/evadventure/characters.py](../../../api/evennia.contrib.tutorials.evadventure.characters.md)中
是字元類別結構的範例。
```
上面的 `LivingMixin` 類別不能單獨工作 - 它只是用一些所有生物都應該能夠執行的額外功能來「修補」其他類別。這是_多重繼承_的一個例子。繼承的順序在這裡很重要 - `LivingMixin` 必須在 `DefaultCharacter` （或 EvAdventureNPC 等）之前，以便在呼叫時首先找到它的方法。多重繼承是物件導向程式設計中的強大工具，瞭解它很有用。但要小心過度使用它。如果你有太多的 mixin，那就很難理解哪個方法來自哪裡。


(living-mixin-class)=
## 生活混音類

> 建立一個新模組`mygame/evadventure/characters.py`

讓我們獲得一些所有生物都應該在我們的遊戲中使用的有用的通用方法。

```python
# in mygame/evadventure/characters.py

from .rules import dice

class LivingMixin:

    # makes it easy for mobs to know to attack PCs
    is_pc = False

	@property
    def hurt_level(self):
        """
        String describing how hurt this character is.
        """
        percent = max(0, min(100, 100 * (self.hp / self.hp_max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        elif 80 < percent <= 95:
            return "|gScraped|n"
        elif 60 < percent <= 80:
            return "|GBruised|n"
        elif 45 < percent <= 60:
            return "|yHurt|n"
        elif 30 < percent <= 45:
            return "|yWounded|n"
        elif 15 < percent <= 30:
            return "|rBadly wounded|n"
        elif 1 < percent <= 15:
            return "|rBarely hanging on|n"
        elif percent == 0:
            return "|RCollapsed!|n"

    def heal(self, hp):
        """
        Heal hp amount of health, not allowing to exceed our max hp

        """
        damage = self.hp_max - self.hp
        healed = min(damage, hp)
        self.hp += healed

        self.msg(f"You heal for {healed} HP.")

    def at_pay(self, amount):
        """When paying coins, make sure to never detract more than we have"""
        amount = min(amount, self.coins)
        self.coins -= amount
        return amount

    def at_attacked(self, attacker, **kwargs):
		"""Called when being attacked and combat starts."""
		pass

    def at_damage(self, damage, attacker=None):
        """Called when attacked and taking damage."""
        self.hp -= damage

    def at_defeat(self):
        """Called when defeated. By default this means death."""
        self.at_death()

    def at_death(self):
        """Called when this thing dies."""
        # this will mean different things for different living things
        pass

    def at_do_loot(self, looted):
        """Called when looting another entity"""
        looted.at_looted(self)

    def at_looted(self, looter):
        """Called when looted by another entity"""

        # default to stealing some coins
        max_steal = dice.roll("1d10")
        stolen = self.at_pay(max_steal)
        looter.coins += stolen

```
其中大部分是空的，因為它們對於角色和 npc 的行為有所不同。但是將它們放在 mixin 中意味著我們可以期望這些方法可用於所有生物。

一旦我們建立了更多的遊戲，我們將需要記住實際呼叫這些鉤子方法，以便它們可以發揮作用。例如，一旦我們實施戰鬥，我們必須記住呼叫`at_attacked`以及其他涉及傷害、失敗或死亡的方法。

(character-class)=
## 字元類

我們現在將根據 _Knave_ 的需要開始製作基本的角色類別。

```python
# in mygame/evadventure/characters.py

from evennia import DefaultCharacter, AttributeProperty
from .rules import dice

class LivingMixin:
    # ...


class EvAdventureCharacter(LivingMixin, DefaultCharacter):
    """
    A character to use for EvAdventure.
    """
    is_pc = True

    strength = AttributeProperty(1)
    dexterity = AttributeProperty(1)
    constitution = AttributeProperty(1)
    intelligence = AttributeProperty(1)
    wisdom = AttributeProperty(1)
    charisma = AttributeProperty(1)

    hp = AttributeProperty(8)
    hp_max = AttributeProperty(8)

    level = AttributeProperty(1)
    xp = AttributeProperty(0)
    coins = AttributeProperty(0)

    def at_defeat(self):
        """Characters roll on the death table"""
        if self.location.allow_death:
            # this allow rooms to have non-lethal battles
            dice.roll_death(self)
        else:
            self.location.msg_contents(
                "$You() $conj(collapse) in a heap, alive but beaten.",
                from_obj=self)
            self.heal(self.hp_max)

    def at_death(self):
        """We rolled 'dead' on the death table."""
        self.location.msg_contents(
            "$You() collapse in a heap, embraced by death.",
            from_obj=self)
        # TODO - go back into chargen to make a new character!
```

我們對這裡的房間做出假設 - 他們擁有 `.allow_death` 的財產。我們需要做一個註釋，以便稍後將這樣的屬性新增到房間中！

在我們的 `Character` 類別中，我們實作了想要從 _Knave_ 規則集中模擬的所有屬性。 `AttributeProperty` 是一種以類似欄位的方式新增 Attribute 的方法；每個角色都可以透過多種方式存取這些內容：

- 作為`character.strength`
- 作為`character.db.strength`
- 作為`character.attributes.get("strength")`

請參閱[屬性](../../../Components/Attributes.md) 以瞭解屬性的工作原理。

與基地 _Knave_ 不同，我們將 `coins` 儲存為單獨的 Attribute，而不是作為庫存中的物品，這使得以後更容易處理以物易物和交易。

我們實現了`at_defeat`和`at_death`的玩家角色版本。我們也使用 `LivingMixin` 類別中的 `.heal()`。

(funcparser-inlines)=
### 函式解析器內聯

上面 `at_defeat` 方法中的這段程式碼值得更多額外的解釋：

```python
self.location.msg_contents(
    "$You() $conj(collapse) in a heap, alive but beaten.",
    from_obj=self)
```

請記住，`self` 是此處的角色例項。所以 `self.location.msg_contents` 的意思是「向我目前位置內的所有內容傳送訊息」。換句話說，向與該角色處於同一位置的每個人傳送訊息。

`$You() $conj(collapse)` 是 [FuncParser 內聯](../../../Components/FuncParser.md)。這些是在字串中執行的函式。對於不同的受眾來說，產生的字串可能看起來不同。 `$You()` 行內函數將使用 `from_obj` 來確定「您」是誰，並顯示您的名字或「您」。  `$conj()`（動詞變形器）將調整（英文）動詞以符合。

- 您將看到：`"You collapse in a heap, alive but beaten."`
- 房間裡的其他人將會看到：`"Thomas collapses in a heap, alive but beaten."`

請注意 `$conj()` 如何選擇 `collapse/collapses` 以使句子在語法上正確。

(backtracking)=
### 回溯

我們第一次使用`rules.dice`滾輪在死亡桌上滾動！您可能還記得，在上一課中，我們不知道在這張桌子上滾動“死亡”時該怎麼做。現在我們知道了 - 我們應該對角色呼叫 `at_death`。因此，讓我們在之前 TODOs 的位置新增：

```python
# mygame/evadventure/rules.py

class EvAdventureRollEngine:

    # ...

    def roll_death(self, character):
        ability_name = self.roll_random_table("1d8", death_table)

        if ability_name == "dead":
            # kill the character!
            character.at_death()  # <------ TODO no more
        else:
            # ...

            if current_ability < -10:
                # kill the character!
                character.at_death()  # <------- TODO no more
            else:
                # ...
```

(connecting-the-character-with-evennia)=
## 將角色與Evennia連線

您可以使用以下方法輕鬆地讓自己成為遊戲中的`EvAdventureCharacter`
`type`指令：

    type self = evadventure.characters.EvAdventureCharacter

現在您可以執行 `examine self` 來檢查您的型別已更新。

如果您希望_所有_新角色都屬於這種型別，您需要告知Evennia。 Evennia 使用全域設定 `BASE_CHARACTER_TYPECLASS` 來瞭解建立角色時（例如登入時）要使用哪一個 typeclass。預設為 `typeclasses.characters.Character`（即 `mygame/typeclasses/characters.py` 中的 `Character` 類）。

因此，有兩種方法可以將新的 Character 類別編織到 Evennia 中：

1. 更改 `mygame/server/conf/settings.py` 並新增 `BASE_CHARACTER_TYPECLASS = "evadventure.characters.EvAdventureCharacter"`。
2. 或者，將 `typeclasses.characters.Character` 更改為從 `EvAdventureCharacter` 繼承。

您必須始終重新載入伺服器才能使此類變更生效。

```{important}
在本教學中，我們將在資料夾 `mygame/evadventure/` 中進行所有變更。這意味著我們可以隔離
我們的程式碼，但這意味著我們需要執行一些額外的步驟將角色（和其他物件）繫結到 Evennia 中。
對於自己的遊戲，直接開始編輯`mygame/typeclasses/characters.py`就可以了
相反。
```


(unit-testing)=
## 單元測試

> 建立一個新模組`mygame/evadventure/tests/test_characters.py`

為了測試，我們只需要建立一個新的 EvAdventure 字元並檢查呼叫它的方法不會出錯。

```python
# mygame/evadventure/tests/test_characters.py

from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest

from ..characters import EvAdventureCharacter

class TestCharacters(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        self.character = create.create_object(EvAdventureCharacter, key="testchar")

    def test_heal(self):
        self.character.hp = 0
        self.character.hp_max = 8

        self.character.heal(1)
        self.assertEqual(self.character.hp, 1)
        # make sure we can't heal more than max
        self.character.heal(100)
        self.assertEqual(self.character.hp, 8)

    def test_at_pay(self):
        self.character.coins = 100

        result = self.character.at_pay(60)
        self.assertEqual(result, 60)
        self.assertEqual(self.character.coins, 40)

        # can't get more coins than we have
        result = self.character.at_pay(100)
        self.assertEqual(result, 40)
        self.assertEqual(self.character.coins, 0)

    # tests for other methods ...

```
如果您遵循了前面的課程，這些測驗應該看起來很熟悉。考慮新增其他方法的測試作為練習。詳細內容請參考之前的課程。

為了執行您所做的測試：

     evennia test --settings settings.py .evadventure.tests.test_characters


(about-races-and-classes)=
## 關於比賽和班級

_Knave_ 沒有任何 D&D 風格的_職業_（如小偷、戰士等）。它也不關心_種族_（如矮人、精靈等）。這使得教學變得更短，但您可能會問自己如何新增這些功能。

在我們為 _Knave_ 勾勒出的框架中，這很簡單 - 你可以將你的種族/職業新增為你的角色的 Attribute：

```python
# mygame/evadventure/characters.py

from evennia import DefaultCharacter, AttributeProperty
# ...

class EvAdventureCharacter(LivingMixin, DefaultCharacter):

    # ...

    charclass = AttributeProperty("Fighter")
    charrace = AttributeProperty("Human")

```
我們在這裡使用`charclass`而不是`class`，因為`class`是Python的保留關鍵字。將 `race` 命名為 `charrace` 因此在風格上配對。

然後我們需要擴充套件我們的[規則模組](./Beginner-Tutorial-Rules.md)（稍後
[字元產生](./Beginner-Tutorial-Chargen.md) 檢查並包含這些類別的含義。


(summary)=
## 概括


`EvAdventureCharacter` 類別就位後，我們可以更瞭解我們的電腦在 _Knave_ 下的樣子。

目前，我們只有一些零碎的東西，還沒有在遊戲中測試這段程式碼。但如果你願意的話，你現在就可以把自己變成`EvAdventureCharacter`。登入您的遊戲並執行指令

    type self = evadventure.characters.EvAdventureCharacter

如果一切順利，`ex self` 現在會將您的 typeclass 顯示為 `EvAdventureCharacter`。  看看你的實力

    py self.strength = 3

```{important}
執行 `ex self` 時，您將不會看到列出的所有能力。這是因為用 `AttributeProperty` 新增的屬性在至少被訪問一次之前才可用。因此，一旦您設定（或檢視）上面的 `.strength`，從那時起 `strength` 將顯示在 `examine` 中。
```
