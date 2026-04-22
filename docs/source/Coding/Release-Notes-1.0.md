(evennia-10-release-notes)=
# Evennia 1.0 發行說明

這總結了這些變化。完整清單請參閱[變更日誌](./Changelog.md)。

- 現在主要開發在 `main` 分支上。 `master` 分支仍然存在，但不會再更新。

(minimum-requirements)=
## 最低要求

- 現在至少需要 Python 3.10。 Ubuntu LTS 現在隨 3.10 一起安裝。 Evennia 1.0 也使用 Python 3.11 進行了測試 - 這是 Linux/Mac 的建議版本。 Windows 使用者可能希望繼續使用 Python 3.10，除非他們同意安裝 C++ 編譯器。
- 扭曲22.10+
- 姜戈 4.1+

(major-new-features)=
## 主要新功能

- Evennia 現在位於 PyPi 上，並且可以作為 [pip install evennia](../Setup/Installation.md) 安裝。
- 完全修改的檔案位於 https://www.evennia.com/docs/latest. 舊的 wiki 和 readmedocs 頁面將關閉。
-  Evennia 1.0 現在有 REST API，它允許您使用 CRUD 操作 GET/POST 等訪問遊戲物件。有關詳細資訊，請參閱 [The Web-API 檔案][Web-API]。
- Evennia 頻道和 Discord 伺服器之間的 [Evennia<>Discord 整合](../Setup/Channels-to-Discord.md)。
- [Script](../Components/Scripts.md)大修：Scripts'計時器元件獨立於script物件刪除；現在可以啟動/停止計時器而不刪除Script。 `.persistent` 標誌現在僅控制計時器是否在重新載入後倖存 - Script 必須像其他型別分類實體一樣用 `.delete()` 刪除。這使得 Scripts 作為通用儲存實體更加有用。
- [FuncParser](../Components/FuncParser.md) 集中並極大地改進了所有字串內函式呼叫，例如 `say the result is $eval(3 * 7)` 並表示結果 `the result is 21`。解析器完全取代了舊的`parse_inlinefunc`。新的解析器可以處理引數和 kwargs，也可用於原型解析以及導演立場訊息傳遞，例如使用 `$You()` 在字串中表示自己，並根據看到您的人而得出不同的結果。
- [頻道](../Components/Channels.md) 使用 `channel` 指令和缺口的新頻道系統。舊的`ChannelHandler`被刪除，通道的自訂和操作也簡化了很多。舊的指令語法指令現在以 contrib 的形式提供。
- [幫助系統](../Components/Help-System.md)已重構。
	- 新型 `FileHelp` 系統可讓您將遊戲內說明檔案新增為外部 Python 檔案。這意味著可以透過三種方式在 Evennia 中新增說明專案：1) 從 Command 程式碼自動產生。 2) 從遊戲中的 `sethelp` 指令手動新增到資料庫，以及 3) 建立為 Evennia 載入並在遊戲中可用的外部 Python 檔案。
	- 我們現在使用 `lunr` 搜尋索引來獲得更好的 `help` 匹配和建議。還改善
主幫助指令的預設清單輸出。
	- 幫助指令現在使用 `view` lock 來確定 cmd/entry 是否顯示在索引中，並使用 `read` lock 來確定它是否可以讀取。後者的角色曾經是`view`。
	- 如果在建立新條目時隱藏其他幫助型別，`sethelp` 指令現在會發出警告。
	- 使 `help` 索引輸出可供 webclient/MXP 的使用者端點選（PR 由 davewiththenicehat 提供）
-  重新設計 [Web](../Components/Website.md) 設定，使其結構更加一致並更新到最新的 Django。 `mygame/web/static_overrides` 和 `-template_overrides` 已被刪除。這些資料夾現在只有 `mygame/web/static` 和 `/templates`，並在幕後處理資料的自動複製。 `app.css` 到 `website.css` 以保持一致性。舊的 `prosimii-css` 檔案已被刪除。
- [AttributeProperty] 以及 `AliasProperty` 和 `PermissionProperty` 允許以與 Django 欄位相同的方式管理 typeclasses 上的屬性、Tags、別名和許可權。這大大減少了在 `at_create_object` 掛鉤中分配 Attributes/Tags 的需要。
- 舊的 `MULTISESSION_MODE` 被分成更小的設定，以便更好地控制使用者連線時發生的情況、是否應自動建立角色以及可以同時控制多少個角色。詳細說明請參閱[連線樣式](../Concepts/Connection-Styles.md)。
- Evennia 現在支援自訂 `evennia` 啟動器指令（e.g。`evennia mycmd foo bar`）。將新指令新增為接受 `*args` 的可呼叫項，例如 `settings.EXTRA_LAUNCHER_COMMANDS = {'mycmd': 'path.to.callable',...}`。


