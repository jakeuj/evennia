(security-hints-and-practices)=
# 安全提示和實踐

如今的駭客沒有歧視性，他們的背景從無聊的青少年到國際情報機構。他們的 scripts 和機器人無休止地爬行網路，尋找他們可以闖入的易受攻擊的系統。誰擁有該系統並不重要——它屬於你還是五角大樓並不重要，目標是利用安全性較差的系統，看看可以控製或竊取哪些資源。

如果您正在考慮部署到基於雲端的主機，那麼您對保護應用程式有既得利益——您可能有一張存檔的信用卡，您的主機可以自由地計費。駭客將您的 CPU 與挖掘加密貨幣掛鉤或使您的網路連線飽和以參與殭屍網路或傳送垃圾郵件可能會增加您的託管費用、暫停您的服務或獲取您的地址/網站
已被ISPs列入黑名單。在事件發生後，要消除這種損害可能會是一場艱難的法律或政治鬥爭。
事實。

作為一名即將將 Web 應用程式暴露給現代網際網路威脅環境的開發人員，
以下是一些可以提高 Evennia 安裝安全性的提示。

(know-your-logs)=
## 瞭解您的日誌
如果遇到緊急情況，請檢查您的日誌！預設情況下，它們位於 `server/logs/` 資料夾中。
以下是一些更重要的問題以及您應該關心的原因：

* `http_requests.log` 將顯示針對 Evennia 內建的 webserver (TwistedWeb) 發出了哪些 HTTP 請求。這是檢視人們是否無害地瀏覽您的網站或試圖透過程式碼注入破壞網站的好方法。
* `portal.log`將向您顯示各種與網路相關的資訊。這是檢查遊戲連線是否奇怪或不尋常的型別或數量，或其他與網路相關的問題的好地方 - 例如當使用者報告無法連線時。
* `server.log` 是 MUX 管理員最好的朋友。您可以在這裡找到有關誰試圖透過猜測密碼闖入您的系統、誰建立了哪些物件等資訊。如果您的遊戲無法啟動或崩潰，並且您不知道原因，那麼這是您應該尋找答案的第一個地方。與安全相關的事件以 `[SS]` 為字首，因此當出現問題時，您可能需要特別注意這些事件。

(disable-developmentdebugging-options)=
## 停用開發/偵錯選項

當您第一次建立遊戲時，會設定一些 Evennia/Django 選項，以使問題出現的位置對您來說更加明顯。在將遊戲投入生產之前，應停用這些選項 - 保留它們可能會暴露變數或程式碼，惡意者可以輕鬆濫用這些選項來危害您的環境。

在`server/conf/settings.py`中：

    # Disable Django's debug mode
    DEBUG = False
    # Disable the in-game equivalent
    IN_GAME_ERRORS = False
    # If you've registered a domain name, force Django to check host headers. Otherwise leave this as-is.
    # Note the leading period-- it is not a typo!
    ALLOWED_HOSTS = ['.example.com']

(handle-user-uploaded-images-with-care)=
## 小心處理使用者上傳的影象

如果您決定允許使用者上傳自己的影象以從您的網站提供服務，則必須特別小心。 Django 將讀取檔案頭以確認它是映像（而不是檔案或 zip 檔案），但[程式碼可以注入到映像檔中](https://insinuator.net/2014/05/django-image-validation-vulnerability/) *之後*可以解釋為 HTML 的標頭和/或為攻擊者提供一個可以透過其存取的 Web shell
其他檔案系統資源。

[Django 對如何處理使用者上傳的檔案有更全面的概述](https://docs.djangoproject.com/en/4.1/topics/security/#user-uploaded-content-security)，但是
簡而言之，您應該注意做以下兩件事之一：

* 從*單獨的*網域或CDN（*不是*您已有的網域的子網域！）提供所有使用者上傳的資產。例如，您可能正在瀏覽 `reddit.com`，但請注意，所有使用者提交的影象都是從 `redd.it` 網域提供的。這樣做既有安全性又有效能優勢（網頁伺服器傾向於逐一載入本機資源，而它們會大量請求外部資源）。
* 如果您不想支付第二個網域的費用，不明白這意味著什麼，或者不想被額外的基礎設施所困擾，那麼只需在收到使用者影象後使用影象庫重新處理使用者影象即可。例如，將它們轉換為不同的格式。 *毀掉原來的東西！ *

(disable-the-web-interface-if-you-only-want-telnet)=
## 停用 Web 介面（如果您只需要 telnet）

Web 介面允許訪客檢視資訊頁面以及登入基於瀏覽器的 telnet 使用者端來存取 Evennia。它還提供身份驗證端點，攻擊者可以嘗試驗證被盜的憑證列表，以檢視哪些憑證可能被您的使用者共用。 Django 的安全性很強大，但如果您不想要/不需要這些功能並且完全打算這樣做
要強制您的使用者使用傳統使用者端存取您的遊戲，您可以考慮停用
任一/兩者都可以最大限度地減少您的攻擊面。

在`server/conf/settings.py`中：

    # Disable the Javascript webclient
    WEBCLIENT_ENABLED = False
    # Disable the website altogether
    WEBSERVER_ENABLED = False

(change-your-ssh-port)=
## 更改你的 ssh 埠

自動攻擊通常會針對連線埠 22，因為它是 SSH 流量的標準連線埠。此外，許多公共 WiFi 熱點會阻止連線埠 22 上的 ssh 流量，因此如果您想遠端工作或沒有家庭網路連線，您可能無法從這些位置存取伺服器。

如果您不打算執行網站或使用 TLS 保護網站，您可以透過將 ssh 使用的連線埠變更為 443 來緩解這兩個問題，大多數/所有熱點供應商都假定該連線埠是 HTTPS 流量並允許透過。

(Ubuntu) 在 /etc/ssh/sshd_config 中，更改以下變數：

    # What ports, IPs and protocols we listen for
    Port 443

儲存，關閉，然後執行以下指令：

    sudo service ssh restart

(set-up-a-firewall)=
## 設定防火牆

Ubuntu 使用者可以使用簡單的 ufw 實用程式。其他人都可以使用 iptables。

    # Install ufw (if not already)
    sudo apt-get install ufw

UFW 的預設策略是拒絕一切。我們必須指定允許哪些內容透過防火牆。

    # Allow terminal connections to your game
    sudo ufw allow 4000/tcp
    # Allow browser connections to your website
    sudo ufw allow 4001/tcp

根據 ssh 守護程式正在偵聽的埠，使用接下來兩個指令的 ONE：

    sudo ufw allow 22/tcp
    sudo ufw allow 443/tcp

最後：

    sudo ufw enable

現在唯一開啟的連線埠將是您的管理 ssh 連線埠（無論您選擇哪一個），以及 4000-4001 上的 Evennia。

(use-an-external-webserver-proxy)=
## 使用外部webserver/代理

在 Evennia 伺服器前面部署 _proxy_ 有一些好處；值得注意的是，這意味著您可以從 HTTPS: url（加密）提供 Evennia 網站和 webclient 資料。可以使用任何代理，例如：

    -[HaProxy](./Config-HAProxy.md)
    -[Apache as a proxy](./Config-Apache-Proxy.md)
    - Nginx 
    - etc.