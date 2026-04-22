(parsing-command-arguments-theory-and-best-practices)=
# 解析指令引數、理論和最佳實踐


本教學將詳細介紹解析指令引數的多種方法。  之後的第一步
[新增指令](Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)通常是解析其引數。  有很多
方法，但有些確實比其他方法更好，本教學將嘗試介紹它們。

如果您是 Python 初學者，本教學可能會對您有很大幫助。  如果您已經熟悉
Python 語法，本教學可能仍包含有用的資訊。  還有很多
我在標準庫中發現的東西讓我感到驚訝，儘管它們一直都在那裡。
對於其他人來說可能也是如此。

在本教學中，我們將：

- 用數字解析引數。
- 使用分隔符號解析引數。
- 看一下可選引數。
- 解析包含物件名稱的引數。

(what-are-command-arguments)=
## 什麼是指令引數？

我將在本教學中詳細討論指令引數和解析。  所以我們要確保
在進一步討論之前先討論同樣的事情：

> 指令是處理特定使用者輸入的 Evennia 物件。

例如，預設的 `look` 是一個指令。  建立 Evennia 遊戲後，並且
連線到它後，您應該能夠輸入 `look` 來檢視周圍的情況。  在這種情況下，`look` 是
一個指令。

> 指令引數是在指令之後傳遞的附加文字。

按照相同的範例，您可以輸入 `look self` 來檢視自己。  在這種情況下，`self`
是`look`之後指定的文字。  `" self"` 是 `look` 指令的引數。

作為遊戲開發人員，我們的部分任務是將使用者輸入（主要是指令）與遊戲中的操作連線起來。
遊戲。  大多數時候，輸入指令是不夠的，我們必須依賴引數來執行
更準確地指定操作。

採取`say`指令。  如果您無法指定指令引數的內容 (`say hello!`)，
您在遊戲中與其他人溝通會遇到困難。  人們需要建立一個不同的
對每種單字或句子都進行指令，這當然是不切實際的。

最後一件事：什麼是解析？

> 在我們的例子中，解析是將指令引數轉換為我們可以使用的東西的過程。

我們通常不會按原樣使用指令引數（它只是文字，在 Python 中型別為 `str`）。  我們
需要提取有用的資訊。  我們可能想向使用者詢問號碼或姓名
另一個角色出現在同一個房間。  我們現在將看看如何做到這一切。

(working-with-strings)=
## 使用字串

用物件術語來說，當你在 Evennia 中寫指令時（當你寫 Python 類別時），
引數儲存在 `args` attribute 中。  也就是說，在你的 `func` 方法中，你可以
訪問 `self.args` 中的指令引數。

(selfargs)=
### self.args

首先，看這個例子：

```python
class CmdTest(Command):

    """
    Test command.

    Syntax:
      test [argument]

    Enter any argument after test.

    """

    key = "test"

    def func(self):
        self.msg(f"You have entered: {self.args}.")
```

如果您新增此指令並對其進行測試，您將收到與您輸入的內容完全相同的內容，而無需任何操作
解析：

```
> test Whatever
You have entered:  Whatever.
> test
You have entered: .
```

> 以 `>` 開頭的行表示您在用戶端中輸入的內容。  其他幾行是什麼
您從遊戲伺服器收到。

這裡請注意兩件事：

1. 指令鍵（此處為“test”）和指令引數之間的左側空格不會被刪除。
這就是為什麼我們的輸出中第 2 行有兩個空格。嘗試輸入“testok”之類的內容。
2. 即使您不輸入指令引數，該指令仍將以空字串呼叫
在`self.args`中。

也許對我們的程式碼稍作修改就可以看到發生了什麼。  我們會
使用一個小快捷方式強制 Python 將指令引數顯示為除錯字串。

```python
class CmdTest(Command):

    """
    Test command.

    Syntax:
      test [argument]

    Enter any argument after test.

    """

    key = "test"

    def func(self):
        self.msg(f"You have entered: {self.args!r}.")
```

我們唯一更改的行是最後一行，我們在大括號之間新增了 `!r` 來告訴
Python 列印引數的除錯版本（repr-ed 版本）。  讓我們看看結果：

```
> test Whatever
You have entered: ' Whatever'.
> test
You have entered: ''.
> test And something with '?
You have entered: " And something with '?".
```

