(the-web-admin)=
# 網路管理員

Evennia _Web admin_ 是自訂的 [Django 管理網站](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)
用於使用圖形介面操作遊戲資料庫。你
必須登入該網站才能使用它。然後它顯示為 `Admin` 連結
您網站的頂部。您也可以轉到 [http://localhost:4001/admin](http://localhost:4001/admin)
本地執行。

幾乎所有在管理員中完成的操作也可以透過使用管理員在遊戲中完成-
或生成器指令。

(usage)=
## 用法

管理非常不言自明 - 您可以看到每種物件型別的列表，
建立每種型別的新例項並新增屬性/tags 它們。的
管理首頁將給出所有相關實體及其狀態的摘要
使用過。

不過，有一些用例需要一些額外的解釋。

(adding-objects-to-attributes)=
### 將物件新增至屬性

Attribute 的 `value` 欄位被醃製為特殊形式。這通常不是
您需要擔心的事情（管理員將醃製/取消醃製）值
對您來說），_除非_如果您想將資料庫物件儲存在 attribute 中。這樣的
物件實際上儲存為具有物件唯一資料的`tuple`。

1. 找到您要新增到Attribute的物件。在第一部分的底部
您會找到_序列化字串_欄位。該字串顯示一個 Python 元組，例如

       ('__packed_dbobj__', ('objects', 'objectdb'), '2021:05:15-08:59:30:624660', 358)

完全按照原樣標記此元組字串並將其複製到剪貼簿（括號等）。
2. 轉到應具有新 Attribute 的實體並建立 Attribute。在其`value`
在欄位中，貼上您先前複製的元組字串。節省！
3. 如果你想將多個物件儲存在一個清單中，你可以透過字面意思來做到這一點
在貼上序列化的位置輸入 python 清單 `[tuple, tuple, tuple,...]`
   帶逗號的元組字串。在某些時候，在程式碼中執行此操作可能更容易...

(linking-accounts-and-characters)=
### 連結帳戶和角色

在`MULTISESSION_MODE`0或1中，每個連線可以有一個Account和一個
角色，通常有相同的名字。通常這是由使用者完成的
建立一個新帳戶並登入 - 然後將出現一個匹配的角色
為他們創造的。不過，您也可以在管理員中手動執行此操作：

1. 首先在管理員中建立完整的帳戶。
2. 接下來，建立物件（通常為 `Character` typeclass）並將其命名為相同的名稱
作為帳戶。它還需要一個指令集。預設的 CharacterCmdset 是一個不錯的選擇。
3. 在 `Puppeting Account` 欄位中，選擇帳戶。
4. 確保儲存所有內容。
5. 點選 `Link to Account` 按鈕（只有先儲存後才有效）。這將
將所需的鎖和屬性新增到帳戶中，以允許他們立即
   當角色下次登入時連線到角色。這將（如果可能）：
   - 將 `account.db._last_puppet` 設定為角色。
   - 將角色新增至 `account.db._playabel_characters` 清單。
   - 新增/擴充套件角色上的 `puppet:` lock 以包括 `puppet:pid(<Character.id>)`

(building-with-the-admin)=
### 與管理員一起建構

構建和描述是可能的（如果可能在規模上不太實用）
管理室中的房間。

1. 使用合適的房間名稱建立 `Object` 的 Room-typeclass。
2. 在房間上設定 Attribute 'desc' - 該 Attribute 的值是
房間的描述。
3. 新增`type`「別名」的`Tags`以新增房間別名（常規tags沒有型別）

退出：

1. 退出是 `Exit` typeclass 的 `Objects`，因此建立一個。
2. 出口擁有您剛剛建立的房間的`Location`。
3. 將 `Destination` 設定為出口通往的位置。
4. 設定“desc”Attribute，如果有人檢視出口，則會顯示此內容。
5. `type`「別名」中的 `Tags` 是使用者可用來瀏覽的備用名稱
這個出口。

(grant-others-access-to-the-admin)=
## 授予其他人存取管理員的許可權

對管理員的訪問由 `Staff status` 標誌控制
帳戶。  如果沒有設定此標誌，即使是超級使用者也看不到管理員
網頁上的連結。員工狀態在遊戲中沒有同等地位。


只有超級使用者可以更改 `Superuser status` 標誌，並授予新的
帳戶的許可權。超級使用者是唯一的許可權級別
也與遊戲相關。 `User Permissions` 和 `Groups` 在 `Account` 上找到
管理頁面_僅_影響管理員 - 他們與遊戲內沒有聯絡
[許可權](./Permissions.md)（玩家、建造者、管理員等）。

對於一個 `Staff status` 的員工來說，能夠真正做任何事情，
超級使用者必須至少為其帳戶授予一些許可權。這個
也可以很好地限制錯誤。不允許是個好主意
例如，`Can delete Account` 許可權。

```{important}

如果您向帳戶授予員工身分和許可權，但他們仍然無法
  存取管理員的內容，嘗試重新載入伺服器。

```

```{warning}

    If a staff member has access to the in-game ``py`` command, they can just as
    well have their admin ``Superuser status`` set too. The reason is that ``py``
    grants them all the power they need to set the ``is_superuser`` flag on their
    account manually. There is a reason access to the ``py`` command must be
    considered carefully ...

```

(customizing-the-web-admin)=
## 自訂網路管理

自訂管理是一個大主題，超出了本文的範圍
文件。請參閱[Django 官方檔案](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)
細節。這只是一個簡短的總結。

請參閱[網站](./Website.md)頁面，以瞭解相關元件的概述
產生網頁。 Django 管理員使用相同的原則，除了
Django 提供了很多工具來為我們自動化管理生成。

管理範本位於 `evennia/web/templates/admin/` 但您會發現
這是比較空的。這是因為大多數模板只是
直接從 Django 包中的原始位置繼承
(`django/contrib/admin/templates/`)。所以如果你想覆蓋一個你可以
將其從_there_複製到您的`mygame/templates/admin/`資料夾中。同樣的道理
對於 CSS 檔案。

管理站點的後端程式碼（檢視）位於 `evennia/web/admin/` 中。它
被組織成 `admin` 類，如 `ObjectAdmin`、`AccountAdmin` 等。
這些自動使用底層資料庫模型來產生有用的檢視
對我們來說，如果沒有我們，我們就不必自己寫表格等。

頂層`AdminSite`（django檔案中引用的管理設定）
位於 `evennia/web/utils/adminsite.py` 中。


(change-the-title-of-the-admin)=
### 更改管理員的頭銜

預設情況下，管理員的頭銜是`Evennia web admin`。若要變更此設定，請新增
以下為您的`mygame/web/urls.py`：

```python
# in mygame/web/urls.py

# ...

from django.conf.admin import site

#...

site.site_header = "My great game admin"


```

重新載入伺服器，管理員的標題標題將會變更。
