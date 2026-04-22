(inputfuncs)=
# 輸入函式

```
          Internet│
            ┌─────┐ │                                   ┌────────┐
┌──────┐    │Text │ │  ┌────────────┐    ┌─────────┐    │Command │
│Client├────┤JSON ├─┼──►commandtuple├────►Inputfunc├────►DB query│
└──────┘    │etc  │ │  └────────────┘    └─────────┘    │etc     │
            └─────┘ │                                   └────────┘
                    │Evennia

```

Inputfunc 是 [傳入訊息路徑](../Concepts/Messagepath.md#ingoing-message-path) 上的最後一個固定步驟。使用從用戶端傳送的 `commandtuple` 結構來尋找並呼叫可用的 Inputfunc。 Inputfunc 的工作是透過觸發指令、執行資料庫查詢或任何需要的操作來執行要求的任何操作。

在表格上給出`commandtuple`

    (commandname, (args), {kwargs})

Evennia將嘗試在表單上尋找並呼叫Inputfunc

```python
def commandname(session, *args, **kwargs):
    # ...

```
或者，如果沒有找到匹配項，它將在此表單上呼叫名為「default」的 inputfunc

```python
def default(session, cmdname, *args, **kwargs):
    # cmdname is the name of the mismatched inputcommand

```

預設輸入函式位於 [evennia/server/inputfuncs.py](evennia.server.inputfuncs) 中。

(adding-your-own-inputfuncs)=
## 新增您自己的輸入函式

1. 在上面的表單上新增一個函式到`mygame/server/conf/inputfuncs.py`。您的函式必須位於該模組的全域最外層範圍內，且不以下劃線 (`_`) 開頭才能被辨識為 inputfunc。  我
2. `reload` 伺服器。

要過載預設的 inputfunc（見下文），只需新增一個同名的函式即可。您還可以擴充套件設定列表`INPUT_FUNC_MODULES`。

    INPUT_FUNC_MODULES += ["path.to.my.inputfunc.module"]

這些模組中名稱不以 `_` 開頭的所有全域級函式將被 Evennia 用作 inputfunc。該列表是從左到右匯入的，因此後面匯入的函式將替換前面的函式。

(default-inputfuncs)=
## 預設輸入功能

Evennia 定義了一些預設的輸入函式來處理常見情況。這些定義在
`evennia/server/inputfuncs.py`。

(text)=
### 文字

 - 輸入：`("text", (textstring,), {})`
 - 輸出：取決於觸發的指令

這是最常見的輸入，也是所有傳統泥漿支援的唯一輸入。引數通常是使用者從指令列傳送的內容。由於所有文字都來自使用者輸入
就像這被認為是一個[指令](./Commands.md)，這個輸入函式將執行諸如缺口替換之類的操作，然後將輸入傳遞給中央指令處理程式。

(echo)=
### 迴音

 - 輸入：`("echo", (args), {})`
 - 輸出：`("text", ("Echo returns: %s" % args), {})`

這是一個測試輸入，它只是將引數作為文字回顯到 session。可用於測試自訂用戶端輸入。

(default)=
### 預設

如上所述，預設功能吸收所有未識別的輸入指令。預設只會記錄一個錯誤。

(client_options)=
### client_options

 - 輸入：`("client_options, (), {key:value,...})`
 - 輸出：
  - 正常：無
  - 得到：`("client_options", (), {key:value,...})`

這是用於設定協定選項的直接指令。這些可以用 `@option` 設定
指令，但這提供了一種用戶端方式來設定它們。並非所有連線協定都使用
所有標誌，但以下是可能的關鍵字：

 - get (bool)：如果為 true，則忽略所有其他 kwargs 並立即傳回目前設定
作為輸出指令`("client_options", (), {key=value,...})`-
 - client (str)：用戶端識別符，如「mushclient」。
 - version (str)：用戶端版本
 - ansi (bool): 支援 ansi 顏色
 - xterm256 (bool): 是否支援 xterm256 顏色
 - mxp (bool): 是否支援MXP
 - utf-8 (bool): 是否支援UTF-8
 - screenreader (bool)：螢幕閱讀器模式開/關
 - mccp (bool): MCCP 壓縮開/關
 - screenheight (int): 螢幕高度（以行為單位）
 - screenwidth (int): 螢幕寬度（以字元為單位）
 - inputdebug (bool)：偵錯輸入函式
 - nomarkup (bool): 刪除所有文字tags
 - raw (bool): 保留文字 tags 未解析

> 請注意，此 inputfunc 有兩個 GMCP 別名 - `hello` 和 `supports_set`，這表示它將透過某些用戶端假定的 GMCP `Hello` 和 `Supports.Set` 指令進行存取。

(get_client_options)=
### get_client_options

 - 輸入：`("get_client_options, (), {key:value,...})`
 - 輸出：`("client_options, (), {key:value,...})`

這是一個方便的包裝器，透過將“get”傳送到上面的 `client_options` 來檢索當前選項。

(get_inputfuncs)=
### get_inputfuncs

- 輸入：`("get_inputfuncs", (), {})`
- 輸出：`("get_inputfuncs", (), {funcname:docstring,...})`
 
傳回格式為 `("get_inputfuncs", (), {funcname:docstring,...})` 的輸出指令 - 所有可用輸入函式及其檔案字串的清單。

(login)=
### 登入

> 注意：這目前是實驗性的，還沒有經過很好的測試。

 - 輸入：`("login", (username, password), {})`
 - 輸出：取決於登入掛鉤

這將在目前 Session 上執行 inputfunc 版本的登入操作。它旨在由自訂用戶端設定使用。

(get_value)=
### get_value

輸入：`("get_value", (name, ), {})`
輸出：`("get_value", (value, ), {})`

從此 Session 目前控制的角色或帳戶中檢索值。採用一個引數，這只會接受特定的白名單名稱，您需要過載函式才能擴充。預設情況下，可以檢索以下值：

 - “name”或“key”：帳號或傀儡角色的金鑰。
 - “location”：目前位置的名稱，或“無”。
 - “servername”：連線到的Evennia伺服器的名稱。

(repeat)=
### 重複

 - 輸入：`("repeat", (), {"callback":funcname,  "interval": secs, "stop": False})`
 - 輸出：取決於重複函式。將返回 `("text", (repeatlist),{}` 以及列表
如果給定一個不熟悉的回呼名稱，則接受名稱。

這將告訴 evennia 以給定的時間間隔重複呼叫命名函式。這將在幕後設定一個 [Ticker](./TickerHandler.md)。只有以前可接受的函式可以透過這種方式重複呼叫，您需要過載此 inputfunc 來新增您想要提供的函式。預設情況下，只允許兩個範例函式，“test1”和“test2”，它們只會以給定的時間間隔回顯文字。透過傳送 `"stop": True` 停止重複（請注意，您必須包含回呼名稱和 Evennia 的時間間隔才能知道要停止什麼）。

(unrepeat)=
### 不重複

 - 輸入：`("不重複", (), ("回呼":funcname,
                             "interval": secs)`
 - 輸出：無

這是一個方便的包裝器，用於將“stop”傳送到 `repeat` inputfunc。

(monitor)=
### 監視器

 - 輸入：`("monitor", (), ("name":field_or_argname, stop=False)`
 - 輸出（變化時）：`("monitor", (), {"name":name, "value":value})`

這將設定屬性或資料庫欄位的物件監控。每當欄位或 Attribute 以任何方式變更時，都會傳送輸出指令。這是在幕後使用[MonitorHandler](./MonitorHandler.md)。透過「停止」鍵停止監控。請注意，在停止時您還必須提供名稱，以便讓系統知道應取消哪個監視器。

僅允許使用白名單中的欄位/屬性，您必須過載此函式才能新增更多。預設情況下，可以監控以下欄位/屬性：

 - “name”：目前角色名稱
 - “位置”：目前位置
 - “desc”：描述引數

(unmonitor)=
### 取消監控

 - 輸入：`("unmonitor", (), {"name":name})`
 - 輸出：無

一個方便的包裝器，將“stop”傳送到 `monitor` 函式。