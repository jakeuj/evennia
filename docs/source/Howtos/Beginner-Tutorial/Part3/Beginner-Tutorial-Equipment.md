(handling-equipment)=
# 搬運裝置

在_Knave_中，你有一定數量的庫存「插槽」。槽位的數量由`CON + 10`給出。  所有物品（除了金幣）都有一個`size`，表示它使用了多少個插槽。你攜帶的物品不能超過你的插槽空間。揮舞或磨損的物品也計入插槽。

然而，我們仍然需要追蹤角色正在使用什麼：他們準備的武器會影響他們可以造成的傷害。他們使用的盾牌、頭盔和盔甲會影響他們的防禦力。

當我們定義物件時，我們已經設定了可能的“佩戴/揮舞位置”
[在上一課中](./Beginner-Tutorial-Objects.md)。這就是 `enums.py` 中的內容：

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
```

基本上，所有武器/盔甲位置都是專有的 - 每個位置只能擁有一件物品（或沒有）。  BACKPACK 很特殊 - 它包含任意數量的專案（最多可達最大插槽使用量）。

(equipmenthandler-that-saves)=
## EquipmentHandler 儲存

> 建立一個新模組`mygame/evadventure/equipment.py`。

```{sidebar}
如果你想了解更多關於 Evennia 如何使用處理程式的資訊，有一個
【專用教學】(../../Tutorial-Persistent-Handler.md)講原理。
```
在預設的Evennia中，你拾取的所有東西最終都會出現在你的角色物件的「內部」（也就是說，你是它的`.location`）。這稱為您的_庫存_並且沒有限制。當我們拾取物品時，我們將繼續“將物品移入我們體內”，但我們將使用_裝置處理程式_新增更多功能。

處理程式（就我們的目的而言）是一個位於另一個實體「之上」的物件，包含執行一項特定操作的功能（在我們的例子中是管理裝置）。

這是我們的處理程式的開始：

```python 
# in mygame/evadventure/equipment.py 

from .enums import WieldLocation

class EquipmentHandler: 
    save_attribute = "inventory_slots"
    
    def __init__(self, obj): 
        # here obj is the character we store the handler on 
        self.obj = obj 
        self._load() 
        
    def _load(self):
        """Load our data from an Attribute on `self.obj`"""
        self.slots = self.obj.attributes.get(
            self.save_attribute,
            category="inventory",
            default={
                WieldLocation.WEAPON_HAND: None, 
                WieldLocation.SHIELD_HAND: None, 
                WieldLocation.TWO_HANDS: None, 
                WieldLocation.BODY: None,
                WieldLocation.HEAD: None,
                WieldLocation.BACKPACK: []
            } 
        )
    
    def _save(self):
        """Save our data back to the same Attribute"""
        self.obj.attributes.add(self.save_attribute, self.slots, category="inventory") 
```

這是一款緊湊且實用的小型處理程式。在分析它是如何工作之前，這是這樣的
我們將其新增到角色中：

```python
# mygame/evadventure/characters.py

# ... 

from evennia.utils.utils import lazy_property
from .equipment import EquipmentHandler 

# ... 

class EvAdventureCharacter(LivingMixin, DefaultCharacter):
    
    # ... 

    @lazy_property 
    def equipment(self):
        return EquipmentHandler(self)
