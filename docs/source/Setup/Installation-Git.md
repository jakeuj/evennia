(installing-with-git)=
# 使用 GIT 安裝

這將從其來源安裝並執行 Evennia。如果您想為 Evennia 本身做出貢獻或更輕鬆地探索程式碼，則這是必需的。請參閱基本[安裝](./Installation.md)
庫的快速安裝。如果您執行，請參閱[疑難排解](./Installation-Troubleshooting.md)
陷入麻煩。

```{important}
如果您要從先前版本轉換現有遊戲，請[請參閱此處](./Installation-Upgrade.md)。
```

(summary)=
## 概括

對於不耐煩的人。如果您在邁步時遇到困難，您應該跳到
適用於您的平臺的更詳細說明。

1. 安裝Python和GIT。啟動控制檯/終端。
2. `cd` 到您想要進行開發的某個位置（例如資料夾
Linux 上的 `/home/anna/muddev/` 或 Windows 上個人使用者目錄中的資料夾）。
3. `git clone https://github.com/evennia/evennia.git`（建立了新資料夾`evennia`）
4. `python3.12 -m venv evenv` (Linux/Mac)、`py -3.12 -m venv evenv` (Windows) - 建立新資料夾 `evenv`
5. `source evenv/bin/activate`（Linux、Mac）、`evenv\Scripts\activate`（Windows）
6. `pip install -e evennia`
7. `evennia --init mygame`
8. `cd mygame`
9. `evennia migrate`
10. `evennia start`（確保在詢問時建立超級使用者）

Evennia 現在應該正在執行，您可以透過將 Web 瀏覽器指向它來連線
`http://localhost:4001` 或 MUD telnet 使用者端到 `localhost:4000`（如果您的 OS 不支援，則使用 `127.0.0.1`）
無法辨識`localhost`）。

(virtualenv)=
## 虛擬環境

