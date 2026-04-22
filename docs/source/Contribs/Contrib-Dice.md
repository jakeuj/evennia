(dice-roller)=
# 骰滾筒

Griatch 的貢獻，2012 年、2023 年

適用於任意數量和麵的骰子的骰子滾輪。新增遊戲中的骰子滾動
（如 `roll 2d10 + 1`）以及條件（低於/高於/等於目標）
以及程式碼中擲骰子的函式。指令還支援隱藏或秘密
供人類遊戲大師使用的捲。


(installation)=
## 安裝：


將此模組中的 `CmdDice` 指令新增至角色的 cmdset
（然後重新啟動伺服器）：

```python
# in mygame/commands/default_cmdsets.py

# ...
from evennia.contrib.rpg import dice  <---

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(dice.CmdDice())  # <---

```

(usage)=
## 用法：

    > roll 1d100 + 2
    > roll 1d20
    > roll 1d20 - 4

滾動的結果將迴響到房間。

也可以指定一個標準的 Python 運運算元來指定
最終目標數字並獲得公平且有保證的結果
公正的方式。  例如：

    > roll 2d6 + 2 < 8

滾動將通知所有各方滾動是否確實低於 8。

    > roll/hidden 1d100

通知房間正在進行擲骰，但不告知結果如何
是。

    > roll/secret 1d20

這是一個隱藏的捲，不會告知房間它發生了。

(rolling-dice-from-code)=
## 從程式碼擲骰子

您可以將第一個引數指定為標準 RPG d 語法上的字串（NdM，
其中 N 是要擲骰子的數量，M 是每個骰子的面數）：

```python
from evennia.contrib.rpg.dice import roll

roll("3d10 + 2")
```

您也可以給出條件（然後您將得到 `True`/`False` 返回）：

```python
roll("2d6 - 1 >= 10")
```

如果將第一個引數指定為整數，它將被解釋為
擲骰子，然後您可以更明確地建立骰子。這可以是
如果您將滾筒與其他系統一起使用並且想要
用元件構造捲筒。


```python
roll(dice, dicetype=6, modifier=None, conditional=None, return_tuple=False,
      max_dicenum=10, max_dicetype=1000)
```

以下是如何使用顯式語法滾動 `3d10 + 2`：

```python
roll(3, 10, modifier=("+", 2))
```

以下是滾動 `2d6 - 1 >= 10` 的方法（您將獲得 `True`/`False` 回報）：

```python
roll(2, 6, modifier=("-", 1), conditional=(">=", 10))
```

(dice-pools-and-other-variations)=
### 骰子池和其他變體

您一次只能擲一組骰子。如果您的 RPG 要求您投擲多個
骰子組並以更高階的方式組合它們，您可以使用多個骰子來實現
`roll()` 呼叫。根據您的需要，您可能只想將其表達為
特定於您的遊戲的輔助函式。

以下是如何進行 D&D 優勢擲骰（擲 d20 兩次，選出最高）：

```python
    from evennia.contrib.rpg.dice import roll

    def roll_d20_with_advantage():
        """Get biggest result of two d20 rolls"""
        return max(roll("d20"), roll("d20"))

```

這是一個自由聯盟風格骰子池的範例，您可以在其中擲一堆 d6
並想知道你得到了多少個 1 和 6：

```python
from evennia.contrib.rpg.dice import roll

def roll_dice_pool(poolsize):
    """Return (number_of_ones, number_of_sixes)"""
    results = [roll("1d6") for _ in range(poolsize)]
    return results.count(1), results.count(6)

```



(get-all-roll-details)=
### 獲取所有捲的詳細資訊

如果您需要單獨的擲骰（e.g。對於骰子池），請設定 `return_tuple` kwarg：

```python
roll("3d10 > 10", return_tuple=True)
(13, True, 3, (3, 4, 6))  # (result, outcome, diff, rolls)
```

回傳的是一個元組 `(result, outcome, diff, rolls)`，其中 `result` 是
擲骰結果，若條件為 `outcome` 則為 `True/False`
給定（`None` 否則），`diff` 是
條件和結果（`None` 否則）和 `rolls` 是一個包含
單獨的擲骰結果。


----

<small>此檔案頁面是從`evennia\contrib\rpg\dice\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
