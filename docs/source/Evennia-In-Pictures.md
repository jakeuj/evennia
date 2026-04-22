# Evennia 圖解

```{sidebar}
這_不是_一份鉅細靡遺的總覽。你可以把它當成一組值得優先認識的重點快照。
```

這篇文章試著從高層次介紹 Evennia 伺服器，以及它由哪些主要部分組成。希望能幫助你更快理解整體架構是如何串在一起的。

<div style="clear: right;"></div>

## Evennia 的兩大組件
![Evennia 的 Portal 與 Server][image1]

這張圖裡顯示的是你從 Evennia 下載下來的主體部分。它本身_還不能_單獨啟動一個完整遊戲。接下來我們很快就會補上那塊缺少的「拼圖」，不過在那之前，先看看目前手上有哪些東西。

首先你會發現，Evennia 主要由兩個部分組成，也就是 [Portal 與 Server](Components/Portal-And-Server.md)。它們是彼此分開的程序。

Portal 負責追蹤所有對外連線，也理解 Telnet protocol、websocket、SSH 等連線方式。它完全不碰資料庫，也不知道遊戲狀態。Portal 和 Server 之間傳遞的資料與連線協定無關，意思是無論玩家透過哪種方式連進來，Server 收發的都是同一種資料。因為有 Portal 作為外層保護，所以就算 Server 完整重開，玩家也不會因此斷線。