```

重新載入伺服器後，現在可以在角色例項上存取裝置處理程式，如下所示

    character.equipment

`@lazy_property` 的工作方式是，在有人實際嘗試使用 `character.equipment` 取得該處理程式之前，它不會載入該處理程式。當這種情況發生時，我們啟動處理程式並為其提供 `self`（`Character` 例項本身）。這就是上面 `EquipmentHandler` 程式碼中將 `__init__` 輸入為 `.obj` 的內容。

現在我們在角色上有了一個處理程式，並且該處理程式具有對其所在角色的反向引用。

由於處理程式本身只是一個常規的 Python 物件，因此我們需要使用 `Character` 來儲存
我們的資料 - 我們的_Knave_「老虎機」。我們必須將它們儲存到資料庫中，因為我們希望伺服器即使在重新載入後也能記住它們。

使用`self.obj.attributes.add()`和`.get()`，我們將資料儲存到角色中一個專門命名的[Attribute](../../../Components/Attributes.md)中。由於我們使用`category`，所以我們不太可能與
其他屬性。

我們的儲存結構是 `dict`，其鍵位於可用的 `WieldLocation` 列舉之後。每個只能有一項，除了 `WieldLocation.BACKPACK` 之外，它是一個清單。

(connecting-the-equipmenthandler)=
## 連線EquipmentHandler

每當一個物件從一個位置離開到下一個位置時，Evennia 將在移動的物件、來源位置及其目的地上呼叫一組 _hooks_（方法）。這對於所有移動的物體都是一樣的 - 無論是在房間之間移動的角色還是從你手中掉落到地上的物品。

我們需要將新的 `EquipmentHandler` 繫結到這個系統。透過閱讀 [Objects](../../../Components/Objects.md) 上的檔案頁面，或檢視 [DefaultObject.move_to](evennia.objects.objects.DefaultObject.move_to) 檔案字串，我們將找出 Evennia 將呼叫什麼鉤子。這裡 `self` 是從 `source_location` 移動到 `destination` 的物件：


1. `self.at_pre_move(destination)`（如果返回False則中止）
2. `source_location.at_pre_object_leave(self, destination)`（如果返回False則中止）
3. `destination.at_pre_object_receive(self, source_location)`（如果返回False則中止）
4. `source_location.at_object_leave(self, destination)`
5. `self.announce_move_from(destination)`
6. （移動發生在這裡）
7. `self.announce_move_to(source_location)`
8. `destination.at_object_receive(self, source_location)`
9. `self.at_post_move(source_location)`

所有這些鉤子都可以被覆蓋以定製移動行為。在這種情況下，我們感興趣的是控制專案如何「進入」和「離開」我們的角色 - 在角色「內部」與它們「攜帶」角色相同。我們有三個很好的鉤子候選者可以用於此目的。

- `.at_pre_object_receive` - 用於檢查你是否真的可以拾取東西，或者你的裝備商店是否已滿。
- `.at_object_receive` - 用於將專案新增至裝置處理程式中
- `.at_object_leave` - 用於從裝置處理程式中刪除該專案

你也可以想像使用 `.at_pre_object_leave` 來限制掉落（被詛咒的？）物品，但是
在本教學中我們將跳過它。

```python 
# mygame/evadventure/character.py 

# ... 

class EvAdventureCharacter(LivingMixin, DefaultCharacter): 

    # ... 
    
    def at_pre_object_receive(self, moved_object, source_location, **kwargs): 
        """Called by Evennia before object arrives 'in' this character (that is,
        if they pick up something). If it returns False, move is aborted.
        
        """ 
        return self.equipment.validate_slot_usage(moved_object)
    
    def at_object_receive(self, moved_object, source_location, **kwargs): 
        """ 
        Called by Evennia when an object arrives 'in' the character.
        
        """
        self.equipment.add(moved_object)

    def at_object_leave(self, moved_object, destination, **kwargs):
        """ 
        Called by Evennia when object leaves the Character. 
        
        """
        self.equipment.remove(moved_object)
```

上面我們假設 `EquipmentHandler` (`.equipment`) 有方法 `.validate_slot_usage`、`.add` 和 `.remove`。但我們實際上還沒有新增它們 - 我們只是新增了一些合理的名稱！在使用它之前，我們需要實際新增這些方法。

當你執行`create/drop monster:NPC`之類的操作時，NPC 會短暫出現在你的庫存中，然後被扔到地上。由於 NPC 不是有效的裝備，EquipmentHandler 會抱怨 `EquipmentError`（我們對此的定義見下文）。所以我們需要

(expanding-the-equipmenthandler)=
## 擴充裝置處理程式

(validate_slot_usage)=
## `.validate_slot_usage`

讓我們從實現上面提出的第一個方法開始，`validate_slot_usage`：
```python 
# mygame/evadventure/equipment.py 

from .enums import WieldLocation, Ability

class EquipmentError(TypeError):
    """All types of equipment-errors"""
    pass

