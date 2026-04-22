(batch-command-processor)=
# 批次指令處理器


有關使用批處理器的介紹和動機，請參閱[此處](./Batch-Processors.md)。這個
頁面描述了 Batch-*command* 處理器。 Batch-*code* 已在[此處](Batch-Code-
Processor) 介紹。

批次指令處理器是一個僅限超級使用者的函式，由

     > batchcommand path.to.batchcmdfile

其中 `path.to.batchcmdfile` 是以「`.ev`」檔案結尾的*批次指令檔*的路徑。
該路徑類似於相對於您定義的用於儲存批次檔的資料夾的 python 路徑，設定
在您的設定中包含`BATCH_IMPORT_PATH`。預設資料夾是（假設您的遊戲位於`mygame`
資料夾）`mygame/world`。因此，如果您想執行範例批次檔案
`mygame/world/batch_cmds.ev`，你可以使用

     > batchcommand batch_cmds

批次指令檔案包含由註解分隔的 Evennia 遊戲內指令清單。的
處理器將從頭到尾執行批次檔。請注意，*如果指令在
它失敗*（處理器沒有通用的方法來知道所有的失敗是什麼樣子的）
不同的指令）。因此，請密切注意輸出，或使用*互動模式*（見下文）來
以更受控、漸進的方式執行該檔案。

(the-batch-file)=
## 批次檔

批次檔是一個簡單的純文字檔案，包含 Evennia 指令。就像你會寫的那樣
它們在遊戲中，除了你有更多的換行自由。

以下是 `*.ev` 檔案的語法規則。你會發現它真的非常非常簡單：

- 所有具有`#`（雜湊）符號*作為該行第一行*的行都被視為*註解*。所有非註解行都被視為指令和/或其引數。
- 註解行有一個實際的功能－它們標記*前一個指令定義的結束*。因此，切勿將兩個指令直接放在檔案中 - 用註釋將它們分開，否則兩個指令中的第二個將被視為第一個指令的引數。此外，無論如何，使用大量註釋是一種很好的做法。
- 以 `#INSERT` 開頭的行是註解行，但也表示特殊指令。語法為 `#INSERT <path.batchfile>` 並嘗試將給定的批次指令檔案匯入此檔案。插入的批次檔（以`.ev`結尾的檔案）將從`#INSERT`指令處正常運作。
- 指令定義中的額外空格將被*忽略*。  - 完全空白行會轉換為文字中的換行符號。因此，兩個空白行意味著一個新段落（這顯然僅與接受此類格式的指令相關，例如 `@desc` 指令）。
- 檔案中的最後一個指令不需要以註解結尾。
- 您*不能*將另一個 `batchcommand` 語句巢狀到批次檔中。如果要將多個批次檔連結在一起，請改用 `#INSERT` 批次指令。您也無法從批次檔啟動 `batchcode` 指令，這兩個批次處理器不相容。

以下是在 `evennia/contrib/tutorials/batchprocessor/example_batch_cmds.ev` 中找到的範例檔案的版本。

```bash
    #
    # This is an example batch build file for Evennia. 
    #
    
    # This creates a red button
    create button:red_button.RedButton
    # (This comment ends input for create)
    # Next command. Let's create something. 
    set button/desc = 
      This is a large red button. Now and then 
      it flashes in an evil, yet strangely tantalizing way. 
    
      A big sign sits next to it. It says:

    
    -----------
    
     Press me! 
    
    -----------

    
      ... It really begs to be pressed! You 
    know you want to! 
    
    # This inserts the commands from another batch-cmd file named
    # batch_insert_file.ev.
    #INSERT examples.batch_insert_file
    
      
    # (This ends the set command). Note that single line breaks 
    # and extra whitespace in the argument are ignored. Empty lines 
    # translate into line breaks in the output.
    # Now let's place the button where it belongs (let's say limbo #2 is 
    # the evil lair in our example)
    teleport #2
    # (This comments ends the teleport command.) 
    # Now we drop it so others can see it. 
    # The very last command in the file needs not be ended with #.
    drop button
```

若要對此進行測試，請在檔案上執行 `batchcommand`：

    > batchcommand tutorials.batchprocessor.example_batch_cmds