Python [虛擬環境](https://docs.python.org/3/library/venv.html) 允許您安裝 Evennia 且其所有依賴項都位於自己的獨立小資料夾中，與系統的其餘部分分開。這也意味著您可以在沒有任何額外許可權的情況下進行安裝 - 所有內容都會進入您磁碟機上的資料夾。

使用 virtualenv 是可選的，但強烈建議使用。這不僅是常見的 Python 實踐，它還會使您的生活更輕鬆，並避免與您可能擁有的其他 Python 程式發生衝突。

Python 原生支援 virtualenv：

```{sidebar} 在 Windows 上使用 py
在 Windows 上，使用帶有版本標誌 (e.g.`py -3.12`) 的 `py` 啟動器來選擇正確的 Python 版本。啟動 virtualenv 後，`python` 在所有平臺上的工作方式相同。
```
```bash
python3.12 -m venv evenv   (Linux/Mac)
py -3.12 -m venv evenv     (Windows)
```

這將在目前目錄中建立一個新資料夾 `evenv`。 
像這樣啟用它：

```
source evenv/bin/activate (Linux, Mac)

evenv\Scripts\activate    (Windows Console)

.\evenv\scripts\activate  (Windows PS Shell, 
                           Git Bash etc)
```
文字 `(evenv)` 應出現在提示旁邊，以表示虛擬
環境已啟用。您_不需要_實際位於 `evenv` 資料夾中或附近
環境要活躍。

```{important}
請記住，您需要像這樣（重新）啟動 virtualenv *每次*您
啟動新的終端機/控制檯（或重新啟動電腦）。在此之前，`evennia` 指令將不可用。
```

(linux-install)=
## Linux安裝

對於 Debian 衍生系統（如 Ubuntu、Mint 等），啟動終端並
安裝要求：

```bash
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv python3.12-dev gcc
```
您應該確保在此步驟之後 *不是* 為 `root`，執行為 `root` 是
安全風險。現在建立一個您想要執行所有 Evennia 操作的資料夾
發展：

```bash
mkdir muddev
cd muddev
```

接下來我們取得 Evennia 本身：

```
git clone https://github.com/evennia/evennia.git
```
將出現一個新資料夾 `evennia`，其中包含 Evennia 庫。僅此而已
雖然包含原始碼，但尚未「安裝」。

此時它是可選的，但建議您初始化並啟動 [virtualenv](#virtualenv)。

接下來，安裝 Evennia （系統範圍內，或安裝到您的活動 virtualenv 中）。確保你是站著的
在 mud 目錄樹的頂部（所以你會看到 `evennia/` 資料夾，可能還有 `evenv` virtualenv 資料夾）並執行
```{sidebar} 
`-e ` 表示我們以可編輯模式安裝 evennia。如果您想在 Evennia 本身上進行開發，這表示您對程式碼所做的更改會立即反映在您正在執行的伺服器上（您不必每次進行更改時都重新安裝）。
```
```
pip install -e evennia
```

測試您是否可以執行 `evennia` 指令。

接下來您可以繼續按照常規的[安裝說明](./Installation.md)初始化您的遊戲。


(mac-install)=
## Mac 安裝

Evennia 伺服器是一個終端程式。開啟終端e.g。來自
*應用程式->實用程式->終端機*。如果您不確定它是如何運作的，[這裡是Mac終端機的介紹](https://blog.teamtreehouse.com/introduction-to-the-mac-os-x-command-line)。

* Python 應該已經安裝，但您必須確保它的版本足夠高 - 選擇 3.12。 （[此](https://docs.python-guide.org/en/latest/starting/install/osx/) 討論如何升級它）。
* GIT 可以透過 [git-osx-installer](https://code.google.com/p/git-osx-installer/) 或透過 MacPorts [如此處所述](https://git-scm.com/book/en/Getting-Started-Installing-Git#Installing-on-Mac) 獲得。
* 如果稍後安裝 `Twisted` 時遇到問題，您可能需要安裝 `gcc` 和 Python 標頭。

此後，您將不再需要 `sudo` 或任何更高的許可權來安裝任何內容。

現在建立一個您想要進行所有 Evennia 開發的資料夾：

```
mkdir muddev
cd muddev
```

接下來我們取得 Evennia 本身：

```
git clone https://github.com/evennia/evennia.git
```

將出現一個新資料夾 `evennia`，其中包含 Evennia 庫。雖然它只包含原始程式碼，但它還沒有“安裝”。

此時它是可選的，但建議您初始化並啟動 [virtualenv](#virtualenv)。

接下來，安裝 Evennia （系統範圍內，或安裝到您的活動 virtualenv 中）。確保你是站著的
在 mud 目錄樹的頂部（所以你會看到 `evennia/`，並且可能會看到 `evenv` virtualenv
資料夾）並執行

```
pip install --upgrade pip   # Old pip versions may be an issue on Mac.
pip install --upgrade setuptools   # Ditto concerning Mac issues.
pip install -e evennia
```

測試您是否可以執行 `evennia` 指令。

接下來您可以繼續按照常規的[安裝說明](./Installation.md)初始化您的遊戲。

(windows-install)=
## Windows安裝

> 如果您使用的是 Windows10+，請考慮使用 _Windows Subsystem for Linux_ > ([WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux))。只需使用 Ubuntu 映像設定 WSL 並按照上面的 Linux 安裝說明進行操作即可。

Evennia 伺服器本身就是一個指令列程式。在Windows啟動選單中，啟動*所有程式->附件->指令提示字元*，您將獲得Windows指令列介面。如果您不熟悉的話，這裡是[有關使用 Windows 指令列的眾多教程之一](https://www.bleepingcomputer.com/tutorials/windows-command-prompt-introduction/)。

* [從 Python 首頁](https://www.python.org/downloads/windows/) 安裝 Python。您需要成為 Windows 管理員才能安裝軟體包。取得 Python **3.12** 或更高版本，64 位元版本。使用預設設定；確保安裝了 `py` 啟動器。
* 您還需要取得 [GIT](https://git-scm.com/downloads) 並安裝它。您可以使用預設安裝選項，但當系統要求您“調整您的 PATH 環境”時，您應該選擇第二個選項“從 Windows 指令提示字元使用 Git”，這樣您可以更自由地選擇在何處使用程式。
* 如果由於建置 C 擴充功能失敗而導致安裝 Evennia 時出現問題，則可能需要 [Visual Studio 建置工具](https://aka.ms/vs/16/release/vs_buildtools.exe)。下載並執行安裝程式，按一下 `Individual Components` 選項卡，然後安裝最新的 Windows SDK。
* 您*可能*需要 [pypiwin32](https://pypi.python.org/pypi/pypiwin32) Python 標頭。僅當您遇到問題時才安裝這些。

您可以將 Evennia 安裝在任何您想要的地方。 `cd` 到該位置並建立一個
用於所有 Evennia 開發的新資料夾（我們稱之為 `muddev`）。

```
mkdir muddev
cd muddev
```

> 如果 `cd` 不起作用，您可以使用 `pushd` 來強制更改目錄。

接下來我們取得 Evennia 本身：

```
git clone https://github.com/evennia/evennia.git
```

將出現一個新資料夾 `evennia`，其中包含 Evennia 庫。僅此而已
雖然包含原始碼，但尚未「安裝」。

此時它是可選的，但建議您初始化並啟動 [virtualenv](#virtualenv)。

接下來，安裝 Evennia （系統範圍內，或安裝到 virtualenv 中）。確保你是站著的
在 mud 目錄樹的頂部（因此您在執行 `dir` 指令時會看到 `evennia`，並且可能會看到 `evenv` virtualenv 資料夾）。然後做：

```
pip install -e evennia
```

測試您是否可以在 virtualenv (evenv) 處於活動狀態時在任何地方執行 `evennia` 指令。

接下來您可以繼續按照常規的[安裝說明](./Installation.md)初始化您的遊戲。
