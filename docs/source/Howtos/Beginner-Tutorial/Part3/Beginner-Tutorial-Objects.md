(in-game-objects-and-items)=
# 遊戲內的物品和物品

在上一課中，我們確定了遊戲中的「角色」。在我們繼續之前
我們還需要知道什麼是“專案”或“物件”。

檢視 _Knave_ 的專案列表，我們可以瞭解需要追蹤的內容：

- `size` - 這是該物品在角色的庫存中使用的「槽位」數量。
- `value` - 如果我們想出售或購買該物品，則為基礎值。
- `inventory_use_slot` - 有些物品可以穿戴或揮舞。例如頭上需要戴頭盔，手上需要戴盾牌。有些物品根本不能這樣使用，只能放在揹包裡。
- `obj_type` - 這是哪種「型別」的物品。
  

(new-enums)=
## 新列舉

我們在[實用工具教學](./Beginner-Tutorial-Utilities.md) 中加入了一些能力的編號。
在繼續之前，讓我們用列舉來擴充套件使用槽和物件型別。

```python
# mygame/evadventure/enums.py

# ...

class WieldLocation(Enum):
    
    BACKPACK = "backpack"
    WEAPON_HAND = "weapon_hand"
    SHIELD_HAND = "shield_hand"
    TWO_HANDS = "two_handed_weapons"
    BODY = "body"  # armor
    HEAD = "head"  # helmets

class ObjType(Enum):
    
    WEAPON = "weapon"
    ARMOR = "armor"
    SHIELD = "shield"
    HELMET = "helmet"
    CONSUMABLE = "consumable"
    GEAR = "gear"
    MAGIC = "magic"
    QUEST = "quest"
    TREASURE = "treasure"
```

一旦我們有了這些列舉，我們將使用它們來引用事物。

(the-base-object)=
## 基礎物件

> 建立一個新模組`mygame/evadventure/objects.py`

```{sidebar}
[evennia/contrib/tutorials/evadventure/objects.py](../../../api/evennia.contrib.tutorials.evadventure.objects.md) 有
實現的一整套物件。
```
<div style="clear: right;"></div>

我們將根據 Evennia 的標準 `DefaultObject` 制定基本 `EvAdventureObject` 等級。然後我們將新增子類別來表示相關型別：

```python 
# mygame/evadventure/objects.py

from evennia import AttributeProperty, DefaultObject 
from evennia.utils.utils import make_iter
from .utils import get_obj_stats 
from .enums import WieldLocation, ObjType


class EvAdventureObject(DefaultObject): 
    """ 
    Base for all evadventure objects. 
    
    """ 
    inventory_use_slot = WieldLocation.BACKPACK
    size = AttributeProperty(1, autocreate=False)
    value = AttributeProperty(0, autocreate=False)
    
    # this can be either a single type or a list of types (for objects able to be 
    # act as multiple). This is used to tag this object during creation.
    obj_type = ObjType.GEAR

    # default evennia hooks

    def at_object_creation(self): 
        """Called when this object is first created. We convert the .obj_type 
        property to a database tag."""
        
        for obj_type in make_iter(self.obj_type):
            self.tags.add(self.obj_type.value, category="obj_type")

    def get_display_header(self, looker, **kwargs):
	    """The top of the description""" 
	    return "" 

	def get_display_desc(self, looker, **kwargs):
		"""The main display - show object stats""" 
		return get_obj_stats(self, owner=looker)

    # custom evadventure methods

	def has_obj_type(self, objtype): 
		"""Check if object is of a certain type""" 
		return objtype.value in make_iter(self.obj_type)

    def at_pre_use(self, *args, **kwargs): 
        """Called before use. If returning False, can't be used""" 
        return True 

	def use(self, *args, **kwargs): 
		"""Use this object, whatever that means""" 
		pass 

    def post_use(self, *args, **kwargs): 
	    """Always called after use.""" 
	    pass

    def get_help(self):
        """Get any help text for this item"""
        return "No help for this item"
```

(using-attributes-or-not)=
### 是否使用屬性

理論上，`size` 和 `value` 不會改變，_也可以_設定為常規 Python
類別上的屬性：

```python 
class EvAdventureObject(DefaultObject):
    inventory_use_slot = WieldLocation.BACKPACK 
    size = 1 
    value = 0 
```

