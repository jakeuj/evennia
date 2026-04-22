(sessions)=
# Sessions

```
┌──────┐ │   ┌───────┐    ┌───────┐   ┌──────┐
│Client├─┼──►│Session├───►│Account├──►│Object│
└──────┘ │   └───────┘    └───────┘   └──────┘
                 ^
```

Evennia *Session* 表示與伺服器建立的一個連線。取決於
Evennia session，一個人可以多次連線，例如使用不同的
多個視窗中的用戶端。每個這樣的連線都由一個 session 物件表示。

session 物件有自己的 [cmdset](./Command-Sets.md)，通常是「未登入」cmdset。這是用於顯示登入畫面並處理建立新帳戶（或 evennia 行話中的 [帳戶](./Accounts.md)）的指令，讀取初始幫助並使用現有帳戶登入遊戲。 session 物件可以“登入”，也可以不“登入”。  登入意味著使用者已經透過身份驗證。當發生這種情況時，session 與帳戶物件關聯（它儲存以帳戶為中心的內容）。然後，該帳戶可以依次操縱任意數量的物件/角色。

Session 不是*持久* - 它不是 [Typeclass](./Typeclasses.md) 且沒有與資料庫的連線。當使用者斷開連線時，Session 將消失，並且如果伺服器重新載入，您將丟失其中的所有自訂資料。 Sessions 上的 `.db` 處理程式用於呈現統一的 API（因此，即使您不知道收到的是物件還是 Session，您也可以假設 `.db` 存在），但這只是 `.ndb` 的別名。因此，請勿在 Sessions 上儲存您無法承受重新載入時遺失的任何資料。

(working-with-sessions)=
## 與 Sessions 一起工作

(properties-on-sessions)=
### Sessions 上的屬性

以下是（伺服器-）Sessions 上可用的一些重要屬性

- `sessid` - 唯一的session-id。這是一個從 1 開始的整數。
- `address` - 連線的用戶端的位址。不同的協議在這裡提供不同的資訊。
- `logged_in` - `True`（如果使用者透過此 session 進行身份驗證）。
- `account` - Session 附加到的 [帳戶](./Accounts.md)。如果尚未登入，則為 `None`。
- `puppet` - 目前由該帳戶/Session組合操縱的[角色/物件](./Objects.md)。如果未登入或處於 OOC 模式，則為 `None`。
- `ndb` - [非持久 Attribute](./Attributes.md) 處理程式。
- `db` - 如上所述，Sessions 沒有常規屬性。這是 `ndb` 的別名。
- `cmdset` - Session 的 [CmdSetHandler](./Command-Sets.md)

Session統計資料主要由Evennia內部使用。

- `conn_time` - 此 Session 連線了多長時間
- `cmd_last` - 最後活動時間戳記。這將透過傳送 `idle` keepalive 來重設。
- `cmd_last_visible` - 最後活動時間戳記。這會忽略 `idle` keepalive 並代表
上次這個 session 確實明顯處於活動狀態。
- `cmd_total` - 透過此 Session 傳遞的指令總數。

(returning-data-to-the-session)=
### 正在將資料返回到session

當您使用 `msg()` 將資料傳回給使用者時，您呼叫 `msg()` 的物件很重要。的
`MULTISESSION_MODE` 也很重要，尤其是大於 1 時。

例如，如果您使用 `account.msg("hello")`，則 evennia 無法知道它是哪個 session
應將問候傳送至。在這種情況下，它將傳送給所有 sessions。如果你想要一個特定的
session 您需要將其 session 提供給 `msg` 呼叫 (`account.msg("hello",
session=我的會話)`)。

另一方面，如果您在傀儡物件上呼叫 `msg()` 訊息，例如
`character.msg("hello")`，角色已經知道控制它的session - 它會
巧妙地為您自動新增此內容（如果您特別想傳送，可以指定不同的 session
東西到另一個session）。

最後，所有指令類別上都有一個 `msg()` 的包裝器：`command.msg()`。這將
透明地檢測哪個 session 正在觸發指令（如果有）並重定向到該 session
（這通常是您想要的）。如果您在重定向到給定的 session 時遇到問題，
`command.msg()` 通常是最安全的選擇。

您可以透過兩種主要方式取得 `session`：
* [帳戶](./Accounts.md) 和[物件](./Objects.md)（包括字元）具有`sessions` 屬性。
這是一個*處理程式*，追蹤所有附加到或操縱它們的Sessions。使用e.g。
`accounts.sessions.get()` 取得附加到該實體的 Sessions 清單。
* Command 例項有一個 `session` 屬性，該屬性始終指向觸發的 Session
它（它總是一個）。如果不涉及 session，則為 `None`，例如當生物或
script 觸發指令。

