(npc-merchants)=
# NPC商戶

```
*** Welcome to ye Old Sword shop! ***
   Things for sale (choose 1-3 to inspect, quit to exit):
_________________________________________________________
1. A rusty sword (5 gold)
2. A sword with a leather handle (10 gold)
3. Excalibur (100 gold)
```

這將引入 NPC 能夠出售東西。實際上，這意味著當您與他們互動時，您會看到一個_選單_選擇。 Evennia 提供 [EvMenu](../Components/EvMenu.md) 實用程式來輕鬆建立遊戲內選單。

我們會將商家的所有商品存放在他們的庫存中。這意味著他們可能站在實際的商店房間、市場或漫步在路上。  我們還將使用“黃金”作為示例貨幣。  
要進入商店，你只需要站在同一個房間並使用`buy/shop`指令。

(making-the-merchant-class)=
## 打造商人階級

商家將在他們面前回應您發出 `shop` 或 `buy` 指令。

```python
# in for example mygame/typeclasses/merchants.py 

from typeclasses.objects import Object
from evennia import Command, CmdSet, EvMenu

class CmdOpenShop(Command): 
    """
    Open the shop! 

    Usage:
        shop/buy 

    """
    key = "shop"
    aliases = ["buy"]

    def func(self):
        # this will sit on the Merchant, which is self.obj. 
        # the self.caller is the player wanting to buy stuff.    
        self.obj.open_shop(self.caller)
        

class MerchantCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdOpenShop())


class NPCMerchant(Object):

     def at_object_creation(self):
         self.cmdset.add_default(MerchantCmdSet)

     def open_shop(self, shopper):
         menunodes = {}  # TODO! 
         shopname = self.db.shopname or "The shop"
         EvMenu(shopper, menunodes, startnode="shopfront", 
                shopname=shopname, shopkeeper=self, wares=self.contents)

```

我們也可以將指令放在單獨的模組中，但為了緊湊性，我們將其全部放在商家 typeclass 中。

請注意，我們將商家設為`Object`！由於我們沒有給他們任何其他指令，所以讓他們成為 `Character` 沒有意義。

我們製作一個非常簡單的 `shop`/`buy` 指令，並確保將其新增至商家自己的 cmdset 指令。

我們在 `shopper` 上初始化 `EvMenu`，但我們還沒有建立任何 `menunodes`，所以此時實際上不會做太多事情。重要的是，我們將 `shopname`、`shopkeeper` 和 `wares` 傳遞到選單中，這意味著它們將作為 EvMenu 例項上的屬性提供 - 我們將能夠從選單內部存取它們。

(coding-the-shopping-menu)=
## 編寫購物選單程式碼

[EvMenu](../Components/EvMenu.md) 將選單拆分為由 Python 函式表示的_節點_。每個節點代表選單中的一個站點，使用者必須在其中做出選擇。

為簡單起見，我們將在同一模組中的 `NPCMerchant` 類別上方編寫商店介面。

商店的起始節點名為「老劍店！」如果只有 3 件商品可供出售，將如下所示：

```
*** Welcome to ye Old Sword shop! ***
   Things for sale (choose 1-3 to inspect, quit to exit):
_________________________________________________________
1. A rusty sword (5 gold)
2. A sword with a leather handle (10 gold)
3. Excalibur (100 gold)
```


```python
# in mygame/typeclasses/merchants.py

# top of module, above NPCMerchant class.

def node_shopfront(caller, raw_string, **kwargs):
    "This is the top-menu screen."

    # made available since we passed them to EvMenu on start 
    menu = caller.ndb._evmenu
    shopname = menu.shopname
    shopkeeper = menu.shopkeeper 
    wares = menu.wares

    text = f"*** Welcome to {shopname}! ***\n"
    if wares:
        text += f"   Things for sale (choose 1-{len(wares)} to inspect); quit to exit:"
    else:
        text += "   There is nothing for sale; quit to exit."

    options = []
    for ware in wares:
        # add an option for every ware in store
        gold_val = ware.db.gold_value or 1
        options.append({"desc": f"{ware.key} ({gold_val} gold)",
                        "goto": ("inspect_and_buy", 
                                 {"selected_ware": ware})
                       })
                       
    return text, options
```

在節點內部，我們可以透過 `caller.ndb._evmenu` 存取呼叫方的選單。我們傳遞到 `EvMenu` 的額外關鍵字在此選單例項上可用。有了這個，我們就可以輕鬆呈現商店介面。每個選項都將成為該畫面上的編號選項。

請注意我們如何透過每個選項傳遞 `ware` 並將其標記為 `selected_ware`。這將可以在下一個節點的 `**kwargs` 引數中訪問

如果玩家選擇其中一件商品，他們應該能夠檢查它。如果他們在 Old Sword 商店中選擇了 `1`，情況應該是這樣的：

