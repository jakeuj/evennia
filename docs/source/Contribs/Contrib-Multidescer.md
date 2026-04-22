(evennia-multidescer)=
# Evennia 多重解析器

Gratch 2016 的貢獻

「multidescer」是來自 MUSH 世界的概念。它允許
將您的描述分成任意命名的“部分”，您可以
然後隨意交換。這是一種快速管理您的外觀的方法（例如當
更自由的角色扮演系統中的換衣服）。這也將
與 `rpsystem` contrib 配合良好。

這個 multidescer 不需要對 Character 類別進行任何更改，而是需要
將使用 `multidescs` Attribute （清單），如果不存在則建立它。
它新增了一個新的 `+desc` 指令（其中 + 在 Evennia 中是可選的）。

(installation)=
## 安裝

與任何自訂指令一樣，您只需將新的 `+desc` 指令新增至預設指令
cmdset：將`evennia.contrib.game_systems.multidescer.CmdMultiDesc`匯入
`mygame/commands/default_cmdsets.py` 並將其新增到 `CharacterCmdSet` 類中。

重新載入伺服器，您應該可以使用 `+desc` 指令（它
將替換預設的 `desc` 指令）。

(usage)=
## 用法

在遊戲中使用`+desc`指令：

    +desc [key]                - show current desc desc with <key>
    +desc <key> = <text>       - add/replace desc with <key>
    +desc/list                 - list descriptions (abbreviated)
    +desc/list/full            - list descriptions (full texts)
    +desc/edit <key>           - add/edit desc <key> in line editor
    +desc/del <key>            - delete desc <key>
    +desc/swap <key1>-<key2>   - swap positions of <key1> and <key2> in list
    +desc/set <key> [+key+...] - set desc as default or combine multiple descs

例如，您可以為衣服設定一個描述，為靴子設定另一個描述，
髮型或任何你喜歡的東西。使用 `|/` 為多行描述新增換行符
段落，以及 `|_` 來強制縮排和空格（我們不
在範例中包含顏色，因為它們未在本文件中顯示）。

    +desc base = A handsome man.|_
    +desc mood = He is cheerful, like all is going his way.|/|/
    +desc head = On his head he has a red hat with a feather in it.|_
    +desc shirt = His chest is wrapped in a white shirt. It has golden buttons.|_
    +desc pants = He wears blue pants with a dragorn pattern on them.|_
    +desc boots = His boots are dusty from the road.
    +desc/set base + mood + head + shirt + pants + boots

當檢視這個字元時，您現在將看到（假設自動換行）

    A hansome man. He is cheerful, like all is going his way.

    On his head he has a red hat with a feather in it. His chest is wrapped in a
    white shirt. It has golden buttons. He wears blue pants with a dragon
    pattern on them. His boots are dusty from the road.

如果你現在這樣做

    +desc mood = He looks sullen and forlorn.|/|/
    +desc shirt = His formerly white shirt is dirty and has a gash in it.|_

您的描述現在將是

    A handsome man. He looks sullen and forlorn.

    On his head he as a red hat with a feathre in it. His formerly white shirt
    is dirty and has a gash in it. He wears blue pants with a pattern on them.
    His boots are dusty from the road.

您可以使用任意數量的“片段”來建立您的描述，並且可以交換
並根據您的喜好和 RP 的要求替換它們。


----

<small>此檔案頁面是從`evennia\contrib\game_systems\multidescer\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
