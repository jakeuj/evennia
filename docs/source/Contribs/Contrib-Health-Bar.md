(health-bar)=
# 生命棒

蒂姆·阿什利·詹金斯 (Tim Ashley Jenkins) 貢獻，2017 年

此模組提供的功能可讓您輕鬆展示視覺效果
條或米作為彩色條而不僅僅是數字。一個“健康棒”
這只是最明顯的用途，但該欄是高度可自訂的
並且可以用於玩家健康以外的任何型別的適當資料。

今天的玩家可能更習慣檢視健康狀況等統計資料，
耐力、魔法等顯示為條形而非純粹的數字
值，因此使用此模組以這種方式呈現此資料可能會使其
更容易接近。但請記住，玩家也可能會使用
螢幕閱讀器連線到您的遊戲，這將無法
以任何方式表示條形的顏色。預設情況下，這些值
表示呈現為條內的文字，可以透過
螢幕閱讀器。

(usage)=
## 用法

無需安裝，只需從此匯入並使用`display_meter`
模組：

```python
    from evennia.contrib.rpg.health_bar import display_meter

    # health is 23/100
    health_bar = display_meter(23, 100)
    caller.msg(prompt=health_bar)

```

健康欄將考慮當前值高於最大值或
低於 0，將它們渲染為完全滿或空的條形
內顯示的值。



----

<small>此檔案頁面是從`evennia\contrib\rpg\health_bar\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