這樣做的問題是，如果我們想建立一個`size 3`和`value 20`的新物件，我們必須為其建立一個新類別。我們無法即時更改它，因為更改只會儲存在記憶體中，並且會在下次伺服器重新載入時遺失。

因為我們使用`AttributeProperties`，所以我們可以在建立物件時（或以後）將`size`和`value`設定為我們喜歡的任何內容，並且屬性將無限期地記住我們對該物件的更改。

為了提高效率，我們使用`autocreate=False`。通常，當您建立定義了 `AttributeProperties` 的新物件時，會立即同時建立符合的 `Attribute`。因此，通常情況下，該物件將與兩個屬性 `size` 和 `value` 一起建立。對於 `autocreate=False`，不會建立 Attribute _除非更改預設值_。也就是說，只要你的物件有`size=1`，就根本不會建立資料庫`Attribute`。建立大量物件時，這可以節省時間和資源。

缺點是，由於沒有建立 Attribute，因此您無法使用 `obj.db.size` 或 `obj.attributes.get("size")` 引用它_除非您更改其預設值_。您也無法在資料庫中查詢帶有 `size=1` 的所有物件，因為大多數物件還沒有資料庫內資料
`size` Attribute 進行搜尋。

在我們的例子中，我們只會將這些屬性稱為 `obj.size` 等，並且不需要查詢
所有具有特定尺寸的物體。所以我們應該是安全的。

(creating-tags-in-at_object_creation)=
### 在 `at_object_creation` 中建立 tags

`at_object_creation` 是 Evennia 的方法，每當首次建立 `DefaultObject` 的每個子級時都會呼叫該方法。

我們在這裡做了一件棘手的事情，將 `.obj_type` 轉換為一個或多個 [Tags](../../../Components/Tags.md)。像這樣標記物件意味著您以後可以有效地查詢給定型別（或組合）的所有物件
型別）與 Evennia 的搜尋功能：

```python
    from .enums import ObjType 
    from evennia.utils import search 
    
    # get all shields in the game
    all_shields = search.search_object_by_tag(ObjType.SHIELD.value, category="obj_type")
```

我們允許 `.obj_type` 作為單一值或值列表給出。我們使用 evennia 實用程式庫中的 `make_iter` 來確保我們不會猶豫。例如，這意味著您可以擁有一個同樣是魔法的盾牌。

(other-object-types)=
## 其他物件型別

到目前為止，其他一些物件型別非常簡單。

```python 
# mygame/evadventure/objects.py 

from evennia import AttributeProperty, DefaultObject
from .enums import ObjType 

class EvAdventureObject(DefaultObject): 
    # ... 
    
    
class EvAdventureQuestObject(EvAdventureObject):
    """Quest objects should usually not be possible to sell or trade."""
    obj_type = ObjType.QUEST
 
class EvAdventureTreasure(EvAdventureObject):
    """Treasure is usually just for selling for coin"""
    obj_type = ObjType.TREASURE
    value = AttributeProperty(100, autocreate=False)
    
```

(consumables)=
## 耗材

「消耗品」是具有一定次數「使用」的物品。一旦完全消耗，就無法再使用。一個例子是健康藥水。


```python 
# mygame/evadventure/objects.py 

# ... 

class EvAdventureConsumable(EvAdventureObject): 
    """An item that can be used up""" 
    
    obj_type = ObjType.CONSUMABLE
    value = AttributeProperty(0.25, autocreate=False)
    uses = AttributeProperty(1, autocreate=False)
    
    def at_pre_use(self, user, target=None, *args, **kwargs):
        """Called before using. If returning False, abort use."""
		if target and user.location != target.location:
			user.msg("You are not close enough to the target!")
		    return False
		
		if self.uses <= 0:
		    user.msg(f"|w{self.key} is used up.|n")
		    return False

    def use(self, user, *args, **kwargs):
        """Called when using the item""" 
        pass
    
    def at_post_use(self, user, *args, **kwargs):
        """Called after using the item""" 
        # detract a usage, deleting the item if used up.
        self.uses -= 1
        if self.uses <= 0: 
            user.msg(f"{self.key} was used up.")
            self.delete()
```

