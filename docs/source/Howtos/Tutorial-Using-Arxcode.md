(using-the-arxcode-game-dir)=
# 使用 Arxcode 遊戲目錄

```{warning} arxcode 是單獨維護的。

雖然 Arxcode 使用 Evennia，但它_不是 Evennia 本身的一部分；我們僅將此檔案作為向使用者提供的服務提供。此外，雖然 Arxcode 仍在積極維護（2022 年），但這些指令是基於截至 *2018 年 8 月 12 日*發布的 Arx 程式碼。它們可能不再能夠 100% 開箱即用。

Arxcode 錯誤應定向到 [Arxcode github 問題追蹤器](https://github.com/Arx-Game/arxcode/issues)。
```

[Arx - 清算之後](https://play.arxmush.org/) 是一款大型且非常流行的基於 [Evennia](https://www.evennia.com) 的遊戲。 Arx 很大程度上以角色扮演為中心，依靠遊戲大師來推動故事發展。從技術上講，最好的描述可能是「a MUSH，但具有更多編碼系統」。 2018年8月，遊戲開發商Tehom慷慨地在github上發布了[Arx的原始碼](https://github.com/Arx-Game/arxcode)。對於想要挑選想法甚至想要建立起始遊戲的開發者來說，這是一個寶庫。

從原始程式碼執行 Arx 並不太難（當然，您將從空資料庫開始），但是
由於 Arx 的一部分是有機成長的，因此它並不遵循任何地方的標準 Evennia 正規化。
本頁介紹如何安裝和設定一些東西，同時使您的新的基於 Arx 的遊戲更好地匹配普通 Evennia 安裝。

(installing-evennia)=
## 正在安裝Evennia

首先，在磁碟機上留出一個資料夾/目錄以供後續操作使用。

您需要先按照 OS 的大部分 [Git 安裝說明](../Setup/Installation-Git.md) 安裝 [Evennia](https://www.evennia.com)。不同之處在於，您應該這樣做，而不是從上游Evennia克隆

    git clone https://github.com/TehomCD/evennia.git
    
這是因為 Arx 使用 TehomCD 的較舊 Evennia 0.8 [fork](https://github.com/TehomCD/evennia)，特別是仍然使用 Python2。如果引用較新的 Evennia 文件，此細節很重要。

如果您是 Evennia 的新手，*強烈*建議您完整執行正常的安裝說明 - 包括初始化和啟動新的空遊戲並連線到它。
這樣您就可以確保 Evennia 作為基準正確工作。

安裝後，`virtualenv` 應該正在執行，並且您的預留資料夾中應該有以下檔案結構：

```
muddev/
   vienv/
   evennia/
   mygame/
```

這裡`mygame`是您在Evennia安裝期間建立的空遊戲，帶有`evennia --init`。前往
然後執行`evennia stop`以確保你的空遊戲沒有執行。我們會讓 Evenna
執行 Arx，所以原則上你可以刪除 `mygame` - 但擁有一個乾淨的遊戲也可能很好
來比較。

(installing-arxcode)=
## 安裝 Arxcode

`cd` 到目錄的根目錄並從 github 克隆已發布的原始碼：

    git clone https://github.com/Arx-Game/arxcode.git myarx

新資料夾 `myarx` 應該會出現在您已有的資料夾旁邊。您可以將其重新命名為
如果你想要別的東西。

`cd` 變為 `myarx`。如果您想了解遊戲目錄的結構，您可以[在此處閱讀更多相關資訊](Beginner-Tutorial/Part1/Beginner-Tutorial-Gamedir-Overview.md)。

(clean-up-settings)=
### 清理設定

Arx 已將 evennia 的正常設定拆分為 `base_settings.py` 和 `production_settings.py`。它
還有自己的解決方案來管理設定檔案的“秘密”部分。我們將保留大部分 Arx
方式，但我們將刪除秘密處理並將其替換為正常的 Evennia 方法。

`cd` 到 `myarx/server/conf/` 並在文字編輯器中開啟檔案 `settings.py`。頂部部分（內
`"""..."""`) 只是幫助文字。擦掉下面的所有東西，讓它看起來像這樣
（不要忘記儲存）：

```
from base_settings import *

TELNET_PORTS = [4000]
SERVERNAME = "MyArx"
GAME_SLOGAN = "The cool game"

try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
```

> 注意：縮排和大小寫在 Python 中很重要。為了您自己的理智，請縮排 4 個空格（而不是製表符）。如果您想要 Evennia 中的 Python 初學者，[您可以檢視此處](Beginner-Tutorial-Python-basic- introduction)。

這將匯入 Arx 的基本設定並使用 Evennia-預設 telnet 連線埠覆蓋它們，並為遊戲命名。此口號會變更網站標題中遊戲名稱下顯示的子文字。您可以稍後根據自己的喜好調整這些。

接下來，在與 `settings.py` 檔案相同的位置建立新的空白檔案 `secret_settings.py`。
這可以只包含以下內容：

```python
SECRET_KEY = "sefsefiwwj3 jnwidufhjw4545_oifej whewiu hwejfpoiwjrpw09&4er43233fwefwfw"

```

將長隨機字串替換為您自己的隨機 ASCII 字元。不應共享金鑰。

接下來，在文字編輯器中開啟 `myarx/server/conf/base_settings.py`。我們想要刪除/註解掉所有提及 `decouple` 套件的內容，Evennia 不使用該套件（我們使用 `private_settings.py` 來隱藏不應共享的設定）。

透過在行開頭新增 `#` 註解掉 `from decouple import config`：`# from decouple import config`。然後在檔案中搜尋 `config(` 並註解掉所有使用它的行。其中許多是特定於原始 Arx 執行的伺服器環境的，因此與我們無關。

(install-arx-dependencies)=
### 安裝Arx依賴項

除了普通的 Evennia 之外，Arx 還有一些進一步的依賴項。從 `cd`: 開始到你的根目錄
`myarx` 資料夾。

> 如果您執行 *Linux* 或 *Mac*：編輯 `myarx/requirements.txt` 並註解掉該行
> `pypiwin32==219` - 僅在 Windows 上需要，在其他平臺上會發生錯誤。

確保您的 `virtualenv` 處於活動狀態，然後執行

    pip install -r requirements.txt

將為您安裝所需的 Python 套件。

(adding-logs-folder)=
### 新增日誌/資料夾

Arx 儲存庫不包含 `myarx/server/logs/` 資料夾 Evennia 期望用於儲存伺服器
日誌。新增起來很簡單：

    # linux/mac
    mkdir server/logs
    # windows
    mkdir server\logs

(setting-up-the-database-and-starting)=
### 設定資料庫並啟動

從 `myarx` 資料夾中，執行

    evennia migrate

這將建立資料庫並將逐步完成所需的所有資料庫遷移。

    evennia start

如果一切順利，Evennia 現在將啟動，執行 Arx！您可以使用 Telnet 使用者端在 `localhost`（或 `127.0.0.1`，如果您的平臺沒有別名 `localhost`）、連線埠 `4000` 上連線到它。或者，您可以使用網頁瀏覽器瀏覽至 `http://localhost:4001` 以檢視遊戲的網站並造訪網頁使用者端。

當您登入時，您將收到標準的 Evennia 問候語（因為資料庫為空），但您可以
嘗試 `help` 看看確實是 Arx 在執行。

(additional-setup-steps)=
### 附加設定步驟

使用上述`evennia migrate`步驟建立資料庫後第一次啟動Evennia時，
它應該為您建立一些起始物件 - 您的超級使用者帳戶，它會提示您
進入，一個起始房間（地獄邊境）和一個角色物件。如果由於某種原因這沒有
發生這種情況，您可能需要按照以下步驟操作。  第一次超級使用者登入時，您可能必須
執行步驟 7-8 和 10 建立並連線到您傳入的角色。

1. 使用您的超級使用者帳號登入遊戲網站。
2. 按 `Admin` 按鈕進入（Django-）管理介面。
3. 導航至 `Accounts` 部分。
4. 新增以新員工命名的新帳戶。使用佔位符密碼和虛擬電子郵件
地址。
5. 將帳戶標記為 `Staff` 並套用 `Admin` 許可權群組（這假設您已經在 Django 中設定了管理群組）。
6. 新增名為 `player` 和 `developer` 的 Tags。
7. 使用您的超級使用者帳號使用 Web 使用者端（或第三方 Telnet 使用者端）登入遊戲。移動到您希望新員工角色出現的位置。
8. 在遊戲使用者端中，執行 `@create/drop <staffername>:typeclasses.characters.Character`，其中 `<staffername>` 通常與您之前在管理員中建立的 Staffer 帳戶使用的名稱相同（如果您要為超級使用者建立角色，請使用您的超級使用者帳戶名稱）。這將建立一個新的遊戲角色並將其放置在您當前的位置。
9. 讓新的管理員玩家登入遊戲。
10. 讓新管理員用 `@ic StafferName` 操縱角色。
11. 讓新管理員更改其密碼 - `@password <old password> = <new password>`。

現在您已經有了一個角色和一個帳戶物件，為了讓某些指令正常執行，您可能還需要執行一些其他操作。您可以在`ic`（控制您的角色物件）時將這些作為遊戲內指令執行。

    py from web.character.models import RosterEntry;RosterEntry.objects.create(player=self.player, character=self)

    py from world.dominion.models import PlayerOrNpc, AssetOwner;dompc = PlayerOrNpc.objects.create(player=self.player);AssetOwner.objects.create(player=dompc)

這些步驟將為您提供「RosterEntry」、「PlayerOrNpc」和「AssetOwner」物件。 RosterEntry
即使在離線狀態下，也將角色和帳戶物件明確連線在一起，並且包含
有關角色目前在遊戲中的存在的附加資訊（例如他們屬於哪個「名單」）
中，如果您選擇使用活躍的角色名冊）。 PlayerOrNpc 是更多的角色擴充套件，以及對遊戲中不存在且僅由角色家庭的螢幕外成員的名稱代表的 NPC 的支援。它還允許成為組織的成員。 AssetOwner 儲存有關角色或組織的金錢和資源的資訊。

(alternate-windows-install-guide)=
## 備用 Windows 安裝指南

_由帕克斯貢獻_

如果您因為某些原因無法使用適用於 Linux 的 Windows 子系統（將使用與上述相同的指令），則可以在 Anaconda for Windows 下執行 Evennia/Arx。這個過程有點棘手。

確保您有：
 * 適用於 Windows 的 Git https://git-scm.com/download/win
 * 適用於 Windows 的 Anaconda https://www.anaconda.com/distribution/
 * VC++ Python 2.7 編譯器 https://aka.ms/vcpython27

    conda update conda
    conda create -n arx python=2.7
    source activate arx

為事物設定一個方便的儲存位置。

    cd ~
    mkdir Source
    cd Source
    mkdir Arx
    cd Arx

將下面的 SSH git clone 連結替換為您自己的 github 分支。
如果您根本不打算更改 Evennia，則可以使用
evennia/evennia.git 儲存庫而不是分叉的儲存庫。

    git clone git@github.com:<youruser>/evennia.git
    git clone git@github.com:<youruser>/arxcode.git

Evennia 本身就是一個軟體包，因此我們要安裝它及其所有內容
先決條件，切換到適當標示的分支後
阿爾克斯程式碼。

    cd evennia
    git checkout tags/v0.7 -b arx-master
    pip install -e .

Arx 有一些自己的依賴項，所以現在我們要安裝它們
由於它不是一個包，我們將使用正常的需求檔案。

    cd ../arxcode
    pip install -r requirements.txt

git 儲存庫不包含空日誌目錄，如果您這樣做，Evennia 會不滿意
沒有它，所以當仍在 arxcode 目錄中時...

    mkdir server/logs

現在點選https://github.com/evennia/evennia/wiki/Arxcode-installing-help並且
更改「清理設定」部分中的設定內容。

然後我們將建立我們的預設資料庫...

    ../evennia/bin/windows/evennia.bat migrate

...並進行第一次執行。您需要 winpty 因為 Windows 沒有 TTY/PTY
 預設情況下，Python 控制檯輸入指令（用於第一個提示）
 run）會失敗，你最終會陷入一個不愉快的境地。未來的跑步，你應該
 不需要winpty。

    winpty ../evennia/bin/windows/evennia.bat start

完成此操作後，您的 Evennia 伺服器應該執行 Arxcode
 在連線埠 4000 的本機上，webserver 位於 http://localhost:4001/.