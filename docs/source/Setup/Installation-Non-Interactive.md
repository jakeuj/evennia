(non-interactive-setup)=
# 非互動式設定

第一次執行`evennia start`（建立資料庫後）時，系統會詢問您
以互動方式插入超級使用者使用者名稱、電子郵件和密碼。如果您正在部署 Evennia
作為自動建置 script 的一部分，您不想手動輸入此資訊。

您可以透過將環境變數傳遞給您的系統來自動建立超級使用者
構建script：

- `EVENNIA_SUPERUSER_USERNAME`
- `EVENNIA_SUPERUSER_PASSWORD`
- `EVENNIA_SUPERUSER_EMAIL` 是可選的。如果未給出，則使用空字串。
 
這些環境變數只會在_第一次_伺服器啟動時使用，然後被忽略。例如：

```
EVENNIA_SUPERUSER_USERNAME=myname EVENNIA_SUPERUSER_PASSWORD=mypwd evennia start
```