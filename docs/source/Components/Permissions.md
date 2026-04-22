(permissions)=
# 許可權

*許可權* 只是儲存在 `Objects` 和 `Accounts` 上的處理程式 `permissions` 中的文字字串。將其視為一種特殊的 [Tag](./Tags.md) - 專門用於訪問檢查。因此它們經常與[鎖](./Locks.md)緊密耦合。許可權字串不區分大小寫，因此“Builder”與“builder”等相同。

許可權被用作建構存取層級和層次結構的便捷方法。它由 `perm` 指令設定，並由 `PermissionHandler.check` 方法以及特殊的 `perm()` 和 `pperm()` [lock 函式](./Locks.md) 檢查。

所有新帳戶都會獲得一組由 `settings.PERMISSION_ACCOUNT_DEFAULT` 定義的預設許可權。

(the-super-user)=
## 超級使用者

嚴格來說Evennia中有兩種型別的使用者，*超級使用者*和其他人。的
超級使用者是您建立的第一個使用者，物件`#1`。這是全能的伺服器擁有者帳戶。
從技術上講，超級使用者不僅可以存取所有內容，還可以「繞過」許可權檢查
完全。

這使得超級使用者不可能lock出局，但卻不適合實際玩-
測試遊戲的鎖定和限制（請參閱下面的`quell`）。通常不需要有
但有一個超級使用者。

(working-with-permissions)=
## 使用許可權

在遊戲中，您可以使用`perm`指令新增和刪除許可權

     > perm/account Tommy = Builders
     > perm/account/del Tommy = Builders

請注意 `/account` 開關的使用。這意味著您將許可權分配給[帳戶](./Accounts.md) Tommy，而不是任何恰好名為「Tommy」的[角色](./Objects.md)。如果您不想使用 `/account`，您也可以在名稱前加上 `*` 字首以指示正在尋找帳戶：

    > perm *Tommy = Builders
    
在物件上放置許可權可能有原因（尤其是 NPCS），但為了向玩家授予權力，您通常應該在 `Account` 上放置許可權 - 這保證了它們被保留，*無論*他們目前正在操縱哪個角色。

從「層次結構樹」（見下文）分配許可權時，記住這一點尤其重要，因為帳戶的許可權將推翻其角色的許可權。因此，為了避免混淆，您通常應該將層次結構許可權放在帳戶上，而不是放在他們的角色/人偶上。

如果您_確實_想要開始使用_puppet_上的許可權，請使用 `quell`

    > quell 
    > unquell   

這會下降到傀儡物件的許可權，然後再次返回您的帳戶許可權。如果你想「像」別人一樣嘗試某件事，壓制是有用的。它對於超級使用者也很有用，因為這使他們容易受到鎖定的影響（因此他們可以測試事物）。

在程式碼中，您可以透過 `PermissionHandler` 新增/刪除許可權，該許可權位於所有許可權上
將實體型別分類為屬性 `.permissions`：

```python
    account.permissions.add("Builders")
    account.permissions.add("cool_guy")
    obj.permissions.add("Blacksmith")
    obj.permissions.remove("Blacksmith")
```

(the-permission-hierarchy)=
### 許可權層次結構

可以透過編輯元組將選定的許可權字串組織在*許可權層次結構*中
`settings.PERMISSION_HIERARCHY`。  Evennia的預設許可權層次如下
（依功率遞增順序）：

     Guest            # temporary account, only used if GUEST_ENABLED=True (lowest)
     Player           # can chat and send tells (default level)
     Helper           # can edit help files
     Builder          # can edit the world
     Admin            # can administrate accounts
     Developer        # like superuser but affected by locks (highest)

（除了不區分大小寫之外，分層許可權還瞭解複數形式，因此您可以互換使用 `Developers` 和 `Developer`）。

檢查分層許可權時（使用遵循的方法之一），您將透過您的等級*及以下*的檢查。也就是說，如果您擁有「Admin」分層許可權，您還將透過要求「Builder」、「Helper」等的檢查。

相比之下，如果您檢查非分層許可權，例如“鐵匠”，您必須“完全”擁有該許可權才能透過。

(checking-permissions)=
### 檢查許可權

