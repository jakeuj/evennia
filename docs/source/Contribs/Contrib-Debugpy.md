(debugpy-vscode-debugger-integration)=
# DebugPy VSCode 偵錯程式整合

Electroglyph 的貢獻，2025 年

這會註冊一個遊戲內指令 `debugpy`，該指令啟動 debugpy 偵錯器並偵聽連線埠 5678。
目前，這僅適用於 Visual Studio Code (VS Code)。

如果您是 JetBrains PyCharm 使用者並且想要使用此功能，請在以下位置發出聲音：
https://youtrack.jetbrains.com/issue/PY-63403/Support-debugpy


這要歸功於 Evennia Discord 取得幫助頻道上的 Moony，謝謝 Moony！


(installation)=
## 安裝

這需要 VS 程式碼和 debugpy，因此請確保您使用的是 VS 程式碼。

從安裝 Evennia 的 venv 執行：

`pip install debugpy`

(enable-the-command-in-evennia)=
### 啟用Evennia中的指令

在您的 Evennia mygame 資料夾中，開啟 `/commands/default_cmdsets.py`

在頂部附近的某個位置新增`from evennia.contrib.utils.debugpy import CmdDebugPy`。

在 `CharacterCmdSet.at_cmdset_creation` 的 `super().at_cmdset_creation()` 下加入以下內容：

`self.add(CmdDebugPy)`


(add-remote-attach-option-to-vs-code-debugger)=
### 將“遠端連線”選項新增至VS程式碼偵錯器

啟動VS程式碼並開啟你的launch.json，如下所示：

![截圖](./vscode.png)

將其新增至您的設定：

```json
        {
            "name": "Python Debugger: Remote Attach",
            "justMyCode": false,
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "127.0.0.1",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "${workspaceFolder}"
                }
            ]
        },
```

如果您從要偵錯的同一臺電腦上執行 Evennia，請使用 `127.0.0.1` 作為主機。  否則，如果您想除錯遠端伺服器，請根據需要更改主機（可能還有遠端根對映）。

之後它應該看起來像這樣：

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
        },
        {
            "name": "Python Debugger: Remote Attach",
            "justMyCode": false,
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "127.0.0.1",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "${workspaceFolder}"
                }
            ]
        },
    ]
}
```

（注意大括號之間的逗號）

(usage)=
## 用法

在 VS 程式碼中您希望偵錯器停止的位置設定斷點。

在Evennia中執行`debugpy`指令。

您應該會看到“正在等待偵錯程式連線...”

傳回 VS 程式碼附加偵錯器：

![截圖](./attach.png)

返回Evennia，您應該看到「已連線偵錯器」。

現在觸發您設定的斷點，您將使用一個漂亮的圖形偵錯器。


----

<small>此檔案頁面是從`evennia\contrib\utils\debugpy\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
