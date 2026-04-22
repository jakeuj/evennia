(a-voice-operated-elevator-using-events)=
# 使用事件的語音操作電梯

本教學將引導您使用 [in-
遊戲Python系統](./Contrib-Ingame-Python.md)。本教學假設遊戲中使用 Python
系統是按照該檔案中的說明安裝的。 **您無需閱讀**全文
文件，這是一個很好的參考，但不是瞭解它的最簡單的方法。  因此這些
教學。

遊戲中的 Python 系統允許在某些情況下在單一物件上執行程式碼。  你不
安裝過去後必須修改原始程式碼才能新增這些功能。  整個系統
可以輕鬆地在某些物件（但不是全部）中新增特定功能。

> 我們將嘗試做什麼？

在本教學中，我們將建立一個簡單的語音操作電梯。  從功能上來說，我們
將會：

- 使用引數探索事件。
- 致力於更有趣的回撥。
- 瞭解連鎖事件。
- 在回撥中使用變數修改。

(our-study-case)=
## 我們的研究案例

讓我們先總結一下我們想要實現的目標。  我們想建立一個房間來代表
我們的電梯內部。  在這個房間裡，角色可以只說“1”、“2”或“3”，然後
電梯將開始移動。  門將在新樓層關閉和開啟（出口通往
進出電梯將進行修改）。

我們將首先處理基本功能，然後會調整一些功能，向您展示如何簡單且強大
可以透過遊戲內的Python系統設定獨立的動作。

(creating-the-rooms-and-exits-we-need)=
## 建立我們需要的房間和出口

我們將在我們的房間中建立一部電梯（通常稱為“Limbo”，ID 2）。  你可以輕鬆地
如果您已經有一些房間和出口，請調整以下說明，當然，請記住
檢查 ID。

> 注意：遊戲中的 Python 系統在很多事情上都會使用 ID。  雖然這不是強制性的，但它是
瞭解回呼的 ID 是一個好習慣，因為這會使操作變得更加頻繁
更快。  還有其他方法來識別物件，但由於它們取決於許多因素，ID 是
通常是我們回呼中最安全的路徑。

讓我們進入困境 (`#2`) 增加電梯。  我們將把它新增到北部。  為了建立這個房間，
在遊戲中你可以輸入：

    tunnel n = Inside of an elevator

