(adding-command-cooldowns)=
# 新增指令冷卻時間

    > hit goblin with sword 
    You strike goblin with the sword. It dodges! 
    > hit goblin with sword 
    You are off-balance and can't attack again yet.

某些型別的遊戲想要限制指令執行的頻率。如果一個
角色施展咒語 *Firestorm*，您可能不希望他們傳送垃圾郵件
一遍又一遍地指揮。在先進的戰鬥系統中，大幅度的擺動可能會
提供大量損壞的機會，但代價是無法重做
一會兒。

此類效果稱為「指令冷卻時間」。

```{sidebar}
[冷卻contrib](../Contribs/Contrib-Cooldowns.md)是指令冷卻的現成解決方案。它基於這個howto並在物件上實作了一個[handler](Tutorial-Peristent-Handler)來方便地管理和儲存冷卻時間。
```
本指南舉例說明瞭一種非常節省資源的冷卻方式。一個更多
「主動」方式是使用非同步延遲，如 [Command-Duration howto](./Howto-Command-Duration.md#blocking-commands) 中建議的那樣。  如果您想在冷卻結束後向使用者回顯一些訊息，那麼將這兩個指南結合起來可能會很有用。

(an-efficient-cooldown)=
## 高效率的冷卻時間

這個想法是，當 [Command](../Components/Commands.md) 執行時，我們儲存它執行的時間。當它下次執行時，我們再次檢查當前時間。只有在自現在和上次執行以來經過了足夠的時間後，才允許執行該指令。這是一個非常有效率的實現，僅按需檢查。

```python
# in, say, mygame/commands/spells.py

import time
from evennia import default_cmds

class CmdSpellFirestorm(default_cmds.MuxCommand):
    """
    Spell - Firestorm

    Usage:
      cast firestorm <target>

    This will unleash a storm of flame. You can only release one
    firestorm every five minutes (assuming you have the mana).
    """
    key = "cast firestorm"
    rate_of_fire = 60 * 2  # 2 minutes

    def func(self):
        "Implement the spell"

        now = time.time()
        last_cast = caller.db.firestorm_last_cast  # could be None
        if last_cast and (now - last_cast < self.rate_of_fire):
            message = "You cannot cast this spell again yet."
            self.caller.msg(message)
            return

        # [the spell effect is implemented]

        # if the spell was successfully cast, store the casting time
        self.caller.db.firestorm_last_cast = now
```

我們指定 `rate_of_fire`，然後檢查 `caller.` 上的 [Attribute](../Components/Attributes.md) `firestorm_last_cast` 它是 `None` （因為該法術以前從未施展過）或表示該法術上次施展時間的時間戳。

(non-persistent-cooldown)=
### 非持續冷卻時間

上述實作將在重新載入後繼續存在。如果您不希望這樣，您可以改為讓 `firestorm_last_cast` 成為 [NAtrribute](../Components/Attributes.md#in-memory-attributes-nattributes)。例如：

```python
        last_cast = caller.ndb.firestorm_last_cast
        # ... 
        self.caller.ndb.firestorm_last_cast = now 
```
即，使用 `.ndb` 而不是 `.db`。由於 `NAttribute`s 純粹位於記憶體中，因此它們的讀取和寫入速度比 `Attribute` 更快。因此，如果您的間隔很短並且需要經常改變，那麼這可能是更理想的選擇。缺點是如果伺服器重新載入，它們會重置。

(make-a-cooldown-aware-command-parent)=
## 建立一個冷卻感知指令父級

如果你有許多不同的法術或其他有冷卻時間的指令，你就不需要
想要每次都新增此程式碼。相反，你可以進行“冷卻”
指令 mixin”類別。_mixin_ 是一個可以“新增”到另一個類別的類
（透過多重繼承）賦予它一些特殊的能力。這是一個例子
具有永續性儲存：

```python
# in, for example, mygame/commands/mixins.py

import time

class CooldownCommandMixin:

    rate_of_fire = 60
    cooldown_storage_key = "last_used"
    cooldown_storage_category = "cmd_cooldowns"

    def check_cooldown(self):
        last_time = self.caller.attributes.get(
            key=self.cooldown_storage_key,
            category=self.cooldown_storage_category)
        )
        return (time.time() - last_time) < self.rate_of_fire

    def update_cooldown(self):
        self.caller.attribute.add(
            key=self.cooldown_storage_key,
            value=time.time(),
            category=self.cooldown_storage_category

        )
```

這意味著要混合到指令中，因此我們假設 `self.caller` 存在。
我們允許設定使用 Attribute 鍵/類別來儲存冷卻時間。

它還使用 Attribute-類別來確保它儲存的內容不會混淆
與呼叫者的其他屬性。

它的使用方法如下：

```python
# in, say, mygame/commands/spells.py

from evennia import default_cmds
from .mixins import CooldownCommandMixin


class CmdSpellFirestorm(
        CooldownCommandMixin, default_cmds.MuxCommand):
    key = "cast firestorm"

    cooldown_storage_key = "firestorm_last_cast"
    rate_of_fire = 60 * 2

    def func(self):

        if not self.check_cooldown():
            self.caller.msg("You cannot cast this spell again yet.")
            return

        # [the spell effect happens]

        self.update_cooldown()

```

所以和以前一樣，我們剛剛隱藏了冷卻時間檢查，你可以
在所有冷卻時間中重複使用此 mixin。

(command-crossover)=
### 指令交叉

這個冷卻檢查範例也適用於*之間*指令。例如，
你可以讓所有與火焰相關的法術儲存相同的冷卻時間
`cooldown_storage_key`（如`fire_spell_last_used`）。這意味著鑄造
*火焰風暴*會在一段時間內阻擋所有其他與火焰相關的法術。

同樣，當你揮出大劍時，其他型別的攻擊也可能會發生。
在您恢復餘額之前被封鎖。
