(creating-things)=
# 創造事物

我們已經創造了一些東西——例如龍。不過 Evennia 中有很多不同的東西可以創造。在 [Typeclasses 教學](./Beginner-Tutorial-Learning-Typeclasses.md) 中，我們注意到有 7 個預設的 Typeclasses 隨 Evennia 開箱即用：

| Evennia基礎typeclass | mygame.typeclasses 孩子 | 描述 |  
| --------------- |  --------------| ------------- | 
| `evennia.DefaultObject` | `typeclasses.objects.Object` | 一切都有位置 |
| `evennia.DefaultCharacter`（`DefaultObject` 的子級） | `typeclasses.characters.Character` | 玩家頭像 |
| `evennia.DefaultRoom`（`DefaultObject` 的子級） | `typeclasses.rooms.Room` | 遊戲內地點 | 
| `evennia.DefaultExit`（`DefaultObject` 的子代） | `typeclasses.exits.Exit` | 房間之間的連結 | 
| `evennia.DefaultAccount` | `typeclasses.accounts.Account` | 一個玩家帳號 | 
| `evennia.DefaultChannel` | `typeclasses.channels.Channel` | 遊戲內通訊 | 
|  `evennia.DefaultScript` | `typeclasses.scripts.Script` | 沒有位置的實體 | 

假設您有一個匯入的 Typeclass，有四種方法可以建立它的例項：

- 首先，你可以直接呼叫該類，然後`.save()`它：

        obj = SomeTypeClass(db_key=...)
        obj.save()

這有兩個操作的缺點；您還必須匯入該類別並且必須透過
   實際的資料庫欄位名稱，例如 `db_key` 而不是 `key` 作為關鍵字引數。這最接近「普通」Python 類別的工作方式，但不建議。
- 其次，您可以使用 Evennia 建立助手：

        obj = evennia.create_object(SomeTypeClass, key=...)

如果您嘗試用 Python 建立東西，這是推薦的方法。第一個引數可以是類別或 typeclass 的 python 路徑，例如 `"path.to.SomeTypeClass"`。也可以是 `None`，在這種情況下將使用 Evennia 預設值。雖然所有的創作方法
   在 `evennia` 上可用，它們實際上在 [evennia/utils/create.py](../../../api/evennia.utils.create.md) 中實現。每個不同的基底類別都有自己的建立函式，如`create_account`和`create_script`等。
- 第三，您可以對 Typeclass 本身使用 `.create` 方法：

    ```python
    obj, err = SomeTypeClass.create(key=...)
    ```
	Since `.create` is a method on the typeclass, this form is useful if you want to customize how the creation process works for your custom typeclasses. Note that it returns _two_ values - the `obj` is  either the new object or `None`, in which case `err` should be a list of error-strings detailing what went wrong.
- 最後，您可以使用遊戲內指令建立物件，例如

        create obj:path.to.SomeTypeClass

作為開發人員，您通常最好使用其他方法，但指令通常是讓沒有 Python 訪問許可權的普通玩家或構建者幫助構建遊戲世界的唯一方法。

(creating-objects)=
## 建立物件

[物件](../../../Components/Objects.md) 是最常見的建立型別之一。這些是從任何距離的 `DefaultObject` 繼承的實體。它們存在於遊戲世界中，包括房間、角色、出口、武器、花盆和城堡。

    > py
    > import evennia 
    > rose = evennia.create_object(key="rose")

由於我們沒有指定 `typeclass` 作為第一個引數，因此將使用 `settings.BASE_OBJECT_TYPECLASS` （開箱即用的 `typeclasses.objects.Object`）給出的預設值。

`create_object` 有[很多選項](evennia.utils.create.create_object)。程式碼中更詳細的範例：

```python 
from evennia import create_object, search_object

meadow = search_object("Meadow")[0]

lasgun = create_object("typeclasses.objects.guns.LasGun", 
					   key="lasgun", 
					   location=meadow,
					   attributes=[("desc", "A fearsome Lasgun.")])

```

在這裡，我們設定了武器的位置，並給了它一個 [Attribute](../../../Components/Attributes.md) `desc`，這是 `look` 指令在檢視這個和其他東西時將使用的。

(creating-rooms-characters-and-exits)=
## 建立房間、角色和出口

`Characters`、`Rooms` 和 `Exits` 都是 `DefaultObject` 的子類別。因此，例如沒有單獨的 `create_character`，您只需建立 `create_object` 指向 `Character` typeclass 的字元。

