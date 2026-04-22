(core-components)=
# 核心元件

這些是構建 Evennia 的“構建塊”。本文件是對 [API](../Evennia-API.md) 中每個元件的文件字串的補充，並且通常比其更深入。

(base-components)=
<a id="base-components"></a>
## 基礎元件

這些是用於製作 Evennia 遊戲的基礎零件。大多數都是長期存在的並且持久存在於資料庫中。

```{toctree} 
:maxdepth: 2
Portal-And-Server.md
Sessions.md
Typeclasses.md
Accounts.md
Objects.md
Characters.md
Rooms.md
Exits.md
Scripts.md
Channels.md
Msg.md
Attributes.md
Nicks.md
Tags.md
Prototypes.md
Help-System.md
Permissions.md
Locks.md
```

(commands)=
<a id="commands"></a>
## 指令

Evennia 的指令系統處理使用者傳送到伺服器的所有內容。

```{toctree} 
:maxdepth: 2

Commands.md
Command-Sets.md
Default-Commands.md
Batch-Processors.md
Inputfuncs.md
```


(utils-and-tools)=
<a id="utils-and-tools"></a>
## 工具與實用模組

Evennia提供程式碼資源庫來幫助建立遊戲。

```{toctree} 
:maxdepth: 2

Coding-Utils.md
EvEditor.md
EvForm.md
EvMenu.md
EvMore.md
EvTable.md
FuncParser.md
MonitorHandler.md
OnDemandHandler.md
TickerHandler.md
Signals.md
```

(web-components)=
<a id="web-components"></a>
## Web 元件

Evennia 也是它自己的 webserver，有一個網站和瀏覽器內 webclient 您可以擴充套件。

```{toctree} 
:maxdepth: 2

Website.md
Webclient.md
Web-Admin.md
Webserver.md
Web-API.md
Web-Bootstrap-Framework.md
```