class EquipmentHandler: 

    # ... 
    
    @property
    def max_slots(self):
        """Max amount of slots, based on CON defense (CON + 10)""" 
        return getattr(self.obj, Ability.CON.value, 1) + 10
        
    def count_slots(self):
        """Count current slot usage""" 
        slots = self.slots
        wield_usage = sum(
            getattr(slotobj, "size", 0) or 0
            for slot, slotobj in slots.items()
            if slot is not WieldLocation.BACKPACK
        )
        backpack_usage = sum(
            getattr(slotobj, "size", 0) or 0 for slotobj in slots[WieldLocation.BACKPACK]
        )
        return wield_usage + backpack_usage
    
    def validate_slot_usage(self, obj):
          """
          Check if obj can fit in equipment, based on its size.
          
          """
          if not inherits_from(obj, EvAdventureObject):
              # in case we mix with non-evadventure objects
              raise EquipmentError(f"{obj.key} is not something that can be equipped.")
  
         size = obj.size
         max_slots = self.max_slots
         current_slot_usage = self.count_slots()
         return current_slot_usage + size <= max_slots

```

```{sidebar}
`@property` 裝飾器將方法轉換為屬性，因此您不需要「呼叫」它。 
也就是說，您可以訪問 `.max_slots` 而不是 `.max_slots()`。在這種情況下，它只是一個
打字少一點。
```
我們新增兩個助手 - `max_slots` _property_ 和 `count_slots`，這是一種計算目前正在使用的插槽的方法。讓我們弄清楚它們是如何工作的。

(max_slots)=
### `.max_slots`

對於 `max_slots`，請記住處理程式上的 `.obj` 是對我們放置此處理程式的 `EvAdventureCharacter` 的反向引用。 `getattr` 是一種用於檢索物件的命名屬性的 Python 方法。 `Enum` `Ability.CON.value` 是字串 `Constitution`（如果您不記得的話，請檢視[第一個實用程式和列舉教學](./Beginner-Tutorial-Utilities.md)）。

所以要明確的是，

```python 
getattr(self.obj, Ability.CON.value) + 10
```
和寫作一樣

```python 
getattr(your_character, "Constitution") + 10 
```

這與執行以下操作相同：

```python 
your_character.Constitution + 10 
```

在我們的程式碼中，我們編寫 `getattr(self.obj, Ability.CON.value, 1)` - 額外的 `1` 意味著如果 `self.obj` 上不存在屬性“Constitution”，我們不應該出錯，而應該返回 1。


(count_slots)=
### `.count_slots`

在這個幫助程式中，我們使用兩個 Python 工具 - `sum()` 函式和 [列表理解](https://www.w3schools.com/python/python_lists_comprehension.asp)。前者只是將任何可迭代的值加在一起。後者是建立清單的更有效方法：

    new_list = [item for item in some_iterable if condition]
    all_above_5 = [num for num in range(10) if num > 5]  # [6, 7, 8, 9]
    all_below_5 = [num for num in range(10) if num < 5]  # [0, 1, 2, 3, 4]

為了更容易理解，請嘗試將上面的最後一行讀作「對於 0-9 範圍內的每個數字，選擇所有值低於 5 的數字並列出它們」。您也可以將此類推導式直接嵌入到函式呼叫中，例如 `sum()`，而無需在其周圍使用 `[]`。

在`count_slots`中我們有這樣的程式碼：

```python 
wield_usage = sum(
    getattr(slotobj, "size", 0)
    for slot, slotobj in slots.items()
    if slot is not WieldLocation.BACKPACK
)
```

我們應該能夠遵循除 `slots.items()` 之外的所有內容。由於 `slots` 是 `dict`，我們可以使用 `.items()` 來取得 `(key, value)` 對的序列。我們將它們儲存在 `slot` 和 `slotobj` 中。所以上面可以理解為「對於`slots`中的每一個`slot`和`slotobj`-對，檢查它在哪個插槽位置。如果它_不在_在揹包中，則獲取它的大小並將其新增到列表中。對所有這些求和
尺寸」。

一種不太緊湊但可能更可讀的編寫方法是：

```python 
backpack_item_sizes = [] 
for slot, slotobj in slots.items(): 
    if slot is not WieldLocation.BACKPACK:
       size = getattr(slotobj, "size", 0) 
       backpack_item_sizes.append(size)
