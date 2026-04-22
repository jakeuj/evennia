(crafting-system)=
# 製作系統

Gratch 2020 的貢獻

這實現了完整的製作系統。原則就是“食譜”，
您將物品（標記為成分）組合起來創造出新的東西。食譜還可以
需要某些（非消耗性）工具。一個例子是使用“麵包配方”
將「麵粉」、「水」和「酵母」與「烤箱」結合起來烘烤「一條麵包」。

配方過程可以這樣理解：

    ingredient(s) + tool(s) + recipe -> object(s)

在這裡，「原料」是在製作過程中消耗的，而「工具」是
該過程所必需的，但不會被該過程破壞。

包含的 `craft` 指令的工作方式如下：

    craft <recipe> [from <ingredient>,...] [using <tool>, ...]

(examples)=
## 範例

使用`craft`指令：

    craft toy car from plank, wooden wheels, nails using saw, hammer

食譜不需要使用工具，甚至不需要使用多種食材：

    snow + snowball_recipe -> snowball

相反，人們也可以想像使用沒有消耗品的工具，例如

    spell_book + wand + fireball_recipe -> fireball

該系統足夠通用，也可以用於類似冒險的謎題（但是
人們需要更改指令並根據內容確定配方
正在合併）：

    stick + string + hook -> makeshift_fishing_rod
    makeshift_fishing_rod + storm_drain -> key

請參閱[劍範例](evennia.contrib.game_systems.crafting.example_recipes) 的範例
介紹如何設計用於從基本元素製作劍的配方樹。

(installation-and-usage)=
## 安裝與使用

從 evennia/contrib/crafting/crafting.py 匯入 `CmdCraft` 指令並
將其新增到您的角色cmdset。重新載入，`craft` 指令將是
可供您使用：

    craft <recipe> [from <ingredient>,...] [using <tool>, ...]

在程式碼中，您可以使用
`evennia.contrib.game_systems.crafting.craft` 功能：

```python
from evennia.contrib.game_systems.crafting import craft

result = craft(caller, "recipename", *inputs)

```
在這裡，`caller` 是進行製作的人，`*inputs` 是以下任何組合
消耗品和/或工具物件。系統將透過以下方式識別哪個是哪個
[Tags](../Components/Tags.md) 在它們上（見下文） `result` 始終是一個清單。

要使用手工藝，您需要食譜。新增一個新變數
`mygame/server/conf/settings.py`：

    CRAFT_RECIPE_MODULES = ['world.recipes']

這些模組中的所有頂級類別（其名稱不以`_`開頭）都將
被 Evennia 解析為配方以供製作系統使用。  使用
在上面的範例中，建立 `mygame/world/recipes.py` 並將您的食譜新增至
那裡：

一個簡單的範例（請繼續閱讀以瞭解更多詳細資訊）：

```python

from evennia.contrib.game_systems.crafting import CraftingRecipe, CraftingValidationError


class RecipeBread(CraftingRecipe):
  """
  Bread is good for making sandwitches!

  """

  name = "bread"   # used to identify this recipe in 'craft' command
  tool_tags = ["bowl", "oven"]
  consumable_tags = ["flour", "salt", "yeast", "water"]
  output_prototypes = [
    {"key": "Loaf of Bread",
     "aliases": ["bread"],
     "desc": "A nice load of bread.",
     "typeclass": "typeclasses.objects.Food",  # assuming this exists
     "tags": [("bread", "crafting_material")]  # this makes it usable in other recipes ...
    }

  ]

  def pre_craft(self, **kwargs):
    # validates inputs etc. Raise `CraftingValidationError` if fails

  def do_craft(self, **kwargs):
    # performs the craft - report errors directly to user and return None (if
    # failed) and the created object(s) if successful.

  def post_craft(self, result, **kwargs):
    # any post-crafting effects. Always called, even if do_craft failed (the
    # result would be None then)

```

(adding-new-recipes)=
## 新增食譜

*recipe* 是繼承自的類
`evennia.contrib.game_systems.crafting.CraftingRecipe`。這個類別實作了
最常見的製作形式 - 使用遊戲中的物件。每個食譜都是一個
單獨的類，使用您提供的消耗品/工具進行初始化。

為了讓 `craft` 指令找到您的自訂食譜，您需要告訴 Evennia
他們在哪裡。將新行新增至您的 `mygame/server/conf/settings.py` 檔案中，
包含帶有配方類別的任何新模組的清單。

```python
CRAFT_RECIPE_MODULES = ["world.myrecipes"]
```

（新增後需要重新載入）。這些中的所有全域性級別的課程
系統會考慮模組（其名稱不以下劃線開頭）
作為可行的食譜。

這裡我們假設您建立了 `mygame/world/myrecipes.py` 來匹配上面的內容
設定範例：

```python
# in mygame/world/myrecipes.py

from evennia.contrib.game_systems.crafting import CraftingRecipe

class WoodenPuppetRecipe(CraftingRecipe):
    """A puppet""""
    name = "wooden puppet"  # name to refer to this recipe as
    tool_tags = ["knife"]
    consumable_tags = ["wood"]
    output_prototypes = [
        {"key": "A carved wooden doll",
         "typeclass": "typeclasses.objects.decorations.Toys",
         "desc": "A small carved doll"}
    ]

```

這指定要在輸入中尋找哪個tags。它定義了一個
[原型](../Components/Prototypes.md) 用於產生的配方
動態結果（如果需要，一個配方可以產生多個結果）。
您也可以只提供一個，而不是指定完整的原型字典
您擁有的現有原型的 `prototype_key`s 清單。

