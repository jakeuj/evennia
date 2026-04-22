(connect-evennia-to-twitter)=
# 將 Evennia 連線到 Twitter


[Twitter](https://en.wikipedia.org/wiki/twitter) 是一種線上社交網路服務，使使用者能夠傳送和閱讀稱為「推文」的短訊息。以下是一個簡短的教程，說明如何使使用者能夠從 Evennia 內部傳送推文。

(configuring-twitter)=
## 設定 Twitter

您首先必須有一個 Twitter 帳戶。在 [Twitter 開發網站](https://apps.twitter.com/) 登入並註冊應用程式。確保您啟用「寫入」推文的存取許可權！

要從 Evennia 發推文，您將需要“API 令牌”和“API 秘密”字串以及“訪問令牌”和“訪問秘密”字串。

Twitter 更改了要求，要求 Twitter 帳戶上有手機號碼才能註冊具有寫入許可權的新應用程式。  如果您無法執行此操作，請參閱[此開發帖子](https://dev.twitter.com/notifications/new-apps-registration)，其中描述如何解決此問題。

要使用 Twitter，您必須安裝 [Twitter](https://pypi.python.org/pypi/twitter) Python 模組：

```
pip install python-twitter
```

(setting-up-twitter-step-by-step)=
## 逐步設定 Twitter

(a-basic-tweet-command)=
### 基本推文指令

Evennia 沒有開箱即用的 `tweet` 指令，因此您需要編寫自己的小 [指令](../Components/Commands.md) 才能發推文。如果您不確定指令如何運作以及如何新增它們，最好在繼續之前先閱讀[新增指令教學](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)。

您可以根據需要在單獨的指令模組（例如 `mygame/commands/tweet.py`）中或與其他自定義指令一起建立指令。 
它看起來是這樣的：

```python
# in mygame/commands.tweet.py, for example

import twitter
from evennia import Command

# here you insert your unique App tokens
# from the Twitter dev site
TWITTER_API = twitter.Api(consumer_key='api_key',
                          consumer_secret='api_secret',
                          access_token_key='access_token_key',
                          access_token_secret='access_token_secret')

class CmdTweet(Command):
    """
    Tweet a message

    Usage: 
      tweet <message>

    This will send a Twitter tweet to a pre-configured Twitter account.
    A tweet has a maximum length of 280 characters. 
    """

    key = "tweet"
    locks = "cmd:pperm(tweet) or pperm(Developers)"
    help_category = "Comms"

    def func(self):
        "This performs the tweet"
 
        caller = self.caller
        tweet = self.args

        if not tweet:
            caller.msg("Usage: tweet <message>")      
            return
 
        tlen = len(tweet)
        if tlen > 280:
            caller.msg(f"Your tweet was {tlen} chars long (max 280).")
            return

        # post the tweet        
        TWITTER_API.PostUpdate(tweet)

        caller.msg(f"You tweeted:\n{tweet}")
```

請務必在適當的位置替換您自己的實際 API/存取金鑰和機密。

我們預設推文存取許可權制為具有 `Developers` 級別存取許可權的玩家*或*具有「推文」許可權的玩家

若要允許單一字元發推文，請設定 `tweet` 許可權

    perm/player playername = tweet
    
您可以根據需要更改[lock](../Components/Locks.md)。如果您希望每個人都能夠發推文，請將整體許可權變更為 `Players`。

現在將此指令新增至您的預設指令集（`mygame/commands/defalt_cmdsets.py` 中的e.g）和`reload` 伺服器。從現在開始，擁有存取許可權的人只需使用 `tweet <message>` 即可檢視遊戲 Twitter 帳戶發布的推文。

(next-steps)=
### 下一步

這僅顯示了基本的推文設定，其他要做的事情可能是：

* 自動將角色名稱新增至推文中
* 對帖子進行更多錯誤檢查
* 改變鎖定，讓推文向更多人開放
* 將您的推文回顯到遊戲內頻道

您可以設定 Script 來傳送自動推文，例如發布更新的遊戲統計資料，而不是使用明確指令。請參閱[推文遊戲統計教學](../Howtos/Web-Tweeting-Game-Stats.md) 尋求協助。