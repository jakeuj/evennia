(overview-of-your-new-game-dir)=
# 新遊戲目錄概述

到目前為止，我們已經「執行了遊戲」一點，並開始在 Evennia 中使用 Python 進行遊戲。
是時候開始審視「遊戲之外」的情況了。

讓我們瀏覽一下您的遊戲目錄（我們假設它名為 `mygame`）。

> 檢視檔案時，忽略以 `.pyc` 結尾的檔案和 `__pycache__` 資料夾（如果存在）。這是您永遠不需要接觸的內部 Python 編譯檔。檔案`__init__.py`也經常是空的並且可以被忽略（它們與Python套件管理有關）。

你可能已經注意到，當我們在遊戲中建立東西時，我們經常透過「python路徑」引用程式碼，例如

    create/drop button:tutorial_examples.red_button.RedButton
	
這是編碼 Evennia 的一個基本面向 - _您建立程式碼，然後告訴 Evennia 該程式碼在哪裡以及何時應該使用_。上面我們告訴它透過從 `contrib/` 資料夾中提取特定程式碼來建立一個紅色按鈕。同樣的原則在任何地方都適用。因此，瞭解程式碼在哪裡以及如何正確指向它非常重要。

```{sidebar} Python 路徑
「python 路徑」使用「.」而不是 '/' 或 '`\\`' 並跳過檔案的 `.py` 結尾。它也可以指向python檔案的程式碼內容。由於 Evennia 已經在您的遊戲目錄中尋找程式碼，因此您的 python 路徑可以從那裡開始。因此路徑 `/home/foo/devel/mygame/commands/command.py` 將轉換為 Python 路徑 `commands.command`。
```


 - `mygame/`
    - `commands/` - 這包含所有自訂指令（使用者輸入處理程式）。您可以從此處新增自己的預設值並覆寫 Evennia 的預設值。
    - `server`/ - 此資料夾的結構不應更改，因為 Evennia 需要它。
        - `conf/` - 所有伺服器設定檔都位於此處。最重要的檔案是`settings.py`。
        - `logs/` - 伺服器日誌檔案儲存在此。當你使用 `evennia --log` 時，你實際上是
        tailing the files in this directory.
    - `typeclasses/` - this holds empty templates describing all database-bound entities in the  game, like Characters, Scripts, Accounts etc. Adding code here allows to customize and extend the defaults.  
    - `web/` - This is where you override and extend the default templates, views and static files used  for Evennia's web-presence, like the website and the HTML5 webclient.
    - `world/` - this is a "miscellaneous" folder holding everything related to the world you are building, such as build scripts and rules modules that don't fit with one of the other folders.

> `server/` 子資料夾應保持原樣 - Evennia 期望如此。但是您可以更改遊戲目錄其餘部分的結構，以最適合您的喜好。
> 也許您不想要單一世界/資料夾，而是更喜歡包含世界不同方面的多個資料夾？為您的 RPG 規則建立一個新資料夾「規則」？將您的指令與您的物件組合在一起，而不是將它們分開？這很好。如果你移動東西，你只需要更新 Evennia 的預設設定以指向新結構中的正確位置。

(commands)=
## 指令/

`commands/` 資料夾包含與建立和擴充 [Commands](../../../Components/Commands.md) 相關的 Python 模組
Evennia。這些在遊戲中體現出來，例如伺服器理解 `look` 或 `dig` 等輸入。

```{sidebar} 課程

`class` 是用於在 Python 中建立特定型別的物件例項的範本。我們將在下一課中更詳細地解釋課程。

```
- [command.py](github:evennia/game_template/commands/command.py)（Python 路徑：`commands.command`） - 這包含
用於設計新輸入指令的基類，或覆寫預設值。
- [default_cmdsets.py](github:evennia/game_template/commands/default_cmdsets.py)（Python 路徑：`commands.default_commands`）-
a cmdset（指令集）將指令組合在一起。可以動態地向物件新增和刪除指令集，
  這意味著使用者可以根據自己的情況使用不同的指令集（或指令版本）
  在遊戲中。為了向遊戲新增新指令，通常會匯入新指令類
  從 `command.py` 並將其新增到此模組中的預設 cmdsets 之一。
  
(server)=
## 伺服器/

此資料夾包含執行 Evennia 所需的資源。與其他資料夾相反，該資料夾的結構應保持原樣。

- `evennia.db3` - 只有當您使用預設的 SQLite3 資料庫時，您才會擁有此檔案。該檔案包含整個資料庫。只需複製它即可進行備份。對於開發，您也可以在設定完所需的所有內容後製作副本，然後將其複製回「重設」狀態。如果刪除此檔案，您可以透過執行 `evennia migrate` 輕鬆地重新建立它。

(serverlogs)=
### 伺服器/日誌/

