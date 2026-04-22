(connect-evennia-channels-to-grapevine)=
# 將 Evennia 頻道連線到 Grapevine


[Grapevine](https://grapevine.haus) 是 `MU*`*** 遊戲的新聊天網路。由
將遊戲內頻道連線到小道訊息網路，遊戲中的玩家
可以與其他遊戲中的玩家聊天，也可以與非Evennia遊戲中的玩家聊天。

(configuring-grapevine)=
## 設定小道訊息

要使用 Grapevine，您首先需要 `pyopenssl` 模組。將其安裝到您的
Evennia python 環境

    pip install pyopenssl

要設定 Grapevine，您需要在設定檔中啟動它。

```python
    GRAPEVINE_ENABLED = True
```

接下來，在 https://grapevine.haus. 註冊帳戶 登入後，
轉到“設定/設定檔”和“`Games`”子選單。在這裡您註冊您的
透過填寫資訊來建立新遊戲。註冊結束後，您將前往
得到 `Client ID` 和 `Client Secret`。這些不應該被共享。

開啟/建立檔案 `mygame/server/conf/secret_settings.py` 並新增以下內容：

```python
  GRAPEVINE_CLIENT_ID = "<client ID>"
  GRAPEVINE_CLIENT_SECRET = "<client_secret>"
```

您也可以自訂允許連線的 Grapevine 頻道。這個
新增到 `GRAPEVINE_CHANNELS` 設定。您可以檢視哪些頻道可用
前往此處的 Grapevine 線上聊天：https://grapevine.haus/chat.

啟動/重新載入 Evennia 並以特權使用者身分登入。你現在應該有一個新的
可用指令：`@grapevine2chan`。該指令的呼叫方式如下：

     @grapevine2chan[/switches] <evennia_channel> = <grapevine_channel>

這裡，`evennia_channel` 必須是現有 Evennia 通道的名稱，並且
`grapevine_channel` `GRAPEVINE_CHANNELS` 中受支援的通道之一。

> 在撰寫本文時，Grapevine 網路只有兩個通道：
> `testing` 和 `gossip`。 Evennia 預設允許連線到兩者。使用
> `testing` 嘗試連線。

(setting-up-grapevine-step-by-step)=
## 逐步設定 Grapevine

您可以將 Grapevine 連線到任何 Evennia 通道（因此您可以將其連線到
預設的*公共*頻道（如果您願意），但為了測試，讓我們設定一個
新頻道`gw`。

     @ccreate gw = This is connected to an gw channel!

您將自動加入新頻道。

接下來我們將建立與 Grapevine 網路的連線。

     @grapevine2chan gw = gossip

Evennia 現在將建立一個新連線並將其連線到 Grapevine。連線
到https://grapevine.haus/chat進行檢查。


在 Evennia 頻道 *gw* 中寫入一些內容並檢查，以便在
小道訊息聊天。在聊天中寫下回復，小道訊息機器人應該會回顯
將其傳送到您的遊戲頻道。

您的 Evennia 玩家現在可以與外部 Grapevine 頻道上的使用者聊天！
