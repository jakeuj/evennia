(objects)=
# 物件

**訊息路徑：**
```
┌──────┐ │   ┌───────┐    ┌───────┐   ┌──────┐
│Client├─┼──►│Session├───►│Account├──►│Object│
└──────┘ │   └───────┘    └───────┘   └──────┘
                                         ^
```

Evennia 中的所有遊戲內物體，無論是角色、椅子、怪物、房間或手榴彈，統稱為 Evennia *物體*。 An Object is generally something you can look and interact with in the game world. When a message travels from the client, the Object-level is the last stop.

物件構成了 Evennia 的核心，並且可能是您花費最多時間處理的物件。物件是[型別分類](./Typeclasses.md)實體。

根據定義，Evennia 物件是一個 Python 類，其父類中包含 [evennia.objects.objects.DefaultObject](evennia.objects.objects.DefaultObject)。 Evennia定義了`DefaultObject`的幾個子類別：

- `Object` - 遊戲中的基本實體。發現於`mygame/typeclasses/objects.py`。直接繼承自`DefaultObject`。
- [角色](./Characters.md) - 遊戲中的普通角色，由玩家控制。發現於`mygame/typeclasses/characters.py`。繼承自 `DefaultCharacter`，它是 `DefaultObject` 的子級。
- [房間](./Rooms.md) - 遊戲世界中的一個位置。發現於`mygame/typeclasses/rooms.py`。繼承自 `DefaultRoom`，而 `DefaultRoom` 又是 `DefaultObject` 的子級）。
- [Exits](./Exits.md) - 表示到另一位置的單向連線。在 `mygame/typeclasses/exits.py` 中找到（繼承自 `DefaultExit`，而 `DefaultExit` 又是 `DefaultObject` 的子級）。

(object)=
## 目的

**繼承樹：**
```
┌─────────────┐
│DefaultObject│
└──────▲──────┘
       │       ┌────────────┐
       │ ┌─────►ObjectParent│
       │ │     └────────────┘
     ┌─┴─┴──┐
     │Object│
     └──────┘
```

> 有關 `ObjectParent` 的說明，請參閱下一節。

`Object` 類別旨在用作建立既不是角色、房間也不是出口的事物的基礎 - 任何武器和盔甲、裝置和房屋都可以透過擴充套件 Object 類別來表示。根據您的遊戲，這也適用於 NPCs 和怪物（在某些遊戲中，您可能希望將 NPCs 視為只是一個非傀儡的 [角色](./Characters.md)）。

您不應該將物件用於遊戲_系統_。不要使用「隱形」物件來追蹤天氣、戰鬥、經濟或公會會員資格 - 這就是 [Scripts](./Scripts.md) 的用途。

(objectparent-adding-common-functionality)=
## ObjectParent - 新增常用功能

`Object` 以及 `Character`、`Room` 和 `Exit` 類別都另外繼承自 `mygame.typeclasses.objects.ObjectParent`。

`ObjectParent` 是一個空的「mixin」類別。您可以向此類新增您希望所有遊戲實體都具有的內容。

這是一個例子：

```python
# in mygame/typeclasses/objects.py
# ... 

from evennia.objects.objects import DefaultObject 

class ObjectParent:
    def at_pre_get(self, getter, **kwargs):
       # make all entities by default un-pickable
      return False
```

現在全部`Object`、`Exit`。 `Room` 和 `Character` 預設無法使用 `get` 指令拾取。

(working-with-children-of-defaultobject)=
## 與 DefaultObject 的兒童一起工作

此功能由 `DefaultObject` 的所有子類別共用。您可以透過修改遊戲目錄中的 typeclasses 之一或進一步繼承它們來輕鬆新增自己的遊戲內行為。

您可以將新的 typeclass 直接放入相關模組中，或者您可以以其他方式組織程式碼。這裡我們假設我們建立了一個新模組`mygame/typeclasses/flowers.py`：

