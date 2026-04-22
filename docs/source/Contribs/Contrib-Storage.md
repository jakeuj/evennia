(item-storage)=
# 物品存放

helpme 的貢獻 (2024)

此模組允許將某些房間標記為存放位置。

在這些房間中，玩家可以`list`、`store`和`retrieve`物品。儲存可以是共享的，也可以是單獨的。

(installation)=
## 安裝

該實用程式會新增與儲存相關的指令。將模組匯入到您的指令中並將其新增至您的指令集中以使其可用。

具體來說，在`mygame/commands/default_cmdsets.py`中：

```python
...
from evennia.contrib.game_systems.storage import StorageCmdSet   # <---

class CharacterCmdset(default_cmds.Character_CmdSet):
    ...
    def at_cmdset_creation(self):
        ...
        self.add(StorageCmdSet)  # <---

```

然後`reload` 使`list`、`retrieve`、`store` 和`storage` 指令可用。

(usage)=
## 用法

若要將某個位置標記為具有專案儲存，請使用 `storage` 指令。預設情況下，這是一個建構器等級的指令。儲存可以共享，這意味著使用儲存的每個人都可以存取儲存在其中的所有專案，也可以單獨訪問，這意味著只有儲存專案的人才能檢索它。有關詳細資訊，請參閱 `help storage`。

(technical-info)=
## 科技資訊

這是一個基於 tag 的系統。設定為儲藏室的房間帶有識別符號，將其標記為共享或非共享。儲存在這些房間中的物品都標有儲藏室識別符號，如果儲藏室不共享，則標記有角色識別符號，然後將它們從網格i.e中刪除。他們的位置設定為`None`。檢索後，物品將被取消標記並移回角色庫存。

當使用 `storage` 指令取消將房間標記為儲存空間時，所有儲存的物件都將取消標記並放入該房間。您應該使用 `storage` 指令來建立和刪除儲存，否則儲存的物件可能會遺失。

----

<small>此檔案頁面是從`evennia\contrib\game_systems\storage\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
