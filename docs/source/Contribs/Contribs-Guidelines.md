(guidelines-for-evennia-contribs)=
# Evennia contribs 的準則

Evennia 有一個 [contrib](./Contribs-Overview.md) 目錄，其中包含按類別組織的可選社群共享程式碼。歡迎任何人做出貢獻。

(what-is-suitable-for-a-contrib)=
## 什麼適合contrib？

- 一般來說，您可以貢獻任何您認為可能對其他開發人員有用的內容。與「核心」Evennia 不同，contribs 也可以是高度特定於遊戲型別的。
- 非常小的或不完整的程式碼片段（e.g。旨在貼到其他程式碼中）最好在 [社群 Contribs 和程式碼片段](https://github.com/evennia/evennia/discussions/2488) 討論論壇類別中作為帖子進行分享。
- 如果您的程式碼「主要」是作為範例或展示概念/原理而不是工作系統，請考慮是否透過編寫新教學或指南來[為檔案做出貢獻](../Contributing-Docs.md)更好。
- 如果可能的話，盡量讓你的貢獻與型別無關，並假設
您的程式碼將應用於與您建立時所設想的完全不同的遊戲。
- 該貢獻最好應該與其他 contribs 隔離工作（僅使用核心 Evennia），以便可以輕鬆投入使用。如果它確實依賴其他contribs或第三方模組，則必須清楚記錄這些模組並將其作為安裝說明的一部分。
- 如果您不確定您的 contrib 想法是否合適或合理，*請在投入任何工作之前透過討論或聊天進行詢問*。例如，我們不太可能接受需要對遊戲目錄結構進行大量修改的contribs。

(layout-of-a-contrib)=
## contrib 的佈局

- contrib 必須僅包含在以下 contrib 類別之一下的單一資料夾中。  詢問您是否不確定哪個類別最適合您的contrib。

|  |  | 
| --- | --- | 
| `base_systems/` | _系統不一定與特定的遊戲機制相關，但對整個遊戲有用。範例包括登入系統、新指令語法和建置 helpers._ |
| `full_systems/` | _「完整」的遊戲引擎，可以直接用於開始建立內容，無需進一步新增（除非您願意）。 _ |
| `game_systems/` | _遊戲內的遊戲系統，如製作、郵件、戰鬥等等。每個系統都應該逐步採用並用於您的遊戲。這不包括特定於角色扮演的系統，這些系統可在 `rpg` category._ 中找到 |
| `grid/` | _與遊戲世界的拓樸和結構相關的系統。 Contribs與房間、出口和地圖相關building._ |
| `rpg/` | _專門與角色扮演和規則實施相關的系統，例如角色特徵、擲骰子和emoting._ | 
| `tutorials/` | _幫助資源專門用於教授開發概念或舉例說明 Evennia 系統。與檔案教學相關的任何額外資源都可以在此處找到。也是教學世界和 Evadventure 演示 codes._ 的所在地 | 
| `utils/` | _用於操作文字、安全審核和more._的各種工具|


- 資料夾（包）應採用以下形式：

    ```
    evennia/
       contrib/ 
           category/    # rpg/, game_systems/ etc
               mycontribname/
                   __init__.py
                   README.md
                   module1.py
                   module2.py
                   ...
                   tests.py
    ```

    It's often a good idea to import useful resources in `__init__.py` to make it easier to import them.
- 您的程式碼應遵守 [Evennia 樣式指南](../Coding/Evennia-Code-Style.md)。寫得容易閱讀。
- 您的貢獻_必須_包含在[單元測試](../Coding/Unit-Testing.md) 中。將您的測試放在 contrib 資料夾下的模組 `tests.py` 中（如上所示） - Evennia 將自動找到它們。如果多個模組中有許多測試，請使用資料夾 `tests/` 對測試進行分組。
-  `README.md` 檔案將被解析並轉換為從 [contrib 概述頁面](./Contribs-Overview.md) 連結的檔案。它需要採用以下形式：

    ```markdown
    # MyContribName

    Contribution by <yourname>, <year>

    A paragraph (can be multi-line)
    summarizing the contrib (required)

    Optional other text

    ## Installation

    Detailed installation instructions for using the contrib (required)

    ## Usage

    ## Examples

    etc.

    ```

> 致謝資訊和第一段摘要將自動包含在每個貢獻的 Contrib 概述頁面索引中，因此只需在此表單上。


(submitting-a-contrib)=
## 正在提交contrib

```{sidebar} 並非所有 PR 都能被接受
雖然大多數 PR 都會合併，但這並不能保證：合併 contrib 意味著 Evennia 專案承擔維護和支援新程式碼的責任。由於各種原因，這可能被認為是不可行的。

如果您的程式碼因某種原因*不*被接受，我們仍然可以從我們的連結頁面連結它；它也可以釋出在我們的論壇中。
```
- contrib 必須始終[作為拉取請求](../Coding/Version-Control.md#contributing-to-evennia) (PR) 呈現。
- PR 會經過審核，因此如果您在合併之前被要求修改或更改程式碼，請不要感到驚訝（或沮喪）。您的程式碼在被接受之前最終可能會經歷多次迭代。
- 為了使許可情況清晰，我們假設所有貢獻都使用相同的[許可為Evennia](../Licensing.md)發布。如果由於某種原因無法做到這一點，請與我們聯絡，我們將根據具體情況進行處理。