這將以您在 Python 直譯器中看到的方式顯示字串。  可能會更容易
無論如何，閱讀...進行除錯。

我非常堅持這一點，因為它至關重要：指令引數只是一個字串（型別為
`str`），我們將用它來解析它。  您將看到的內容大多不是 Evennia 特定的，而是
Python 特定的，可以在您有相同需求的任何其他專案中使用。

(stripping)=
### 剝離

正如您所看到的，我們的指令引數與空格一起儲存。  以及指令之間的空格
而且爭論往往並不重要。

> 為什麼它一直存在？

Evennia會盡力尋找符合的指令。  如果使用者輸入您的指令鍵
引數（但省略空格），Evennia 仍然能夠找到並呼叫該指令。  你可能會
已經看到如果使用者輸入 `testok` 會發生什麼。  在這種情況下，`testok` 很可能是
指令（Evennia 檢查該指令），但沒有看到任何內容，並且因為有一個 `test` 指令，Evennia
使用引數 `"ok"` 呼叫它。

但大多數時候，我們並不真正關心這個剩餘空間，所以你經常會看到程式碼
刪除它。  在 Python 中有不同的方法可以做到這一點，但指令案例是 `strip`
`str` 及其表兄弟 `lstrip` 和 `rstrip` 上的方法。

- `strip`：刪除兩端的一個或多個字元（空格或其他字元）
細繩。
- `lstrip`：同樣的事情，但只從字串的左端（左條帶）刪除。
- `rstrip`：同樣的事情，但只從字串的右端（右條帶）刪除。

一些 Python 範例可能會有所幫助：

```python
>>> '   this is '.strip() # remove spaces by default
'this is'
>>> "   What if I'm right?   ".lstrip() # strip spaces from the left
"What if I'm right?   "
>>> 'Looks good to me...'.strip('.') # removes '.'
'Looks good to me'
>>> '"Now, what is it?"'.strip('"?') # removes '"' and '?' from both ends
'Now, what is it'
```

通常，因為我們不需要空格分隔符，但仍然希望我們的指令在沒有空格分隔符的情況下工作
分隔符，我們在指令引數上呼叫 `lstrip`：

```python
class CmdTest(Command):

    """
    Test command.

    Syntax:
      test [argument]

    Enter any argument after test.

    """

    key = "test"

    def parse(self):
        """Parse arguments, just strip them."""
        self.args = self.args.lstrip()

    def func(self):
        self.msg(f"You have entered: {self.args!r}.")
```

> 我們現在開始重寫指令的 `parse` 方法，該方法通常僅適用於
引數解析。  該方法在`func`之前執行，因此`func()`中的`self.args`將包含
我們的`self.args.lstrip()`。

我們來試試：

```
> test Whatever
You have entered: 'Whatever'.
> test
You have entered: ''.
> test And something with '?
You have entered: "And something with '?".
> test     And something with lots of spaces
You have entered: 'And something with lots of spaces'.
```

保留字串末尾的空格，但刪除開頭的所有空格：

> `strip`、`lstrip` 和 `rstrip` 不含引數將去除空格、換行符和其他常見的
分隔符號。  您可以指定一個或多個字元作為引數。  如果您指定多個
字元，所有這些都將從原始字串中刪除。

(convert-arguments-to-numbers)=
### 將引數轉換為數字

如所指出的，`self.args` 是一個字串（型別為 `str`）。  如果我們希望使用者輸入一個
號碼？

讓我們舉一個非常簡單的例子：建立一個指令 `roll`，它允許滾動六面骰。
玩家必須猜測數字，並將數字指定為引數。  為了獲勝，玩家必須
將數字與骰子配對。  讓我們來看一個例子：

```
> roll 3
You roll a die.  It lands on the number 4.
You played 3, you have lost.
> dice 1
You roll a die.  It lands on the number 2.
You played 1, you have lost.
> dice 1
You roll a die.  It lands on the number 1.
You played 1, you have won!
```

如果這是您的第一個指令，那麼這是嘗試編寫它的好機會。  一個簡單的指令
有限的角色始終是不錯的起始選擇。  這是我們（首先）如何寫它......但是它
不會照原樣工作，我警告你：

