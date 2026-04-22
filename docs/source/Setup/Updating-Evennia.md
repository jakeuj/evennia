(updating-evennia)=
# 正在更新Evennia

當Evennia更新到新版本時，您通常會在[討論論壇](github:discussions)和[開發部落格](https://www.evennia.com/devblog/index.html)中看到它的公告。您也可以在 [github](github:) 上或透過我們的其他[連結頁面](../Links.md) 之一檢視變更。

(if-you-installed-with-pip)=
## 如果您安裝了`pip`

如果您按照[正常安裝說明](./Installation.md) 進行操作，則升級步驟如下：

1. 閱讀[變更日誌](../Coding/Changelog.md) 以瞭解發生了什麼變化以及這是否意味著您需要對遊戲程式碼進行任何更改。
2. 如果您使用 [virtualenv](#Installation-Git#virtualenv)，請確保它處於活動狀態。
3. `cd` 到您的遊戲目錄 (e.g。`mygame`)
4. `evennia stop`
5. `pip install --upgrade evennia`
6. `cd` 到你的遊戲目錄
7. `evennia migrate` - 這樣做是安全的，但可以跳過，除非釋出公告/變更日誌明確告訴您這樣做。 _忽略_任何關於執行 `makemigrations` 的警告，它不應該_完成！
8. `evennia start`

(if-you-installed-with-git)=
## 如果您安裝了`git`

如果您遵循 [git-install 說明](./Installation-Git.md)，則適用。在 Evennia 1.0 之前，這是安裝 Evennia 的唯一方法。

在任何時候，開發要麼發生在 `main` 分支（最新穩定版）中，要麼發生在 `develop`（實驗版）中。哪一個在給定時間處於活動狀態且「最新」取決於 - 發布後，`main` 將看到最多更新，接近新版本時，`develop` 通常將是變化最快的。

1. 閱讀[變更日誌](../Coding/Changelog.md) 以瞭解發生了什麼變化以及這是否意味著您需要對遊戲程式碼進行任何更改。
2. 如果您使用 [virtualenv](#Installation-Git#virtualenv)，請確保它處於活動狀態。
3. `cd` 到您的遊戲目錄 (e.g。`mygame`)
4. `evennia stop`
5. `cd` 到您在 git 安裝過程中克隆的 `evennia` repo 資料夾。
6. `git pull`
7. `pip install --upgrade -e.`（記得最後的`.`！）
9. `cd`回到你的遊戲目錄
10. `evennia migrate` - 這樣做是安全的，但可以跳過，除非釋出公告/變更日誌明確告訴您這樣做。 _忽略_任何關於執行 `makemigrations` 的警告，它不應該_完成！
11. `evennia start`

(if-you-installed-with-docker)=
## 如果您安裝了`docker`

如果您按照[docker安裝說明](./Installation-Docker.md)，您需要為您想要的分支拉取最新的docker映像：

- `docker pull evennia/evennia`（`main`分支）
- `docker pull evennia/evennia:develop`（實驗`develop`分支）

然後重新啟動容器。

(resetting-your-database)=
## 重置您的資料庫

如果您想完全從頭開始，則無需重新下載Evennia。您只需要清除資料庫。

第一的：

1.  `cd` 到您的遊戲目錄 (e.g。`mygame`)
2.  `evennia stop`

(sqlite3-default)=
### SQLite3（預設）

```{sidebar} 暗示
建立超級使用者後，請複製 `evennia.db3` 檔案。當您想要重設時（只要不必執行任何新的遷移），您只需停止 evennia 並將該檔案複製回 `evennia.db3` 即可。這樣您就不必每次都執行相同的遷移並建立超級使用者！
```

3. 刪除檔案`mygame/server/evennia.db3`
4. `evennia migrate`
5. `evennia start`

(postgresql)=
### PostgreSQL

3. `evennia dbshell`（開啟psql客戶端介面）
    ```
    psql> DROP DATABASE evennia;
    psql> exit
    ```
 4. 現在您應該按照 [PostgreSQL 安裝說明](./Choosing-a-Database.md#postgresql) 建立新的 evennia 資料庫。
 5. `evennia migrate`
 6. `evennia start`

(mysqlmariadb)=
### MySQL/MariaDB

3. `evennia dbshell`（開啟mysql客戶端介面）
````
   mysql>DROP1evennia；
   mysql> 退出
   ````
4. 現在您應該按照 [MySQL 安裝說明](./Choosing-a-Database.md#mysql-mariadb) 建立新的 evennia 資料庫。
5. `evennia migrate`
6. `evennia start`

(what-are-database-migrations)=
### 什麼是資料庫遷移？

如果Evennia更新修改了資料庫*架構*（即有關資料如何儲存在資料庫中的底層詳細資訊），您必須相應地更新現有資料庫以符合變更。如果不這樣做，更新後的 Evennia 將抱怨無法正確讀取資料庫。儘管隨著 Evennia 的成熟，模式變更應該變得越來越罕見，但它仍然可能不時發生。

處理此問題的一種方法是使用資料庫的指令列將變更手動套用到資料庫。這通常意味著新增/刪除新表或欄位，以及可能轉換現有資料以匹配新 Evennia 版本所期望的內容。很明顯，這很快就會變得麻煩且容易出錯。  如果您的資料庫不包含任何關鍵內容，那麼最簡單的方法可能是簡單地重置它並重新開始，而不是費心進行轉換。

輸入*遷移*。遷移會追蹤資料庫架構中的變更並自動為您套用它們。基本上，每當模式發生變化時，我們都會隨來源一起分發稱為「遷移」的小檔案。它們準確地告訴系統如何實施更改，因此您不必手動執行此操作。新增遷移後，我們會在 Evennia 的郵件清單和提交訊息中告訴您 - 然後您只需執行 `evennia migrate` 即可再次獲得最新狀態。
