(web-client)=
# 網頁用戶端

Evennia 隨附一個 MUD 使用者端，可透過普通 Web 瀏覽器存取。開發過程中你可以嘗試
它在`http://localhost:4001/webclient`。用戶端由幾個部分組成，全部在
`evennia/web`：

`templates/webclient/webclient.html` 和 `templates/webclient/base.html` 是非常簡單的
描述 webclient 佈局的 django html 模板。

`static/webclient/js/evennia.js` 是主要的 evennia javascript 函式庫。這處理所有
Evennia 和用戶端之間透過 websocket 進行通訊，如果瀏覽器無法透過 AJAX/COMET 進行通訊
處理網路套接字。它將使得 Evennia 物件可用於 javascript 名稱空間，這
提供透明地向伺服器傳送資料和從伺服器接收資料的方法。此舉旨在
如果更換 GUI 前端也可以使用。

`static/webclient/js/webclient_gui.js` 是預設的外掛管理器。它新增了 `plugins` 和
`plugin_manager` 物件指向 javascript 名稱空間，協調 GUI 之間的操作
各種外掛，並使用 Evennia 物件庫進行所有輸入/輸出。

`static/webclient/js/plugins` 提供了一組預設的外掛來實現“類似 telnet”
介面和幾個範例外掛來展示如何實現新的外掛功能。

`static/webclient/css/webclient.css`是用戶端的CSS檔案；它也定義瞭諸如如何
顯示 ANSI/Xterm256 顏色等。

伺服器端 webclient 協定位於 `evennia/server/portal/webclient.py` 和
`webclient_ajax.py` 用於兩種型別的連線。您不能（也不應該需要）修改
這些。

(customizing-the-web-client)=
## 自訂 Web 使用者端

就像網站的情況一樣，您可以覆蓋遊戲目錄中的webclient。你需要
在專案的 `mygame/web/` 目錄中的符合目錄位置新增/修改檔案。
這些目錄NOT在遊戲運作時直接被Web伺服器使用，
伺服器將 Evennia 資料夾中與 Web 相關的所有內容複製到 `mygame/server/.static/`，然後
複製所有 `mygame/web/` 檔案。  這可能會導致某些情況，如果您編輯檔案，但它不會
似乎對伺服器的行為有任何影響。  **在做任何其他事情之前，請嘗試關閉
關閉遊戲並從指令列執行`evennia collectstatic`，然後重新啟動，清除
您的瀏覽器快取，然後檢視您的編輯是否顯示。 **

範例：要變更正在使用的外掛程式列表，您需要透過複製覆蓋 base.html
`evennia/web/templates/webclient/base.html` 至
`mygame/web/templates/webclient/base.html` 並編輯它以新增新外掛。

(evennia-web-client-api-from-evenniajs)=
## Evennia Web 使用者端 API（來自 evennia.js）
* `Evennia.init( opts )`
* `Evennia.connect()`
* `Evennia.isConnected()`
* `Evennia.msg( cmdname, args, kwargs, callback )`
* `Evennia.emit( cmdname, args, kwargs )`
* `log()`

(plugin-manager-api-from-webclient_guijs)=
## 外掛程式管理器API（來自webclient_gui.js）
* `options` 物件，儲存可由外掛用來協調行為的鍵/值「狀態」。
* `plugins` 物件，所有已載入外掛的鍵/值列表。
* `plugin_handler` 物件
  * `plugin_handler.add("name", plugin)`
  * `plugin_handler.onSend(string)`

(plugin-callbacks-api)=
## 外掛回呼API
* `init()` -- 唯一需要的回呼
* `boolean onKeydown(event)` 此外掛監聽 Keydown 事件
* `onBeforeUnload()` 這個外掛在 webclient 頁面/選項卡之前做了一些特殊的事情
關閉。
* `onLoggedIn(args, kwargs)` 該外掛程式會在 webclient 首次登入時執行某些操作。
* `onGotOptions(args, kwargs)` 該外掛使用從伺服器傳送的選項執行某些操作。
* `boolean onText(args, kwargs)` 該外掛程式對從伺服器傳送的訊息執行某些操作。
* `boolean onPrompt(args, kwargs)` 當伺服器傳送提示時，該外掛程式會執行某些操作。
* `boolean onUnknownCmd(cmdname, args, kwargs)` 該外掛程式使用「未知指令」執行某些操作。
* `onConnectionClose(args, kwargs)` 當 webclient 斷開連線時，此外掛程式會執行某些操作
伺服器.
* `newstring onSend(string)` 該外掛程式檢查/更改其他外掛程式產生的文字。 **使用
謹慎行事**

`base.html` 中定義的外掛的順序很重要。  每個外掛的所有回撥
將按該順序執行。  上面標記為“布林”的函式必須傳回 true/false。  返回
true 將短路執行，因此 base.html 清單中較低的其他外掛程式不會有
他們對此事件的回撥被呼叫。  這使得諸如上/下箭頭鍵之類的功能成為可能
history.js 外掛始終在 default_in.js 外掛將該鍵新增到當前輸入之前發生
緩衝區。

