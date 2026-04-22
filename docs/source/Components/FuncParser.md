(funcparser-inline-text-parsing)=
# FuncParser內嵌文字解析

[FuncParser](evennia.utils.funcparser.FuncParser) 提取並執行嵌入在 `$funcname(args, kwargs)` 形式的字串中的“行內函數”，執行匹配的“行內函數”並將呼叫替換為呼叫的返回值。

為了測試它，讓我們告訴 Evennia 在每個傳出訊息上應用 Funcparser。預設會停用此功能（並非每個人都需要此功能）。要啟用，請新增到您的設定檔：

FUNCPARSER_PARSE_OUTGOING_MESSAGES_ENABLED = 正確

重新載入後，您可以在遊戲中嘗試此操作

```shell
> say I got $randint(1,5) gold!
You say "I got 3 gold!"
```

要轉義 inlinefunc（e.g。向某人解釋它是如何工作的，請使用 `$$`）

```{shell}
> say To get a random value from 1 to 5, use $$randint(1,5).
You say "To get a random value from 1 to 5, use $randint(1,5)."
```

雖然 `randint` 的外觀和工作方式可能與標準 Python 庫中的 `random.randint` 類似，但它_不是_。相反，它是一個名為 `randint` 的 `inlinefunc`，可供 Evennia 使用（後者又使用標準函式庫函式）。出於安全原因，只有明確指定用作行內函數的函式才是可行的。

您可以手動應用`FuncParser`。解析器使用它應該在該字串中識別的 inlinefunc 進行初始化。下面是一個解析器只理解單一 `$pow` inlinefunc 的範例：

```python
from evennia.utils.funcparser import FuncParser

def _power_callable(*args, **kwargs):
    """This will be callable as $pow(number, power=<num>) in string"""
    pow = int(kwargs.get('power', 2))
    return float(args[0]) ** pow

# create a parser and tell it that '$pow' means using _power_callable
parser = FuncParser({"pow": _power_callable})

```
接下來，只需將字串傳遞到解析器中，其中包含 `$func(...)` 標記：

```python
parser.parse("We have that 4 x 4 x 4 is $pow(4, power=3).")
"We have that 4 x 4 x 4 is 64."
```

通常返回總是轉換為字串，但您也可以從呼叫中獲取實際的資料型別：

```python
parser.parse_to_any("$pow(4)")
16
```

您不必從頭開始定義所有行內函數。在 `evennia.utils.funcparser` 中，您將找到可以匯入並插入解析器的現成的內嵌函式字典。有關缺陷，請參閱下面的[預設 funcparser 可呼叫物件](#default-funcparser-callables)。

(working-with-funcparser)=
## 與 FuncParser 一起工作

FuncParser 可以應用於任何字串。開箱即用，它適用於以下幾種情況：

- _傳出訊息_。從伺服器傳送的所有訊息都透過 FuncParser 進行處理，並且每個可呼叫物件都提供接收訊息的物件的 [Session](./Sessions.md)。這可能允許即時修改訊息，使不同的收件者看起來有所不同。
- _原型值_。 [Prototype](./Prototypes.md) 字典的值透過解析器執行，以便每個可呼叫物件都獲得原型其餘部分的參考。在原型 ORM 中，這將允許建構者安全地呼叫函式將非字串值設為原型值、獲取隨機值、引用
原型的其他領域等等。
- _向他人傳達訊息時的演員立場_。在 [Object.msg_contents](evennia.objects.objects.DefaultObject.msg_contents) 方法中，將解析傳出字串以查詢特殊的 `$You()` 和 `$conj()` 可呼叫物件，以確定給定收件人是否
應該看到“你”或角色的名字。

```{important}

內嵌函式解析器並非設計為「軟程式碼」程式語言。例如，它沒有迴圈和條件等內容。雖然原則上您可以擴充套件它來執行非常高階的操作並為構建者提供大量功能，但Evennia 希望您在遊戲外部而不是遊戲內部在適當的文字編輯器中進行全面編碼。
```

您可以將行內函數解析套用至任何字串。的
[FuncParser](evennia.utils.funcparser.FuncParser) 匯入為 `evennia.utils.funcparser`。

```python
from evennia.utils import funcparser

parser = FuncParser(callables, **default_kwargs)
parsed_string = parser.parse(input_string, raise_errors=False,
                              escape=False, strip=False,
                              return_str=True, **reserved_kwargs)

# callables can also be passed as paths to modules
parser = FuncParser(["game.myfuncparser_callables", "game.more_funcparser_callables"])
```

這裡，`callables` 指向普通 Python 函式的集合（請參閱下一節）供您製作
當您用它解析字串時，解析器可以使用它。它可以是
- `{"functionname": callable,...}` 的 `dict`。這使您可以準確選擇哪些可呼叫物件
包括以及如何命名它們。您是否希望一個可呼叫物件可以在多個名稱下使用？
  只需使用不同的鍵將其多次新增到字典中即可。
- 模組的 `module` 或（較常見）`python-path`。這個模組可以定義一個字典
`FUNCPARSER_CALLABLES = {"funcname": callable,...}` - 這將像上面的 `dict` 一樣被匯入和使用。
  如果沒有定義這樣的變數，則模組中的_every_頂級函式（其名稱不以
  底線 `_`) 將被視為合適的可呼叫物件。函式的名稱將是 `$funcname`
  透過它可以被呼叫。