將在 Limbo 中建​​立、描述並放置一個按鈕。所有指令都將由呼叫該指令的使用者執行。

> 請注意，如果您與按鈕互動，您可能會發現其描述發生變化，從而丟失上面的自訂設定描述。這就是這個特定物件的工作方式。

(interactive-mode)=
## 互動模式

互動模式可讓您更逐步地控制批次檔的執行方式。這對於偵錯很有用，如果您有一個很大的批次檔並且只更新其中的一小部分，那麼再次執行整個檔案將是浪費時間（例如，在 `create`-ing 物件的情況下，您最終會得到同名物件的多個副本）。使用 `batchcommand` 和 `/interactive` 標誌進入互動模式。

     > batchcommand/interactive tutorials.batchprocessor.example_batch_cmds

你會看到這個：

    01/04: create button:red_button.RedButton  (hh for help) 

這表示您正在執行 `create` 指令，這是該批次檔中僅有的四個指令中的第一個。請注意，指令 `create` 此時「尚未」被實際處理！

若要檢視您將要執行的完整指令，請使用 `ll` （批次版本
`look`）。使用 `pp` 實際處理當前指令（這實際上將 `create` 按鈕）——並確保它按計劃工作。使用`nn`（下一個）轉到下一個指令。  使用 `hh` 作為指令清單。

如果有錯誤，請在批次檔中修復它們，然後使用 `rr` 重新載入檔案。您仍將使用相同的指令，並且可以根據需要使用 `pp` 輕鬆重新執行它。這使得除錯週期變得簡單。它還允許您重新執行單一麻煩的指令 - 如前所述，在大型批次檔中這可能非常有用。請注意，在許多情況下，指令依賴前面的指令（e.g。如果上例中的 `create` 失敗，則後面的指令將沒有任何操作）。

使用 `nn` 和 `bb`（下一個和後一個）逐步瀏覽檔案； e.g。 `nn 12` 將向前跳 12 步（中間不處理任何指令）。在互動模式下工作時，Evennia 的所有正常指令也應該起作用。

(limitations-and-caveats)=
## 限制和注意事項

批次指令建置的主要問題是，當您執行批次指令 script 時，您（*您*，就像您的角色一樣）實際上是在遊戲中按順序移動建立和建立房間，就像您手動一一輸入這些指令一樣。

建立檔案時必須考慮到這一點，以便您可以按順序「行走」（或傳送）到正確的位置。這也意味著你可能會受到你所創造的事物的影響，例如攻擊你的小怪或立即傷害你的陷阱。

如果您知道您的房間和物件將透過批次指令 script 部署，您可以提前對此進行規劃。為了幫助解決此問題，您可以利用以下事實：非持久 Attribute `batch_batchmode` 僅在批次處理器執行時設定。以下是如何使用它的範例：

```python
class HorribleTrapRoom(Room):
    # ... 
    def at_object_receive(self, received_obj, source_location, **kwargs):
        """Apply the horrible traps the moment the room is entered!"""
        if received_obj.ndb.batch_batchmode: 
            # skip if we are currently building the room
            return 
        # commence horrible trap code
```
因此，如果我們目前正在建造房間，我們就跳過這個鉤子。這可以用於任何事情，包括確保小怪在您建立它們時不會開始攻擊您。

還有其他策略，例如向活動物件新增開/關開關，並確保在建立時將其始終設定為“關閉”。

(editor-highlighting-for-ev-files)=
## .ev 檔案的編輯器反白顯示

- [GNU Emacs](https://www.gnu.org/software/emacs/) 使用者可能會發現使用 emacs 的 *evennia 模式*很有趣。這是在 `evennia/utils/evennia-mode.el` 中找到的 Emacs 主模式。在 Emacs 中編輯 `.ev` 檔案時，它提供正確的語法突出顯示和 `<tab>` 縮排。有關安裝說明，請參閱該檔案的標頭。
- [VIM](https://www.vim.org/) 使用者可以使用 amfl 的 [vim-evennia](https://github.com/amfl/vim-evennia) 模式代替，請參閱其自述檔案以取得安裝說明。