```python
from random import randint

from evennia import Command

class CmdRoll(Command):

    """
    Play random, enter a number and try your luck.

    Usage:
      roll <number>

    Enter a valid number as argument.  A random die will be rolled and you
    will win if you have specified the correct number.

    Example:
      roll 3

    """

    key = "roll"

    def parse(self):
        """Convert the argument to a number."""
        self.args = self.args.lstrip()

    def func(self):
        # Roll a random die
        figure = randint(1, 6) # return a pseudo-random number between 1 and 6, including both
        self.msg(f"You roll a die.  It lands on the number {figure}.")

        if self.args == figure: # THAT WILL BREAK!
            self.msg(f"You played {self.args}, you have won!")
        else:
            self.msg(f"You played {self.args}, you have lost.")
```

如果你嘗試這段程式碼，Python 會抱怨你嘗試將數字與字串進行比較：`figure`
是一個數字，`self.args` 是一個字串，不能在 Python 中按原樣進行比較。  Python 不做
像某些語言一樣「隱式轉換」。  順便說一句，這有時可能會很煩人，而其他
有時你會很高興它試圖鼓勵你明確而不是隱晦地表達要做什麼
做。  這是程式設計師之間持續爭論的話題。  讓我們繼續前進吧！

因此我們需要將指令引數從 `str` 轉換為 `int`。  有幾種方法可以做到
它。  但正確的方法是嘗試轉換並處理`ValueError` Python 異常。

在 Python 中將 `str` 轉換為 `int` 非常簡單：只需使用 `int` 函式，給它
字串並傳回一個整數（如果可以的話）。  如果不能，則會提高`ValueError`。  所以
我們需要抓住這一點。  然而，我們也必須向Evennia表明，這個數字應該是
無效，不應進行進一步的解析。  這是我們指令的新嘗試
轉換：

```python
from random import randint

from evennia import Command, InterruptCommand

class CmdRoll(Command):

    """
    Play random, enter a number and try your luck.

    Usage:
      roll <number>

    Enter a valid number as argument.  A random die will be rolled and you
    will win if you have specified the correct number.

    Example:
      roll 3

    """

    key = "roll"

    def parse(self):
        """Convert the argument to number if possible."""
        args = self.args.lstrip()

        # Convert to int if possible
        # If not, raise InterruptCommand.  Evennia will catch this
        # exception and not call the 'func' method.
        try:
            self.entered = int(args)
        except ValueError:
            self.msg(f"{args} is not a valid number.")
            raise InterruptCommand

    def func(self):
        # Roll a random die
        figure = randint(1, 6) # return a pseudo-random number between 1 and 6, including both
        self.msg(f"You roll a die.  It lands on the number {figure}.")

        if self.entered == figure:
            self.msg(f"You played {self.entered}, you have won!")
        else:
            self.msg(f"You played {self.entered}, you have lost.")
```

在享受結果之前，讓我們進一步檢查 `parse` 方法：它的作用是嘗試
將輸入的引數從 `str` 轉換為 `int`。  這可能會失敗（如果使用者輸入 `roll
something`). 在這種情況下，Python 會拋出 `ValueError` 例外。 我們在我們的
`try/except` 區塊，向使用者傳送訊息並引發 `InterruptCommand` 異常
回應告訴 Evennia 不要執行 `func()`，因為我們沒有提供有效的數字。

在`func`方法中，我們不使用`self.args`，而是使用我們在中定義的`self.entered`
我們的 `parse` 方法。  您可以預期，如果執行 `func()`，則 `self.entered` 包含有效的
數量。

如果您嘗試此指令，這次它將按預期工作：數字將按預期轉換
並與模具卷進行比較。  您可能會花幾分鐘玩這個遊戲。  暫停！

我們還需要解決其他問題：在我們的小範例中，我們只希望使用者輸入
1 到 6 之間的正數。使用者可以輸入 `roll 0` 或 `roll -8` 或 `roll 208`
沒關係，遊戲仍然有效。  這可能值得解決。  同樣，你可以寫一個
這樣做的條件，但由於我們捕獲了異常，我們最終可能會得到更乾淨的東西
透過分組：

