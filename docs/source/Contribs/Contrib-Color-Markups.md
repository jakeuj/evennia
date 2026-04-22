(additional-color-markups)=
# 附加顏色標記

Contrib，作者：格里奇，2017

Evennia 的附加顏色標記樣式（擴充或取代預設值
`|r`、`|234`）。新增對 MUSH 樣式（`%cr`、`%c123`）和/或舊版Evennia 的支援
（`{r`，`{123`）。


(installation)=
## 安裝

將所需的樣式變數從此模組匯入到
mygame/server/conf/settings.py 並將它們新增到下面的設定變數中。
每個都被指定為一個列表，並且可以將多個這樣的列表新增到每個列表中
變數以支援多種格式。請注意，列表順序會影響哪些正規表示式
首先應用。您必須重新啟動 Portal 和顏色 tags 的伺服器才能
更新。

分配給以下設定變數（請參閱下面的範例）：

    COLOR_ANSI_EXTRA_MAP - a mapping between regexes and ANSI colors
    COLOR_XTERM256_EXTRA_FG - regex for defining XTERM256 foreground colors
    COLOR_XTERM256_EXTRA_BG - regex for defining XTERM256 background colors
    COLOR_XTERM256_EXTRA_GFG - regex for defining XTERM256 grayscale foreground colors
    COLOR_XTERM256_EXTRA_GBG - regex for defining XTERM256 grayscale background colors
    COLOR_ANSI_BRIGHT_BG_EXTRA_MAP = ANSI does not support bright backgrounds; we fake
    this by mapping ANSI markup to matching bright XTERM256 backgrounds

    COLOR_NO_DEFAULT - Set True/False. If False (default), extend the default
    markup, otherwise replace it completely.

(example)=
## 例子

若要新增 {- "curly-bracket" 樣式，請將以下內容新增至您的設定檔中，
然後重新啟動伺服器和Portal：

```python
from evennia.contrib.base_systems import color_markups
COLOR_ANSI_EXTRA_MAP = color_markups.CURLY_COLOR_ANSI_EXTRA_MAP
COLOR_XTERM256_EXTRA_FG = color_markups.CURLY_COLOR_XTERM256_EXTRA_FG
COLOR_XTERM256_EXTRA_BG = color_markups.CURLY_COLOR_XTERM256_EXTRA_BG
COLOR_XTERM256_EXTRA_GFG = color_markups.CURLY_COLOR_XTERM256_EXTRA_GFG
COLOR_XTERM256_EXTRA_GBG = color_markups.CURLY_COLOR_XTERM256_EXTRA_GBG
COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP = color_markups.CURLY_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP
```

若要新增`%c-`「mux/mush」樣式，請將以下內容新增至您的設定檔中，然後
重新啟動伺服器和Portal：

```python
from evennia.contrib.base_systems import color_markups
COLOR_ANSI_EXTRA_MAP = color_markups.MUX_COLOR_ANSI_EXTRA_MAP
COLOR_XTERM256_EXTRA_FG = color_markups.MUX_COLOR_XTERM256_EXTRA_FG
COLOR_XTERM256_EXTRA_BG = color_markups.MUX_COLOR_XTERM256_EXTRA_BG
COLOR_XTERM256_EXTRA_GFG = color_markups.MUX_COLOR_XTERM256_EXTRA_GFG
COLOR_XTERM256_EXTRA_GBG = color_markups.MUX_COLOR_XTERM256_EXTRA_GBG
COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP = color_markups.MUX_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP
```


----

<small>此檔案頁面是從`evennia\contrib\base_systems\color_markups\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
