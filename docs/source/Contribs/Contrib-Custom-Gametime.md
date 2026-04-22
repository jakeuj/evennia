(custom-gameime)=
# 自訂遊戲模式

Contrib 由 vlgeoff，2017 年 - 基於 Griatch 的核心原創

這重新實現了 `evennia.utils.gametime` 模組，但帶有 _custom_
您的遊戲世界的日曆（每週/每月/每年的異常天數等）。
與原始版本一樣，它允許安排事件在給定的時間發生
遊戲中的時間，但現在考慮到這個自訂日曆。

(installation)=
## 安裝

以與正常情況相同的方式匯入和使用它
`evennia.utils.gametime` 模組。

透過在您的設定中新增 `TIME_UNITS` 字典來自訂行事曆（請參閱
下面的例子）。


(usage)=
## 用法：

```python
    from evennia.contrib.base_systems import custom_gametime

    gametime = custom_gametime.realtime_to_gametime(days=23)

    # scedule an event to fire every in-game 10 hours
    custom_gametime.schedule(callback, repeat=True, hour=10)

```

可以透過將 `TIME_UNITS` 字典新增至您的日曆中來自訂日曆
設定檔。這將單位名稱對映到其長度，以最小的形式表示
單位。以下是預設值的範例：

    TIME_UNITS = {
        "sec": 1,
        "min": 60,
        "hr": 60 * 60,
        "hour": 60 * 60,
        "day": 60 * 60 * 24,
        "week": 60 * 60 * 24 * 7,
        "month": 60 * 60 * 24 * 7 * 4,
        "yr": 60 * 60 * 24 * 7 * 4 * 12,
        "year": 60 * 60 * 24 * 7 * 4 * 12, }

使用自訂日曆時，這些時間單位名稱會用作 kwargs
轉換器在此模組中起作用。即使您的日曆使用其他名稱
對於幾個月/幾週等，系統內部需要預設名稱。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\custom_gametime\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
