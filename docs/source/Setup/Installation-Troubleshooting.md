(installation-troubleshooting)=
# 安裝故障排除

如果您遇到此處未涵蓋的問題，[請回報](https://github.com/evennia/evennia/issues/new/choose)，以便可以修復該問題或找到解決方法！

伺服器日誌位於`mygame/server/logs/`。要在終端機中輕鬆檢視伺服器日誌，
您可以執行`evennia -l`，或使用`evennia start -l`或`evennia reload -l`啟動/重新載入伺服器。

(check-your-requirements)=
## 檢查您的要求

任何支援Python3.10+的系統都應該可以工作。
- Linux/Unix
- Windows（Win7、Win8、Win10、Win11）
- Mac OSX（建議 >10.5）

- [Python](https://www.python.org)（已測試3.11、3.12、3.13，建議3.13）
- [扭曲](https://twistedmatrix.com) (v24.11+)
    - [ZopeInterface](https://www.zope.org/Products/ZopeInterface) (v3.0+) - 通常包含在 Twisted 包中
    - Linux/Mac 使用者可能需要 `gcc` 和 `python-dev` 軟體套件或同等軟體套件。
    - Windows 使用者需要 [MS Visual C++](https://aka.ms/vs/16/release/vs_buildtools.exe) 和 *也許* [pypiwin32](https://pypi.python.org/pypi/pypiwin32)。
- [Django](https://www.djangoproject.com) (v5.2+)，請注意，最新的開發版本通常未經 Evennia 測試。
- [GIT](https://git-scm.com/) - 如果您想安裝原始程式碼，請使用版本控制軟體（但也可用於追蹤您自己的程式碼）
  -  Mac 使用者可以使用 [git-osx-installer](https://code.google.com/p/git-osx-installer/) 或 [MacPorts 版本](https://git-scm.com/book/en/Getting-Started-Installing-Git#Installing-on-Mac)。

(confusion-of-location-git-installation)=
## 位置混亂（GIT安裝）

在進行[Git安裝](./Installation-Git.md)時，有些人可能會感到困惑，並將Evennia安裝在錯誤的位置。按照說明（並使用 virtualenv）後，資料夾結構應如下所示：

```
muddev/
    evenv/
    evennia/
    mygame/
```

evennia 函式庫程式碼本身位於 `evennia/evennia/` 內部（因此向下兩級）。你不應該改變這個；在 `mygame/` 中完成所有工作。  您的設定檔是 `mygame/server/conf/settings.py`，_parent_ 設定檔是 `evennia/evennia/settings_default.py`。

(virtualenv-setup-fails)=
## Virtualenv 設定失敗

在執行 `python3.x -m venv evenv`（其中 x 是 python3 版本）步驟時，一些使用者報告出現錯誤；像這樣的東西：

    Error: Command '['evenv', '-Im', 'ensurepip', '--upgrade', '--default-pip']'
    returned non-zero exit status 1

您可以透過安裝 `python3.11-venv`（或更高版本）軟體包（或 OS 的等效軟體包）來解決此問題。或者，您可以透過以下方式引導它：

    python3.x -m --without-pip evenv

這應該設定沒有 `pip` 的 virtualenv。啟動新的 virtualenv，然後從其中安裝 pip（一旦 virtualenv 處於活動狀態，您無需指定 python 版本）：

    python -m ensurepip --upgrade

如果失敗了，更糟糕的選擇是嘗試

    curl https://bootstrap.pypa.io/get-pip.py | python3.x    (linux/unix/WSL only)

無論哪種方式，您現在應該能夠繼續安裝。

(localhost-not-found)=
## 找不到本地主機

如果嘗試連線到本地遊戲時 `localhost` 不起作用，請嘗試 `127.0.0.1`，這是相同的事情。

(linux-troubleshooting)=
## Linux 故障排除

- 如果您在安裝 Evennia 時遇到錯誤（尤其是提到的行
未能包含 `Python.h`)，然後嘗試 `sudo apt-get install python3-setuptools python3-dev`。  安裝後，再次運作`pip install -e evennia`。
- 執行 [git install](./Installation-Git.md) 時，某些未更新的 Linux 發行版可能會發生錯誤
關於太舊的 `setuptools` 或丟失的 `functools`。如果是這樣，請更新您的環境
  與`pip install --upgrade pip wheel setuptools`。然後再嘗試`pip install -e evennia`。
- 一位使用者報告 Ubuntu 16 上的一個罕見問題是安裝 Twisted 時出現安裝錯誤； `Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-vnIFTg/twisted/`，有 `distutils.errors.DistutilsError: Could not find suitable distribution for Requirement.parse('incremental>=16.10.1')` 等錯誤。這似乎可以透過簡單地用 `sudo apt-get update && sudo apt-get dist-upgrade` 更新 Ubuntu 來解決。
- Fedora（特別是 Fedora 24）的使用者報告了 `gcc` 錯誤，指出該目錄
儘管 `gcc` 本身已安裝，但 `/usr/lib/rpm/redhat/redhat-hardened-cc1` 丟失。 [
  已確認的解決方法](https://gist.github.com/yograterol/99c8e123afecc828cb8c) 似乎是使用 e.g 安裝 `redhat-rpm-config` 軟體套件。 `sudo dnf install redhat-rpm-config`。
- 一些嘗試在 NTFS 檔案系統上設定 virtualenv 的使用者發現由於不支援符號連結問題而失敗。答案是不要用NTFS（說真的，為什麼要對自己這樣做？）

(mac-troubleshooting)=
## Mac 故障排除

- 一些 Mac 使用者報告無法連線到 `localhost`（i.e。您自己的電腦）。如果是這樣，請嘗試連線到 `127.0.0.1`，這是相同的事情。照常使用 mud 使用者端的連線埠 4000 和 Web 瀏覽器的連線埠 4001。
- 如果在啟動 Evennia 或檢視日誌時收到 `MemoryError`，這可能是由於 sqlite 版本控制問題造成的。 [我們論壇中的一位使用者](https://github.com/evennia/evennia/discussions/2637) 找到了一個可行的解決方案。 [這裡](https://github.com/evennia/evennia/issues/2854) 是解決此問題的另一種變體。 [另一位使用者](https://github.com/evennia/evennia/issues/3704) 也撰寫了此問題的詳細摘要以及故障排除說明。

(windows-troubleshooting)=
## Windows 故障排除

- 如果使用`pip install evennia`安裝並發現`evennia`指令不可用，請執行一次`py -m evennia`。這應該會將 evennia 二進位檔案新增至您的環境。如果失敗，請確保您使用的是 [virtualenv](./Installation-Git.md#virtualenv)。最糟的情況是，您可以在使用 `evennia` 指令的地方繼續使用 `py -m evennia`。
- - 如果安裝後嘗試直接執行 `evennia` 程式時出現 `command not found`，請嘗試關閉 Windows 主機並再次啟動（如果使用的話，請記住重新啟動 virtualenv！）。有時，Windows 未正確更新其環境，`evennia` 僅在新控制檯中可用。
- 如果您安裝了 Python，但 `python` 指令不可用（即使在新控制檯中），那麼您可能錯過了在路徑上安裝 Python。在 Windows Python 安裝程式中，您將獲得要安裝的選項清單。除了這個之外，大多數或所有選項都已預先檢查，您甚至可能需要向下滾動才能看到它。重新安裝 Python 並確保已選取它。 [從 Python 首頁](https://www.python.org/downloads/windows/) 安裝 Python。您需要成為 Windows 管理員才能安裝軟體包。
- 如果您的 MUD 使用者端無法連線到 `localhost:4000`，請嘗試等效的 `127.0.0.1:4000`。 Windows 上的某些 MUD 使用者端似乎無法辨識別名 `localhost`。
- 一些 Windows 使用者在安裝 Twisted「輪子」時遇到錯誤。 Wheel 是 Python 的預編譯二進位套件。出現此錯誤的常見原因是您使用的是 32 位元版本的 Python，但 Twisted 尚未上傳最新的 32 位元輪。解決此問題的最簡單方法是安裝稍舊的 Twisted 版本。因此，如果版本 `22.1` 失敗，請使用 `pip install twisted==22.0` 手動安裝 `22.0`。或者，您可以檢查是否使用 64 位元版本的 Python 並解除安裝任何 32 位元版本。如果是這樣，您必須`deactivate` virtualenv，刪除`evenv` 資料夾並使用新Python 重新建立它。
- 如果您已經完成了 git 安裝，並且您的伺服器不會啟動並出現 `AttributeError: module 'evennia' has no attribute '_init'` 之類的錯誤訊息，則可能是 python 路徑問題。在終端機中，cd 到 `(your python directory)\site-packages` 並執行指令 `echo "C:\absolute\path\to\evennia" > local-vendors.pth`。開啟您最喜歡的 IDE 中建立的檔案，並確保它以 *UTF-8* 編碼儲存，而不是 *UTF-8 以 BOM* 編碼儲存。
- 一些使用者報告了在 Evennia 開發過程中 Windows WSL 和防毒軟體出現的問題。逾時錯誤和無法運作`evennia connections`可能是因為您的防毒軟體幹擾所致。嘗試停用或變更防毒軟體設定。
