(cooldowns)=
# 冷卻時間

owllex 的貢獻，2021 年

冷卻時間用於對速率限制的操作進行建模，例如
角色可以執行給定的動作；直到過了一定的時間
指令無法再次使用。這個contrib提供了一個簡單的冷卻時間
可以附加到任何 typeclass 的處理程式。冷卻時間是輕量級的永續性
非同步計時器，您可以查詢該計時器以檢視是否已經過了某個時間。

冷卻時間是完全非同步的，必須查詢才能知道它們的冷卻時間
狀態。它們不會觸發回撥，因此不太適合用例
需要在特定時間表上發生某事（使用延遲或
TickerHandler 代替）。

另請參閱 evennia [操作方法](../Howtos/Howto-Command-Cooldown.md) 以瞭解更多資訊
關於這個概念。

(installation)=
## 安裝

要使用，只需將以下屬性新增至任何的 typeclass 定義中
您想要支援冷卻時間的物件型別。它將暴露一個新的`cooldowns`
將資料儲存到物件的 attribute 儲存的屬性。你可以這樣設定
在你的基地 `Object` typeclass 上啟用每種型別的冷卻時間跟蹤
物件，或只是將其放在您的 `Character` typeclass 上。

預設 CooldownHandler 將使用 `cooldowns` 屬性，但您可以
如果需要，可以透過為 `db_attribute` 傳遞不同的值來自訂此設定
引數。

```python
from evennia.contrib.game_systems.cooldowns import CooldownHandler
from evennia.utils.utils import lazy_property

@lazy_property
def cooldowns(self):
    return CooldownHandler(self, db_attribute="cooldowns")
```

(example)=
## 例子

假設你已經在你的角色typeclasses上安裝了冷卻時間，你可以使用
冷卻時間來限制您執行指令的頻率。下面的程式碼
程式碼片段會將強力攻擊指令的使用限制為每 10 秒一次
每個字元。

```python
class PowerAttack(Command):
    def func(self):
        if self.caller.cooldowns.ready("power attack"):
            self.do_power_attack()
            self.caller.cooldowns.add("power attack", 10)
        else:
            self.caller.msg("That's not ready yet!")

```


----

<small>此檔案頁面是從`evennia\contrib\game_systems\cooldowns\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
