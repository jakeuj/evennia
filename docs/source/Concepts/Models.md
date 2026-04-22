(new-models)=
# 新型號

*注意：這被認為是一個高階主題。 *

Evennia 提供了許多方便的方法來儲存物件資料，例如透過屬性或Scripts。這對於大多數用例來說已經足夠了。但如果您的目標是建立一個大型獨立系統，嘗試將儲存需求壓縮到這些系統中可能會比您想像的更複雜。範例可能是儲存公會資料以便公會成員能夠更改、追蹤整個遊戲經濟系統中的資金流動或實現需要以快速存取的方式儲存自訂資料的其他自訂遊戲系統。

雖然 [Tags](../Components/Tags.md) 或 [Scripts](../Components/Scripts.md) 可以處理許多情況，但有時透過新增您自己的_資料庫模型_可能會更容易處理。

(overview-of-database-tables)=
## 資料庫表格概述

SQL-型別資料庫（這是Evennia支援的）基本上是高度最佳化的系統
檢索儲存在表中的文字。表格可能看起來像這樣

```
     id | db_key    | db_typeclass_path          | db_permissions  ...
    ------------------------------------------------------------------
     1  |  Griatch  | evennia.DefaultCharacter   | Developers       ...
     2  |  Rock     | evennia.DefaultObject      | None            ...
```

資料庫中的每一行都相當長。每列稱為一個“欄位”，每行都是一個單獨的物件。你可以自己檢查一下。如果您使用預設的 sqlite3 資料庫，請前往您的遊戲資料夾並執行

     evennia dbshell

您將進入資料庫 shell。在那裡，嘗試：

     sqlite> .help       # view help

     sqlite> .tables     # view all tables

     # show the table field names for objects_objectdb
     sqlite> .schema objects_objectdb

     # show the first row from the objects_objectdb table
     sqlite> select * from objects_objectdb limit 1;

     sqlite> .exit

