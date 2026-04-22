(configuring-an-apache-proxy)=
# 設定 Apache 代理

Evennia有它自己的webserver。通常不應更換它。但是想要使用像 Apache 這樣的外部 webserver 的另一個原因是充當 Evennia webserver 前面的*代理*。使用 TLS（加密）來實現此功能需要本頁末尾介紹的一些額外工作。

```{warning} 可能已經過時了
下面的 Apache 說明可能已過時。如果出現問題，或者您在不同的伺服器上使用 Evennia，請告訴我們。
```

(running-apache-as-a-proxy-in-front-of-evennia)=
## 在 Evennia 前面執行 Apache 作為代理

以下是使用前端代理程式 (Apache HTTP) 執行 Evennia 的步驟，`mod_proxy_http`，
`mod_proxy_wstunnel` 和 `mod_ssl`。 `mod_proxy_http` 和 `mod_proxy_wstunnel` 只是
下面簡稱`mod_proxy`。

(install-mod_ssl)=
### 安裝`mod_ssl`

- *Fedora/RHEL* - Apache HTTP Server 和 `mod_ssl` 在 Fedora 和 RHEL 的標準套件儲存庫中可用：
    ```
    $ dnf install httpd mod_ssl
    or
    $ yum install httpd mod_ssl
    
    ```
- *Ubuntu/Debian* - Apache HTTP Server 和 `mod_sslj`kl 一起安裝在 `apache2` 軟體包中，並在 Ubuntu 和 Debian 的標準軟體包儲存庫中提供。安裝後需啟用`mod_ssl`：
    ```
    $ apt-get update
    $ apt-get install apache2 
    $ a2enmod ssl

    ```

(tls-proxywebsocket-configuration)=
### TLS代理+websocket設定

以下是 Evennia 的範例設定，其中TLS-啟用了 http 和 websocket 代理程式。

(apache-http-server-configuration)=
#### Apache HTTP 伺服器設定

```
<VirtualHost *:80>
  # Always redirect to https/443
  ServerName mud.example.com
  Redirect / https://mud.example.com
</VirtualHost>

<VirtualHost *:443>
  ServerName mud.example.com
  
  SSLEngine On
  
  # Location of certificate and key
  SSLCertificateFile /etc/pki/tls/certs/mud.example.com.crt
  SSLCertificateKeyFile /etc/pki/tls/private/mud.example.com.key
  
  # Use a tool https://www.ssllabs.com/ssltest/ to scan your set after setting up.
  SSLProtocol TLSv1.2
  SSLCipherSuite HIGH:!eNULL:!NULL:!aNULL
  
  # Proxy all websocket traffic to port 4002 in Evennia
  ProxyPass /ws ws://127.0.0.1:4002/
  ProxyPassReverse /ws ws://127.0.0.1:4002/
  
  # Proxy all HTTP traffic to port 4001 in Evennia
  ProxyPass / http://127.0.0.1:4001/
  ProxyPassReverse / http://127.0.0.1:4001/
  
  # Configure separate logging for this Evennia proxy
  ErrorLog logs/evennia_error.log
  CustomLog logs/evennia_access.log combined
</VirtualHost>
```

(evennia-secure-websocket-configuration)=
#### Evennia 安全 websocket 設定

設定 Evennia 時有一個小技巧，以便 websocket 流量能夠由
代理。您必須在 `mymud/server/conf/settings.py` 檔案中設定 `WEBSOCKET_CLIENT_URL` 設定：

```
WEBSOCKET_CLIENT_URL = "wss://external.example.com/ws"
```

上面的設定是客戶端瀏覽器實際使用的設定。請注意，使用 `wss://` 是因為我們的客戶端將透過加密連線進行通訊（「wss」表示基於 SSL/TLS 的 Websocket）。另外，請特別注意 URL 末端的附加路徑 `/ws`。就是這樣
Apache HTTP 伺服器識別出應將特定請求代理到 Evennia 的 websocket
port 但這也應該適用於其他型別的代理人（如 nginx）。


(run-apache-instead-of-the-evennia-webserver)=
## 執行 Apache 而不是 Evennia webserver

```{warning} 不支援也不建議這樣做。
這是因為有人問過這個問題。 webclient 不起作用。它還會在程式外執行，導致競爭條件。這不受直接支援，因此如果您嘗試這樣做，您就得靠自己了。
```

(install-mod_wsgi)=
### 安裝`mod_wsgi`

- *Fedora/RHEL* - Apache HTTP 伺服器和 `mod_wsgi` 在標準​​套件中可用
Fedora 和 RHEL 的儲存庫：
    ```
    $ dnf install httpd mod_wsgi
    or
    $ yum install httpd mod_wsgi
    ```
- *Ubuntu/Debian* - Apache HTTP 伺服器和 `mod_wsgi` 在標準​​套件中可用
Ubuntu 和 Debian 的儲存庫：
   ````
   $ apt-get 更新
   $ apt-get 安裝 apache2 libapache2-mod-wsgi
   ````

(copy-and-modify-the-vhost)=
### 複製並修改VHOST

安裝`mod_wsgi`後，將`evennia/web/utils/evennia_wsgi_apache.conf`檔案複製到您的
apache2 vhosts/sites 資料夾。在 Debian/Ubuntu 上，這是 `/etc/apache2/sites-enabled/`。讓你的
將檔案複製到那裡**之後**進行修改。

閱讀註釋並更改路徑以指向設定中的適當位置。

(restartreload-apache)=
### 重新啟動/重新載入 Apache

更改設定後，您需要重新載入或重新啟動 apache2。

- *Fedora/RHEL/Ubuntu*
    ```
    $ systemctl restart httpd
    ```
- *Ubuntu/Debian*
    ```
    $ systemctl restart apache2
    ```

運氣好的話，您將能夠將瀏覽器指向您設定的網域或子網域
您的虛擬主機並檢視漂亮的預設 Evennia 網頁。如果沒有，請閱讀希望提供資訊的錯誤
訊息和工作從那裡開始。問題可直接傳送至我們的 [Evennia 社群
站點](https://evennia.com)。

(a-note-on-code-reloading)=
### 關於程式碼重新載入的說明

如果您的 `mod_wsgi` 設定為在守護程式模式下執行（Debian 和
Ubuntu），您可以使用 `touch` 指令告訴 `mod_wsgi` 重新載入
`evennia/game/web/utils/apache_wsgi.conf`。當`mod_wsgi`看到檔案修改時間已經
更改後，它將強制重新載入程式碼。對程式碼的任何修改都不會傳播到
您網站的即時例項，直到重新載入。

如果您沒有以守護程式模式執行或想要強制解決該問題，只需重新啟動或重新載入 apache2
應用您的更改。

(further-notes-and-hints)=
### 進一步的註釋和提示：

如果您從 Apache 收到奇怪的（通常是無訊息的）`Permission denied` 錯誤，請確保
您的 `evennia` 目錄位於 webserver 實際可存取的位置。例如，
某些 Linux 發行版可能預設對使用者的 `/home` 具有非常嚴格的存取許可權
目錄。

一位使用者評論說，他們必須將以下內容新增到 Apache 設定中才能正常運作。
尚未證實，但如果出現問題值得嘗試。

    <Directory "/home/<yourname>/evennia/game/web">
                    Options +ExecCGI
                    Allow from all
    </Directory>