(npcs-reacting-to-your-presence)=
# NPCs 對你的出現做出反應


    > north 
    ------------------------------------
    Meadow
    You are standing in a green meadow. 
    A bandit is here. 
    ------------------------------------
    Bandit gives you a menacing look!

本教學展示了 NPC 物件的實現，該物件響應輸入的字元
位置。

我們需要的是以下內容：

- 當有人進入時可以做出反應的NPC typeclass。
- 自訂[房間](../Components/Objects.md#rooms)typeclass，可以告訴NPC有人進入。
- 我們也會稍微調整預設的`Character` typeclass。

```python
# in mygame/typeclasses/npcs.py  (for example)

from typeclasses.characters import Character

class NPC(Character):
    """
    A NPC typeclass which extends the character class.
    """
    def at_char_entered(self, character, **kwargs):
        """
        A simple is_aggressive check.
        Can be expanded upon later.
        """
        if self.db.is_aggressive:
            self.execute_cmd(f"say Graaah! Die, {character}!")
        else:
            self.execute_cmd(f"say Greetings, {character}!")
```

```{sidebar} 傳遞額外訊息
請注意，我們此處不使用 `**kwargs` 屬性。這可用於將額外資訊傳遞到遊戲中的掛鉤中，並在您建立自訂移動指令時使用。例如，如果您`run`進入房間，您可以透過執行`obj.move_to(..., running=True)`通知所有鉤子。也許你的圖書館員NPC應該對跑進他們圖書館的人有單獨的反應！

我們確保從下面的標準 `at_object_receive` 掛鉤傳遞 `**kwargs`。
```

這裡我們對`NPC`˙做了一個簡單的方法，稱為`at_char_entered`。我們期望當（玩家）角色進入房間時呼叫它。我們實際上並沒有預先設定`is_aggressive` [Attribute](../Components/Attributes.md)；我們將其留給管理員在遊戲中啟動。如果沒有設定，NPC 就是非敵對的。

每當_something_進入`Room`時，它的[at_object_receive](DefaultObject.at_object_receive)鉤子就會被呼叫。所以我們應該重寫它。


```python
# in mygame/typeclasses/rooms.py

from evennia import utils

# ... 

class Room(ObjectParent, DefaultRoom):

    # ... 
    
    def at_object_receive(self, arriving_obj, source_location, **kwargs):
        if arriving_obj.account: 
            # this has an active acccount - a player character
            for item in self.contents:
                # get all npcs in the room and inform them
                if utils.inherits_from(item, "typeclasses.npcs.NPC"):
                    item.at_char_entered(arriving_obj, **kwargs)

```

```{sidebar} 通用物件方法
請記住，房間是`Objects`，其他物件也有這些相同的鉤子。因此，當你拿起某樣東西時，`at_object_receive` 鉤子會為你觸發（讓你「收到」它）。或例如在盒子裡放東西時。
```
目前操縱的角色將附加一個 `.account`。我們用它來知道到達的東西是一個角色。然後，我們使用 Evennia 的 [utils.inherits_from](evennia.utils.utils.inherits_from) 輔助實用程式來取得房間中的每個 NPC 可以使用他們新建立的 `at_char_entered` 方法。

確保`reload`。

讓我們建立一個 NPC 並使其具有攻擊性。在本範例中，我們假設您的名字是“Anna”，並且您目前位置的北邊有一個房間。

    > create/drop Orc:typeclasses.npcs.NPC
    > north 
    > south 
    Orc says, Greetings, Anna!

現在讓獸人變得更具攻擊性。

    > set orc/is_aggressive = True 
    > north 
    > south 
    Orc says, Graah! Die, Anna!

這是一個容易激怒的獸人！