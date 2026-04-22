(protocols)=
# 協定

```
            Internet│ Protocol
            ┌─────┐ │ | 
┌──────┐    │Text │ │  ┌──────────┐    ┌────────────┐   ┌─────┐
│Client◄────┤JSON ├─┼──┤outputfunc◄────┤commandtuple◄───┤msg()│
└──────┘    │etc  │ │  └──────────┘    └────────────┘   └─────┘
            └─────┘ │
                    │Evennia
```

_Protocol_ 描述 Evennia 如何透過線路傳送和接收資料到用戶端。每種連線型別（telnet、ssh、webclient 等）都有自己的協定。某些協定也可能有變體（例如純文字 Telnet 與 Telnet SSL）。

有關資料如何流經 Evennia 的大圖，請參閱[訊息路徑](./Messagepath.md)。

Evennia中，`PortalSession`代表用戶端連線。 session 被告知使用特定協議。傳送資料時，session 必須提供「Outputfunc」以將通用 `commandtuple` 轉換為協定可以理解的形式。對於傳入資料，伺服器還必須提供適當的 [Inputfuncs](../Components/Inputfuncs.md) 來處理傳送到伺服器的指令。

(adding-a-new-protocol)=
## 新增協議

Evennia 有一個外掛系統，可以將協定作為新的「服務」新增到應用程式中。

若要將您自己的新服務（例如您自己的自訂用戶端協定）新增至 Portal 或伺服器，請展開 `mygame/server/conf/server_services_plugins` 和 `portal_services_plugins`。

若要擴充 Evennia 尋找外掛程式的位置，請使用以下設定：
```python
    # add to the Server
    SERVER_SERVICES_PLUGIN_MODULES.append('server.conf.my_server_plugins')
    # or, if you want to add to the Portal
    PORTAL_SERVICES_PLUGIN_MODULES.append('server.conf.my_portal_plugins')
```

> 新增的使用者端連線時，您很可能只需要在 Portal-外掛檔案中新增內容。

外掛模組必須包含函式 `start_plugin_services(app)`，其中 `app` 引數指的是 Portal/伺服器應用程式本身。這由伺服器或 Portal 在啟動時呼叫。它必須包含所需的所有啟動程式碼。

例子：

```python
    # mygame/server/conf/portal_services_plugins.py

    # here the new Portal Twisted protocol is defined
    class MyOwnFactory( ... ):
       # [...]

    # some configs
    MYPROC_ENABLED = True # convenient off-flag to avoid having to edit settings all the time
    MY_PORT = 6666

    def start_plugin_services(portal):
        "This is called by the Portal during startup"
         if not MYPROC_ENABLED:
             return
         # output to list this with the other services at startup
         print(f"  myproc: {MY_PORT}")

         # some setup (simple example)
         factory = MyOwnFactory()
         my_service = internet.TCPServer(MY_PORT, factory)
         # all Evennia services must be uniquely named
         my_service.setName("MyService")
         # add to the main portal application
         portal.services.addService(my_service)
```

一旦模組在設定中被定義和定位，只需重新載入伺服器和新的
協議/服務應該從其他開始。

(writing-your-own-protocol)=
### 編寫自己的協議

```{important}
這被認為是一個高階主題。
```

從頭開始編寫穩定的通訊協定不是我們在這裡討論的內容，這不是一項簡單的任務。好訊息是 Twisted 提供了許多通用協議的實現，可以隨時進行調整。

在 Twisted 中編寫協議實作通常涉及建立一個繼承自現有 Twisted 協定類別和 `evennia.server.session.Session`（多個
繼承），然後過載特定協定用來將它們連結到的方法
Evennia特定輸入。

這是一個展示這個概念的例子：