在`at_pre_use`中，我們檢查是否指定了目標（治療其他人或向敵人投擲火焰彈？），確保我們位於同一位置。我們也確保還剩下`usages`。在`at_post_use`中，我們確保勾選用法。

每個消耗品的具體作用會有所不同 - 我們稍後需要實現此類的子級，以不同的效果覆蓋 `at_use`。

(weapons)=
## 武器

所有武器都需要描述它們在戰鬥中的效率的屬性。 「使用」武器意味著用它進行攻擊，因此我們可以讓武器本身處理有關執行攻擊的所有邏輯。在武器上新增攻擊程式碼也意味著，如果我們將來想要一種武器在攻擊時做一些特殊的事情（例如，在傷害敵人時治癒攻擊者的吸血鬼劍），我們可以輕鬆地將其新增到相關武器子類中，而無需修改其他程式碼。

```python 
# mygame/evadventure/objects.py 

from .enums import WieldLocation, ObjType, Ability

# ... 

class EvAdventureWeapon(EvAdventureObject): 
    """Base class for all weapons"""

    obj_type = ObjType.WEAPON 
    inventory_use_slot = AttributeProperty(WieldLocation.WEAPON_HAND, autocreate=False)
    quality = AttributeProperty(3, autocreate=False)
    
    attack_type = AttributeProperty(Ability.STR, autocreate=False)
    defense_type = AttributeProperty(Ability.ARMOR, autocreate=False)
    
    damage_roll = AttributeProperty("1d6", autocreate=False)


def at_pre_use(self, user, target=None, *args, **kwargs):
       if target and user.location != target.location:
           # we assume weapons can only be used in the same location
           user.msg("You are not close enough to the target!")
           return False

       if self.quality is not None and self.quality <= 0:
           user.msg(f"{self.get_display_name(user)} is broken and can't be used!")
           return False
       return super().at_pre_use(user, target=target, *args, **kwargs)

   def use(self, attacker, target, *args, advantage=False, disadvantage=False, **kwargs):
       """When a weapon is used, it attacks an opponent"""

       location = attacker.location

       is_hit, quality, txt = rules.dice.opposed_saving_throw(
           attacker,
           target,
           attack_type=self.attack_type,
           defense_type=self.defense_type,
           advantage=advantage,
           disadvantage=disadvantage,
       )
       location.msg_contents(
           f"$You() $conj(attack) $You({target.key}) with {self.key}: {txt}",
           from_obj=attacker,
           mapping={target.key: target},
       )
       if is_hit:
           # enemy hit, calculate damage
           dmg = rules.dice.roll(self.damage_roll)

           if quality is Ability.CRITICAL_SUCCESS:
               # doble damage roll for critical success
               dmg += rules.dice.roll(self.damage_roll)
               message = (
                   f" $You() |ycritically|n $conj(hit) $You({target.key}) for |r{dmg}|n damage!"
               )
           else:
               message = f" $You() $conj(hit) $You({target.key}) for |r{dmg}|n damage!"

           location.msg_contents(message, from_obj=attacker, mapping={target.key: target})
           # call hook
           target.at_damage(dmg, attacker=attacker)

       else:
           # a miss
           message = f" $You() $conj(miss) $You({target.key})."
           if quality is Ability.CRITICAL_FAILURE:
               message += ".. it's a |rcritical miss!|n, damaging the weapon."
			   if self.quality is not None:
                   self.quality -= 1
               location.msg_contents(message, from_obj=attacker, mapping={target.key: target})

   def at_post_use(self, user, *args, **kwargs):
       if self.quality is not None and self.quality <= 0:
           user.msg(f"|r{self.get_display_name(user)} breaks and can no longer be used!")
```

在EvAdventure中，我們假設所有武器（包括弓箭等）都在與目標相同的位置使用。武器還有`quality` attribute，如果使用者發生嚴重故障，武器就會磨損。一旦品質降到0，武器就壞了，需要修理。

`quality` 是我們需要在 _Knave_ 中追蹤的內容。當攻擊嚴重失敗時，武器的品質就會下降。當它達到0時，它就會破裂。我們假設 `None` 的 `quality` 意味著品質不適用（即該物品牢不可破），因此我們在檢查時必須考慮到這一點。

