(locks)=
# 鎖具


對於大多數遊戲來說，限制人們可以做的事情是個好主意。在 Evennia 中，此類限制由稱為「鎖」的東西應用和檢查。所有 Evennia)、[Scripts](./Scripts.md)、[帳戶](./Accounts.md)、[幫助系統](./Help-System.md)、[訊息](./Msg.md) 和 [通道](./Channels.md) 均透過鎖定存取。

lock 可以被視為限制 Evennia 實體的特定使用的「存取規則」。
每當另一個實體想要這種存取許可權時，lock 將以不同的方式分析該實體，以確定是否應授予存取許可權。 Evennia 實現了「鎖定」理念 - 所有實體都不可訪問，除非您明確定義允許部分或完全訪問的 lock。

讓我們舉個例子：一個物件本身有一個lock，它限制了人們「刪除」該物件的方式。除了知道它限制刪除之外，lock 還知道只有特定 ID（例如 `34`）的玩家才允許刪除它。因此，每當玩家嘗試在物件上執行 `delete` 時，`delete` 指令都會確保檢查該玩家是否真的被允許這樣做。它呼叫 lock，後者檢查玩家的 id 是否為 `34`。只有這樣，它才會允許 `delete` 繼續其工作。

(working-with-locks)=
## 使用鎖

遊戲中設定物件鎖定的指令是`lock`：

     > lock obj = <lockstring>

`<lockstring>` 是某種形式的字串，定義了 lock 的行為。我們將在下一節中更詳細地介紹 `<lockstring>` 的外觀。

從程式碼角度來看，Evennia 透過所有相關實體上通常稱為 `locks` 的方式處理鎖定。這是一個允許您新增、刪除和檢查鎖定的處理程式。

```python
     myobj.locks.add(<lockstring>)
```

人們可以呼叫 `locks.check()` 來執行 lock 檢查，但為了隱藏底層實現，所有物件還具有一個名為 `access` 的便利函式。最好應該使用這個。在下面的範例中，`accessing_obj` 是請求「刪除」存取的物件，而 `obj` 是可能被刪除的物件。這就是 `delete` 指令內部的樣子（而且確實如此）：

```python
     if not obj.access(accessing_obj, 'delete'):
         accessing_obj.msg("Sorry, you may not delete that.")
         return
```

(defining-locks)=
### 定義鎖

在 Evennia 中定義 lock（i.e。存取限制）是透過新增 lock 的簡單字串來完成的
使用 `obj.locks.add()` 定義物件的 `locks` 屬性。

以下是 lock 字串的一些範例（不包括引號）：

```python
     delete:id(34)   # only allow obj #34 to delete
     edit:all()      # let everyone edit
     # only those who are not "very_weak" or are Admins may pick this up
     get: not attr(very_weak) or perm(Admin)
```

形式上，鎖字串具有以下語法：

```python
     access_type: [NOT] lockfunc1([arg1,..]) [AND|OR] [NOT] lockfunc2([arg1,...]) [...]
```

其中 `[]` 標記可選部分。 `AND`、`OR` 和 `NOT` 不區分大小寫，多餘的空格將被忽略。 `lockfunc1, lockfunc2` 等是 lock 系統可用的特殊_鎖定函式_。

因此，鎖字串由限制型別（`access_type`）、冒號（`:`）和涉及函式呼叫的表示式組成，該函式呼叫確定透過lock 所需的內容。每個函式傳回 `True` 或 `False`。 `AND`、`OR` 和 `NOT` 的運作方式與 Python 中的正常運作方式相同。如果總結果是`True`，則lock透過。

您可以透過在鎖定字串中以分號 (`;`) 分隔來依序建立多個 lock 型別。下面的字串產生與前面的範例相同的結果：

    delete:id(34);edit:all();get: not attr(very_weak) or perm(Admin)


(valid-access_types)=
### 有效access_types