Evennia 使用 [Django](https://docs.djangoproject.com)，它抽象化了資料庫 SQL 操作，並允許您完全在 Python 中搜尋和操作資料庫。每個資料庫表在 Django 中都由一個通常稱為「模型」的類別表示，因為它描述了表的外觀。 Evennia、物件、Scripts、通道等是 Django 模型的範例，我們隨後對其進行擴充套件和建置。

(adding-a-new-database-table)=
## 新增新的資料庫表

以下是新增自己的資料庫表格/模型的方法：

1. 用 Django 術語來說，我們將建立一個新的「應用程式」——主 Evennia 程式下的子系統。對於本範例，我們將其稱為“myapp”。執行以下指令（在執行此操作之前，您需要執行有效的 Evennia，因此請確保您已先執行 [安裝快速入門](Getting- Started) 中的步驟）：

        evennia startapp myapp
        mv myapp world  (linux)
        move myapp world   (windows)

1. 將建立一個新資料夾 `myapp`。從現在開始，「myapp」也將是名稱（「應用程式標籤」）。我們將其移至此處的 `world/` 子資料夾中，但如果更有意義，您可以將其保留在 `mygame` 的根目錄中。 1. `myapp`資料夾包含一些空的預設檔。我們現在感興趣的是`models.py`。在 `models.py` 中您定義您的模型。每個模型將是資料庫中的一個表。請參閱下一部分，在新增所需模型之前不要繼續。
1. 現在您需要告訴 Evennia 您的應用程式的模型應該是您的資料庫方案的一部分。將此行新增至您的 `mygame/server/conf/settings.py` 檔案（確保使用放置 `myapp` 的路徑，並且不要忘記元組末尾的逗號）：

    ```
    INSTALLED_APPS = INSTALLED_APPS + ("world.myapp", )
    ```

1. 從`mygame/`開始，執行

        evennia makemigrations myapp
        evennia migrate myapp

這會將您的新資料庫表新增至資料庫。如果您已將遊戲置於版本控制之下（如果沒有，[您應該](../Coding/Version-Control.md)），請不要忘記 `git add myapp/*` 新增所有專案
到版本控制。

(defining-your-models)=
## 定義你的模型

Django *模型* 是資料庫表的 Python 表示。它可以像任何其他 Python 類別一樣處理。它在自身上定義了“欄位”，即特殊型別的物件。這些成為資料庫表的「列」。最後，您建立模型的新例項以將新行新增至資料庫。

我們不會在這裡描述 Django 模型的所有方面，因為我們參考了有關該主題的大量 [Django 檔案](https://docs.djangoproject.com/en/4.1/topics/db/models/)。這是一個（非常）簡短的例子：

```python
from django.db import models

class MyDataStore(models.Model):
    "A simple model for storing some data"
    db_key = models.CharField(max_length=80, db_index=True)
    db_category = models.CharField(max_length=80, null=True, blank=True)
    db_text = models.TextField(null=True, blank=True)
    # we need this one if we want to be
    # able to store this in an Evennia Attribute!
    db_date_created = models.DateTimeField('date created', editable=False,
                                            auto_now_add=True, db_index=True)
```

我們建立四個欄位：兩個有限長度的字元欄位和一個沒有長度的文字欄位
最大長度。最後我們建立一個包含我們建立該物件的當前時間的欄位。

> 如果您希望能夠將自訂模型的例項儲存在 Evennia [Attribute](../Components/Attributes.md) 中，則具有此名稱的 `db_date_created` 欄位是*必需的*。它會在建立時自動設定，之後就無法更改。擁有此欄位將允許您執行 e.g。 `obj.db.myinstance = mydatastore`。如果您知道永遠不會將模型例項儲存在屬性中，則 `db_date_created` 欄位是可選的。

您*必須*以 `db_` 開頭欄位名稱，這是 Evennia 約定。儘管如此，還是建議您使用 `db_`，部分是為了與 Evennia 保持清晰和一致（如果您想共享您的程式碼），部分是為了您以後決定使用 Evennia 的情況
`SharedMemoryModel` 父級。

欄位關鍵字`db_index`為此欄位建立一個*資料庫索引*，這樣可以更快地尋找，因此建議將其放在您知道在查詢中經常使用的欄位上。 `null=True` 和 `blank=True` 關鍵字意味著這些欄位可以留空或設定為空字串，而資料庫不會抱怨。還有許多其他欄位型別和關鍵字來定義它們，請參閱 django 檔案以獲取更多資訊。

與使用 [django-admin](https://docs.djangoproject.com/en/4.1/howto/legacy-databases/) 類似，您可以執行 `evennia inspectdb` 來取得現有資料庫的模型資訊的自動清單。  與任何模型生成工具的情況一樣，您應該僅將其用作起點
為您的模型點。

(referencing-existing-models-and-typeclasses)=
## 引用現有模型和typeclasses

您可能需要使用 `ForeignKey` 或 `ManyToManyField` 將新模型與現有模型關聯起來。

為此，我們需要為要儲存為字串的根物件型別指定應用程式路徑（我們必須使用字串而不是直接使用類，否則您將遇到模型尚未初始化的問題）。

- `"objects.ObjectDB"` 適用於所有[物件](../Components/Objects.md)（如出口、房間、角色等）
- [帳戶](../Components/Accounts.md) `"accounts.AccountDB"`。
- `"scripts.ScriptDB"` 為 [Scripts](../Components/Scripts.md)。
- `"comms.ChannelDB"` 用於[頻道](../Components/Channels.md)。
- `"comms.Msg"` 用於 [Msg](../Components/Msg.md) 物件。
- `"help.HelpEntry"` 用於[幫助條目](../Components/Help-System.md)。

這是一個例子：

```python
from django.db import models

class MySpecial(models.Model):
    db_character = models.ForeignKey("objects.ObjectDB")
    db_items = models.ManyToManyField("objects.ObjectDB")
    db_account = modeles.ForeignKey("accounts.AccountDB")
```

這可能看起來違反直覺，但這將正確工作：

    myspecial.db_character = my_character  # a Character instance
    my_character = myspecial.db_character  # still a Character

這是有效的，因為當 `.db_character` 欄位載入到 Python 中時，實體本身知道它應該是 `Character` 並將其本身載入到該表單中。

這樣做的缺點是資料庫不會_強制_您儲存在關係中的物件型別。這是我們為 Typeclass 系統的許多其他優點所付出的代價。

雖然如果您嘗試儲存 `Account`，`db_character` 欄位會失敗，但它會很樂意接受繼承自 `ObjectDB` 的 typeclass 的任何例項，例如房間、出口或其他非字元物件。由您來驗證您儲存的內容是否符合您的預期。

(creating-a-new-model-instance)=
## 建立新的模型例項

若要在表中建立新行，請例項化模型，然後呼叫其 `save()` 方法：

```python
     from evennia.myapp import MyDataStore

     new_datastore = MyDataStore(db_key="LargeSword",
                                 db_category="weapons",
                                 db_text="This is a huge weapon!")
     # this is required to actually create the row in the database!
     new_datastore.save()

```

請注意，模型的 `db_date_created` 欄位未指定。它的標誌 `at_now_add=True` 確保在建立物件時將其設為當前日期（建立後也不能進一步更改）。

當您使用某些新欄位值更新現有物件時，請記住之後必須儲存該物件，否則資料庫將不會更新：

```python
    my_datastore.db_key = "Larger Sword"
    my_datastore.save()
```

Evennia 的普通模型不需要明確儲存，因為它們基於 `SharedMemoryModel` 而不是原始 django 模型。這將在下一節中介紹。

(using-the-sharedmemorymodel-parent)=
## 使用 `SharedMemoryModel` 父級

Evennia 的大部分模型並非基於原始 `django.db.models.Model`，而是基於 Evennia 基本模型 `evennia.utils.idmapper.models.SharedMemoryModel`。造成這種情況的主要原因有二：

1. 無需顯式呼叫`save()`即可輕鬆更新欄位
2. 物件記憶體永續性和資料庫快取

第一點（也是最不重要的一點）意味著只要您將欄位命名為 `db_*`，Evennia 就會自動為它們建立欄位包裝器。這種情況發生在模型的 [元類](http://en.wikibooks.org/wiki/Python_Programming/Metaclasses) 中，因此不會造成速度損失。包裝器的名稱將與欄位的名稱相同，減去 `db_` 字首。因此 `db_key` 欄位將有一個名為 `key` 的包裝屬性。然後你可以這樣做：

```python
    my_datastore.key = "Larger Sword"
```

且之後不必明確呼叫 `save()` 。儲存也在後臺以更有效的方式進行，使用 django 最佳化僅更新欄位而不是整個模型。請注意，如果您要手動將屬性或方法 `key` 新增至模型中，則將使用它而不是自動包裝器，並允許您根據需要完全自訂存取。

為瞭解釋第二個也是更重要的一點，請考慮以下使用預設 Django 模型父級的範例：

```python
    shield = MyDataStore.objects.get(db_key="SmallShield")
    shield.cracked = True # where cracked is not a database field
```

然後在另一個函式你做

```python
    shield = MyDataStore.objects.get(db_key="SmallShield")
    print(shield.cracked)  # error!
```

最後一個印出語句的結果是*未定義*！它可能*也許*隨機工作，但很可能您會因為找不到 `cracked` 屬性而得到 `AttributeError`。原因是`cracked`並不代表資料庫中的實際欄位。它只是在執行時新增的，因此 Django 不關心它。當您稍後檢索遮蔽匹配時，即使您搜尋相同的資料庫物件，也*不*保證您將獲得定義 `cracked` 的模型的*相同的 Python 例項*。

Evennia 嚴重依賴模型處理程式和其他動態建立的屬性。因此，Evennia 使用 `SharedMemoryModel`，而不是使用普通的 Django 模型，這會徵收名為 *idmapper* 的東西。 idmapper 快取模型例項，以便我們在第一次查詢給定物件後始終獲得*相同的*例項。使用 idmapper，上面的範例可以正常工作，您可以隨時檢索 `cracked` 屬性 - 直到所有非永續性資料消失後重新啟動。

使用 idmapper 對於*每個物件*來說更直觀、更有效率；它會減少很多
從磁碟讀取。缺點是該系統*總體*往往更需要記憶體。因此，如果您知道您 *永遠* 不需要向正在執行的例項新增新屬性，或者知道您將一直建立新物件但很少再次訪問它們（就像日誌系統一樣），那麼您最好製作「普通」Django 模型，而不是使用 `SharedMemoryModel` 及其 idmapper。

要使用 idmapper 和欄位包裝器功能，您只需讓模型類別繼承自 `evennia.utils.idmapper.models.SharedMemoryModel` 而不是預設的 `django.db.models.Model`：

```python
from evennia.utils.idmapper.models import SharedMemoryModel

class MyDataStore(SharedMemoryModel):
    # the rest is the same as before, but db_* is important; these will
    # later be settable as .key, .category, .text ...
    db_key = models.CharField(max_length=80, db_index=True)
    db_category = models.CharField(max_length=80, null=True, blank=True)
    db_text = models.TextField(null=True, blank=True)
    db_date_created = models.DateTimeField('date created', editable=False,
                                            auto_now_add=True, db_index=True)
```

(searching-for-your-models)=
## 搜尋您的型號

要搜尋新的自訂資料庫表，您需要使用其資料庫*管理器*來建立*查詢*。請注意，即使您按照上一節所述使用 `SharedMemoryModel`，您也必須在查詢中使用實際的*欄位名稱*，而不是包裝器名稱（因此 `db_key` 而不僅僅是 `key`）。

```python
     from world.myapp import MyDataStore

     # get all datastore objects exactly matching a given key
     matches = MyDataStore.objects.filter(db_key="Larger Sword")
     # get all datastore objects with a key containing "sword"
     # and having the category "weapons" (both ignoring upper/lower case)
     matches2 = MyDataStore.objects.filter(db_key__icontains="sword",
                                           db_category__iequals="weapons")
     # show the matching data (e.g. inside a command)
     for match in matches2:
        self.caller.msg(match.db_text)
```

有關查詢資料庫的更多資訊，請參閱[Django 查詢入門教學](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Django-queries.md)。