wield_usage = sum(backpack_item_sizes)
```

對於 BACKPACK 槽中實際的專案也執行相同的操作。總尺寸已新增
在一起。

(validating-slots)=
### 驗證插槽

有了這些助手，`validate_slot_usage` 現在就變得簡單了。我們用`max_slots`來看看我們能攜帶多少。然後，我們取得已經使用的插槽數量（`count_slots`），並檢視新的 `obj` 的大小對我們來說是否太大。

(add-and-remove)=
## `.add` 和 `.remove`

我們會將其設定為 `.add` 將某些東西放入 `BACKPACK` 位置，並且 `remove` 將其丟棄，無論它在哪裡（即使它在您手中）。

```python 
# mygame/evadventure/equipment.py 

from .enums import WieldLocation, Ability

# ... 

class EquipmentHandler: 

    # ... 
     
    def add(self, obj):
        """
        Put something in the backpack.
        """
        if self.validate_slot_usage(obj):
	        self.slots[WieldLocation.BACKPACK].append(obj)
	        self._save()

 def remove(self, obj_or_slot):
        """
        Remove specific object or objects from a slot.

        Returns a list of 0, 1 or more objects removed from inventory.
        """
        slots = self.slots
        ret = []
        if isinstance(obj_or_slot, WieldLocation):
            # a slot; if this fails, obj_or_slot must be obj
            if obj_or_slot is WieldLocation.BACKPACK:
                # empty entire backpack
                ret.extend(slots[obj_or_slot])
                slots[obj_or_slot] = []
            else:
                ret.append(slots[obj_or_slot])
                slots[obj_or_slot] = None
        elif obj_or_slot in self.slots.values():
            # obj in use/wear slot
            for slot, objslot in slots.items():
                if objslot is obj_or_slot:
                    slots[slot] = None
                    ret.append(objslot)
        elif obj_or_slot in slots[WieldLocation.BACKPACK]:             # obj in backpack slot
            try:
                slots[WieldLocation.BACKPACK].remove(obj_or_slot)
                ret.append(obj_or_slot)
            except ValueError:
                pass
        if ret:
            self._save()
        return ret
```

在`.add`中，我們利用`validate_slot_usage`來
仔細檢查我們是否確實可以容納該物品，然後將其新增到揹包中。

在 `.remove` 中，我們允許透過 `WieldLocation` 或明確說明要刪除哪個物件來清空。請注意，第一個 `if` 語句檢查 `obj_or_slot` 是否為一個槽。因此，如果失敗，那麼其他 `elif` 中的程式碼可以安全地假設它必須是一個物件！

任何移除的物件都會被傳回。如果我們指定 `BACKPACK` 作為插槽，我們會清空揹包並返回其中的所有物品。

每當我們更改裝置載入時，我們必須確保結果為`._save()`，否則伺服器重新載入後它將遺失。

(moving-things-around)=
## 移動東西
 
在`.remove()`和`.add()`的幫助下，我們可以將東西進出`BACKPACK`裝置位置。我們還需要從揹包中取出東西並使用或穿著它。我們在 `EquipmentHandler` 上新增一個 `.move` 方法來執行此操作：

```python 
# mygame/evadventure/equipment.py 

from .enums import WieldLocation, Ability

# ... 

class EquipmentHandler: 

    # ... 
    
    def move(self, obj): 
         """Move object from backpack to its intended `inventory_use_slot`.""" 
         
        # make sure to remove from equipment/backpack first, to avoid double-adding
        self.remove(obj) 
        if not self.validate_slot_usage(obj):
            return

        slots = self.slots
        use_slot = getattr(obj, "inventory_use_slot", WieldLocation.BACKPACK)

        to_backpack = []
        if use_slot is WieldLocation.TWO_HANDS:
            # two-handed weapons can't co-exist with weapon/shield-hand used items
            to_backpack = [slots[WieldLocation.WEAPON_HAND], slots[WieldLocation.SHIELD_HAND]]
            slots[WieldLocation.WEAPON_HAND] = slots[WieldLocation.SHIELD_HAND] = None
            slots[use_slot] = obj
        elif use_slot in (WieldLocation.WEAPON_HAND, WieldLocation.SHIELD_HAND):
            # can't keep a two-handed weapon if adding a one-handed weapon or shield
            to_backpack = [slots[WieldLocation.TWO_HANDS]]
            slots[WieldLocation.TWO_HANDS] = None
            slots[use_slot] = obj
        elif use_slot is WieldLocation.BACKPACK:
            # it belongs in backpack, so goes back to it
            to_backpack = [obj]
        else:
            # for others (body, head), just replace whatever's there
            to_backpack = [slots[use_slot]]
            slots[use_slot] = obj
       
        for to_backpack_obj in to_backpack:
            # put stuff in backpack
            if to_backpack_obj:
                slots[WieldLocation.BACKPACK].append(to_backpack_obj)
       
        # store new state
        self._save() 