```python
    # mygame/typeclasses/flowers.py

    from typeclasses.objects import Object

    class Rose(Object):
        """
        This creates a simple rose object        
        """    
        def at_object_creation(self):
            "this is called only once, when object is first created"
            # add a persistent attribute 'desc' 
            # to object (silly example).
            self.db.desc = "This is a pretty rose with thorns."     
```
   
現在你只需要用`create`指令指向*Rose*類別來製作一朵新的玫瑰：

     create/drop MyRose:flowers.Rose

`create` 指令實際上*做*的是使用 [evennia.create_object](evennia.utils.create.create_object) 函式。您可以在程式碼中自己做同樣的事情：

```python
    from evennia import create_object
    new_rose = create_object("typeclasses.flowers.Rose", key="MyRose")
```

（`create` 指令將自動將最可能的路徑附加到 typeclass，如果您手動輸入呼叫，則必須提供類別的完整路徑。`create.create_object` 函式功能強大，並且應該用於所有編碼物件建立（因此這是您在定義自己的建置指令時使用的）。

這個特定的 Rose 類別並沒有真正做太多事情，它所做的只是確保 attribute `desc`（這是 `look` 指令查詢的內容）是預先設定的，這是毫無意義的，因為您通常希望在構建時更改它（使用 `desc` 指令或使用 [Spawner](./Prototypes.md)）。
 
(properties-and-functions-on-objects)=
### 物件的屬性和函式

除了分配給所有 [typeclassed](./Typeclasses.md) 物件的屬性之外（請參閱該頁面的列表
其中），該物件還具有以下自訂屬性：

- `aliases` - 處理程式，允許您為此物件新增和刪除別名。使用 `aliases.add()` 新增別名，使用 `aliases.remove()` 刪除別名。
- `location` - 對目前包含此物件的物件的引用。
- `home` 是備份位置。主要動機是在物件 `location` 被破壞時有一個安全的地方可以將其移動到的地方。為了安全起見，所有物件通常都應該有一個固定位置。
- `destination` - 這儲存了對該物件以某種方式連結到的另一個物件的引用。它的主要用途是[退出](./Exits.md)，否則通常不設定。
- `nicks` - 與別名相反，[Nick](./Nicks.md) 擁有一個方便的暱稱替換真實姓名、單字或序列，僅對該物件有效。如果物件用作遊戲角色，這主要是有意義的 - 然後它可以儲存更短的短褲，例如以便快速引用遊戲指令或其他角色。使用 nicks.add（別名、真實姓名）新增名稱。
- `account` - 這包含控制此物件（如果有）的已連線 [帳戶](./Accounts.md) 的參考。請注意，如果控制帳戶目前「不」線上，也會設定此設定 - 若要測試帳戶是否線上，請改用 `has_account` 屬性。
- `sessions` - 如果設定了 `account` 欄位*並且帳戶線上*，這是所有活動 sessions（伺服器連線）的列表，用於聯絡他們（如果設定中允許多個連線，則可能不只一個）。
- `has_account` - 用於檢查*線上*帳戶目前是否連線到該物件的簡寫。
- `contents` - 這將傳回引用此物件「內部」的所有物件的清單（即，將此物件設為其 `location`）。
- `exits` - 這將傳回該物件內*退出*的所有物件，即設定了 `destination` 屬性。
- `appearance_template` - 當有人檢視物件時，這有助於格式化物件的外觀（請參閱下一節）。 l
- `cmdset` - 這是一個儲存在物件上定義的所有[指令集](./Command-Sets.md)（如果有）的處理程式。
- `scripts` - 這是管理附加到物件（如果有）的 [Scripts](./Scripts.md) 的處理程式。

該物件還具有許多有用的實用函式。有關引數和更多詳細資訊，請參閱 `src/objects/objects.py` 中的函式頭。