這儲存了伺服器日誌。當您執行 `evennia --log` 時，evennia 程式實際上正在尾隨並連線此目錄中的 `server.log` 和 `portal.log` 檔案。日誌每週輪換一次。根據您的設定，您也可以在此處找到其他日誌，例如 webserver HTTP 請求日誌。

(serverconf)=
### 伺服器/conf/

這包含 Evennia 伺服器的所有設定檔。這些是常規 Python 模組，這意味著它們必須使用有效的 Python 進行擴充。如果您願意，您也可以為它們新增邏輯。

這些設定的共同點是，您通常不會直接透過 python 路徑匯入它們；相反，Evennia 知道它們在哪裡，並將在啟動時讀取它們以設定自身。

- `settings.py` - 這是迄今為止最重要的檔案。預設情況下它幾乎是空的，而不是你
預計會從 [evennia/default_settings.py](../../../Setup/Settings-Default.md) 複製並貼上您需要的變更。預設設定檔有大量檔案記錄。匯入/存取設定檔中的值是透過特殊方式完成的，如下所示：
            
        from django.conf import settings 

    To get to the setting `TELNET_PORT` in the settings file you'd then do 
    
        telnet_port = settings.TELNET_PORT
        
    You cannot assign to the settings file dynamically; you must change the `settings.py` file directly to  change a setting. See [Settings](../../../Setup/Settings.md) documentation for more details.
- `secret_settings.py` - 如果您要公開您的程式​​碼工作，您可能不想線上上分享所有設定。  可能存在特定於伺服器的秘密，或者只是對您的遊戲系統進行微調，您希望對玩家保密。將此類設定放在這裡，它將覆蓋 `settings.py` 中的值並且不包含在版本控制中。
- `at_initial_setup.py` - 當 Evennia 第一次啟動時，它會執行一些基本任務，例如建立超級使用者和 Limbo 房間。新增至此檔案可以為其新增更多操作以進行首次啟動。
- `at_search.py` - When searching for objects and either finding no match or more than one match, it will respond by giving a warning or offering the user to differentiate between the multiple mat。
- `at_server_startstop.py` - 這允許注入程式碼在每次伺服器以不同方式啟動、停止或重新載入時執行。
- `connection_screens.py` - 這允許更改您首次連線到遊戲時看到的連線畫面。
- `inlinefuncs.py` - [Inlinefuncs](../../../Concepts/Inline-Functions.md) 是可選且有限的“函式”，可以嵌入到傳送給玩家的任何字串中。它們被寫為 `$funcname(args)` 並用於根據接收它的使用者自訂輸出。例如，向人們傳送文字 `"Let's meet at $realtime(13:00, GMT)!` 會顯示每個看到該字串的玩家都在自己的時區給出的時間。新增到該模組的函式將成為遊戲中新的行內函數。另請參閱 [FuncParser](../../../Components/FuncParser.md)。
- `inputfuncs.py` - 當伺服器收到 `look` 這樣的指令時，它會由 [Inputfunc](InputFuncs) 處理，將其重定向到 cmdhandler 系統。但可能還有來自用戶端的其他輸入，例如按下按鈕或更新健康欄的請求。雖然已經涵蓋了大多數常見情況，但這是新增新函式來處理新型別輸入的地方。
- `lockfuncs.py` - [鎖定](../../../Components/Locks.md) 及其元件 _LockFuncs_ 限制對遊戲中事物的存取。 Lock func 在迷你語言中用來定義更複雜的鎖。例如，您可以使用 lockfunc 來檢查使用者是否攜帶給定物品、正在流血或具有一定的技能值。此模組中新增的函式將可在 lock 定義中使用。
- `mssp.py` - Mud 伺服器狀態協定是線上 MUD 檔案/清單（您通常必須註冊）追蹤哪些 MUDs 目前線上、他們有多少玩家等的一種方式。雖然 Evennia 自動處理動態訊息，但您可以在此處設定有關遊戲的元資訊，例如遊戲主題、是否允許殺死玩家等等。這是 Evennia Game 目錄的更通用形式。
- `portal_services_plugins.py` - 如果您想將新的外部連線協定新增至Evennia，則可以在此處新增它們。
- `server_services_plugins.py` - 這允許覆蓋內部伺服器連線協定。
- `web_plugins.py` - 這允許在啟動時將外掛新增到 Evennia webserver。

(typeclasses)=
### typeclasses/

Evennia 的 [Typeclasses](../../../Components/Typeclasses.md) 是 Evennia 特定的 Python 類，其例項將自身儲存到資料庫中。這允許角色保留在同一個地方，並且您更新的強度統計資料在伺服器重新啟動後仍然相同。

