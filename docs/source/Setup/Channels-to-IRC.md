(connect-evennia-channels-to-irc)=
# 將 Evennia 通道連線到 IRC

[IRC（網路中繼聊天）](https://en.wikipedia.org/wiki/Internet_Relay_Chat) 是長期存在的
許多開源專案使用聊天協定進行即時通訊。透過連線其中之一
Evennia 的 [頻道](../Components/Channels.md) 到 IRC 頻道，您也可以與不在其中的人進行交流
本身就是泥。如果您僅在本地執行 Evennia MUD，您也可以使用 IRC
計算機（您的遊戲不需要向公眾開放）！您所需要的只是網路連線。
對於 IRC 操作，您還需要 [twisted.words](https://twistedmatrix.com/trac/wiki/TwistedWords)。
這可以在許多 Linux 發行版中作為 *python-twisted-words* 套件簡單地使用，或直接使用
可從連結下載。

(configuring-irc)=
## 設定IRC

要設定 IRC，您需要在設定檔中啟動它。

```python
    IRC_ENABLED = True
```

啟動 Evennia 並以特權使用者登入。您現在應該有一個可用的新指令：
`@irc2chan`。該指令的呼叫方式如下：

     @irc2chan[/switches] <evennia_channel> = <ircnetwork> <port> <#irchannel> <botname>

如果您已經知道 IRC 是如何運作的，那麼使用起來應該是不言而喻的。閱讀幫助條目
瞭解更多功能。

(setting-up-irc-step-by-step)=
## 逐步設定IRC

您可以將 IRC 連線到任何 Evennia 頻道（因此您可以將其連線到預設的 *public* 頻道
如果你願意的話），但是為了測試，讓我們設定一個新頻道`irc`。

     @ccreate irc = This is connected to an irc channel!

您將自動加入新頻道。

接下來，我們將建立與外部 IRC 網路和通道的連線。有很多很多IRC
網。 [這裡是一些最大的列表](https://www.irchelp.org/networks/popular.html)
，您選擇的那個並不是非常重要，除非您想連線到特定的
通道（也要確保網路允許「機器人」連線）。

為了進行測試，我們選擇 *Freenode* 網路，`irc.freenode.net`。我們將連線到測試
通道，我們稱之為 *#myevennia-test* （IRC 通道始終以 `#` 開頭）。最好如果你
選擇一個以前不存在的晦澀頻道名稱 - 如果不存在，則會建立它
為了你。

> *不要*連線`#evennia`進行測試和除錯，那是Evennia的官方聊天頻道！
一旦一切正常，歡迎您將遊戲連線到 `#evennia` - 它
可能是獲得幫助和想法的好方法。但如果您這樣做，請在遊戲內頻道開啟的情況下進行
僅適用於您的遊戲管理員和開發人員）。

所需的*連線埠*取決於網路。對於 Freenode，這是 `6667`。

將會發生的情況是，您的 Evennia 伺服器將以普通使用者身分連線到此 IRC 通道。這個
「使用者」（或「機器人」）需要一個名稱，您也必須提供該名稱。我們稱之為「泥機器人」。

要測試機器人是否正確連線，您還需要使用單獨的、
第三方 IRC 客戶端。有數百個這樣的客戶可用。如果您使用 Firefox，
*Chatzilla* 外掛很好而且簡單。 Freenode 也提供自己的網路為基礎的聊天頁面。  一旦你
已連線到網路，加入的指令通常是`/join #channelname`（不要忘記
＃）。

接下來我們將 Evennia 與 IRC 頻道連線。

     @irc2chan irc = irc.freenode.net 6667 #myevennia-test mud-bot

Evennia 現在將建立一個新的 IRC 機器人 `mud-bot` 並將其連線到 IRC 網路和通道
#myevennia。如果您連線到 IRC 頻道，您很快就會看到使用者 *mud-bot* 連線。

在Evennia頻道*irc*寫一些東西。

     irc Hello, World!
    [irc] Anna: Hello, World!

如果您正在使用單獨的 IRC 客戶端檢視 IRC 頻道，您應該會看到出現的文字
在那裡，機器人說：

    mud-bot> [irc] Anna: Hello, World!

在您的IRC客戶端視窗中寫入`Hello!`，它將出現在您的正常頻道中，並標有
您使用的IRC頻道的名稱（此處為#evennia）。

    [irc] Anna@#myevennia-test: Hello!

您的 Evennia 玩家現在可以與外部 IRC 頻道上的使用者聊天！