- `list` 的模組/路徑。這允許您從多個來源提取模組進行解析。
- `**default` kwargs 是可選的 kwargs，將傳遞給 _all_
每次使用此解析器時都會呼叫 - 除非使用者在中明確覆蓋它
  他們的電話。這對於提供使用者可以使用的合理標準非常有用
  根據需要進行調整。

`FuncParser.parse` 需要更多引數，並且對於每個解析的字串可能會有所不同。

- `raise_errors` - 預設情況下，可呼叫的任何錯誤都會被悄悄忽略，結果
失敗的函式呼叫將逐字顯示。如果設定了`raise_errors`，
  然後解析將停止，並且將引發發生的任何異常。由你來處理
  這個正確。
- `escape` - 傳回一個字串，其中每個 `$func(...)` 已轉義為 `\$func()`。
- `strip` - 從字串中刪除所有 `$func(...)` 呼叫（就好像每個呼叫都回傳 `''`）。
- `return_str` - 當 `True`（預設）時，`parser` 始終傳回字串。如果`False`，可能會返回
字串中單一函式呼叫的回傳值。這與使用 `.parse_to_any` 相同
  方法。
- `**reserved_keywords` 總是被傳遞給字串中的每個可呼叫物件。
它們會覆蓋例項化解析器時給出的任何 `**defaults` 並且不能
  被使用者覆蓋 - 如果他們輸入相同的 kwarg 它將被忽略。
  這對於提供當前的 session、設定等非常有用。
- `funcparser` 和 `raise_errors`
總是新增為保留關鍵字 - 第一個是
  向後引用 `FuncParser` 例項和第二個例項
  是賦予 `FuncParser.parse` 的 `raise_errors` 布林值。

以下是使用預設/保留關鍵字的範例：

```python
def _test(*args, **kwargs):
    # do stuff
    return something

parser = funcparser.FuncParser({"test": _test}, mydefault=2)
result = parser.parse("$test(foo, bar=4)", myreserved=[1, 2, 3])
```
這裡可呼叫的將稱為

```python
_test('foo', bar='4', mydefault=2, myreserved=[1, 2, 3],
      funcparser=<FuncParser>, raise_errors=False)
```

如果我們以 `$test(mydefault=...)` 進行呼叫，則 `mydefault=2` kwarg 可能會被覆蓋，但 `myreserved=[1, 2, 3]` 將_始終_按原樣傳送，並將覆蓋呼叫 `$test(myreserved=...)`。
`funcparser`/`raise_errors` kwargs 也總是作為保留 kwargs 包含在內。

(defining-custom-callables)=
## 定義自訂可呼叫物件

解析器可用的所有可呼叫物件必須具有以下簽名：

```python
def funcname(*args, **kwargs):
    # ...
    return something
```

