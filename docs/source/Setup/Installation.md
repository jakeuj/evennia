(installation)=
# 安裝

安裝 Evennia 最快的方法是使用 Python 隨附的 `pip` 安裝程式（繼續閱讀）。您也可以[從 github 克隆 Evennia](./Installation-Git.md) 或使用 [docker](./Installation-Docker.md)。  有些使用者也嘗試過[在Android上安裝Evennia](./Installation-Android.md)。

如果您要轉換現有遊戲，請按照[升級說明](./Installation-Upgrade.md) 進行操作。

(requirements)=
## 要求

```{sidebar} 孤立發展
安裝 Evennia 不會使任何內容線上上可見。除了安裝和更新之外，如果您願意，您還可以在沒有任何網路連線的情況下開發遊戲。
```
- Evennia 需要 [Python](https://www.python.org/downloads/) 3.11、3.12 或 3.13（建議）。任何支援 Python 的 OS 都應該可以工作。
	- _Windows_：在安裝程式中，確保選擇`add python to path`。如果您安裝了多個版本的 Python，請使用 `py` 指令而不是 `python` 讓 Windows 自動使用最新版本。
- 不要以管理員或超級使用者身分安裝 Evennia。
- 如果遇到問題，請參閱[安裝疑難排解](./Installation-Troubleshooting.md)。

(install-with-pip)=
## 使用`pip`安裝

```{important}
建議您設定一個輕量級的 Python virtualenv 來安裝 Evennia。使用 virtualenv 是 Python 中的標準做法，它允許您獨立於其他程式安裝所需的內容。 virtualenv 系統是 Python 的一部分，將使您的生活更輕鬆！
```

建議您先[設定一個輕量級Python virtualenv](./Installation-Git.md#virtualenv)。

Evennia 從終端機（Windows 上的控制檯/指令提示字元）進行管理。安裝 Python 後，如果您使用的是 virtualenv，則在啟動 virtualenv 後，安裝 Evennia：

點安裝evennia

可選：如果您使用警告您需要其他軟體包的 [contrib](../Contribs/Contribs-Overview.md)，您可以使用以下指令安裝所有額外的依賴項：

pip install evennia[額外]

若要稍後更新 Evennia，請執行以下操作：

pip install --升級evennia

```{note} **僅限 Windows 使用者 -**
您現在必須執行 `python -m evennia` 一次。這應該會使 `evennia` 指令在您的環境中永久可用。
```

安裝後，請確保 `evennia` 指令有效。使用 `evennia -h` 獲取使用協助。如果您使用的是 virtualenv，請確保稍後需要使用 `evennia` 指令時它處於活動狀態。

(initialize-a-new-game)=
## 初始化新遊戲

我們將建立一個新的「遊戲目錄」來建立您的遊戲。在這裡以及 Evennia 檔案的其餘部分中，我們將此遊戲目錄稱為 `mygame`，但當然，您應該根據自己的喜好命名您的遊戲。要建立新的 `mygame` 資料夾&mdash;或您選擇的任何內容&mdash;在目前位置：

```{sidebar} 遊戲目錄與遊戲名稱
您建立的遊戲目錄不必與您的遊戲名稱相符。您可以稍後透過編輯 `mygame/server/conf/settings.py` 更改遊戲名稱。
```

evennia --init mygame

產生的資料夾包含啟動 Evennia 伺服器所需的所有空白模板和預設設定。

(start-the-new-game)=
## 開始新遊戲

首先，建立預設資料庫（Sqlite3）：

cd我的遊戲
	evennia遷移

產生的資料庫檔案在 `mygame/server/evennia.db3` 中建立。如果您想從新資料庫啟動，只需刪除該檔案並重新執行 `evennia migrate` 指令即可。

接下來，使用以下指令啟動 Evennia 伺服器：

evennia開始

出現提示時，輸入遊戲中「上帝」或「超級使用者」的使用者名稱和密碼。提供電子郵件地址是可選的。

> 您也可以[自動](./Installation-Non-Interactive.md)建立超級使用者。

如果一切順利，您的新 Evennia 伺服器現已啟動並執行！要玩您的新遊戲（儘管是空的），請將舊版 MUD/telnet 使用者端指向 `localhost:4000` 或將 Web 瀏覽器指向 [http://localhost:4001](http://localhost:4001)。您可以作為新帳戶登入或使用您在上面建立的超級使用者帳戶。

(restarting-and-stopping)=
## 重新啟動和停止


您可以透過發出以下指令重新啟動伺服器（無需斷開玩家連線）：

evennia重新啟動

並且，要完全停止並重新啟動（斷開玩家連線），請使用：

evennia重新啟動

伺服器完全停止（使用 `evennia start` 重新啟動）是透過以下方式實現的：

evennia停止

有關詳細資訊，請參閱[伺服器啟動-停止-重新載入](./Running-Evennia.md) 檔案頁面。

(view-server-logs)=
## 檢視伺服器日誌

日誌檔案位於`mygame/server/logs`。您可以透過以下方式即時追蹤日誌記錄：

evennia --日誌

或只是：

evennia-l

按`Ctrl-C`（Mac 為`Cmd-C`）停止檢視即時日誌。

您也可以透過將 `-l/--log` 新增至 `evennia` 指令立即開始檢視即時日誌，例如在啟動伺服器時：

    evennia start -l

(server-configuration)=
## 伺服器設定

您的伺服器的設定檔是`mygame/server/conf/settings.py`。預設情況下它是空的。 **僅**將您想要/需要的設定從 [預設設定檔](./Settings-Default.md) 複製並貼上到伺服器的 `settings.py`。此時在設定伺服器之前，請參閱[設定](./Settings.md) 檔案以取得更多資訊。

(register-with-the-evennia-game-index-optional)=
## 使用 Evennia 遊戲索引註冊（可選）

為了讓全世界知道您正在開發一款基於 Evennia 的新遊戲，您可以透過發出以下指令向 _Evennia 遊戲索引_ 註冊您的伺服器：

    evennia connections

然後，請按照提示操作即可。你不必開放玩家才能做到這一點——只需將您的遊戲標記為已關閉和「pre-alpha」。

請參閱[此處](./Evennia-Game-Index.md)以瞭解更多說明，並請事先[檢視索引](http:games.evennia.com)以確保您沒有選擇已被佔用的遊戲名稱 –乖一點！

(next-steps)=
## 下一步

你可以走了！

接下來，何不前往[入門教學](../Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.md) 學習如何開始製作新遊戲！
