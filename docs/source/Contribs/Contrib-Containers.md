(containers)=
# 貨櫃
貢獻者InspectorCaracal (2023)

透過提供容器 typeclass 並擴充套件某些基本指令，增加將物件放入其他容器物件的能力。

(installation)=
## 安裝

要安裝、匯入 `ContainerCmdSet` 並將其新增至 `default_cmdsets.py` 檔案中的 `CharacterCmdSet`：

```python
from evennia.contrib.game_systems.containers import ContainerCmdSet

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    
    def at_cmdset_creation(self):
        # ...
        self.add(ContainerCmdSet)
```

這會將預設的 `look` 和 `get` 指令替換為 contrib 提供的容器友善版本，並新增新的 `put` 指令。

(usage)=
## 用法

contrib 包括 `ContribContainer` typeclass，它具有用作容器所需的所有設定。使用時，您需要做的就是在遊戲中建立一個帶有 typeclass 的物件 - 它也會自動繼承您在基礎物件 typeclass 中實現的任何內容。

    create bag:game_systems.containers.ContribContainer

contrib 的 `ContribContainer` 具有其可容納的最大物品數量的容量限制。這可以針對每個單獨的物件進行更改。

在程式碼中：
```py
obj.capacity = 5
```
遊戲中：

    set box/capacity = 5

您也可以透過設定 `get_from` lock 型別來使任何其他物件可用作容器。

    lock mysterious box = get_from:true()

(extending)=
## 延伸

`ContribContainer` 類別旨在按原樣使用，但您也可以為自己的容器類別繼承它以擴充套件其功能。除了在物件建立時預先設定容器 lock 之外，它還具有三個主要附加功能：

(capacity-property)=
### `capacity`屬性

`ContribContainer.capacity` 是一個 `AttributeProperty` - 意味著您可以在程式碼中使用 `obj.capacity` 存取它，也可以在遊戲中使用 `set obj/capacity = 5` 設定它 - 它將容器的容量表示為整數。您可以使用自己的容器類別上更複雜的容量表示來覆蓋它。

(at_pre_get_from-and-at_pre_put_in-methods)=
### `at_pre_get_from` 和 `at_pre_put_in` 方法

當嘗試從容器取得物件或將物件放入容器時，`ContribContainer` 上的這兩個方法將被呼叫作為額外檢查。預設情況下，contrib 的 `ContribContainer.at_pre_get_from` 不執行任何附加驗證，而 `ContribContainer.at_pre_put_in` 執行簡單的容量檢查。

您可以在自己的子類別上重寫這些方法以執行任何其他容量或存取檢查。

----

<small>此檔案頁面是從`evennia\contrib\game_systems\containers\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