(customizing-the-session-object)=
### 自訂Session物件

什麼時候需要自訂 Session 物件？例如，考慮角色建立系統：您可能決定將其保持在不符合角色的層級。這意味著您在某種選單選擇結束時建立角色。實際的 char-create cmdset 通常會存入該帳戶。  只要您的`MULTISESSION_MODE`低於2，此功能就可以正常運作。對於更高的模式，替換帳戶cmdset將影響*所有*您連結的sessions，以及那些不參與角色建立的人。在這種情況下，您希望將 char-create cmdset 放在 Session 級別上 - 那麼所有其他 sessions 將繼續正常工作，儘管您在其中一個建立了新角色。

預設情況下，session 物件在使用者首次連線時取得 `commands.default_cmdsets.UnloggedinCmdSet`。一旦 session 透過身份驗證，它就沒有預設值。若要將「已登入」cmdset 新增至 Session，請使用 `settings.CMDSET_SESSION` 給出 cmdset 類別的路徑。這一套
從此以後，只要帳戶登入，就會始終存在。

若要進一步自訂，您可以使用自己的子類別完全覆蓋 Session。若要替換預設的 Session 類，請將 `settings.SERVER_SESSION_CLASS` 變更為指向您的自訂類別。這是一種危險的做法，錯誤很容易使您的遊戲無法玩。  請務必注意[原始](evennia.server.session)並仔細進行更改。

(portal-and-server-sessions)=
## Portal 和伺服器 Sessions

*注意：這被認為是一個高階主題。您不需要在第一次通讀時就知道這一點。 *

Evennia 分為兩部分，[Portal 和伺服器](./Portal-And-Server.md)。每一方都追蹤自己的Sessions，並將它們相互同步。

我們通常所說的「Session」實際上是`ServerSession`。 Portal 上的對應部分
邊是`PortalSession`。伺服器 sessions 處理遊戲狀態，而 portal session
處理連線協定本身的細節。兩者還充當關鍵的備份
資料，例如伺服器重新啟動時的資料。

新帳戶連線由 Portal 使用它理解的[協定](Portal-And- Server)（例如 telnet、ssh、webclient 等）偵聽和處理。建立新連線時，會在 Portal 端建立 `PortalSession`。這個 session 物件看起來有所不同，取決於用於連線的協議，但所有物件仍然具有對所有 sessions 通用的最小屬性集。

這些公共屬性透過 AMP 連線從 Portal 傳送到伺服器，伺服器現在被告知已建立新連線。  在伺服器端，建立一個 `ServerSession` 物件來表示這一點。只有`ServerSession`一種；無論帳戶如何連線，它看起來都是一樣的。

從現在開始，AMP一側的`ServerSession`之間是一對一的匹配
連線和 `PortalSession` 位於另一個連線上。  到達 Portal Session 的資料被傳送到
其映象伺服器session，反之亦然。

在某些情況下，portal- 和伺服器端 sessions 是
彼此「同步」：
- 玩家關閉他們的用戶端，殺死Portal Session。 Portal 與伺服器同步
確保相應的伺服器Session也被刪除。
- 玩家從遊戲內部退出，殺死伺服器Session。  然後伺服器與
Portal 以確保徹底關閉 Portal 連線。
- 伺服器重新啟動/重置/關閉 - 伺服器 Sessions 被複製（「儲存」）到
Portal 側。當伺服器恢復時，該資料由 Portal 傳回，因此兩者再次
同步。這樣，帳戶的登入狀態和其他連結關鍵的內容就可以在
伺服器重新啟動（顯然，假設 Portal 沒有同時停止）。

(sessionhandlers)=
### 會話處理程式

Portal 和伺服器都有一個 *sessionhandler* 來管理連線。這些處理程式
全域實體包含透過 AMP 橋中繼資料的所有方法。所有型別的
Sessions 持有其各自會話處理程式的參考（該屬性稱為
`sessionhandler`)，以便他們可以中繼資料。有關建構新協議的詳細資訊，請參閱[協議](../Concepts/Protocols.md)。

要取得遊戲中的所有 Sessions（i.e。所有目前連線的使用者端），您可以存取伺服器端 Session 處理程式，您可以透過該處理程式取得
```
from evennia.server.sessionhandler import SESSION_HANDLER
```
> 注意：`SESSION_HANDLER` 單例有一個較舊的別名 `SESSIONS`，它也常見於不同的地方。

有關 `ServerSessionHandler` 功能的詳細資訊，請參閱 [sessionhandler.py](evennia.server.sessionhandler) 模組。