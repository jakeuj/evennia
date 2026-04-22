(inline-functions)=
# 行內函數

```{sidebar}
有關行內函數的更多資訊，請參閱 [FuncParser](../Components/FuncParser.md) 文件
```
_行內函數_，也稱為_funcparser函式_是表單上的嵌入字串

    $funcname(args, kwargs)

例如

    > say the answer is $eval(24 * 12)!
    You say, "the answer is 288!"

預設情況下禁用傳出字串的常規處理。若要啟動傳出字串的行內函數解析，請將其新增至您的設定檔：

    FUNCPARSER_PARSE_OUTGOING_MESSAGES_ENABLED=True    

行內函數由[FuncParser](../Components/FuncParser.md)提供。它在其他幾種情況下啟用：

- [原型]的處理(../Components/Prototypes.md)；這些「prototypefuncs」允許原型的值在產生時動態變化。例如，您可以設定 `{key: '$choice(["Bo", "Anne", "Tom"])'` 並每次產生一個隨機命名的角色。
- 將字串處理為 `msg_contents` 方法。這允許[根據誰將看到它們傳送不同的訊息](./Change-Message-Per-Receiver.md)。