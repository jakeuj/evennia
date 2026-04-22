(non-player-characters)=
# 非玩家角色

```{sidebar} vNPC
您通常應該避免建立數百個 NPC 物件來填充您的「繁忙城鎮」 - 在文字遊戲中，這麼多 NPCs 只會在螢幕上傳送垃圾郵件並惹惱您的玩家。由於這是一個文字遊戲，您通常可以使用_vNPcs_ - 虛擬NPCs。 vNPC僅以文字描述——房間可以被描述為熙熙攘攘的街道，農民可以被描述為互相喊叫。為此使用房間描述效果很好，但有關 [EvAdventure 房間](./Beginner-Tutorial-Rooms.md) 的教學課程中有一個名為 [向房間新增生命](./Beginner-Tutorial-Rooms.md#adding-life-to-a-room) 的部分，可用於使 vNPC 看起來在後臺執行操作。
```

_非玩家角色_，或 NPCs，是所有不受玩家控制的活躍代理的通用術語。 NPCs 可以是任何東西，從商人和任務提供者，到怪物和老闆。 他們也可以是「風味」角色，例如做家務的城鎮居民、耕作的農夫，讓世界感覺「更有活力」。

在本課中，我們將基於 _Knave_ 規則集建立 _EvAdventure_ NPCs 的基底類別。根據_Knave_規則，與我們之前設計的[PC字元](./Beginner-Tutorial-Characters.md)相比，NPCs有一些簡化的統計資料。

<div style="clear: right;"></div>

(the-npc-base-class)=
## NPC基類

```{sidebar}
有關 npc 模組的現成範例，請參閱 [evennia/contrib/tutorials/evadventure/npcs.py](evennia.contrib.tutorials.evadventure.npcs)。
```
> 建立一個新模組`evadventure/npcs.py`。

```{code-block} python
:linenos: 
:emphasize-lines: 9, 12, 13, 15, 17, 19, 25, 23, 59, 61

# in evadventure/npcs.py 

from evennia import DefaultCharacter, AttributeProperty

from .characters import LivingMixin
from .enums import Ability
from .objects import get_bare_hands

class EvAdventureNPC(LivingMixin, DefaultCharacter): 
	"""Base class for NPCs""" 

    is_pc = False
    hit_dice = AttributeProperty(default=1, autocreate=False)
    armor = AttributeProperty(default=1, autocreate=False)  # +10 to get armor defense
    hp_multiplier = AttributeProperty(default=4, autocreate=False)  # 4 default in Knave
    hp = AttributeProperty(default=None, autocreate=False)  # internal tracking, use .hp property
    morale = AttributeProperty(default=9, autocreate=False)
    allegiance = AttributeProperty(default=Ability.ALLEGIANCE_HOSTILE, autocreate=False)

    weapon = AttributeProperty(default=get_bare_hands, autocreate=False)  # instead of inventory
    coins = AttributeProperty(default=1, autocreate=False)  # coin loot
 
    is_idle = AttributeProperty(default=False, autocreate=False)
    
    @property
    def strength(self):
        return self.hit_dice
        
    @property
    def dexterity(self):
        return self.hit_dice
 
    @property
    def constitution(self):
        return self.hit_dice
 
    @property
    def intelligence(self):
        return self.hit_dice
 
    @property
    def wisdom(self):
        return self.hit_dice
 
    @property
    def charisma(self):
        return self.hit_dice
 
    @property
    def hp_max(self):
        return self.hit_dice * self.hp_multiplier
    
    def at_object_creation(self):
         """
         Start with max health.
  
         """
         self.hp = self.hp_max
         self.tags.add("npcs", category="group")


class EvAdventureMob(EvAdventureNPC): 
    """
    Mob(ile) NPC to be used for enemies.
     
    """

```

- **第 9 行**：透過使用_多重繼承_，我們使用我們在[角色課程](./Beginner-Tutorial-Characters.md)中建立的`LinvingMixin`。這包括許多有用的方法，例如顯示我們的「傷害等級」、用於治療的方法、受到攻擊、傷害時呼叫的鉤子等等。我們可以在即將到來的 NPC 子類別中重複使用所有這些。
- **第 12 行**：`is_pc` 是一種快速便捷的方法來檢查這是否是 PC。我們將在接下來的[戰鬥基礎課程](./Beginner-Tutorial-Combat-Base.md)中使用它。
- **第 13 行**：NPC 被簡化，因為所有統計資料僅基於 `Hit dice` 數字（請參閱 **第 25-51 行**）。我們將 `armor` 和 `weapon` 作為直接[屬性](../../../Components/Attributes.md) 儲存在班級上，而不是費心實現完整的裝備系統。
- **第 17、18 行**：`morale` 和 `allegiance` 是 _Knave_ 屬性，決定 NPC 在戰鬥情況下逃跑的可能性以及他們是敵對還是友好。
- **第 19 行**：`is_idle` Attribute 是一個有用的屬性。它應該在所有 NPCs 上可用，並將用於完全停用 AI。
- **第 59 行**：我們確保 tag NPCs。我們可能希望稍後將不同的 NPCs 分組在一起，例如，如果其中一個受到攻擊，則讓所有具有相同 tag 的 NPCs 做出回應。

我們建立一個空子類別`EvAdventureMob`。 「暴民」（「移動」的縮寫）是一個常見的 MUD 術語，表示可以自行移動的 NPCs。我們將來將使用這個類別來代表遊戲中的敵人。我們將回到這堂課[在關於新增AI的課程中][Beginner-Tutoroal-AI]。

(testing)=
## 測試

> 建立一個新模組`evadventure/tests/test_npcs.py`

還沒有太多需要測試的內容，但我們將來將使用相同的模組來測試 NPCs 的其他方面，所以讓我們現在建立它。

```python 
# in evadventure/tests/test_npcs.py

from evennia import create_object                                           
from evennia.utils.test_resources import EvenniaTest                        
                                                                            
from .. import npcs                                                         
                                                                            
class TestNPCBase(EvenniaTest):                                             
	"""Test the NPC base class""" 
	
    def test_npc_base(self):
        npc = create_object(
            npcs.EvAdventureNPC,
            key="TestNPC",
            attributes=[("hit_dice", 4)],  # set hit_dice to 4
        )
        
        self.assertEqual(npc.hp_multiplier, 4)
        self.assertEqual(npc.hp, 16)
        self.assertEqual(npc.strength, 4)
        self.assertEqual(npc.charisma, 4)



```

這裡沒什麼特別的。請注意 `create_object` 輔助函式如何將 `attributes` 作為關鍵字。這是一個元組列表，我們用來為屬性設定與預設值不同的值。然後我們檢查一些屬性以確保它們傳回我們期望的結果。


(conclusions)=
## 結論

在_Knave_中，NPC是玩家角色的簡化版本。在其他遊戲和規則系統中，它們可能幾乎完全相同。

NPC 類別就位後，我們就足以建立一個「測試虛擬物件」。由於它還沒有AI，所以它不會反擊，但當我們在接下來的課程中測試我們的戰鬥時，有東西可以擊中就足夠了。
