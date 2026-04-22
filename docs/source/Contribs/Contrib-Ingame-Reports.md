(in-game-reporting-system)=
# 遊戲內檢舉系統

Contrib，InspectorCaracal，2024 年

這個contrib提供了一個遊戲內報告系統，預設處理錯誤報告、玩家報告和想法提交。它還支援新增您自己的報告型別，或刪除任何預設報告型別。

每種型別的報告都有自己的提交新報告的指令，並且還提供了管理指令用於透過選單管理報告。

(installation)=
## 安裝

要安裝報告 contrib，只需將提供的 cmdset 新增至預設的 AccountCmdSet：

```python
# in commands/default_cmdset.py

from evennia.contrib.base_systems.ingame_reports import ReportsCmdSet

class AccountCmdSet(default_cmds.AccountCmdSet):
    # ...

    def at_cmdset_creation(self):
        # ...
        self.add(ReportsCmdSet)
```

contrib 還有兩個可選設定：`INGAME_REPORT_TYPES` 和 `INGAME_REPORT_STATUS_TAGS`。

「新增型別的報告」部分詳細介紹了 `INGAME_REPORT_TYPES` 設定。

「管理報告」部分介紹了 `INGAME_REPORT_STATUS_TAGS` 設定。

(usage)=
## 用法

預設情況下，以下報告型別可用：

* 錯誤：報告遊戲過程中遇到的錯誤。
* 想法：提交遊戲改進建議。
* 玩家：舉報玩家的不當行為。

玩家可以透過每種報告型別的指令提交新報告，工作人員可以存取報告管理指令和選單。

(submitting-reports)=
### 提交報告

玩家可以使用以下指令提交報告：

* `bug <text>` - 提交錯誤報告。可以包含一個可選目標 - `bug <target> = <text>` - 使開發人員/建置人員更容易追蹤問題。
* `report <player> = <text>` - 舉報玩家的不當或違反規則的行為。 *需要*提供一個目標 - 預設它會在帳戶中搜尋。
* `idea <text>` - 提交一般性建議，沒有目標。它還有一個別名 `ideas`，讓您可以檢視所有提交的想法。

(managing-reports)=
### 管理報告

`manage reports` 指令允許工作人員透過啟動管理選單來檢視和管理各種型別的報告。

此指令將根據可用報告的型別動態為其自身新增別名，每個指令字串都會啟動該特定報告型別的選單。別名基於模式 `manage <report type>s` 建置 - 預設情況下，這意味著它使 `manage bugs`、`manage players` 和 `manage ideas` 與預設的 `manage reports` 和 e.g 一起可用。 `manage bugs` 將啟動 `bug` 型別報告的管理選單。

除了閱讀現有報告之外，該選單還允許您更改任何給定報告的狀態。預設情況下，contrib 包括兩個不同的狀態tags：`in progress` 和`closed`。

> 注意：建立的報告沒有狀態tags，被視為“開啟”

如果您希望報告有一組不同的狀態，您可以將 `INGAME_REPORT_STATUS_TAGS` 定義為狀態清單。

**例子**

```python
# in server/conf/settings.py

# this will allow for the statuses of 'in progress', 'rejected', and 'completed', without the contrib-default of 'closed'
INGAME_REPORT_STATUS_TAGS = ('in progress', 'rejected', 'completed')
```

(adding-new-types-of-reports)=
### 新增型別的報告

contrib 旨在使向系統新增新型別的報告盡可能簡單，只需兩個步驟：

1. 更新您的設定檔以包含 `INGAME_REPORT_TYPES` 設定。
2. 建立新的 `ReportCmd` 並將其新增至您的指令集中。

(update-your-settings)=
#### 更新您的設定

contrib 可以選擇引用 `settings.py` 中的 `INGAME_REPORT_TYPES` 以檢視可以管理哪些型別的報告。如果您想要變更可用的報表型別，則需要定義此設定。

```python
# in server/conf/settings.py

# this will include the contrib's report types as well as a custom 'complaint' report type
INGAME_REPORT_TYPES = ('bugs', 'ideas', 'players', 'complaints')
```

您還可以使用此設定刪除 contrib 的任何報告型別 - contrib 在構建其 cmdset 時將遵循此設定，無需其他步驟。

```python
# in server/conf/settings.py

# this redefines the setting to not include 'ideas', so the ideas command and reports won't be available
INGAME_REPORT_TYPES = ('bugs', 'players')
```

(create-a-new-reportcmd)=
#### 創造一個新的ReportCmd

`ReportCmdBase` 是一個父指令類，主要功能是提交報告。建立新的報告指令就像從此類繼承並定義幾個類別屬性一樣簡單。

* `key` - 這與任何其他指令相同，設定指令的可用鍵。如果未明確設定，它也充當報告型別。
* `report_type` - 此指令所針對的報告型別（e.g。`player`）。只有當您想要與金鑰不同的字串時才需要設定它。
* `report_locks` - 您想要套用於建立的報表的鎖定。預設為`"read:pperm(Admin)"`
* `success_msg` - 提交此類報告後傳送給玩家的字串。預設為`"Your report has been filed."`
* `require_target`：如果您的報告型別需要目標（e.g。玩家報告），則設定為 `True`。

> 注意：contrib 自己的指令 - `CmdBug`、`CmdIdea` 和 `CmdReport` - 的實現方式相同，因此您可以將它們作為示例進行檢視。

例子：

```python
from evennia.contrib.base_systems.ingame_reports.reports import ReportCmdBase

class CmdCustomReport(ReportCmdBase):
    """
    file a custom report

    Usage:
        customreport <message>

    This is a custom report type.
    """

    key = "customreport"
    report_type = "custom"
    success_message = "You have successfully filed a custom report."
```

將此新指令新增至預設cmdset 以啟用歸檔新報告型別。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\ingame_reports\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