攻擊/防禦型別追蹤我們如何解決使用武器的攻擊，例如`roll + STR vs ARMOR + 10`。

在 `use` 方法中，我們利用[先前建立的](./Beginner-Tutorial-Rules.md) `rules` 模組來執行解決攻擊所需的所有擲骰子操作。

這段程式碼需要一些額外的解釋：
```python
location.msg_contents(
    f"$You() $conj(attack) $you({target.key}) with {self.key}: {txt}",
    from_obj=attacker,
    mapping={target.key: target},
)
```
`location.msg_contents` 向 `location` 中的每個人傳送訊息。由於人們通常會注意到您是否向某人揮舞劍，因此告訴人們這一點是有意義的。然而，這則訊息看起來應該_不同_取決於誰看到它。

我應該看到：

    You attack Grendel with sword: <dice roll results> 

其他人應該看到

    Beowulf attacks Grendel with sword: <dice roll results>  

格倫德爾應該看到

    Beowulf attacks you with sword: <dice roll results>

我們向`msg_contents`提供以下字串：
```python 
f"$You() $conj(attack) $You({target.key}) with {self.key}: {txt}"
```

`{...}` 是普通的 f 字串格式標記，就像我們之前使用的一樣。 `$func(...)` 位元是 [Evennnia FuncParser](../../../Components/FuncParser.md) 函式呼叫。 FuncParser 呼叫作為函式執行，結果會取代它們在字串中的位置。當該字串被 Evennia 解析時，會發生以下情況：

首先替換 f 字串標記，這樣我們就得到了：

```python 
"$You() $cobj(attack) $you(Grendel) with sword: \n rolled 8 on d20 ..."
```

接下來執行 funcparser 函式：

 - `$You()` 成為名稱或 `You`，取決於字串是否傳送到該物件。它使用 `from_obj=` kwarg 到 `msg_contents` 方法來瞭解這一點。由於 `msg_contents=attacker` ，在此範例中變為 `You` 或 `Beowulf` 。
 - `$you(Grendel)` 尋找 `mapping=` kwarg 到 `msg_contents` 以確定應在此處處理的人員。如果將其替換為顯示名稱或小寫`you`。我們新增了 `mapping={target.key: target}` - 即 `{"Grendel": <grendel_obj>}`。因此，這將變成 `you` 或 `Grendel`，具體取決於誰看到字串。
- `$conj(attack)`_結合_動詞取決於誰看到它。結果將是 `You attack...` 或 `Beowulf attacks`（注意額外的 `s`）。

一些 funcparser 呼叫將所有這些觀點壓縮到一個字串中！

(magic)=
## 魔法

在_Knave_中，任何人只要雙手持有符文石（我們對咒語書的稱呼），就可以使用魔法。每次休息只能使用一次符文石。因此，符文石是「魔法武器」的一個例子，同時也是一種「消耗品」。


```python 
# mygame/evadventure/objects.py 

# ... 
class EvAdventureConsumable(EvAdventureObject): 
    # ... 

class EvAdventureWeapon(EvAdventureObject): 
    # ... 

class EvAdventureRuneStone(EvAdventureWeapon, EvAdventureConsumable): 
    """Base for all magical rune stones"""
    
    obj_type = (ObjType.WEAPON, ObjType.MAGIC)
    inventory_use_slot = WieldLocation.TWO_HANDS  # always two hands for magic
    quality = AttributeProperty(3, autocreate=False)

    attack_type = AttributeProperty(Ability.INT, autocreate=False)
    defense_type = AttributeProperty(Ability.DEX, autocreate=False)
    
    damage_roll = AttributeProperty("1d8", autocreate=False)

    def at_post_use(self, user, *args, **kwargs):
        """Called after usage/spell was cast""" 
        self.uses -= 1 
        # we don't delete the rune stone here, but 
        # it must be reset on next rest.
        
    def refresh(self):
        """Refresh the rune stone (normally after rest)"""
        self.uses = 1
```

我們使符文石成為武器和消耗品的混合體。請注意，我們不必再增加 `.uses`，它是從 `EvAdventureConsumable` 父級繼承的。 `at_pre_use`和`use`方法也是繼承的；我們只涵蓋`at_post_use`，因為我們不希望符石在用完後被刪除。