``` 

這裡我們記得每個 `EvAdventureObject` 都有一個 `inventory_use_slot` 屬性告訴我們它去了哪裡。因此，我們只需將物件移動到該插槽，替換先前該位置中的任何內容。我們替換的任何東西都會返回揹包，只要它實際上是一個物品，而不是 `None`（在我們將物品移到空插槽的情況下）。

(get-everything)=
## 得到一切

為了視覺化我們的庫存，我們需要某種方法來獲取我們攜帶的所有東西。


```python 
# mygame/evadventure/equipment.py 

from .enums import WieldLocation, Ability

# ... 

class EquipmentHandler: 

    # ... 

    def all(self):
        """
        Get all objects in inventory, regardless of location.
        """
        slots = self.slots
        lst = [
            (slots[WieldLocation.WEAPON_HAND], WieldLocation.WEAPON_HAND),
            (slots[WieldLocation.SHIELD_HAND], WieldLocation.SHIELD_HAND),
            (slots[WieldLocation.TWO_HANDS], WieldLocation.TWO_HANDS),
            (slots[WieldLocation.BODY], WieldLocation.BODY),
            (slots[WieldLocation.HEAD], WieldLocation.HEAD),
        ] + [(item, WieldLocation.BACKPACK) for item in slots[WieldLocation.BACKPACK]]
        return lst
```

在這裡，我們獲取所有裝置位置並將它們的內容一起新增到元組列表中
`[(item, WieldLocation),...]`。這樣方便顯示。

(weapon-and-armor)=
## 武器和盔甲

讓 `EquipmentHandler` 輕鬆告訴您目前使用的武器以及所有穿戴的裝備提供的_裝甲_等級是很方便的。否則，您需要弄清楚哪個物品位於哪個揮舞槽中，並在每次需要知道時手動新增裝甲槽。


```python 
# mygame/evadventure/equipment.py 

from .enums import WieldLocation, Ability
from .objects import get_bare_hand

# ... 

class EquipmentHandler: 

    # ... 
    
    @property
    def armor(self):
        slots = self.slots
        return sum(
            (
                # armor is listed using its defense, so we remove 10 from it
                # (11 is base no-armor value in Knave)
                getattr(slots[WieldLocation.BODY], "armor", 1),
                # shields and helmets are listed by their bonus to armor
                getattr(slots[WieldLocation.SHIELD_HAND], "armor", 0),
                getattr(slots[WieldLocation.HEAD], "armor", 0),
            )
        )

    @property
    def weapon(self):
        # first checks two-handed wield, then one-handed; the two
        # should never appear simultaneously anyhow (checked in `move` method).
        slots = self.slots
        weapon = slots[WieldLocation.TWO_HANDS]
        if not weapon:
            weapon = slots[WieldLocation.WEAPON_HAND]
        # if we still don't have a weapon, we return None here
        if not weapon:
 ~          weapon = get_bare_hands()
        return weapon

```

在`.armor()`方法中，我們從每個相關的揮舞槽（身體、盾牌、頭部）中獲取物品（如果有），並抓住它們的`armor` Attribute。然後我們將它們全部`sum()`起來。

在`.weapon()`中，我們只是檢查哪些可能的武器槽（武器手或兩隻手）中有東西。如果不是，我們將退回到我們先前在[物件教學](./Beginner-Tutorial-Objects.md#your-bare-hands)中建立的「Bare Hands」物件。

(fixing-the-character-class)=
### 修復角色類

因此，我們新增了裝置處理程式，以驗證我們放入其中的內容。然而，當我們在遊戲中建立諸如NPCs、e.g之類的東西時，這會導致問題。和

    create/drop monster:evadventure.npcs.EvAdventureNPC

問題是，當/怪物被建立時，它會在被丟棄之前短暫出現在你的庫存中，因此當你這樣做時，此程式碼會向你觸發（假設你是`EvAdventureCharacter`）：

```python
# mygame/evadventure/characters.py
# ... 

