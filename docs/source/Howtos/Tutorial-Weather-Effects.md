(adding-weather-messages-to-a-room)=
# 將天氣訊息加入房間


本教學將讓我們為MUD 建立一個簡單的天氣系統。  我們想要使用它的方式是讓所有室外房間以定期和半隨機的間隔向房間回顯與天氣相關的訊息。諸如「烏雲密佈」、「開始下雨了」等。

人們可以想像遊戲中的每個室外房間都有一個 script 自行執行並定期觸發。然而，對於這個特定的範例，採用另一種方​​式更有效，即使用「股票訂閱」模型。

原理很簡單：它們不是讓每個物件單獨追蹤時間，而是訂閱由處理時間記錄的全域自動收報機呼叫。  這不僅可以將大部分程式碼集中並組織在一個地方，而且還可以減少計算開銷。

Evennia的[TickerHandler](../Components/TickerHandler.md)專門提供了這樣的訂閱模式。我們將把它用於我們的天氣系統。

我們將創造一個新的 WeatherRoom typeclass 來感知晝夜週期。

```{code-block} python
:linenos:
:emphasize-lines: 

    import random
    from evennia import DefaultRoom, TICKER_HANDLER
    
    ECHOES = ["The sky is clear.", 
              "Clouds gather overhead.",
              "It's starting to drizzle.",
              "A breeze of wind is felt.",
              "The wind is picking up"] # etc  

    class WeatherRoom(DefaultRoom):
        "This room is ticked at regular intervals"        
       
        def at_object_creation(self):
            "called only when the object is first created"
            TICKER_HANDLER.add(60 * 60, self.at_weather_update)

        def at_weather_update(self, *args, **kwargs):
            "ticked at regular intervals"
            echo = random.choice(ECHOES)
            self.msg_contents(echo)
```



在 `at_object_creation` 方法中，我們只是將自己加到 TickerHandler 並告訴它
每小時呼叫 `at_weather_update`（`60*60` 秒）。在測試過程中，您可能會想玩一下
持續時間較短。

為此，我們還建立了一個自訂掛鉤 `at_weather_update(*args, **kwargs)`，這是
TickerHandler 掛鉤需要呼號。

從今以後，當天氣改變時，房間會通知裡面的每個人。這個特殊的例子
當然是非常簡單的 - 天氣回波只是隨機選擇的，並不關心什麼
天氣先於它而來。將其擴充套件得更現實是一項有用的練習。