> 必須始終包含 `*args` 和 `**kwargs`。如果您不確定 `*args` 和 `**kwargs` 在 Python 中如何運作，[在此處閱讀有關它們](https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3)。

可呼叫物件中最裡面的 `$funcname(...)` 呼叫的輸入始終是 `str`。這是
`$toint` 函式的範例；它將數字轉換為整數。

    "There's a $toint(22.0)% chance of survival."

將輸入 `$toint` 可呼叫（如 `args[0]`）的是 _string_ `"22.0"`。該函式負責將其轉換為數字，以便我們可以將其轉換為整數。我們還必須正確處理無效輸入（例如非數字）。

如果您想標記錯誤，請提出 `evennia.utils.funcparser.ParsingError`。這會停止字串的整個解析，並且可能會也可能不會引發異常，這取決於您在建立解析器時設定 `raise_errors` 的內容。

但是，如果您_巢狀_函式，則最內層函式的傳回值可能不是
一個字串。讓我們介紹一下 `$eval` 函式，它使用以下方法計算簡單表示式
Python 的 `literal_eval` 和/或 `simple_eval`。它會傳回任何資料型別
評估為.

    "There's a $toint($eval(10 * 2.2))% chance of survival."

由於 `$eval` 是最裡面的呼叫，因此它將獲取一個字串作為輸入 - 字串 `"10 * 2.2"`。
它對此進行評估並返回 `float` `22.0`。這次最外面的 `$toint` 將被呼叫
這個 `float` 而不是用字串。

> 安全地驗證您的輸入非常重要，因為使用者最終可能會以任何順序巢狀您的可呼叫物件。請參閱下一節，以瞭解有助於解決此問題的有用工具。

在這些範例中，結果將嵌入到較大的字串中，因此整個解析的結果將是一個字串：

```python
  parser.parse(above_string)
  "There's a 22% chance of survival."
```

但是，如果您使用`parse_to_any`（或`parse(..., return_str=False)`）並且_不要在最外層函式呼叫周圍新增任何額外的字串_，您將獲得最外層可回撥的返回型別：

```python
parser.parse_to_any("$toint($eval(10 * 2.2)")
22
parser.parse_to_any("the number $toint($eval(10 * 2.2).")
"the number 22"
parser.parse_to_any("$toint($eval(10 * 2.2)%")
"22%"
```

(escaping-special-character)=
### 轉義特殊字元

當在字串中輸入 funcparser 可呼叫物件時，它看起來像常規的
字串內的函式呼叫：

```python
"This is a $myfunc(arg1, arg2, kwarg=foo)."
```

逗號 (`,`) 和等號 (`=`) 被視為分隔引數並
誇格斯。同樣，右括號 (`)`) 結束引數清單。
有時你會想在引數中包含逗號而不破壞
引數列表。

```python
"The $format(forest's smallest meadow, with dandelions) is to the west."
```

你可以透過多種方式逃脫。

- 在 `,` 和 `=` 等特殊字元前加入轉義字元 `\`

```python
"The $format(forest's smallest meadow\, with dandelions) is to the west."
```

- 將字串用雙引號引起來。與原始 Python 不同，你
無法用單引號 `'` 轉義，因為這些也可能是撇號（例如
`forest's` 以上）。結果將是一個逐字字串，其中包含
除了最外面的雙引號之外的所有內容。

```python
'The $format("forest's smallest meadow, with dandelions") is to the west.'
```
- 如果您希望逐字雙引號出現在字串中，您可以轉義
他們依次與`\"`。

```python
'The $format("forest's smallest meadow, with \"dandelions\"') is to the west.'
```

(safe-convertion-of-inputs)=
### 輸入的安全轉換

由於您不知道使用者可以按什麼順序使用您的可呼叫物件，因此他們應該
始終檢查其輸入的型別並轉換為可呼叫所需的型別。
另請注意，從字串轉換時，您輸入的內容有限制
可以支援。這是因為 FunctionParser 字串可以被使用
非開發者玩家/建造者和一些東西（例如複雜的
類別/可呼叫物件等）只是不安全/不可能從字串轉換
代表。

