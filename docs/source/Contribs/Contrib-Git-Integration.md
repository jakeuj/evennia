(in-game-git-integration)=
# 遊戲內 Git 整合

helpme 的貢獻 (2022)

一個在遊戲中整合 git 精簡版本的模組，讓開發人員可以檢視其 git 狀態、更改分支以及提取本地 mygame 儲存庫和 Evennia 核心的更新程式碼。成功拉取或簽出後，git 指令將重新載入遊戲：可能需要手動重新啟動才能套用某些會影響持久scripts 等的變更。

設定 contrib 後，整合遠端變更就像在遊戲中輸入以下內容一樣簡單：

```
git pull
```

您想要使用的儲存庫（無論是本機 mygame 儲存庫、僅 Evennia core 還是兩者）都必須是 git 目錄，指令才能發揮作用。如果您只想使用它來獲取上游 Evennia 更改，則僅 Evennia 儲存庫需要是 git 儲存庫。 [從這裡開始版本控制。 ](https://www.evennia.com/docs/1.0-dev/Coding/Version-Control.html)

(dependencies)=
## 依賴關係

該套件需要依賴項“gitpython”，這是一個用於
與 git 儲存庫互動。安裝，安裝Evennia最簡單
額外要求：

    pip install evennia[extra]

如果您安裝了`git`，您也可以這樣做

- `cd` 到 Evennia 儲存庫的根目錄。
- `pip install --upgrade -e.[extra]`

(installation)=
## 安裝

該實用程式新增了一系列簡單的“git”指令。將模組匯入到您的指令中並將其新增至您的指令集中以使其可用。

具體來說，在`mygame/commands/default_cmdsets.py`中：

```python
...
from evennia.contrib.utils.git_integration import GitCmdSet   # <---

class CharacterCmdset(default_cmds.Character_CmdSet):
    ...
    def at_cmdset_creation(self):
        ...
        self.add(GitCmdSet)  # <---

```

然後 `reload` 使 git 指令可用。

(usage)=
## 用法

只有當您希望使用的目錄是 git 目錄時，此實用程式才有效。如果不是，系統將提示您在終端機中使用以下指令將目錄啟動為 git 儲存庫：

```
git init
git remote add origin 'link to your repository'
```

預設情況下，git 指令僅適用於具有開發人員及更高許可權的人員。您可以透過覆蓋指令並將其鎖定從「cmd:pperm(Developer)」設定為您選擇的 lock 來變更此設定。

支援的指令有：
* git status：您的 git 儲存庫的概述、哪些檔案已在本機變更以及您正在進行的提交。
* gitbranch：有哪些分支可供您檢視。
* git checkout 'branch'：簽出一個分支。
* git pull：從目前分支中提取最新程式碼。

* 所有這些指令也可與「evennia」一起使用，以提供與 Evennia 目錄相關的相同功能。所以：
* git evennia 狀態
* git evennia 分支
* git evennia 簽出“分支”
* git evennia pull：拉取最新的Evennia程式碼。

(settings-used)=
## 使用的設定

該實用程式使用settings.py 中的現有GAME_DIR 和EVENNIA_DIR 設定。如果您有標準目錄設定，則不需要更改它們，它們應該存在而無需您進行任何設定。


----

<small>此檔案頁面是從`evennia\contrib\utils\git_integration\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
