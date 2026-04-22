(online-setup)=
# 線上設定

除了取得更新之外，Evennia 無需任何 Internet 連線即可進行開發。然而，在某些時候，您可能希望讓您的遊戲線上可見，無論是作為向公眾開放遊戲的一部分，還是允許其他開發人員或 Beta 測試人員訪問它。

(connecting-to-evennia-over-the-internet)=
## 透過 Internet 連線到 Evennia

從外部存取您的 Evennia 伺服器本身並不困難。任何問題通常都是由於您的電腦、網路或託管服務的各種安全措施造成的。這些通常會（並且正確地）阻止外部存取您電腦上的伺服器，除非您另有說明。

我們將首先展示如何在您自己的本機電腦上託管伺服器。即使你打算
稍後在遠端主機上託管「真正的」遊戲，在本地進行設定是有用的做法。我們涵蓋
本文件後面的遠端託管。

開箱即用，Evennia 使用三個連線埠進行向外通訊。如果您的電腦有防火牆，則應開啟這些埠以進行輸入/輸出通訊（並且只有這些埠，Evennia 使用的其他埠僅是您計算機的內部埠）。

 - `4000`，telnet，用於傳統的 mud 使用者端
 - `4001`、HTTP，用於網站
 - `4002`，websocket，用於網頁客戶端

預設情況下，Evennia 將接受所有介面 (`0.0.0.0`) 上的傳入連線，因此原則上任何知道要使用的連線埠並且擁有您電腦的 IP 位址的人都應該能夠連線到您的遊戲。

```{sidebar} 關閉日誌檢視
如果需要關閉日誌檢視，請使用`Ctrl-C`。僅單獨使用 `evennia --log` 即可再次開始追蹤日誌。
```
 - 確保已安裝 Evennia 並且您已啟動 virtualenv。使用 `evennia start --log` 啟動伺服器。 `--log`（或`-l`）將確保日誌回顯到終端。
 - 確保您可以使用網頁瀏覽器連線到 `http://localhost:4001` 或 `http://127.0.0.1:4001`（兩者是相同的）。您應該獲得 Evennia 網站並能夠在 Web 使用者端中玩遊戲。另請檢查以便您可以與 mud 使用者端連線到主機 `localhost`、連線埠 `4000` 或主機 `127.0.0.1`、連線埠 `4000`。
