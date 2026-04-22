# 貢獻 Evennia 文件

```{sidebar} 想在本機建置文件嗎？
你_不需要_能在本機測試或建置文件，才能送出文件 PR。我們會在合併與建置文件時處理相關問題。如果你真的想自己在本機建置，說明在[本文最後](#building-the-docs-locally)。
```
- 你可以透過建立 [Documentation issue](github:issue) 來貢獻文件。
- 你也可以像處理一般程式碼那樣，透過 [PR](./Contributing.md) 來貢獻文件。來源檔位於 `evennia/docs/source/`。

文件原始檔是 `*.md`（Markdown）檔案。Markdown 是一般文字檔，可以用任何普通文字編輯器修改。它們也可以包含 raw HTML directives（但這種情況很少需要）。Evennia 文件使用的是 [Markdown][commonmark] 語法，並搭配 [MyST extensions][MyST]。

## 原始檔結構

這些原始檔大致分成幾個類別，而 `evennia/docs/source/` 根目錄本身只放少數管理性質的文件。

- `source/Components/` 介紹的是 Evennia 各個獨立的 building blocks，也就是那些你可以匯入並直接使用的東西。這些內容會補充並延伸 API docs 本身能提供的資訊，例如 `Accounts`、`Objects` 與 `Commands` 的文件。
- `source/Concepts/` 說明的是 Evennia 較大尺度的功能如何彼此協作，也就是那些無法輕易拆解成單一 isolated component 的主題。這裡可能會談到 Models 與 Typeclasses 如何互動，也可能會說明一則訊息如何從 client 進到 server，再傳回 client。
- `source/Setup/` 收錄的是安裝、執行與維護 Evennia 伺服器，以及相關基礎設施的詳細文件。
- `source/Coding/` 提供如何操作、使用與理解 Evennia 程式碼庫本身的說明。這裡也包含一些不只限於 Evennia 的一般開發概念，以及如何建立健康開發環境的建議。
- `source/Contribs/` 專門放 `evennia/contribs/` 資料夾內各套件的文件。任何 contrib 專屬教學通常都會放在這裡，而不是放到 `Howtos`。
- `source/Howtos/` 收錄的是如何在 Evennia 中達成某個具體目標、效果或結果的文件。它們通常會比較像教學或 FAQ，也會引導讀者再去看其他文件做延伸閱讀。
- `source/Howtos/Beginner-Tutorial/` 收錄的是新手教學流程中的所有文件。

其他檔案與資料夾：
- `source/api/` 包含自動生成的 API 文件來源頁；建置後會輸出為 `.html`。不要手動編輯這些檔案，因為它們是由原始來源自動生成的。
- `source/_templates` 與 `source/_static` 存放的是文件系統本身要用的檔案。除非你想調整文件生成的外觀或結構，否則通常不需要修改。
- `conf.py` 保存 Sphinx 設定。通常除非是新 branch 要更新 Evennia 版本，否則不建議修改。

## 自動生成的文件頁

有些文件頁面是自動生成的。直接修改它們的生成後 Markdown 檔，最後都會被覆蓋。正確做法是去修改自動化流程實際讀取的來源。

- `source/api` 下面的所有 API docs 都是由 Evennia core code 的 doc strings 建出來的。若要修正這些文件，應該去修改對應 module、function、class 或 method 的 docstring。
- [Contribs/Contribs-Overview.md](Contribs/Contribs-Overview.md) 在建置文件時，會由 `evennia/docs/pylib/contrib_readmes2docs.py` 腳本完全從零生成。
    - 上述頁面中的所有 contrib 簡介，都是取自 `evennia/contrib/*/*/README.md` 中每個 contrib `README.md` 的第一段。
    - 同樣地，從該頁面連出去的所有 contrib 文件，也都是由各 contrib 的 `README.md` 自動生成。
- [Components/Default-Commands.md](Components/Default-Commands.md) 是從 `evennia/commands/default/` 底下的 command classes 生成的。
- [Coding/Evennia-Code-Style.md](Coding/Evennia-Code-Style.md) 是從 `evennia/CODING_STYLE.md` 生成的。
- [Coding/Changelog.md](Coding/Changelog.md) 是從 `evennia/CHANGELOG.md` 生成的。
- [Setup/Settings-Default.md](Setup/Settings-Default.md) 是從預設設定檔 `evennia/default_settings.py` 生成的。

大多數自動生成頁面都會在頁首放一個警告，提醒你這是 auto-generated 內容。

## 編輯語法

