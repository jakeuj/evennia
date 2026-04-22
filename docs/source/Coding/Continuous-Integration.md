(continuous-integration-ci)=
# 持續整合（CI）

[持續整合(CI)](https://en.wikipedia.org/wiki/Continuous_integration)是一種開發實踐，要求開發人員將程式碼整合到共享儲存庫中。然後，每次簽入都會透過自動建置進行驗證，使團隊能夠及早發現問題。例如，可以將其設定為僅在測試透過後才將資料安全地部署到生產伺服器。

對於Evennia，持續整合允許自動化建置流程：

* 從原始碼管理下載最新版本。
* 在支援 SQL 資料庫上執行遷移。
* 自動化該專案的其他獨特任務。
* 執行單元測試。
* 將這些檔案釋出到伺服器目錄
* 重新載入遊戲。

(continuous-integration-guides)=
## 持續整合指南

Evennia 本身大量使用了 [github actions](https://github.com/features/actions)。它與 Github 整合，可能是大多數人的首選，尤其是如果您的程式碼已經在 Github 上的話。您可以在[此處](https://github.com/evennia/evennia/actions)檢視並分析Evennia的操作如何運作。

然而，有許多工具和服務提供CI 功能。   [這裡是部落格概述](https://www.atlassian.com/continuous-delivery/continuous-integration/tools)（外部連結）。