- [Google 搜尋「我的 ip」](https://www.google.se/search?q=my+ip) 或使用任何線上服務來找出您的「向外」IP 地址。出於我們的目的，假設您的外向 IP 是 `203.0.113.0`。
 - 接下來，透過在瀏覽器中開啟 `http://203.0.113.0:4001` 來嘗試面向外的 IP。如果這有效，那就這樣了！也可以嘗試 telnet，將伺服器設定為 `203.0.113.0`，連線埠設定為 `4000`。然而，它很可能“不起作用”。如果是這樣，請繼續閱讀。
 - 如果您的電腦有防火牆，它可能會阻止我們需要的連線埠（也可能阻止整個 telnet）。如果是這樣，您需要開啟向外的連線埠以進行輸入/輸出通訊。有關如何執行此操作的資訊，請參閱防火牆軟體的手冊/說明。為了測試，您也可以暫時完全關閉防火牆，看看這是否確實是問題所在。
 - 無法連線的另一個常見問題是您使用的是硬體路由器（如 WiFi 路由器）。路由器位於您的電腦和網際網路「之間」。因此，您透過 Google 找到的 IP 是*路由器的* IP，而不是您電腦的IP。要解決此問題，您需要將路由器設定為將其連線埠上獲得的資料「轉送」至 IP 以及位於您的專用網路中的電腦的連線埠。如何執行此操作取決於路由器的品牌；您通常使用普通的網頁瀏覽器對其進行設定。在路由器介面中，尋找“連線埠轉送”或“虛擬伺服器”。如果這不起作用，請嘗試暫時將您的電腦直接連線到 Internet 插座（假設您的電腦有相應的連線埠）。您需要再次檢查您的 IP。如果有效，表示問題出在路由器。

```{note}
如果您需要重新設定路由器，則路由器的面向 Internet 的連線埠*不必*必須與您的電腦（和 Evennia）的連線埠具有相同的編號！例如，您可能想要將 Evennia 的傳出連線埠 4001 連線到傳出路由器連線埠 80 - 這是 HTTP 請求使用且 Web 瀏覽器自動尋找的連線埠 - 如果您這樣做，您可以前往 `http://203.0.113.0` 而無需在末尾新增連線埠。但這會與您透過該路由器執行的任何其他 Web 服務發生衝突。
```

(settings-example)=
### 設定範例

您可以將 Evennia 連線到 Internet，而無需更改您的設定。預設設定易於使用，但不一定是最安全的。您可以在[設定檔](./Settings.md#settings-file) 中自訂您的線上狀態。要讓 Evennia 識別更改的連線埠設定，您必須執行完整的 `evennia reboot` 來重新啟動 Portal 而不僅僅是伺服器元件。

下面是一組簡單設定的範例，大部分使用預設值。 Evennia 將需要存取五個電腦埠，其中三個（僅）應向外界開放。下面我們
繼續假設我們的伺服器位址是`203.0.113.0`。

```python
# in mygame/server/conf/settings.py

SERVERNAME = "MyGame"

# open to the internet: 4000, 4001, 4002
# closed to the internet (internal use): 4005, 4006
TELNET_PORTS = [4000]
WEBSOCKET_CLIENT_PORT = 4002
WEBSERVER_PORTS = [(4001, 4005)]
AMP_PORT = 4006

# This needs to be set to your website address for django or you'll receive a
# CSRF error when trying to log on to the web portal
CSRF_TRUSTED_ORIGINS = ['https://mymudgame.com']

# Optional - security measures limiting interface access
# (don't set these before you know things work without them)
TELNET_INTERFACES = ['203.0.113.0']
WEBSOCKET_CLIENT_INTERFACE = '203.0.113.0'
ALLOWED_HOSTS = [".mymudgame.com"]

# uncomment if you want to lock the server down for maintenance.
# LOCKDOWN_MODE = True

```

請繼續閱讀各個設定的說明。

(telnet)=
### 遠端登入

```python
# Required. Change to whichever outgoing Telnet port(s)
# you are allowed to use on your host.
TELNET_PORTS = [4000]
# Optional for security. Restrict which telnet
# interfaces we should accept. Should be set to your
# outward-facing IP address(es). Default is ´0.0.0.0´
# which accepts all interfaces.
TELNET_INTERFACES = ['0.0.0.0']
```

`TELNET_*` 設定是讓傳統基礎遊戲運作的最重要的設定。您可以使用哪些 IP 位址取決於您的伺服器代管解決方案（請參閱下一節）。有些主機會限制您可以使用的埠，因此請務必檢查。

(web-server)=
### 網路伺服器

```python
# Required. This is a list of tuples
# (outgoing_port, internal_port). Only the outgoing
# port should be open to the world!
# set outgoing port to 80 if you want to run Evennia
# as the only web server on your machine (if available).
WEBSERVER_PORTS = [(4001, 4005)]
# Optional for security. Change this to the IP your
# server can be reached at (normally the same
# as TELNET_INTERFACES)
WEBSERVER_INTERFACES = ['0.0.0.0']
# Optional for security. Protects against
# man-in-the-middle attacks. Change  it to your server's
# IP address or URL when you run a production server.
ALLOWED_HOSTS = ['*']
```

Web 伺服器始終同時設定兩個連線埠。 *傳出*連線埠（`4001` 由
default) 是外部連線可以使用的連線埠。如果您不希望使用者必須指定
連線時的埠，您應該將其設定為 `80` - 但這僅在您未執行時才有效
電腦上的任何其他 Web 伺服器。

*內部*連線埠（預設為 `4005`）由 Evennia 在內部使用，以在
伺服器和Portal。它不應該向外界公開。通常你只需要
更改傳出埠，除非預設內部埠與其他程式衝突。

(web-client)=
### 網頁客戶端

```python
# Required. Change this to the main IP address of your server.
WEBSOCKET_CLIENT_INTERFACE = '0.0.0.0'
# Optional and needed only if using a proxy or similar. Change
# to the IP or address where the client can reach
# your server. The ws:// part is then required. If not given, the client
# will use its host location.
WEBSOCKET_CLIENT_URL = ""
# Required. Change to a free port for the websocket client to reach
# the server on. This will be automatically appended
# to WEBSOCKET_CLIENT_URL by the web client.
WEBSOCKET_CLIENT_PORT = 4002
```

基於 websocket 的 Web 使用者端需要能夠回呼伺服器，並且必須變更這些設定才能找到要尋找的位置。如果找不到伺服器，您將在瀏覽器的控制檯（在瀏覽器的開發工具中）中收到警告，並且使用者端將恢復到AJAX-
相反，基於客戶端，這往往會更慢。

(other-ports)=
### 其他港口

```python
# Optional public facing. Only allows SSL connections (off by default).
SSL_PORTS = [4003]
SSL_INTERFACES = ['0.0.0.0']
# Optional public facing. Only if you allow SSH connections (off by default).
SSH_PORTS = [4004]
SSH_INTERFACES = ['0.0.0.0']
# Required private. You should only change this if there is a clash
# with other services on your host. Should NOT be open to the
# outside world.
AMP_PORT = 4006
```

需要`AMP_PORT` 才能運作，因為這是將Evennia 的[伺服器和Portal](../Components/Portal-And-Server.md) 元件連結在一起的內部連線埠。其他埠是加密埠，可能對自訂協定有用，但在其他情況下不會使用。

(lockdown-mode)=
### 鎖定模式

當您進行測試並檢查設定時，您可能不希望玩家打擾您。
同樣，如果您正在對實時遊戲進行維護，您可能需要將其離線一段時間
解決最終的問題，而不會給人們帶來連結的風險。為此，請停止伺服器
`evennia stop` 並將 `LOCKDOWN_MODE = True` 新增到您的設定檔中。當你啟動伺服器時
同樣，您的遊戲只能從本地主機存取。

(registering-with-the-evennia-game-directory)=
### 正在向Evennia遊戲目錄註冊

一旦您的遊戲上線，您應該確保使用 [Evennia 遊戲索引](http://games.evennia.com/) 註冊它。註冊索引將幫助人們找到您的伺服器，激發對您遊戲的興趣，也可以向人們表明 Evennia 正在被使用。即使您剛開始開發，您也可以這樣做 - 如果您不提供任何 telnet/web 地址，它將顯示為_尚未公開_並且只是一個預告片。如果是這樣，請選擇 _pre-alpha_ 作為開發狀態。

要註冊，請站在您的遊戲目錄中，執行

    evennia connections

並按照說明進行操作。更多詳情請參閱[遊戲索引頁](./Evennia-Game-Index.md)。

(ssl-and-https)=
## SSL 和 HTTPS

SSL 對於網路使用者端來說非常有用。它將保護使用者的憑證和遊戲玩法
如果他們在公共場所，則透過 Web 使用者端進行，並且您的 Websocket 也可以切換到 WSS 以獲得相同的好處。 SSL 證書過去每年都要花錢，但現在有一個程式可以免費頒發證書並提供輔助設定，以使整個過程不那麼痛苦。

與 SSL 代理程式結合使用時可能有用的選項：

```
# See above for the section on Lockdown Mode.
# Useful for a proxy on the public interface connecting to Evennia on localhost.
LOCKDOWN_MODE = True

# Have clients communicate via wss after connecting with https to port 4001.
# Without this, you may get DOMException errors when the browser tries
# to create an insecure websocket from a secure webpage.
WEBSOCKET_CLIENT_URL = "wss://fqdn:4002"
```

(lets-encrypt)=
### 讓我們加密

[Let's Encrypt](https://letsencrypt.org) 是一家憑證授權單位，提供免費憑證以保護網站的HTTPS。若要開始使用 Let's Encrypt 為您的 Web 伺服器頒發證書，請參閱以下連結：

 - [Let's Encrypt - 入門](https://letsencrypt.org/getting-started/)
 - [CertBot客戶端](https://certbot.eff.org/)是一個用於自動取得憑證、使用它並在您的網站上維護它的程式。

此外，在 Freenode 上，請造訪 #letsencrypt 頻道以獲取社群的協助。對於額外的資源，Let's Encrypt 有一個非常活躍的[社群論壇](https://community.letsencrypt.org/)。

[某人設定 Let's Encrypt 的部落格](https://www.digitalocean.com/community/tutorials/how-to-secure-apache-with-let-s-encrypt-on-ubuntu-16-04)

上述所有檔案中唯一缺少的過程是如何透過驗證。這就是 Let's Encrypt 驗證您是否擁有對網域的控制權（不一定是所有權，而是網域驗證 (DV)）的方式。這可以透過在 Web 伺服器上設定特定路徑或透過 DNS 中的 TXT 記錄來完成。您想要做哪一個是個人喜好，但也可以基於您的託管選擇。在受控/cPanel 環境中，您很可能必須使用 DNS 驗證。

(relevant-ssl-proxy-setup-information)=
### 相關 SSL 代理設定訊息

- [Apache webserver 設定](./Config-Apache-Proxy.md)（可選）
- [HAProxy 設定](./Config-HAProxy.md)


(hosting-evennia-from-your-own-computer)=
## 從您自己的電腦託管 Evennia

我們上面展示的是迄今為止最簡單且可能最便宜的選項：在您自己的家用電腦上執行 Evennia。此外，由於 Evennia 是它自己的網頁伺服器，因此您不需要安裝任何額外的東西來擁有網站。

**優點**
- 免費（網路費用和電費除外）。
- 完全控制伺服器和硬體（它就在那裡！）。
- 易於設定。
- 適合快速設定 - e.g。向您的合作者簡要地展示結果。

**缺點**
- 您需要良好的網際網路連線，最好沒有任何上傳/下載限制/費用。
- 如果您想以這種方式執行完整的遊戲，您的電腦需要始終處於開啟狀態。可能會很吵，
如前所述，必須考慮電費。
- 沒有支援或安全 - 如果你的房子被燒毀，你的遊戲也會被燒毀。還有，你就是你自己
負責定期進行備份。
- 如果您不知道如何開啟防火牆或路由器中的埠，則可能沒那麼容易。
- Home IP 號碼通常是動態分配的，因此對於永久線上時間，您需要設定 DNS 以始終重新指向正確的位置（請參閱下文）。 - 您個人應對您的網路連線的任何使用/誤用負責 - 儘管不太可能（但並非不可能），如果執行您的伺服器以某種方式給網路上的其他客戶帶來問題，違反您的 ISP 的服務條款（許多 ISPs 堅持將您升級到業務層連線），或者您是版權所有者採取法律行動的物件，您可能會因此發現您的主要網路。

(setting-up-your-own-machine-as-a-server)=
#### 將您自己的機器設定為伺服器

本頁的[第一部分](./Online-Setup.md#connecting-to-evennia-over-the-internet) 描述如何執行此操作並允許使用者連線到您的電腦/路由器的 IP 位址。

使用像這樣的特定 IP 地址的一個複雜問題是，您的家 IP 可能不再是
一樣。許多ISPs（網際網路服務供應商）為您分配*動態*IP，該值可能會在以下時間發生變化
任何時候。當這種情況發生時，你告訴人們去的IP將毫無價值。還有，那麼長
一串數字不太漂亮，是嗎？難以記憶且不易用於行銷
你的遊戲。您需要的是將其別名為更明智的網域 - 跟隨您的別名
當 IP 發生變化時也是如此。

1. 要設定網域別名，我們建議從以下地址開始使用免費網域：
[FreeDNS](https://freedns.afraid.org/)。一旦您在那裡註冊（免費），您就可以訪問數十個
人們「捐贈」的數千個網域允許您將其用於您自己的子網域。
例如，`strangled.net` 是這些可用域之一。所以將我們的 IP 位址繫結到
`strangled.net` 使用子網域 `evennia` 意味著從此以後可以引導人們訪問
`http://evennia.strangled.net:4001` 滿足他們的遊戲需求 - 更容易記住！
1. 那麼，如果我們的 IP 發生變化，我們如何讓這個新的、漂亮的網域也跟著我們呢？為此我們需要
在我們的電腦上設定一個小程式。每當我們的 ISP 決定更改我們的 IP 時它就會檢查
並告訴FreeDNS。從 FreeDNS:s 主頁可以找到許多替代方案，其中之一是
適用於多個平臺的是 [inadyn](http://www.inatech.eu/inadyn/)。從他們的頁面獲取，或者，
在 Linux 中，透過類似 `apt-get install inadyn` 的方式。
1. 接下來，您在 FreeDNS 上登入您的帳戶並前往
[動態](https://freedns.afraid.org/dynamic/) 頁。您應該有一個子網域清單。點選
`Direct URL` 連結，您將看到一個包含簡訊的頁面。忽略它並檢視 URL
頁面。它應該以很多隨機字母結尾。問號後面的所有內容都是您的
獨特的“雜湊”。複製該字串。
1. 現在，您可以使用以下指令啟動 inadyn (Linux)：

    `inadyn --dyndns_system default@freedns.afraid.org -a <my.domain>,<hash> &`

其中 `<my.domain>` 是 `evennia.strangled.net` ，`<hash>` 是我們複製的數字字串
從FreeDNS開始。 `&` 表示我們在背景執行（在其他操作中可能無效）
系統）。 `inadyn` 此後將每 60 秒檢查一次更改。你應該把`inadyn`
指令字串位於啟動 script 某處，以便每當您的電腦啟動時它就會啟動。

(hosting-evennia-on-a-remote-server)=
## 在遠端伺服器上託管 Evennia

您的普通「網路飯店」可能不足以執行 Evennia。網路飯店通常旨在
一個非常具體的用法 - 提供網頁，最多包含一些動態內容。 「蟒蛇
他們在主頁上提到的“scripts”通常只是為了CGI-如scripts啟動
按他們的webserver。即使它們允許您 shell 存取（因此您可以安裝 Evennia 依賴項
首先），資源使用可能會受到很大限制。執行一個成熟的遊戲
像 Evennia 這樣的伺服器可能會被避開或完全不可能。  如果您不確定，
聯絡您的網路飯店並詢問他們對您執行第三方伺服器的政策
開啟自訂連線埠。

您可能需要尋找的選項是 *shell 帳戶服務*、*VPS:es* 或 *雲
服務*。 「Shell帳戶」服務表示您在伺服器上取得Shell帳戶並且可以登入
像任何普通使用者一樣。相較之下，*VPS*（虛擬私人伺服器）服務通常意味著您
獲得 `root` 存取許可權，但在虛擬機器中。還有*雲端*型別的服務，允許
啟動多個虛擬機器並為您使用的資源付費。

**優點**
- Shell 帳戶/VPS/雲端比一般的網路飯店提供更多的靈活性 - 它能夠
登入遠離家鄉的共享電腦。
- 通常執行 Linux 風格，使其易於安裝Evennia。
- 支援。您無需維護伺服器硬體。如果你的房子被燒毀，至少你的
遊戲保持線上。許多服務保證一定程度的正常運作時間並進行定期備份
為了你。請務必檢查一下，有些提供較低的價格以換取您自己的充分體驗
負責您的資料/備份。
- 通常提供固定域名，因此無需弄亂 IP 地址。
- 可能能夠輕鬆部署 evennia 的 [docker](./Installation-Docker.md) 版本
和/或你的遊戲。

**缺點**
- 可能相當昂貴（比網路飯店貴）。請注意，Evennia 通常需要
至少 100MB RAM，對於大型製作遊戲來說可能更多。
- 對於不習慣 ssh/PuTTy 和 Linux 指令列的使用者來說，Linux 風格可能會感到陌生。
- 您可能與許多其他人共用伺服器，因此您不能完全負責。 CPU
使用可能會受到限制。另外，如果伺服器人員決定關閉伺服器進行維護，
你別無選擇，只能袖手旁觀（但希望你會提前收到警告）。

(installing-evennia-on-a-remote-server)=
#### 在遠端伺服器上安裝 Evennia

首先，如果您熟悉伺服器基礎設施，可以考慮使用[Docker](Running-Evennia-in-
Docker)將您的遊戲部署到遠端伺服器；它可能會簡化安裝和部署。
如果您對 Docker 映像完全陌生，那麼它們可能會有點令人困惑。

如果不使用 docker，並且假設您知道如何透過 ssh/PuTTy 連線到您的帳戶，您應該
能夠正常按照[安裝快速入門](./Installation.md) 說明進行操作。你只需要Python
並預裝GIT；這些都應該在任何伺服器上都可用（如果沒有，您應該能夠
輕鬆要求安裝它們）。在 VPS 或雲端服務上，您可以自行安裝它們
需要。

如果`virtualenv`不可用且你無法取得它，你可以下載它（它只是一個檔案）
來自[virtualenv pypi](https://pypi.python.org/pypi/virtualenv)。使用 `virtualenv` 你可以
安裝所有內容，實際上不需要進一步的 `root` 存取許可權。連線埠可能是一個問題，
因此，請確保您知道哪些連線埠可供使用，並相應地重新設定 Evennia。

(hosting-options-and-suggestions)=
## 託管選項和建議

要查詢商業解決方案，請瀏覽網頁以查詢“shell 訪問”、“VPS”或“雲端服務”
地區。您可能會在 [Low End Box][7] 上找到「低成本」VPS 託管的有用優惠。相關的
[低端談話][8] 論壇對於檢查許多小型企業提供的健康狀況很有用
「價值」託管，偶爾提供技術建議。

有各種可用的服務。以下是一些國際建議
Evennia使用者：

| 主機名稱       |  型別          |  最低價格  |  評論 |
|---|---| ---| --- |
| [silvren.com][1]   | 空殼帳戶 | 免費 MU*  | 私人愛好提供者，因此不要假裝置份或期望立即支援。若要要求帳戶，請使用 MUD 使用者端連線至 rostdev.mushpark.com、連線埠 4201 並要求「Jarin」。 |
| [數位海洋][2] | VPS | 4 美元/月 | 如果您使用推薦連結https://m.do.co/c/8f64fec2670c，您可以獲得 50 美元的積分 - 如果您這樣做，一旦您擁有足夠長的時間支付 25 美元，我們將獲得該積分作為推薦獎金來幫助 Evennia 的發展。|
| [亞馬遜網路服務][3] | 雲 | ~$5/月/按需 | 前 12 個月免費。全球可用區域。|
| [亞馬遜 Lightsail][9] | 雲 | 5 美元/月 | 第一個月免費。 AWS 的「固定成本」產品。|
| [Azure 應用服務][12] | 雲 | 自由的 | 業餘愛好者的免費套餐，區域有限。 |
| [華為雲][13] | 雲 | 一經請求 | 類似亞馬遜。 12 個月免費套餐，區域有限。 |
| [赫赫][5] | VPS & 雲 | 5 美元/月 | 多個地區。  1GB RAM 伺服器最便宜的是 5 美元/月。 |
| [刻度][6] | 雲 | 3 歐元/月/按需 | EU 總部（巴黎、阿姆斯特丹）。最小選項提供 2GB RAM。 |
| [程式][10] | VPS | 5 美元/月 | 預付一年，免費 1 個月。您可能需要一些使用此選項的伺服器的經驗，因為它們沒有太多支援。|
| [Akami（原Linode）][11] | VPS | 5 美元/月/按需 | 多個地區。最小選項（5 美元/月）提供 1GB RAM。也提供雲端服務。 |
| [創世紀 MUD 託管][4] | 空殼帳戶 | 8 美元/月 | 專用 MUD 主機提供的記憶體非常有限。可能執行非常舊的 Python 版本。 Evennia *至少*需要「豪華」包（50MB RAM），對於製作遊戲來說可能「高很多」。雖然有時會在 MUD 上下文中提及該主機，但「不」建議在 Evennia 中使用此主機。|

*請幫助我們擴充套件此列表。 *

[1]: https://silvren.com
[2]: https://www.digitalocean.com/pricing
[3]: https://aws.amazon.com/pricing/
[4]: https://www.genesismuds.com/
[5]: https://www.heficed.com/
[6]: https://www.scaleway.com/
[7]: https://lowendbox.com/
[8]: https://www.lowendtalk.com
[9]: https://amazonlightsail.com
[10]: https://prgmr.com/
[11]: https://www.linode.com/
[12]: https://azure.microsoft.com/en-us/pricing/details/app-service/windows/
[13]: https://activity.huaweicloud.com/intl/en-us/free_packages/index.html


(cloud9)=
### 雲9

如果您有興趣線上上開發環境 [Cloud9](https://c9.io/) 中執行 Evennia，您
可以使用 Evennia Linux 安裝說明透過正常的線上設定啟動它。的
您需要做的另一件事是更新 `mygame/server/conf/settings.py` 並新增
`WEBSERVER_PORTS = [(8080, 4001)]`。然後，您將可以存取網頁伺服器並執行所有操作
其他一切正常。

請注意，截至 2017 年 12 月，Amazon 將 Cloud9 作為其 AWS 雲端中的服務重新發布
提供的服務。有權享受 1 年 AWS「免費套餐」的新客戶可能會發現它提供
有足夠的資源免費執行 Cloud9 開發環境。
https://aws.amazon.com/cloud9/
