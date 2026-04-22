(batch-code-processor)=
# 批次程式碼處理器


有關使用批處理器的介紹和動機，請參閱[此處](./Batch-Processors.md)。本頁描述了 Batch-*code* 處理器。 Batch-*command* 已在[此處](Batch-Command- Processor) 介紹。

批次程式碼處理器是一個僅限超級使用者的函式，由

     > batchcode path.to.batchcodefile

其中 `path.to.batchcodefile` 是*批次程式碼檔案*的路徑。此類檔案的名稱應以“`.py`”結尾（但不應將其包含在路徑中）。該路徑類似於相對於您定義的用於儲存批次檔的資料夾的 python 路徑，由設定中的 `BATCH_IMPORT_PATH` 設定。預設資料夾是（假設您的遊戲名為“mygame”）`mygame/world/`。因此，如果您想在 `mygame/world/batch_code.py` 中執行範例批次檔案，您可以簡單地使用

     > batchcode batch_code

這將嘗試一次性執行整個批次檔。對於更漸進的「互動式」控制，您可以使用 `/interactive` 開關。  開關 `/debug` 會將處理器置於*偵錯*模式。請閱讀下文以瞭解更多資訊。

(the-batch-file)=
## 批次檔

批次程式碼檔案是普通的 Python 檔案。不同之處在於，由於批處理器載入並執行檔案而不是匯入檔案，因此您可以可靠地更新檔案，然後再次呼叫它，一遍又一遍並檢視您的更改，而無需 `reload` 伺服器。這使得測試變得容易。在批次程式碼檔案中，您還可以存取以下全域變數：

- `caller` - 這是對執行批處理器的物件的參考。
- `DEBUG` - 這是一個布林值，可讓您確定此檔案目前是否正在偵錯模式下執行。請參閱下文，瞭解這有何用處。

透過處理器執行一個普通的 Python 檔案只會從頭到尾執行該檔案。如果您想更好地控制執行，可以使用處理器的“互動”模式。這會自行執行某些程式碼區塊，僅重新執行該部分，直到您對此感到滿意為止。為此，您需要在檔案中新增特殊標記，以將其分成更小的區塊。它們採用註釋的形式，因此該檔案在 Python 中仍然有效。

- `#CODE` 作為一行中的第一個標記*程式碼*區塊的開始。它將持續到另一個標記的開頭或檔案的末尾。程式碼區塊包含功能性Python程式碼。每個 `#CODE` 區塊將與檔案的其他部分完全隔離地執行，因此請確保它是獨立的。
- `#HEADER` 作為一行中的第一個標記 *header* 區塊的開始。它持續到下一個標記或檔案末尾。這是為了儲存所有其他區塊所需的匯入和變數。標頭區塊中定義的所有 python 程式碼將始終插入檔案中每個 `#CODE` 區塊的頂部。您可能有多個 `#HEADER` 區塊，但這相當於擁有一個大塊。請注意，您無法在程式碼區塊之間交換資料，因此在一個程式碼區塊中編輯標頭變數不會影響任何其他程式碼區塊中的該變數！
- `#INSERT path.to.file` 將在該位置插入另一個批次程式碼 (Python) 檔案。 - 未啟動 `#HEADER`、`#CODE` 或 `#INSERT` 指令的 `#` 被視為註解。
- 在區塊內，應用普通的 Python 語法規則。為了縮排，每個區塊充當一個單獨的 python 模組。

以下是在 `evennia/contrib/tutorial_examples/` 中找到的範例檔案的版本。

```python
    #
    # This is an example batch-code build file for Evennia. 
    #
    
    #HEADER
    
    # This will be included in all other #CODE blocks
    
    from evennia import create_object, search_object
    from evennia.contrib.tutorial_examples import red_button
    from typeclasses.objects import Object
    
    limbo = search_object('Limbo')[0]
    
    
    #CODE 
 
    red_button = create_object(red_button.RedButton, key="Red button", 
                               location=limbo, aliases=["button"])
    
    # caller points to the one running the script
    caller.msg("A red button was created.")
    
    # importing more code from another batch-code file
    #INSERT batch_code_insert
    
    #CODE
    
    table = create_object(Object, key="Blue Table", location=limbo)
    chair = create_object(Object, key="Blue Chair", location=limbo)
    
    string = f"A {table} and {chair} were created."
    if DEBUG:
        table.delete()
        chair.delete()
        string += " Since debug was active, they were deleted again." 
    caller.msg(string)
```

這使用Evennia的PythonAPI按順序建立三個物件。

(debug-mode)=
## 偵錯模式

嘗試執行範例 script

     > batchcode/debug tutorial_examples.example_batch_code

批次 script 將執行到最後並告訴您它已完成。您還將收到有關按鈕和兩件傢俱已建立的訊息。  環顧四周，您應該會看到那裡有按鈕。但你不會看到任何椅子或桌子！這是因為我們使用 `/debug` 開關執行此指令，該開關在 script 內直接可見為 `DEBUG==True`。在上面的例子中，我們透過再次刪除椅子和桌子來處理這種狀態。

除錯模式旨在測試批次指令碼時使用。也許您正在尋找程式碼中的錯誤或嘗試檢視事情是否按其應有的方式執行。一遍又一遍地執行 script 將建立不斷增長的一堆椅子和桌子，它們都具有相同的名稱。您稍後必須返回並煞費苦心地刪除它們。

(interactive-mode)=
## 互動模式

互動模式的工作方式與[批次指令處理器對應部分](Batch-Command- Processor) 非常相似。它允許您更逐步地控制批次檔的執行方式。這對於除錯或僅選擇特定的區塊來執行非常有用。  使用 `batchcode` 和 `/interactive` 標誌進入互動模式。

     > batchcode/interactive tutorial_examples.batch_code