```python
from random import randint

from evennia import Command, InterruptCommand

class CmdRoll(Command):

    """
    Play random, enter a number and try your luck.

    Usage:
      roll <number>

    Enter a valid number as argument.  A random die will be rolled and you
    will win if you have specified the correct number.

    Example:
      roll 3

    """

    key = "roll"

    def parse(self):
        """Convert the argument to number if possible."""
        args = self.args.lstrip()

        # Convert to int if possible
        try:
            self.entered = int(args)
            if not 1 <= self.entered <= 6:
                # self.entered is not between 1 and 6 (including both)
                raise ValueError
        except ValueError:
            self.msg(f"{args} is not a valid number.")
            raise InterruptCommand

    def func(self):
        # Roll a random die
        figure = randint(1, 6) # return a pseudo-random number between 1 and 6, including both
        self.msg(f"You roll a die.  It lands on the number {figure}.")

        if self.entered == figure:
            self.msg(f"You played {self.entered}, you have won!")
        else:
            self.msg(f"You played {self.entered}, you have lost.")
```

使用這樣的分組異常可以讓我們的程式碼更容易閱讀，但如果你覺得更舒服
然後檢查使用者輸入的數字是否在正確的範圍內，您可以在
後一種情況。

> 請注意，我們僅在最後一次嘗試中更新了 `parse` 方法，而不是 `func()` 方法
保持不變。  這是將引數解析與指令處理分開的目標之一，
這兩個操作最好保持隔離。

(working-with-several-arguments)=
### 使用多個引數

通常一個指令需要多個引數。  到目前為止，在我們使用“roll”指令的範例中，我們只
期望有一個引數：一個數字並且只是一個數字。  如果我們想讓使用者指定幾個怎麼辦？
數字？  首先是擲骰子的數量，然後是猜測？

> 如果您擲 5 個骰子，您不會經常獲勝，但僅此而已。

所以我們想解釋這樣的指令：

    > roll 3 12

（理解：擲3個骰子，我猜總數是12。）

我們需要的是剪下我們的指令引數，即 `str`，在空格處斷開它（我們使用
空格作為分隔符號）。  Python 提供了我們將使用的 `str.split` 方法。  再說一次，這裡有
Python 直譯器的一些範例：

    >>> args = "3 12"
    >>> args.split(" ")
    ['3', '12']
    >>> args = "a command with several arguments"
    >>> args.split(" ")
    ['a', 'command', 'with', 'several', 'arguments']
    >>>

正如你所看到的，`str.split` 會將我們的字串「轉換」為字串列表。  指定的
引數（在我們的例子中為 `" "`）用作分隔符號。  所以Python會瀏覽我們的原始字串。  當它
看到一個分隔符，它會採用該分隔符之前的任何內容並將其附加到清單中。

這裡的要點是 `str.split` 將用於分割我們的引數。  但是，正如你從
上面的輸出，我們此時永遠無法確定列表的長度：

    >>> args = "something"
    >>> args.split(" ")
    ['something']
    >>> args = ""
    >>> args.split(" ")
    ['']
    >>>

同樣，我們可以使用條件來檢查分割引數的數量，但 Python 提供了更好的方法
方法，利用其異常機制。  我們將為 `str.split` 提供第二個引數，即
要做的最大分割數。  讓我們來看一個例子，這個功能一開始可能會令人困惑
一目瞭然：

    >>> args = "that is something great"
    >>> args.split(" ", 1) # one split, that is a list with two elements (before, after)
[‘那’，‘是一件很棒的事’]
   >>>

根據需要多次閱讀此示例以理解它。  我們給出的第二個論點
`str.split`不是應該回傳的清單長度，而是我們有的次數
分裂。  因此，我們在這裡指定 1，但我們得到一個包含兩個元素的列表（在分隔符號之前，
在分隔符之後）。

> 如果 Python 無法分割我們請求的次數，會發生什麼事？

它不會：

    >>> args = "whatever"
    >>> args.split(" ", 1) # there isn't even a space here...
    ['whatever']
    >>>

這是我希望有一個例外的時刻，但沒有得到。  但還有另一種方法
如果發生錯誤：變數解包，則會引發異常。

我們在這裡不會詳細討論這個功能。  事情會很複雜。  但程式碼確實是
使用簡單。  讓我們以 roll 指令為例，但要加入第一個引數：
the number of dice to roll.

