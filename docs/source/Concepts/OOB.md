(out-of-band-messaging)=
# 帶外訊息傳遞

OOB，或帶外，表示在 Evennia 和使用者使用者端之間傳送資料，而無需使用者
提示它或必須意識到它正在被透過。常見用途是更新
用戶端健康欄，處理用戶端按鈕按下或以不同的方式顯示某些標記文字
窗玻璃。

如果您還沒有，您應該熟悉 [Messagepath](./Messagepath.md)，它描述了訊息如何進入和離開 Evennia，以及在此過程中所有訊息如何轉換為稱為 `commandtuple` 的通用格式：

    (commandname, (args), {kwargs})

(sending-and-receiving-an-oob-message)=
## 傳送和接收 OOB 訊息

傳送很簡單。您只需使用要傳送到其 session 的物件的正常 `msg` 方法即可。

```python
    caller.msg(commandname=((args, ...), {key:value, ...}))
```

該關鍵字成為 `commandtuple` 的指令名稱部分，其值成為 `args` 和 `kwargs` 部分。您也可以同時傳送不同`commandname`s的多個訊息。

一種特殊情況是 `text` 呼叫。它是如此常見，以至於它是 `msg` 方法的預設值。所以這些是等價的：

```python
    caller.msg("Hello")
    caller.msg(text="Hello")
```

您不必指定完整的 `commandtuple` 定義。例如，如果您的特定指令只需要 kwargs，您可以跳過 `(args)` 部分。就像 `text` 的情況一樣，你可以跳過
如果只有一個引數，則寫入元組...等等 - 輸入非常靈活。如果有
根本不需要給出空元組 `msg(cmdname=(,)` 的引數（給出 `None` 意味著
單一引數`None`）。

(which-command-names-can-i-send)=
### 我可以傳送哪些指令名稱？

這取決於用戶端和協定。如果您使用Evennia [webclient](../Components/Webclient.md)，您可以修改它以使其支援您喜歡的任何指令名稱。

許多第三方 MUD 使用者端支援下面列出的一系列 OOB 協定。如果使用者端不支援特定的 OOB 指令/指令，Evennia 將僅向其傳送 `text` 指令，並悄悄地刪除所有其他 OOB 指令。

> 請注意，給定的訊息可能會傳送到具有不同功能的多個用戶端。因此，除非您完全關閉 telnet 並且僅依賴 webclient，否則您永遠不應該依賴非 `text` OOB 訊息始終到達所有目標。

(which-command-names-can-i-receive)=
### 我可以接收哪些指令名稱

這取決於您定義的 [Inputfuncs](../Components/Inputfuncs.md)。您可以根據需要擴充套件 Evennia 的預設值，但在 `settings.INPUT_FUNC_MODULES` 指向的模組中新增您自己的函式。
 
(supported-oob-protocols)=
## 支援OOB協議

Evennia 支援使用以下協定之一的用戶端：

(telnet)=
### 遠端登入

預設情況下，telnet（以及 telnet+SSL）僅支援普通的 `text` 輸出指令。 Evennia 偵測使用者端是否支援標準 telnet 協定的兩個 MUD-特定 OOB *擴充*之一 - GMCP 或 MSDP。 Evennia 同時支援兩者並將切換到用戶端使用的協定。如果用戶端兩者都支援，則將使用GMCP。

> 請注意，對於 Telnet，`text` 具有特殊狀態，即「帶內」操作。因此 `text` 輸出指令直接透過線路傳送 `text` 引數，而不經過下面描述的 OOB 轉換。

(telnet-gmcp)=
#### 遠端登入 + GMCP