Evennia 文件採用 [Markdown][commonmark-help]（CommonMark）格式。雖然 Markdown 對某些元素支援不只一種寫法，但為了保持一致性，我們盡量統一使用下面這些形式。

### Italic/Bold（斜體/粗體）

我們通常使用底線表示斜體，用雙星號表示粗體：

- `_Italic text_` - _Italic text_
- `**Bold Text**` - **Bold text**

### Headings（標題）

我們使用 `#` 來表示章節/標題。`#` 越多，代表層級越深（字也會越小）。

- `# Heading`
- `## SubHeading`
- `### SubSubHeading`
- `#### SubSubSubHeading`

> 同一個頁面裡不要重複使用完全相同的 heading/subheading 名稱。雖然 Markdown 本身不會阻止你，但那會讓該 heading 無法被唯一引用。Evennia 的文件前處理器會偵測到這種情況並報錯。

### Lists（列表）

你可以建立 bullet-point list，也可以建立 numbered list：

```
- first bulletpoint
- second bulletpoint
- third bulletpoint
```

- first bulletpoint
- second bulletpoint
- third bulletpoint

```
1. Numbered point one
2. Numbered point two
3. Numbered point three
```

1. Numbered point one
2. Numbered point two
3. Numbered point three

### Blockquotes（引用區塊）

