(tickerhandler)=
# TickerHandler


實現動態 MUD 的一種方法是使用“程式碼”，也稱為“心跳”。自動收報機是一個按給定時間間隔觸發（“滴答”）的計時器。勾選會觸發各種遊戲系統的更新。

在其他 mud 程式碼庫中，程式碼非常常見，甚至是不可避免的。  某些程式碼庫甚至被硬編碼為依賴全域「tick」的概念。 Evennia 沒有這樣的概念 - 使用程式碼的決定很大程度上取決於您的遊戲的需要以及您的要求。 「股票配方」只是啟動輪子的一種方式。

管理時間流的最細微的方法是使用 [utils.delay](evennia.utils.utils.delay)（使用 [TaskHandler](evennia.scripts.taskhandler.TaskHandler)）。另一種是使用[Scripts](./Scripts.md)的時間重複能力。這些工具對單一物件進行操作。

然而，許多型別的操作（天氣是典型的例子）都是以相同的方式定期在多個物件上完成的，為此，為每個此類物件設定單獨的延遲/scripts 效率很低。

做到這一點的方法是使用帶有“訂閱模型”的股票程式碼 - 讓物件註冊成為
以相同的時間間隔觸發，當不再需要更新時取消訂閱。這意味著所有物件的計時機制僅設定一次，從而使訂閱/取消訂閱更快。

Evennia 提供訂閱模型的最佳化實現 - *TickerHandler*。這是一個可從 [evennia.TICKER_HANDLER](evennia.utils.tickerhandler.TickerHandler) 存取的單例全域處理程式。您可以將任何*可呼叫*（函式，或更常見的是資料庫物件上的方法）指派給此處理程式。然後 TickerHandler 將按照您指定的時間間隔呼叫此可呼叫函式，並使用新增它時提供的引數。這將持續到可呼叫物件取消訂閱股票程式碼為止。該處理程式在重新啟動後仍然存在，並且在資源使用方面進行了高度最佳化。

(usage)=
## 用法

以下是匯入 `TICKER_HANDLER` 並使用它的範例：

```python
    # we assume that obj has a hook "at_tick" defined on itself
    from evennia import TICKER_HANDLER as tickerhandler    

    tickerhandler.add(20, obj.at_tick)
``` 
就是這樣 - 從現在開始，`obj.at_tick()` 將每 20 秒呼叫一次。

```{important}
您提供給 `TickerHandler.add` 的所有內容都需要在某個時刻進行 pickle 才能儲存到資料庫中 - 如果您使用 `persistent=False` 也是如此。大多數情況下，處理程式將正確儲存資料庫物件等內容，但與 [屬性](./Attributes.md) 相同的限制適用於 TickerHandler 可以儲存的內容。
```

您也可以匯入一個函式並勾選：

```python
    from evennia import TICKER_HANDLER as tickerhandler
    from mymodule import myfunc

    tickerhandler.add(30, myfunc)
```

刪除（停止）股票程式碼按預期工作：

```python
    tickerhandler.remove(20, obj.at_tick)
    tickerhandler.remove(30, myfunc) 
```

請注意，您還必須提供 `interval` 來識別要刪除的訂閱。這是因為 TickerHandler 維護了一個股票程式碼池，而給定的可呼叫物件可以訂閱以任意數量的不同時間間隔進行股票程式碼更新。

`tickerhandler.add` 方法的完整定義是

```python
    tickerhandler.add(interval, callback, 
                      idstring="", persistent=True, *args, **kwargs)
```

這裡 `*args` 和 `**kwargs` 將每隔 `interval` 秒傳遞給 `callback`。如果`persistent`
是 `False`，此訂閱將被_伺服器關閉_擦除（正常重新載入後仍會存在）。

透過建立可呼叫本身的鍵、股票程式碼間隔、`persistent` 標誌和 `idstring`（如果未明確給出，後者為空字串）來識別和儲存股票程式碼。

由於引數不包含在股票程式碼的標識中，因此必須使用 `idstring` 來以相同的時間間隔但使用不同的引數多次觸發特定的回撥：

```python
    tickerhandler.add(10, obj.update, "ticker1", True, 1, 2, 3)
    tickerhandler.add(10, obj.update, "ticker2", True, 4, 5)
```

> 請注意，當我們想要在股票處理程式中向回撥傳送引數時，我們需要在先前指定 `idstring` 和 `persistent` ，除非我們將引數稱為關鍵字，這通常更具可讀性：

```python
    tickerhandler.add(10, obj.update, caller=self, value=118)
```

如果您新增具有完全相同的回撥、間隔和 idstring 組合的股票程式碼，它將
使現有的股票代號超載。此標識對於以後刪除（停止）訂閱也至關重要：

```python
    tickerhandler.remove(10, obj.update, idstring="ticker1")
    tickerhandler.remove(10, obj.update, idstring="ticker2")
```

`callable` 可以採用任何形式，只要它接受您在 `TickerHandler.add` 中傳送給它的引數。

測試時，您可以使用`tickerhandler.clear()`停止整個遊戲中的所有行情。您也可以透過`tickerhandler.all()`檢視目前訂閱的物件。

有關使用 TickerHandler 的範例，請參閱[天氣教學](../Howtos/Tutorial-Weather-Effects.md)。

(when-not-to-use-tickerhandler)=
### 當*不*使用TickerHandler時

使用 TickerHandler 可能聽起來非常有用，但重要的是要考慮何時不使用它。即使您習慣於習慣性地依賴程式碼來獲取其他程式碼庫中的所有內容，也請停下來思考您真正需要它的用途。這是要點：
 
> 你不應該*永遠*使用股票程式碼來捕捉*變化*。

想一想 - 您可能必須每秒執行一次股票行情自動收錄器才能足夠快地對變化做出反應。在某個特定時刻，很可能什麼都不會改變。因此，您正在執行毫無意義的呼叫（因為跳過呼叫會產生與執行呼叫相同的結果）。確保不發生任何變更甚至可能會耗費大量運算資源，具體取決於系統的複雜性。更不用說您可能需要對資料庫中的每個物件執行檢查。每一秒。只是為了維持現狀...

與其一遍又一遍地檢查是否有變化，不如考慮採取更主動的方法。您能否實現很少變化的系統，以便在其狀態變更時「自身」報告？  如果您可以「按需」做事，那麼它幾乎總是便宜/有效率得多。 Evennia 本身就是因為這個原因才使用鉤子方法。

因此，如果您考慮一個會經常觸發但您預計 99% 的時間都沒有效果的自動收錄器，請考慮以其他方式處理事情。對於快速更新的屬性來說，自我報告的按需解決方案通常也更便宜。還要記住，有些東西可能不需要更新，直到有人真正檢查或使用它們 - 在那一刻發生的任何臨時更改都是毫無意義的計算時間浪費。

需要股票程式碼的主要原因是當您希望多個物件同時發生事情而無需其他東西的輸入時。