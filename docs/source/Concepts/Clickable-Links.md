(clickable-links)=
# 可點選的連結

Evennia 允許為支援它的使用者端提供可點選的文字連結。這會標記某些文字，以便可以透過滑鼠點選它並觸發給定的 Evennia 指令，或在外部 Web 瀏覽器中開啟 URL。要檢視可點選的連結，玩家必須使用 Evennia webclient 或支援 [MXP](http://www.zuggsoft.com/zmud/mxp.htm) 的第三方 telnet 用戶端（*注：Evennia 僅支援可點選的連結，不支援其他 MXP 功能*）。

用戶端缺乏 MXP 支援的使用者將只能看到普通文字形式的連結。

```{important}
預設情況下，無法從遊戲內新增可點選連結。嘗試這樣做將使連結返回為普通文字。這是一項安全措施。請參閱[設定](#settings) 以瞭解更多資訊。
```

(click-to-run-a-command)=
## 點選以執行指令

```
|lc command |lt text |le
```

例子：

```
"If you go |lcnorth|ltto the north|le you will find a cottage."
```

這將顯示為「如果你去 __to the north__，你會發現一座小屋。」點選該連結將執行指令 `north`。

(click-to-open-an-url-in-a-web-browser)=
## 按一下以在網頁瀏覽器中開啟 URL

```
|lu url |lt text |le 
```

例子：

```
"Omnious |luhttps://mycoolsounds.com/chanting|ltchanting sounds|le are coming from beyond the door."
```

這將顯示為“Omnious **誦經聲**從門外傳來”，如果用戶端支援這樣做，則單擊連結將在瀏覽器中開啟 URL。

(settings)=
## 設定

整體啟用/停用MXP（預設啟用）。

```
MXP_ENABLED = True 
```

預設情況下，幫助條目具有可按一下的主題。

```
HELP_CLICKABLE_TOPICS = True
```

預設情況下，可點選連結只能從_程式碼中提供的字串_（或透過[batch script](../Components/Batch-Processors.md)）取得。您_無法_從遊戲內部建立可點選的連結 - 結果將不會顯示為可點選的。

這是一項安全措施。考慮使用者是否能夠在其描述中輸入可點選的連結，如下所示：

```
|lc give 1000 gold to Bandit |ltClick here to read my backstory!|le
```

這將由可憐的玩家點選連結來執行，結果他們向強盜支付 1000 金幣。

這是由以下預設設定控制的：

```
MXP_OUTGOING_ONLY = True
```

只有當您知道您的遊戲無法以這種方式被利用時，才停用此保護。