Blockquote 會建立一個縮排區塊，適合用來做強調。做法是在一行或多行開頭加上 `>`。如果你想做正式的「註記」，也可以改用明確的 [Note](#note)。

```
> This is an important
> thing to remember.
```

> Note: This is an important
> thing to remember.

(links)=
### Links（連結）

連結語法是 `[linktext](url_or_ref)`，這會產生一個可點擊的連結 [linktext](#links)。

#### Internal links（內部連結）

大多數連結都會指向其他文件頁面，或指向 Evennia 的 API docs。每個文件 heading 都可以被引用。引用永遠從 `#` 開始；heading 名稱會自動轉成小寫，並忽略非字母字元。標題中的空白會被替換成單一的 `-`。

例如，假設 `Menu-stuff.md` 這個檔案內容如下：

```
# Menu items

Some text...

## A yes/no? example

Some more text...
```

- 若是在_同一個檔案內部_，你可以這樣引用各個 heading：

      [menus](#menu-items)
      [example](#a-yesno-example)

- 若是從_另一個檔案_引用，則可以這樣寫：

      [menus](Menu-Stuff.md#menu-items)
      [example](Menu-Stuff.md#a-yesno-example)

> 引用時不寫 `.md` 副檔名也沒關係。Evennia 的文件前處理器會自動幫你修正，也會在需要時補上正確的相對路徑。

(api-links)=
#### API links（API 連結）

文件系統包含 Evennia 全部原始碼的自動生成文件。你只要給出該資源的 Python path，並以 `evennia.` 開頭，就可以直接把讀者導向對應來源：

      [DefaultObject](evennia.objects.objects.DefaultObject) <- like this!

[DefaultObject](evennia.objects.objects.DefaultObject)  <- like this!

> 請注意，你不能用這種方式引用 `mygame` 資料夾裡的檔案。遊戲目錄是動態生成的，不屬於 API docs 的一部分。最接近的是 `evennia.game_template`，也就是 `evennia --init` 建立 game dir 時會複製的範本。

#### External links（外部連結）

這類連結會指向文件之外的資源。我們也提供了一些方便的 shortcut：

```
[evennia.com](https://evennia.com) - link to an external website.
```

- 你可以把 `(github:evennia/objects/objects.py)` 當成 link target，直接指向 Evennia GitHub 頁面（main branch）上的某個位置。
- 使用 `(github:issue)` 則可以直接指向 GitHub issue 建立頁。

 > 如果你想引用程式碼，通常最好是[連到 API](#api-links)，而不是直接指向 GitHub。

### 將 URLs/References 集中寫在一處

URL 可能會很長，如果你在很多地方都用到同一個 url/reference，正文看起來就會有點凌亂。這時你可以把 url 寫成文件尾端的「footnote」，正文只透過方括號 `[ ]` 去引用它。範例如下：

```
This is a [clickable link][mylink]. This is [another link][1].

...


[mylink]: http://...
[1]: My-Document.md#this-is-a-long-ref

```

這樣正文就會簡潔一些。

### Tables（表格）

表格可以這樣寫：

````
| heading1 | heading2 | heading3 |
| --- | --- | --- |
| value1 | value2 | value3 |
|  | value 4 | |
| value 5 | value 6 | |
````

| heading1 | heading2 | heading3 |
| --- | --- | --- |
| value1 | value2 | value3 |
|  | value 4 | |
| value 5 | value 6 | |

如你所見，Markdown 的表格語法其實可以很寬鬆（欄位不一定要排得整整齊齊），只要你有加上標題分隔線，並確保每一行都有正確數量的 `|` 即可。


### Verbatim text（原樣文字）

你常常會想把某些內容標記成原樣顯示，也就是完全照寫出來、不經 Markdown 解析。在行內文字中，這是透過 backticks（\`）完成的，例如 \`verbatim text\` 會變成 `verbatim text`。

如果你想把 verbatim 內容單獨放成一個區塊，也可以直接在前面縮排 4 個空白（兩側加上空行可提升可讀性）：

```
This is normal text

    This is verbatim text

This is normal text
```

另一種方式是使用 triple-backticks：

````
```
Everything within these backticks will be verbatim.

```
````

### Code blocks（程式碼區塊）

程式碼範例可以視為一種特殊的「verbatim」內容，但通常我們希望它同時帶有語法上色以便閱讀。做法是在 triple-backticks 後面標明語言：

````
```python
from evennia import Command
class CmdEcho(Command):
    """
    Usage: echo <arg>
    """
    key = "echo"
    def func(self):
        self.caller.msg(self.args.strip())
```
````

```python
from evennia import Command
class CmdEcho(Command):
  """
  Usage: echo <arg>
  """
  key = "echo"
  def func(self):
    self.caller.msg(self.args.strip())
```

如果是示範 Python command-line，請使用 `python` 語言型別與 `>>>` prompt。
````
```python
>>> print("Hello World")
Hello World
```
````

```python
>>> print("Hello World")
Hello World
```

如果是示範遊戲內指令，請使用 `shell` 語言型別，並以 `>` 當作 prompt。遊戲回傳內容請縮排。

````
```shell
> look at flower
  Red Flower(#34)
  A flower with red petals.
```
````

```shell
> look at flower
  Red Flower(#34)
  A flower with red petals.
```


如果是實際 shell prompt，你可以使用 `bash` 語言型別，或單純把該行縮排。若你想清楚區分輸入與輸出，可使用 `$` 當 prompt；否則也可以省略，因為對不熟命令列的使用者來說，過多 prompt 有時反而會造成混淆。

````
```bash
$ ls
evennia/ mygame/
```
    evennia start --log
````

```bash
$ ls
evennia/ mygame/
```

    evennia start --log


### MyST directives

Markdown 易讀又好用，但雖然它已經能處理大部分需求，還是有些地方表達力不太夠。因此我們會搭配擴充的 [MyST][MyST] 語法，基本形式如下：

````
```{directive} any_options_here

content

```
````


(note)=
#### Note（註記）

這種 note 會比單純寫 `> Note: ...` 更醒目。

````
```{note}

This is some noteworthy content that stretches over more than one line to show how the content indents.
Also the important/warning notes indents like this.

```
````

```{note}

This is some noteworthy content that stretches over more than one line to show how the content indents.
Also the important/warning notes indents like this.

```

#### Important（重要）

這適合用在特別重要、需要高度可見性的說明。

````
```{important}
  This is important because it is!
```

````
```{important}
  This is important because it is!
```

#### Warning（警告）

Warning block 用來提醒特別危險的事情，或那些很容易出錯的功能。

````
```{warning}
  Be careful about this ...
```
````

```{warning}
  Be careful about this ...
```

#### Version changes and deprecations（版本變更與棄用）

這些 directive 會顯示成單行提示，用來說明某個功能自特定版本起被新增、修改或棄用。

````
```{versionadded} 1.0
```
````

```{versionadded} 1.0
```

````
```{versionchanged} 1.0
  How the feature changed with this version.
```
````

```{versionchanged} 1.0
  How the feature changed with this version.
```

````
```{deprecated} 1.0
```
````

```{deprecated} 1.0
```

#### Sidebar

這會顯示一個浮在正文旁邊的資訊 sidebar。它很適合用來提醒讀者某些與本文相關的重要概念。

````
```{sidebar} Things to remember

- There can be bullet lists
- in here.

Separate sections with

an empty line.
```
````

```{sidebar} Things to remember

- There can be bullet lists
- in here.

Separate sections with

an empty line.
```

提示：如果你想確保下一個標題出現在獨立的一行，而不是被擠在 sidebar 左邊，可以在 Markdown 中直接嵌入這樣一段純 HTML：

```html
<div style="clear: right;"></div>
```

<div style="clear: right;"></div>

#### 更有彈性的程式碼區塊

一般的 Markdown Python code block 通常就夠用了，但如果你想更直接地控制樣式，也可以改用帶有額外 `:options:` 的 `{code-block}` directive：

````
```{code-block} python
:linenos:
:emphasize-lines: 1-2,8
:caption: An example code block
:name: A full code block example

from evennia import Command
class CmdEcho(Command):
    """
    Usage: echo <arg>
    """
    key = "echo"
    def func(self):
        self.caller.msg(self.args.strip())
```
````

```{code-block} python
:linenos:
:emphasize-lines: 1-2,8
:caption: An example code block
:name: A full code block example

from evennia import Command
class CmdEcho(Command):
    """
    Usage: echo <arg>
    """
    key = "echo"
    def func(self):
        self.caller.msg(self.args.strip())
```
其中，`:linenos:` 會打開行號，`:emphasize-lines:` 則能讓特定行用不同顏色強調。`:caption:` 會顯示說明文字，而 `:name:` 會成為這個區塊可被引用的名稱（因此在同一份文件裡應該保持唯一）。



#### eval-rst directive

如果真的有必要，最後也可以退回直接撰寫 [ReST][ReST] directives：


````
```{eval-rst}

    This will be evaluated as ReST.
    All content must be indented.

```
````

在 ReST block 裡，必須使用 Restructured Text 語法，它和 Markdown 並不相同。

- 文字外圍用單一 backticks 會變成 _italic_。
- 文字外圍用雙 backticks 會變成 `verbatim`。
- 連結則是寫在 backticks 裡，並在結尾加上一個底線：

      `python <www.python.org>`_

[這裡有一份 ReST 格式速查表](https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html)。

## 為 autodocs 撰寫程式碼 docstrings

原始碼中的 docstring 會被當成 Markdown 解析。撰寫 module docstring 時，你可以使用 Markdown 格式，包含最深到第 4 層的標題（`#### SubSubSubHeader`）。

在 module 文件結尾加上四個連字號 `----` 通常是個好習慣。這會在說明文件與後續 class/function docs 之間畫出一條清楚的分隔線。可參考 [Traits docs](evennia.contrib.rpg.traits)。

所有非 private 的 classes、methods 與 functions 都必須有 Google-style docstring，做法請依照 [Evennia coding style guidelines][github:evennia/CODING_STYLE.md]。這樣它們才能被正確格式化成整齊的 API docs。

(building-the-docs-locally)=
## 在本機建置文件

Evennia 使用 [Sphinx][sphinx] 搭配 [MyST][MyST] extension，因此我們可以用輕量的 Markdown（更精確地說是像 GitHub 那樣的 [CommonMark][commonmark]）來寫文件，而不必直接使用 Sphinx 原生的 ReST 語法。`MyST` parser 也額外提供了一些語法，讓我們能表達比純 Markdown 更複雜的版面。

至於 [autodoc-generation][sphinx-autodoc]，我們使用 sphinx-[napoleon][sphinx-napoleon] extension，讓系統能正確理解 classes、functions 等位置使用的 Google-style docstrings。

`evennia/docs/source/` 裡的原始檔會透過 Sphinx 靜態文件生成系統，加上 Evennia 自訂的 _pre-parsers_（repo 內也有附），一起建成最終文件。

如果你要在本機做這件事，需要使用支援 `make` 的環境（Linux/Unix/Mac 或 [Windows-WSL][Windows-WSL]）。理論上你也可以手動跑 sphinx build commands；如果想知道本文提到的 `make` 命令實際做了什麼，可以直接去看 `evennia/docs/Makefile`。

```{important}
如前面提過的，你不_一定_要在本機建置文件才能貢獻。Markdown 沒那麼難，不看建置結果通常也能寫得很像樣；我們在合併前也能再幫忙潤飾。

另外，你也可以用像 [Grip][grip] 這樣的 Markdown viewer 先大致確認外觀。像 [ReText][retext] 這類編輯器，或 [PyCharm][pycharm] 這類 IDE，也都內建 Markdown 預覽。

不過，若你想百分之百確認結果和自己預期一致，本機建置依然是唯一辦法。處理器也會順便幫你抓出一些錯誤，例如連結打錯字。

```
### 只建置主要文件

這是最快看到修改結果的方式。它只會建置主要文件頁，不會包含 API auto-docs 或版本文件。整個流程都在 terminal/console 中完成。

- （可選，但建議）啟用一個使用 Python 3.11 的 virtualenv。
- `cd` 進到 `evennia/docs` 資料夾。
- 安裝文件建置所需套件：

    ```
    make install
    or
    pip install -r requirements.txt
    ```

- 接著建置 HTML 文件（未來每次修改後也都是重新執行這一步）：

    ```
    make quick
    ```
    
- 留意你編輯過的檔案是否有報錯。
- HTML 文件會出現在新的 `evennia/docs/build/html/` 資料夾中。
- 用瀏覽器開啟 `file://<path-to-folder>/evennia/docs/build/html/index.html` 來查看文件。注意：如果你點到 auto-docs 的連結，會出錯，因為這一步沒有建它們。

### 建置主要文件與 API docs

完整文件包含一般文件頁，以及從 Evennia 原始碼生成的 API 文件。若要建這一套，你必須先安裝 Evennia，並初始化一個使用預設資料庫的新遊戲（不需要真的把 server 跑起來）。

- 建議使用 virtualenv。將你 clone 下來的 Evennia 安裝進去，安裝目標要指向 repo 根目錄（也就是包含 `/docs` 的那層）：

    ```
    pip install -e evennia
    ```

- 確認你目前位於_包含_ `evennia/` repo 的上層目錄（也就是比 `evennia/docs/` 再往上兩層）。
- 在和 `evennia` repo 同一層的位置，建立一個名稱必須正好叫做 `gamedir` 的新遊戲目錄：

    ```
    evennia --init gamedir
    ```

- 接著 `cd` 進去，建立一個新的空資料庫。你不需要真的啟動遊戲，也不需要做其他修改。

    ```
    evennia migrate
    ```

- 到這一步時，目錄結構應該長這樣：

    ```
      (top)
      |
      ----- evennia/  (the top-level folder, containing docs/)
      |
      ----- gamedir/
    ```

（如果你本來就已經在開發某個遊戲，當然也可以同時把你的「真正」遊戲目錄放在那裡；這個流程不會去動它。）

- 回到 `evennia/docs/`，安裝文件建置需求（這一步通常只要做一次）：

    ```
    make install
    or
    pip install -r requirements.txt
    ```

- 最後，建置完整文件，包含 auto-docs：

    ```
    make local
    ```

- 生成後的檔案會出現在 `evennia/docs/build/html/` 新資料夾中。留意你編輯過的檔案是否有任何錯誤。
- 在瀏覽器中開啟 `file://<path-to-folder>/evennia/docs/build/html/index.html`，即可查看完整文件。

#### 使用其他 gamedir 建置

如果你因為某些原因想使用另一個位置的 `gamedir/`，或想改用別的名稱（例如你本來就把自己開發用的目錄叫做 `gamedir`），也可以透過把 `EVGAMEDIR` 環境變數設成替代 game dir 的絕對路徑來達成。例如：

```
EVGAMEDIR=/my/path/to/mygamedir make local
```

### 建置 multiversion docs

完整版 Evennia 文件包含許多新舊版本的內容。這是透過抓取 Evennia 舊 release branches 的文件，然後全部一起建置來完成的，讓讀者可以自行選擇要看哪一版。只有特定的官方 Evennia branches 會被納入，因此你不能拿它來建自己的測試 branch。

- 所有本機變更都必須先 commit 到 git，因為版本文件的建置是直接根據 git tree 進行的。
- 如果你只是想在本機檢查，請執行（`mv` 代表 "multi-version"）：

    ```
    make mv-local
    ```

這是在本機上最接近「正式版」文件的建置方式。不同版本會出現在 `evennia/docs/build/versions/` 底下。部署時，`latest` symlink 會指向最新版本的文件。

[sphinx]: https://www.sphinx-doc.org/en/master/
[MyST]: https://myst-parser.readthedocs.io/en/latest/syntax/reference.html
[commonmark]: https://spec.commonmark.org/current/
[commonmark-help]: https://commonmark.org/help/
[sphinx-autodoc]: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc
[sphinx-napoleon]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
[getting-started]: Setup/Installation
[contributing]: ./Contributing
[ReST]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
[ReST-tables]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#tables
[ReST-directives]: https://www.sphinx-doc.org/en/master/usage/restruturedtext/directives.html
[Windows-WSL]: https://docs.microsoft.com/en-us/windows/wsl/install-win10
[linkdemo]: #links
[retext]: https://github.com/retext-project/retext
[grip]: https://github.com/joeyespo/grip
[pycharm]: https://www.jetbrains.com/pycharm/
