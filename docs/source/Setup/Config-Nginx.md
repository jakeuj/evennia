(configuring-nginx-for-evennia-with-ssl)=
# 為 Evennia 設定 NGINX 和 SSL

[Nginx](https://nginx.org/en/)是代理伺服器；您可以將其放在 Evennia 和外界之間，透過加密連線為您的遊戲提供服務。另一個選擇是[HAProxy](./Config-HAProxy.md)。

> 這是NOT完整的設定指南！它假設您知道如何取得自己的 `Letsencrypt` 證書，您已經安裝了 nginx，並且熟悉 Nginx 設定檔。 **如果您尚未使用 nginx，** 您最好使用[使用 HAProxy 的指南](./Config-HAProxy.md)。

(ssl-on-the-website-and-websocket)=
## SSL 在網站和 websocket 上

網站和 websocket 都應該透過您正常的 HTTPS 連線埠訪問，因此它們應該一起定義。

對於 nginx，這是一個範例設定，使用 Evennia 的預設連線埠：
```
server {
	server_name example.com;

	listen [::]:443 ssl;
	listen 443 ssl;
	ssl_certificate	 /path/to/your/cert/file;
	ssl_certificate_key /path/to/your/cert/key;

	location /ws {
		# The websocket connection
		proxy_pass http://localhost:4002;
		proxy_http_version 1.1;
		# allows the handshake to upgrade the connection
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "Upgrade";
		# forwards the connection IP
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Host $host;
	}

	location / {
		# The main website
		proxy_pass http://localhost:4001;
		proxy_http_version 1.1;
		# forwards the connection IP
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Host $http_host;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

這將透過 `/ws` 位置以及網站的根位置代理 websocket 連線。

對於 Evennia，這裡是一個範例設定設定，將與上述 nginx 設定一起使用，以進入生產伺服器的 `server/conf/secret_settings.py`

> `secret_settings.py` 檔案不包含在 `git` 提交中，並且用於秘密內容。透過將僅用於生產的設定放入此檔案中，您可以繼續使用預設存取點進行本地開發，從而使您的生活更輕鬆。

```python
SERVER_HOSTNAME = "example.com"
# Set the FULL URI for the websocket, including the scheme
WEBSOCKET_CLIENT_URL = "wss://example.com/ws"
# Turn off all external connections
LOCKDOWN_MODE = True
```
這可確保 evennia 使用正確的 URI 進行 Websocket 連線。將 `LOCKDOWN_MODE` 設為 on 還將阻止任何直接到 Evennia 連線埠的外部連線，將其限制為透過 nginx 代理的連線。

(telnet-ssl)=
## 遠端登入SSL

> 這將透過 nginx 代理程式 ALL telnet 存取！如果您希望玩家直接連線到Evennia的telnet連線埠而不是透過nginx，請保留`LOCKDOWN_MODE`關閉並使用不同的SSL實現，例如啟動Evennia的內部telnet SSL連線埠（請參閱[預設設定檔](./Settings-Default.md)中的`settings.SSL_ENABLED`和`settings.SSL_PORTS`）。

如果您只在網站上使用過 nginx，那麼 telnet 會稍微複雜一些。您需要在主設定檔中設定流引數 - e.g。 `/etc/nginx/nginx.conf` - 預設安裝通常不包括。

我們選擇並行 `stream` 的 `http` 結構，將 conf 檔案新增至 `streams-available` 並將它們符號連結到 `streams-enabled`，與其他網站相同。

```
stream {
	include /etc/nginx/conf.streams.d/*.conf;
	include /etc/nginx/streams-enabled/*;
}
```
當然，您需要在與其他 nginx 設定相同的位置建立所需的資料夾：

    $ sudo mkdir conf.streams.d streams-available streams-enabled

telnet 連線的範例設定檔 - 使用任意外部連線埠 `4040` - 將是：
```
server {
	listen [::]:4040 ssl;
	listen 4040 ssl;

	ssl_certificate  /path/to/your/cert/file;
	ssl_certificate_key  /path/to/your/cert/key;

	# connect to Evennia's internal NON-SSL telnet port
	proxy_pass localhost:4000;
	# forwards the connection IP - requires --with-stream-realip-module
	set_real_ip_from $realip_remote_addr:$realip_remote_port
}
```
玩家現在可以使用 telnet+SSL 連線到位於 `example.com:4040` 的伺服器 - 但*不能*連線到 `4000` 的內部連線。

> ***IMPORTANT：使用此設定，預設首頁將為 WRONG。 *** 您將需要更改 `index.html` 範本並更新 telnet 部分（NOT telnet ssl 部分！）以顯示正確的資訊。


(dont-forget)=
## 不要忘記！

`certbot` 會自動為你更新你的證書，但 nginx 在不重新載入的情況下不會看到它們。確保設定每月的 cron 作業來重新載入 nginx 服務，以避免因憑證過期而導致服務中斷。
