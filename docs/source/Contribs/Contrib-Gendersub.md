(gendersub)=
# 性別子

Griatch 2015 年的貢獻

這是一個簡單的性別感知角色類，允許使用者
在文字中插入自訂標記以表示性別意識
訊息傳遞。它依賴於修改後的 msg() 並且意味著
如何做這樣的事情的靈感和起點。

一個物件可以有以下性別：

- 男性（他/他的）
- 女性（她/她的）
- 中性（它/它的）
- 模稜兩可的（他們/他們/他們的/他們的）

(installation)=
## 安裝

匯入`SetGender`指令並將其新增到您的預設cmdset中
`mygame/commands/default_cmdset.py`：

```python
# mygame/commands/default_cmdsets.py

# ...

from evennia.contrib.game_systems.gendersub import SetGender   # <---

# ...

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(SetGender())   # <---
```

讓您的 `Character` 繼承自 `GenderCharacter`。

```python
# mygame/typeclasses/characters.py

# ...

from evennia.contrib.game_systems.gendersub import GenderCharacter  # <---

class Character(GenderCharacter):  # <---
    # ...
```

重新載入伺服器（從遊戲內部`evennia reload`或`reload`）。


(usage)=
## 用法

使用時，訊息可以包含特殊的 tags 來指示代名詞性別
基於正在處理的問題。大寫字母將保留。

- `|s`, `|S`: 主觀形式: he, she, it, He, She, It, They
- `|o`、`|O`：客觀形式：他、她、它、他、她、它、他們
- `|p`、`|P`：所有格形式：他的、她的、它的、他的、她的、它的、他們的
- `|a`、`|A`：絕對所有格形式：his、hers、its、His、Hers、Its、Theirs

例如，

```
char.msg("%s falls on |p face with a thud." % char.key)
"Tom falls on his face with a thud"
```

預設性別是「模糊的」（they/them/their/theirs）。

要使用，請讓 DefaultCharacter 繼承於此，或更改
設定.DEFAULT_CHARACTER 指向此類。

`gender`指令用於設定性別。需要將其新增到
在可用之前預設為 cmdset。



----

<small>此檔案頁面是從`evennia\contrib\game_systems\gendersub\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
