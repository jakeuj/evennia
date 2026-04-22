(configuring-haproxy)=
# 設定HAProxy

如今，面向公眾的現代網站應該透過加密提供服務
連線。所以網站的`https:`而不是`http:`
對於 webclient 使用的 websocket 連線，`wss:` 而不是 `ws:`。

原因是安全性 - 它不僅確保使用者最終處於正確的位置
網站（而不是劫持原始地址的欺騙），它會阻止
邪惡的中間人窺探透過網路傳送的資料（如密碼）
電線。

Evennia本身不實現https/wss連線。這是最好的事情
由能夠保持最新安全性的專用工具處理
做法。

所以我們要做的就是在 Evennia 和 的傳出連線埠之間安裝 _proxy_
你的伺服器。  本質上，Evennia 會認為它只在本地執行（在
localhost, IP 127.0.0.1)，而代理程式將透明地將其對應到
「真正的」傳出連線埠並為我們處理HTTPS/WSS。

             Evennia
                |
    (inside-only local IP/ports serving HTTP/WS)
                |
              Proxy
                |
    (outside-visible public IP/ports serving HTTPS/WSS)
                |
             Firewall
                |
             Internet

這些說明假設您執行一個使用 Unix/Linux 的伺服器（如果您
使用遠端託管）並且您擁有該伺服器的 root 存取許可權。

我們需要的零件：