(exampledefault-plugins-pluginsjs)=
### 範例/預設外掛 (`plugins/*.js`)

* `clienthelp.js` 從 options2 外掛定義 onOptionsUI。  這是一個大部分空的外掛
為您的遊戲新增一些“操作方法”資訊。
* `default_in.js` 定義 onKeydown。 `<enter>` 鍵或滑鼠點選箭頭將傳送目前鍵入的文字。
* `default_out.js` 定義 onText、onPrompt 和 onUnknownCmd。  為使用者產生 HTML 輸出。
* `default_unload.js` 定義 onBeforeUnload。  提示使用者確認他們的意圖
離開/關閉遊戲。
* `font.js` 定義 onOptionsUI。該外掛新增了選擇字型和字型大小的功能。
* `goldenlayout_default_config.js` 實際上不是一個外掛，定義了一個全域變數
Goldenlayout 用於確定其視窗佈局，已知tag路由等。
* `goldenlayout.js` 定義 onKeydown、onText 和自訂函式。  一個非常強大的「選項卡式」視窗管理器，用於拖放視窗、文字路由等。
* `history.js` 定義 onKeydown 和 onSend。建立過去傳送的指令的歷史記錄，並使用箭頭鍵進行細讀。
* `hotbuttons.js` 定義 onGotOptions。一個預設禁用的外掛，定義了一個按鈕欄
使用者可分配的指令。
* `html.js` 一個基本外掛，允許用戶端處理來自伺服器的「原始 html」訊息，這
允許伺服器傳送本機HTML訊息，例如&gt;div style='s'&lt;styled text&gt;/div&lt;
* `iframe.js` 定義 onOptionsUI。  一個僅用於黃金佈局的外掛，用於建立受限瀏覽子
並排 Web/文字介面的視窗，主要是如何建立新的 HTML 的範例
黃金佈局的「元件」。
* `message_routing.js` 定義 onOptionsUI、onText、onKeydown。  這個僅限金色佈局的外掛
實現正規表示式匹配，允許使用者“tag”匹配任意文字，這樣就得到
路由到正確的視窗。與其他用戶端的“Spawn”功能類似。
* `multimedia.js` 一個基本外掛，允許用戶端處理來自伺服器的「影象」、「音訊」和「視訊」訊息並將它們顯示為內聯HTML。
* `notifications.js` 定義 onText。為每個新訊息產生瀏覽器通知事件
當選項卡隱藏時。
* `oob.js` 定義 onSend。允許使用者測試/傳送帶外 json 訊息到伺服器。
* `options.js` 定義大多數回撥。提供基於彈出視窗的 UI 來協調伺服器的選項設定。
* `options2.js` 定義大多數回撥。提供基於 Goldenlayout 的選項/設定選項卡版本。透過自訂 onOptionsUI 回呼與其他外掛程式整合。
* `popups.js` 提供預設彈出視窗/對話方塊 UI 供其他外掛程式使用。
* `text2html.js` 提供新的訊息處理程式型別：`text2html`，類似於多媒體和 html 外掛程式。該外掛提供了一種將常規管道樣式的 ASCII 訊息渲染到用戶端的方法。  這允許伺服器完成更少的工作，同時也允許用戶端有地方自訂此轉換過程。  要使用此外掛，您需要覆蓋 Evennia 中的當前指令，更改生成原始文字輸出訊息的任何位置並將其轉換為 `text2html` 訊息。例如：`target.msg("my text")` 變成：`target.msg(text2html=("my text"))` （更好的是，使用 webclient 窗格路由 tag：`target.msg(text2html=("my text", {"type": "sometag"}))`） `text2html` 訊息的格式和行為應與伺服器端產生的 text2html() 輸出相同。

(a-side-note-on-html-messages-vs-text2html-messages)=
### 關於 html 訊息與 text2html 訊息的旁註

所以...假設您希望讓 webclient 輸出更像標準網頁...
對於 telnet 使用者端，您可以將一堆文字行收集在一起，並帶有 ASCII 格式化邊框等。然後透過 text2html 外掛將結果傳送到用戶端呈現。

但對於 Web 使用者端，您可以直接使用 html 外掛程式格式化訊息，將整個內容呈現為 HTML 表，如下所示：

```
    # Server Side Python Code:

    if target.is_webclient():
        # This can be styled however you like using CSS, just add the CSS file to web/static/webclient/css/...
        table = [
                 "<table>",
                  "<tr><td>1</td><td>2</td><td>3</td></tr>",
                  "<tr><td>4</td><td>5</td><td>6</td></tr>",
                 "</table>"
               ]
        target.msg( html=( "".join(table), {"type": "mytag"}) )
    else:
        # This will use the client to render this as "plain, simple" ASCII text, the same
        #   as if it was rendered server-side via the Portal's text2html() functions
        table = [ 
                "#############",
                "# 1 # 2 # 3 #",
                "#############",
                "# 4 # 5 # 6 #",
                "#############"
               ]
        target.msg( html2html=( "\n".join(table), {"type": "mytag"}) )
```