(linking-exits-and-rooms-in-code)=
### 在程式碼中連結出口和房間

`Exit` 是房間之間的單向連結。例如，`east` 可以是`Forest` 房間和`Meadow` 房間之間的`Exit`。

    Meadow -> east -> Forest 

`east` 出口的 `key` 為 `east`，`location` 為 `Meadow`，`destination` 為 `Forest`。如果您希望能夠從森林返回草地，則需要建立一個新的 `Exit`，例如 `west`，其中 `location` 是 `Forest`，`destination` 是 `Meadow`。

    Meadow -> east -> Forest 
	Forest -> west -> Meadow

在遊戲中，您可以使用 `tunnel` 和 `dig` 指令執行此操作，但如果您想在程式碼中設定這些連結，您可以這樣做：

```python
from evennia import create_object 
from mygame.typeclasses import rooms, exits 

# rooms
meadow = create_object(rooms.Room, key="Meadow")
forest = create_object(rooms.Room, key="Forest")

# exits 
create_object(exits.Exit, key="east", location=meadow, destination=forest)
create_object(exits.Exit, key="west", location=forest, destination=meadow)
```

(creating-accounts)=
## 建立帳戶

[帳號](../../../Components/Accounts.md) 是一個不正常的 (OOC) 實體，在遊戲世界中不存在。 
您可以在 `typeclasses/accounts.py` 中找到 Accounts 的父類別。

通常，您希望在使用者進行身份驗證時建立帳戶。預設情況下，這種情況發生在 `UnloggedInCmdSet` 中的 `create account` 和 `login` 預設指令中。這意味著自訂它只意味著替換這些指令！

因此，通常您會修改這些指令，而不是從頭開始製作一些東西。但原則是這樣的：

```python 
from evennia import create_account 

new_account = create_account(
            accountname, email, password, 
            permissions=["Player"], 
            typeclass="typeclasses.accounts.MyAccount"
 )
```
輸入通常是透過指令從玩家那裡獲取的。必須給出`email`，但如果您不使用它，可以是`None`。 `accountname` 在伺服器上必須是全域唯一的。 `password` 被加密儲存在資料庫中。  如果未給出 `typeclass`，則將使用 `settings.BASE_ACCOUNT_TYPECLASS` (`typeclasses.accounts.Account`)。


(creating-channels)=
## 建立頻道

[頻道](../../../Components/Channels.md)就像一個總機，用於在使用者之間傳送遊戲內訊息；就像 IRC- 或不和諧頻道，但在遊戲內部。

使用者透過`channel`指令與通道互動：

頻道/全部
	頻道/建立頻道名稱
	頻道/誰頻道名稱
	頻道/子頻道名稱
    ...
	(see 'help channel')

如果存在名為 `myguild` 的通道，使用者只需寫入通道名稱即可傳送訊息：

	> 我的公會 你好！我有一些問題...

建立通道遵循熟悉的語法：

```python 
from evennia import create_channel

new_channel = create_channel(channelname)
```

伺服器還可以透過設定 `DEFAULT_CHANNELS` 設定自動建立通道。有關詳細資訊，請參閱[通道檔案](../../../Components/Channels.md)。


(creating-scripts)=
## 正在建立Scripts

[Script](../../../Components/Scripts.md) 是一個沒有遊戲內位置的實體。它可用於儲存任意資料，通常用於需要永續性儲存但您無法在遊戲中「檢視」的遊戲系統。例如經濟系統、天氣和戰鬥處理程式。

Scripts 是多用途的，根據它們的用途，給定的 script 可以是「全域」的，也可以「附加到」另一個物件（如房間或角色）。

```python 
from evennia import create_script, search_object 
# global script 
new_script = create_script("typeclasses.scripts.MyScript", key="myscript")

# on-object script 
meadow = search_object("Meadow")[0]
new_script = create_script("typeclasses.scripts.MyScripts", 
						   key"myscript2", obj=meadow)

```

建立全域 scripts 的一個便捷方法是在 `GLOBAL_SCRIPTS` 設定中定義它們； Evennia 將確保初始化它們。 Scripts 還有一個可選的「計時器」元件。有關詳細資訊，請參閱專用的 [Script](../../../Components/Scripts.md) 檔案。

(conclusion)=
## 結論

任何遊戲都需要資料的永久儲存。這是如何建立型別分類實體的每種預設型別的快速概述。  如果您建立自己的typeclasses（作為預設typeclasses），則可以以相同的方式建立它們。

接下來我們將學習如何透過在資料庫中_搜尋_來再次找到它們。




