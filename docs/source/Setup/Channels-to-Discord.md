(connect-evennia-channels-to-discord)=
# 將 Evennia 個頻道連線到 Discord

[Discord](https://discord.com) 是一種受歡迎的聊天服務，尤其是遊戲
社群。如果您的遊戲有 Discord 伺服器，您可以連線它
到您的遊戲內頻道，以便在遊戲內和遊戲外之間進行交流。

(configuring-discord)=
## 設定不和諧

您需要做的第一件事是設定一個 Discord 機器人來連線到您的遊戲。
進入[機器人應用程式](https://discord.com/developers/applications)頁面並建立一個新的應用程式。你將需要
「MESSAGE CONTENT」切換開啟，並將您的機器人代幣新增至您的設定。

```python
# mygame/server/conf/secret_settings.py
DISCORD_BOT_TOKEN = '<your Discord bot token>'
```

如果尚未安裝，您還需要 `pyopenssl` 模組。
將其安裝到您的 Evennia python 環境中

    pip install pyopenssl

最後，在您的設定中啟用 Discord

```python
DISCORD_ENABLED = True
```

啟動/重新載入 Evennia 並以特權使用者身分登入。你現在應該有一個新的
可用指令：`discord2chan`。輸入 `help discord2chan` 進行解釋
它的選項。

使用以下指令新增新的頻道連結：

     discord2chan <evennia_channel> = <discord_channel_id>

`evennia_channel` 引數必須是現有 Evennia 頻道的名稱，
`discord_channel_id` 是 Discord 頻道的完整數字 ID。

> 您的機器人需要新增到正確的 Discord 伺服器並有權訪問
> 通道以傳送或接收訊息。此指令NOT驗證
> 你的機器人有 Discord 許可權！

(step-by-step-discord-setup)=
## 逐步 Discord 設定

本節將介紹設定 Discord 的整個過程
逐步連線到您的 Evennia 遊戲。如果您已完成其中任何一項
步驟已經完成，請隨意跳到下一步。

(creating-a-discord-bot-application)=
### 建立 Discord 機器人應用程式

> 您將需要一個活躍的 Discord 帳戶和對 Discord 伺服器的管理員存取許可權
> 以便將 Evennia 連線到它。這假設您已經這樣做了。

確保您已登入 Discord 網站，然後造訪
https://discord.com/developers/applications. 點選“新應用程式”
按鈕，然後輸入新應用程式的名稱 -
您的 Evennia 遊戲的名稱是不錯的選擇。

接下來，您將進入新應用程式的設定頁面。點選“機器人”
在側邊欄選單上，然後選擇“Build-a-Bot”以建立您的機器人帳戶。

**儲存顯示的令牌！ ** 這將是 Discord 允許的 ONLY 時間
您可以看到該令牌 - 如果您遺失了它，則必須重設它。這個令牌是
您的機器人如何確認其身份，因此非常重要。

接下來，將此令牌新增到您的_secret_ 設定中。

```python
# file: mygame/server/conf/secret_settings.py

DISCORD_BOT_TOKEN = '<token>'
```

儲存後，向下滾動機器人頁面一點，找到切換按鈕
“訊息內容意圖”。您需要將其切換為 ON，否則您的機器人不會
能夠閱讀任何人的訊息。

最後，您可以為新的機器人帳戶新增任何其他設定：顯示影象、
顯示暱稱、簡介等。您可以隨時返回並更改這些內容，因此
現在不用太擔心。

(adding-your-bot-to-your-server)=
### 將您的機器人新增到您的伺服器

仍在新應用程式中時，請點選側面選單上的“OAuth2”，然後點選“URL
發電機」。在此頁面上，您將為您的應用程式產生邀請 URL，然後訪問
URL 將其新增至您的伺服器。

在頂部框中，找到 `bot` 的核取方塊並選中它：這將建立第二個
出現許可權框。在該方塊中，您至少要勾選
以下框：

- 閱讀訊息/檢影片道（在「一般許可權」）
- 傳送訊息（在「文字許可權」中）

最後，向下捲動到頁面底部並複製結果 URL。應該
看起來像這樣：

    https://discord.com/api/oauth2/authorize?client_id=55555555555555555&permissions=3072&scope=bot

訪問該連結，選擇用於 Evennia 連線的伺服器，然後確認。

將機器人新增至您的伺服器後，您可以進一步微調許可權
透過通常的 Discord 伺服器管理。

(activating-discord-in-evennia)=
### 啟動 Evennia 中的 Discord

在連線之前，您還需要對 Evennia 遊戲執行兩件事
不和諧。

首先，將 `pyopenssl` 安裝到您的虛擬環境中（如果尚未安裝）。

    pip install pyopenssl

其次，在您的設定檔中啟用 Discord 整合。

```python
# file: server/conf/settings.py
DISCORD_ENABLED = True
```

啟動或重新載入遊戲以應用更改的設定，然後以帳戶身份登入
至少具有 `Developer` 許可權並在 Evennia 上初始化機器人帳戶
`discord2chan` 指令。您應該會收到一條訊息，表明機器人已建立，並且
沒有與 Discord 的活動連結。

(connecting-an-evennia-channel-to-a-discord-channel)=
### 將 Evennia 頻道連線到 Discord 頻道

您將需要 Evennia 頻道的名稱以及 Discord 的頻道 ID
頻道。當您造訪某個頻道時，頻道 ID 是 URL 的最後一部分。

e.g。如果網址是`https://discord.com/channels/55555555555555555/12345678901234567890`
那麼您的頻道 ID 是 `12345678901234567890`

使用以下指令連結兩個通道：

    discord2chan <evennia channel> = <discord channel id>

兩個通道現在應該互相中繼。透過發布來確認這是否有效
evennia 頻道上的訊息，以及 Discord 頻道上的另一個訊息 - 他們應該
兩者都出現在另一端。

> 如果您沒有看到任何來自 Discord 的訊息，請確保您的機器人
> 有權讀取和傳送訊息並且您的應用程式具有
> “訊息內容意圖”標誌設定。

(further-customization)=
### 進一步定製

`discord2chan` 的幫助檔案包含有關如何使用該指令的更多資訊
自訂您轉發的訊息。

但是，對於更複雜的事情，您可以建立自己的子類
`DiscordBot` 並將其新增到您的設定中。

```python
# file: mygame/server/conf/settings.py
# EXAMPLE
DISCORD_BOT_CLASS = 'accounts.bots.DiscordBot'
```

> 如果您已經設定了 Discord 中繼並且想要更改此設定，請確保您
> 要麼刪除 Evennia 中的舊機器人帳戶，要麼更改其 typeclass，否則不會
> 生效。

核心 DiscordBot 帳戶類別已經設定了幾個有用的掛鉤
處理和中繼 Discord 和 Evennia 頻道之間的頻道訊息，
以及（預設未使用）`direct_msg` 鉤子，用於處理傳送到的 DM
Discord 上的機器人。

預設僅處理訊息和伺服器更新，但 Discord 自訂
協議將所有其他未處理的排程資料傳遞到 Evennia 機器人帳戶
這樣您就可以自己新增額外的處理。但是，**此整合不是完整的庫**
並且沒有記錄所有可能發生的 Discord 事件。