[GMCP](https://www.gammon.com.au/gmcp)，*通用泥漿通訊協定*以 `cmdname + JSONdata` 的形式傳送資料。這裡的 cmdname 應該要採取「Package.Subpackage」的形式。還可能有額外的子子包等。這些「包」和「子包」的名稱沒有那麼標準化，超出了個人 MUDs 或公司多年來選擇使用的名稱。您可以決定自己的套件名稱，但其他人正在使用以下名稱：

- [土狼GMCP](https://www.aardwolf.com/wiki/index.php/Clients/GMCP)
- [飛碟世界GMCP](https://discworld.starturtle.net/lpc/playing/documentation.c?path=/concepts/gmcp)
- [頭像GMCP](https://www.outland.org/infusions/wiclear/index.php?title=MUD%20Protocols&lang=en)
- [IRE 遊戲 GMCP](https://nexus.ironrealms.com/GMCP)

Evennia 會將底線轉換為 `.` 並大寫以符合規範。因此輸出指令 `foo_bar` 將變成 GMCP 指令名 `Foo.Bar`。 GMCP 指令「Foo.Bar」將出現 `foo_bar`。要傳送 GMCP 指令，該指令會變成不帶下劃線的 Evennia 輸入指令，請使用 `Core` 包。因此 `Core.Cmdname` 變成 Evennia 中的 `cmdname`，反之亦然。

在電線上，`commandtuple`

    ("cmdname", ("arg",), {}) 
   
將作為 GMCP telnet 指令透過線路傳送

    IAC SB GMCP "cmdname" "arg" IAC SE

其中所有大寫單字都是 ][evennia/server/portal/telnet_oob](evennia.server.portal/telnet_oob.py) 中指定的 telnet 字元常數。這些由協定解析/新增，我們不將它們包含在下面的列表中。

| `commandtuple` | GMCP-指令 | 
| --- | ---| 
| `(cmd_name, (), {})`  |  `Cmd.Name` |
| `(cmd_name, (arg,), {})` |      `Cmd.Name arg` | 
| `(cmd_na_me, (args,...),{})`  |     `Cmd.Na.Me [arg, arg...]` | 
| `(cmd_name, (), {kwargs})` |    `Cmd.Name {kwargs}` | 
| `(cmdname, (arg,), {kwargs})` | `Core.Cmdname [[args],{kwargs}]` | 

由於 Evennia 已經提供了與最常見的 GMCP 實現所期望的名稱不匹配的預設輸入函式，因此我們有一些硬編碼的對映：

| GMCP 指令名 | `commandtuple` 指令名 |
| --- | --- | 
| `"Core.Hello"` | `"client_options"` | 
| `"Core.Supports.Get"` | `"client_options"` | 
| `"Core.Commands.Get"` | `"get_inputfuncs"` | 
| `"Char.Value.Get"` | `"get_value"` | 
| `"Char.Repeat.Update"` | `"repeat"` |
| `"Char.Monitor.Update"`| `"monitor"` | 

(telnet-msdp)=
#### 遠端登入 + MSDP

[MSDP](http://tintin.sourceforge.net/msdp/)，*泥漿伺服器資料協定*，是 GMCP 的競爭標準。 MSDP 協議頁指定一系列「推薦」可用的 MSDP 指令名稱。 Evennia *不*支援這些 - 因為 MSDP 沒有為其指令名稱指定特殊格式（如 GMCP 那樣），用戶端可以並且應該僅透過其實際名稱呼叫內部 Evennia inputfunc。

MSDP 使用 Telnet 字元常數透過線路打包各種結構化資料。 MSDP 支援字串、陣列（列表）和表格（字典）。這些用於定義所需的 cmdname、args 和 kwargs。當為 `("cmdname", ("arg",), {})` 傳送 MSDP 時，產生的 MSDP 指令將如下所示：

    IAC SB MSDP VAR cmdname VAL arg IAC SE

各種可用的MSDP常量，例如`VAR`（變數）、`VAL`（值）、`ARRAYOPEN`/`ARRAYCLOSE`
`TABLEOPEN`/`TABLECLOSE` 在 `evennia/server/portal/telnet_oob` 中指定。

| `commandtuple` | MSDP指令 | 
| --- | --- | 
| `(cmdname, (), {})` | `VAR cmdname VAL` | 
| `(cmdname, (arg,), {})` | `VAR cmdname VAL arg` | 
| `(cmdname, (arg,...),{})`  | `VAR cmdname VAL ARRAYOPEN VAL arg VAL arg... ARRAYCLOSE` | 
| `(cmdname, (), {kwargs})`  | `VAR cmdname VAL TABLEOPEN VAR key VAL val... TABLECLOSE` | 
| `(cmdname, (args,...), {kwargs})` | `VAR cmdname VAL ARRAYOPEN VAL arg VAL arg... ARRAYCLOSE VAR cmdname VAL TABLEOPEN VAR key VAL val... TABLECLOSE` |

請注意 `VAR... VAL` 始終標識 `cmdnames`，因此如果有多個以相同 cmdname 標記的陣列/字典，它們將附加到該 inputfunc 的 args、kwargs 中。反之亦然，一個
不同的`VAR... VAL`（表外）將作為第二個不同的指令輸入出現。

(ssh)=
### SSH

SSH 僅支援`text` 輸入/輸出指令。

(web-client)=
### 網頁用戶端

我們的 Web 使用者端使用純 [JSON](https://en.wikipedia.org/wiki/JSON) 結構進行所有通訊，包括 `text`。這直接對應到 Evennia 內部輸出/輸入指令，包括最終的空引數/kwargs。

| `commandtuple` | Evennia Webclient JSON | 
| --- | --- | 
| `(cmdname, (), {})` |  `["cmdname", [], {}]` | 
| `(cmdname, (arg,), {})` | `["cmdname", [arg], {}]` |
| `(cmdname, (arg,...),{})`  |  `["cmdname", [arg,...], {})` |
| `(cmdname, (), {kwargs})`  | `["cmdname", [], {kwargs})` | 
| `(cmdname, (arg,...), {kwargs})` | `["cmdname", [arg,...], {kwargs})` | 

由於 JSON 是 Javascript 原生的，因此 webclient 很容易處理。