(writing-your-own-plugins)=
## 編寫自己的外掛

所以，您喜歡 webclient 的功能，但您的遊戲有特定的
需要在視覺上將不同型別的文字分離到自己的空間。
Goldenlayout 外掛程式框架可以幫助解決這個問題。

(goldenlayout)=
### GoldenLayout

GoldenLayout 是一個 Web 框架，可讓 Web 開發人員及其使用者建立自己的
選項卡式/視窗式佈局。  視窗/選項卡可以透過點選並從一個位置拖曳到另一個位置
點選標題列並拖曳，直到出現“框架線”。  將視窗拖曳到
另一個視窗的標題列將建立一個選項卡式「堆疊」。  Evenniagoldenlayout外掛定義了3個
視窗的基本型別：主視窗、輸入視窗和非主文字輸出視窗。  主要
視窗和第一個輸入視窗的獨特之處在於它們無法「關閉」。

最基本的自訂是為您的使用者提供預設佈局，而不僅僅是一個主佈局
輸出和一個起始輸入視窗。  這是透過修改您的伺服器來完成的
goldenlayout_default_config.js。

首先建立一個新的
`mygame/web/static/webclient/js/plugins/goldenlayout_default_config.js` 檔案，並新增
以下 JSON 變數：

```
var goldenlayout_config = {
    content: [{
        type: 'column',
        content: [{
            type: 'row',
            content: [{
                type: 'column',
                content: [{
                    type: 'component',
                    componentName: 'Main',
                    isClosable: false,
                    tooltip: 'Main - drag to desired position.',
                    componentState: {
                        cssClass: 'content',
                        types: 'untagged',
                        updateMethod: 'newlines',
                    },
                }, {
                    type: 'component',
                    componentName: 'input',
                    id: 'inputComponent',
                    height: 10,
                    tooltip: 'Input - The last input in the layout is always the default.',
                }, {
                    type: 'component',
                    componentName: 'input',
                    id: 'inputComponent',
                    height: 10,
                    isClosable: false,
                    tooltip: 'Input - The last input in the layout is always the default.',
                }]
            },{
                type: 'column',
                content: [{
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'example',
                    height: 60,
                    isClosable: false,
                    componentState: {
                        types: 'some-tag-here',
                        updateMethod: 'newlines',
                    },
                }, {
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'sheet',
                    isClosable: false,
                    componentState: {
                        types: 'sheet',
                        updateMethod: 'replace',
                    },
                }],
            }],
        }]
    }]
};
```
這有點難看，但希望從縮排中，您可以看到它建立了一個並排的
（2 列）介面，左側有 3 個視窗（主視窗和 2 個輸入視窗）和一對視窗
右側用於額外輸出。  任何標有“some-tag-here”的文字都會流到底部
「範例」視窗中的任何標記為「工作表」的文字都會取代「工作表」中已有的文字
視窗。

注意：GoldenLayout 會使 VERY 感到困惑，如果您使用「Main」建立兩個視窗，則會中斷
元件名稱.

現在，假設您想使用不同的 CSS 在每個視窗上顯示文字。  這就是新的地方
Goldenlayout「元件」登場。每個元件就像一個藍圖，當
您建立該元件的新例項，一旦定義，就不會輕易更改。  你
需要定義一個新元件，最好是在新的外掛檔案中，然後將其新增到您的
頁面（透過 javascript 動態到 DOM，或透過將新的外掛檔案包含到
base.html）。

首先，請按照上面自訂 Web 使用者端部分中的說明來覆蓋
base.html。

接下來，將新外掛程式新增至您的 base.html 副本：
```
<script src={% static "webclient/js/plugins/myplugin.js" %} language="javascript"
type="text/javascript"></script>
```
請記住，外掛依賴載入順序，因此請確保新的 `<script>` tag 在 `goldenlayout.js` 之前。

接下來，建立一個新的外掛檔案`mygame/web/static/webclient/js/plugins/myplugin.js`並
編輯它。

```
let myplugin = (function () {
    //
    //
    var postInit = function() {
        var myLayout = window.plugins['goldenlayout'].getGL();

        // register our component and replace the default messagewindow
        myLayout.registerComponent( 'mycomponent', function (container, componentState) {
            let mycssdiv = $('<div>').addClass('myCSS');
            mycssdiv.attr('types', 'mytag');
            mycssdiv.attr('update_method', 'newlines');
            mycssdiv.appendTo( container.getElement() );
        });

        console.log("MyPlugin Initialized.");
    }

    return {
        init: function () {},
        postInit: postInit,
    }
})();
window.plugin_handler.add("myplugin", myplugin);
```
然後，您可以將「mycomponent」新增至 `goldenlayout_default_config.js` 中專案的 `componentName`。

確保停止您的伺服器，evennia收集靜態，然後重新啟動您的伺服器。  然後確保在載入 webclient 頁面之前清除瀏覽器快取。
