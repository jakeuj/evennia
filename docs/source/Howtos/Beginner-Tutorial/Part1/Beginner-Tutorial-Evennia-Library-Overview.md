(overview-of-the-evennia-library)=
# Evennia 庫概述

```{sidebar} API

API 代表`Application Programming Interface`，描述如何存取程式或庫的資源。
```
有幾種探索 Evennia 庫的好方法。
- 本文件包含從來源自動產生的 [Evennia-API 檔案](../../../Evennia-API.md)。嘗試點選一些條目 - 一旦您足夠深入，您將看到每個元件的完整描述及其檔案。您也可以點選 `[source]` 檢視每個事物的完整 Python 原始碼。
- 如果您需要更詳細的解釋，[每個元件都有單獨的檔案頁](../../../Components/Components-Overview.md)。
- 您可以瀏覽[github上的evennia儲存庫](https://github.com/evennia/evennia)。這正是您可以從我們這裡下載的內容。
- 最後，您可以將 evennia 儲存庫克隆到您自己的電腦並閱讀原始程式碼。如果您想*真正*瞭解正在發生的事情，或幫助 Evennia 的開發，這是必要的。如果您想執行此操作，請參閱[擴充安裝說明](../../../Setup/Installation-Git.md)。

(where-is-it)=
## 它在哪裡？

如果安裝了Evennia，您可以簡單地從它匯入

    import evennia
    from evennia import some_module
    from evennia.some_module.other_module import SomeClass

等等。

如果您使用 `pip install` 安裝了 Evennia，則庫資料夾將安裝在 Python 安裝的深處；你最好[在 github 上檢視](github:evennia)。如果您克隆了它，您應該有一個 `evennia` 資料夾可供檢視。

您會發現這是最外層的結構：

    evennia/
        bin/
        CHANGELOG.md
        ...
        ...
        docs/
        evennia/

此外層用於Evennia的安裝和軟體包分發。該內部資料夾 `evennia/evennia/` 是 _actual_ 程式庫，API 自動檔案涵蓋的內容以及執行 `import evennia` 時獲得的內容。

> `evennia/docs/` 資料夾包含本文件的原始碼。看
> 如果您想了解有關其工作原理的更多資訊，請[為檔案做出貢獻](../../../Contributing-Docs.md)。

這是Evennia庫的結構：

 - evennia
   - [`__init__.py`](../../../Evennia-API.md#shortcuts) - Evennia 的「平坦 API」位於此處。
   - [`settings_default.py`](../../../Setup/Settings.md#settings-file) - Evennia 的根設定。將設定從此處複製到 `mygame/server/settings.py` 檔案。
   - [`commands/`](../../../Components/Commands.md) - 指令解析器和處理程式。
     - `default/` - [預設指令](../../../Components/Default-Commands.md) 和 cmdsets。
   - [`comms/`](../../../Components/Channels.md) - 用於遊戲內通訊的系統。
   - `contrib/` - 可選外掛程式對於核心 Evennia 來說太特定於遊戲。
   - `game_template/` - 使用`evennia --init`時複製成為「遊戲目錄」。
   - [`help/`](../../../Components/Help-System.md) - 處理說明條目的儲存和建立。
   - `locale/` - 語言檔案 ([i18n](../../../Concepts/Internationalization.md))。
   - [`locks/`](../../../Components/Locks.md) - Lock 用於限制對遊戲內實體的存取的系統。
   - [`objects/`](../../../Components/Objects.md) - 遊戲內實體（所有型別的物品和角色）。
   - [`prototypes/`](../../../Components/Prototypes.md) - 物件原型/生成系統和 OLC 選單
   - [`accounts/`](../../../Components/Accounts.md) - 遊戲外 Session 控制的實體（帳戶、機器人等）
   - [`scripts/`](../../../Components/Scripts.md) - 遊戲外實體等同於物件，也具有計時器支援。
   - [`server/`](../../../Components/Portal-And-Server.md) - 核心伺服器程式碼和 Session 處理。
     - `portal/` - Portal 代理程式和連線協定。
   - [`typeclasses/`](../../../Components/Typeclasses.md) - typeclass 儲存和資料庫系統的抽象類別。
   - [`utils/`](../../../Components/Coding-Utils.md) - 各種有用的編碼資源。
   - [`web/`](../../../Concepts/Web-Features.md) - Web 資源和 webserver。初始化時部分複製到遊戲目錄。

```{sidebar} __init__.py

`__init__.py` 檔案是一個特殊的 Python 檔名，用來表示 Python「套件」。當您單獨匯入 `evennia` 時，您將匯入此檔案。當您執行 `evennia.foo` 時，Python 將首先在 `__init__.py` 中尋找屬性 `.foo`，然後在同一位置尋找具有該名稱的模組或資料夾。

```

雖然所有實際的 Evennia 程式碼都可以在各個資料夾中找到，但 `__init__.py` 代表整個套件 `evennia`。它包含實際位於其他地方的程式碼的“快捷方式”。如果您在 Evennia-API 頁面上[向下滾動一點](../../../Evennia-API.md)，則會列出大多數快捷方式。

(an-example-of-exploring-the-library)=
## 探索圖書館的例子

在[上一課](./Beginner-Tutorial-Python-classes-and-objects.md#on-classes-and-objects)中，我們簡要介紹了 `mygame/typeclasses/objects` 作為 Python 模組的範例。讓我們再次開啟它。

```python
"""
module docstring
"""
from evennia import DefaultObject

class Object(DefaultObject):
    """
    class docstring
    """
    pass
```

我們有 `Object` 類，它繼承自 `DefaultObject`。模組頂部附近是這一行：

    from evennia import DefaultObject

我們想弄清楚這個 DefaultObject 到底能提供什麼。由於這是直接從 `evennia` 匯入的，因此我們實際上是從 `evennia/__init__.py` 匯入的。

[檢視 `evennia/__init__.py` 的第 160 行](github:evennia/__init__.py#L160)，你會發現這一行：

    from .objects.objects import DefaultObject

```{sidebar} 相對進口和絕對進口

`from.objects.objects...` 中的第一個句號表示我們正在從目前位置匯入。這稱為`relative import`。相比之下，`from evennia.objects.objects` 是 `absolute import`。在這種特殊情況下，兩者會給出相同的結果。
```

> 您也可以檢視[API 首頁的右側部分](../../../Evennia-API.md#typeclasses)，然後按一下檢視程式碼。

由於 `DefaultObject` 在這裡被匯入到 `__init__.py` 中，因此即使該類別的程式碼實際上並不在這裡，也可以將其匯入為 `from evennia import DefaultObject` 。

因此，要查詢 `DefaultObject` 的程式碼，我們需要檢視 `evennia/objects/objects.py`。以下是在檔案中尋找它的方法：

1. 開啟[API首頁](../../../Evennia-API.md)
2. 找到 [evennia.objects.objects](../../../api/evennia.objects.objects.md) 的連結並點選它。
3. 您現在位於 python 模組中。向下捲動（或在網頁瀏覽器中搜尋）找到 `DefaultObject` 類。
4. 現在您可以閱讀它的作用以及它的方法。如果您想檢視完整的原始程式碼，請點選旁邊的\[原始程式碼\]連結。

(conclusions)=
## 結論

這是一個重要的教訓。它教您如何為自己找到資訊。瞭解如何遵循類別繼承樹並導航到您需要的內容是學習像 Evennia 這樣的新程式庫的一個重要部分。

接下來，我們將開始利用迄今為止所學到的知識，並將其與 Evennia 提供的構建塊結合。