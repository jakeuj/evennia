(default-command-syntax)=
# 預設指令語法


Evennia 允許任何指令語法。

如果您喜歡 DikuMUDs、LPMuds 或 MOOs 處理事情的方式，您可以使用 Evennia 來模擬。如果您雄心勃勃，您甚至可以設計一種全新的風格，完美契合您自己的理想遊戲夢想。請參閱[指令](../Components/Commands.md) 檔案以瞭解如何執行此操作。

不過，我們確實提供了預設設定。預設 Evennia 設定往往*類似* [MUX2](https://www.tinymux.org/) 及其表兄弟 [PennMUSH](https://www.pennmush.org)、[TinyMUSH](https://github.com/TinyMUSH/TinyMUSH/wiki) 和 [RhostMUSH](http://www.rhostmush.com/)：

```
command[/switches] object [= options]
```

雖然這種相似性的原因部分是歷史原因，但這些程式碼庫為管理和建置提供了非常成熟的功能集。

不過，Evennia *不是* MUX 系統。它的工作原理在很多方面都非常不同。例如Evennia
故意缺少線上軟程式碼語言（我們的[軟程式碼政策頁面](./Soft-Code.md) 上解釋的政策）。 Evennia 在認為適當的時候也不迴避使用自己的文法：
MUX 語法經過很長一段時間的有機發展，坦白說，有些地方相當神秘。  全部投入
所有預設的指令語法最多應該被稱為「MUX-like」或「MUX-inspired」。

```{toctree}
:hidden:
Soft-Code
```