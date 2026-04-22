(legacy-comms-commands)=
# 舊版通訊指令

Gratch 2021 的貢獻

在 Evennia 1.0+ 中，舊的 Channel 指令（最初受 MUX 啟發）是
替換為執行所有這些功能的單一 `channel` 指令。
這個contrib（摘自Evennia 0.9.5）將功能分解為
MU* 使用者更熟悉的單獨指令。這只是為了展示，
main `channel` 指令仍然在後臺呼叫。

| Contrib 文法 | 預設 `channel` 語法                                  |
| -------------- | --------------------------------------------------------- |
| `allcom`       |  `channel/all` 和 `channel`                              |
| `addcom`       | `channel/alias`、`channel/sub` 和 `channel/unmute`       |
| `delcom`       | `channel/unalias`、`alias/unsub` 和 `channel/mute`       |
| `cboot`        | `channel/boot`（不支援`channel/ban`和`/unban`） |
| `cwho`         | `channel/who`                                             |
| `ccreate`      | `channel/create`                                          |
| `cdestroy`     | `channel/destroy`                                         |
| `clock`        | `channel/lock`                                            |
| `cdesc`        | `channel/desc`                                            |

(installation)=
## 安裝

- 將 `CmdSetLegacyComms` cmdset 從此模組匯入到 `mygame/commands/default_cmdsets.py`
- 將其新增到 CharacterCmdSet 的 `at_cmdset_creation` 方法中（見下文）。
- 重新載入伺服器。

```python
# in mygame/commands/default_cmdsets.py

# ..
from evennia.contrib.base_systems.mux_comms_cmds import CmdSetLegacyComms   # <----

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(CmdSetLegacyComms)   # <----

```

請注意，您仍然可以使用 `channel` 指令；這實際上是
這些指令仍然在幕後使用。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\mux_comms_cmds\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
