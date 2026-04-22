(upgrading-an-existing-installation)=
# 升級現有安裝

這與您已經擁有舊 Evennia 版本中的程式碼有關。如果您是新手，或者還沒有太多程式碼，那麼按照[安裝](./Installation.md) 說明重新開始並手動複製內容可能會更容易。

(evennia-v095-to-10)=
## Evennia v0.9.5 至 1.0+

(upgrading-the-evennia-library)=
### 正在升級 Evennia 庫

在 1.0 之前，所有 Evennia 安裝都是 [Git-installs](./Installation-Git.md)。這些說明假設您已經有克隆的 `evennia` 儲存庫，並使用 virtualenv（最佳實踐）。

- 確保使用遊戲目錄中的 `evennia stop` 完全停止 Evennia 0.9.5。
- `deactivate` 離開您的活動虛擬環境。
- 刪除舊的 virtualenv `evenv` 資料夾，或重新命名它（如果您想繼續使用 0.9.5 一段時間）。
- `cd` 進入您的 `evennia/` 根資料夾（您希望在其中看到 `docs/` 和 `bin/` 目錄以及巢狀的 `evennia/` 資料夾）
- `git pull`
- `git checkout main`（而非用於`0.9.5`的`master`）

從這裡開始，繼續進行 [Git 安裝](./Installation-Git.md)，除了跳過克隆 Evennia（因為您已經擁有儲存庫）。請注意，如果您不需要或不想使用 git 追蹤前緣更改，也不希望能夠幫助為 Evennia 本身做出貢獻，您也可以遵循正常的 [pip install](./Installation.md)。

(upgrading-your-game-dir)=
### 升級你的遊戲目錄

如果您沒有任何想要保留在現有遊戲目錄中的內容，則可以使用正常的[安裝說明](./Installation.md) 啟動一個新遊戲。如果您想保留/轉換現有的遊戲目錄，請繼續以下操作。

- 首先，對您現有的遊戲目錄進行_備份_！如果您使用版本控制，請確保提交目前狀態。
- `cd` 到您現有的基於 0.9.5 的遊戲資料夾（如 `mygame`）。
- 如果您已變更 `mygame/web`，請將資料夾_重新命名_為 `web_0.9.5`。如果您沒有更改任何內容（或沒有任何想要保留的內容），則可以將其完全刪除。
- 將 `evennia/evennia/game_template/web` 複製到 `mygame/`（e.g。使用 `cp -Rf` 或檔案總管）。這個新的 `web` 資料夾_取代舊的資料夾_並且具有非常不同的結構。
- 您可能需要替換/註解掉匯入和對已棄用的 [`django.conf.urls`](https://docs.djangoproject.com/en/4.1/ref/urls/#url) 的呼叫。呼叫它的新方法是[在此處提供](https://docs.djangoproject.com/en/4.0/ref/urls/#django.urls.re_path)。
- 執行 `evennia migrate` - 請注意，在這裡看到一些警告是正常的，即使系統要求您也不要執行 `makemigrations`。
- 執行`evennia start`

如果您在遊戲目錄中進行了大量工作，您可能會發現需要對程式碼進行一些（希望是較小的）更改才能以 Evennia 1.0 開始。一些要點：

- `evennia/contrib/` 資料夾更改了結構 - 現在有分類的子資料夾，因此您必須更新匯入。
- 任何 `web` 變更都需要手動從備份移回 `web/` 的新結構。
- 有關所有更改，請參閱 [Evennia 1.0 更改日誌](../Coding/Changelog.md)。
