(the-message-path)=
# 訊息路徑

```shell
> look

A Meadow 

This is a beautiful meadow. It is full of flowers.

You see: a flower
Exits: north, east
```

當您將 `look` 之類的指令傳送到 Evennia 時 - 實際會發生什麼？ `CmdLook` 類別最終如何處理 `look` 字串？當我們使用 e.g 時會發生什麼。 `caller.msg()` 發回訊息嗎？

瞭解此資料流 - _訊息路徑_ 對於理解 Evennia 的工作原理非常重要。

(ingoing-message-path)=
## 傳入訊息路徑

```
            Internet│
            ┌─────┐ │                                   ┌────────┐
┌──────┐    │Text │ │  ┌────────────┐    ┌─────────┐    │Command │
│Client├────┤JSON ├─┼──►commandtuple├────►Inputfunc├────►DB query│
└──────┘    │etc  │ │  └────────────┘    └─────────┘    │etc     │
            └─────┘ │                                   └────────┘
                    │Evennia
```

(incoming-command-tuples)=
### 傳入指令元組

來自用戶端的傳入資料（作為原始字串或序列化 JSON 傳入）將以 Evennia 轉換為 `commandtuple`。無論使用什麼用戶端或連線，主題都是相同的。 `commandtuple` 是一個包含三個元素的簡單元組：

```python
(commandname, (args), {kwargs})
```

對於 `look` 指令（以及玩家編寫的任何其他指令），將產生 `text` `commandtuple`：

```python
("text", ("look",), {})
```

(inputfuncs)=
### 輸入函式

在 Evennia 伺服器端，註冊了 [inputfuncs](../Components/Inputfuncs.md) 清單。您可以透過擴充套件 `settings.INPUT_FUNC_MODULES` 新增您自己的。

```python
inputfunc_commandname(session, *args, **kwargs)
```
這裡的 `session` 表示來自的唯一用戶端連線（也就是說，它僅標識_誰_正在傳送此輸入）。

其中一種輸入函式名為 `text`。對於傳送`look`，它將被稱為
```{sidebar}
如果您知道 `*args` 和 `**kwargs` 在 Python 中如何運作，您會發現這與呼叫 `text(session, "look")` 相同
```

```python
text(session, *("look",), **{})  
```

`inputfunc` 對此的作用取決於。對於[帶外](./OOB.md)指令，它可以取得玩家的生命值或減少某些計數器的值。