```
You inspect A rusty sword:

This is an old weapon maybe once used by soldiers in some
long forgotten army. It is rusty and in bad condition.
__________________________________________________________
1. Buy A rusty sword (5 gold)
2. Look for something else.
```

如果你買了就會看到

```
You pay 5 gold and purchase A rusty sword!
```
或者
```
You cannot afford 5 gold for A rusty sword!
```

無論哪種方式，您最終都應該再次回到購物選單的頂層，並可以繼續瀏覽或使用 `quit` 退出選單。

程式碼如下：

```python
# in mygame/typeclasses/merchants.py 

# right after the other node

def _buy_item(caller, raw_string, **kwargs):
    "Called if buyer chooses to buy"
    selected_ware = kwargs["selected_ware"]
    value = selected_ware.db.gold_value or 1
    wealth = caller.db.gold or 0

    if wealth >= value:
        rtext = f"You pay {value} gold and purchase {ware.key}!"
        caller.db.gold -= value
        move_to(caller, quiet=True, move_type="buy")
    else:
        rtext = f"You cannot afford {value} gold for {ware.key}!"
    caller.msg(rtext)
    # no matter what, we return to the top level of the shop
    return "shopfront"

def node_inspect_and_buy(caller, raw_string, **kwargs):
    "Sets up the buy menu screen."

    # passed from the option we chose 
    selected_ware = kwargs["selected_ware"]

    value = selected_ware.db.gold_value or 1
    text = f"You inspect {ware.key}:\n\n{ware.db.desc}"
    gold_val = ware.db.gold_value or 1

    options = ({
        "desc": f"Buy {ware.key} for {gold_val} gold",
        "goto": (_buy_item, kwargs)
    }, {
        "desc": "Look for something else",
        "goto": "shopfront",
    })
    return text, options
```

在這個節點中，我們從 `kwargs` 獲取 `selected_ware` - 這是我們從前一個節點上的選項傳遞過來的。我們顯示它的描述和值。如果使用者購買，我們將透過 `_buy_item` 輔助函式重新路由（這不是一個節點，它只是一個必須傳回要轉到的下一個節點的名稱的可呼叫函式。）。在`_buy_item`中，我們檢查買家是否可以購買該商品，如果可以，我們會將其移至他們的庫存中。無論哪種方式，此方法都會傳回 `shop_front` 作為下一個節點。

我們在這裡引用了兩個節點：`"shopfront"` 和 `"inspect_and_buy"` ，我們應該將它們對應到選單中的程式碼。向下捲動到同一模組中的 `NPCMerchant` 類，再次找到未完成的 `open_shop` 方法：


```python
# in /mygame/typeclasses/merchants.py

def node_shopfront(caller, raw_string, **kwargs):
    # ... 

def _buy_item(caller, raw_string, **kwargs):
    # ...

def node_inspect_and_buy(caller, raw_string, **kwargs):
    # ... 

class NPCMerchant(Object):

     # ...

     def open_shop(self, shopper):
         menunodes = {
             "shopfront": node_shopfront,
             "inspect_and_buy": node_inspect_and_buy
         }
         shopname = self.db.shopname or "The shop"
         EvMenu(shopper, menunodes, startnode="shopfront", 
                shopname=shopname, shopkeeper=self, wares=self.contents)

```


現在，我們將節點新增到其正確標籤下的 Evmenu 中。商家現在已經準備好了！


(the-shop-is-open-for-business)=
## 本店已開始營業！

確保`reload`。

讓我們透過在遊戲中建立商人和一些商品來嘗試。請記住，我們也必須創造一些黃金來推動經濟發展。

```
> set self/gold = 8

> create/drop Stan S. Stanman;stan:typeclasses.merchants.NPCMerchant
> set stan/shopname = Stan's previously owned vessles

> create/drop A proud vessel;ship 
> set ship/desc = The thing has holes in it.
> set ship/gold_value = 5

> create/drop A classic speedster;rowboat 
> set rowboat/gold_value = 2
> set rowboat/desc = It's not going anywhere fast.
```

請注意，無法存取 Python 程式碼的建構者現在只需使用遊戲內指令即可設定個人化商家。  商店設定完畢後，我們只需要在同一個房間就可以開始消費了！

```
> buy
*** Welcome to Stan's previously owned vessels! ***
   Things for sale (choose 1-3 to inspect, quit to exit):
_________________________________________________________
1. A proud vessel (5 gold)
2. A classic speedster (2 gold)

> 1 

You inspect A proud vessel:

The thing has holes in it.
__________________________________________________________
1. Buy A proud vessel (5 gold)
2. Look for something else.

> 1
You pay 5 gold and purchase A proud vessel!

*** Welcome to Stan's previously owned vessels! ***
   Things for sale (choose 1-3 to inspect, quit to exit):
_________________________________________________________
1. A classic speedster (2 gold)

```