```python
# In module that we'll later add to the system through PORTAL_SERVICE_PLUGIN_MODULES

# pseudo code 
from twisted.something import TwistedClient
# this class is used both for Portal- and Server Sessions
from evennia.server.session import Session 

from evennia.server.portal.portalsessionhandler import PORTAL_SESSIONS

class MyCustomClient(TwistedClient, Session): 

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.sessionhandler = PORTAL_SESSIONS

    # these are methods we must know that TwistedClient uses for 
    # communication. Name and arguments could vary for different Twisted protocols
    def onOpen(self, *args, **kwargs):
        # let's say this is called when the client first connects

        # we need to init the session and connect to the sessionhandler. The .factory
        # is available through the Twisted parents

        client_address = self.getClientAddress()  # get client address somehow

        self.init_session("mycustom_protocol", client_address, self.factory.sessionhandler)
        self.sessionhandler.connect(self)

    def onClose(self, reason, *args, **kwargs):
        # called when the client connection is dropped
        # link to the Evennia equivalent
        self.disconnect(reason)

    def onMessage(self, indata, *args, **kwargs): 
        # called with incoming data
        # convert as needed here        
        self.data_in(data=indata) 

    def sendMessage(self, outdata, *args, **kwargs):
        # called to send data out
        # modify if needed        
        super().sendMessage(self, outdata, *args, **kwargs)

     # these are Evennia methods. They must all exist and look exactly like this
     # The above twisted-methods call them and vice-versa. This connects the protocol
     # the Evennia internals.  
     
     def disconnect(self, reason=None): 
         """
         Called when connection closes. 
         This can also be called directly by Evennia when manually closing the connection.
         Do any cleanups here.
         """
         self.sessionhandler.disconnect(self)

     def at_login(self): 
         """
         Called when this session authenticates by the server (if applicable)
         """    

     def data_in(self, **kwargs):
         """
         Data going into the server should go through this method. It 
         should pass data into `sessionhandler.data_in`. THis will be called
         by the sessionhandler with the data it gets from the approrpriate 
         send_* method found later in this protocol. 
         """
         self.sessionhandler.data_in(self, text=kwargs['data'])

     def data_out(self, **kwargs):
         """
         Data going out from the server should go through this method. It should
         hand off to the protocol's send method, whatever it's called.
         """
         # we assume we have a 'text' outputfunc
         self.onMessage(kwargs['text'])

     # 'outputfuncs' are defined as `send_<outputfunc_name>`. From in-code, they are called 
     # with `msg(outfunc_name=<data>)`. 

     def send_text(self, txt, *args, **kwargs): 
         """
         Send text, used with e.g. `session.msg(text="foo")`
         """
         # we make use of the 
         self.data_out(text=txt)

     def send_default(self, cmdname, *args, **kwargs): 
         """
         Handles all outputfuncs without an explicit `send_*` method to handle them.
         """
         self.data_out(**{cmdname: str(args)})

```
這裡的原則是重寫 Twisted 特定的方法以將輸入/輸出重新導向到
Evennia特定方法。

(sending-data-out)=
### 傳送資料

要透過此協議傳送資料，您需要取得其Session，然後才能e.g。

```python
    session.msg(text="foo")
```

該訊息將穿過系統，以便會話處理程式將挖掘 session 並檢查它是否有 `send_text` 方法（它有）。然後它將把“foo”傳遞給該方法，該方法
在我們的例子中意味著透過網路傳送「foo」。

(receiving-data)=
### 接收資料

僅僅因為協議存在，並不意味著 Evennia 知道如何處理它。必須存在 [Inputfunc](../Components/Inputfuncs.md) 才能接收它。在上面範例的 `text` 輸入的情況下，Evennia 已經處理此輸入 - 它將其解析為指令名稱後跟其輸入。因此，您需要簡單地在接收 Session（和/或它所操縱的物件/角色）上新增 cmdset 和指令。如果沒有，您可能需要新增自己的 Inputfunc（請參閱 [Inputfunc](../Components/Inputfuncs.md) 頁面以瞭解如何執行此操作。

這些可能並非在所有協議中都那麼明確，但原則是存在的。這四個基本元件 - 無論如何訪問 - 連結到 *Portal Session*，這是不同低階協定和 Evennia 之間的實際公共介面。