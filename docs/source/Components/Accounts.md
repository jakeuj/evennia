(accounts)=
# 帳戶

```
┌──────┐ │   ┌───────┐    ┌───────┐   ┌──────┐
│Client├─┼──►│Session├───►│Account├──►│Object│  
└──────┘ │   └───────┘    └───────┘   └──────┘
                              ^
```

_Account_ 代表一個唯一的遊戲帳號 - 一個玩家在玩遊戲。儘管一名玩家可能會從多個用戶端/Sessions 連線到遊戲，但他們通常只有一個帳戶。

帳號物件沒有遊戲內的表示。為了真正進入遊戲，帳戶必須「操縱」一個[物件](./Objects.md)（通常是[角色](./Objects.md#characters)）。

到底有多少 Sessions 可以同時與帳號及其傀儡互動取決於
Evennia的[MULTISESSION_MODE](../Concepts/Connection-Styles.md#multisession-mode-and-multiplaying)

除了儲存登入資訊和其他特定帳戶的資料之外，帳戶物件是在 Evennia 的預設 [頻道](./Channels.md) 上聊天的物件。  它也是儲存[許可權](./Locks.md)的好地方，以便在不同的遊戲角色之間保持一致。它還可以儲存玩家級別的設定選項。

帳戶物件有自己的預設值 [CmdSet](./Command-Sets.md)，`AccountCmdSet`。無論玩家扮演哪個角色，都可以使用該集的指令。最值得注意的是，預設遊戲的 `exit`、`who` 和聊天頻道指令位於帳戶 cmdset 中。

    > ooc 

預設的 `ooc` 指令會導致您離開當前的人偶並進入 OOC 模式。在此模式下，您沒有位置，只有 Account-cmdset 可用。它充當切換角色的暫存區域（如果您的遊戲支援），以及如果您的角色被意外刪除時的安全性回退。

    > ic 

這重新傀儡了最新的角色。

請注意，帳戶物件可以（並且通常確實）擁有與其控制的角色不同的一組[許可權](./Permissions.md)。  通常，您應該將許可權置於帳戶層級 - 這將推翻角色層級上設定的許可權。為了使角色的許可權發揮作用，可以使用預設的`quell`指令。這允許使用不同的許可權集探索遊戲（但您不能以這種方式升級許可權 - 對於 `Builder`、`Admin` 等分層許可權，將始終使用角色/帳戶上的*較低*許可權）。


(working-with-accounts)=
## 使用帳戶

對於所有新帳戶，您通常不需要多個帳戶 typeclass。

根據定義，Evennia 帳戶是一個在其父類別中包含 `evennia.DefaultAccount` 的 Python 類別。在`mygame/typeclasses/accounts.py`中有一個空類別可供您修改。 Evennia 預設使用這個（它直接繼承自 `DefaultAccount`）。

以下是在程式碼中修改預設 Account 類別的範例：

```python
    # in mygame/typeclasses/accounts.py

    from evennia import DefaultAccount

    class Account(DefaultAccount): 
        # [...]
    	def at_account_creation(self): 
        	"this is called only once, when account is first created"
    	    self.db.real_name = None      # this is set later 
    	    self.db.real_address = None   #       "
    	    self.db.config_1 = True       # default config 
    	    self.db.config_2 = False      #       "
    	    self.db.config_3 = 1          #       "
    
    	    # ... whatever else our game needs to know 
``` 

使用`reload`重新載入伺服器。

……但是，如果您使用`examine *self`（星號讓您檢查您的帳戶物件而不是您的角色），您將看不到新屬性。這是因為 `at_account_creation` 僅在「第一次」呼叫該帳戶並且您的帳戶物件已經存在時才被呼叫（但任何連線的新帳戶都會看到它們）。要更新自己，您需要確保重新觸發您已建立的所有帳戶的掛鉤。以下是如何使用 `py` 執行此操作的範例：

``` py [account.at_account_creation() for account in evennia.managers.accounts.all()] ```

You should now see the Attributes on yourself.

> If you wanted Evennia to default to a completely *different* Account class located elsewhere, you > must point Evennia to it. Add `BASE_ACCOUNT_TYPECLASS` to your settings file, and give the python path to your custom class as its value. By default this points to `typeclasses.accounts.Account`, the empty template we used above.


### Properties on Accounts

Beyond those properties assigned to all typeclassed objects (see [Typeclasses](./Typeclasses.md)), the Account also has the following custom properties:

- `user` - a unique link to a `User` Django object, representing the logged-in user.
- `obj` - an alias for `character`.
- `name` - an alias for `user.username`
- `sessions` - an instance of [ObjectSessionHandler](github:evennia.objects.objects#objectsessionhandler) managing all connected Sessions (physical connections) this object listens to (Note: In older versions of Evennia, this was a list). The so-called `session-id` (used in many places) is found as a property `sessid` on each Session instance.
- `is_superuser` (bool: True/False) - if this account is a superuser.

Special handlers:
- `cmdset` - This holds all the current [Commands](./Commands.md) of this Account. By default these are
  the commands found in the cmdset defined by `settings.CMDSET_ACCOUNT`.
- `nicks` - This stores and handles [Nicks](./Nicks.md), in the same way as nicks it works on Objects. For Accounts, nicks are primarily used to store custom aliases for [Channels](./Channels.md).

Selection of special methods (see `evennia.DefaultAccount` for details):
- `get_puppet` - get a currently puppeted object connected to the Account and a given session id, if any.
- `puppet_object` - connect a session to a puppetable Object.
- `unpuppet_object` - disconnect a session from a puppetable Object.
- `msg` - send text to the Account
- `execute_cmd` - runs a command as if this Account did it.
- `search` - search for Accounts.