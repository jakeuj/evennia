(start-stop-reload)=
# 開始 停止 重新載入


您可以使用 `evennia` 從您的遊戲資料夾控制 Evennia（我們在此稱之為 `mygame/`）
程式。如果 `evennia` 程式在指令列上不可用，則必須先安裝
Evennia，如[安裝](./Installation.md)頁面所述。

```{sidebar} evennia 找不到？
如果您嘗試使用 `evennia` 指令並收到錯誤訊息，抱怨該指令不可用，請確保您的 [virtualenv](./Installation-Git.md#virtualenv) 處於活動狀態。在 Windows 上，您可能需要先執行 `py -m evennia` 一次。
```

下面描述了各種管理選項。跑步

    evennia -h

為您提供簡短的協助

    evennia menu

為您提供帶有選項的選單。

(starting-evennia)=
## 開始Evennia

Evennia 由兩個元件組成：Evennia [Portal 和伺服器](../Components/Portal-And-Server.md)。  簡而言之，*伺服器*就是執行泥漿的東西。它處理所有特定於遊戲的事情，但並不關心玩家如何連線，只關心他們如何連線。 *Portal* 是玩家連線的閘道器。它瞭解有關 telnet、ssh、webclient 協議等的所有內容，但對遊戲知之甚少。兩者都是遊戲正常運作所必需的。

     evennia start

上述指令將啟動 Portal，後者將啟動伺服器。該指令將列印該過程的摘要，除非出現錯誤，否則您將看不到進一步的輸出。兩個元件都將記錄到 `mygame/server/logs/` 中的日誌檔案中。為了方便起見，您可以透過將 `-l` 附加到指令來直接在終端機中追蹤這些日誌：

     evennia -l

將開始追蹤已執行伺服器的日誌。當開始Evennia時你也可以這樣做

     evennia start -l

> 若要停止檢視日誌檔案，請按 `Ctrl-C`（在 Mac 上為 `Cmd-C`）。

(reloading)=
## 重新裝彈

*重新載入*的行為意味著Portal將告訴伺服器關閉然後再次啟動。每個人都會收到一條訊息，並且隨著伺服器重新啟動，所有帳戶的遊戲都會短暫暫停。由於它們連線到*Portal*，因此它們的連線不會遺失。


重新載入就像您能得到的最接近的“熱重啟”。它重新初始化 Evennia 的所有程式碼，但不會終止「持久」[Scripts](../Components/Scripts.md)。它還對所有物件呼叫 `at_server_reload()` 掛鉤，以便您可以儲存所需的最終臨時屬性。

在遊戲中使用 `reload` 指令。您也可以從遊戲外部重新載入伺服器：

     evennia reload

有時，如果您新增了某種阻止遊戲內輸入的錯誤，則需要從「外部」重新載入。

(stopping)=
## 停止

完全關閉會完全關閉 Evennia，包括伺服器和 Portal。所有帳戶將被啟動並且
系統儲存並乾淨地關閉。

在遊戲內部，您可以使用 `shutdown` 指令啟動關閉。  從指令列你做

     evennia stop

您將看到伺服器和 Portal 關閉的訊息。所有帳戶都將被關閉
訊息，然後斷開連線。


(foreground-mode)=
## 前臺模式

通常，Evennia 作為「守護程式」在背景執行。如果您願意，您可以啟動其中一個
程式（但不是兩者）作為*互動*模式下的前臺程式。這意味著他們將記錄
直接到終端（而不是記錄我們然後回顯到終端的檔案），您可以
使用 `Ctrl-C` 終止程式（而不僅僅是日誌檔案檢視）。

    evennia istart

將以互動模式啟動/重新啟動*伺服器*。如果您想執行，這是必需的
[偵錯程式](../Coding/Debugging.md)。下次您`evennia reload`伺服器時，它將返回正常模式。

    evennia ipstart

將以互動模式啟動 *Portal*。

