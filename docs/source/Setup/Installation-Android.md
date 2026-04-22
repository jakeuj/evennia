(installing-on-android)=
# 在安卓上安裝


本頁介紹如何在 Android 手機上安裝和執行 Evennia 伺服器。這將涉及從 Google Play 商店安裝大量第三方程式，因此在開始之前請確保您同意這一點。

```{warning}
Android 安裝是實驗性的，未在更高版本的 Android 上進行測試。 
報告你的發現。
```

(install-termux)=
## 安裝Termux

要做的第一件事是安裝終端模擬器，允許執行「完整」版本的 Linux。請注意，Android 本質上是在 Linux 之上執行的，因此如果您擁有已 root 的手機，則可以跳過此步驟。不過，您「不需要」擁有 root 許可權的手機即可安裝 Evennia。

假設我們沒有root，我們將安裝[Termux](https://play.google.com/store/apps/details?id=com.termux&hl=en)。 Termux 提供了 Linux 必需品的基本安裝，包括 apt 和 Python，並將它們放在可寫入目錄下。它也為我們提供了一個可以輸入指令的終端。預設情況下，Android 不會授予您根資料夾的許可權，因此 Termux 會假裝自己的安裝目錄是根目錄。

Termux 將在首次啟動時為我們設定一個基本系統，但我們需要安裝 Evennia 的一些先決條件。您應該在 Termux 中執行的指令如下所示：

```
$ cat file.txt
```

`$` 符號是您的提示符號 - 執行指令時不要包含它。

(prerequisites)=
## 先決條件

要安裝 Evennia 需要的一些函式庫，即 Pillow 和 Twisted，我們必須先
安裝一些他們依賴的套件。在 Termux 中，執行以下指令
```
$ pkg install -y clang git zlib ndk-sysroot libjpeg-turbo libcrypt python
```

Termux 隨附 Python 3，完美。 Python 3有venv（virtualenv）和pip（Python的模組
安裝程式）內建。

那麼，讓我們來設定虛擬環境。這使得我們安裝的Python套件與系統分離
版本。

```
$ cd
$ python3 -m venv evenv
```

這將建立一個名為 `evenv` 的新資料夾，其中包含新的 python 執行檔。
接下來，讓我們啟動新的 virtualenv。每次你想要處理 Evennia 時，你需要執行
以下指令：

```
$ source evenv/bin/activate
```

您的提示將變更為如下所示：
```
(evenv) $
```
更新 venv 中的更新程式和安裝程式：pip、setuptools 和wheel。
```
python3 -m pip install --upgrade pip setuptools wheel
```

(installing-evennia)=
### 正在安裝Evennia

現在一切就緒，我們準備下載並安裝 Evennia 本身。

神秘的咒語
```
export LDFLAGS="-L/data/data/com.termux/files/usr/lib/"
export CFLAGS="-I/data/data/com.termux/files/usr/include/"
```
（這些告訴 C 編譯器 clang 在建置 Pillow 時在哪裡可以找到 zlib 的位元）

以允許您編輯來源的方式安裝最新的Evennia
```
(evenv) $ pip install --upgrade -e 'git+https://github.com/evennia/evennia#egg=evennia'
```

此步驟可能需要相當長的時間 - 我們正在下載 Evennia 然後安裝它，
建置 Evennia 執行的所有要求。如果您在這一步驟遇到問題，請
請參閱[疑難排解](./Installation-Android.md#troubleshooting)。

您可以使用 `cd $VIRTUAL_ENV/src/evennia` 前往安裝 Evennia 的目錄。 `git grep
（某事）` can be handy, as can `git diff`

(final-steps)=
### 最後步驟

至此，Evennia已安裝到您的手機上！現在您可以繼續原來的操作
[安裝快速入門](./Installation.md) 說明，為了清楚起見，我們在此重複它們。

要開始新遊戲：

```
(evenv) $ evennia --init mygame
(evenv) $ ls
mygame evenv
```

第一次開始遊戲：

```
(evenv) $ cd mygame
(evenv) $ evennia migrate
(evenv) $ evennia start
```

您的遊戲現在應該正在執行！開啟 http://localhost:4001 的 Web 瀏覽器或指向 telnet
使用者端存取 localhost:4000 並使用您建立的使用者登入。

(running-evennia)=
## 正在執行Evennia

當您希望執行 Evennia 時，請進入 Termux 控制檯並確保您已啟用
virtualenv 以及您的遊戲目錄中。然後您可以正常執行 evennia start 。

```
$ cd ~ && source evenv/bin/activate
(evenv) $ cd mygame
(evenv) $ evennia start
```

您可能希望檢視 [Linux 說明](./Installation-Git.md#linux-install) 以瞭解更多資訊。

(caveats)=
## 注意事項

- Android 的作業系統模組不支援某些功能 - 特別是 getloadavg。因此，執行
遊戲中的指令 @server 會丟擲例外。到目前為止，這個問題還沒有解決辦法。
- 正如您所預料的那樣，效能並不令人驚奇。
- Android 在記憶體處理方面相當積極，您可能會發現您的伺服器程式
如果你的手機被徵收重稅，就會被殺死。 Termux 似乎保留了一個通知來阻止這種情況發生。

(troubleshooting)=
## 故障排除

隨著時間的推移和報告錯誤，此部分將被新增到。

無論如何，請嘗試一些步驟：
* 確保您的軟體包是最新的，嘗試執行 `pkg update && pkg upgrade -y`
* 確保您已經安裝了 clang 套件。如果沒有，請嘗試`pkg install clang -y`
* 確保您位於正確的目錄中。 `cd ~/mygame
* 確保您已經取得了 virtualenv 的來源。輸入`cd && source evenv/bin/activate`
* 檢視 shell 是否會啟動：`cd ~/mygame; evennia shell`
* 檢視 ~/mygame/server/logs/ 中的日誌檔案