```{sidebar} 在此之前沒有發生任何文字解析
如果您傳送 `look here`，則呼叫將為 `text(session, *("look here", **{})`。在此步驟之後，所有文字輸入的解析都發生在指令解析器中。
```
對於 `text` `inputfunc`，將呼叫 Evennia [CommandHandler](../Components/Commands.md) 並進一步分析引數，以便確定要執行哪個指令。

在 `look` 的範例中，將呼叫 `CmdLook` 指令類別。這將檢索當前位置的描述。

(outgoing-message-path)=
## 傳出訊息路徑

```
            Internet│
            ┌─────┐ │
┌──────┐    │Text │ │  ┌──────────┐    ┌────────────┐   ┌─────┐
│Client◄────┤JSON ├─┼──┤outputfunc◄────┤commandtuple◄───┤msg()│
└──────┘    │etc  │ │  └──────────┘    └────────────┘   └─────┘
            └─────┘ │
                    │Evennia
```

(msg-to-outgoing-commandtuple)=
### `msg` 到傳出指令元組

當 `inputfunc` 完成了它應該做的事情時，伺服器可能會也可能不會決定回傳結果（某些型別的 `inputcommands` 可能根本不期望或不需要回應）。伺服器也經常在沒有任何先前匹配的傳入資料的情況下傳送傳出訊息。

每當需要將資料「傳送」到 Evennia 時，我們必須將其概括為（現在正在傳出）`commandtuple` `(commandname, (args), {kwargs})`。我們使用 `msg()` 方法來做到這一點。為了方便起見，每個主要實體都可以使用此方法，例如 `Object.msg()` 和 `Account.msg()`。它們都連結回`Session.msg()`。

```python
msg(text=None, from_obj=None, session=None, options=None, **kwargs)
```

`text` 非常常見，因此它被作為預設值：

```python
msg("A meadow\n\nThis is a beautiful meadow...")
```

這將轉換為 `commandtuple`，如下所示：
```python
("text", ("A meadow\n\nThis is a beutiful meadow...",) {})
```

`msg()` 方法可讓您直接定義 `commandtuple`，用於您想要尋找的任何傳出指令：

```python
msg(current_status=(("healthy", "charged"), {"hp": 12, "mp": 20}))
```

這將轉換為 `commandtuple`，如下所示：

```python
("current_status", ("healthy", "charged"), {"hp": 12, "mp": 20})
```

(outputfuncs)=
### 輸出函式

```{sidebar}
`outputfuncs` 與協議緊密耦合，您通常不需要接觸它們，除非您完全[新增協議](./Protocols.md)。
```
由於 `msg()` 知道要傳送到哪一個 [Session](../Components/Sessions.md)，因此傳出的 `commandtuple` 最終總是指向正確的用戶端。

每個受支援的 Evennia 協定（Telnet、SSH、Webclient 等）都有自己的 `outputfunc`，它將通用 `commandtuple` 轉換為特定協定可以理解的形式，例如 telnet 指令或 JSON。

對於 telnet（無 SSL），`look` 將透過線路以純文字形式傳回：

    A meadow\n\nThis is a beautiful meadow...

當傳送到 webclient 時，`commandtuple` 被轉換為序列化的 JSON，如下所示：

    '["look", ["A meadow\\n\\nThis is a beautiful meadow..."], {}]'

然後透過線路將其傳送到用戶端。然後由客戶來正確解釋和處理資料。


(components-along-the-path)=
## 沿路徑的元件

(ingoing)=
### 傳入

```
                ┌──────┐                ┌─────────────────────────┐
                │Client│                │                         │
                └──┬───┘                │  ┌────────────────────┐ │
                   │             ┌──────┼─►│ServerSessionHandler│ │
┌──────────────────┼──────┐      │      │  └───┬────────────────┘ │
│ Portal           │      │      │      │      │                  │
│        ┌─────────▼───┐  │    ┌─┴─┐    │  ┌───▼─────────┐        │
│        │PortalSession│  │    │AMP│    │  │ServerSession│        │
│        └─────────┬───┘  │    └─┬─┘    │  └───┬─────────┘        │
│                  │      │      │      │      │                  │
│ ┌────────────────▼───┐  │      │      │  ┌───▼─────┐            │
│ │PortalSessionHandler├──┼──────┘      │  │Inputfunc│            │
│ └────────────────────┘  │             │  └─────────┘            │
│                         │             │                  Server │
└─────────────────────────┘             └─────────────────────────┘
```

1. 用戶端 - 透過線路傳送握手或指令。此資訊由 Evennia [Portal](../Components/Portal-And-Server.md) 接收。
2. `PortalSession`代表一個用戶端連線。它瞭解所使用的通訊協定。它將協定特定的輸入轉換為通用的 `commandtuple` 結構 `(cmdname, (args), {kwargs})`。
3. `PortalSessionHandler` 處理所有連線。它將 `commandtuple` 與 session-id 一起醃製。
4.  Pickled 資料透過 `AMP`（非同步訊息協定）連線傳送到 Evennia 的 [伺服器](Server-And-Portal) 部分。
5. `ServerSessionHandler` 取消 `commandtuple` 並將 session-id 與匹配的 `SessionSession` 進行配對。
6. `ServerSession`代表伺服器端的session-連線。它透過其登錄檔 [Inputfuncs](../Components/Inputfuncs.md) 來尋找匹配項。
7. 使用 `commandtuple` 中包含的 args/kwargs 呼叫適當的 `Inputfunc`。根據`Inputfunc`，這可能會產生不同的效果。對於 `text` inputfunc，它會觸發 [CommandHandler](../Components/Commands.md)。

(outgoing)=
### 傳出

```
                ┌──────┐                ┌─────────────────────────┐
                │Client│                │                         │
                └──▲───┘                │  ┌────────────────────┐ │
                   │             ┌──────┼──┤ServerSessionHandler│ │
┌──────────────────┼──────┐      │      │  └───▲────────────────┘ │
│ Portal           │      │      │      │      │                  │
│        ┌─────────┴───┐  │    ┌─┴─┐    │  ┌───┴─────────┐        │
│        │PortalSession│  │    │AMP│    │  │ServerSession│        │
│        └─────────▲───┘  │    └─┬─┘    │  └───▲─────────┘        │
│                  │      │      │      │      │                  │
│ ┌────────────────┴───┐  │      │      │  ┌───┴──────┐           │
│ │PortalSessionHandler◄──┼──────┘      │  │msg() call│           │
│ └────────────────────┘  │             │  └──────────┘           │
│                         │             │                  Server │
└─────────────────────────┘             └─────────────────────────┘
```

1. `msg()` 方法被呼叫
2. `ServerSession`，特別是 `ServerSession.msg()` 是中心點，所有 `msg()` 呼叫都透過它進行路由，以便將資料傳送到該 [Session](../Components/Sessions.md)。
3. `ServerSessionHandler` 將`msg` 輸入轉換為正確的`commandtuple` 結構`(cmdname, (args), {kwargs})`。   It pickles the `commandtuple` together with the session-id.
4.  Pickled 資料透過 `AMP`（非同步訊息協定）連線傳送到 Evennia 的 [Portal](Server-And-Portal) 部分。
5. `PortalSessionHandler` 取消 `commandtuple` 並將其 session id 與匹配的 `PortalSession` 進行配對。
6. `PortalSession` 現在負責將通用 `commandtuple` 轉換為該特定連線使用的通訊協定。
7. 用戶端接收資料並可以對其採取行動。