- [accounts.py](github:evennia/game_template/typeclasses/accounts.py)（Python 路徑：`typeclasses.accounts`） - [帳號](../../../Components/Accounts.md) 代表連結遊戲的玩家。它包含電子郵件、密碼和其他異常詳細資訊等資訊。
- [channels.py](github:evennia/game_template/typeclasses/channels.py)（Python 路徑：`typeclasses.channels`） - [頻道](../../../Components/Channels.md) 用於管理玩家之間的遊戲內通訊。
- [objects.py](github:evennia/game_template/typeclasses/objects.py)（Python 路徑：`typeclasses.objects`） - [物件](../../../Components/Objects.md) 代表在遊戲世界中擁有位置的所有事物。
- [characters.py](github:evennia/game_template/typeclasses/characters.py)（Python 路徑：`typeclasses.characters`） - [角色](../../../Components/Objects.md#characters) 是物件的子類，由帳戶控制 - 它們是遊戲世界中玩家的化身。
- [rooms.py](github:evennia/game_template/typeclasses/rooms.py) (Python-path: `typeclasses.rooms`) - [Room](../../../Components/Objects.md#rooms) 也是 Object 的子類別；描述離散位置。雖然傳統術語是“房間”，但這樣的位置可以是適合您的遊戲的任何位置和任何規模，從森林空地、整個星球或真正的地下城房間。
- [exits.py](github:evennia/game_template/typeclasses/exits.py)（Python 路徑：`typeclasses.exits`） - [Exits](../../../Components/Objects.md#exits) 是 Object 的另一個子類別。出口將一個房間連線到另一個房間。
- [scripts.py](github:evennia/game_template/typeclasses/scripts.py)（Python 路徑：`typeclasses.scripts`） - [Scripts](../../../Components/Scripts.md) 是「不符合字元」的物件。它們在遊戲中沒有位置，可以作為任何需要資料庫永續性的基礎，例如戰鬥、天氣或經濟系統。它們還能夠在計時器上重複執行程式碼。

(web)=
### 網路/

此資料夾包含子資料夾，用於使用您自己的設計覆蓋 Evennia 的預設 Web 存在。除了 README 檔案或其他空資料夾的子集之外，大多數資料夾都是空的。請參閱[Web 概述](../../../Components/Components-Overview.md#web-components) 以瞭解更多詳細資訊（我們稍後也會在本初學者教學中回到 Web）。

- `media/` - 這個空資料夾是您可以放置​​自己的映像或希望 Web 伺服器提供服務的其他媒體檔案的位置。如果您要發布帶有大量媒體的遊戲（特別是如果您想要影片），您應該考慮重新指向 Evennia 以使用某些外部服務來為您的媒體提供服務。
- `static_overrides/` - “靜態”檔案包括字型 CSS 和 JS。在此資料夾中，您將找到用於覆蓋 `admin`（這是 Django Web 管理員）、`webclient`（這是 HTML5 webclient）和 `website` 的靜態檔案的子資料夾。向此資料夾新增檔案將取代預設 Web 狀態中的同名檔案。
- `template_overrides/` - 這些是HTML 檔案，分別用於`webclient` 和`website`。 HTML 檔案是使用 [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) 範本編寫的，這意味著可以覆蓋
    only particular parts of a default template without touching others. 
- `static/` - 這是 Web 系統的工作目錄，不應手動修改。基本上，Evennia 會在伺服器啟動時從 `static_overrides` 複製靜態資料。
- `urls.py` - 該模組將 Python 程式碼連結到您在瀏覽器中造訪的 URLs。

(world)=
### 世界/

該資料夾僅包含一些範例檔案。它旨在儲存遊戲實現的“其餘部分”。許多人以各種方式改變和重組它，以更好地適應他們的想法。

- [batch_cmds.ev](github:evennia/game_template/world/batch_cmds.ev) - 這是一個 `.ev` 檔案，本質上只是按順序執行的 Evennia 指令的清單。這個是空的，可以擴充。 [教學世界](./Beginner-Tutorial-Tutorial-World.md)就是用這樣的批次檔建構的。
- [prototypes.py](github:evennia/game_template/world/prototypes.py) - [原型](../../../Components/Prototypes.md) 是一種輕鬆改變物件而不改變其基礎 typeclass 的方法。例如，可以使用原型來告訴兩個妖精，雖然都是「妖精」類別（因此它們遵循相同的程式碼邏輯），但應該具有不同的裝備、統計資料和外觀。
- [help_entries.py](github:evennia/game_template/world/help_entries.py) - 您可以透過多種方式新增新的遊戲內[說明條目](../../../Components/Help-System.md)，例如使用`sethelp`指令將它們新增至資料庫中，或（對於指令）直接從原始程式碼讀取協助。您也可以透過 python 模組新增它們。本模組是有關如何執行此操作的範例。