重新載入伺服器後，該配方現在就可以使用了。嘗試一下
我們應該建立材料和工具來插入配方中。


此配方分析輸入，尋找 [Tags](../Components/Tags.md)
具體tag-類別。  可以使用以下指令為每個食譜設定所使用的 tag-類別
（分別為`.consumable_tag_category` 和`.tool_tag_category`）。預設值
是 `crafting_material` 和 `crafting_tool`。對於
對於木偶，我們需要一個帶有 `wood` tag 的物件，另一個帶有 `knife` 的物件
tag：

```python
from evennia import create_object

knife = create_object(key="Hobby knife", tags=[("knife", "crafting_tool")])
wood = create_object(key="Piece of wood", tags[("wood", "crafting_material")])
```

請注意，物件可以有任何名稱，重要的是
tag/tag-類別。這意味著如果「刺刀」也有「刀」製作tag，
它也可以用來雕刻木偶。這也可能很有趣
用於拼圖並允許使用者進行實驗並找到替代方案
知道成分。

順便說一下，還有一個簡單的快捷方式可以完成此操作：

```
tools, consumables = WoodenPuppetRecipe.seed()
```

`seed` 類別方法將建立滿足以下條件的簡單虛擬物件
菜譜的要求。這對於測試來說非常有用。

假設這些物品已放入我們的庫存中，我們現在可以使用
遊戲內指令：

```bash
> craft wooden puppet from wood using hobby knife
```
在程式碼中我們會這樣做

```python
from evennia.contrib.game_systems.crafting import craft
puppet = craft(crafter, "wooden puppet", knife, wood)

```
在對 `craft` 的呼叫中，`knife` 和 `wood` 的順序並不重要 -
食譜會根據他們的tags來分類。

(deeper-customization-of-recipes)=
## 更深入的客製化食譜

為了進一步定製食譜，它有助於瞭解如何使用
直接食譜類：

```python
class MyRecipe(CraftingRecipe):
    # ...

tools, consumables = MyRecipe.seed()
recipe = MyRecipe(crafter, *(tools + consumables))
result = recipe.craft()

```
這對於測試很有用，並且允許您直接使用該類，而無需
將其新增到 `settings.CRAFTING_RECIPE_MODULES` 中的模組中。

即使不修改類別屬性以外的內容，也有很多
在 `CraftingRecipe` 類上設定的選項。最簡單的就是參考
[CraftingRecipe API
檔案](evennia.contrib.game_systems.crafting.crafting.CraftingRecipe)。  例如，
您可以自訂驗證錯誤訊息，決定成分是否有
完全正確，如果失敗仍然會消耗成分，並且
更多。

為了獲得更多控制，您可以覆蓋您自己的類別中的鉤子：

- `pre_craft` - 這應該處理輸入驗證並將其資料儲存在 `.validated_consumables` 中
分別為`validated_tools`。出現錯誤時，這會將錯誤報告給工匠並引發
  `CraftingValidationError`。
- `craft` - 僅當 `pre_craft` 完成且無異常時才會呼叫此函式。這應該
透過生成原型來返回製作結果。或如果是手工製作則為空白列表
  由於某種原因失敗。如果需要，可以在此處新增技能檢定或隨機機會
  為您的遊戲。
- `post_craft` - 這接收來自 `craft` 的結果並處理錯誤訊息並刪除
任何需要的消耗品。它也可能在傳回結果之前修改結果。
- `msg` - 這是 `self.crafter.msg` 的包裝，應用於將訊息傳送到
工匠。集中化這意味著您以後也可以在一處輕鬆修改傳送樣式。

類別建構函式（和 `craft` 存取函式）採用可選的 `**kwargs`。這些都透過了
進入每個製作鉤。這些預設未使用，但可用於自訂每次呼叫的內容。

(skilled-crafters)=
### 熟練的工匠

製作系統沒有現成的「技能」系統 -
如果你的技術不夠熟練，你可能會失敗。究竟如何
技能工作取決於遊戲，因此要新增此內容，您需要製作自己的食譜
父類並讓你的食譜繼承它。


```python
from random import randint
from evennia.contrib.game_systems.crafting import CraftingRecipe

class SkillRecipe(CraftingRecipe):
   """A recipe that considers skill"""

    difficulty = 20

    def craft(self, **kwargs):
        """The input is ok. Determine if crafting succeeds"""

        # this is set at initialization
        crafter = self.crafte

        # let's assume the skill is stored directly on the crafter
        # - the skill is 0..100.
        crafting_skill = crafter.db.skill_crafting
        # roll for success:
        if randint(1, 100) <= (crafting_skill - self.difficulty):
            # all is good, craft away
            return super().craft()
        else:
            self.msg("You are not good enough to craft this. Better luck next time!")
            return []
```
在此範例中，我們為配方引入 `.difficulty` 並進行「擲骰子」來檢視
如果我們成功了。當然，我們會在完整的遊戲中使其更加身臨其境和更加細緻。在
原則上你可以按照你想要的方式自訂每個食譜，但你也可以繼承
像這樣的中央父母可以減少工作。

[劍配方範例模組](evennia.contrib.game_systems.crafting.example_recipes)也顯示了一個範例
在父母身上實施隨機技能檢查，然後繼承以供多種使用。

(even-more-customization)=
## 更多客製化

如果您想建立更自訂的東西（可能使用不同輸入型別的驗證邏輯）
您也可以檢視 `CraftingRecipe` 父類 `CraftingRecipeBase`。
它只實現了食譜所需的最低限度，對於大的改變，你最好開始
從此而不是更固執己見的`CraftingRecipe`。



----

<small>此檔案頁面是從`evennia\contrib\game_systems\crafting\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
