(signals)=
# 訊號


_此功能從 evennia 0.9 及更高版本開始可用_。

您可以透過多種方式將自己的功能插入 Evennia 中。
最常見的方法是透過 *hooks* - typeclasses 上的方法
在特定事件中被呼叫。當你想要一個遊戲實體時，Hooks 是很棒的選擇
當事情發生時以某種方式行事。 _訊號_補充
當您想要輕鬆附加新功能而無需使用掛鉤的情況下
覆蓋 typeclass 上的內容。

當 Evennia 發生某些事件時，會觸發_Signal_。這個想法是
您可以將任意數量的事件處理程式「附加」到這些訊號。您可以附上
任意數量的處理程式，只要任何實體觸發，它們都會觸發
訊號。

Evennia使用[Django訊號系統](https://docs.djangoproject.com/en/4.1/topics/signals/)。


(working-with-signals)=
## 使用訊號

首先建立你的處理程式

```python

def myhandler(sender, **kwargs):
  # do stuff

```

`**kwargs` 是強制性的。然後將其附加到您選擇的訊號上：

```python
from evennia.server import signals

signals.SIGNAL_OBJECT_POST_CREATE.connect(myhandler)

```

此特定訊號在帳戶連線到遊戲（發布）後觸發。
發生這種情況時，`myhandler` 將觸發，`sender` 是剛剛連線的帳戶。

如果您只想回應特定實體的影響，您可以這樣做
像這樣：

```python
from evennia import search_account
from evennia import signals

account = search_account("foo")[0]
signals.SIGNAL_ACCOUNT_POST_CONNECT.connect(myhandler, account)
```

(available-signals)=
### 可用訊號

所有訊號（包括一些 django 特定的預設值）都在模組中可用
`evennia.server.signals`
（使用快捷方式`evennia.signals`）。訊號按傳送者型別命名。所以`SIGNAL_ACCOUNT_*`
回報
`Account` 例項作為寄件人，`SIGNAL_OBJECT_*` 傳回 `Object`s 等。額外關鍵字 (kwargs)
應該
從訊號處理程式中的 `**kwargs` 字典中提取。

- `SIGNAL_ACCOUNT_POST_CREATE` - 這在 `Account.create()` 的最後觸發。注意
呼叫`evennia.create.create_account`（由`Account.create`內部呼叫）將
*不是*
  觸發此訊號。這是因為使用 `Account.create()` 預計是最常用的
  使用者在登入時自行建立帳戶的方式。它透過並額外 kwarg `ip`
  連結帳戶的用戶端IP。
- `SIGNAL_ACCOUNT_POST_LOGIN` - 當帳戶經過身份驗證時，這將始終觸發。  傳送
涉及新的 [Session](./Sessions.md) 物件的額外 kwarg `session`。
- `SIGNAL_ACCCOUNT_POST_FIRST_LOGIN` - 這會在 `SIGNAL_ACCOUNT_POST_LOGIN` 之前觸發，但僅
如果
  這是完成的*第一個*連線（也就是說，如果沒有先前的 sessions 連線）。還有
  將 `session` 作為 kwarg 傳遞。
- `SIGNAL_ACCOUNT_POST_LOGIN_FAIL` - 當有人嘗試登入帳戶失敗時傳送。
通行證
  `session` 作為額外的 kwarg。
- `SIGNAL_ACCOUNT_POST_LOGOUT` - 當帳戶登出時總是觸發，無論其他sessions
留下或不留下。將斷開連線 `session` 作為 kwarg 傳遞。
- `SIGNAL_ACCOUNT_POST_LAST_LOGOUT` - 在 `SIGNAL_ACCOUNT_POST_LOGOUT` 之前觸發，但前提是這是
*最後* Session 中斷該帳戶的連線。將 `session` 作為 kwarg 傳遞。
- `SIGNAL_OBJECT_POST_PUPPET` - 當帳戶操縱此物件時觸發。額外的 kwargs `session`
`account` 代表傀儡實體。
  `SIGNAL_OBJECT_POST_UNPUPPET` - 當傳送物件未被操縱時觸發。額外的 kwargs 是
  `session`和`account`。
- `SIGNAL_ACCOUNT_POST_RENAME` - 由`Account.username`的設定觸發。額外透過
夸克`old_name`，`new_name`。
- `SIGNAL_TYPED_OBJECT_POST_RENAME` - 當任何 Typeclassed 實體的 `key` 變更時觸發。
額外
  傳遞的 kwargs 是 `old_key` 和 `new_key`。
- `SIGNAL_SCRIPT_POST_CREATE` - 在任何鉤子之後首次建立 script 時觸發。
- `SIGNAL_CHANNEL_POST_CREATE` - 在任何鉤子之後首次建立 Channel 時觸發。
- `SIGNAL_HELPENTRY_POST_CREATE` - 首次建立幫助條目時觸發。
- `SIGNAL_EXIT_TRAVERSED` - 當穿過出口時觸發，就在 `at_traverse` 鉤子之後。 `sender` 是出口本身，`traverser=` 關鍵字儲存遍歷出口的出口。

`evennia.signals` 模組還可讓您輕鬆存取預設的 Django 訊號（這些
使用一個
不同的命名約定）。

- `pre_save` - 在任何儲存之前觸發任何資料庫實體的 `.save` 方法時觸發
發生了。
- `post_save` - 儲存資料庫實體後觸發。
- `pre_delete` - 在刪除資料庫實體之前觸發。
- `post_delete` - 刪除資料庫實體後觸發。
- `pre_init` - 在 typeclass' `__init__` 方法之前觸發（依序
發生在 `at_init` 鉤子觸發之前）。
- `post_init` - 在 `__init__` 末尾觸發（仍在 `at_init` 掛鉤之前）。

這些是高度專業化的 Django 訊號，對大多數使用者來說不太可能有用。但是
為了完整起見，將它們包含在此處。

- `m2m_changed` - 在多對多欄位（如 `db_attributes`）更改後觸發。
- `pre_migrate` - 在資料庫遷移以 `evennia migrate` 開始之前觸發。
- `post_migrate` - 資料庫遷移完成後觸發。
- `request_started` - 當 HTTP 請求開始時傳送。
- `request_finished` - 當 HTTP 請求結束時傳送。
- `settings_changed` - 因 `@override_settings` 更改設定時傳送
裝飾器（僅與單元測試相關）
- `template_rendered` - 當測試系統呈現http模板時傳送（僅對單元測試有用）。
- `connection_creation` - 與資料庫初始連線時傳送。
