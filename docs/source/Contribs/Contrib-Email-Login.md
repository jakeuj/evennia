(email-based-login-system)=
# 基於電子郵件的登入系統

Contrib，格里奇，2012

這是登入系統的變體，要求提供電子郵件地址
而不是使用者名稱來登入。請注意，它不會驗證電子郵件，
它只是將其用作識別符號而不是使用者名稱。

這曾經是預設的 Evennia 登入名，然後將其替換為
更標準的使用者名稱+密碼系統（必須提供電子郵件
由於某種原因，當人們想要擴充套件時引起了很多混亂
在它上面。該電子郵件並不是內部嚴格需要的，也不是任何內部都需要的。
無論如何，確認電子郵件已發出）。

(installation)=
## 安裝

在您的設定檔中，新增/編輯以下行：

```python
CMDSET_UNLOGGEDIN = "contrib.base_systems.email_login.UnloggedinCmdSet"
CONNECTION_SCREEN_MODULE = "contrib.base_systems.email_login.connection_screens"

```

就是這樣。重新載入伺服器並重新連線即可檢視。

(notes)=
## 筆記：

如果您想要修改連線螢幕的外觀，請指向
`CONNECTION_SCREEN_MODULE` 到您自己的模組。使用預設值作為
指南（另請參閱 Evennia 檔案）。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\email_login\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
