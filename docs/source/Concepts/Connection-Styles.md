(character-connection-styles)=
# 字元連線樣式

```shell
> login Foobar password123
```

Evennia支援多種方式供玩家連結遊戲。這允許 Evennia 模仿各種其他伺服器的行為，或為自訂解決方案開放事物。

(changing-the-login-screen)=
## 更改登入畫面

這是透過修改 `mygame/server/conf/connection_screens.py` 並重新載入來完成的。如果您不喜歡預設登入，可以檢視兩個 contribs 作為靈感。

- [電子郵件登入](../Contribs/Contrib-Email-Login.md) - 安裝時需要電子郵件，使用電子郵件登入。
- [選單登入](../Contribs/Contrib-Menu-Login.md) - 使用多個提示登入，要求依序輸入使用者名稱和密碼。

(customizing-the-login-command)=
## 自訂登入指令

當玩家連線到遊戲時，它會執行`CMD_LOGINSTART` [系統指令](../Components/Commands.md#system-commands)。預設情況下，這是 [CmdUnconnectedLook](evennia.commands.default.unloggedin.CmdUnconnectedLook)。這將顯示歡迎畫面。 [UnloggedinCmdSet](evennia.commands.default.cmdset_unloggedin.UnloggedinCmdSet) 中的其他指令定義了登入體驗。因此，如果您想自訂它，您只需替換/刪除這些指令即可。

```{sidebar}
如果您讓指令繼承自 `default_cmds.UnConnectedLook`，您甚至不必指定金鑰（因為您的類別將繼承它）！
```
```python
# in mygame/commands/mylogin_commands.py

from evennia import syscmdkeys, default_cmds, Command


class MyUnloggedinLook(Command):

    # this will now be the first command called when connecting
    key = syscmdkeys.CMD_LOGINSTART 

    def func(self):
        # ... 
```
 
接下來，將其新增到 `UnloggedinCmdSet` 中的正確位置：

```python
# in mygame/commands/default_cmdsets.py

from commands.mylogin_commands import MyUnloggedinLook
# ... 

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    # ... 
    def at_cmdset_creation(self):
        super().at_cmdset_creation
        self.add(MyUnloggedinLook())
```

`reload` 並且將使用您的備用指令。檢查預設指令，您將能夠更改有關登入的所有內容。

(multisession-mode-and-multi-playing)=
## 多會話模式和多人遊戲

可以同時連線到給定帳戶的 sessions 數量及其工作方式由 `MULTISESSION_MODE` 設定給出：

* `MULTISESSION_MODE=0`：每個帳戶 1session。當與新的 session 連線時，舊的將斷開連線。這是預設模式，模擬許多經典的 mud 程式碼庫。
    ```
    ┌──────┐ │   ┌───────┐    ┌───────┐   ┌─────────┐
    │Client├─┼──►│Session├───►│Account├──►│Character│
    └──────┘ │   └───────┘    └───────┘   └─────────┘
    ```
* `MULTISESSION_MODE=1`：每個帳戶有許多sessions，來自/到每個session的輸入/輸出被視為相同。對於玩家來說，這意味著他們可以從多個用戶端連線到遊戲，並在所有用戶端中看到相同的輸出。在一個用戶端中給出的指令的結果（即，透過一個Session）將無差別地返回到*所有*連線的Sessions/用戶端。
    ```
             │
    ┌──────┐ │   ┌───────┐
    │Client├─┼──►│Session├──┐
    └──────┘ │   └───────┘  └──►┌───────┐   ┌─────────┐
             │                  │Account├──►│Character│
    ┌──────┐ │   ┌───────┐  ┌──►└───────┘   └─────────┘
    │Client├─┼──►│Session├──┘
    └──────┘ │   └───────┘
             │
    ```

* `MULTISESSION_MODE=2`：每個帳戶許多sessions，每個session一個字元。在此模式下，傀儡物件/角色將僅將傀儡連結回執行傀儡操作的特定 Session。也就是說，來自 Session 的輸入將利用該物件/字元的 CmdSet，並且傳出訊息（例如 `look` 的結果）將僅傳遞回該傀儡 Session。如果另一個 Session 嘗試操縱同一個角色，舊的 Session 將自動取消操縱它。從玩家的角度來看，這意味著他們可以使用一個遊戲帳戶開啟單獨的遊戲使用者端並在每個用戶端中扮演不同的角色。
    ```
             │                 ┌───────┐
    ┌──────┐ │   ┌───────┐     │Account│    ┌─────────┐
    │Client├─┼──►│Session├──┐  │       │  ┌►│Character│
    └──────┘ │   └───────┘  └──┼───────┼──┘ └─────────┘
             │                 │       │
    ┌──────┐ │   ┌───────┐  ┌──┼───────┼──┐ ┌─────────┐
    │Client├─┼──►│Session├──┘  │       │  └►│Character│
    └──────┘ │   └───────┘     │       │    └─────────┘
             │                 └───────┘
    ```
* `MULTISESSION_MODE=3`：每個帳戶*和*字元有許多sessions。這是完整的多重傀儡模式，其中多個sessions不僅可以連線到玩家帳戶，而且多個sessions也可以同時傀儡單一角色。從使用者的角度來看，這意味著可以開啟多個用戶端視窗，有些用於控制不同的角色，有些則像模式 1 一樣共享角色的輸入/輸出。此模式在其他方面與模式 2 相同。
    ```
             │                 ┌───────┐
    ┌──────┐ │   ┌───────┐     │Account│    ┌─────────┐
    │Client├─┼──►│Session├──┐  │       │  ┌►│Character│
    └──────┘ │   └───────┘  └──┼───────┼──┘ └─────────┘
             │                 │       │
    ┌──────┐ │   ┌───────┐  ┌──┼───────┼──┐
    │Client├─┼──►│Session├──┘  │       │  └►┌─────────┐
    └──────┘ │   └───────┘     │       │    │Character│
             │                 │       │  ┌►└─────────┘
    ┌──────┐ │   ┌───────┐  ┌──┼───────┼──┘             ▼
    │Client├─┼──►│Session├──┘  │       │
    └──────┘ │   └───────┘     └───────┘
             │
    ```

> 請注意，即使多個 Sessions 操縱一個角色，該角色也只有一個例項。

模式 `0` 是預設值，模仿了許多遺留程式碼庫的工作方式，尤其是在 DIKU 世界中。更高模式的等價物通常被「駭客」到現有伺服器中，以允許玩家擁有多個角色。

    MAX_NR_SIMULTANEOUS_PUPPETS = 1

此設定限制您的_帳號_可以_同時_操縱的_不同_傀儡數量。這用於限制真正的多人遊戲。大於 1 的值沒有任何意義，除非 `MULTISESSION_MODE` 也設定為 `>1`。  設定為 `None` 無限制。

(character-creation-and-auto-puppeting)=
## 角色建立和自動傀儡

當玩家第一次建立帳戶時，Evennia會自動建立一個同名的`Character`傀儡。當玩家登入時，他們會自動傀儡這個角色。此預設設定向玩家隱藏了帳戶與角色的分離，並將他們立即放入遊戲中。此預設行為與許多舊版 MU 伺服器中的工作方式類似。

要控制此行為，您需要調整設定。這些是預設值：

    AUTO_CREATE_CHARACTER_WITH_ACCOUNT = True
    AUTO_PUPPET_ON_LOGIN = True 
    MAX_NR_CHARACTERS = 1
    
有一個預設的 `charcreate` 指令。這要注意`MAX_NR_CHARACTERS`；如果您建立自己的角色建立指令，您也應該這樣做。它至少需要`1`。設定為 `None` 無限制。有關如何製作更高階的角色生成系統的想法，請參閱[初學者教學](../Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.md)。

```{sidebar}
將這些設定與 `MAX_NR_SIMULTANEOUS_PUPPETS` 結合可以允許玩家（例如）建立一個「穩定」的角色，但一次只能玩一個角色。
```
如果您選擇不自動建立角色，則需要提供角色生成，並且不會有（初始）角色可供傀儡。在這兩種設定中，登入後您最初都會處於 `ooc` 模式。這是放置角色生成畫面/選單的好地方（您可以e.g。替換[CmdOOCLook](evennia.commands.default.account.CmdOOCLook)以觸發除正常ooc-look之外的其他內容）。

建立角色後，如果設定了自動傀儡，則每次登入時都會自動傀儡最新的傀儡角色。如果未設定，您將始終啟動OOC（並且應該能夠選擇要操縱的角色）。

