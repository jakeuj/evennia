(menu-based-login-system)=
# 基於選單的登入系統

Vincent-lg 2016 年貢獻。 Griatch 2019 年重新設計現代 EvMenu。

這將Evennia登入更改為要求輸入帳戶名稱和密碼作為一系列
問題，而不是要求您同時輸入兩個問題。它使用Evennia的
選單系統 `EvMenu` 在引擎蓋下。

(installation)=
## 安裝

要安裝，請將其新增到 `mygame/server/conf/settings.py`：

    CMDSET_UNLOGGEDIN = "evennia.contrib.base_systems.menu_login.UnloggedinCmdSet"
    CONNECTION_SCREEN_MODULE = "evennia.contrib.base_systems.menu_login.connection_screens"

重新載入伺服器並重新連線以檢視變更。

(notes)=
## 筆記

如果您想要修改連線螢幕的外觀，請指向
`CONNECTION_SCREEN_MODULE` 到您自己的模組。使用預設值作為
指南（另請參閱 Evennia 檔案）。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\menu_login\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
