(automatically-tweet-game-stats)=
# 自動發布遊戲統計資料


本教學將建立一個簡單的 script ，它將向您已設定的 Twitter 帳戶傳送推文。如果您還沒有這樣做，請參閱：[如何將 Evennia 連線到 Twitter](../Setup/Channels-to-Twitter.md)。

script 可以擴充套件涵蓋您可能希望發布推文的各種統計資料
定期，從玩家死亡到經濟中有多少貨幣等。

```python
# evennia/typeclasses/tweet_stats.py

import twitter
from random import randint
from django.conf import settings
from evennia import ObjectDB
from evennia.prototypes import prototypes
from evennia import logger
from evennia import DefaultScript

class TweetStats(DefaultScript):
    """
    This implements the tweeting of stats to a registered twitter account
    """

    # standard Script hooks 

    def at_script_creation(self):
        "Called when script is first created"

        self.key = "tweet_stats"
        self.desc = "Tweets interesting stats about the game"
        self.interval = 86400  # 1 day timeout
        self.start_delay = False
        
    def at_repeat(self):
        """
        This is called every self.interval seconds to 
        tweet interesting stats about the game.
        """
        
        api = twitter.Api(consumer_key='consumer_key',
          consumer_secret='consumer_secret',
          access_token_key='access_token_key',
          access_token_secret='access_token_secret')
        
        # Game Chars, Rooms, Objects taken from `stats` command
        nobjs = ObjectDB.objects.count()
        base_char_typeclass = settings.BASE_CHARACTER_TYPECLASS
        nchars = (              
            ObjectDB.objects
           .filter(db_typeclass_path=base_char_typeclass)
           .count()
        )
        nrooms =(
            ObjectDB.objects
            .filter(db_location__isnull=True)
            .exclude(db_typeclass_path=base_char_typeclass)
            .count()
        )
        nexits = (
            ObjectDB.objects
            .filter(db_location__isnull=False,
                    db_destination__isnull=False)
            .count()
        )
        nother = nobjs - nchars - nrooms - nexits
        tweet = f"Chars: {ncars}, Rooms: {nrooms}, Objects: {nother}"

        # post the tweet 
        try:
            response = api.PostUpdate(tweet)
        except:
            logger.log_trace(f"Tweet Error: When attempting to tweet {tweet}")
```

在`at_script_creation`方法中，我們將script設定為立即觸發（對於測試有用）
並設定延遲（1天）以及使用`@scripts`時看到的script訊息

在 `at_repeat` 方法中（立即呼叫，然後每隔幾秒鐘呼叫）我們設定
Twitter API（就像 Twitter 的初始設定一樣）。然後我們顯示玩家角色、房間和其他/物體的數量。

[Scripts 檔案](../Components/Scripts.md) 將向您展示如何將其新增為全域 script，但是用於測試
從遊戲中快速啟動/停止它可能很有用。  假設您建立該檔案
如 `mygame/typeclasses/tweet_stats.py` 可以使用以下指令啟動

    script Here = tweet_stats.TweetStats