`access_type` 是鎖定字串的第一部分，定義 lock 控制哪種功能，例如「刪除」或「編輯」。原則上您可以為 `access_type` 命名任何名稱，只要它對於特定物件是唯一的即可。存取型別的名稱不區分大小寫。

但是，如果您想確保使用 lock，則應選擇您（或預設指令集）實際檢查的 `access_type` 名稱，如上面使用「刪除」`access_type` 的 `delete` 範例。

以下是預設指令集檢查的access_types。

- [指令](./Commands.md)
    - `cmd` - 這定義了誰可以呼叫此指令。
- [物件](./Objects.md):
    - `control` - 誰是物件的「所有者」。可以設定鎖、刪除等。預設為物件的建立者。
    - `call` - 誰可以呼叫儲存在該物件上的物件指令（物件本身除外）。預設情況下，物件與同一位置的任何人共用其指令（e.g。因此您可以「按下」房間中的 `Button` 物件）。對於角色和生物（他們可能只為自己使用這些指令並且不想共享它們），通常應該完全關閉它，使用類似 `call:false()` 的東西。
    - `examine` - 誰可以檢查該物件的屬性。
   - `delete` - 誰可以刪除該物件。
   - `edit` - 誰可以編輯物件的特性和屬性。
   - `view` - `look` 指令是否會在描述中顯示/列出此物件，以及您是否能夠看到其描述。請注意，如果您專門透過名稱來定位它，系統仍然會找到它，只是無法檢視它。請參閱 `search` lock 以完全隱藏該專案。
   - `search` - 這控制是否可以使用 `DefaultObject.search` 方法找到物件（通常在指令中以 `caller.search` 引用）。這就是建立完全「不可檢測」的遊戲內物件的方法。如果未明確設定此 lock，則假定所有物件均可搜尋。
   - `get`- 誰可以撿起該物體並隨身攜帶。
   - `puppet` - 誰可以「成為」這個物件並控制它作為他們的「角色」。
   - `attrcreate` - 誰可以在物件上建立新屬性（預設 True）