```python
from random import randint

from evennia import Command, InterruptCommand

class CmdRoll(Command):

    """
    Play random, enter a number and try your luck.

    Specify two numbers separated by a space.  The first number is the
    number of dice to roll (1, 2, 3) and the second is the expected sum
    of the roll.

    Usage:
      roll <dice> <number>

    For instance, to roll two 6-figure dice, enter 2 as first argument.
    If you think the sum of these two dice roll will be 10, you could enter:

        roll 2 10

    """

    key = "roll"

    def parse(self):
        """Split the arguments and convert them."""
        args = self.args.lstrip()

        # Split: we expect two arguments separated by a space
        try:
            number, guess = args.split(" ", 1)
        except ValueError:
            self.msg("Invalid usage.  Enter two numbers separated by a space.")
            raise InterruptCommand

        # Convert the entered number (first argument)
        try:
            self.number = int(number)
            if self.number <= 0:
                raise ValueError
        except ValueError:
            self.msg(f"{number} is not a valid number of dice.")
            raise InterruptCommand

        # Convert the entered guess (second argument)
        try:
            self.guess = int(guess)
            if not 1 <= self.guess <= self.number * 6:
                raise ValueError
        except ValueError:
            self.msg(f"{self.guess} is not a valid guess.")
            raise InterruptCommand

    def func(self):
        # Roll a random die X times (X being self.number)
        figure = 0
        for _ in range(self.number):
            figure += randint(1, 6)

        self.msg(f"You roll {self.number} dice and obtain the sum {figure}.")

        if self.guess == figure:
            self.msg(f"You played {self.guess}, you have won!")
        else:
            self.msg(f"You played {self.guess}, you have lost.")
```

`parse()` 方法的開頭是我們最感興趣的：

```python
try:
    number, guess = args.split(" ", 1)
except ValueError:
    self.msg("Invalid usage.  Enter two numbers separated by a space.")
    raise InterruptCommand
```

我們使用 `str.split` 分割引數，但我們將結果捕獲到兩個變數中。  Python 很聰明
足以知道我們想要第一個變數中空格的左邊是什麼，右邊的是什麼
第二個變數中的空格。  如果字串中甚至沒有空格，Python 將引發
`ValueError` 異常。

這段程式碼比瀏覽`str.split`回傳的字串更容易閱讀。  我們可以
按照我們之前的方式轉換這兩個變數。  其實這方面並沒有那麼多的改變
版本和前一版本相比，大部分是由於為了清晰起見而進行了名稱更改。

> 在解析指令時，以最大分割數分割字串是很常見的情況
論據。  您也可以看到 `str.rspli8t` 方法執行相同的操作，但從右側
字串。  因此，它將嘗試在字串末尾找到分隔符號並努力實現
它的開始。

我們使用空格作為分隔符號。  這是完全沒有必要的。  你可能還記得
大多數預設 Evennia 指令可以採用 `=` 符號作為分隔符號。  現在你知道如何解析它們了
還有：

    >>> cmd_key = "tel"
    >>> cmd_args = "book = chest"
    >>> left, right = cmd_args.split("=") # mighht raise ValueError!
    >>> left
    'book '
    >>> right
    ' chest'
    >>>

(optional-arguments)=
### 可選引數

有時，您會遇到具有可選引數的指令。  這些論點不
必要的，但如果需要更多資訊，可以設定它們。  我不會提供完整的指令
程式碼在這裡，但足以顯示 Python 中的機制：

同樣，我們將使用 `str.split`，因為我們知道我們可能根本沒有任何分隔符號。  例如，
玩家可以輸入「tel」指令，如下所示：

    > tel book
    > tell book = chest

等號及其後面指定的內容是可選的。  我們的一個可能的解決方案
`parse` 方法是：

```python
    def parse(self):
        args = self.args.lstrip()

        # = is optional
        try:
            obj, destination = args.split("=", 1)
        except ValueError:
            obj = args
            destination = None
```

如果使用者沒有指定任何等號，此程式碼會將使用者輸入的所有內容放在 `obj` 中。
否則，等號之前的內容會進入`obj`，等號之後的內容會進入
`destination`。  這使得之後可以進行快速測試，使用更少的條件來獲得更健壯的程式碼
如果您不小心，可能很容易破壞您的程式碼。

> 同樣，我們在這裡指定了最大分割數。  如果使用者輸入：

    > tel book = chest = chair

那麼`destination`將包含：`" chest = chair"`。  這通常是所希望的，但這取決於您
根據您的喜好設定解析。

(evennia-searches)=
## Evennia 次搜尋

在快速瀏覽了一些 `str` 方法之後，我們將看看一些 Evennia 特定的功能
在標準 Python 中找不到。

