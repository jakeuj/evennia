(evennia-code-style)=
# Evennia 程式碼風格

提交或提交給 Evennia 專案的所有程式碼應旨在遵循
[Python PEP 8][pep8] 中概述的指南。保持程式碼風格統一
使人們更容易協作和閱讀程式碼。

檢查程式碼是否遵循 PEP8 的一個好方法是使用 [PEP8 工具][pep8tool]
關於你的訊息來源。

(main-code-style-specification)=
## 主要程式碼風格規範

 * 4 個空格縮排，NO TABS！
 * Unix 行結尾。
 * 100 個字元的行寬
 * CamelCase 僅用於類，無其他用途。
 * 所有非全域變數名稱和所有函式名稱應為
小寫，單字之間用底線分隔。變數名應該
   長度始終超過兩個字母。
 * 模組級全域變數（僅）應採用 CAPITAL 字母。
 * 匯入應按以下順序進行：
   - Python 模組（內建模組和標準函式庫）
   - 扭曲模組
   - Django 模組
   - Evennia 庫模組 (`evennia`)
   - Evennia contrib 模組 (`evennia.contrib`)
 * 所有模組、類別、函式和方法都應具有格式化的檔案字串
如下所述。
 * 所有預設指令都應具有一致的文件字串，格式為
概述如下。

(code-docstrings)=
## 程式碼檔案字串

所有模組、類別、函式和方法都應該有檔案字串
採用 [Google 風格][googlestyle] 啟發的縮排進行格式化，使用
[Markdown][githubmarkdown] 在需要時進行格式化。 Evennia的`api2md`
解析器將使用它來建立漂亮的 API 檔案。


(module-docstrings)=
### 模組檔案字串

模組都應以至少幾行文件字串開頭
他們的頂部描述了模組的內容和目的。

模組檔案字串範例（檔案頂部）：

```python
"""
This module handles the creation of `Objects` that
are useful in the game ...

"""
```

切片（`# title`、`## subtile` 等）不應用於
自由格式的檔案字串 - 這會混淆自動的分段
檔案頁面和 auto-api 將自動建立它。
僅將部分名稱以粗體形式寫在自己的行上以標記部分。
超出部分應根據需要使用 markdown 進行格式化
文字。

程式碼範例應使用[多行語法突出顯示][markdown-hilight]
使用“python”識別符號來標記多行程式碼區塊。只是
縮排程式碼區塊（常見於 Markdown）不會產生
想要的外觀。

當使用任何程式碼tags（內聯或區塊）時，建議您
不要讓程式碼延伸超過大約 70 個字元，否則它會
需要在 wiki 中水平滾動（這不會影響任何
其他文字，僅程式碼）。

(class-docstrings)=
### 類別文件字串

根類文件字串應該描述
類。它通常不應描述確切的呼叫順序或列表
重要的方法，這往往很難保持更新，因為API
發展。不要使用節標記（`#`、`##` 等）。

類別文件字串範例：

```python
class MyClass(object):
    """
    This class describes the creation of `Objects`. It is useful
    in many situations, such as ...

    """
```

(function-method-docstrings)=
### 函式/方法檔案字串

函式或方法檔案字串範例：

```python

def funcname(a, b, c, d=False, **kwargs):
    """
    This is a brief introduction to the function/class/method

    Args:
        a (str): This is a string argument that we can talk about
            over multiple lines.
        b (int or str): Another argument.
        c (list): A list argument.
        d (bool, optional): An optional keyword argument.

    Keyword Args:
        test (list): A test keyword.

    Returns:
        str: The result of the function.

    Raises:
        RuntimeException: If there is a critical error,
            this is raised.
        IOError: This is only raised if there is a
            problem with the database.

    Notes:
        This is an example function. If `d=True`, something
        amazing will happen.

    """
```

語法非常“寬鬆”，但縮排很重要。也就是說，你
應該以換行符號結束區塊頭（如 `Args:`），後面接著
一個縮排。當你需要換行時，你應該開始下一行
與另一個縮排。為了與程式碼保持一致，我們建議所有
縮排為 4 個空格寬（沒有製表符！）。

以下是所有支援的塊頭：

```
    """
    Args
        argname (freeform type): Description endind with period.
    Keyword Args:
        argname (freeform type): Description.
    Returns/Yields:
        type: Description.
    Raises:
        Exceptiontype: Description.
    Notes/Note/Examples/Example:
        Freeform text.
    """
```

