(beginner-tutorial)=
# 新手教學

```{sidebar} 初學者教程部分
- **[簡介](./Beginner-Tutorial-Overview.md)**
<br>正在設定。
- 第1部分：[我們擁有什麼](Part1/Beginner-Tutorial-Part1-Overview.md)
<br>Evennia 概覽以及如何使用這些工具，包括 Python 簡介。
- 第二部分：[我們想要什麼](Part2/Beginner-Tutorial-Part2-Overview.md)
<br>規劃我們的教程遊戲以及規劃您自己的遊戲時要考慮的事項。
- 第 3 部分：[我們如何實現目標](Part3/Beginner-Tutorial-Part3-Overview.md)
<br>開始著手擴充Evennia來製作你的遊戲。
- 第 4 部分：[使用我們建立的內容](Part4/Beginner-Tutorial-Part4-Overview.md)
<br>建立一個技術演示和世界內容以配合我們的程式碼。
- 第五部分：[向世界展示](Part5/Beginner-Tutorial-Part5-Overview.md)
<br>將我們的新遊戲上線並讓玩家嘗試。
```

歡迎來到Evennia！這個由多部分組成的初學者教程將幫助您起步並開始執行。

您可以選擇看起來有趣的主題，但是，如果您按照本教程進行到底，您將建立自己的小型線上遊戲來與其他人一起玩和分享！

使用右側的選單導覽本教學每個部分的索引。使用每個頁面頂部/右下角的[下一個](Part1/Beginner-Tutorial-Part1-Overview.md)和[上一個](../Howtos-Overview.md)連結在課程之間跳轉。

(things-you-need)=
## 你需要的東西

- 指令列介面
- MUD 使用者端（或網頁瀏覽器）
- 文字編輯器/IDE
- Evennia已安裝並已初始化遊戲目錄

(a-command-line-interface)=
### 指令列介面

您需要知道如何在您的 OS 中找到終端/控制檯。 Evennia 伺服器可以在遊戲中控制，但您實際上需要使用指令列介面才能到達任何地方。以下是一些入門者：

- [不同OS的指令列線上介紹:es](https://tutorial.djangogirls.org/en/intro_to_command_line/)

> 請注意，檔案通常使用正斜線 (`/`) 作為檔案系統路徑。 Windows 使用者應將它們轉換為反斜線 (`\`)。

(a-fresh-game-dir)=
### 新鮮的遊戲目錄？

您應該確保您已成功[安裝了Evennia](../../Setup/Installation.md)。如果您按照說明操作，您將已經建立了一個遊戲目錄。檔案將繼續將此遊戲目錄稱為 `mygame`，因此您可能想要重複使用它或僅針對本教學建立新的目錄 - 這取決於您。

如果您已經有一個遊戲目錄，並且想要一個特定於本教學的新遊戲目錄，請使用 `evennia stop` 指令停止正在執行的伺服器。然後，[初始化一個新的遊戲目錄](../../Setup/Installation.md#initialize-a-new-game)在其他地方（_不是_在之前的遊戲目錄中！）。

(a-mud-client)=
### MUD 使用者端

您可能已經有首選的 MUD 客戶。檢視[支援的客戶端網格](../../Setup/Client-Support-Grid.md)。或者，如果您不喜歡 telnet，您也可以在您首選的瀏覽器中使用 Evennia 的網頁使用者端。

確保您知道如何連線並登入本地執行的 Evennia 伺服器。

> 在本文件中，我們經常互換使用術語「MUD」、「MU」和「MU*」來表示歷史上所有不同形式的基於文字的多人遊戲風格（i.e、MUD、MUX、MUSH、MUCK、MOO 等）。 Evennia 可用於建立任何這些遊戲風格......以及更多！

(a-text-editor-or-ide)=
### 文字編輯器或IDE

您需要一個文字編輯器應用程式來編輯 Python 原始檔。大多數可以編輯和輸出原始文字的東西都應該可以工作（...所以不是 Microsoft Word）。

- [這是一篇總結各種文字編輯器選項的部落格文章](https://www.elegantthemes.com/blog/resources/best-code-editors) - 這些東西每年都沒有太大變化。 Python 的熱門選擇是 PyCharm、VSCode、Atom、Sublime Text 和 Notepad++。 Evennia 在很大程度上是用 VIM 編碼的，但它不適合初學者。

```{important} 使用空格而不是製表符
確保設定您的文字編輯器，以便按“Tab”鍵插入 _4 個空格_ 而不是製表符。因為 Python 能夠識別空格，所以這個簡單的練習將使您的生活變得更加輕鬆。
```

(running-python-commands-outside-game-optional)=
### 在遊戲外執行 python 指令（可選）

本教學主要假設您正在透過遊戲使用者端使用遊戲中的 `py` 指令來試驗 Python。但您也可以在遊戲之外探索 Python 指令。從遊戲目錄資料夾中執行以下指令：

    $ evennia shell

```{sidebar}
`evennia shell` 控制檯可以方便地進行 Python 實驗。但請注意，如果您從 `evennia shell` 操作資料庫物件，則在重新載入伺服器之前，這些變更在遊戲內部將不可見。同樣，在重新啟動之前，`evennia shell` 主機可能看不到遊戲中的變更。作為指導，使用 `evennia shell` 進行測試。不要用它來改變正在執行的遊戲的狀態。初學者教程使用遊戲中的 `py` 指令以避免混淆。
```
這將開啟一個 Evennia/Django 感知的 python shell。你應該使用這個而不是僅僅執行普通的`python`，因為後者不會為你設定Django，並且如果沒有大量額外的設定，你將無法匯入`evennia`。為了獲得更好的體驗，建議您安裝`ipython`程式：

     $ pip install ipython3

如果已安裝，`evennia shell` 指令將自動使用 `ipython`。

---

您現在應該準備好繼續學習[初學者教程的第一部分](Part1/Beginner-Tutorial-Part1-Overview.md)！ （以後，請使用頁面頂部/底部的 `previous | next` 按鈕進行操作。）

<details>

<summary>
點選此處檢視初學者教程所有部分和課程的完整索引。
</summary>

```{toctree}

Part1/Beginner-Tutorial-Part1-Overview
Part2/Beginner-Tutorial-Part2-Overview
Part3/Beginner-Tutorial-Part3-Overview
Part4/Beginner-Tutorial-Part4-Overview
Part5/Beginner-Tutorial-Part5-Overview

```

</details>
