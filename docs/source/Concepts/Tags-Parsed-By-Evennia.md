(in-text-tags-parsed-by-evennia)=
# 文內 tags 由 Evennia 解析
```{toctree}
:maxdepth: 2

Colors.md
Clickable-Links.md
Inline-Functions.md
```

Evennia 將解析嵌入文字中的各種特殊 tags 和標記，並根據資料是否傳入或傳出伺服器來動態轉換。

- _顏色_ - 使用 `|r`、`|n` 等可用於以顏色標記文字部分。顏色會
對於 Telnet 連線，變為 ANSI/XTerm256 顏色 tags；對於 webclient，變為 CSS 資訊。
    ```
    > say Hello, I'm wearing my |rred hat|n today. 
    ```
- _可點選連結_ - 這允許您提供使用者可以點選以執行的文字
遊戲中的指令。其格式為 `|lc command |lt text |le`。可點選的連結通常僅在_outgoing_方向上進行解析，因為如果使用者可以提供它們，它們可能會成為潛在的安全問題。要啟用，必須將 `MXP_ENABLED=True` 新增到設定（預設為停用）。
    ```
    py self.msg("This is a |c look |ltclickable 'look' link|le")
    ```
- _FuncParser callables_ - 這些是 `$funcname(args, kwargs)` 形式的成熟函式呼叫，導致對 Python 函式的呼叫。解析器可以在不同的情況下使用不同的可用可呼叫物件來執行。如果 `settings.FUNCPARSER_PARSE_OUTGOING_MESSAGES_ENABLED=True`（預設為停用），則對所有傳出訊息執行解析器。
    ```
    > say The answer is $eval(40 + 2)! 
    ```


