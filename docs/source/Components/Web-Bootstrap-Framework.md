(bootstrap-frontend-framework)=
# Bootstrap前端框架

Evennia 的預設網頁使用名為 [Bootstrap](https://getbootstrap.com/) 的框架。該框架在網際網路上廣泛使用 - 一旦您學習了一些常見的設計模式，您可能會開始認識到它的影響。這個開關對於 Web 開發人員（也許像您一樣）來說非常有用，因為我們不必考慮設定不同的網格系統或其他設計人員使用的自定義類，而是有一個基礎，一個載入程式，可以用來工作。 Bootstrap 預設是響應式的，並附帶了一些預設樣式，Evennia 已稍微覆蓋這些預設樣式，以保留您在先前的設計中習慣的一些相同的顏色和樣式。

e，Bootstrap 的簡要概述如下。如需瞭解更深入的資訊，請
閱讀[檔案](https://getbootstrap.com/docs/4.0/getting-started/introduction/)。

(grid-system)=
## 網格系統

除了 Bootstrap 包含的基本樣式外，它還包含[內建的佈局和網格系統](https://getbootstrap.com/docs/4.0/layout/overview/)。

(the-container)=
### 容器

網格系統的第一部分是[容器](https://getbootstrap.com/docs/4.0/layout/overview/#containers)。

此容器用於儲存所有頁面內容。 Bootstrap提供兩種：固定寬度和
全形。固定寬度容器佔用一定的頁面最大寬度 - 它們對於限制桌面或平板電腦平臺上的寬度非常有用，而不是使內容跨越頁面的寬度。

```
<div class="container">
    <!--- Your content here -->
</div>
```
全寬容器佔據了它們可用的最大寬度 - 它們將跨越很寬的寬度 -
螢幕桌面或較小螢幕的手機，邊緣到邊緣。
```
<div class="container-fluid">
    <!--- This content will span the whole page -->
</div>
```

(the-grid)=
### 網格

佈局系統的第二部分是[網格](https://getbootstrap.com/docs/4.0/layout/grid/)。

這是 Bootstrap 佈局的基礎 - 它允許您根據螢幕的大小更改元素的大小，而無需編寫任何媒體查詢。我們將簡要回顧一下 - 要了解更多資訊，請閱讀文件或在瀏覽器中檢視 Evennia 主頁的原始碼。

> 重要的！網格元素應位於.container 或.container-fluid 中。這將使
您網站的內容。

Bootstrap 的網格系統可讓您透過套用基於斷點的類別來建立行和列。預設斷點為特小、小、中、大和特大。如果您想了解有關這些斷點的更多資訊，請[檢視以下檔案]
他們。 ](https://getbootstrap.com/docs/4.0/layout/overview/#responsive-breakpoints)

要使用網格系統，首先為您的內容建立一個容器，然後新增行和列，如下所示：
```
<div class="container">
    <div class="row">
        <div class="col">
           1 of 3
        </div>
        <div class="col">
           2 of 3
        </div>
        <div class="col">
           3 of 3
        </div>
    </div>
</div>
```
此佈局將建立三個等寬的列。

要指定您的大小 - 例如，Evennia 的預設網站在桌面上有三列，
平板電腦，但在較小的螢幕上回流為單列。嘗試一下！
```
<div class="container">
    <div class="row">
        <div class="col col-md-6 col-lg-3">
            1 of 4
        </div>
        <div class="col col-md-6 col-lg-3">
            2 of 4
        </div>
        <div class="col col-md-6 col-lg-3">
            3 of 4
        </div>
        <div class="col col-md-6 col-lg-3">
            4 of 4
        </div>
    </div>
</div>
```
此佈局在大螢幕上為 4 列，在中型螢幕上為 2 列，在大螢幕上為 1 列。
任何更小的東西。

要了解有關 Bootstrap 網格的更多資訊，請[檢視
檔案](https://getbootstrap.com/docs/4.0/layout/grid/)
我
(general-styling-elements)=
## 一般樣式元素

Bootstrap 為您的網站提供基本樣式。這些可以透過CSS自訂，但是預設的
樣式旨在為網站提供一致、乾淨的外觀。

(color)=
### 顏色
大多數元素都可以使用預設顏色設定樣式。 [檢視檔案](https://getbootstrap.com/docs/4.0/utilities/colors/) 以瞭解有關這些顏色的更多資訊
- 可以說，加入一類text-*或bg-*，例如text-primary，設定文字顏色
或背景顏色。

(borders)=
### 邊框

只需在元素中新增“border”類別即可為該元素新增邊框。為了更深入
資訊，請[閱讀有關邊框的文件。 ](https://getbootstrap.com/docs/4.0/utilities/borders/)。
```
<span class="border border-dark"></span>
```
您也可以透過新增類別來輕鬆圓角。
```
<img src="..." class="rounded" />
```

(spacing)=
### 間距
Bootstrap 提供了一些類別來輕鬆新增響應式邊距和填充。大多數時候，您可能希望透過 CSS 本身新增邊距或填充 - 但是這些類別在預設的 Evennia 網站中使用。 [檢視檔案](https://getbootstrap.com/docs/4.0/utilities/spacing/)
瞭解更多。

(buttons)=
### 按鈕

Bootstrap 中的[按鈕](https://getbootstrap.com/docs/4.0/components/buttons/) 非常容易使用 - 可以將按鈕樣式新增至 `<button>`、`<a>` 和 `<input>` 元素。
```
<a class="btn btn-primary" href="#" role="button">I'm a Button</a>
<button class="btn btn-primary" type="submit">Me too!</button>
<input class="btn btn-primary" type="button" value="Button">
<input class="btn btn-primary" type="submit" value="Also a Button">
<input class="btn btn-primary" type="reset" value="Button as Well">
```

(cards)=
### 牌

[Cards](https://getbootstrap.com/docs/4.0/components/card/) 為其他元素提供容器
從頁面的其餘部分中脫穎而出。 “帳戶”、“最近連線”和“資料庫”
預設網頁上的「統計資料」全部以卡片形式顯示。卡片提供了相當多的格式化選項 -
以下是一個簡單的範例，但請閱讀檔案或檢視網站的原始程式碼以瞭解更多資訊。
```
<div class="card">
  <div class="card-body">
    <h4 class="card-title">Card title</h4>
    <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
    <p class="card-text">Fancy, isn't it?</p>
    <a href="#" class="card-link">Card link</a>
  </div>
</div>
```

(jumbotron)=
### 超大螢幕

[大螢幕](https://getbootstrap.com/docs/4.0/components/jumbotron/) 對於展示
您的遊戲的影象或標語。它們可以與您的其餘內容一起流動或佔據全部內容
頁面寬度 - Evennia 的基本網站使用前者。
```
<div class="jumbotron jumbotron-fluid">
  <div class="container">
    <h1 class="display-3">Full Width Jumbotron</h1>
    <p class="lead">Look at the source of the default Evennia page for a regular Jumbotron</p>
  </div>
</div>
```

(forms)=
### 表格

[表單](https://getbootstrap.com/docs/4.0/components/forms/) 可以使用 Bootstrap 進行高度自訂。
若想更深入瞭解如何在您自己的 Evennia 網站中使用表單及其樣式，請閱讀
結束[網頁角色生成教學](../Howtos/Web-Character-Generation.md)

(further-reading)=
## 進一步閱讀

Bootstrap 還提供了大量實用程式，以及樣式和內容元素。要了解有關它們的更多資訊，請[閱讀 Bootstrap 檔案](https://getbootstrap.com/docs/4.0/getting- started/introduction/) 或閱讀我們的其他網路教學之一。