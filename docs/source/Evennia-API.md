# API 摘要（英文）

> 這個 fork 的 API 參考仍然是從 Evennia 原始碼 docstrings 自動生成，目前維持英文。

[evennia](api/evennia-api.md) - 函式庫原始碼樹
- [evennia.accounts](evennia.accounts) - 代表玩家的 out-of-character 實體
- [evennia.commands](evennia.commands) - 處理所有輸入，也包含預設 commands
- [evennia.comms](evennia.comms) - 遊戲內頻道與訊息系統
- [evennia.contrib](evennia.contrib) - 由社群提供、偏向遊戲用途的工具與程式碼
- [evennia.help](evennia.help) - 遊戲內 help 系統
- [evennia.locks](evennia.locks) - 控制各種系統與資源存取權限的機制
- [evennia.objects](evennia.objects) - 所有遊戲內實體，例如 Rooms、Characters、Exits 等
- [evennia.prototypes](evennia.prototypes) - 用 dict 來客製化實體
- [evennia.scripts](evennia.scripts) - 所有 out-of-character 遊戲物件
- [evennia.server](evennia.server) - 核心的 Server 與 Portal 程式，也包含網路 protocols
- [evennia.typeclasses](evennia.typeclasses) - 核心的資料庫與 Python 橋接層
- [evennia.utils](evennia.utils) - 大量實用的開發工具與 utilities
- [evennia.web](evennia.web) - webclient、網站與其他 web 資源


## 常用捷徑

Evennia 的「flat API」提供了許多常用工具的捷徑，只要匯入 `evennia` 就能取得。
flat API 定義在 `__init__.py`，可[由此查看](github:evennia/__init__.py)。


### 主要設定

- [evennia.settings_default](Setup/Settings-Default.md) - 所有設定（在 `mygame/server/settings.py` 中修改或 override）

### 搜尋函式

- [evennia.search_account](evennia.utils.search.search_account)
- [evennia.search_object](evennia.utils.search.search_object)
- [evennia.search_tag](evennia.utils.search.search_tag)
- [evennia.search_script](evennia.utils.search.search_script)
- [evennia.search_channel](evennia.utils.search.search_channel)
- [evennia.search_message](evennia.utils.search.search_message)
- [evennia.search_help](evennia.utils.search.search_help_entry)

### 建立函式

- [evennia.create_account](evennia.utils.create.create_account)
- [evennia.create_object](evennia.utils.create.create_object)
- [evennia.create_script](evennia.utils.create.create_script)
- [evennia.create_channel](evennia.utils.create.create_channel)
- [evennia.create_help_entry](evennia.utils.create.create_help_entry)
- [evennia.create_message](evennia.utils.create.create_message)

### Typeclasses

- [evennia.DefaultAccount](evennia.accounts.accounts.DefaultAccount) - 玩家帳號 class（[docs](Components/Accounts.md)）
- [evennia.DefaultGuest](evennia.accounts.accounts.DefaultGuest) - guest 帳號的基礎 class
- [evennia.DefaultObject](evennia.objects.objects.DefaultObject) - 所有物件的基礎 class（[docs](Components/Objects.md)）
- [evennia.DefaultCharacter](evennia.objects.objects.DefaultCharacter) - 遊戲內角色的基礎 class（[docs](Components/Characters.md)）
- [evennia.DefaultRoom](evennia.objects.objects.DefaultRoom) - 房間的基礎 class（[docs](Components/Rooms.md)）
- [evennia.DefaultExit](evennia.objects.objects.DefaultExit) - 出口的基礎 class（[docs](Components/Exits.md)）
- [evennia.DefaultScript](evennia.scripts.scripts.DefaultScript) - OOC 物件的基礎 class（[docs](Components/Scripts.md)）
- [evennia.DefaultChannel](evennia.comms.comms.DefaultChannel) - 遊戲內頻道的基礎 class（[docs](Components/Channels.md)）

### Commands

- [evennia.Command](evennia.commands.command.Command) - 基礎 [Command](Components/Commands.md) class。另請參考 `evennia.default_cmds.MuxCommand`
- [evennia.CmdSet](evennia.commands.cmdset.CmdSet) - 基礎 [CmdSet](Components/Command-Sets.md) class
- [evennia.default_cmds](Components/Default-Commands.md) - 可將所有預設 command class 當成屬性存取

- [evennia.syscmdkeys](Components/Commands.md#system-commands) - 可將 system command keys 當成屬性存取

### Utilities

- [evennia.utils.utils](evennia.utils.utils) - 各種雜項但實用的工具
- [evennia.gametime](evennia.utils.gametime.TimeScript) - 伺服器運作時間與遊戲時間（[docs](Components/Coding-Utils.md#game-time)）
- [evennia.logger](evennia.utils.logger) - 記錄工具
- [evennia.ansi](evennia.utils.ansi) - ANSI 著色工具
- [evennia.spawn](evennia.prototypes.spawner.spawn) - spawn/prototype 系統（[docs](Components/Prototypes.md)）
- [evennia.lockfuncs](evennia.locks.lockfuncs) - 預設的 lock functions，用於存取控制（[docs](Components/Locks.md)）
- [evennia.EvMenu](evennia.utils.evmenu.EvMenu) - 選單系統（[docs](Components/EvMenu.md)）
- [evennia.EvTable](evennia.utils.evtable.EvTable) - 文字表格產生器
- [evennia.EvForm](evennia.utils.evform.EvForm) - 文字表單產生器
- Evennia.EvMore - 文字分頁器
- [evennia.EvEditor](evennia.utils.eveditor.EvEditor) - 遊戲內逐行文字編輯器（[docs](Components/EvEditor.md)）
- [evennia.utils.funcparser.Funcparser](evennia.utils.funcparser.FuncParser) - inline 函式 parsing（[docs](Components/FuncParser.md)）

### 全域 singleton handlers

- [evennia.TICKER_HANDLER](evennia.scripts.tickerhandler.TickerHandler) - 讓物件可以訂閱 ticker（[docs](Components/TickerHandler.md)）
- [evennia.MONITOR_HANDLER](evennia.scripts.monitorhandler.MonitorHandler) - 監看變更（[docs](Components/MonitorHandler.md)）
- [evennia.SESSION_HANDLER](evennia.server.sessionhandler.SessionHandler) - 管理所有 sessions 的主要 session handler

### 資料庫核心 models（供較進階查詢使用）

- [evennia.ObjectDB](evennia.objects.models.ObjectDB)
- [evennia.accountDB](evennia.accounts.models.AccountDB)
- [evennia.ScriptDB](evennia.scripts.models.ScriptDB)
- [evennia.ChannelDB](evennia.comms.models.ChannelDB)
- [evennia.Msg](evennia.comms.models.Msg)
- evennia.managers - 包含所有 database managers 的捷徑

### Contributions

- [evennia.contrib](Contribs/Contribs-Overview.md) - 遊戲導向的 contributions 與 plugins

```{toctree} 
:hidden:
api/evennia-api.md

```
