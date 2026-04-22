(slow-exit)=
# 緩慢退出

Griatch 2014 年的貢獻

延遲其遍歷的退出型別的範例。這模擬了
緩慢的移動，在許多遊戲中很常見。 contrib 也
包含兩個指令，`setspeed` 和 `stop` 用於改變移動速度
並分別中止正在進行的遍歷。

(installation)=
## 安裝：

要嘗試這種型別的出口，您可以連線兩個現有房間
使用這樣的東西：

    @open north:contrib.grid.slow_exit.SlowExit = <destination>

若要使其成為新的預設出口，請修改 `mygame/typeclasses/exits.py`
匯入此模組並將預設的 `Exit` 類別變更為繼承
從 `SlowExit` 開始。

```
# in mygame/typeclasses/exits.py

from evennia.contrib.grid.slowexit import SlowExit

class Exit(SlowExit):
    # ...

```

若要獲得改變速度並中止移動的能力，請匯入

```python
# in mygame/commands/default_cmdsets.py

from evennia.contrib.grid import slow_exit  <---

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(slow_exit.SlowDoorCmdSet)  <---

```

只需將此模組中的 CmdSetSpeed 和 CmdStop 匯入並新增到您的
預設cmdset（如果您不確定，請參閱有關如何執行此操作的教學）。

要嘗試這種型別的出口，您可以使用以下指令連線兩個現有房間
像這樣的東西：

    @open north:contrib.grid.slow_exit.SlowExit = <destination>


(notes)=
## 筆記：

這種實現是高效的，但不持久；如此不完整
伺服器重新載入時移動將會遺失。這對大多數人來說是可以接受的
遊戲型別 - 模擬更長的旅行時間（超過幾個
此處假定秒），使用 Scripts 或的更持久的變體
TickerHandler 可能會更好。


----

<small>此檔案頁面是從`evennia\contrib\grid\slow_exit\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