一項非常常見的任務是將 `str` 轉換為 Evennia 物件。  就拿前面的例子來說：
在變數中包含 `"book"` 很好，但我們更想知道使用者在說什麼
關於...這`"book"`是什麼？

為了從字串中獲取物件，我們執行 Evennia 搜尋。  Evennia 提供了 `search` 方法
所有型別分類的物件（您很可能會在角色或帳戶上使用該物件）。  這個方法
支援非常廣泛的引數並且有[它自己的教學](Beginner-Tutorial/Part1/Beginner-Tutorial-Searching-Things.md)。
一些有用案例的例子如下：

(local-searches)=
### 本地搜尋

當帳號或角色輸入指令時，會在`caller`中找到該帳號或角色
attribute。  因此，`self.caller` 將包含一個帳戶或一個角色（或 session，如果是的話）
session 指令，儘管不那麼頻繁）。  `search` 方法將在此可用
來電者。

讓我們以我們的小「tel」指令為例。  使用者可以指定一個物件為
論點：

```python
    def parse(self):
        name = self.args.lstrip()
```

然後我們需要將此字串「轉換」為 Evennia 物件。  將搜尋 Evennia 物件
預設位於呼叫者的位置及其內容中（也就是說，如果該指令已被
角色輸入後，會搜尋該角色房間內的物品以及該角色的房間內的物品
庫存）。

```python
    def parse(self):
        name = self.args.lstrip()

        self.obj = self.caller.search(name)
```

我們在這裡只為 `search` 方法指定一個引數：要搜尋的字串。  如果 Evennia 找到
匹配，它將返回它，我們將其儲存在 `obj` attribute 中。  如果找不到任何東西，它會
回傳 `None` 所以我們需要檢查：

```python
    def parse(self):
        name = self.args.lstrip()

        self.obj = self.caller.search(name)
        if self.obj is None:
            # A proper error message has already been sent to the caller
            raise InterruptCommand
```

就是這樣。  在此條件之後，您知道 `self.obj` 中的內容是有效的 Evennia 物件
（另一個角色，一個物體，一個出口......）。

(quiet-searches)=
### 安靜的搜尋

預設情況下，Evennia 將處理在搜尋中找到多個匹配項的情況。  使用者
將被要求縮小範圍並重新輸入指令。  但是，您可以要求退還
匹配列表並自行處理該列表：

```python
    def parse(self):
        name = self.args.lstrip()

        objs = self.caller.search(name, quiet=True)
        if not objs:
            # This is an empty list, so no match
            self.msg(f"No {name!r} was found.")
            raise InterruptCommand
        
        self.obj = objs[0] # Take the first match even if there are several
```

為了取得列表，我們所做的只是 `search` 方法中的關鍵字引數：`quiet`。  如果設定
到 `True`，那麼錯誤將被忽略，並且始終返回一個列表，因此我們需要這樣處理它。
請注意，在此範例中，`self.obj` 也會包含一個有效物件，但如果有多個匹配項
發現，`self.obj` 將包含第一個，即使有更多匹配。

(global-searches)=
### 全球搜尋

預設情況下，Evennia將執行本地搜尋，即受所在位置限制的搜尋
來電者是。  如果要進行全域搜尋（在整個資料庫中搜尋），只需設定
`global_search` 關鍵字引數到 `True`：

```python
    def parse(self):
        name = self.args.lstrip()
        self.obj = self.caller.search(name, global_search=True)
```

(conclusion)=
## 結論

解析指令引數對於大多數遊戲設計師來說至關重要。  如果你設計“智慧”指令，
使用者應該能夠在不閱讀幫助或快速檢視的情況下猜測如何使用它們
說幫忙。  好的指令對於使用者來說是直覺的。  更好的指令會照著指示去做。  對於
遊戲設計師致力於MUDs，指令是使用者進入遊戲的主要入口點。  這是
沒有什麼微不足道的。  如果指令正確執行（如果它們的引數被解析，如果它們的行為不正確）
意想不到的方式並報告正確的錯誤），您將擁有可能留下來的更快樂的玩家
遊戲時間較長。  我希望本教學能夠為您提供一些關於如何提高您的指令的指導
解析。  當然，您還會發現其他方法，或者您已經在自己的​​應用程式中使用的方法。
程式碼。
