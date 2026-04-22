(webserver)=
# Webserver

當 Evennia 啟動時，它也會啟動自己的基於 Twisted 的 Web 伺服器。的
webserver 負責提供遊戲網站的 html 頁面。它
還可以提供影象和音樂等靜態資源。

webclient 作為 [伺服器](./Portal-And-Server.md) 程式的一部分執行
Evennia。這意味著它可以直接存取修改後的快取物件
在遊戲中，並且不存在使用臨時物件的風險
資料庫中不同步。

webserver 在 Twisted 上執行，旨在用於生產
環境。它利用 Django Web 框架並提供：

- 一個[遊戲網站](./Website.md) - 這是你造訪時看到的
`localhost:4001`。網站的外觀旨在根據您的需求進行定製
  遊戲。登入網站的使用者將自動登入遊戲，如果
  使用 webclient 執行此操作，因為它們共用相同的登入憑證（有
  無法安全地使用 telnet 使用者端進行自動登入）。
- [Web Admin](./Web-Admin.md) 基於 Django Web 管理，讓您
在圖形介面中編輯遊戲資料庫。
- [Webclient](./Webclient.md) 頁面由 webserver 提供服務，但實際
遊戲通訊（傳送/接收資料）由javascript用戶端完成
  在頁面上直接開啟到 Evennia 的 Portal 的 websocket 連線。
- [Evennia REST-API](./Web-API.md) 允許從遊戲外部存取資料庫
（僅當`REST_API_ENABLED=True時）。


(basic-webserver-data-flow)=
## 基本Webserver資料流

1. 使用者在瀏覽器中輸入 URL（或按一下按鈕）。這導致
瀏覽器向伺服器傳送包含 url 路徑的_HTTP 請求_
   （就像 `https://localhost:4001/` 一樣，我們需要考慮的 url 部分
   `/`）。其他可能性是`/admin/`、`/login/`、`/channels/` 等。
2. evennia（透過Django）將使用註冊的正規表示式
在 `urls.py` 檔案中。  這充當 _views_ 的重新路由器，它們是
   能夠處理傳入的常規 Python 函式或可呼叫類
   請求（將這些視為類似於正確的 Evennia 指令
   選擇來處理您的輸入 - 從這個意義上說，檢視就像指令）。在
   在 `/` 的情況下，我們重新路由到處理主索引頁的檢視
   網站。
3. 檢視程式碼將準備網頁所需的所有資料。對於預設的
索引頁面，這意味著收集遊戲統計資料，以便您可以看到有多少
   目前已連線到遊戲等。
4. 接下來檢視將取得_template_。範本是具有特殊屬性的 HTML-文件
'佔位符'tags（通常寫為`{{...}}`或`{%... %}`）。這些
   佔位符允許檢視將動態內容注入 HTML 並使
   根據當前情況自訂的頁面。對於索引頁來說，這意味著
   在 html 頁面的正確位置注入當前玩家計數。這個
   稱為“渲染”模板。結果是一個完整的HTML頁面。
5. （該檢視也可以拉入_form_以類似的方式自訂使用者輸入。）
6. 完成的HTML頁面被打包到_HTTP回應_中並返回到
網路瀏覽器，現在可以顯示頁面了！

(a-note-on-the-webclient)=
### 關於 webclient 的註釋

Web 瀏覽器還可以直接執行程式碼，而無需與伺服器通訊。
該程式碼必須寫入/載入到網頁中，並使用
Javascript 程式語言（沒有辦法解決這個問題，這就是網路
瀏覽器可以理解）。執行 Javascript 是網頁瀏覽器所做的事情，
它獨立於 Evennia 運作。 javascript 的小片段可以是
在頁面上用於讓按鈕做出反應、製作小動畫等
需要伺服器。

對於 [Webclient](./Webclient.md)，Evennia 將載入 Webclient 頁面
如上所述，但頁面隨後啟動負責的 Javascript 程式碼（很多）
用於實際顯示用戶端GUI，允許您調整視窗大小等。

啟動後，webclient 會「打電話回家」並啟動
[websocket](https://en.wikipedia.org/wiki/WebSocket) 連結到 Evennia Portal - 這個
這就是所有資料的交換方式。所以在初始載入之後
webclient 頁，上述序列不會再次發生，直到關閉選項卡並
返回或您在瀏覽器中手動重新載入它。