- `msg()` - 此函式用於將訊息從伺服器傳送到連線到此物件的帳戶。
- `msg_contents()` - 對該物件內的所有物件呼叫 `msg`。
- `search()` - 這是在給定位置或全域搜尋特定物件的便捷簡寫。它主要在定義指令時有用（在這種情況下，執行指令的物件被命名為 `caller`，並且可以執行 `caller.search()` 來查詢房間中要操作的物件）。
- `execute_cmd()` - 讓物件執行給定的字串，就像在指令列上給出的一樣。
- `move_to` - 將此物件完全移動到新位置。  這是主要的移動方法，將呼叫所有相關的鉤子，執行所有檢查等。
- `clear_exits()` - 將從該物件刪除所有到*和*的[退出](./Exits.md)。
- `clear_contents()` - 這不會刪除任何內容，而是將所有內容（退出除外）移至指定的 `Home` 位置。
- `delete()` - 刪除此物件，先呼叫 `clear_exits()` 和 `clear_contents()`。
- `return_appearance` 是讓物件直觀地描述自身的主要鉤子。

物件 Typeclass 定義了超出 `at_object_creation` 的更多*鉤子方法*。 Evennia 在不同的點呼叫這些鉤子。  實作自訂物件時，您將從基礎父級繼承並使用您自己的自訂程式碼過載這些掛鉤。有關所有可用掛鉤的更新列表，請參閱 `evennia.objects.objects` 或[此處 DefaultObject 的API](evennia.objects.objects.DefaultObject)。


(changing-an-objects-appearance)=
## 改變物件的外觀

當您鍵入 `look <obj>` 時，發生的事件順序如下：

1. 此指令檢查指令的 `caller`（「檢視器」）是否透過了目標 `obj` 的 `view` [lock](./Locks.md)。如果沒有，他們將找不到任何東西可看（這就是使物件不可見的方法）。
1. `look` 指令呼叫 `caller.at_look(obj)` - 也就是說，呼叫「looker」（指令的呼叫者）上的 `at_look` 掛鉤來對目標物件執行尋找。該指令將回顯該鉤子返回的任何內容。
2. `caller.at_look` 呼叫並傳回`obj.return_apperance(looker, **kwargs)` 的結果。這裡`looker`是指令的`caller`。換句話說，我們要求 `obj` 將自己描述為 `looker`。
3. `obj.return_appearance` 利用其 `.appearance_template` 屬性並呼叫一系列輔助鉤子來填充此模板。這是模板預設的樣子：

            ```python
            appearance_template = """
            {header}
            |c{name}|n
            {desc}
            {exits}{characters}{things}
            {footer}
            """```

4. 模板的每個欄位都由匹配的輔助方法填充（及其預設回傳）：
    - `name` -> `obj.get_display_name(looker, **kwargs)` - 回傳 `obj.name`。
    - `desc` -> `obj.get_display_desc(looker, **kwargs)` - 回傳 `obj.db.desc`。
    - `header` -> `obj.get_display_header(looker, **kwargs)` - 預設為空。
    - `footer` -> `obj.get_display_footer(looker, **kwargs)` - 預設為空。
    - `exits` -> `obj.get_display_exits(looker, **kwargs)` - 在此物件內找到的 `DefaultExit` 繼承物件的清單（通常只有在 `obj` 是 `Room` 時才出現）。
    - `characters` -> `obj.get_display_characters(looker, **kwargs)` - 此物件內的 `DefaultCharacter` 繼承實體的清單。
    - `things` -> `obj.get_display_things(looker, **kwargs)` - `obj` 內所有其他物件的清單。
5. `obj.format_appearance(string, looker, **kwargs)` 是填充模板字串經歷的最後一步。這可用於最終調整，例如去除空白。使用者將看到此方法的傳回結果。

由於每個鉤子（以及模板本身）都可以在您的子類別中覆蓋，因此您可以廣泛地自訂您的外觀。您還可以讓物件看起來有所不同，具體取決於觀看它們的人。預設不會使用額外的`**kwargs`，但如果需要的話（例如光照條件等），可以允許您將額外的資料傳遞到系統中