`evennia.utils.utils` 中有一個名為 [safe_convert_to_types](evennia.utils.utils.safe_convert_to_types) 的助手。此函式以安全的方式自動轉換簡單資料型別：

```python
from evennia.utils.utils import safe_convert_to_types

def _process_callable(*args, **kwargs):
    """
    $process(expression, local, extra1=34, extra2=foo)

    """
    args, kwargs = safe_convert_to_type(
      (('py', str), {'extra1': int, 'extra2': str}),
      *args, **kwargs)

    # args/kwargs should be correct types now

```

換句話說，在可呼叫的 `$process(expression, local, extra1=.., extra2=...)` 中，第一個引數將由 'py' 轉換器處理（如下所述），第二個引數將透過常規 Python `str` 傳遞，kwargs 將分別由 `int` 和 `str` 處理。您可以提供自己的轉換器函式，只要它接受一個引數並傳回轉換後的結果即可。

```python
args, kwargs = safe_convert_to_type(
        (tuple_of_arg_converters, dict_of_kwarg_converters), *args, **kwargs)
```

特殊轉換器 `"py"` 將嘗試在以下工具的幫助下將字串引數轉換為 Python 結構（您可能會發現這些工具對於您自己的實驗很有用）：

- [ast.literal_eval](https://docs.python.org/3.8/library/ast.html#ast.literal_eval) 是內建的 Python 函式。它_僅_支援字串、位元組、數字、元組、列表、字典、集合、布林值和`None`。就是這樣 - 不允許進行算術或資料修改。這對於將輸入行中的單一值和列表/字典轉換為真實的 Python 物件很有用。
- [simleeval](https://pypi.org/project/simpleeval/) 是 Evennia 附帶的第三方工具。這允許評估簡單（因此安全）的表示式。人們可以使用 `+-/*` 對數字和字串進行操作，也可以進行簡單的比較，例如 `4 > 3` 等。它確實_不_接受更複雜的容器，例如列表/字典等，因此這和 `literal_eval` 是相互補充的。

```{warning}
使用 Python 的內建 ``eval()`` 或 ``exec()`` 函式作為轉換器可能很誘人，因為它們能夠將任何有效的 Python 原始碼轉換為 Python。 NEVER DO THIS 除非你真的、真的知道 ONLY 開發人員會修改進入可呼叫的字串。此解析器適用於不受信任的使用者（如果您受信任，您就已經可以存取 Python）。讓不受信任的使用者將字串傳遞給 ``eval``/``exec`` 會帶來 MAJOR 的安全風險。它允許呼叫者在您的伺服器上執行任意 Python 程式碼。這是惡意刪除硬碟的路徑。只是不要這樣做，晚上睡得更好。
```

(default-funcparser-callables)=
## 預設 funcparser 可呼叫物件

這些是一些可呼叫的範例，您可以匯入並新增解析器。它們被分為`evennia.utils.funcparser`的全域級字典。只需匯入字典並在建立 `FuncParser` 例項時合併/新增一個或多個字典即可使這些可呼叫專案可用。

(evenniautilsfuncparserfuncparser_callables)=
### `evennia.utils.funcparser.FUNCPARSER_CALLABLES`

這些是“基本”可呼叫項。

- `$eval(expression)` ([code](evennia.utils.funcparser.funcparser_callable_eval)) - 這使用 `literal_eval` 和 `simple_eval` （請參閱上一節）嘗試將字串表示式轉換為 python 物件。這處理 e.g。文字清單 `[1, 2, 3]` 和簡單表示式如 `"1 + 2"`。
- `$toint(number)` ([code](evennia.utils.funcparser.funcparser_callable_toint)) - 如果可能的話，始終將輸出轉換為整數。
- `$add/sub/mult/div(obj1, obj2)` ([程式碼](evennia.utils.funcparser.funcparser_callable_add)) -
這對元素進行加/減/乘和除。雖然可以使用 `$eval` 完成簡單的加法，但這也可以用於將兩個清單新增在一起，這是使用 `eval` 不可能實現的；例如`$add($eval([1,2,3]), $eval([4,5,6])) -> [1, 2, 3, 4, 5, 6]`。
- `$round(float, significant)` ([程式碼](evennia.utils.funcparser.funcparser_callable_round)) - 將輸入浮點數四捨五入為提供的有效位數。例如`$round(3.54343, 3) -> 3.543`。
- `$random([start, [end]])` ([code](evennia.utils.funcparser.funcparser_callable_random)) - 這與 Python `random()` 函式類似，但如果開始/結束都是隨機的，則會隨機化為整數值
整數。如果沒有引數，將傳回 0 到 1 之間的浮點數。
- `$randint([start, [end]])` ([code](evennia.utils.funcparser.funcparser_callable_randint)) - 與 `randint()` python 函式類似，並且始終傳回一個整數。
- `$choice(list)` ([code](evennia.utils.funcparser.funcparser_callable_choice)) - 輸入將自動以與 `$eval` 相同的方式進行解析，並且預計是一個可迭代的。將傳回該清單的隨機元素。
- `$pad(text[, width, align, fillchar])` ([程式碼](evennia.utils.funcparser.funcparser_callable_pad)) - 這將填入內容。 `$pad("Hello", 30, c, -)` 將產生一個以 30 寬區塊為中心的文字，周圍有 `-` 個字元。
- `$crop(text, width=78, suffix='[...]')` ([code](evennia.utils.funcparser.funcparser_callable_crop)) - 這將裁剪比寬度長的文字，預設以也適合寬度的 `[...]` 字尾結尾。如果未給出寬度，則將使用用戶端寬度或 `settings.DEFAULT_CLIENT_WIDTH`。
- `$space(num)` ([程式碼](evennia.utils.funcparser.funcparser_callable_space)) - 這將插入 `num` 空格。
- `$just(string, width=40, align=c, indent=2)` ([code](evennia.utils.funcparser.funcparser_callable_justify)) - 將文字調整為給定寬度，左/右/中心對齊，或「f」完整對齊（跨寬度展開文字）。
- `$ljust` - 左對齊的捷徑。接受 `$just` 的所有其他 kwarg。
- `$rjust` - 右對齊的捷徑。
- `$cjust` - 居中對齊的捷徑。
- `$clr(startcolor, text[, endcolor])` ([程式碼](evennia.utils.funcparser.funcparser_callable_clr)) - 彩色文字。顏色由一兩個字元給出，前面不帶 `|`。如果沒有給出結束顏色，字串將恢復為中性，因此 `$clr(r, Hello)` 相當於 `|rHello|n`。

(evenniautilsfuncparsersearching_callables)=
### `evennia.utils.funcparser.SEARCHING_CALLABLES`

這些是需要存取檢查才能搜尋物件的可呼叫物件。因此，它們需要在執行解析器時傳遞一些額外的保留 kwargs：
```python

parser.parse_to_any(string, caller=<object or account>, access="control", ...)

```
`caller` 是必需的，它是要執行訪問檢查的物件。 `access` kwarg 是
 [lock type](./Locks.md) 進行檢查，預設為`"control"`。

- `$search(query,type=account|script,return_list=False)` ([code](evennia.utils.funcparser.funcparser_callable_search)) - 這將尋找並嘗試透過鍵或別名來匹配物件。請使用 `type` kwarg 來搜尋 `account` 或 `script`。預設情況下，如果有多個符合項，則不會傳回任何內容；如果 `return_list` 是 `True`，則會傳回 0、1 或更多符合項的清單。
- `$obj(query)`、`$dbref(query)` - `$search` 的舊別名。
- `$objlist(query)` - `$search` 的舊別名，始終返回清單。


(evenniautilsfuncparseractor_stance_callables)=
### `evennia.utils.funcparser.ACTOR_STANCE_CALLABLES`

這些用於實現演員立場情感。預設情況下，[DefaultObject.msg_contents](evennia.objects.objects.DefaultObject.msg_contents) 方法使用它們。您可以在頁面上閱讀更多相關資訊
[更改每個接收者的訊息](../Concepts/Change-Message-Per-Receiver.md)。

在解析器方面，所有這些行內函數都需要將額外的 kwargs 傳遞到解析器中（預設由 `msg_contents` 完成）：

```python
parser.parse(string, caller=<obj>, receiver=<obj>, mapping={'key': <obj>, ...})
```

這裡 `caller` 是傳送訊息的人，`receiver` 是檢視訊息的人。 `mapping` 包含對可透過這些可呼叫物件存取的其他物件的參考。

- `$you([key])` ([程式碼](evennia.utils.funcparser.funcparser_callable_you)) -
如果沒有給出 `key`，則表示 `caller`，否則表示 `mapping` 中的物件
  將被使用。由於此郵件傳送給不同的收件人，`receiver` 將發生變化，這將
  替換為字串 `you`（如果您和接收者是同一實體）或替換為
  `you_obj.get_display_name(looker=receiver)`的結果。這允許單一字串以不同的方式回顯
  取決於誰看到它，並以同樣的方式引用其他人。
- `$You([key])` - 與 `$you` 相同，但始終大寫。
- `$conj(verb [,key])` ([程式碼](evennia.utils.funcparser.funcparser_callable_conjugate)) - 動詞變位
第二人在場到第三人在場之間取決於誰
  看到字串。例如`"$You() $conj(smiles)".`將顯示為「你微笑」。和“湯姆微笑”。取決於
  關於誰看到它。這利用了 [evennia.utils.verb_conjugation](evennia.utils.verb_conjugation) 中的工具
  這樣做，並且僅適用於英語動詞。
- `$pron(pronoun [,options] [,key])` ([程式碼](evennia.utils.funcparser.funcparser_callable_pronoun)) - 動態
在第一人稱/第二人稱到第三人稱之間對映代名詞（如他的、她自己的、你的、它的等）。
- `$pconj(verb, [,key])` ([程式碼](evennia.utils.funcparser.funcparser_callable_conjugate_for_pronouns)) - 綴合物
第二人稱和第三人稱之間的動詞，如 `$conj`，但用代名詞而不是名詞來表示複數
  性別化。例如，對於“男性”性別，`"$Pron(you) $pconj(smiles)"` 將向其他人顯示為“他微笑”，或者
  “他們微笑”代表“複數”性別。


(evenniaprototypesprotfuncs)=
### `evennia.prototypes.protfuncs`

這是由[原型系統](./Prototypes.md) 使用的，並允許在原型內新增引用。 funcparsing 將在生成之前發生。

原型可用的行內函數：

- 全部 `FUNCPARSER_CALLABLES` 和 `SEARCHING_CALLABLES`
- `$protkey(key)` - 傳回同一原型中另一個鍵的值。請注意，系統會嘗試將其轉換為「真實」值（例如將字串「3」轉換為整數 3），出於安全原因，並非所有嵌入值都​​可以透過這種方式轉換。但請注意，您可以使用 inlinefunc 進行巢狀呼叫，包括新增您自己的轉換器。

(example)=
### 例子

以下是包含預設可呼叫物件和兩個自訂可呼叫物件的範例。

```python
from evennia.utils import funcparser
from evennia.utils import gametime

def _dashline(*args, **kwargs):
    if args:
        return f"\n-------- {args[0]} --------"
    return ''

def _uptime(*args, **kwargs):
    return gametime.uptime()

callables = {
    "dashline": _dashline,
    "uptime": _uptime,
    **funcparser.FUNCPARSER_CALLABLES,
    **funcparser.ACTOR_STANCE_CALLABLES,
    **funcparser.SEARCHING_CALLABLES
}

parser = funcparser.FuncParser(callables)

string = "This is the current uptime:$dashline($toint($uptime()) seconds)"
result = parser.parse(string)

```

上面我們定義了兩個可呼叫物件 `_dashline` 和 `_uptime` 並將它們對應到名稱 `"dashline"` 和 `"uptime"`，
這就是我們可以在字串中稱為 `$header` 和 `$uptime` 的內容。我們還可以訪問
所有預設值（如 `$toint()`）。

上面的解析結果會是這樣的：

    This is the current uptime:
    ------- 343 seconds -------