- [字](./Objects.md#characters):
  - 與物件相同
- [退出](./Objects.md#exits):
  - 與物件相同
  - `traverse` - 誰可以透過出口。
- [帳戶](./Accounts.md):
  - `examine` - 誰可以檢查帳戶的屬性。
  - `delete` - 誰可以刪除該帳戶。
  - `edit` - 誰可以編輯帳戶的屬性和特性。
  - `msg` - 誰可以向該帳戶傳送訊息。
  - `boot` - 誰可以啟動該帳戶。
- [屬性](./Attributes.md)：（僅由`obj.secure_attr`檢查）
  - `attrread` - 檢視/訪問 attribute
  - `attredit` - 更改/刪除 attribute
- [頻道](./Channels.md):
  - `control` - 誰在管理頻道。這意味著能夠刪除頻道、啟動偵聽器等。
  - `send` - 誰可以傳送到頻道。
  - `listen` - 誰可以訂閱和收聽該頻道。
- [HelpEntry](./Help-System.md):
  - `view` - 幫助條目標題是否應顯示在幫助索引中
  - `read` - 誰可以檢視此幫助條目（通常是所有人）
  - `edit` - 誰可以編輯此幫助條目。

舉個例子，每當要遍歷出口時，都會檢查*traverse*型別的lock。因此，為退出物件定義適當的 lock 型別將涉及鎖定字串 `traverse: <lock functions>`。
(custom-access_types)=
### 自訂access_types

如上所述，lock 的 `access_type` 部分只是 lock 的「名稱」或「型別」。文字是任意字串，對於物件來說必須是唯一的。如果新增與物件上已存在的`access_type` 相同的lock，則新的lock 會覆蓋舊的lock。

例如，如果您想要建立一個公告板系統並想要限制誰可以閱讀公告板或在公告板上釋出。然後您可以定義鎖，例如：

```python
     obj.locks.add("read:perm(Player);post:perm(Admin)")
```

這將為具有 `Player` 或以上許可權的角色建立「讀取」存取型別，並為具有 `Admin` 或以上許可權的角色建立「發布」存取型別（請參閱下方 `perm()` lock 函式的工作原理）。  當需要測試這些許可權時，只需像這樣檢查（在本範例中，`obj` 可能是公告板系統上的一塊板，`accessing_obj` 是嘗試讀取板的玩家）：

```python
     if not obj.access(accessing_obj, 'read'):
         accessing_obj.msg("Sorry, you may not read that.")
         return
```

(lock-functions)=
### Lock 函式

_lock 函式_ 是一個普通的 Python 函式，放​​置在 Evennia 尋找此類函式的位置。模組Evennia檢視的是清單`settings.LOCK_FUNC_MODULES`。 *任何這些模組中的所有函式*將自動被視為有效的 lock 函式。預設值位於 `evennia/locks/lockfuncs.py` 中，您可以在 `mygame/server/conf/lockfuncs.py` 中開始新增自己的值。您可以附加設定以新增更多模組路徑。要替換預設的 lock 函式，只需新增您自己的同名函式即可。

這是 lock 函式的基本定義：

```python 
def lockfunc_name(accessing_obj, accessed_obj, *args, **kwargs):
    return True # or False
```
`accessing object` 是想要存取的物件。  `accessed object` 是正在訪問的物件（帶有 lock 的物件）。該函式始終傳回一個布林值，確定 lock 是否透過。

`*args` 將成為賦予 lockfunc 的引數元組。因此，對於鎖定字串 `"edit:id(3)"` （名為 `id` 的 lockfunc）， lockfunc 中的 `*args` 將是 `(3,)` 。

`**kwargs` 字典有一個始終由 Evennia 提供的預設關鍵字，即 `access_type`，它是一個正在檢查存取型別的字串。對於鎖定字串 `"edit:id(3)"`，`access_type"` 將是 `"edit"`。預設未使用此值 Evennia。

lock 定義中明確給出的任何引數都會顯示為額外引數。

```python
# A simple example lock function. Called with e.g. `id(34)`. This is
# defined in, say mygame/server/conf/lockfuncs.py

def id(accessing_obj, accessed_obj, *args, **kwargs):
    if args:
        wanted_id = args[0]
        return accessing_obj.id == wanted_id
    return False
```

例如，上面的內容可以用在 lock 函式中，如下所示：

```python
    # we have `obj` and `owner_object` from before
    obj.locks.add(f"edit: id({owner_object.id})")
```

我們可以檢查“edit”lock 是否透過，如下所示：

```python
    # as part of a Command's func() method, for example
    if not obj.access(caller, "edit"):
        caller.msg("You don't have access to edit this!")
        return
```

在此範例中，除了具有正確 `id` 的 `caller` 之外，每個人都會收到錯誤。

> （使用 `*` 和 `**` 語法會導致 Python 神奇地將所有額外引數分別放入清單 `args` 中，並將所有關鍵字引數放入字典 `kwargs` 中。如果您不熟悉 `*args` 和 `**kwargs` 的工作原理，請參閱 Python 手冊）。

一些有用的預設值lockfuncs（有關更多資訊，請參閱`src/locks/lockfuncs.py`）：

- `true()/all()` - 授予所有人存取許可權
- `false()/none()/superuser()` - 不授予任何存取許可權。超級使用者完全繞過檢查，因此是唯一能夠透過此檢查的使用者。
- `perm(perm)` - 這嘗試匹配給定的 `permission` 屬性，首先在帳戶上，其次在角色上。參見[下文](./Permissions.md)。
- `perm_above(perm)` - 與 `perm` 類似，但需要比給定的許可權等級「更高」的許可權。
- `id(num)/dbref(num)` - 檢查 access_object 是否有特定的 dbref/id。
- `attr(attrname)` - 檢查 accessing_object 上是否存在某個 [Attribute](./Attributes.md)。
- `attr(attrname, value)` - 檢查 accessing_object 上是否存在 attribute *並且* 具有給定值。
- `attr_gt(attrname, value)` - 檢查 accessing_object 的值是否大於給定值 (`>`)。
- `attr_ge, attr_lt, attr_le, attr_ne` - 對應於 `>=`、`<`、`<=` 和 `!=`。
- `tag(tagkey[, category])` - 檢查 accessing_object 是否有指定的 tag 和可選類別。
- `objtag(tagkey[, category])` - 檢查 *accessed_object* 是否有指定的 tag 和選用類別。
- `objloctag(tagkey[, category])` - 檢查 *accessed_obj* 的位置是否有指定的 tag 和可選類別。
- `holds(objid)` - 檢查存取物件是否包含給定名稱或資料庫參考的物件。
- `inside()` - 檢查訪問對像是否位於被訪問物件內部（`holds()` 的相反）。
- `pperm(perm)`、`pid(num)/pdbref(num)` - 與 `perm`、`id/dbref` 相同，但始終尋找 *帳戶* 的許可權和 dbref，而不是字元。
- `serversetting(settingname, value)` - 僅當 Evennia 具有給定設定或設定為給定值時才傳回 True。

(checking-simple-strings)=
### 檢查簡單字串

有時你並不真的需要查詢某個lock，你只是想檢查一個鎖定字串。常見用途是在指令內部，以檢查使用者是否具有特定許可權。鎖定處理程式有一個方法 `check_lockstring(accessing_obj, lockstring, bypass_superuser=False)` 允許這樣做。

```python
     # inside command definition
     if not self.caller.locks.check_lockstring(self.caller, "dummy:perm(Admin)"):
         self.caller.msg("You must be an Admin or higher to do this!")
         return
```

請注意，此處 `access_type` 可以保留為虛擬值，因為此方法實際上並未執行 Lock 查詢。

(default-locks)=
### 預設鎖

Evennia 在所有新物件和帳戶上設定一些基本鎖（如果我們不這樣做，那麼從一開始就沒有人可以存取任何內容）。  這些都是在相應實體的根 [Typeclasses](./Typeclasses.md) 中定義的，在鉤子方法 `basetype_setup()` 中（您通常不想編輯它，除非您想更改房間和出口等基本內容儲存其內部變數的方式）。這在 `at_object_creation` 之前被呼叫一次，因此只需將它們放入子物件的後一個方法中即可更改預設值。此外，像 `create` 這樣的建立指令會更改您建立的物件的鎖定 - 例如，它設定 `control` lock_type 以便允許您（其建立者）控制和刪除該物件。


(more-lock-definition-examples)=
## 更多 Lock 定義範例

    examine: attr(eyesight, excellent) or perm(Builders)

只有當您具有「優秀」視力（即具有您自己定義的 Attribute `eyesight` 且值為 `excellent` 的值）或分配有「Builders」許可權字串時，您才可以對此物件進行*檢查*。

    open: holds('the green key') or perm(Builder)

這可以透過「門」物件上的 `open` 指令來呼叫。如果您是建造者或庫存中有正確的鑰匙，則檢查透過。

    cmd: perm(Builders)

Evennia 的指令處理程式會尋找 `cmd` 型別的 lock 以確定是否允許使用者呼叫特定指令。  當你定義一個指令時，這是你必須設定的lock。請參閱預設指令集以取得大量範例。如果角色/帳戶未透過 `cmd` lock 型別，則該指令甚至不會出現在其 `help` 清單中。

    cmd: not perm(no_tell)

「許可權」也可用於阻止使用者或實施高度具體的禁令。上面的範例將作為 lock 字串新增至 `tell` 指令中。這將允許每個*不*具有「許可權」`no_tell` 的人使用 `tell` 指令。您可以輕鬆地授予帳戶“許可權”`no_tell`，以禁止其使用此特定指令。


```python
    dbref = caller.id
    lockstring = "control:id(%s);examine:perm(Builders);delete:id(%s) or perm(Admin);get:all()" %
(dbref, dbref)
    new_obj.locks.add(lockstring)
```

這就是 `create` 指令設定新物件的方式。依序，此許可權字串將此物件的擁有者設定為建立者（執行 `create` 的人）。建構者可以檢查物件，而只有管理員和建立者可以刪除它。大家都可以撿起來。

(a-complete-example-of-setting-locks-on-an-object)=
### 給物件設定鎖的完整範例

假設我們有兩個物件 - 一個是我們自己（不是超級使用者），另一個是 [Object](./Objects.md)
稱為`box`。

     > create/drop box
     > desc box = "This is a very big and heavy box."

我們想要限制哪些物體可以拿起這個沉重的盒子。假設要做到這一點，我們要求未來的舉重運動員本身俱有 attribute *力量*，其值大於 50。我們首先將其分配給我們自己。

     > set self/strength = 45

好的，為了測試我們讓自己變得強大，但還不夠強大。  現在我們需要看看當有人試圖拿起盒子時會發生什麼 - 他們使用 `get` 指令（在預設設定中）。這是在 `evennia/commands/default/general.py` 中定義的。在它的程式碼中我們找到這個片段：

```python
    if not obj.access(caller, 'get'):
        if obj.db.get_err_msg:
            caller.msg(obj.db.get_err_msg)
        else:
            caller.msg("You can't get that.")
        return
```

因此 `get` 指令會找出型別為 *get* 的 lock （這並不奇怪）。它也在名為 _get_err_msg_ 的已檢查物件上尋找 [Attribute](./Attributes.md)，以便傳回自訂錯誤訊息。聽起來不錯！讓我們從在盒子上設定它開始：

     > set box/get_err_msg = You are not strong enough to lift this box.

接下來我們需要在我們的盒子上製作一個*get*型別的Lock。我們希望僅當訪問物件具有正確值的 attribute *強度* 時才傳遞它。為此，我們需要建立一個 lock 函式來檢查屬性的值是否大於給定值。幸運的是，Evennia 中已經包含了這樣一個（參見 `evennia/locks/lockfuncs.py`），稱為 `attr_gt`。

因此 lock 字串將如下所示：`get:attr_gt(strength, 50)`。  我們現在把它放在盒子上：

     lock box = get:attr_gt(strength, 50)

嘗試`get`該物體，你應該會收到我們不夠強大的訊息。然而，將你的力量提高到 50 以上，你就會毫無問題地拿起它。完畢！好重的一個箱子！

如果你想在 python 程式碼中設定它，它看起來像這樣：

```python

 from evennia import create_object

    # create, then set the lock
    box = create_object(None, key="box")
    box.locks.add("get:attr_gt(strength, 50)")

    # or we can assign locks in one go right away
    box = create_object(None, key="box", locks="get:attr_gt(strength, 50)")

    # set the attributes
    box.db.desc = "This is a very big and heavy box."
    box.db.get_err_msg = "You are not strong enough to lift this box."

    # one heavy box, ready to withstand all but the strongest...
```

(on-djangos-permission-system)=
## 淺談Django的許可權系統

Django 也實現了自己的全面許可權/安全系統。  我們不使用它的原因是因為它是以應用程式為中心的（Django 意義上的應用程式）。  其許可權字串的格式為`appname.permstring`，並且它會自動為應用程式中的每個資料庫模型新增其中三個 - 對於應用程式evennia/物件，這將是例如“object.create”、“object.admin”和“object.edit”。這對於 Web 應用程式來說很有意義，但對於 MUD 來說意義不大，尤其是當我們試圖隱藏盡可能多的底層架構時。

然而 django 許可權並沒有完全消失。我們用它來在登入期間驗證密碼。它還專門用於管理 Evennia 的基於 Web 的管理站點，這是 Evennia 資料庫的圖形前端。您可以直接從 Web 介面編輯和指派此類許可權。它獨立於上述許可權。
