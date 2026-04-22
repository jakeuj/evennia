(connect-evennia-channels-to-rss)=
# 將 Evennia 通道連線到 RSS


[RSS](https://en.wikipedia.org/wiki/RSS) 是一種用於輕鬆追蹤網站更新的格式。的
原理很簡單 - 每當網站更新時，都會更新一個小文字檔案。 RSS 讀者可以
然後定期上線，檢查此檔案是否有更新，並讓使用者知道有什麼新內容。

Evennia 允許將任意數量的 RSS 來源連線到任意數量的遊戲內頻道。提要的更新將方便地回顯到頻道。這有許多潛在用途：例如 MUD 可能使用單獨的網站來託管其論壇。透過RSS，當有新貼文釋出時，玩家可以收到通知。另一個例子是讓每個人都知道您更新了您的開發部落格。管理員可能還想透過我們自己的 RSS feed [此處](https://code.google.com/feeds/p/evennia/updates/basic) 追蹤最新的 Evennia 更新。

(configuring-rss)=
## 設定RSS

要使用RSS，首先需要安裝[feedparser](https://code.google.com/p/feedparser/) python
模組。

    pip install feedparser

接下來，透過設定 `RSS_ENABLED=True` 在設定檔中啟動 RSS 支援。

以特權使用者身分啟動/重新載入 Evennia。您現在應該有一個可用的新指令，`@rss2chan`：

     @rss2chan <evennia_channel> = <rss_url>

(setting-up-rss-step-by-step)=
## 逐步設定RSS

您可以將 RSS 連線到任何 Evennia 頻道，但為了進行測試，讓我們設定一個新頻道「rss」。

     @ccreate rss = RSS feeds are echoed to this channel!

讓我們將 Evennia 的程式碼更新來源連線到此通道。 evennia 更新的 RSS url 是
`https://github.com/evennia/evennia/commits/main.atom`，所以讓我們加入：

     @rss2chan rss = https://github.com/evennia/evennia/commits/main.atom

就是這樣，真的。新的 Evennia 更新現在將在頻道中顯示為單行標題和連結。
單獨給出 `@rss2chan` 指令即可顯示所有連線。若要從頻道中刪除提要，
您再次指定連線（使用指令在列表中檢視它）但新增 `/delete`
開關：

     @rss2chan/delete rss = https://github.com/evennia/evennia/commits/main.atom

您可以透過這種方式將任意數量的 RSS feed 連線到頻道。您也可以將它們連線到
與 [Channels-to-IRC](./Channels-to-IRC.md) 相同的頻道也可以將回饋回顯到外部聊天頻道。
