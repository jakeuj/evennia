(give-objects-weight)=
# 賦予物體重量

您可以觸控的所有遊戲內物體通常都有一定的重量。重量的作用因遊戲而異。通常它會限制您可以攜帶的數量。如果一塊重石頭落在您身上，對您的傷害也可能比氣球更大。如果你想玩點花俏的，壓力板只有踩在壓力板上的人夠重時才可能觸發。

```{code-block} python 
:linenos:
:emphasize-lines: 6,8,10,12

# inside your mygame/typeclasses/objects.py

from evennia import DefaultObject 
from evennia import AttributeProperty 

class ObjectParent: 

    weight = AttributeProperty(default=1, autocreate=False)

    @property 
    def total_weight(self):
        return self.weight + sum(obj.total_weight for obj in self.contents) 


class Object(ObjectParent, DefaultObject):
    # ...
```

```{sidebar} 為什麼不是大眾？
是的，我們知道重量隨重力而改變。 「彌撒」在科學上更正確。但「質量」在 RPGs 中不太常用，所以我們在這裡堅持使用「重量」。只要知道您的科幻角色是否可以在月球（地球重力的 1/6）上度假，您應該考慮在任何地方使用 `mass` 並即時計算當前重量。
```

- **第 6 行**：我們使用 `ObjectParent` mixin。由於此 mixin 用於 `Characters`、`Exits` 和 `Rooms` 以及 `Object`，這意味著所有這些都將自動_也_具有權重！
- **第 8 行**：我們使用 [AttributeProperty](../Components/Attributes.md#using-attributeproperty) 設定「預設」權重 1（無論是什麼）。設定 `autocreate=False` 意味著在權重從預設值 1 實際變更之前不會建立實際的 `Attribute`。請參閱 `AttributeProperty` 檔案以瞭解與此相關的注意事項。
- **第 10 行和第 11 行**：在 `total_weight` 上使用 `@property` 裝飾器意味著我們稍後可以呼叫 `obj.total_weight` 而不是 `obj.total_weight()`。
- **第 12 行**：我們透過迴圈 `self.contents` 來總結該物件「中」的所有內容的所有權重。由於現在_所有_物體都有重量，所以這應該總是有效！

讓我們看看一些值得信賴的盒子的重量
```
> create/drop box1
> py self.search("box1").weight
1 
> py self.search("box1").total_weight
1 
``` 

讓我們將另一個盒子放入第一個盒子中。

```
> create/drop box2 
> py self.search("box2").total_weight
1 
> py self.search("box2").location = self.search("box1")
> py self.search(box1).total_weight 
2
```


(limit-inventory-by-weight-carried)=
## 按攜帶重量限制庫存

要限制自己可以攜帶的東西，首先要了解自己的力量

```python
# in mygame/typeclasses/characters.py 

from evennia import AttributeProperty

# ... 

class Character(ObjectParent, DefaultCharacter): 

    carrying_capacity = AttributeProperty(10, autocreate=False)

    @property
    def carried_weight(self):
        return self.total_weight - self.weight

```

在這裡，我們確保新增另一個 `AttributeProperty` 告訴我們要攜帶多少。在真實遊戲中，這可能取決於角色的強度。當我們考慮我們已經攜帶了多少重量時，我們不應該包括我們自己的重量，所以我們減去它。

為了遵守此限制，我們需要覆蓋預設的 `get` 指令。


```{sidebar} 覆蓋預設指令

在此範例中，我們實現了 `CmdGet` 的開頭，然後在末尾呼叫完整的 `CmdGet()`。這不是很有效，因為父級 `CmdGet` 必須再次執行 `caller.search()`。為了提高效率，您可能需要將整個 `CmdGet` 程式碼複製到您自己的版本中並進行修改。
```

```python 
# in mygame/commands/command.py 

# ... 
from evennia import default_cmds 

# ... 

class WeightAwareCmdGet(default_cmds.CmdGet):

    def func(self):
        caller = self.caller 
        if not self.args: 
            caller.msg("Get what?")
            return 

        obj = caller.search(self.args)

        if (obj.weight + caller.carried_weight 
                > caller.carrying_capacity):
            caller.msg("You can't carry that much!")
            return 
        super().func()
```

在這裡，我們對要拾取的物體的重量新增了額外的檢查，然後我們將正常的 `CmdGet` 稱為 `super().func()`。