class EvAdventureCharacter(LivingMixin, DefaultCharacter): 

    # ... 

    def at_object_receive(self, moved_object, source_location, **kwargs): 
        """ 
        Called by Evennia when an object arrives 'in' the character.
        
        """
        self.equipment.add(moved_object)
```

這意味著裝置處理程式將檢查NPC，並且由於它不是可裝備的東西，因此將引發`EquipmentError`，從而導致建立失敗。由於我們希望能夠輕鬆建立 npc 等，因此我們將使用 `try...except` 語句來處理此錯誤，如下所示：

```python
# mygame/evadventure/characters.py
# ... 
from evennia import logger 
from .equipment import EquipmentError

class EvAdventureCharacter(LivingMixin, DefaultCharacter): 

    # ... 

    def at_object_receive(self, moved_object, source_location, **kwargs): 
        """ 
        Called by Evennia when an object arrives 'in' the character.
        
        """
        try:
            self.equipment.add(moved_object)
        except EquipmentError:
            logger.log_trace()
            
```

使用 Evennia 的 `logger.log_trace()` 我們捕獲錯誤並將其定向到伺服器日誌。這允許您檢視這裡是否也存在真正的錯誤，但是一旦一切正常並且這些錯誤是垃圾郵件，您也可以將 `logger.log_trace()` 行替換為 `pass` 來隱藏這些錯誤。

(extra-credits)=
## 額外學分

這涵蓋了裝置處理程式的基本功能。還有其他有用的方法
可以新增：

- 給定一個物品，找出它目前位於哪個裝置插槽
- 製作一個表示當前載入的字串
- 將所有物品放入揹包（僅限）
- 從揹包中取得所有可使用的物品（武器、盾牌）
- 從揹包中取得所有可用物品（使用位置為`BACKPACK`的物品）

嘗試新增這些。完整的範例位於
[evennia/contrib/tutorials/evadventure/equipment.py](../../../api/evennia.contrib.tutorials.evadventure.equipment.md)。

(unit-testing)=
## 單元測試

> 建立一個新模組`mygame/evadventure/tests/test_equipment.py`。

```{sidebar}
請參閱[evennia/contrib/tutorials/evadventure/tests/test_equipment.py](../../../api/evennia.contrib.tutorials.evadventure.tests.test_equipment.md)
取得完成的測試範例。
```

要測試`EquipmentHandler`，最簡單的是建立一個`EvAdventureCharacter`（現在應該
有 `EquipmentHandler` 可用作為 `.equipment`) 和一些測試物件；然後測試
將它們傳遞到處理程式的方法。


```python 
# mygame/evadventure/tests/test_equipment.py 

from evennia.utils import create 
from evennia.utils.test_resources import BaseEvenniaTest 

from ..objects import EvAdventureObject, EvAdventureHelmet, EvAdventureWeapon
from ..enums import WieldLocation
from ..characters import EvAdventureCharacter

class TestEquipment(BaseEvenniaTest): 
    
    def setUp(self): 
        self.character = create.create_object(EvAdventureCharacter, key='testchar')
        self.helmet = create.create_object(EvAdventureHelmet, key="helmet") 
        self.weapon = create.create_object(EvAdventureWeapon, key="weapon") 
         
    def test_add_remove): 
        self.character.equipment.add(self.helmet)
        self.assertEqual(
            self.character.equipment.slots[WieldLocation.BACKPACK],
            [self.helmet]
        )
        self.character.equipment.remove(self.helmet)
        self.assertEqual(self.character.equipment.slots[WieldLocation.BACKPACK], []) 
        
    # ... 
```

(summary)=
## 概括

_Handlers_ 對於將功能分組在一起非常有用。既然我們花了時間製作`EquipmentHandler`，我們就不必再擔心專案槽了——處理程式為我們「處理」所有細節。只要我們呼叫它的方法，細節就可以忘記。

我們也學會了使用 _hooks_ 將 _Knave_ 的自訂裝置處理繫結到 Evennia 中。

`Characters`、`Objects` 和現在 `Equipment` 就位後，我們應該能夠繼續進行角色生成 - 玩家可以建立自己的角色！