您應該看到以下內容：

    01/02: red_button = create_object(red_button.RedButton, [...]         (hh for help) 

這表示您位於第一個 `#CODE` 區塊，這是該批次中僅有的兩個指令中的第一個。請注意，此時該區塊實際上「尚未」執行！

若要檢視您將要執行的完整程式碼片段，請使用 `ll`（`look` 的批次版本）。

```python
    from evennia.utils import create, search
    from evennia.contrib.tutorial_examples import red_button
    from typeclasses.objects import Object
    
    limbo = search.objects(caller, 'Limbo', global_search=True)[0]

    red_button = create.create_object(red_button.RedButton, key="Red button", 
                                      location=limbo, aliases=["button"])
    
    # caller points to the one running the script
    caller.msg("A red button was created.")
```

與前面給出的範例程式碼進行比較。請注意 `#HEADER` 的內容是如何貼到 `#CODE` 區塊的頂部的。使用 `pp` 實際執行此區塊（這將建立按鈕
並給您留言）。使用`nn`（下一個）轉到下一個指令。使用 `hh` 作為指令清單。

如果存在回溯，請在批次檔中修復它們，然後使用 `rr` 重新載入檔案。您仍將處於相同的程式碼區塊，並且可以根據需要使用 `pp` 輕鬆重新執行它。這使得除錯週期變得簡單。它還允許您重新執行單一麻煩的區塊 - 如前所述，在大型批次檔中這可能非常有用（也不要忘記 `/debug` 模式）。

使用 `nn` 和 `bb`（下一個和後一個）逐步瀏覽檔案； e.g。 `nn 12` 將向前跳 12 步（不處理中間的任何區塊）。在互動模式下工作時，Evennia 的所有正常指令也應該起作用。

(limitations-and-caveats)=
## 限制和注意事項

批次程式碼處理器是迄今為止建立 Evennia 世界的最靈活的方式。然而，您需要記住一些注意事項。

(safety)=
### 安全
或者更確切地說，缺乏它。只允許*超級使用者*執行批次程式碼是有原因的
預設處理器。程式碼處理器運作**沒有任何 Evennia 安全檢查**並允許
完全訪問Python。如果不受信任的一方可以執行他們可以執行的程式碼處理器
你的機器上有任意的Python程式碼，這可能是一件非常危險的事。  如果你想
允許其他使用者存取批次程式碼處理器，您應該確保將 Evennia 作為
您電腦上的單獨且存取許可權非常有限的使用者（i.e。在「監獄」中）。相比之下，該批次
指令處理器更安全，因為執行它的使用者仍然在遊戲“內部”並且無法
確實可以做遊戲指令允許之外的任何事情。

(no-communication-between-code-blocks)=
### 程式碼塊之間沒有通訊
全域變數在程式碼批次檔中不起作用，每個區塊都作為獨立環境執行。 `#HEADER` 區塊實際上貼在每個 `#CODE` 區塊的頂部，因此更新區塊中的某些標頭變數不會使該變更在另一個區塊中可用。鑑於 python 執行限制，允許這樣做也會導致在使用互動模式時非常難以除錯程式碼 - 這將是「義大利麵程式碼」的典型範例。

主要的實際問題是建構 e.g 時。一個程式碼區塊中的一個房間，稍後想要將該房間與您在目前程式碼區塊中建立的房間連線起來。有兩種方法可以做到這一點：

- 對您建立的房間的名稱執行資料庫搜尋（因為您無法事先知道它被指派了哪個 dbref）。問題是名稱可能不唯一（您可能有很多“黑暗森林”房間）。有一個簡單的方法可以處理這個問題 - 使用 [Tags](./Tags.md) 或 *別名*。您可以為任何物件分配任意數量的 tags 和/或別名。確保這些 tags 或別名之一對於房間來說是唯一的（例如“room56”），以後您將能夠始終唯一地搜尋並找到它。
- 使用`caller`全域屬性作為區塊間儲存。例如，您可以在 `ndb` 中有一個房間引用字典：
    ```python
    #HEADER 
    if caller.ndb.all_rooms is None:
        caller.ndb.all_rooms = {}

    #CODE 
    # create and store the castle
    castle = create_object("rooms.Room", key="Castle")
    caller.ndb.all_rooms["castle"] = castle

    #CODE 
    # in another node we want to access the castle
    castle = caller.ndb.all_rooms.get("castle")
    ```
請注意，在建立字典之前，如果 `caller.ndb.all_rooms` 尚不存在，我們如何檢查 `#HEADER`。請記住，`#HEADER` 被複製到每個 `#CODE` 區塊的前面。沒有那個 `if` 語句
我們會擦除每個區塊的字典！

(dont-treat-a-batchcode-file-like-any-python-file)=
### 不要像任何 Python 檔案一樣對待批次程式碼檔案

儘管批次程式碼檔案是有效的 Python 檔案，但它應該「僅」由批次程式碼處理器執行。您不應該在其中定義 Typeclasses 或指令，或將它們匯入到其他程式碼中。在 Python 中匯入模組將執行該模組的基礎級別，對於普通批次程式碼檔案來說，這可能意味著每次都會建立大量新物件。

(dont-let-code-rely-on-the-batch-files-real-file-path)=
### 不要讓程式碼依賴批次檔的真實檔案路徑

當您將內容匯入批次程式碼檔案時，請不要使用相對匯入，而是始終使用從遊戲目錄或 evennia 庫的根目錄開始的路徑匯入。依賴批次檔「實際」位置的程式碼*將會失敗*。批次程式碼檔案作為文字讀取並執行字串。當程式碼執行時，它不知道這些字串曾經屬於哪個檔案。