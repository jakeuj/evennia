(coding-using-version-control)=
# 使用版本控制進行編碼

[版本控制](https://en.wikipedia.org/wiki/Version_control) 允許您追蹤程式碼的變更。您可以儲存進度的“快照”，這意味著您可以輕鬆地回滾撤消操作。版本控制還可讓您輕鬆地將程式碼備份到線上_儲存庫_，例如 Github。它還允許您與其他人就同一程式碼進行協作，而不會發生衝突或擔心誰更改了什麼。

```{sidebar} 做吧！
_強烈_建議您[將您的遊戲資料夾置於版本控制之下](#putting-your-game-dir-under-version-control)。使用 git 也是為 Evennia 本身做出貢獻的方式。
```

Evennia 使用最常用的版本控制系統 [Git](https://git-scm.com/) 。  有關使用 Git 的其他協助，請參閱[官方 GitHub 檔案](https://help.github.com/articles/set-up-git#platform-all)。

(setting-up-git)=
## 設定 Git

- **Fedora Linux**

        yum install git-core

- **Debian Linux** _（Ubuntu、Linux Mint 等）_

        apt-get install git

- **Windows**：建議使用[Git for Windows](https://gitforwindows.org/)。
- **Mac**：Mac 平臺提供兩種安裝方法，一種透過 MacPorts，您可以在[此處](https://git-scm.com/book/en/Getting-Started-Installing-Git#Installing-on-Mac)找到該方法，或者您可以使用 [Git OSX 安裝程式](https://sourceforge.net/projects/git-osx-installer/)。

> 您可以在[此處](https://git-scm.com/book/en/Getting-Started-Installing-Git)找到詳細的安裝說明。

```{sidebar} Git 使用者暱稱
如果您曾經線上上提供程式碼（或為 Evennia 做出貢獻），那麼閱讀程式碼提交歷史記錄的人將可以看到您的名字。因此，如果您不習慣在網路上使用真實的全名，請在此輸入暱稱（或您的 github 處理程式）。
```
為了避免以後出現常見問題，您需要設定一些設定；首先，您需要告訴 Git 您的使用者名稱，然後是您的電子郵件地址，這樣當您稍後提交程式碼時，您就會得到正確的認可。


1. 設定提交時使用的 git 預設名稱：

        git config --global user.name "Your Name Here"

2. 設定 git 在提交時使用的預設電子郵件：

        git config --global user.email "your_email@example.com"

> 要開始使用 Git，這裡有 [關於它的 YouTube 的精彩討論](https://www.youtube.com/watch?v=1ffBJ4sVUb4#t=1m58s)。它有點長，但它將幫助您理解 GIT 背後的基本思想（這反過來又使其使用起來更加直觀）。

(common-git-commands)=
## 常用 Git 指令

```{sidebar} Git 儲存庫
這只是您指定受版本控制的資料夾的一個奇特名稱。我們會將您的 `mygame` 遊戲資料夾放入這樣的儲存庫中。 Evennia 程式碼也在（單獨的）git 儲存庫中。
```
Git 可以透過GUI 進行控制。但使用基本終端機/控制檯指令通常更容易，因為它可以清楚地表明是否出現問題。

所有這些操作都需要從 _git 儲存庫_ 內部完成。

Git 乍看之下似乎令人畏懼。但在使用 git 時，99% 的時間您都會使用相同的 2-3 個指令。您可以設定 git _aliases_ 讓它們更容易記住。


(git-init)=
### `git init`

這會將磁碟機上的資料夾/目錄初始化為“git 儲存庫”

    git init .

`.` 表示應用於目前目錄。如果您位於 `mygame` 內，這會使您的遊戲目錄變成 git 儲存庫。真的，這就是全部。您只需執行一次此操作。

(git-add)=
### `git add`

    git add <file> 

這告訴 Git 開始_追蹤_版本控制下的檔案。建立新檔案時需要執行此操作。您也可以新增目前目錄中的所有檔案：

    git add . 

或者

    git add *

目前目錄中的所有檔案現在都由 Git 追蹤。您只需為要追蹤的每個檔案執行一次此操作。

(git-commit)=
### `git commit`

    git commit -a -m "This is the initial commit"

這將_提交_您的更改。它儲存目前所有程式碼 (`-a`) 的快照，新增一則訊息 `-m`，以便您知道自己做了什麼。稍後您可以按照給定時間的方式「檢查」您的程式碼。  該訊息是強制性的，如果編寫清晰且描述性的日誌訊息，您稍後會感謝自己。如果您不新增 `-m`，則會開啟一個文字編輯器供您撰寫訊息。

`git commit` 是你會一直使用的東西，所以為它建立一個 _git 別名_ 會很有用：

    git config --global alias.cma 'commit -a -m'

執行後，您可以更簡單地提交，如下所示：

    git cma "This is the initial commit"

更容易記住！

(git-status-git-diff-and-git-log)=
### `git status`、`git diff` 和 `git log`


    git status -s 

這給出了自上次 `git commit` 以來更改的檔案的一小部分 (`-s`)。

    git diff --word-diff`

這準確地顯示了自您上次建立 `git commit` 以來每個檔案中發生的更改。 `--word-diff` 選項意味著它將標記一行中是否有單字發生更改。

    git log

This shows the log of all `commits` done.每個日誌都會向您顯示誰進行了更改、提交訊息和唯一描述該提交的唯一 _hash_ （如 `ba214f12ab12e123...`）。

您可以使用更多選項使 `log` 指令更加簡潔：

    ls=log --pretty=format:%C(green)%h\ %C(yellow)[%ad]%Cred%d\ %Creset%s%Cblue\ [%an] --decorate --date=relative

這會增加色彩和其他奇特的效果（使用 `git help log` 看看它們的意思）。

讓我們加入別名：

    git config --global alias.st 'status -s'
    git config --global alias.df 'diff --word-diff'
    git config --global alias.ls 'log --pretty=format:%C(green)%h\ %C(yellow)[%ad]%Cred%d\ %Creset%s%Cblue\ [%an] --decorate --date=relative'

您現在可以使用更短的

    git st    # short status
    git dif   # diff with word-marking
    git ls    # log with pretty formatting

對於這些有用的功能。

(git-branch-checkout-and-merge)=
### `git branch`、`checkout` 和 `merge`

Git 允許您使用_分支_。這些是您的程式碼可能採用的單獨的開發路徑，彼此完全獨立。您稍後可以將程式碼從一個分支_合併_回另一個分支。 Evennia 的 `main` 和 `develop` 分支就是這樣的例子。

    git branch -b branchaname 

這將建立一個新分支，與您所在的分支完全相同。  它還會將您移至該分支。

    git branch -D branchname 

刪除一個分支。

    git branch 

顯示您的所有分支，標記您目前所在的分支。

    git checkout branchname 

這會檢查另一個分支。只要您位於一個分支中，所有 `git commit`s 就會只將程式碼提交到該分支。

    git checkout .

這會檢查您的_當前分支_，並具有丟棄自上次提交以來的所有更改的效果。這就像是撤銷自上次儲存點以來所做的操作。

    git checkout b2342bc21c124

這會檢查一個特定的_commit_，由您用 `git log` 找到的雜湊值標識。這將開啟一個“臨時分支”，其中的程式碼與您進行此提交時的程式碼相同。例如，您可以使用它來檢查引入錯誤的位置。檢視現有分支以返回正常時間線，或使用 `git branch -b newbranch` 將此程式碼分解到可以繼續工作的新分支。

    git merge branchname

這會將 `branchname` 中的程式碼合併到您目前所在的分支中。如果相同的程式碼在兩個分支中以不同的方式更改，這樣做可能會導致合併衝突。請參閱[如何解決 git 中的合併衝突](https://phoenixnap.com/kb/how-to-resolve-merge-conflicts-in-git) 以獲得更多協助。

(git-glone-git-push-and-git-pull)=
### `git glone`、`git push` 和 `git pull`

所有這些其他指令只處理位於本機儲存庫資料夾中的程式碼。相反，這些指令允許您與 _remote_ 儲存庫交換程式碼 - 通常是線上儲存庫（例如在 github 上）。

> [下一節](#pushing-your-code-online) 描述如何實際設定遠端儲存庫。

    git clone repository/path

這會將遠端儲存庫複製到您的目前位置。如果您使用 [Git 安裝說明](../Setup/Installation-Git.md) 安裝 Evennia，則這就是您用來取得 Evennia 儲存庫的本機副本的方法。

    git pull

複製或以其他方式設定遠端儲存庫後，使用 `git pull` 會將遠端儲存庫與本機儲存庫重新同步。如果您下載的內容與本機變更發生衝突，git 將強制您進行 `git commit` 更改，然後才能繼續 `git pull`。

    git push 

這會將您目前分支的本機變更上傳到遠端儲存庫上的同名分支。為了能夠執行此操作，您必須具有遠端儲存庫的寫入許可權。

(other-git-commands)=
### 其他 git 指令

還有很多其他 git 指令。線上閱讀它們：

    git reflog 

顯示各個 git 操作的雜湊值。這允許您傳回 git 事件歷史記錄本身。


    git reset 
    
強制將分支重置為較早的提交。這可能會丟失一些歷史記錄，所以要小心。

    git grep -n -I -i <query>

在 git 追蹤的所有檔案中快速搜尋短語/文字。對於快速找到東西在哪裡非常有用。設定別名 `git gr`

```
git config --global alias.gr 'grep -n -I -i'
```

(putting-your-game-dir-under-version-control)=
## 將您的遊戲目錄置於版本控制之下

這利用了上一節中列出的 git 指令。

```{sidebar} git 別名
如果您為上一節中建議的指令設定了 git 別名，則可以使用它們！
```

    cd mygame 
    git init . 
    git add *
    git commit -a -m "Initial commit"

    
您的遊戲目錄現在由 git 追蹤。

您會注意到有些檔案沒有被 git 版本控制覆蓋，特別是您的秘密設定檔 (`mygame/server/conf/secret_settings.py`) 和 sqlite3 資料庫檔案 `mygame/server/evennia.db3`。這是故意的，並由檔案 `mygame/.gitignore` 控制。

```{warning}
你不應該*永遠*透過刪除它的條目將你的 sqlite3 資料庫檔案放入 git 中
在`.gitignore`中。 GIT 用於備份您的程式碼，而不是您的資料庫。那樣
謊言是瘋狂的，你很可能會困惑自己。犯一個錯誤或進行本地更改，經過幾次提交和恢復後，您將無法追蹤資料庫中是否存在內容。如果您想備份 SQlite3 資料庫，只需將資料庫檔案複製到安全位置即可。
```

(pushing-your-code-online)=
### 線上推送您的程式碼

到目前為止，您的程式碼僅位於您的私人電腦上。一個好主意是線上備份。最簡單的方法是將其 `git push` 到您自己的遠端儲存庫 GitHub 上。因此，為此您需要一個（免費）Github 帳戶。

如果您不希望您的程式碼公開可見，Github 還允許您設定一個僅對您可見的_private_ 儲存庫。

在 Github 上建立一個新的空白儲存庫。 [Github 在這裡解釋瞭如何](https://help.github.com/articles/create-a-repo/) 。 _不允許_允許它新增README、許可證等，這只會與我們稍後上傳的內容衝突。

```{sidebar} 起源
我們將遠端儲存庫標記為“origin”。這是 git 預設值，表示我們稍後不需要明確指定它。
```

確保您位於本機遊戲目錄（先前已初始化為 git 儲存庫）。

    git remote add origin <github URL>

這告訴 Git 在 `<github URL>` 處有一個遠端儲存庫。請參閱 github 檔案以瞭解要使用哪個 URL。驗證遙控器是否可與 `git remote -v` 搭配使用

現在我們推送到遠端（預設標記為“origin”）：

    git push

根據您設定 github 身份驗證的方式，可能會要求您輸入 github 使用者名稱和密碼。如果您設定了 SSH 身份驗證，則此指令將起作用。

您使用 `git push` 上傳本機更改，以便遠端儲存庫與本機儲存庫同步。如果您使用 Github 編輯器（或協作者推送的程式碼）線上編輯檔案，則可以使用 `git pull` 在另一個方向同步。

(contributing-to-evennia)=
## 貢獻於Evennia

如果您想為 Evennia 做出貢獻，您必須透過_forking_ 來實現 - 在 Github 上製作您自己的 Evennia 儲存庫的遠端副本。為此，您需要一個（免費）Github 帳戶。這樣做與[將你的遊戲目錄置於版本控制之下](#putting-your-game-dir-under-version-control)（你也應該這樣做！）是一個完全獨立的過程。

在[evennia github頁面](https://github.com/evennia/evennia)的右上角，點選「Fork」按鈕：

![叉子按鈕](../_static/images/fork_button.png)

這將在您的 github 帳戶下建立一個新的線上分支 Evennia。

此分叉目前僅存在於網路上。在終端機中，`cd` 到您想要開發的資料夾。此資料夾不應是您的遊戲目錄，也不應是您克隆 Evennia 的位置（如果您使用 [Git 安裝](../Setup/Installation-Git.md)）。

從該目錄執行以下指令：

    git clone https://github.com/yourusername/evennia.git evennia

這會將您的 fork 下載到您的電腦上。它會在您目前的位置建立一個新資料夾 `evennia/`。如果您使用 [Git 安裝](../Setup/Installation-Git.md) 安裝了 Evennia，則此資料夾的內容將與您在安裝期間複製的 `evennia` 資料夾相同。不同之處在於，此儲存庫連線到您的遠端分支，而不是連線到「原始」_upstream_ Evennia。

當我們克隆我們的 fork 時，git 自動設定一個標記為 `origin` 的「遠端儲存庫」指向它。因此，如果我們執行 `git pull` 和 `git push`，我們就會推動分叉。

我們現在想要新增連結到原始 Evennia 儲存庫的第二個遠端儲存庫。我們將這個遠端儲存庫標記為`upstream`：

    cd evennia
    git remote add upstream https://github.com/evennia/evennia.git

如果您還想訪問 Evennia 的 `develop` 分支（前沿開發），請執行以下操作：

    git fetch upstream develop
    git checkout develop

使用

    git checkout main
    git checkout develop

在分支之間切換。

要從上游 Evennia 提取最新版本，只需簽出您想要的分支並執行以下操作

    git pull upstream

```{sidebar} 推上游
除非您對上游 Evennia 儲存庫具有寫入存取許可權，否則您無法執行 `git push upstream`。因此，您不存在意外將自己的程式碼推送到主公共儲存庫的風險。
```

(fixing-an-evennia-bug-or-feature)=
### 修復 Evennia 錯誤或功能

這應該在您的 Evennia 分叉中完成。您應該_始終_在基於您想要改進的 Evennia 分支的_單獨的 git 分支_中執行此操作。

    git checkout main (or develop)
    git branch -b myfixbranch

現在修復任何需要修復的地方。遵守[Evennia程式碼風格](./Evennia-Code-Style.md)。您可以像平常一樣 `git commit` 提交更改。

上游 Evennia 並沒有停滯不前，因此您需要確保您的工作與上游變更保持同步。確保首先提交您的 `myfixbranch` 更改，然後

    git checkout main (or develop)
    git pull upstream 
    git checkout myfixbranch
    git merge main (or develop)

到目前為止，您的 `myfixbranch` 分支僅存在於您的本機電腦上。否
別人可以看到它。

    git push

這將自動在 Evennia 的分叉版本中建立匹配的 `myfixbranch` 並推送到它。在 github 上，您將能夠看到它出現在 `branches` 下拉清單中。您可以根據需要繼續推送到遠端 `myfixbranch`。

一旦您覺得有東西可以分享，您需要[建立拉取請求](https://github.com/evennia/evennia/pulls) (PR)：
這是上游 Evennia 採用並將您的程式碼拉入主儲存庫的正式請求。
1. 點選`New pull request`
2.  選擇`compare across forks`
3. 從 `head repository` 儲存庫的下拉清單中選擇您的分叉。選擇正確的分支到`compare`。
4. 在 Evennia 一側（左側），請確保選擇正確的 `base` 分支：如果您想對 `develop` 分支做出更改，則必須選擇 `develop` 作為 `base`。
5. 然後點選`Create pull request`並在表格中填寫盡可能多的資訊。
6. 可選：儲存 PR 後，您可以進入程式碼（在 github 上）並新增一些每行註解；這可以透過解釋複雜的程式碼或您所做的決定來幫助審閱者。

現在您只需要等待您的程式碼被審核。期望獲得回饋並被要求進行更改、新增更多檔案等。獲得 PR 合併可能需要幾次迭代。

```{sidebar} 並非所有 PR 都可以合併
雖然大多數 PR 都會合併，但 Evennia 無法**保證**您的 PR 程式碼將被視為適合合併到上游 Evennia 中。因此，在您花費大量時間編寫大段程式碼之前，最好先與社群聯絡（儘管修復錯誤始終是安全的選擇！）
```


(troubleshooting)=
## 故障排除

(getting-403-forbidden-access)=
### 取得 403：禁止訪問

一些使用者在其遠端儲存庫的 `git push` 上遇到過這種情況。他們不會被要求提供使用者名稱/密碼（並且沒有設定 ssh 金鑰）。

一些使用者報告，解決方法是在您的主目錄下建立一個檔案 `.netrc` 並在其中新增您的 github 憑證：

```bash
machine github.com
login <my_github_username>
password <my_github_password>
```