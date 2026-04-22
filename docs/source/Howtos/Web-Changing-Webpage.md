(changing-the-game-website)=
# 更改遊戲網站


Evennia 使用 [Django](https://www.djangoproject.com/) Web 框架作為其資料庫設定和其提供的網站的基礎。雖然全面瞭解 Django 需要閱讀 Django 文件，但我們提供了本教學來幫助您瞭解基礎知識以及它們如何與 Evennia 相關。本文詳細介紹如何設定所有內容。 [基於網路的角色檢視教學](./Web-Character-View-Tutorial.md) 提供了製作連線到您的遊戲的自訂網頁的更明確的範例，您可能需要在完成本指南後閱讀該範例。

(a-basic-overview)=
## 基本概述

Django 是一個網路框架。它為您提供了一套用於快速輕鬆地建立網站的開發工具。

Django 專案被分成 *apps*，這些應用程式都貢獻給一個專案。例如，您可能有一個用於進行民意調查的應用程式，或者一個用於顯示新聞帖子的應用程式，或者像我們一樣，一個用於建立網路用戶端的應用程式。

這些應用程式中的每一個都有一個 `urls.py` 檔案，該檔案指定應用程式使用的內容 [URL](https://en.wikipedia.org/wiki/Uniform_resource_locator)、一個 `views.py` 檔案用於 URLs 啟用的程式碼、一個 `templates` 目錄用於在 [HTML](https://en.wikipedia.org/wiki/Html) 中為使用者顯示該程式碼的結果資料夾，其中包含諸如[CSS](https://en.wikipedia.org/wiki/CSS)、[Javascript](https://en.wikipedia.org/wiki/Javascript) 和影象檔案（您可能會注意到您的 mygame/web 資料夾沒有 `static` 或 `template` 資料夾。這是有意的，並在下面進一步解釋）。 Django 應用程式也可能有一個 `models.py` 檔案用於在資料庫中儲存資訊。我們不會在這裡更改任何模型，如果您有興趣，請檢視[新模型](../Concepts/Models.md)頁面（以及模型上的[Django檔案](https://docs.djangoproject.com/en/4.1/topics/db/models/)）。

還有一個根`urls.py`決定了整個專案的URL結構。預設遊戲模板中包含初學者`urls.py`，並自動為您匯入Evennia的所有預設URLs。它位於`web/urls.py`。

(changing-the-logo-on-the-front-page)=
## 更改首頁徽標

Evennia 的預設標誌是一條有趣的、瞪大眼睛的蛇，包裹著一個齒輪地球。儘管它很可愛，但它可能並不代表您的遊戲。因此，您可能希望做的第一件事就是用您自己的徽標替換它。

Django Web 應用程式都有_靜態資產_：CSS 檔案、Javascript 檔案和映像檔。為了確保最終專案擁有所需的所有靜態檔案，系統從每個應用程式的 `static` 資料夾中收集檔案並將其放置在 `settings.py` 中定義的 `STATIC_ROOT` 中。預設情況下，Evennia `STATIC_ROOT` 位於 `web/static` 中。

由於 Django 從所有這些單獨的位置提取檔案並將它們放入一個資料夾中，因此一個檔案可能會覆蓋另一個檔案。我們將使用它來插入我們自己的檔案，而不必更改 Evennia 本身中的任何內容。

預設情況下，Evennia 設定為拉取您放在 `mygame/web/static/`*所有其他靜態檔案*之後*的檔案。這意味著 `mygame/web/static/` 資料夾下的檔案將覆蓋任何先前載入的檔案*在其靜態資料夾下具有相同的路徑*。最後一部分很重要，需要重複：要過載標準 `evennia/web/static` 資料夾中的靜態資源，您需要複製 `mygame/web/static/` 下的資料夾和檔案名稱的路徑。幸運的是，你的遊戲目錄的資料夾已經有很多預製的結構，所以它應該非常清楚：例如，為了覆蓋網站的東西，你把它放在`mygame/web/static/website/`下。 Webclient 將是 `mygame/web/static/webclient` 等等。

讓我們看看這對我們的徽標有何作用。預設 Web 應用程式位於 Evennia 庫本身的 `evennia/web/` 中。我們可以看到這裡有一個`static`資料夾。如果我們向下瀏覽，我們最終會找到 Evennia 徽標檔案的完整路徑：`evennia/web/static/website/images/evennia_logo.png`。

將您自己的徽標放在遊戲資料夾中的相應位置：`mygame/web/static/website/images/evennia_logo.png`。

要獲取此檔案，只需更改為您自己的遊戲目錄並重新載入伺服器：

```
evennia reload
```

這將重新載入設定並引入新的靜態檔案。如果您不想重新載入伺服器，您可以使用

```
evennia collectstatic
```

僅更新靜態檔案而不進行任何其他更改。

> Evennia將在啟動時自動收集靜態檔案。因此，如果 `evennia collectstatic` 報告發現 0 個要收集的檔案，請確保您在某個時刻沒有啟動引擎 - 如果是這樣，收集器已經完成了工作！為了確保這一點，請連線到網站並檢查徽標是否已實際更改為您自己的版本。

> 資產收集器實際上是將所有資料收集到一處，在隱藏目錄`mygame/server/.static/`中。這些檔案實際上是從這裡提供的。有時靜態資源收集器可能會感到困惑。如果無論您做什麼，您的覆蓋檔案都沒有複製到預設值上，請嘗試清空 `mygame/server/.static/` 並重新執行 `evennia collectstatic`。

(changing-the-front-pages-text)=
## 更改首頁的文字

Evennia 的預設首頁包含有關 Evennia 專案的資訊。您可能希望用有關您自己的專案的資訊替換此資訊。更改頁面模板的方式與更改靜態資源類似。

與靜態檔案一樣，Django 會遍歷一系列模板資料夾來尋找它想要的檔案。不同之處在於 Django 不會將所有模板檔案複製到一個位置，它只是搜尋模板資料夾，直到找到與其要尋找的內容相符的模板。這意味著當您編輯範本時，更改是即時的。您不必重新載入伺服器或執行任何額外的指令來檢視這些變更 - 在瀏覽器中重新載入網頁就足夠了。

要替換索引頁的文字，我們需要找到它的範本。我們將在[基於Web的字元檢視教學](./Web-Character-View-Tutorial.md)中更詳細地介紹如何確定使用哪個範本來渲染頁面。現在，您應該知道我們要更改的模板儲存在`evennia/web/website/templates/website/index.html`中。

要替換此模板檔案，您需要將更改後的模板放入 `mygame/web/templates/` 中。與靜態資源一樣，您必須使用複製與主庫中相同的資料夾結構。例如，要覆蓋 `evennia/web/templates/website/index.html` 中找到的主 `index.html` 檔案，請將其複製 `mygame/web/templates/website/index.html` 並根據需要進行自訂。只需重新載入伺服器即可檢視新版本。

(further-reading)=
## 進一步閱讀

有關使用網路存在的更多提示，您現在可以繼續學習[基於網路的角色檢視教學](./Web-Character-View-Tutorial.md)，您可以在其中學習製作一個顯示遊戲中角色統計資料的網頁。您也可以檢視[Django 自己的教學](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) 以更深入地瞭解 Django 的工作原理以及有哪些可能性。