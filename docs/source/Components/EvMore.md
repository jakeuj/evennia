(evmore)=
# EvMore


當向使用者使用者端傳送很長的文字時，它可能會滾動超出用戶端的高度
視窗。 `evennia.utils.evmore.EvMore` 類別使使用者能夠在遊戲中只檢視一個
一次一頁文字。它通常透過其訪問函式`evmore.msg` 使用。

這個名稱來自著名的 UNIX 尋呼機實用程式 *more*，它只執行此功能。

要使用尋呼機，只需將長文字傳遞給它：

```python
from evennia.utils import evmore

evmore.msg(receiver, long_text)
```
其中接收者是[物件](./Objects.md)或[帳戶](./Accounts.md)。如果文字長於
用戶端的螢幕高度（由 NAWS 握手或 `settings.CLIENT_DEFAULT_HEIGHT` 決定）
尋呼機將會出現，如下圖所示：

>[...]
在 voluptate velit 中的 reprehenderit 中的急性 irure dolor
esse cillum dolore eu fugiat nulla pariatur。例外者
Sint Occaecat cupidatat non proident, sunt in culpa qui
Officia deserunt mollit anim id est labourum。

>(**更多** [1/6] 返回**n**|**b**ack|**t**op|**e**nd|**a**bort)


使用者可以按回車鍵移至下一頁，或使用建議的
指令跳至檔案的上一頁、頂部或底部以及中止
尋呼。

尋呼機還需要幾個關鍵字引數來控制訊息輸出。請參閱
[evmore-API](github:evennia.utils.evmore) 以瞭解更多資訊。