遊戲應該透過告訴您做出回應：

    Created room Inside of an elevator(#3) of type typeclasses.rooms.Room.
    Created Exit from Limbo to Inside of an elevator: north(#4) (n).
    Created Exit back from Inside of an elevator to Limbo: south(#5) (s).

請注意給定的 ID：

- `#2`是limbo，系統建立的第一個房間。
- `#3`是我們在電梯內的房間。
- `#4`是從Limbo到我們電梯的北出口。
- `#5`是通往地獄邊境的電梯的南出口。

將這些 ID 儲存在某處以供演示。  您很快就會明白為什麼它們很重要。

> 為什麼我們要建立通往電梯並返回地獄邊境的出口？  電梯不是應該移動嗎？

這是。  但我們需要有一個代表電梯進出通道的出口。  我們什麼
在每一層樓，我們要做的就是改變這些出口，以便它們連線到正確的房間。
稍後您會看到這個過程。

我們還有兩個房間要建立：2 樓和 3 樓。這次，我們將使用 `dig`，因為我們不
需要通往那裡的出口，無論如何還沒有。

    dig The second floor
    dig The third floor

Evennia 應回答：

    Created room The second floor(#6) of type typeclasses.rooms.Room.
    Created room The third floor(#7) of type typeclasses.rooms.Room.

將這些 ID 新增到您的清單中，我們也會使用它們。

(our-first-callback-in-the-elevator)=
## 我們在電梯裡的第一次回撥

我們去電梯吧（如果你的 ID 與我相同，你可以使用 `tel #3`）。

這是我們的電梯間。  它看起來有點空，隨意新增更漂亮的描述或其他
稍微裝飾一下它。

但我們現在想要的是能夠說「1」、「2」或「3」並讓電梯在其中移動
方向。

如果你讀過
[關於在事件中新增對話的其他遊戲內 Python 教學](./Contrib-Ingame-Python-Tutorial-Dialogue.md)，您
可能會記得我們需要做什麼。  如果沒有，這裡有一個總結：當有人時我們需要執行一些程式碼
在房間裡說話。  所以我們需要建立一個回撥（回撥將包含我們的程式碼行）。
我們只需要知道應該在哪個事件上設定它。  您可以輸入`call here`來檢視
這個房間裡可能發生的事件。

在表中，您應該看到“say”事件，當有人在表中說了某事時就會呼叫該事件
房間。  因此，我們需要為此事件新增回撥。  如果您有點迷路，請不要擔心，只需跟隨
接下來的步驟，它們連線在一起的方式將會變得更加明顯。

    call/add here = say 1, 2, 3

1. 我們需要新增一個回撥。  回撥包含將在給定時間執行的程式碼。
所以我們使用`call/add`指令和開關。
2. `here` 是我們的物件，我們所在的房間。
3. 等號。
4. 回撥應連線到的事件的名稱。  在這裡，事件是「說」。
這意味著每次有人在房間裡說話時都會執行此回撥。
5. 但是我們新增了一個事件引數來指示房間中所說的話應該執行我們的關鍵字
打回來。  否則，無論發生什麼，每次有人說話時我們的回撥都會被呼叫。  這裡
我們限制，表示只有當語音訊息包含「1」、「2」或
「3」。

應開啟一個編輯器，邀請您輸入應執行的 Python 程式碼。  第一個
要記住的是閱讀提供的文字（它可能包含重要資訊），並且大多數
all，此回呼中可用的變數清單：

```
Variables you can use in this event:

    character: the character having spoken in this room.
    room: the room connected to this event.
    message: the text having been spoken by the character.

----------Line Editor [Callback say of Inside of an elevator]---------------------
01|
----------[l:01 w:000 c:0000]------------(:h for help)----------------------------
```

這很重要，以便了解我們可以在開箱即用的回撥中使用哪些變數。  讓我們
編寫一行以確保我們的回撥在我們期望的時候被呼叫：

```python
character.msg(f"You just said {message}.")
```

您可以在遊戲中貼上此行，然後輸入 `:wq` 指令退出編輯器並儲存您的
修改。

讓我們檢查一下。  試著在房間裡說「你好」。  您應該看到標準訊息，但什麼也沒有
更多。  現在嘗試說“1”。  在標準訊息下方，您應該會看到：

    You just said 1.

你可以嘗試一下。  只有當我們說「1」、「2」或「3」時才會呼叫我們的回撥。  這正是我們要做的
想要。

讓我們返回程式碼編輯器並新增一些更有用的內容。

    call/edit here = say

> 請注意，我們這次使用了“編輯”開關，因為回撥存在，所以我們只想編輯
它。

編輯器再次開啟。  我們先清空它：

    :DD

並關閉自動縮排，這將幫助我們：

    :=

> 自動縮排是程式碼編輯器的一個有趣功能，但我們最好不要在此時使用它
一點，它會使複製/貼上變得更加複雜。

(our-entire-callback-in-the-elevator)=
## 我們在電梯裡的整個回撥

現在是時候在遊戲中真正編寫我們的回撥程式碼了。  這裡有個小提醒：

1. 我們有三個房間和兩個出口的所有 ID。
2. 當我們說「1」、「2」或「3」時，電梯應該會移動到正確的房間，也就是改變
退出。  請記住，我們已經有了出口，我們只需更改它們的位置和目的地即可。

嘗試自己編寫此回撥是個好主意，但不要因為檢查
立即解決。  您可以將以下程式碼貼到程式碼編輯器中：

```python
# First let's have some constants
ELEVATOR = get(id=3)
FLOORS = {
    "1": get(id=2),
    "2": get(id=6),
    "3": get(id=7),
}
TO_EXIT = get(id=4)
BACK_EXIT = get(id=5)

# Now we check that the elevator isn't already at this floor
floor = FLOORS.get(message)
if floor is None:
    character.msg("Which floor do you want?")
elif TO_EXIT.location is floor:
    character.msg("The elevator already is at this floor.")
else:
    # 'floor' contains the new room where the elevator should be
    room.msg_contents("The doors of the elevator close with a clank.")
    TO_EXIT.location = floor
    BACK_EXIT.destination = floor
    room.msg_contents("The doors of the elevator open to {floor}.",
            mapping=dict(floor=floor))
```

讓我們回顧一下這個較長的回撥：

1. 我們首先獲得兩個出口和三層樓的物體。  我們使用`get()` eventfunc，
這是獲取物件的捷徑。  我們通常用它來檢索特定物件
ID。  我們把地板放進字典裡。  字典的鍵是樓層號碼（如 str），
值是房間物件。
2. 請記住，`message` 變數包含房間中所說的訊息。  所以「1」、「2」或
「3」。  然而，我們仍然需要檢查它，因為如果角色在
room，我們的回呼將會被執行。  讓我們確定她說的是樓層號。
3. 然後我們檢查電梯是否已經到達該樓層。  請注意，我們使用`TO_EXIT.location`。
`TO_EXIT` 包含我們的「北」出口，通往電梯內部。  因此，它的`location`將
是電梯目前所在的房間。
4. 如果樓層不同，則讓電梯“移動”，僅更改位置並
兩個出口的目的地。
   - `BACK_EXIT`（即“北”）應該更改其位置。  電梯不應該
透過我們的舊樓層即可到達。
   - `TO_EXIT`（即“南”，電梯出口）應該有不同的
目的地。  當我們走出電梯時，我們應該發現自己身處新樓層，而不是舊樓層
一。

請隨意擴充套件此範例，更改訊息，進行進一步檢查。  用法與實踐
是鑰匙。

您可以像往常一樣使用 `:wq` 退出編輯器並進行測試。

(adding-a-pause-in-our-callback)=
## 在回撥中加入暫停

讓我們改進我們的回撥。  值得補充的一件事是暫停：暫時，
當我們在電梯裡說出樓層號碼時，門會立即關閉並開啟。  這將是
最好停頓幾秒鐘。  更有邏輯性。

這是瞭解連鎖事件的絕佳機會。  鍊式事件對於建立非常有用
停頓。  與我們迄今為止看到的事件相反，鍊式事件不會自動呼叫。
他們必須由您呼叫，並且可以在一段時間後呼叫。

- 連結事件的名稱始終為 `"chain_X"`。  通常，X 是一個數字，但您可以給出
連鎖事件有一個更明確的名稱。
- 在我們最初的回撥中，我們將在 15 秒內呼叫我們的鍊式事件。
- 我們還必須確保電梯尚未移動。

除此之外，鍊式事件可以像往常一樣連線到回呼。  我們將建立一個鍊式
我們電梯中的事件，僅包含開啟新樓層門所需的程式碼。

    call/add here = chain_1

回呼被加入到`"chain_1"`事件中，該事件不會被自動呼叫
當有事情發生時系統。  在此活動中，您可以貼上程式碼以開啟以下位置的門
新樓層。  您會注意到一些差異：

```python
TO_EXIT.location = floor
TO_EXIT.destination = ELEVATOR
BACK_EXIT.location = ELEVATOR
BACK_EXIT.destination = floor
room.msg_contents("The doors of the elevator open to {floor}.",
        mapping=dict(floor=floor))
```

將此程式碼貼到編輯器中，然後使用 `:wq` 儲存並退出編輯器。

現在讓我們在“say”事件中編輯回撥。  我們必須稍微改變一下：

- 回撥必須檢查電梯是否已經移動。
- 電梯移動時必須改變出口。
- 它必須呼叫我們定義的`"chain_1"`事件。  它應該在 15 秒後呼叫它。

讓我們看看回撥中的程式碼。

    call/edit here = say

刪除目前程式碼並再次停用自動縮排：

    :DD
    :=

您可以貼上以下程式碼。  請注意與我們第一次嘗試的差異：

```python
# First let's have some constants
ELEVATOR = get(id=3)
FLOORS = {
    "1": get(id=2),
    "2": get(id=6),
    "3": get(id=7),
}
TO_EXIT = get(id=4)
BACK_EXIT = get(id=5)

# Now we check that the elevator isn't already at this floor
floor = FLOORS.get(message)
if floor is None:
    character.msg("Which floor do you want?")
elif BACK_EXIT.location is None:
    character.msg("The elevator is between floors.")
elif TO_EXIT.location is floor:
    character.msg("The elevator already is at this floor.")
else:
    # 'floor' contains the new room where the elevator should be
    room.msg_contents("The doors of the elevator close with a clank.")
    TO_EXIT.location = None
    BACK_EXIT.location = None
    call_event(room, "chain_1", 15)
```

發生了什麼變化？

1. 我們新增了一些測試以確保電梯尚未移動。  如果是的話，則
`BACK_EXIT.location`（通往電梯的「南」出口）應為`None`。  我們將刪除
電梯運轉時的出口。
2. 當門關閉時，我們將兩個出口的 `location` 設定為 `None`。  這將他們從他們的
房間，但不會破壞它們。  出口仍然存在，但它們沒有連線任何東西。  如果你說
「2」在電梯裡，電梯執行時環顧四周，你不會看到任何出口。
3. 我們沒有立即開門，而是呼叫`call_event`。  我們給它所包含的物件
要呼叫的事件（這裡是我們的電梯），要呼叫的事件的名稱（這裡是“chain_1”）
以及從現在開始應呼叫該事件的秒數（此處為 `15`）。
4. 我們建立的 `chain_1` 回呼包含「重新開啟」電梯門的程式碼。  那
也就是說，除了顯示訊息之外，它還會重置出口'`location` 和`destination`。

如果您嘗試在電梯中說“3”，您應該會看到門關閉。  看看你和你的周圍
不會看到任何出口。  然後，15 秒後，門應開啟，您可以離開電梯
去三樓。  當電梯執行時，通往電梯的出口將會
無法訪問。

> 注意：我們不會在鍊式事件中再次定義變數，我們只是呼叫它們。  當我們
執行`call_event`，我們目前變數的副本被放置在資料庫中。  這些變數
當呼叫鍊式事件時將被恢復並再次存取。

可以使用`call/tasks`指令檢視等待執行的任務。  例如，說“2”
在房間中，注意門關閉，然後鍵入 `call/tasks` 指令。  你會看到一個任務
在電梯裡，等待呼叫`chain_1`事件。

(changing-exit-messages)=
## 更改退出訊息

這是事件的另一個不錯的小功能：您可以修改單一退出的訊息，而無需
改變其他人。  在這種情況下，當有人向北進入我們的電梯時，我們希望看到
例如：「有人走進電梯。」後面出口類似的東西是
也很棒。

在電梯內，您可以在向外（南）的出口處檢視可用的活動。

    call south

您應該在此表中看到兩行有趣的行：

```
| msg_arrive       |   0 (0) | Customize the message when a character        |
|                  |         | arrives through this exit.                    |
| msg_leave        |   0 (0) | Customize the message when a character leaves |
|                  |         | through this exit.                            |
```

因此，我們可以透過編輯「msg_leave」事件來更改角色離開時其他人看到的訊息。
讓我們這樣做：

    call/add south = msg_leave

花時間閱讀幫助。  它為您提供了您需要的所有資訊。  我們需要
更改“message”變數，並使用自訂對映（在大括號之間）來更改訊息。  我們是
給了一個例子，讓我們使用它。  在程式碼編輯器中，您可以貼上以下行：

```python
message = "{character} walks out of the elevator."
```

再次輸入 `:wq` 儲存並退出編輯器。  你可以建立一個新角色來看著它離開。

    charcreate A beggar
    tel #8 = here

（顯然，如有必要，請調整 ID。）

    py self.search("beggar").move_to(self.search("south"))

這是迫使我們的乞丐離開電梯的一種粗暴方法，但它允許我們進行測試。  你應該
參見：

    A beggar(#8) walks out of the elevator.

偉大的！  讓我們對電梯內部的出口做同樣的事情。  跟著乞丐，
然後編輯“north”的“msg_leave”：

    call/add north = msg_leave

```python
message = "{character} walks into the elevator."
```

同樣，你可以強迫我們的乞丐移動並看到我們剛剛設定的訊息。  本次修改
顯然，適用於這兩個出口：自訂訊息不會用於其他出口。  自從我們
每個樓層使用相同的出口，無論電梯在哪一層都可以使用，
這非常整潔！

(tutorial-faq)=
## 教學常見問題解答

- **問：**如果在任務等待發生時遊戲重新載入或關閉，會發生什麼情況？
- **答：** 如果您的遊戲在任務暫停時重新載入（例如我們樓層之間的電梯），當
遊戲再次可訪問，任務將被呼叫（如有必要，需要採取新的時間差）
考慮到重新載入）。  如果伺服器關閉，顯然任務不會被呼叫，但是
將被儲存並在伺服器再次啟動時執行。
- **問：** 我可以在回呼中使用各種變數嗎？  到底是鏈還是不鏈？
- **答：** 您可以在原始回呼中使用您喜歡的每種變數型別。  但是，如果您
執行`call_event`，由於您的變數儲存在資料庫中，因此它們需要遵守
對持久屬性的約束。  例如，回撥不會以這種方式儲存。
該變數在您的鍊式事件中不可用。
- **問：**當你說我可以將我的連鎖事件稱為「chain_1」、「chain_2」以外的其他名稱時
那麼，命名約定是什麼？
- **答：** 連鎖事件的名稱以 `"chain_"` 開頭。  這對您和對
系統。  但在底線之後，你可以給出一個更有用的名稱，例如我們的`"chain_open_doors"`
案例。
- **問：** 我是否需要暫停幾秒鐘才能呼叫鍊式事件？
- **A：** 不，您可以立即呼叫它。  只需保留第三個引數 `call_event` 即可（它
預設為 0，意味著鍊式事件將立即被呼叫）。  這不會建立一個
任務。
- **問：** 我可以讓連鎖事件自行呼叫嗎？
- **答：** 你可以。  沒有限制。  請小心，一個呼叫自身的回撥，
特別是沒有延遲，可能是無限迴圈的好方法。然而，在某些情況下，它
對於讓連鎖事件呼叫自身、每 X 秒執行相同的重複操作非常有用
例如。
- **問：**如果我需要多部電梯怎麼辦，我需要每次都複製/貼上這些回撥嗎？
- **答：** 不建議。  肯定有更好的方法來處理這種情況。  其中之一是
考慮在原始碼本身中加入程式碼。  另一種可能性是呼叫鍊式事件
具有預期的行為，這使得移植程式碼變得非常容易。連鎖事件的這一面將是
將在下一個教學中顯示。
