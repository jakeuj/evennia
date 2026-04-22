(evennia-game-index)=
# Evennia 遊戲索引


[Evennia 遊戲索引](http://games.evennia.com) 是已建置的遊戲清單或
正在使用 Evennia 建置。任何人都可以將他們的遊戲新增到索引中
- 另外，如果您剛開始開發並且尚未接受外部
玩家。這是一個讓我們知道你的機會，也是你讓我們變得更好的機會
對您即將推出的遊戲感興趣或興奮！

我們所要求的只是您檢查一下，以免您的遊戲名稱與遊戲名稱相衝突
已經在清單中了 - 保持友善！

(connect-with-the-wizard)=
## 與嚮導連線

從你的遊戲目錄執行

    evennia connections 

這將啟動Evennia_連線精靈_。從選單中選擇新增
your game to the Evennia Game Index.按照提示操作，不要忘記
最後儲存您的新設定。如果您更改了您的密碼，請隨時使用 `quit`
介意。

> 嚮導將建立一個新檔案`mygame/server/conf/connection_settings.py`
> 使用您選擇的設定。這是從你的 main 的末端匯入的
> 設定檔案，因此將覆蓋它。您可以編輯這個新檔案，如果您
> 想要，但請記住，如果您再次執行嚮導，您的更改可能會
> 重寫了。

(manual-settings)=
## 手動設定

如果您不想使用該嚮導（可能是因為您已經從
早期版本），您也可以在設定檔中設定索引條目
(`mygame/server/conf/settings.py`)。新增以下內容：

```python
GAME_INDEX_ENABLED = True 

GAME_INDEX_LISTING = {
    # required 
    'game_status': 'pre-alpha',            # pre-alpha, alpha, beta, launched
    'listing_contact': "dummy@dummy.com",  # not publicly shown.
    'short_description': 'Short blurb',    

    # optional 
    'long_description':
        "Longer description that can use Markdown like *bold*, _italic_"
        "and [linkname](https://link.com). Use \n for line breaks."
    'telnet_hostname': 'dummy.com',            
    'telnet_port': '1234',                     
    'web_client_url': 'dummy.com/webclient',   
    'game_website': 'dummy.com',              
    # 'game_name': 'MyGame',  # set only if different than settings.SERVERNAME
}
```

其中，`game_status`、`short_description` 和 `listing_contact` 是
需要。  `listing_contact` 不公開可見，僅用作
如果我們需要就任何清單問題/錯誤與您聯絡，這是最後的手段（所以
到目前為止，這種情況從未發生過）。

如果未設定`game_name`，則將使用`settings.SERVERNAME`。使用空字串
(`''`) 用於此時您不想指定的選用欄位。

(non-public-games)=
## 非公開遊戲

如果您既不指定 `telnet_hostname + port` 也不指定
`web_client_url`，遊戲索引會將您的遊戲列為_尚未公開_。
非公開遊戲被移至指數底部，因為沒有辦法
供人們嘗試。但這是表明你在外面的好方法，即使
如果你還沒準備好迎接玩家。