如果您在前臺模式下執行`Ctrl-C`/`Cmd-C`，則該元件將停止。您需要執行 `evennia start` 才能讓遊戲重新開始。

(resetting)=
## 重置

*重置*相當於「冷重啟」 - 伺服器將關閉然後重新啟動
再次，但表現得就像完全關閉一樣。與「真正的」關閉相反，重置期間不會中斷任何帳戶。然而，重置將清除所有非永續性 scripts 並呼叫 `at_server_shutdown()` 掛鉤。例如，這可能是在開發過程中清除不安全的 scripts 的好方法。

在遊戲中使用 `reset` 指令。從航廈：

    evennia reset


(rebooting)=
## 重新啟動

這將關閉*伺服器和Portal，這意味著所有連線的玩家將失去他們的
連線。只能從終端啟動：

    evennia reboot

這與執行這兩個指令相同：

     evennia stop
     evennia start

(status-and-info)=
## 狀態和訊息

要檢查基本 Evennia 設定，例如哪些連線埠和服務處於活動狀態，這將重複
啟動伺服器時給出的初始回傳：

    evennia info

您還可以使用此指令從兩個元件獲取更短的執行狀態

    evennia status

這對於自動檢查以確保遊戲正在執行並正在響應非常有用。


(killing-linuxmac-only)=
## 殺戮（限 Linux/Mac）

在極端情況下，兩個伺服器程式都沒有鎖定並且不回應指令，
[]()您可以向它們傳送終止訊號以強制它們關閉。僅終止伺服器：

    evennia skill

要殺死伺服器和 Portal：

    evennia kill

請注意，Windows 不支援此功能。


(django-options)=
## Django 選項

`evennia` 程式也會傳遞 `django-admin` 使用的選項。它們以各種方式對資料庫進行操作。

```bash

 evennia migrate # migrate the database
 evennia shell   # launch an interactive, django-aware python shell
 evennia dbshell # launch the database shell

```

有關（許多）更多選項，請參閱 [django-admin 檔案](https://docs.djangoproject.com/en/4.1/ref/django-admin/#usage)。

(advanced-handling-of-evennia-processes)=
## Evennia程式的高階處理

如果您需要手動管理 Evennia 的處理器（或在工作管理員程式中檢視它們）
例如Linux的`top`或更高階的`htop`），你會發現下面的程式是
與 Evennia 相關：

* 1 x `twistd... evennia/server/portal/portal.py` - 這是 Portal 程式。
* 3 x `twistd... server.py` - 其中一個行程管理 Evennia 的伺服器元件，即主遊戲。其他程式（具有相同名稱但不同程式 ID）處理 Evennia 的內部 Web 伺服器執行緒。您可以檢視`mygame/server/server.pid`來決定哪個是主程式。

(syntax-errors-during-live-development)=
### 即時開發期間的語法錯誤

在開發過程中，您通常會修改程式碼，然後重新載入伺服器以檢視變更。
這是透過Evennia從磁碟重新匯入自訂模組來完成的。通常模組中的錯誤會
只是讓您在遊戲、日誌或指令列中看到回溯。  對於一些確實
儘管存在嚴重的語法錯誤，您的模組甚至可能不會被識別為有效的 Python。 Evennia 可能無法正確重新啟動。

在遊戲內部，您會看到一條有關伺服器重新啟動的文字，後面是不斷增長的列表
「……」。通常這只會持續很短的時間（最多幾秒鐘）。如果這種情況繼續下去的話
表示 Portal 仍在執行（您仍連線到遊戲），但伺服器元件
Evennia 重新啟動失敗（即保持關閉狀態）。檢視您的日誌檔案或
終端檢視問題所在 - 您通常會看到清晰的回溯，顯示發生了什麼
錯了。

修復錯誤然後執行

    evennia start

假設錯誤已修復，這將手動啟動伺服器（而不重新啟動Portal）。
在遊戲中，您現在應該收到伺服器已成功重新啟動的訊息。