標有“自由形式”的零件意味著原則上您可以放置任何
使用除節標記之外的任何格式的文字（`#`、`##`
等）。您還必須保留縮排以標記您屬於哪個區塊
的。您通常應該使用指定的格式而不是
自由形式對應（這將產生更好的輸出），但在某些情況下
在這種情況下，自由格式可能會產生更緊湊和可讀的結果
（例如一般描述 `*args` 或 `**kwargs` 語句時
條款）。類別方法的第一個 `self` 引數永遠不應該是
記錄在案。

注意

```
"""
Args:
    argname (type, optional): Description.
"""
```

和

```
"""
Keyword Args:
   sargname (type): Description.
"""
```

意思是一樣的！使用哪一種取決於功能或
方法已記錄，但沒有硬性規則；如果有一個大
`**kwargs` 區塊在函式中，使用 `Keyword Args:` 區塊可能是
好主意，但對於少量引數，只需使用 `Args:`
將關鍵字標記為 `optional` 將縮短檔案字串並使
更容易閱讀。

(default-command-docstrings)=
## 預設指令檔案字串

這些代表一種特殊情況，因為 Evennia 中的指令使用它們的類
檔案字串代表該指令的遊戲內幫助條目。

_預設指令_集中的所有指令都應該有其檔案字串
以類似的形式格式化。對於contribs，這個就放寬了，但是如果有
沒有特別的理由使用不同的形式，應該以相同的形式為目標
contrib-指令檔案字串的樣式。

```python
      """
      Short header

      Usage:
        key[/switches, if any] <mandatory args> [optional] choice1||choice2||choice3

      Switches:
        switch1    - description
        switch2    - description

      Examples:
        Usage example and output

      Longer documentation detailing the command.

      """
```

- 在所有預設指令中，兩個空格用於*縮排*。
- 方括號 `[ ]` 包圍*可選、可跳過的引數*。
- 尖括號 `< >` 包圍著要寫的內容的_描述_而不是確切的語法。
- 明確選擇由 `|` 分隔。為了避免被解析為顏色程式碼，請使用 `||` （這
將顯示為單一 `|`），或如果有足夠的空間，則在角色周圍放置空格（“` | `”）。
- `Switches` 和 `Examples` 區塊是可選的並且基於指令。

以下以 `nick` 指令為例：

```python
      """
      Define a personal alias/nick

      Usage:
        nick[/switches] <nickname> = [<string>]
        alias             ''

      Switches:
        object   - alias an object
        account   - alias an account
        clearall - clear all your aliases
        list     - show all defined aliases (also "nicks" works)

      Examples:
        nick hi = say Hello, I'm Sarah!
        nick/object tom = the tall man

      A 'nick' is a personal shortcut you create for your own use [...]

        """
```

對於*需要引數*的指令，策略是回傳 `Usage:`
如果輸入指令時不帶任何引數，則為字串。所以對於這樣的指令，
指令正文應包含以下內容

```python
      if not self.args:
          self.caller.msg("Usage: nick[/switches] <nickname> = [<string>]")
          return
```

(tools-for-auto-linting)=
## 自動 linting 工具

(black)=
### 黑色的

可以使用以下指令執行自動符合 pep8 的格式化和 linting
`black` 格式化程式：

    black --line-length 100

(pycharm)=
### PyCharm

Python IDE [Pycharm][pycharm] 可以自動產生空文件字串存根。的
但預設使用 `reStructuredText` 形式。改為Evennia的
Google 風格的檔案字串，請遵循[本指南][pycharm-guide]。



[pep8]: http://www.python.org/dev/peps/pep-0008
[pep8tool]: https://pypi.python.org/pypi/pep8
[googlestyle]: https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html
[githubmarkdown]: https://help.github.com/articles/github-flavored-markdown/
[markdown-hilight]: https://help.github.com/articles/github-flavored-markdown/#syntax-highlighting
[command-docstrings]: https://github.com/evennia/evennia/wiki/Using%20MUX%20As%20a%20Standard#documentation-policy
[pycharm]: https://www.jetbrains.com/pycharm/
[pycharm-guide]: https://www.jetbrains.com/help/pycharm/2016.3/python-integrated-tools.html
