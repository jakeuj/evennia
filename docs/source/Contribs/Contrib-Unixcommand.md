(unix-like-command-style)=
# 類似 Unix 的指令風格

Vincent Le Geoff (vlgeoff) 的貢獻，2017 年

該模組包含一個指令類，帶有一個替代語法解析器，實現
遊戲中的 Unix 風格指令語法。這意味著`--options`，位置引數
以及像 `-n 10` 這樣的東西。對普通玩家來說這可能不是最好的語法
但當建構者需要使用單一指令執行操作時，這對他們來說非常有用
很多事情有很多選擇。它使用Python標準中的`ArgumentParser`
引擎蓋下的圖書館。

(installation)=
## 安裝

要使用，請從您自己的指令繼承此模組的`UnixCommand`。你需要
重寫兩個方法：

- `init_parser` 方法，為解析器新增選項。請注意，您
繼承自時通常*不*覆蓋正常的 `parse` 方法
  `UnixCommand`。
- `func` 方法，被呼叫以執行解析後的指令（與任何指令一樣）。

這是一個簡短的例子：

```python
from evennia.contrib.base_systems.unixcommand import UnixCommand


class CmdPlant(UnixCommand):

    '''
    Plant a tree or plant.

    This command is used to plant something in the room you are in.

    Examples:
      plant orange -a 8
      plant strawberry --hidden
      plant potato --hidden --age 5

    '''

    key = "plant"

    def init_parser(self):
        "Add the arguments to the parser."
        # 'self.parser' inherits `argparse.ArgumentParser`
        self.parser.add_argument("key",
                help="the key of the plant to be planted here")
        self.parser.add_argument("-a", "--age", type=int,
                default=1, help="the age of the plant to be planted")
        self.parser.add_argument("--hidden", action="store_true",
                help="should the newly-planted plant be hidden to players?")

    def func(self):
        "func is called only if the parser succeeded."
        # 'self.opts' contains the parsed options
        key = self.opts.key
        age = self.opts.age
        hidden = self.opts.hidden
        self.msg("Going to plant '{}', age={}, hidden={}.".format(
                key, age, hidden))
```

要了解 argparse 的全部功能以及支援的選項型別，請訪問
[argparse 的文件](https://docs.python.org/2/library/argparse.html)。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\unixcommand\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
