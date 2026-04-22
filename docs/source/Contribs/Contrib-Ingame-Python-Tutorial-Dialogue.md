(dialogues-in-events)=
# 事件中的對話

本教學將引導您完成建立多個對話的步驟
角色，使用 Ingame-Python 系統。  本教學假設遊戲中
Python系統已安裝在您的遊戲中。  如果不是，您可以按照
安裝步驟在[主要的遊戲內Python
docs](./Contrib-Ingame-Python.md) 並在完成後返回本教學
系統已安裝。  **您不需要閱讀**整個文件，它是
一個很好的參考，但不是瞭解它的最簡單的方法。  因此這些
教學。

遊戲中的 Python 系統允許在某些情況下在單一物件上執行程式碼
情況。  您不必修改原始程式碼來新增這些功能，
透過安裝。  整個系統可以輕鬆新增特定功能
對於某些物件，但不是全部。  這就是為什麼建立一個非常有用的
利用遊戲內Python系統的對話系統。

> 我們將嘗試做什麼？

在本教學中，我們將建立一個基本對話以自動包含多個角色
回應他人所說的具體訊息。

(a-first-example-with-a-first-character)=
## 具有第一個字元的第一個範例

讓我們先建立一個角色。

    @charcreate a merchant

這將在您目前所在的房間中建立一個商人。  它沒有任何東西，就像
描述，如果你喜歡的話可以稍微裝飾。

如上所述，遊戲中的 Python 系統包括將物件與任意程式碼連結。  這段程式碼
在某些情況下會被執行。  這裡的情況是「當某人在
同一個房間”，並且可能更具體，例如“當有人打招呼時”。  我們將決定什麼程式碼
執行（我們實際上會在遊戲中輸入程式碼）。  使用遊戲中Python系統的詞彙，
我們將建立一個回撥：回呼只是一組將在某些環境下執行的程式碼行
條件。

您可以使用 `@call` 概覽可以建立回呼的每個“條件”
指令（`@callback` 的縮寫）。  您需要給它一個物件作為引數。  例如，我們這裡
可以做：

    @call a merchant

您應該會看到一個包含三列的表格，顯示了我們新建立的事件列表
商人。  雖然還沒有設定任何程式碼行，但它們確實有很多。  對於
在我們的系統中，您可能對描述 `say` 事件的行更感興趣：

    | 說              |   0 (0) | 在另一個角色說了一些話之後 |
    |                  |         | 角色的房間。                         |

我們將在 `say` 事件上建立一個回撥，當我們在商人房間裡說“你好”時呼叫：

    @call/add a merchant = say hello

在檢視此指令顯示的內容之前，讓我們先看看指令語法本身：

- `@call` 是指令名，`/add` 是開關。  您可以閱讀該指令的幫助來獲取
可用開關的幫助和語法的簡要概述。
- 然後我們輸入物件的名稱，此處為「商人」。  您也可以輸入ID（在我的例子中為「#3」），
當您不在同一個房間時，這對於編輯對像很有用。  您甚至可以輸入部分內容
名字，像往常一樣。
- 一個等號，一個簡單的分隔符號。
- 活動的名稱。  這裡是「說」。  當您使用`@call`時顯示可用事件
沒有開關。
- 在一個空格之後，我們輸入呼叫此回撥的條件。  在這裡，
條件代表另一個角色該說的話。  我們輸入“你好”。  意思是如果
有人在房間裡說了一些包含“hello”的話，我們現在建立的回撥將是
叫。

當您輸入此指令時，您應該看到如下內容：

```
After another character has said something in the character's room.
This event is called right after another character has said
something in the same location.  The action cannot be prevented
at this moment.  Instead, this event is ideal to create keywords
that would trigger a character (like a NPC) in doing something
if a specific phrase is spoken in the same location.

To use this event, you have to specify a list of keywords as
parameters that should be present, as separate words, in the
spoken phrase.  For instance, you can set a callback that would
fire if the phrase spoken by the character contains "menu" or
"dinner" or "lunch":
    @call/add ... = say menu, dinner, lunch
Then if one of the words is present in what the character says,
this callback will fire.

Variables you can use in this event:
    speaker: the character speaking in this room.
    character: the character connected to this event.
    message: the text having been spoken by the character.
```

這是一些資訊列表。  現在對我們來說最重要的是：

- 每當其他人在房間裡說話時，就會呼叫「say」事件。
- 我們可以將回撥設定為在短語中出現特定關鍵字時觸發，方法是將它們設為
附加引數。  這裡我們將此引數設定為「hello」。  我們可以有幾個關鍵字
用逗號分隔（稍後我們將更詳細地看到這一點）。
- 我們可以在此回呼中使用三個預設變數：`speaker`，其中包含
說話的角色，`character`，其中包含由遊戲中Python修改的角色
系統（此處為商家），以及包含口語短語的`message`。

變數的概念很重要。  如果它讓事情對你來說變得更簡單，請將它們視為
函式中的引數：它們可以在函式體內使用，因為它們已經被設定
當函式被呼叫時。

這個指令開啟了一個編輯器，我們可以在其中鍵入 Python 程式碼。

```
----------Line Editor [Callback say of a merchant]--------------------------------
01|
----------[l:01 w:000 c:0000]------------(:h for help)----------------------------
```

對於我們的第一個測試，讓我們輸入以下內容：

```python
character.location.msg_contents("{character} shrugs and says: 'well, yes, hello to you!'",
mapping=dict(character=character))
```

