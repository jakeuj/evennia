(simpledoor)=
# SimpleDoor

Griatch 的貢獻，2016 年

一個簡單的雙向出口，代表一扇可以開啟和關閉的門
從兩側關閉。可以輕鬆擴充套件以使其可鎖定，
可破壞等

請注意，simpledoor是基於Evennia鎖定的，所以它會
不適用於超級使用者（繞過所有鎖）。超級使用者
似乎總是能夠一遍又一遍地關/開門
沒有鎖阻止你。要使用門，請使用 `quell` 或
非超級使用者帳戶。

(installation)=
## 安裝：

將 `SimpleDoorCmdSet` 從此模組匯入至 `mygame/commands/default_cmdsets`
並將其新增到您的`CharacterCmdSet`：

```python
# in mygame/commands/default_cmdsets.py

from evennia.contrib.grid import simpledoor  <---

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(simpledoor.SimpleDoorCmdSet)

```

(usage)=
## 用法：

要嘗試一下，`dig`一個新房間，然後使用（超載）`@open`
指令開啟一個新的大門，如下所示：

    @open doorway:contrib.grid.simpledoor.SimpleDoor = otherroom

    open doorway
    close doorway

注意：這使用鎖，因此如果您是超級使用者，您將不會被阻止
鎖著的門 - `quell` 你自己，如果是的話。普通使用者會發現他們
一旦門從另一側關閉，就無法透過門的任何一側
邊。


----

<small>此檔案頁面是從`evennia\contrib\grid\simpledoor\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
