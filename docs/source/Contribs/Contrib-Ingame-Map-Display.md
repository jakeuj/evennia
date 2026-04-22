(basic-map)=
# 基本地圖

貢獻 - helpme 2022

這會將 ascii `map` 新增到給定房間，可以使用 `map` 指令檢視該房間。
您可以輕鬆地更改它以新增特殊字元、房間顏色等。顯示的地圖是
使用時動態生成，並支援所有羅盤方向和向上/向下。其他
方向被忽略。

如果您不希望地圖經常更新，您可以選擇儲存
將地圖計算為房間上的.ndb 值並渲染它而不是執行對映
每次重新計算。

(installation)=
## 安裝：

將 `MapDisplayCmdSet` 新增至預設字元 cmdset 將新增 `map` 指令。

具體來說，在`mygame/commands/default_cmdsets.py`中：

```python
...
from evennia.contrib.grid.ingame_map_display import MapDisplayCmdSet   # <---

class CharacterCmdset(default_cmds.CharacterCmdSet):
    ...
    def at_cmdset_creation(self):
        ...
        self.add(MapDisplayCmdSet)  # <---

```

然後`reload` 使新指令可用。

(settings)=
## 設定:

為了更改預設地圖大小，您可以新增到`mygame/server/settings.py`：

```python
BASIC_MAP_SIZE = 5  # This changes the default map width/height.

```

(features)=
## 特徵：

(ascii-map-and-evennia-supports-utf-8-characters-and-even-emojis)=
### ASCII 地圖（evennia 支援 UTF-8 個字元，甚至表情符號）

這會為可設定大小的玩家產生 ASCII 地圖。

(new-command)=
### 新指令

- `CmdMap` - 檢視地圖


----

<small>此檔案頁面是從`evennia\contrib\grid\ingame_map_display\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