我們新增了一些方便的方法 `refresh` - 我們應該在角色休息時呼叫它，以使符石再次啟動。

符文石的確切用途將在該基類的子類的 `at_use` 方法中實現。由於 _Knave_ 中的魔法往往是非常自訂的，因此它會導致大量自訂程式碼是有道理的。


(armor)=
## 盔甲

盔甲、盾牌和頭盔會增加角色的`ARMOR`屬性。在_Knave_中，儲存的是盔甲的防禦值（值11-20）。我們將儲存「護甲加值」(1-10)。我們知道，防禦總是`bonus + 10`，所以結果是一樣的——這意味著我們可以像任何其他防禦能力一樣使用`Ability.ARMOR`，而不必擔心特殊情況。

``
```python 
# mygame/evadventure/objects.py 

# ... 

class EvAdventureAmor(EvAdventureObject): 
    obj_type = ObjType.ARMOR
    inventory_use_slot = WieldLocation.BODY 

    armor = AttributeProperty(1, autocreate=False)
    quality = AttributeProperty(3, autocreate=False)


class EvAdventureShield(EvAdventureArmor):
    obj_type = ObjType.SHIELD
    inventory_use_slot = WieldLocation.SHIELD_HAND 


class EvAdventureHelmet(EvAdventureArmor): 
    obj_type = ObjType.HELMET
    inventory_use_slot = WieldLocation.HEAD
``` 

(your-bare-hands)=
## 你赤手空拳

當我們沒有武器的時候，我們就用赤手空拳去戰鬥。

我們將在接下來的[裝備教學](./Beginner-Tutorial-Equipment.md)中用它來表示你手中「什麼都沒有」的情況。這樣我們就不需要為此新增任何特殊情況。

```python
# mygame/evadventure/objects.py

from evennia import search_object, create_object

_BARE_HANDS = None 

# ... 

class WeaponBareHands(EvAdventureWeapon):
     obj_type = ObjType.WEAPON
     inventory_use_slot = WieldLocation.WEAPON_HAND
     attack_type = Ability.STR
     defense_type = Ability.ARMOR
     damage_roll = "1d4"
     quality = None  # let's assume fists are indestructible ...


def get_bare_hands(): 
    """Get the bare hands""" 
    global _BARE_HANDS
    if not _BARE_HANDS: 
        _BARE_HANDS = search_object("Bare hands", typeclass=WeaponBareHands).first()
    if not _BARE_HANDS:
    	_BARE_HANDS = create_object(WeaponBareHands, key="Bare hands")
    return _BARE_HANDS
```

```{sidebar}
建立一個在任何地方都使用的單一例項稱為建立_Singleton_。
```
由於每個人的空手都是相同的（在我們的遊戲中），因此我們建立每個人共享的 _one_ `Bare hands` 武器物件。我們透過使用 `search_object` 搜尋物件來做到這一點（`.first()` 意味著我們抓住第一個物件，即使我們不小心建立了多隻手，請參閱 [Django 查詢教學](../Part1/Beginner-Tutorial-Django-queries.md) 以瞭解更多資訊）。如果我們找不到，我們就會創造它。

透過使用 `global` Python 關鍵字，我們將徒手物件 get/create 快取在模組級屬性 `_BARE_HANDS` 中。因此，這充當快取，不必不必要地搜尋資料庫。

從此以後，其他模組只需匯入並執行函式即可輕鬆上手。

(testing-and-extra-credits)=
## 測試和額外學分

還記得之前[實用教學](./Beginner-Tutorial-Utilities.md)中的`get_obj_stats`函式嗎？  我們必須使用虛擬值，因為我們還不知道如何在遊戲中的物件上儲存屬性。

好吧，我們剛剛找到了我們需要的一切！您可以返回並更新 `get_obj_stats` 以正確地從它接收的物件中讀取資料。

當您更改此功能時，您還必須更新相關的單元測試 - 因此您現有的測試也成為測試新物件的好方法！新增更多測試，顯示將不同物件型別提供給 `get_obj_stats` 的輸出。

自己嘗試一下。如果您需要協助，可以在 [evennia/contrib/tutorials/evadventure/utils.py](get_obj_stats) 中找到已完成的實用程式範例。
