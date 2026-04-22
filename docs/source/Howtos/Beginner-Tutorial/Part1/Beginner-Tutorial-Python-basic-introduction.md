(intro-to-using-python-with-evennia)=
# 使用 Python 和 Evennia 的簡介

是時候嘗試一些編碼了！ Evennia是用[Python](https://python.org)編寫和擴充套件的。 Python 是一種成熟且專業的程式語言，使用起來非常快。

也就是說，儘管 Python 被廣泛認為易於學習，但我們在這些課程中只能涵蓋基礎知識。雖然我們希望讓您開始瞭解您需要的最重要的部分，但您可能需要自己學習一些知識來補充。幸運的是，有大量免費的 Python 線上學習資源。請參閱我們的[連結部分](../../../Links.md) 以瞭解一些範例。

> 雖然如果您是一位經驗豐富的開發人員，這將是非常基本的，但您可能至少希望繼續閱讀前幾節，我們將介紹如何從 Evennia 內部執行 Python。

首先，如果你想抑制自己去玩教學世界，請確保你的
超級使用者恢復權力：

       unquell

(evennia-hello-world)=
## Evennia 世界你好

`py` 指令（或 `!`，這是一個別名）允許您作為超級使用者在遊戲中執行原始 Python。這對於快速測試很有用。在遊戲的輸入行中，輸入以下內容：

    > py print("Hello World!")


```{sidebar} 指令輸入

帶`>`的行表示進入遊戲的輸入，下面的行是
該輸入的預期回報。
```

你會看到

    > print("Hello world!")
    Hello World!

`print(...)` *函式* 是 Python 中輸出文字的基本內建方法。我們將“Hello World”作為單一_引數_傳送到此函式。如果我們要傳送多個引數，它們將用逗號分隔。

引號 `"..."` 表示您正在輸入*字串*（i.e.文字）。您也可以使用單引號 `'...'` - Python 兩者都接受。

> 輸入Python字串的第三種方法是使用三引號（`"""..."""`或`'''...'''`。這用於跨多行的較長字串。當我們像這樣直接將程式碼插入到`py`時，我們只能使用一行。

(making-some-text-graphics)=
## 製作一些文字“圖形”

毫不奇怪，在製作文字遊戲時，您會大量使用文字。即使您有偶爾的按鈕甚至圖形元素，正常的過程也是使用者以文字形式輸入指令並獲取文字。正如我們在上面看到的，一段文字在 Python 中被稱為_string_，並用單引號或雙引號括起來。

字串可以相加：

    > py print("This is a " + "breaking change.")
    This is a breaking change.

字串乘以數字將重複該字串多次：

    > py print("|" + "-" * 40 + "|")
    |----------------------------------------|

或者

    > py print("A" + "a" * 5 + "rgh!")
    Aaaaaargh!

(format)=
### 。格式（）

```{sidebar} 函式和方法
- 函式：當您使用零個或多個 `arguments` 呼叫它時執行操作的東西。函式在 python 模組中是獨立的，例如 `print()`
- 方法：位於物件「之上」的函式。它是透過 `.` 運運算元存取的，例如 `obj.msg()`，或在本例中為 `<string>.format()`。
```

雖然組合不同的字串很有用，但更強大的是就地修改字串內容的能力。在 Python 中，有多種方法可以實現此目的，我們將在這裡展示其中的兩種方法。第一種是使用字串的 `.format`_method_：

    > py print("This is a {} idea!".format("good"))
    This is a good idea!


方法可以被認為是另一個物件「上」的資源。此方法知道它位於哪個物件上，因此可以以各種方式影響它。您可以使用句點 `.` 存取它。在本例中，該字串有一個資源 `format(...)` 對其進行修改。更具體地說，它用傳遞給格式的值替換了字串內的 `{}` 標記。你可以做很多次：

    > py print("This is a {} idea!".format("good"))
    This is a good idea!

或者

    > py print("This is the {} and {} {} idea!".format("first", "second", "great"))
    This is the first and second great idea!

> 請注意末尾的雙括號 - 第一個關閉 `format(...` 方法，最外面的雙括號關閉 `print(...`。不關閉它們會給你帶來可怕的`SyntaxError`。我們將在下一節中更多地討論錯誤，現在只需修復，直到它按預期列印為止。

這裡我們將三個逗號分隔的字串作為_arguments_傳遞給字串的`format`方法。它們按照給出的順序替換了 `{}` 標記。

輸入也不必是字串：

    > py print("STR: {}, DEX: {}, INT: {}".format(12, 14, 8))
    STR: 12, DEX: 14, INT: 8

若要分隔同一行上的兩個 Python 指令，請使用分號 `;`。試試這個：

    > py a = "awesome sauce" ; print("This is {}!".format(a))
    This is awesome sauce!

```{warning} MUD 使用者端和分號

有些 MUD 用戶端使用分號 `;` 來分割用戶端輸入
分成單獨的傳送。如果是這樣的話，上面就會報錯。大多數用戶端允許您在「逐字」模式下執行或重新對映以使用 `;` 之外的其他分隔符號。如果仍然遇到問題，請使用 Evennia Web 使用者端。
```

這裡發生的事情是，我們將字串 `"awesome sauce"` 分配給我們選擇命名為 `a` 的變數。在下一條語句中，Python 記住了 `a` 是什麼，我們將其傳遞給 `format()` 以獲得輸出。如果您將 `a` 的值替換為中間的其他值，則會列印 _that_ 。

這是一個統計資料範例，將統計資料移至變數（這裡我們只是設定它們，但在真實遊戲中它們可能會隨著時間的推移而改變，或根據情況進行修改）：

    > py stren, dext, intel = 13, 14, 8 ; print("STR: {}, DEX: {}, INT: {}".format(stren, dext, intel))
    STR: 13, DEX: 14, INT: 8

關鍵是，即使統計資料的值發生變化， print() 語句也不會改變－它只是保持漂亮的列印任何給它的內容。

您也可以使用命名標記，如下所示：

     > py print("STR: {stren}, INT: {intel}, STR again: {stren}".format(dext=10, intel=18, stren=9))
     STR: 9, INT: 18, Str again: 9

我們新增的 `key=value` 對稱為 `format()` 方法的_關鍵字引數_。每個命名引數將轉到字串中匹配的 `{key}`。使用關鍵字時，新增它們的順序並不重要。字串中沒有 `{dext}` 和兩個 `{stren}`，效果很好。

(f-strings)=
### F 弦

使用 `.format()` 非常強大（並且您可以用它做[更多](https://www.w3schools.com/python/ref_string_format.asp)）。但 _f-string_ 可能更方便。 f 字串看起來像普通字串......除了它前面有一個 `f` ，如下所示：

    f"this is now an f-string."

f 字串本身就像任何其他字串一樣。但讓我們使用 f 字串重做之前的範例：

    > py a = "awesome sauce" ; print(f"This is {a}!")
    This is awesome sauce!

我們使用 `{a}` 將該 `a` 變數直接插入 f 字串中。更少的括號
記住和爭論也更容易閱讀！

    > py stren, dext, intel = 13, 14, 8 ; print(f"STR: {stren}, DEX: {dext}, INT: {intel}")
    STR: 13, DEX: 14, INT: 8

在現代 Python 程式碼中，f 字串比 `.format()` 更常用，但要閱讀程式碼，您需要了解兩者。

當我們開始建立指令並需要解析和理解玩家輸入時，我們將探索更複雜的字串概念。

(colored-text)=
### 彩色文字

Python 本身對彩色文字一無所知，這是Evennia 的事情。 Evennia支援傳統MUDs的標準配色。

    > py print("|rThis is red text!|n This is normal color.")

在開始處新增 `|r` 將使我們的輸出變成亮紅色。 `|R` 會使它變成深紅色。 `|n`
給出正常的文字顏色。您也可以使用 0-5 之間的 RGB（紅色-綠色-藍色）值（Xterm256 顏色）：

    > py print("|043This is a blue-green color.|[530|003 Now dark blue text on orange background.")

> 如果您沒有看到預期的顏色，則您的使用者端或終端可能不支援 Xterm256（或
完全沒有顏色）。使用Evennia webclient。

使用指令 `color ansi` 或 `color xterm` 檢視哪些顏色可用。實驗！您也可以在[顏色](../../../Concepts/Colors.md) 檔案中閱讀更多內容。

(importing-code-from-other-modules)=
## 從其他模組匯入程式碼

正如我們在前面幾節中看到的，我們使用 `.format` 來格式化字串，並使用 `me.msg` 來存取 `me` 上的 `msg` 方法。句號字元的這種使用用於存取各種資源，包括其他 Python 模組中的資源。

保持遊戲執行，然後開啟您選擇的文字編輯器。如果你的遊戲資料夾名為
`mygame`，在子資料夾`mygame/world`中建立一個新的文字檔案`test.py`。檔案是這樣的
結構應該看起來：

```
mygame/
    world/
        test.py
```

目前，只需在 `test.py` 中新增一行：

```python
print("Hello World!")
```

```{sidebar} Python模組
這是一個以 `.py` 檔案結尾的文字檔。一個模組
包含 Python 原始碼，並且可以從 Python 內部
透過其 python 路徑匯入來存取其內容。
```

不要忘記_儲存_檔。我們剛剛建立了第一個 Python 模組！
要在遊戲中使用它，我們必須「匯入」它。試試這個：

    > py import world.test
    Hello World

如果您犯了一些錯誤（我們將在下面介紹如何處理錯誤），請確保文字與上面完全相同，然後在遊戲中執行 `reload` 指令以使您的更改生效。

……所以如你所見，匯入`world.test`實際上意味著匯入`world/test.py`。將句點 `.` 視為替換路徑中的 `/`（或 Windows 的 `\`）。

`test.py` 的 `.py` 結尾永遠不會包含在此「Python 路徑」中，但_僅_具有該結尾的檔案可以透過這種方式匯入。 Python 路徑中的 `mygame` 在哪裡？答案是 Evennia 已經告訴 Python 你的 `mygame` 資料夾是尋找匯入的好地方。所以我們不應該在路徑中包含 `mygame` - Evennia 為我們處理這個問題。

當您匯入模組時，它將執行其頂層“級別”。在這種情況下，它會立即
列印“你好世界”。

現在嘗試第二次執行：

    > py import world.test

您將*看不到*這次或任何後續時間的任何輸出！這不是一個錯誤。相反，這是因為 Python 匯入的工作方式 - 它儲存所有匯入的模組，並且會避免多次匯入它們。因此，您的`print`只會在第一次匯入模組時執行。

試試這個：

    > reload

進而

    > py import world.test
    Hello World!

現在我們又看到了。 `reload` 擦除了伺服器記憶體中匯入的內容，因此必須重新匯入。每次想要顯示 hello-world 時都必須執行此操作，這不是很有用。

> 我們將在[稍後的課程](./Beginner-Tutorial-Python-classes-and-objects.md#importing-things) 中回顧更高階的匯入程式碼的方法 - 這是一個重要的主題。但現在，讓我們繼續解決這個特定問題。


(our-first-own-function)=
### 我們的第一個自己的函式

我們希望能夠隨時列印我們的 hello-world 訊息，而不僅僅是在伺服器之後列印一次
重新載入。將 `mygame/world/test.py` 檔案更改為如下所示：

```python
def hello_world():
    print("Hello World!")
```

```{sidebar}
如果您來自其他語言（例如 Javascript 或 C），您可能會熟悉名稱中混合大小寫的變數和函式，例如 `helloWorld()`。雖然您可以選擇以這種方式命名，但它會與其他 Python 程式碼發生衝突 - Python 標準是對所有變數和方法使用小寫字母和下劃線 `_`。
```
當我們轉向多行 Python 程式碼時，需要記住一些重要的事情：

- Python 中大小寫很重要。它必須是 `def` 而不是 `DEF`，`hello_world()` 與 `Hello_World()` 不同。
- 縮排在 Python 中很重要。第二行必須縮排，否則它不是有效的程式碼。您還應該使用一致的縮排長度。我們「強烈」建議您，為了您自己的理智，將編輯器設定為在您按 TAB 鍵時始終縮排 *4 個空格*（**不是**單一製表符）。

那麼關於這個功能。 1號線：

- `def` 是「define」的縮寫，定義一個*函式*（或一個*方法*，如果位於一個物件上）。這是一個[保留的Python關鍵字](https://docs.python.org/2.5/ref/keywords.html)；盡量不要在其他地方使用這些字。
- 函式名稱不能有空格，否則我們幾乎可以稱之為任何名稱。我們稱之為`hello_world`。 Evennia 遵循[Python 的標準命名風格](../../../Coding/Evennia-Code-Style.md)，使用小寫字母和底線。我們建議您也這樣做。
- 第 1 行末尾的冒號（`:`）表示函式頭已完成。

2號線：

- 縮排標記了函式實際操作程式碼的開始（函式的*主體*）。如果我們想要更多的行屬於這個函式，那麼這些行都必須至少從這個縮排層級開始。

現在讓我們試試看。首先`reload`你的遊戲讓它取得我們更新的Python模組，然後匯入它。

    > reload
    > py import world.test

什麼也沒發生！這是因為我們模組中的函式僅透過匯入它不會執行任何操作（這就是我們想要的）。只有當我們“呼叫”它時它才會起作用。所以我們需要先匯入模組，然後再訪問其中的函式：

    > py import world.test ; world.test.hello_world()
    Hello world!

這就是我們的「Hello World」！如前所述，使用分號將多個 Python 語句放在一行上。另請注意先前關於 mud 使用者端使用 `;` 達到自己目的的警告。

那麼那裡發生了什麼事？首先我們像往常一樣匯入`world.test`。但這次模組的「頂層」只定義了一個函式。它實際上並沒有執行該函式的主體。

透過將 `()` 加到 `hello_world` 函式，我們_呼叫_它。也就是說，我們執行函式體並列印文字。現在，我們可以根據需要多次重做此操作，而無需在中間進行`reload`：

    > py import world.test ; world.test.hello_world()
    Hello world!
    > py import world.test ; world.test.hello_world()
    Hello world!

(sending-text-to-others)=
## 向他人傳送文字

`print` 指令是標準的 Python 結構。我們可以在 `py` 指令中使用它，因為我們可以看到輸出。它非常適合除錯和快速測試。但如果您需要向實際玩家傳送文字，`print` 就不行，因為它不知道要傳送給_誰_。試試這個：

    > py me.msg("Hello world!")
    Hello world!

這看起來與 `print` 結果相同，但我們現在實際上正在向特定*物件* `me` 傳送訊息。 `me` 是「us」的捷徑，也就是執行 `py` 指令的。它不是一些特殊的 Python 東西，而是 Evennia 只是為了方便而在 `py` 指令中提供的東西（`self` 是一個別名）。

`me` 是*物件例項*的範例。物件是 Python 中的基礎，Evennia。 `me` 物件還包含許多用於處理該物件的有用資源。我們使用“`.`”存取這些資源。

其中一種資源是 `msg`，其工作方式與 `print` 類似，只不過它將文字傳送到它所在的物件
附於.因此，例如，如果我們有一個物件 `you`，執行 `you.msg(...)` 將會向物件 `you` 傳送一條訊息。

目前，`print` 和 `me.msg` 的行為相同，只需記住 `print` 主要用於
除錯和 `.msg()` 將來對你會更有用。


(parsing-python-errors)=
## 解析Python錯誤

讓我們在剛剛建立的函式中嘗試這個新的文字傳送功能。  返回
您的 `test.py` 檔案並將函式替換為以下內容：

```python
def hello_world():
    me.msg("Hello World!")
```

儲存您的檔案和`reload`您的伺服器以告訴Evennia重新匯入新程式碼，
然後像以前一樣執行它：

     > py import world.test ; world.test.hello_world()

不行－這次你會得到一個_錯誤_！

```python
File "./world/test.py", line 2, in hello_world
    me.msg("Hello World!")
NameError: name 'me' is not defined
```

```{sidebar} 日誌中的錯誤

在常規使用中，回溯通常會出現在日誌中，而不是
在遊戲中。使用`evennia --log`在終端中檢視日誌。製造
如果您預計會出現錯誤但沒有看到它，請務必向後滾動。使用
`Ctrl-C`（或 Mac 上的 `Cmd-C`）退出日誌檢視。
```

這稱為“回溯”。 Python 的錯誤非常友好，大多數時候會告訴您到底出了什麼問題以及出在哪裡。學習解析回溯非常重要，這樣您才能知道如何修復程式碼。

回溯將從_由下而上_讀取：

- （第 3 行）問題是 `NameError` 型別的錯誤...
- （第 3 行）...更具體地說，這是由於變數 `me` 未定義。
- （第2行）這發生在`me.msg("Hello world!")`線上...
- （第 1 行）...位於檔案 `./world/test.py` 的第 `2` 行。

在我們的例子中，回溯很短。上面可能還有更多行，追蹤如何
不同的模組互相呼叫，直到程式到達故障線路。那可以
有時是有用的資訊，但從底層開始閱讀總是一個好的開始。

我們在這裡看到的 `NameError` 是因為模組是它自己獨立的東西。它對其匯入的環境一無所知。它知道`print`是什麼，因為那是一個特殊的[保留的Python關鍵字](https://docs.python.org/2.5/ref/keywords.html)。但 `me` *不是*這樣的保留字（如前所述，它只是 Evennia 為了在 `py` 指令中方便起見而提出的）。就模組而言，`me` 是一個陌生的名字，不知從何而來。因此是`NameError`。

(passing-arguments-to-functions)=
## 將引數傳遞給函式

我們知道，當我們執行 `py` 指令時，`me` 就存在，因為我們可以毫無問題地執行 `py me.msg("Hello World!")`。因此，讓我們將我傳遞給該函式，以便它知道它應該是什麼。返回您的 `test.py` 並將其更改為：

```python
def hello_world(who):
    who.msg("Hello World!")
```
我們現在為函式新增了一個_引數_。我們可以給它取任何名字。無論 `who` 是什麼，我們都會對其呼叫方法 `.msg()`。

像往常一樣，`reload` 伺服器以確保新程式碼可用。

    > py import world.test ; world.test.hello_world(me)
    Hello World!

現在它起作用了。我們_傳遞_ `me` 給我們的函式。它將出現在重新命名為 `who` 的函式內，現在該函式可以正常工作並按預期列印。請注意，`hello_world` 函式並不關心您傳遞給它的內容，只要它有 `.msg()` 方法即可。因此，您可以針對其他合適的目標一遍又一遍地重複使用此函式。

> **額外加分：** 作為練習，嘗試將其他內容傳遞到 `hello_world` 中。嘗試例如
> 傳遞數字 `5` 或字串 `"foo"`。你會收到錯誤訊息，告訴你他們沒有
>attribute `msg`。他們不關心 `me` 本身不是字串或數字。如果你是
>熟悉其他程式語言（尤其是 C/Java），您可能會想在傳送之前開始*驗證* `who` 以確保其型別正確。在 Python 中通常不建議這樣做。 Python 的哲學是在發生錯誤時[處理](https://docs.python.org/2/tutorial/errors.html)
>而不是新增大量程式碼來防止它發生。請參閱[鴨子打字](https://en.wikipedia.org/wiki/Duck_typing)
>以及「先行一步，再看」的概念。


(finding-others-to-send-to)=
## 尋找其他人傳送給

讓我們透過找其他人傳送來結束第一個 Python `py` 速成課程。

在Evennia 的`contrib/` 資料夾(`evennia/contrib/tutorial_examples/mirror.py`) 中有一個方便的小物件，稱為`TutorialMirror`。鏡子將回顯傳送給它的任何內容
它所在的房間。

在遊戲指令列上，我們建立一個映象：

    > create/drop mirror:contrib.tutorials.mirror.TutorialMirror

```{sidebar} 建立物件
`create` 指令首先用於在
[建築材料](./Beginner-Tutorial-Building-Quickstart.md) 教學。你現在應該認識到
它使用“python-path”來告訴 Evennia 從哪裡載入映象的程式碼。
```

您所在的位置應該會出現一面鏡子。

    > look mirror
    mirror shows your reflection:
    This is User #1

你所看到的實際上是你自己在遊戲中的頭像，與`py`指令中的`me`相同。

我們現在的目標相當於`mirror.msg("Mirror Mirror on the wall")`。但我想到的第一件事是行不通的：

    > py mirror.msg("Mirror, Mirror on the wall ...")
    NameError: name 'mirror' is not defined.

這並不奇怪：Python 對「映象」、位置或任何東西一無所知。如前所述，我們一直在使用的 `me` 只是 Evennia 開發人員為 `py` 指令提供的一個方便的東西。他們不可能預測你想和鏡子說話。

相反，我們需要_搜尋_該 `mirror` 物件，然後才能傳送給它。確保您與鏡子位於同一位置，然後嘗試：

    > py me.search("mirror")
    mirror

預設情況下，`me.search("name")` 將搜尋並_傳回_在與 `me` 物件相同的位置_找到的具有給定名稱的物件。如果找不到任何內容，您會看到錯誤。

```{sidebar} 函式返回

雖然像 `print` 這樣的函式只列印它的引數，但它很常見
`return` 的函式/方法是某種結果。想想功能
作為一臺機器——你輸入一些東西，然後輸出你可以使用的結果。在`me.search`的情況下，它將執行資料庫搜尋並吐出它找到的物件。
```

    > py me.search("dummy")
    Could not find 'dummy'.

想要在同一位置找到東西是很常見的，但隨著我們繼續，我們會
發現 Evennia 提供了充足的工具來標記、搜尋和尋找整個遊戲中的內容。

現在我們知道如何找到「映象」物件，我們只需要使用它而不是`me`！

    > py mirror = self.search("mirror") ; mirror.msg("Mirror, Mirror on the wall ...")
    mirror echoes back to you:
    "Mirror, Mirror on the wall ..."

鏡子對於測試很有用，因為它的 `.msg` 方法只是將傳送給它的任何內容回顯到房間。更常見的是與玩家角色交談，在這種情況下，您傳送的文字將出現在他們的遊戲使用者端中。


(multi-line-py)=
## 多行py

到目前為止我們已經在單行模式下使用了`py`，使用`;`來分隔多個輸入。當您想要進行一些快速測試時，這非常方便。但您也可以在 Evennia 內啟動完整的多行 Python 互動式直譯器。

    > py
    Evennia Interactive Python mode
    Python 3.11.0 (default, Nov 22 2022, 11:21:55)
    [GCC 8.2.0] on Linux
    [py mode - quit() to exit]

（輸出的詳細資訊將根據您的Python版本和OS而有所不同）。您現在處於 python 解譯器模式。這意味著
從現在開始你插入的所有內容都將成為Python的一行（你不能再環顧四周或做其他事情）
指令）。

    > print("Hello World")

    >>> print("Hello World")
    Hello World
    [py mode - quit() to exit]

請注意，我們現在不需要將 `py` 放在前面。系統也會回顯您的輸入（即 `>>>` 之後的位元）。為了簡潔起見，在本教學中我們將關閉迴聲。首先退出 `py`，然後使用 `/noecho` 標誌重新開始。

    > quit()
    Closing the Python console.
    > py/noecho
    Evennia Interactive Python mode (no echoing of prompts)
    Python 3.11.0 (default, Nov 22 2022, 11:21:56)
    [GCC 8.2.0] on Linux
    [py mode - quit() to exit]

```{sidebar} 互動式py

- 從 `py` 開始。
- 如果您不希望每行都回顯您的輸入，請使用 `py/noecho`。
- 您的所有輸入現在都將解釋為 Python 程式碼。
- 使用 `quit()` 退出。
```

我們現在可以輸入多行Python程式碼：

    > a = "Test"
    > print(f"This is a {a}.")
    This is a Test.

讓我們試著定義一個函式：

    > def hello_world(who, txt):
    ...
    >     who.msg(txt)
    ...
    >
    [py mode - quit() to exit]

上面一些重要的事情：

- 用 `def` 定義函式意味著我們正在開始一個新的程式碼區塊。 Python 的工作原理是讓你標記內容
帶有縮排的區塊。因此下一行必須手動縮排（4個空格是一個很好的標準）以便
  讓 Python 知道它是函式體的一部分。
- 我們用另一個引數 `txt` 來擴充 `hello_world` 函式。這允許我們傳送任何文字，而不僅僅是
一遍又一遍地「你好世界」。
- 為了告訴 `py` 不再在函式體內新增任何行，我們以空輸入結束。當正常提示返回時，我們知道我們已經完成了。

現在我們定義了一個新函式。讓我們試試看：

    > hello_world(me, "Hello world to me!")
    Hello world to me!

`me` 仍然可供我們使用，因此我們將其作為 `who` 引數以及更長一點的引數傳遞
字串。讓我們將其與尋找鏡子結合。

    > mirror = me.search("mirror")
    > hello_world(mirror, "Mirror, Mirror on the wall ...")
    mirror echoes back to you:
    "Mirror, Mirror on the wall ..."

退出 `py` 模式

    > quit()
    Closing the Python console.

(other-ways-to-test-python-code)=
## 測試 Python 程式碼的其他方法

`py` 指令對於在遊戲中試驗 Python 非常有用。這非常適合快速測試。
但您仍然僅限於透過 telnet 或 webclient 進行工作，這些介面什麼都不知道
關於 Python 本身。

在遊戲外，請前往執行 Evennia 的終端（或執行 `evennia` 指令的任何終端
可用）。

- `cd` 到你的遊戲目錄。
- `evennia shell`

Python shell 將會開啟。這就像 `py` 在遊戲中所做的那樣，除了你沒有
`me` 開箱即用。如果你想要`me`，你需要先找到自己：

    > import evennia
    > me = evennia.search_object("YourChar")[0]

這裡我們利用 evennia 的搜尋功能之一，可以透過直接匯入 `evennia` 來使用。
我們稍後將介紹更高階的搜尋，但可以說，您輸入自己的角色名稱而不是
上面的“YourChar”。

> 最後的 `[0]` 是因為 `.search_object` 回傳一個物件列表，我們想要
找到其中的第一個（從 0 開始計數）。

使用`Ctrl-D`（Mac 上為`Cmd-D`）或`quit()` 退出Python 控制檯。

(ipython)=
## 蟒蛇

The default Python shell is quite limited and ugly. It's *highly* recommended to install `ipython` instead.這個
is a much nicer, third-party Python interpreter with colors and many usability improvements.

    pip install ipython

如果安裝了 `ipython`，`evennia shell` 將自動使用它。

    evennia shell
    ...
    IPython 7.4.0 -- An enhanced Interactive Python. Type '?' for help
    In [1]: You now have Tab-completion:

    > import evennia
    > evennia.<TAB>

也就是說，輸入`evennia.`，然後按TAB鍵 - 您將獲得所有資源的列表
可用於 `evennia` 物件。這對於探索 Evennia 所提供的內容非常有用。例如，
使用箭頭鍵滾動到 `search_object()` 進行填充。

    > evennia.search_object?

新增 `?` 並按回車鍵將為您提供 `.search_object` 的完整檔案。如果您有以下情況，請使用 `??`
想看完整的原始碼。

對於普通的python直譯器，使用`Ctrl-D`/`Cmd-D`或`quit()`退出ipython。

```{important} 持久化程式碼

`py` 和 `python`/`ipython` 的共同點是您編寫的程式碼不是永續性的 - 它會
關閉直譯器後就消失了（但 ipython 會記住你的輸入歷史記錄）。為了製作持久
Python 程式碼，我們需要將其儲存在 Python 模組中，就像我們對 `world/test.py` 所做的那樣。
```


(conclusions)=
## 結論

這涵蓋了相當多的基本 Python 用法。我們列印並格式化字串，定義我們自己的
第一個功能，修復了錯誤，甚至搜尋並與鏡子交談！能夠訪問
遊戲內外的python是測試和除錯的重要技能，但在
實作中，您將在 Python 模組中編寫大部分程式碼。

為此，我們還在 `mygame/` 遊戲目錄中建立了第一個新的 Python 模組，然後匯入並使用它。現在讓我們看看 `mygame/` 資料夾中的其餘內容...