Server 則是主要的「mud driver」，負責處理與遊戲世界及其資料庫有關的一切。它是非同步的，底層使用 [Twisted](http://twistedmatrix.com/trac/)。

在 Server 的同一個程序裡，也包含了 Evennia 的 [Web Server](Components/Webserver.md)。它負責提供遊戲網站。
<div style="clear: right;"></div>

### 初始化遊戲目錄

![建立遊戲目錄][image2]

當你[安裝好 Evennia](Setup/Installation.md) 之後，就會有 `evennia` 這個指令可以使用。你會用它建立一個遊戲目錄（這裡假設叫做 `mygame`）。圖中較深灰色的那一塊就是它，也是剛剛還缺著的部分。你的夢想遊戲，就是在這裡誕生。

在初始化過程中，Evennia 會在 `mygame/` 裡建立 Python module 範本，並串好所有必要設定，讓 `mygame` 變成一個已經完整可運作、雖然還是空白、但可以立刻開始擴充的遊戲。

初始化的一部分也包含建立資料庫，然後啟動伺服器。從這一刻起，你的新遊戲就已經運轉起來了。你可以用 telnet 連到 localhost:4000，或直接在瀏覽器打開 http://localhost:4001 來連進遊戲。

現在，這個新的 `mygame` 世界還需要 Characters、地點、物品，以及更多內容。

## 資料庫

![image3][image3]

Evennia 是完全持久化的系統，並透過 [Django](https://www.djangoproject.com/) 在 Python 中抽象化它的資料庫。資料表數量不多，而且設計得很通用；每一張表都由一個 Python class 代表。就像圖中所示，範例裡的 `ObjectDB` Python class 對應一張資料表。class 上的屬性就是那張表的欄位（fields），而每一列資料都是這個 class 的一個 instance，也就是遊戲中的一個實體。

圖中示範的欄位裡，包含了這個 `ObjectDB` 實體的 key（名稱），以及它目前「location」的 [Foreign key](https://en.wikipedia.org/wiki/Foreign_key) 關聯。

從圖上可以看出，_Trigger_ 正待在 _Dungeon_ 裡，身上還帶著他信賴的十字弓 _Old Betsy_！

`db_typeclass_path` 是個很重要的欄位。它是一個 Python 風格的路徑，用來告訴 Evennia：實際上是哪個 `ObjectDB` subclass 正在代表這個實體。這正是 Evennia [Typeclass system](Components/Typeclasses.md) 的核心，讓你能用一般 Python 方式操作資料庫中的遊戲實體。

### 從資料庫到 Python

![image4][image4]

在這張圖裡，你可以看到一棵稍微簡化過的 Python class inheritance tree，也就是身為 Evennia 開發者時會接觸到的結構，旁邊還搭配了三個實際存在的實體。

[Objects](Components/Objects.md) 代表的是你在遊戲裡實際會看到的東西，而它的子類別則實作了 Evennia 會用到的各種 handler、helper code 與 hook method。在你的 `mygame/` 目錄裡，你只要匯入它們，再 override 你想修改的部分即可。於是 `Crossbow` 就能被改造成只會十字弓才有的行為，而 `CastleRoom` 也能加入城堡房間特有的功能。

當你在遊戲裡建立一個新實體時，資料庫表中就會自動新增一列，接著 `Trigger` 就會在遊戲中出現！如果我們在程式裡查詢資料庫中的 Trigger，得到的會是一個 [Character](Components/Objects.md#characters) class 的 instance，也就是一個可以正常操作的 Python 物件。

看到這裡，你可能會以為自己得為遊戲中的每一種物件都建立一個 class。實際結構當然由你決定，但 Evennia 也提供了其他方法，讓你可以針對單一物件做客製化。繼續看下去。

### Attributes

![image5][image5]

除了前面那些之外，[Attribute](Components/Attributes.md) 也是另一個在幕後直接連到資料庫的 class。每個 `Attribute` 基本上都有一個 key、一個 value，以及一個指向其他 `ObjectDB` 的 ForeignKey 關聯。

`Attribute` 會把 Python 結構序列化後存進資料庫，意思是你幾乎可以存任何合法的 Python 內容，例如圖中那份技能 dictionary。此後，「strength」與「skills」這些 Attributes 就能直接從 _Trigger_ 物件上取得。這個機制（以及其他幾種資源）讓你可以打造高度個別化的實體，同時只為那些行為本質上真的不同的東西建立 class。

<div style="clear: right;"></div>

## 控制遊戲行為

![image6][image6]

_Trigger_ 多半是由一位真人玩家控制。這位玩家會透過一個或多個 [Sessions](Components/Sessions.md) 連上遊戲，每開一個 client，就會對應一個 Session。

他在 `mygame` 裡的帳號，會由一個 [Account](Components/Accounts.md) 實體表示。`AccountDB` 會保存密碼與其他帳號資訊，但它本身不直接存在於遊戲世界中。透過 `Account` 實體，`Sessions` 就能控制（也就是「puppet」）一個或多個遊戲內的 `Object` 實體。

在這張圖裡，某位使用者同時用三個 `Session` 連進遊戲。他登入的是名為 _Richard_ 的玩家 `Account`。透過這些 `Session`，他同時在操作遊戲內的 _Trigger_ 與 _Sir Hiss_ 兩個實體。Evennia 可以設定是否允許這類不同形式的 [Connection Styles](Concepts/Connection-Styles.md)。

### Commands

![image7][image7]

要讓玩家真的能控制自己的遊戲角色並開始玩，他們就必須能送出 [Commands](Components/Commands.md)。

`Command` 可以代表玩家主動輸入到遊戲裡的任何內容，例如 `look`、`get`、`quit`、`emote` 等等。

每個 `Command` 都同時負責參數 parsing 與實際執行。由於每個 Command 都是一般 Python class，所以你可以只實作一次 parsing 邏輯，再讓其他指令去繼承成果。上圖中的 `DIKUCommand` 父類別就實作了所有 DIKU-style 指令共用的語法解析，於是 `CmdLook` 等其他指令就不必重寫。

### Command Sets

![image8][image8]

所有 Evennia Commands 都一定會被收納進 `CommandSet` 裡。`CommandSet` 是能容納多個 `Command` instance 的容器。某個特定的 `Command` class 可以把 instance 提供給任意多個 `CommandSet`，而這些 set 會永遠綁定在遊戲實體上。

在這張圖裡，_Trigger_ 取得了一個包含許多實用指令的 `CommandSet`，所以他本人（以及背後控制他的 `Account`/Player）現在都可以使用這些指令。

![image9][image9]

_Trigger_ 的 `CommandSet` 只對他自己可用。在這張圖裡，我們又把一個含有三個指令的 `CommandSet` 放到了 Dungeon 房間上。房間本身其實不需要用指令，但我們可以把這組 set 設定成影響_房間裡面的人_。請注意，這裡的指令是這些命令的_另一個版本_（所以顏色不同）！下面會解釋原因。

<div style="clear: right;"></div>

### 合併 Command Sets

![image10][image10]

多個 `CommandSet` 可以像 [Set Theory](https://en.wikipedia.org/wiki/Set_theory) 那樣被動態地、暫時地合併，只是 Evennia 允許你自訂合併優先權。在這張圖裡，我們看到的是一種 _Union_ 型的合併：來自 Dungeon、名稱相同的 Commands 會暫時覆蓋 Trigger 原本的指令。當 Trigger 待在 Dungeon 裡時，他使用的就是這一版指令；等他離開後，自己的 `CommandSet` 就會完整恢復。

為什麼要這樣做？例如，假設地城一片漆黑，那我們就可以讓 Dungeon 版本的 `look` 指令只在 Trigger 身上有光源時，才顯示房間內容。沒有光時，你甚至可能沒辦法順利撿起地上的東西，還可能在背包裡亂翻一通！

任意數量的 Command Sets 都可以在執行時即時合併。這讓你能實作多種彼此重疊的狀態（例如在昏暗房間裡戰鬥，而且角色還喝醉了），卻不必為每一種可能組合都寫出巨大的 if 判斷。這種合併是非破壞性的，所以你只要移除 cmdset，就能在需要時回到先前的狀態。

## 現在就去探索吧！

這當然遠遠不是 Evennia 功能的完整清單，但它應該已經提供你一批值得繼續往下深挖的有趣概念。

你可以在本手冊的 [Core Components](Components/Components-Overview.md) 與 [Core Concepts](Concepts/Concepts-Overview.md) 章節中找到更多細節。如果你還沒讀過，也很建議先看看 [Evennia 簡介](./Evennia-Introduction.md)。

[image1]: https://2.bp.blogspot.com/-0-oir21e76k/W3kaUuGrg3I/AAAAAAAAJLU/qlQWmXlAiGUz_eKG_oYYVRf0yP6KVDdmQCEwYBhgL/s1600/Evennia_illustrated_fig1.png
[image2]: https://4.bp.blogspot.com/-TuLk-PIVyK8/W3kaUi-e-MI/AAAAAAAAJLc/DA9oMA6m5ooObZlf0Ao6ywW1jHqsPQZAQCEwYBhgL/s1600/Evennia_illustrated_fig2.png
[image3]: https://3.bp.blogspot.com/-81zsySVi_EE/W3kaVRn4IWI/AAAAAAAAJLc/yA-j1Nwy4H8F28BF403EDdCquYZ9sN4ZgCEwYBhgL/s1600/Evennia_illustrated_fig3.png
[image4]: https://2.bp.blogspot.com/--4_MqVdHj8Q/W3kaVpdAZKI/AAAAAAAAJLk/jvTsuBBUlkEbBCaV9vyIU0IWiuF6PLsSwCEwYBhgL/s1600/Evennia_illustrated_fig4.png
[image5]: https://3.bp.blogspot.com/-6ulv5T_gUCI/W3kaViWBBfI/AAAAAAAAJLU/0NqeAsz3YVsQKwpODzsmjzR-7tICw1pTQCEwYBhgL/s1600/Evennia_illustrated_fig5.png
[image6]: https://4.bp.blogspot.com/-u-npXjlq6VI/W3kaVwAoiUI/AAAAAAAAJLY/T9bhrzhJJuQwTR8nKHH9GUxQ74hyldKOgCEwYBhgL/s1600/Evennia_illustrated_fig6.png
[image7]: https://3.bp.blogspot.com/-_RM9-Pb2uKg/W3kaWIs4ndI/AAAAAAAAJLc/n45Hcvk1PiYhNdBbAAr_JjkebRVReffTgCEwYBhgL/s1600/Evennia_illustrated_fig7.png
[image8]: https://2.bp.blogspot.com/-pgpYPsd4CLM/W3kaWG2ffuI/AAAAAAAAJLg/LKl4m4-1xkYxVA7JXXuVP28Q9ZqhNZXTACEwYBhgL/s1600/Evennia_illustrated_fig8.png
[image9]: https://3.bp.blogspot.com/-acmVo7kUZCk/W3kaWZWlT0I/AAAAAAAAJLk/nnFrNaq_TNoO08MDleadwhHfVQLdO74eACEwYBhgL/s1600/Evennia_illustrated_fig9.png
[image10]: https://4.bp.blogspot.com/--lixKOYjEe4/W3kaUl9SFXI/AAAAAAAAJLQ/tCGd-dFhZ8gfLH1HAsQbZdaIS_OQuvU3wCEwYBhgL/s1600/Evennia_illustrated_fig10.png