輸入此行後，您可以鍵入 `:wq` 儲存編輯器並退出。

現在，如果您使用包含“hello”的訊息的“say”指令：

```
You say, "Hello sir merchant!"
a merchant(#3) shrugs and says: 'well, yes, hello to you!'
```

如果你說的內容不包含“hello”，我們的回撥將不會執行。

**總之**：

1. 當我們在房間裡說話時，使用“say”指令，所有角色的“say”事件
（除了我們）被稱為。
2. 遊戲中的 Python 系統會檢視我們所說的內容，並檢查我們的回撥之一是否在
「say」事件包含我們說過的關鍵字。
3. 如果是這樣，請呼叫它，定義我們已經看到的事件變數。
4. 然後回撥將作為正常的 Python 程式碼執行。  這裡我們稱之為`msg_contents`
方法在角色的位置（可能是一個房間）上向整個房間顯示訊息。  我們
也使用對映來輕鬆顯示角色的名字。  這並非特定於遊戲內
Python系統。  如果您對我們使用的程式碼感到不知所措，只需縮短它並使用一些東西
更簡單，例如：

```python
speaker.msg("You have said something to me.")
```

(the-same-callback-for-several-keywords)=
## 多個關鍵字的相同回撥

很容易建立一個回撥，如果句子包含以下幾個之一，則會觸發該回撥
關鍵字。

    @call/add merchant = say trade, trader, goods

在開啟的編輯器中：

```python
character.location.msg_contents("{character} says: 'Ho well, trade's fine as long as roads are
safe.'", mapping=dict(character=character))
```

然後你可以在句子中使用“trade”、“trader”或“goods”來表達某些內容，這應該
呼叫回撥：

```
You say, "and how is your trade going?"
a merchant(#3) says: 'Ho well, trade's fine as long as roads are safe.'
```

我們可以在新增回撥的時候設定幾個關鍵字。  我們只需要用逗號分隔它們。

(a-longer-callback)=
## 更長的回撥

到目前為止，我們只在回撥中設定了一行。  這很有用，但我們經常需要更多。  對於
整個對話，您可能想做的不只如此。

    @call/add merchant = say bandit, bandits

在編輯器中，您可以貼上以下行：

```python
character.location.msg_contents("{character} says: 'Bandits he?'",
mapping=dict(character=character))
character.location.msg_contents("{character} scratches his head, considering.",
mapping=dict(character=character))
character.location.msg_contents("{character} whispers: 'Aye, saw some of them, north from here.  No
trouble o' mine, but...'", mapping=dict(character=character))
speaker.msg("{character} looks at you more
closely.".format(character=character.get_display_name(speaker)))
speaker.msg("{character} continues in a low voice: 'Ain't my place to say, but if you need to find
'em, they're encamped some distance away from the road, I guess near a cave or
something.'.".format(character=character.get_display_name(speaker)))
```

現在試著向商家詢問強盜的情況：

```
You say, "have you seen bandits?"
a merchant(#3) says: 'Bandits he?'
a merchant(#3) scratches his head, considering.
a merchant(#3) whispers: 'Aye, saw some of them, north from here.  No trouble o' mine, but...'
a merchant(#3) looks at you more closely.
a merchant(#3) continues in a low voice: 'Ain't my place to say, but if you need to find 'em,
they're encamped some distance away from the road, I guess near a cave or something.'.
```

請注意，第一行對話是對著整個房間說的，但隨後商人就
直接與說話者交談，只有說話者聽得到。  對你來說沒有真正的限制
可以用這個來做。

- 你可以設定一個心情繫統，將屬性儲存在NPC本身告訴你他現在是什麼心情，
這將影響他所提供的資訊……也許還會影響其準確性。
- 您可以新增在某些上下文中所說的隨機短語。
- 您可以使用其他操作（您不限於讓商家說些什麼，您可以詢問
他移動，給你一些東西，攻擊（如果你有戰鬥系統），或其他什麼）。
- 回撥是純 Python 語言，因此您可以編寫條件或迴圈。
- 您可以使用連結事件在某些指令之間新增「暫停」。  本教學不會
但是請描述如何做到這一點。  你已經有很多東西可以玩了。

(tutorial-faq)=
## 教學常見問題解答

- **問：** 我可以創造幾個會回答特定對話的角色嗎？
- **答：**當然。  遊戲中的Python系統非常強大，因為你可以為遊戲設定唯一的程式碼
各種物體。  您可以讓多個角色回答不同的事情。  你甚至可以擁有
房間裡的不同角色回答問候。  所有回撥將在之後執行
另一個。
- **問：** 我可以讓兩個角色以完全相同的方式回答同一對話嗎？
- **答：** 有可能，但做起來並不容易。  通常，事件分組是在程式碼中設定的，並且取決於
在不同的遊戲上。  但是，如果是一些不常見的情況，那麼使用它很容易做到
[連鎖事件](./Contrib-Ingame-Python.md))。
- **問：** 是否可以在所有共享相同原型的角色上部署回呼？
- **答：** 不是開箱即用的。  這取決於程式碼中的個人設定。  可以想像，所有
某些型別的角色會共享一些事件，但這是特定於遊戲的。  同一區域的房間也可以共享相同的事件。  這是可以做到的，但需要修改原始碼。

- 下一個教學：[新增帶有事件的語音操作電梯](A-voice-operated-elevator-using- events)。
