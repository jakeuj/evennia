(zones)=
# 區域

Evennia 建議使用 [Tags](../Components/Tags.md) 建立區域和其他分組。

假設您在漂亮的大森林 MUD 中建立了一個名為 *Meadow* 的房間。  這一切都很好，但是
如果您在森林的另一端想要另一個*草地*怎麼辦？作為遊戲創作者，這可以
造成各種混亂。例如，傳送到 *Meadow* 現在會向您發出警告：
有兩個 *Meadow* ，您必須選擇哪一個。這樣做沒問題，你只需
例如，選擇轉到 `2-meadow`，但除非您檢查它們，否則您無法確定哪一個
兩人坐在森林的神奇部分，但事實並非如此。

另一個問題是您是否想按地理區域對房間進行分組。  讓我們說“正常”部分
森林應該有與魔法部分不同的天氣模式。或者也許是一個神奇的
幹擾在所有魔法森林房間中迴響。這樣就可以方便地
只需找到所有“神奇”的房間，這樣您就可以向他們傳送訊息。

(zones-in-evennia)=
## Evennia 中的區域

*區域*嘗試以全球位置分隔房間。在我們的例子中，我們將森林分為兩部分 - 魔法部分和非魔法部分。每個部分都有一個*草地*，屬於每個部分的房間應該很容易檢索。

許多 MUD 程式碼庫將區域硬編碼為引擎和資料庫的一部分。  Evennia 沒有這樣的
區別。

Evennia 中的所有物件可以容納任意數量的 [Tags](../Components/Tags.md)。 Tags 是附加到物件上的短標籤。它們使得檢索物件組變得非常容易。一個物件可以有任意數量的不同tags。因此，讓我們將相關的tag附加到我們的森林中：

```python
     forestobj.tags.add("magicalforest", category="zone")
```

您可以手動新增它，或者在建立過程中以某種方式自動新增（您需要修改您的
`dig` 指令，最有可能）。您也可以在建置過程中使用預設的 `tag` 指令：

     tag forestobj = magicalforest : zone

從此以後，您可以輕鬆地僅檢索具有給定 tag 的物件：

```python
     import evennia
     rooms = evennia.search_tag("magicalforest", category="zone")
```

(using-typeclasses-and-inheritance-for-zoning)=
## 使用 typeclasses 和繼承進行分割槽

上面的標記或別名系統不會在魔法森林房間和普通森林房間之間灌輸任何功能差異 - 它們只是標記物件以便以後快速檢索的任意方法。任何功能差異都必須使用 [Typeclasses](../Components/Typeclasses.md) 表示。

當然，實現區域本身的另一種方法是讓區域中的所有房間/物件繼承給定的 typeclass 父級 - 然後將搜尋限制為從給定父級繼承的物件。效果類似，但您需要將搜尋功能擴充套件到
正確搜尋繼承樹。