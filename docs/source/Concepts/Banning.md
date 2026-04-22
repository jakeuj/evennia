(banning)=
# 班寧


無論是由於濫用、公然違反規則還是其他原因，您最終都會發現
沒有其他辦法，只能踢掉一個特別麻煩的球員。預設指令集有
管理工具來處理這個問題，主要是 `ban`、`unban` 和 `boot`。

假設我們有一個麻煩的玩家“YouSuck” - 這是一個拒絕一般禮貌的人 - 一個濫用和垃圾郵件的帳戶，顯然是由一些無聊的網路流氓建立的，只是為了引起悲傷。你已經嘗試過表現得友善。現在你只想讓這個巨魔消失。

(creating-a-ban)=
## 建立禁令

(name-ban)=
### 姓名禁令

最簡單的辦法是阻止帳戶 YouSuck 再次連線。

     ban YouSuck

這將lock名稱YouSuck（以及「yousuck」和任何其他大寫組合），下次他們嘗試使用此名稱登入時，伺服器將不允許他們！

您也可以給出一個原因，以便您稍後記住為什麼這是一件好事（被禁止的帳戶永遠不會看到這個）

     ban YouSuck:This is just a troll.

如果您確定這只是一個垃圾郵件帳戶，您甚至可以考慮徹底刪除玩家帳戶：

     accounts/delete YouSuck

一般來說，禁止該名稱是停止使用帳戶的更簡單、更安全的方法 - 如果您
如果您改變主意，您可以隨時刪除該阻止，而刪除是永久性的。

(ip-ban)=
### IP 禁止

僅僅因為您封鎖 YouSuck 的名字可能並不意味著該帳戶背後的惡意攻擊者會放棄。他們只需建立一個新帳戶 YouSuckMore 即可返回。讓事情變得更困難的一種方法是告訴伺服器不允許來自其特定 IP 位址的連線。

首先，當有問題的帳戶線上上時，檢查他們使用的是哪個 IP 地址。你可以這樣做
`who` 指令，它會顯示如下內容：

     Account Name     On for     Idle     Room     Cmds     Host          
     YouSuckMore      01:12      2m       22       212      237.333.0.223 

「主機」位是帳戶連線的 IP 位址。使用它來定義禁令而不是名稱：

     ban 237.333.0.223

這將阻止 YouSuckMore 從他們的電腦進行連線。但請注意，IP 位址可能會輕易更改 - 可能是由於玩家的 Internet 服務提供者的操作方式或使用者只是更換電腦所致。您可以透過將星號 `*` 作為地址中三位陣列的萬用字元來進行更全面的禁止。因此，如果您發現!YouSuckMore 主要從 `237.333.0.223`、`237.333.0.225` 和 `237.333.0.256` 連線（僅在其子網路中發生變化），則可能需要像這樣禁止以包含該子網路中的任何數字：

     ban 237.333.0.*

當然，您也應該將 IP 禁令與名稱禁令結合起來，這樣帳戶 YouSuckMore 就會真正被鎖定，無論他們從哪裡連線。

但要小心過度籠統的 IP 禁令（上面有更多星號）。如果您運氣不好，您可能會阻止恰好與犯罪者從同一子網連線的無辜玩家。

(lifting-a-ban)=
### 解除禁令

使用不帶任何引數的`unban`（或`ban`）指令，您將看到所有目前有效禁令的清單：

    Active bans
    id   name/ip       date                      reason 
    1    yousuck       Fri Jan 3 23:00:22 2020   This is just a Troll.
    2    237.333.0.*   Fri Jan 3 23:01:03 2020   YouSuck's IP.

使用此清單中的 `id` 找出要解除的禁令。

     unban 2
      
    Cleared ban 2: 237.333.0.*


(booting)=
## 開機

不過，YouSuck 並沒有真正注意到所有這些禁止 - 並且直到登出並嘗試再次登入後才會注意到。讓我們一起幫助巨魔吧。

     boot YouSuck

好擺脫。您也可以給出啟動的原因（在被踢出之前向玩家回顯）。

     boot YouSuck:Go troll somewhere else.

(summary-of-abuse-handling-tools)=
## 濫用處理工具摘要

以下是處理惱人玩家的其他有用指令。

- **誰** --（作為管理員）查詢帳戶的 IP。請注意，一個帳戶可以連線到
多個 IP，取決於您在設定中允許的內容。
- **檢查/帳戶託馬斯** -- 獲取有關帳戶的所有詳細資訊。您也可以使用 `*thomas` 來獲取
帳戶。如果沒有給出，您將獲得 *Object* thomas（如果它存在於同一位置），這
在這種情況下不是你想要的。
- **boot thomas** -- 啟動給定帳號名稱的所有 sessions。
- **boot 23** -- 透過其唯一 ID 啟動一個特定用戶端 session/IP。
- **ban** -- 列出所有禁令（以 id 列出）
- **ban thomas** -- 禁止具有給定帳戶名稱的使用者
- **ban/ip `134.233.2.111`** -- 被 IP 禁止
- **ban/ip `134.233.2.*`** -- 擴大 IP 禁令
- **ban/ip `134.233.*.*`** -- 更廣泛的 IP 禁令
- **unban 34** -- 刪除 ID #34 的禁令

- **cboot mychannel = thomas** -- 從您控制的頻道啟動訂閱者
- **clock mychannel = control:perm(Admin);listen:all();send:all()** -- 使用 [lock 定義](../Components/Locks.md) 精細控制對頻道的存取。

鎖定特定指令（如 `page`）是這樣完成的：
1. Examine the source of the command. [預設`page`指令類別]( https://github.com/evennia/evennia/blob/main/evennia/commands/default/comms.py#L686)具有lock字串**“cmd:not pperm(page_banned)”**。這意味著除非玩家擁有“許可權”“page_banned”，否則他們可以使用此指令。您可以分配任何 lock 字串，以允許在指令中進行更精細的自訂。您可能會尋找 [Attribute](../Components/Attributes.md) 或 [Tag](../Components/Tags.md) 的值、您目前的位置等。
2. **perm/account thomas = page_banned** -- 授予帳戶“許可權”，這會導致（在本例中）lock 失敗。

- **perm/del/account thomas = page_banned** -- 刪除給定的許可權
- **tel thomas =監獄** -- 傳送玩家至指定位置或#dbref
- **輸入 thomas = FlowerPot** -- 將煩人的玩家變成花盆（假設你已經準備好 `FlowerPot` typeclass）
- **userpassword thomas = fooBarFoo** -- 更改使用者的密碼
- **accounts/delete thomas** -- 刪除玩家帳號（不建議，使用 **ban** 代替）

- **伺服器** -- 顯示伺服器統計訊息，例如CPU負載、記憶體使用情況以及快取了多少物件
- **時間**－提供伺服器正常運作時間、運作時間等
- **reload** -- 重新載入伺服器而不斷開任何人的連線
- **重置** - 重新啟動伺服器，踢掉所有連線
- **shutdown** -- 冷停止伺服器而不再次自動啟動
- **py** —— 執行原始 Python 程式碼，允許動態直接檢查資料庫和帳戶物件。對於高階使用者。