(contribs)=
## Contribs

`contrib` 資料夾結構從 0.9.5 開始已更改。所有 contribs 現在都在子資料夾中並按類別組織。必須更新所有匯入路徑。請參閱[Contribs概述](../Contribs/Contribs-Overview.md)。

- 新的[特質contrib](../Contribs/Contrib-Traits.md)，由Ainneve專案轉換和擴充套件。 （白噪聲，Griatch）
- 新增[製作contrib](../Contribs/Contrib-Crafting.md)，新增完整的製作子系統(Griatch)
- 新增 [XYZGrid contrib](../Contribs/Contrib-XYZGrid.md)，新增 x,y,z 網格座標以及遊戲內地圖和尋路功能。透過自訂 evennia 啟動器指令 (Griatch) 在遊戲外控制
- 新的[指令冷卻時間contrib](../Contribs/Contrib-Cooldowns.md)contrib，讓管理指令變得更容易
使用之間的動態冷卻時間（owllex）
- 新的 [Godot 協議 contrib](../Contribs/Contrib-Godotwebsocket.md) 用於從用開源遊戲引擎 [Godot](https://godotengine.org/) (ChrisLR) 編寫的用戶端連線到 Evennia。
- 新的 [name_generator contrib](../Contribs/Contrib-Name-Generator.md) 用於根據語音規則建立隨機的現實世界或幻想名稱 (InspectorCaracal)
- 新的 [Buffs contrib](../Contribs/Contrib-Buffs.md) 用於管理臨時和永久 RPG 狀態 buff 效果 (tegiminis)
-  現有的 [RPSystem contrib](../Contribs/Contrib-RPSystem.md) 進行了重構，速度得到了提升（InspectorCaracal，其他貢獻者）

(translations)=
## 翻譯

- 新拉丁文 (la) 翻譯 (jamalainm)
- 新的德語 (de) 翻譯 (Zhuraj)
- 更新了義大利文翻譯（rpolve）
- 更新了瑞典文翻譯

(utils)=
## 實用程式

- 新的 `utils.format_grid` 用於輕鬆顯示區塊中的長專案清單。現在用於預設幫助顯示。
- 新增`utils.repeat`和`utils.unrepeat`作為TickerHandler新增/刪除的快捷方式，類似
`utils.delay` 是如何新增 TaskHandler 的捷徑。
- 加入 `utils/verb_conjugation` 以實現自動動詞變形（僅限英文）。這
對於實現演員立場表情以將字串傳送到不同的目標非常有用。
- `utils.evmenu.ask_yes_no` 是一個輔助函式，可以輕鬆提出是/否問題
給使用者並回應他們的輸入。這補充了現有的 `get_input` 幫助程式。
- 用於管理任務的新`tasks`指令以`utils.delay`開始（PR由davewiththenicehat）
- 將 `.deserialize()` 方法新增到 `_Saver*` 結構以完全幫助
將結構與資料庫解耦，無需單獨匯入。
- 新增 `run_in_main_thread` 作為那些想要編寫伺服器程式碼的幫助者
從網頁檢視來看。
- 更新 `evennia.utils.logger` 以使用 Twisted 的新日誌記錄 API。 Evennia API 沒有變化
除了現在可以使用更多標準別名 logger.error/info/exception/debug 等。
- 使用牛津逗號使 `utils.iter_to_str` 格式的字串更漂亮。
- 將 `create_*` 函式移至資料庫管理器，僅剩下 `utils.create`
包裝函式（與`utils.search`一致）。否則不改變 api。

(locks)=
## 鎖具

- 新的 `search:` lock 型別用於完全隱藏物件以使其不被發現
`DefaultObject.search` (`caller.search`) 方法。 (CloudKeeper)
- `holds()` lockfunc 的新預設值 - 從預設值 `True` 更改為預設值 `False`，以禁止丟棄無意義的東西（例如你不持有的東西）。

(hook-changes)=
## 鉤子變化

- 為了保持一致性，將所有 `at_before/after_*` 掛鉤更改為 `at_pre/post_*`
跨Evennia（舊名稱仍然有效，但已棄用）
- `Objects` 上的新 `at_pre_object_leave(obj, destination)` 方法。
- 在所有其他啟動掛鉤之前呼叫新的 `at_server_init()` 掛鉤
啟動模式。用於更通用的覆蓋（volund）
- 物件上的新 `at_pre_object_receive(obj, source_location)` 方法。被召喚
目的地，模仿 `at_pre_move` 鉤子的行為 - 返回 False 將中止移動。
- `Object.normalize_name` 和 `.validate_name` 加到（預設）強制 latinify
關於字元名稱並使用巧妙的 Unicode 字元避免潛在的漏洞 (trhr)
- 使 `object.search` 支援 'stacks=0' 關鍵字 - 如果 ``>0``，則該方法將返回
N 個相同的匹配，而不是觸發多重匹配錯誤。
- 增加 `tags.has()` 方法來檢查物件是否具有 tag 或 tags（PR by ChrisLR）
- 新增 `Msg.db_receiver_external` 欄位以允許外部字串 ID 訊息接收者。
- 新增 `$pron()` 和 `$You()` 行內函數，以便使用 `msg_contents` 在演員立場字串中進行代名詞解析。

(command-changes)=
## 指令變更

- 將預設多重配對語法從 `1-obj`、`2-obj` 更改為 `obj-1`、`obj-2`，這似乎是最期望的。
- 使用輔助方法拆分 `return_appearance` 鉤子並讓它使用模板
字串，以便更容易覆蓋。
- 現在在副本上執行指令以確保 `yield` 不會導致交叉。新增
`Command.retain_instance` 標誌用於重複使用相同的指令例項。
- 如果目標名稱不包含空格，則允許傳送帶有 `page/tell` 且不帶 `=` 的訊息。
- `typeclass` 指令現在將正確搜尋目標的正確資料庫表
obj（避免錯誤地將 AccountDB-typeclass 分配給角色等）。
- 將 `script` 和 `scripts` 指令合併為一個，用於管理全域和
對像上Scripts。已將 `CmdScripts` 和 `CmdObjects` 移至 `commands/default/building.py`。
- `channel` 指令取代所有舊的通道相關指令，例如 `cset` 等
- 將 `examine` 指令的程式碼擴充套件為更具可擴充套件性和模組化。展示
attribute 類別和值型別（當不是字串時）。
	- 新增使用 `examine` 指令檢查 `/script` 和 `/channel` 實體的功能。
- 分配 Attribute 值時加入對 `$dbref()` 和 `$search` 的支援
使用 `set` 指令。這允許分配遊戲中的真實物件。
- 將 `type/force` 預設為 `update`-模式而不是 `reset` 模式並新增更多詳細資訊
使用重置模式時發出警告。

(coding-improvement-highlights)=
## 編碼改進亮點

- db pickle-serializer 現在檢查方法 `__serialize_dbobjs__` 和 `__deserialize_dbobjs__` 以允許自訂打包/解包巢狀 dbobj，以允許儲存在 Attribute 中。請參閱[屬性](../Components/Attributes.md) 檔案。
- 將 `ObjectParent` mixin 新增到預設遊戲資料夾模板中，作為一個簡單的現成的
輕鬆覆寫所有 ObjectDB 繼承物件上的功能的方法。
  來源位置，模仿 `at_pre_move` 鉤子的行為 - 返回 False 將中止移動。
- 新的單元測試父類，可在 Evenia 核心和 mygame 中使用。重組單元測試以始終遵循預設設定。
  
 
(other)=
## 其他

- 統一管理器搜尋方法以始終傳回查詢集，而不是有時傳回查詢集，有時會傳回清單。
- Attribute/NAttribute 使用介面獲得了同質表示，兩者
`AttributeHandler` 和 `NAttributeHandler` 現在具有相同的 api。
- 已將 `content_types` 索引新增至 DefaultObject 的 ContentsHandler。 （沃倫德）
- 完成了大部分網路類，例如協定和SessionHandlers
改裝愛好者可透過 `settings.py` 更換。 （沃倫德）
- 現在可以在 `settings.py` 中替換 `initial_setup.py` 檔案以進行自訂
初始遊戲資料庫狀態。 （沃倫德）
- 讓IP節流使用基於Django的快取系統來實現可選的永續性（PR by strikaco）
- 在 `settings.PROTOTYPE_MODULES` 給出的模組中，spawner 現在將首先尋找全域性
在將模組中的所有字典載入為原型之前列出 `PROTOTYPE_LIST` 的字典。
  動態建立的 `ChannelCmdSet` 的概念。
- 原型現在允許直接將 `prototype_parent` 設定為原型字典。
這使得動態建構模組內原型變得更加容易。
- 讓 `@lazy_property` 裝飾器建立讀取/刪除保護的屬性。這是因為它用於處理程式和e.g。 self.locks=[] 是初學者常見的錯誤。
- 將 `settings.COMMAND_DEFAULT_ARG_REGEX` 預設值從 `None` 變更為正規表示式，這表示
必須用空格或 `/` 分隔 cmdname 和 args。這更符合普遍的期望。
- 新增 `settings.MXP_ENABLED=True` 和 `settings.MXP_OUTGOING_ONLY=True` 作為合理的預設值，以避免玩家輸入 MXP 連結時出現已知的安全問題。
- 使 `MonitorHandler.add/remove` 支援 `category` 用於監視具有類別的屬性（在僅使用鍵之前，完全忽略類別）。
 

