(monitorhandler)=
# MonitorHandler


*MonitorHandler* 是一個用於監視物件屬性或屬性變化的系統。一個
監視器可以被認為是一種響應變化的觸發器。

MonitorHandler 的主要用途是向用戶端報告變化；例如客戶端
Session 可能會要求 Evennia 監控角色 `health` Attribute 的值，並在它改變時回報。
這樣一來，用戶端就可以視需要更新自己的血量條圖形。

(using-the-monitorhandler)=
## 使用MonitorHandler

MontorHandler 是從單例 `evennia.MONITOR_HANDLER` 訪問的。處理程式的程式碼
位於 `evennia.scripts.monitorhandler` 中。

新增監視器的方法如下：

```python
from evennia import MONITOR_HANDLER

MONITOR_HANDLER.add(obj, fieldname, callback,
                    idstring="", persistent=False, **kwargs)

```

 - `obj`（[Typeclassed](./Typeclasses.md) 實體） - 要監視的物件。既然這一定是
typeclassed，這表示您無法使用監視器處理程式監視 [Sessions](./Sessions.md) 上的更改，例如
範例。
 - `fieldname` (str) - `obj` 上的欄位名稱或 [Attribute](./Attributes.md)。如果你想
監視資料庫欄位時，您必須指定其全名，包括起始`db_`（例如
`db_key`、`db_location` 等）。任何不以 `db_` 開頭的名稱都被假定為名稱
屬性。這種差異很重要，因為 MonitorHandler 會自動知道觀看
Attribute 的 `db_value` 欄位。
 - `callback`（可呼叫）- 這將被稱為 `callback(fieldname=fieldname, obj=obj, **kwargs)`
當欄位更新時。
 - `idstring` (str) - 用於分隔同一物件和欄位名稱上的多個監視器。
這是為了稍後正確識別和移除顯示器所必需的。它也用於
儲存它。
 - `persistent` (bool) - 如果為 True，監視器將在伺服器重新啟動後繼續存在。

例子：

```python
from evennia import MONITOR_HANDLER as monitorhandler

def _monitor_callback(fieldname="", obj=None, **kwargs):    
    # reporting callback that works both
    # for db-fields and Attributes
    if fieldname.startswith("db_"):
        new_value = getattr(obj, fieldname)
    else: # an attribute    
        new_value = obj.attributes.get(fieldname)
    obj.msg(f"{obj.key}.{fieldname} changed to '{new_value}'.")

# (we could add _some_other_monitor_callback here too)

# monitor Attribute (assume we have obj from before)
monitorhandler.add(obj, "desc", _monitor_callback)  

# monitor same db-field with two different callbacks (must separate by id_string)
monitorhandler.add(obj, "db_key", _monitor_callback, id_string="foo")  
monitorhandler.add(obj, "db_key", _some_other_monitor_callback, id_string="bar")

```

監視器由它正在監視的*物件例項*的組合來唯一標識
要在該物件及其 `idstring` 上監視的欄位/attribute 的 *名稱* (`obj` + `fieldname` +
`idstring`）。除非明確給出，否則 `idstring` 將是空字串。

因此，要「取消監控」上述內容，您需要提供足夠的資訊，以便系統能夠唯一地找到
要刪除的顯示器：

```
monitorhandler.remove(obj, "desc")
monitorhandler.remove(obj, "db_key", idstring="foo")
monitorhandler.remove(obj, "db_key", idstring="bar")
```
