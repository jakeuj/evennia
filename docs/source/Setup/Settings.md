(changing-game-settings)=
# 更改遊戲設定

Evennia 開箱即用，無需對其設定進行任何更改。但是有幾種重要的方法可以自訂伺服器並使用您自己的外掛來擴充套件它。

所有遊戲特定的設定都位於 `mygame/server/conf/` 目錄中。

(settings-file)=
## 設定檔案

整個檔案中引用的「設定」檔案是該檔案
`mygame/server/conf/settings.py`。

你的新 `settings.py` 相對來說是開箱即用的。 Evennia的核心設定檔是
[設定-預設檔](./Settings-Default.md) 並且更加廣泛。這也是
有大量檔案記錄並且是最新的，因此您應該直接參考此檔案以取得可用設定。

由於 `mygame/server/conf/settings.py` 是一個普通的 Python 模組，因此它只需匯入
`evennia/settings_default.py` 進入頂部。

這意味著，如果您想要更改的任何設定依賴於某些*其他*預設設定，您可能需要複製並貼上這兩個設定才能更改它們並獲得您想要的效果（對於最常更改的設定，這不是您需要擔心的事情）。

您永遠不應該編輯`evennia/settings_default.py`。相反，您應該將要更改的選擇變數複製並貼上到 `settings.py` 中並在那裡編輯它們。這將超載之前匯入的預設值。

```{warning} 不要複製一切！
將 `settings_default.py` 中的*所有內容*複製到您自己的設定檔中，只是為了將其全部放在一處，這可能很誘人。不要這樣做。透過僅複製您需要的內容，您可以更輕鬆地追蹤更改的內容。
```

在程式碼中，可以透過以下方式存取設定

```python
    from django.conf import settings
     # or (shorter):
    from evennia import settings
     # example:
    servername = settings.SERVER_NAME
```

每個設定都顯示為匯入的 `settings` 物件上的屬性。  您也可以使用 `evennia.settings_full` 探索所有可能的選項（這也包括預設 Evennia 中未觸及的進階 Django 預設值）。

> 當像這樣將 `settings` 匯入到程式碼中時，它將是*只讀*。您*無法*透過程式碼編輯您的設定！更改 Evennia 設定的唯一方法是直接編輯 `mygame/server/conf/settings.py`。在變更的設定變得可用之前，您還需要重新啟動伺服器（可能還包括 Portal）。

(other-files-in-the-serverconf-directory)=
## `server/conf`目錄下的其他檔案

除了主要的 `settings.py` 檔案之外，

- `at_initial_setup.py` - 這允許您新增自訂啟動方法（僅）在第一次 Evennia 啟動時（在建立使用者 #1 和 Limbo 的同時）呼叫。它可以啟動您自己的全域 scripts 或設定您的遊戲需要從一開始就執行的其他系統/世界相關的東西。
- `at_server_startstop.py` - 此模組包含 Evennia 將在伺服器每次啟動和停止時分別呼叫的函式 - 這包括由於重新載入和重置而停止以及完全關閉。這是一個有用的地方，可以為處理程式和其他必須在遊戲中執行但沒有資料庫永續性的東西放置自訂啟動程式碼。
- `connection_screens.py` - 此模組中的所有全域字串變數都被 Evennia 解釋為問候螢幕，以在帳戶首次連線時顯示。如果模組中存在多個字串變數，則會隨機選擇一個。
- `inlinefuncs.py` - 您可以在此定義自訂 [FuncParser 函式](../Components/FuncParser.md)。
- `inputfuncs.py` - 您可以在此定義自訂[輸入函式](../Components/Inputfuncs.md) 來處理來自客戶端的資料。
- `lockfuncs.py` - 這是儲存您自己的「安全」*lock 函式* 的眾多可能模組之一，以供 Evennia 的 [鎖定](../Components/Locks.md) 使用。
- `mssp.py` - 這包含有關您的遊戲的元資訊。它被 MUD 搜尋引擎（您經常需要註冊）使用，以顯示您正在執行的遊戲型別以及線上帳戶數量和線上狀態等統計資料。
- `oobfuncs.py` - 在這裡您可以定義自訂[OOB 函式](../Concepts/OOB.md)。
- `portal_services_plugin.py` - 這允許將您自己的自訂服務/協定新增至Portal。它必須定義一個特定的函式，該函式將在啟動時由 Evennia 呼叫。可以有任意數量的服務外掛模組，如果定義的話，所有服務外掛模組都將被匯入和使用。更多資訊可以在[此處](https://code.google.com/p/evennia/wiki/SessionProtocols#Adding_custom_Protocols)找到。
- `server_services_plugin.py` - 這與前一個相同，但用於向伺服器新增服務。更多資訊可以在[此處](https://code.google.com/p/evennia/wiki/SessionProtocols#Adding_custom_Protocols)找到。

其他一些Evennia系統可以透過外掛模組定製，但在`conf/`中沒有明確的模板：

- `cmdparser.py` - 自訂模組可用於完全替換 Evennia 的預設指令解析器。所做的就是將傳入的字串拆分為「指令名稱」和「其餘部分」。它還處理諸如不匹配和多重匹配的錯誤訊息之類的事情，這使得這比聽起來更複雜。預設解析器是*非常*通用的，因此您通常最好透過修改比此處更進一步的內容（在指令解析層級）來獲得最佳服務。
- `at_search.py` - 這允許取代 Evennia 處理搜尋結果的方式。它允許更改錯誤的回顯方式以及多重匹配的解決和報告方式（例如預設如何理解“2-ball”應該匹配第二個“ball”物件，如果房間中有兩個“ball”物件）。