- [HAProxy](https://www.haproxy.org/) - 一個開源代理程式
易於設定和使用。
- [LetsEncrypt](https://letsencrypt.org/getting-started/) 用於提供使用者
建立加密連線所需的憑證。特別是我們將
  使用優秀的[Certbot](https://certbot.eff.org/instructions)程式，
  它使用 LetsEncrypt 自動執行整個證書設定過程。
- `cron` - 所有 Linux/Unix 系統都附帶此選項，並允許自動執行任務
在OS中。

在開始之前，您還需要以下資訊和設定：

- （可選）您的遊戲的主機名稱。這是
您之前必須從_網域註冊商_購買並設定的東西
  用DNS指向您伺服器的IP。為了這個利益
  手冊中，我們假設您的主機名稱是 `my.awesomegame.com`。
- 如果您沒有域名或尚未設定域名，您至少必須
知道您伺服器的 IP 地址。使用 `ifconfig` 或類似的指令查詢此內容
  伺服器內部。如果您使用像 DigitalOcean 這樣的託管服務，您也可以
  在控制檯中找到 Droplet 的 IP 位址。使用它作為主機名
  無處不在。
- 您必須在防火牆中開啟連線埠 80。 This is used by Certbot below to
自動續訂證書。  So you can't really run another webserver alongside
  此設定無需調整。
- You must open port 443 (HTTPS) in your firewall.這將是外部
webserver 連線埠。
- 確保連線埠 4001（內部 webserver 連線埠）在防火牆中_未_開啟
（它通常會預設關閉，除非你明確開啟它
  以前）。
- 在防火牆中開啟連線埠 4002（我們將為內部連線埠使用相同的連線埠號碼）
和外部埠，代理將僅顯示服務 wss 的安全埠）。

(getting-certificates)=
## 取得證書

證書保證您就是您。最簡單的方法是用
[讓加密](https://letsencrypt.org/getting-started/) 和
[Certbot](https://certbot.eff.org/instructions) 程式。 Certbot 有很多
各種作業系統的安裝說明。這是 Debian/Ubuntu 的：

    sudo apt install certbot

確保停止 Evennia 並且沒有使用連線埠 80 的服務正在執行，然後

    sudo certbot certonly --standalone

您將收到一些需要回答的問題，例如要傳送的電子郵件
證書錯誤以及與此一起使用的主機名稱（或 IP，據說）
證書。之後，證書將最終出現在
`/etc/letsencrypt/live/<yourhostname>/*pem`（來自 Ubuntu 的範例）。的
對於我們的目的來說，關鍵檔案是 `fullchain.pem` 和 `privkey.pem`。

Certbot 設定 cron-job/systemd 作業來定期更新憑證。至
檢查這個是否有效，嘗試

```
sudo certbot renew --dry-run

```

該證書一次只有3個月的有效期，因此請務必進行此測試
有效（需要開啟 80 埠）。請查閱 Certbot 頁面以取得更多協助。

我們還沒有完全完成。 HAProxy 期望這兩個檔案是_一個_檔。更多
具體來說我們要去
1. 複製 `privkey.pem` 並將其複製到名為 `<yourhostname>.pem` 的新檔案（例如
`my.awesomegame.com.pem`）
2. 將 `fullchain.pem` 的內容追加到這個新檔案的最後。無空
需要線路。

我們可以透過在文字編輯器中複製和貼上來做到這一點，但以下是如何做到這一點
shell 指令（將範例路徑替換為您自己的路徑）：

    cd /etc/letsencrypt/live/my.awesomegame.com/
    sudo cp privkey.pem my.awesomegame.com.pem
    sudo cat fullchain.pem >> my.awesomegame.com.pem

新的 `my.awesomegame.com.pem` 檔案（或任何你命名的檔案）就是我們想要的
指向下面的 HAProxy 設定。

但這裡有一個問題 - Certbot 將（重新）產生 `fullchain.pem`
在 3 個月的證書到期前幾天自動向我們傳送。
但是HAProxy不會看到這個，因為它正在檢視合併的檔案
仍會附加舊的`fullchain.pem`。

我們將設定一個自動化任務來定期重建 `.pem` 檔案
使用Unix/Linux的`cron`程式。

    crontab -e

編輯器將開啟 crontab 檔案。在底部新增以下內容（全部
在一行上，並將路徑更改為您自己的路徑！）：

    0 5 * * * cd /etc/letsencrypt/live/my.awesomegame.com/ &&
        cp privkey.pem my.awesomegame.com.pem &&
        cat fullchain.pem >> my.awesomegame.com.pem

儲存並關閉編輯器。每天晚上 05:00 (5 AM)，
現在將為您重建`my.awesomegame.com.pem`。自從 Certbot 更新以來
`fullchain.pem` 檔案在證書到期前幾天，這應該
有足夠的時間來確保 HaProxy 永遠不會看到過時的證書。

(installing-and-configuring-haproxy)=
## 安裝與設定HAProxy

安裝 HaProxy 通常很簡單：

    # Debian derivatives (Ubuntu, Mint etc)
    sudo apt install haproxy

    # Redhat derivatives (dnf instead of yum for very recent Fedora distros)
    sudo yum install haproxy

HAProxy 的設定是在單一檔案中完成的。這可以位於任何地方
你喜歡，現在放入你的遊戲目錄並將其命名為`haproxy.cfg`。

這是在 Centos7 和 Ubuntu 上測試的範例。確保將檔案更改為
放入自己的價值觀。

我們在這裡使用 `my.awesomegame.com` 範例，這是埠

- `443` 是標準 SSL 埠
- `4001` 是標準 Evennia webserver 連線埠（防火牆關閉！）
- `4002` 是預設的 Evennia websocket 連線埠（我們使用相同的數字
傳出 wss 埠，因此應在防火牆中開啟）。
- `4000` 是 Evennia 的預設 Telnet 埠，我們透過 HAProxy 進行代理
因此 `7000` 可以用於安全 Telnet 連線。

```shell
# base stuff to set up haproxy
global
    log /dev/log local0
    chroot /var/lib/haproxy
    maxconn  4000
    user  haproxy
    tune.ssl.default-dh-param 2048
    ## uncomment this when everything works
    # daemon
defaults
    mode http
    option forwardfor

# Evennia Specifics
listen evennia-https-website
    bind my.awesomegame.com:443 ssl no-sslv3 no-tlsv10 crt /etc/letsencrypt/live/my.awesomegame.com>/my.awesomegame.com.pem
    server localhost 127.0.0.1:4001
    timeout client 10m
    timeout server 10m
    timeout connect 5m

listen evennia-secure-websocket
    bind my.awesomegame.com:4002 ssl no-sslv3 no-tlsv10 crt /etc/letsencrypt/live/my.awesomegame.com/my.awesomegame.com.pem
    server localhost 127.0.0.1:4002
    timeout client 10m
    timeout server 10m
    timeout connect 5m

listen evennia-secure-telnet
    bind my.awesomegame.com:7000 ssl no-sslv3 no-tlsv10 crt /etc/letsencrypt/live/my.awesomegame.com/my.awesomegame.com.pem
    server localhost 127.0.0.1:4000
    mode tcp
    timeout client 10m
    timeout server 10m
    timeout connect 5m

```

(putting-it-all-together)=
## 把它們放在一起

返回Evennia遊戲目錄並編輯mygame/server/conf/settings.py。新增：

    WEBSERVER_INTERFACES = ['127.0.0.1']
    WEBSOCKET_CLIENT_INTERFACE = '127.0.0.1'

和

    WEBSOCKET_CLIENT_URL="wss://my.awesomegame.com:4002/"

確保完全重新啟動（停止+啟動）evennia：

    evennia reboot


最後啟動代理：

```
sudo haproxy -f /path/to/the/above/haproxy.cfg

```

確保您可以從瀏覽器連線到您的遊戲並且最終
具有 `https://` 頁面並且可以使用 websocket webclient。

一旦一切正常，您可能希望自動啟動代理並在
背景。使用 `Ctrl-C` 停止代理並確保取消註解行 `#
設定檔中的守護程式`。

如果您的伺服器上沒有執行其他代理，您可以複製您的
haproxy.conf 檔案到系統範圍的設定：

    sudo cp /path/to/the/above/haproxy.cfg /etc/haproxy/

代理現在將在重新載入時啟動，您可以使用以下指令控制它

    sudo service haproxy start|stop|restart|status

如果您不想將內容複製到 `/etc/` 您也可以純粹執行 haproxy
透過在伺服器重新啟動時使用 `cron` 執行它來退出當前位置。開啟
再次執行 crontab：

    sudo crontab -e

在檔案末尾新增行：

    @reboot haproxy -f /path/to/the/above/haproxy.cfg

儲存檔案，當您重新啟動時 haproxy 應該會自動啟動
伺服器。接下來只需最後一次手動重新啟動代理程式 - 使用 `daemon`
在設定檔中取消註釋，它現在將作為後臺程式啟動。