需要注意的是，當您檢查*傀儡* [物件](./Objects.md)（如角色）的許可權時，檢查將始終首先使用連線到該物件的任何 `Account` 的許可權，然後再檢查該物件的許可權。在分層許可權（管理員、建構者等）的情況下，將始終使用帳戶許可權（這會阻止帳戶透過傀儡高階角色來升級其許可權）。如果要尋找的許可權不在層次結構中，則需要精確匹配，首先在帳戶上，如果在那裡找不到（或者如果沒有連線帳戶），則在物件本身上進行精確匹配。

(checking-with-objpermissionscheck)=
### 用 obj.permissions.check() 檢查

檢查實體是否具有許可權的最簡單方法是檢查其 _PermissionHandler_，在所有型別分類實體上儲存為 `.permissions`。

    if obj.permissions.check("Builder"):
        # allow builder to do stuff

    if obj.permissions.check("Blacksmith", "Warrior"):
        # do stuff for blacksmiths OR warriors

    if obj.permissions.check("Blacksmith", "Warrior", require_all=True):
        # only for those that are both blacksmiths AND warriors

使用 `.check` 方法是可行的方法，它將採取分層
許可權進入帳戶，檢查帳戶/sessions等。

```{warning}

    Don't confuse `.permissions.check()` with `.permissions.has()`. The .has()
    method checks if a string is defined specifically on that PermissionHandler.
    It will not consider permission-hierarchy, puppeting etc. `.has` can be useful
    if you are manipulating permissions, but use `.check` for access checking.

```

(lock-funcs)=
### Lock 函式

雖然 `PermissionHandler` 提供了一種檢查許可權的簡單方法，[Lock
strings](./Locks.md) 提供了一種迷你語言來描述如何存取某些內容。
`perm()` _lock 函式_ 是使用鎖定中許可權的主要工具。

假設我們有一個 `red_key` 物件。我們也有想要的紅色寶箱
用這把鑰匙解鎖。

    perm red_key = unlocks_red_chests

這為 `red_key` 物件授予了許可權「unlocks_red_chests」。接下來我們
lock我們的紅色寶箱：

    lock red chest = unlock:perm(unlocks_red_chests)

當嘗試用這把鑰匙解鎖紅色寶箱時，寶箱Typeclass可能會
然後拿走鑰匙並進行訪問檢查：

```python
# in some typeclass file where chest is defined

class TreasureChest(Object):

  # ...

  def open_chest(self, who, tried_key):

      if not chest.access(who, tried_key, "unlock"):
          who.msg("The key does not fit!")
          return
      else:
          who.msg("The key fits! The chest opens.")
          # ...

```

預設 `perm` lockfunc 有多種變體：

- `perm_above` - 需要比一級許可權「更高」的層級許可權
假如。例：`"edit: perm_above(Player)"`
- `pperm` - *只*查詢 `Accounts` 上的許可權，從不尋找任何傀儡
物件（無論是否分層燙髮）。
- `pperm_above` - 類似於 `perm_above`，但僅適用於帳戶。

(some-examples)=
### 一些例子

新增許可權並檢查鎖

```python
    account.permissions.add("Builder")
    account.permissions.add("cool_guy")
    account.locks.add("enter:perm_above(Player) and perm(cool_guy)")
    account.access(obj1, "enter") # this returns True!
```

具有連線帳戶的木偶範例：

```python
    account.permissions.add("Player")
    puppet.permissions.add("Builders")
    puppet.permissions.add("cool_guy")
    obj2.locks.add("enter:perm_above(Accounts) and perm(cool_guy)")

    obj2.access(puppet, "enter") # this returns False, since puppet permission
                                 # is lower than Account's perm, and perm takes
                                 # precedence.
```


(quelling)=
## 鎮壓

`quell` 指令可用於強制忽略 `perm()` lockfunc
帳戶上的許可權，而是使用角色上的許可權
僅。這個可以用e.g。由工作人員以較低許可權測試事物
水平。使用`unquell`返回正常操作。  請注意，平息將
使用帳戶或角色的任何分層許可權中最小的一個，因此
無法透過平息到高許可權來升級自己的帳戶許可權
性格。超級使用者也可以透過這種方式取消他們的權力，使他們
受鎖影響。
