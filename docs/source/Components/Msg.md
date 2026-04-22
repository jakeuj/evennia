(msg)=
# 訊息

[Msg](evennia.comms.models.Msg) 物件表示資料庫儲存的通訊片段。將其視為一封獨立的電子郵件 - 它包含一條訊息、一些後設資料，並且始終有一個傳送者和一個或多個收件人。

一旦建立，訊息通常不會更改。它永久儲存在資料庫中。這允許全面記錄通訊。以下是 `Msg` 物件的一些好用處：

- page/tells（`page` 指令是 Evennia 開箱即用的方式）
- 公告板上的訊息
- 遊戲範圍內的電子郵件儲存在「郵箱」中。

```{important}

`Msg` 在遊戲中沒有任何代表。所以如果你想使用它們
  為了代表遊戲中的郵件/信件，實體信件永遠不會
  在房間裡可見（可能會被偷竊、監視等），除非你讓自己的
  間諜系統直接存取訊息（或不厭其煩地產生一個
  基於訊息的實際遊戲中字母物件）


```

```{versionchanged} 1.0
  Channels dropped Msg-support. Now only used in `page` command by default.
```

(working-with-msg)=
## 使用訊息

Msg 旨在專門在程式碼中使用，以建立其他遊戲系統。它_不是_ [Typeclassed](./Typeclasses.md) 實體，這表示它不能（輕易）被覆寫。它不支援屬性（但它_確實_支援[Tags](./Tags.md)）。由於每個訊息都會建立一條新訊息，因此它試圖做到精益化和小型化。 
您使用 `evennia.create_message` 建立一條新訊息：

```python
    from evennia import create_message
    message = create_message(senders, message, receivers,
                             locks=..., tags=..., header=...)
```

您可以透過多種方式搜尋 `Msg` 物件：


```python
  from evennia import search_message, Msg

  # args are optional. Only a single sender/receiver should be passed
  messages = search_message(sender=..., receiver=..., freetext=..., dbref=...)

  # get all messages for a given sender/receiver
  messages = Msg.objects.get_msg_by_sender(sender)
  messages = Msg.objects.get_msg_by_receiver(recipient)

```

(properties-on-msg)=
### 訊息屬性

- `senders` - 必須始終至少有一個寄件者。這是一組
- [帳戶](./Accounts.md)、[物件](./Objects.md)、[Script](./Scripts.md)
或 `str` 的任意組合（但通常訊息僅針對一種型別）。
  對寄件者使用 `str` 表示它是「外部」寄件者，並且
  並可用於指向不是型別分類實體的傳送者。預設不使用此功能
  這取決於系統（可能是唯一的 id 或
  例如，python 路徑）。雖然大多數系統都期望有一個傳送者，但它是
  可以有任意數量的。
- `receivers` - 這些是檢視訊息的人。這些又是以下任何組合
[帳號](./Accounts.md)、[物件](./Objects.md) 或 [Script](./Scripts.md) 或 `str`（「外部」接收者）。
  原則上可以有零個接收者，但 Msg 的大多數用法都需要一個或多個。
- `header` - 這是一個可選文字欄位，可以包含有關訊息的元資訊。為了
類似電子郵件的系統，它將作為主題行。這可以獨立搜尋，使得
  這是快速查詢訊息的強大場所。
- `message` - 正在傳送的實際文字。
- `date_sent` - 這會自動設定為訊息建立的時間（因此可能是傳送的時間）。
- `locks` - Evennia [lock 處理程式](./Locks.md)。與 `locks.add()` 等一起使用，並使用 `msg.access()` 檢查鎖
就像所有其他可鎖定實體一樣。這可用於限制對內容的訪問
  訊息的。要檢查的預設 lock 型別是 `'read'`。
- `hide_from` - 這是[帳戶](./Accounts.md) 或[物件](./Objects.md) 的可選列表，
將看不到此訊息。這種關係主要可用於最佳化
  原因是它允許快速過濾不適合給定的訊息
  目標。


(tempmsg)=
## TempMsg

[evennia.comms.models.TempMsg](evennia.comms.models.TempMsg) 是實現與常規 `Msg` 相同的 API 的物件，但它沒有資料庫元件（因此無法搜尋）。它旨在插入期望 `Msg` 但您只想處理訊息而不儲存訊息的系統。
