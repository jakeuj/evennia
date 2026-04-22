(clothing)=
# 衣服

蒂姆·阿什利·詹金斯 (Tim Ashley Jenkins) 貢獻，2017 年

提供 typeclass 和可穿戴服裝的指令。這些
這些衣服的外觀會附加到角色穿著時的描述中。

服裝物品在穿著時會新增到角色的描述中
在一個清單中。例如，如果穿著以下服裝：

    a thin and delicate necklace
    a pair of regular ol' shoes
    one nice hat
    a very pretty dress

會產生這樣的附加描述：

    Tim is wearing one nice hat, a thin and delicate necklace,
    a very pretty dress and a pair of regular ol' shoes.

(installation)=
## 安裝

若要安裝，請匯入此模組並使用預設字元
從遊戲的 `characters.py` 檔案中的 ClothedCharacter 繼承：

```python

from evennia.contrib.game_systems.clothing import ClothedCharacter

class Character(ClothedCharacter):

```

然後在你的字元集中新增`ClothedCharacterCmdSet`
`mygame/commands/default_cmdsets.py`：

```python

from evennia.contrib.game_systems.clothing import ClothedCharacterCmdSet # <--

class CharacterCmdSet(default_cmds.CharacterCmdSet):
     # ...
     at_cmdset_creation(self):

         super().at_cmdset_creation()
         # ...
         self.add(ClothedCharacterCmdSet)    # <--

```

(usage)=
## 用法

安裝後，您可以使用預設的建構器指令來建立衣服
用於測試系統：

    create a pretty shirt : evennia.contrib.game_systems.clothing.ContribClothing
    set shirt/clothing_type = 'top'
    wear shirt

角色的描述可能如下所示：

    Superuser(#1)
    This is User #1.

    Superuser is wearing one nice hat, a thin and delicate necklace,
    a very pretty dress and a pair of regular ol' shoes.

角色也可以指定其服裝的穿著風格 - I.E.
戴一條圍巾“在脖子上打一個緊結”或“披在身上”
寬鬆地跨在肩上——增加了一種簡單的客製化方式。
例如，輸入後：

    wear scarf draped loosely across the shoulders

這件衣服在描述中是這樣的：

    Superuser(#1)
    This is User #1.

    Superuser is wearing a fanciful-looking scarf draped loosely
    across the shoulders.

衣服可以用來遮蓋其他物品，而且有很多選擇
提供定義您自己的服裝型別及其限制和
行為。例如，自動覆蓋內衣
透過外套，或對每種型別的物品數量進行限制
可以穿的。系統本身是相當自由的 - 你
例如，可以用幾乎任何其他衣服覆蓋任何衣服 - 但它
可以很容易地變得更加嚴格，甚至可以繫結到
裝甲或其他裝置的系統。

(configuration)=
## 設定

contrib 有幾個可選設定，您可以在 `settings.py` 中定義它們
以下是設定及其預設值。

```python
# Maximum character length of 'wear style' strings, or None for unlimited.
CLOTHING_WEARSTYLE_MAXLENGTH = 50

# The order in which clothing types appear on the description.
# Untyped clothing or clothing with a type not in this list goes last.
CLOTHING_TYPE_ORDERED = [
        "hat",
        "jewelry",
        "top",
        "undershirt",
        "gloves",
        "fullbody",
        "bottom",
        "underpants",
        "socks",
        "shoes",
        "accessory",
    ]

# The maximum number of clothing items that can be worn, or None for unlimited.
CLOTHING_OVERALL_LIMIT = 20

# The maximum number for specific clothing types that can be worn.
# If the clothing item has no type or is not specified here, the only maximum is the overall limit.
CLOTHING_TYPE_LIMIT = {"hat": 1, "gloves": 1, "socks": 1, "shoes": 1}

# What types of clothes will automatically cover what other types of clothes when worn.
# Note that clothing only gets auto-covered if it's already being worn. It's perfectly possible
# to have your underpants showing if you put them on after your pants!
CLOTHING_TYPE_AUTOCOVER = {
        "top": ["undershirt"],
        "bottom": ["underpants"],
        "fullbody": ["undershirt", "underpants"],
        "shoes": ["socks"],
    }

# Any types of clothes that can't be used to cover other clothes at all.
CLOTHING_TYPE_CANT_COVER_WITH = ["jewelry"]
```


----

<small>此檔案頁面是從`evennia\contrib\game_systems\clothing\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
