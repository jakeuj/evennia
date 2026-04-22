(choosing-a-database)=
# 選擇資料庫


本頁概述了受支援的 SQL 資料庫以及安裝說明：

 - SQLite3（預設）
 - PostgreSQL
 - MySQL / MariaDB

由於 Evennia 使用 [Django](https://djangoproject.com)，我們的大部分註釋都是基於我們從社群及其檔案中瞭解到的資訊。雖然下面的資訊可能有用，但您始終可以在 Django 的[有關支援的資料庫的註釋](https://docs.djangoproject.com/en/4.1/ref/databases/#ref-databases) 頁面找到最新且「正確」的資訊。

(sqlite3-default)=
## SQLite3（預設）

[SQLite3](https://sqlite.org/) 是一個輕量級單一檔案資料庫。這是我們的預設資料庫，如果您沒有提供其他選項，Evennia 會自動為您設定。

SQLite 將資料庫儲存在單一檔案中 (`mygame/server/evennia.db3`)。這意味著重置此資料庫非常容易 - 只需刪除（或移動）該 `evennia.db3` 檔案並再次執行 `evennia migrate` 即可！不需要伺服器程式，管理開銷和資源消耗很小。由於它在記憶體中執行，因此速度也非常快。對於絕大多數 Evennia 安裝來說，它可能就是所需要的。

SQLite 通常比 MySQL/PostgreSQL 快得多，但其效能有兩個缺點：

* SQLite [忽略設計的長度限制](https://www.sqlite.org/faq.html#q9);可以在技術上不應該接受的欄位中儲存非常大的字串和數字。這不是你會注意到的事情；您的遊戲將讀取和寫入它們並正常執行，但這*可能*會產生一些資料遷移問題，如果您以後確實需要更改資料庫，則需要仔細考慮。
* SQLite 可以很好地擴充套件到儲存數百萬個物件，但是如果您最終遇到一大群使用者試圖同時訪問您的 MUD 和網站，或者您發現自己編寫了長時間執行的函式來更新實時遊戲中的大量物件，那麼這兩種情況都會產生錯誤和乾擾。 SQLite 無法在多個並發執行緒或程式存取其記錄的情況下可靠地工作。這與資料庫檔案的檔案鎖定衝突有關。因此，對於大量使用程式池或執行緒池的生產伺服器來說，合適的資料庫是更合適的選擇。

(install-of-sqlite3)=
### 安裝SQlite3

它作為 Evennia 的一部分進行安裝和設定。執行時資料庫檔案被建立為`mygame/server/evennia.db3`

    evennia migrate

無需更改任何資料庫選項。一個可選的要求是 `sqlite3` 客戶端程式 - 如果您想手動檢查資料庫資料，則這是必需的。將其與 evennia 資料庫一起使用的快捷方式是 `evennia dbshell`。 Linux 使用者應為其發行版尋找 `sqlite3` 軟體包，而 Mac/Windows 則應從本頁取得 [sqlite-tools 軟體包](https://sqlite.org/download.html)。

若要檢查預設的 Evennia 資料庫（建立後），請前往您的遊戲目錄並執行下列操作

```bash
    sqlite3 server/evennia.db3
    # or
    evennia dbshell
```

這將帶您進入 sqlite 指令列。使用 `.help` 進行指示，使用 `.quit` 退出。
有關指令備忘單，請參閱[此處](https://gist.github.com/vincent178/10889334)。

(resetting-sqlite3)=
### 正在重置SQLite3

如果您想重設 SQLite3 資料庫，請參閱[此處](./Updating-Evennia.md#sqlite3-default)。

(postgresql)=
## PostgreSQL

[PostgreSQL](https://www.postgresql.org/)是Django推薦的開源資料庫引擎。雖然正常使用情況下速度不如 SQLite，但其擴充套件性會比 SQLite 更好，特別是如果您的遊戲透過單獨的伺服器程式擁有非常大的資料庫和/或廣泛的 Web 存在。

(install-and-initial-setup-of-postgresql)=
### 安裝並初始設定 PostgreSQL

首先，安裝 posgresql 伺服器。版本 `9.6` 使用 Evennia 進行測試。所有發行版均可輕鬆獲得軟體包。您還需要取得 `psql` 客戶端（在 debian 衍生系統上稱為 `postgresql- client`）。 Windows/Mac使用者可以[在postgresql下載頁面找到他們需要的東西](https://www.postgresql.org/download/)。安裝時，您應該為資料庫超級使用者（始終稱為 `postgres`）設定密碼。

為了與 Evennia 互動，您還需要將 `psycopg` (psycopg3) 安裝到您的 Evennia 安裝中（virtualenv 中的 `pip install psycopg[binary]`）。這充當到資料庫伺服器的 python 橋。

接下來，啟動 postgres 客戶端：

```bash
    psql -U postgres --password
```

```{warning}

使用 `--password` 引數，Postgres 應該會提示您輸入密碼。如果不是，請將其替換為 `-p yourpassword`。除非必要，否則請勿使用 `-p` 引數，因為產生的指令和您的密碼將記錄在 shell 歷史記錄中。
```

這將使用 psql 客戶端開啟 postgres 服務的控制檯。

在 psql 指令列上：

```sql
CREATE USER evennia WITH PASSWORD 'somepassword';
CREATE DATABASE evennia;

-- Postgres-specific optimizations
-- https://docs.djangoproject.com/en/dev/ref/databases/#optimizing-postgresql-s-configuration
ALTER ROLE evennia SET client_encoding TO 'utf8';
ALTER ROLE evennia SET default_transaction_isolation TO 'read committed';
ALTER ROLE evennia SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE evennia TO evennia;
-- For Postgres 10+
ALTER DATABASE evennia owner to evennia;

-- Other useful commands:
--  \l       (list all databases and permissions)
--  \q       (exit)

```
[此處](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546) 是 psql 指令的備忘單。

我們建立一個資料庫使用者「evennia」和一個名為`evennia` 的新資料庫（您可以隨意稱呼它們）。然後，我們授予「evennia」使用者對新資料庫的完全許可權，以便它可以對其進行讀取/寫入等操作。如果您將來想要完全擦除資料庫，一個簡單的方法是再次以 `postgres` 超級使用者身份登入，然後執行 `DROP DATABASE evennia;`，然後再次執行上述 `CREATE` 和 `GRANT` 步驟來重新建立資料庫並授予許可權。

(evennia-postgresql-configuration)=
### Evennia PostgreSQL 設定

編輯 `mygame/server/conf/secret_settings.py` 並新增以下部分：

```python
#
# PostgreSQL Database Configuration
#
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'evennia',
            'USER': 'evennia',
            'PASSWORD': 'somepassword',
            'HOST': 'localhost',
            'PORT': ''    # use default
        }}
```

如果您對資料庫和使用者使用了其他名稱，請輸入這些名稱。跑步

    evennia migrate

填充您的資料庫。如果您想直接檢查資料庫，從現在開始也可以使用

    evennia dbshell

作為進入正確資料庫和使用者的 postgres 指令列的捷徑。

透過資料庫設定，您現在應該能夠正常啟動新資料庫的 Evennia。

(resetting-postgresql)=
### 正在重置PostgreSQL

如果您想重設 PostgreSQL 資料庫，請參閱[此處](./Updating-Evennia.md#postgresql)

(advanced-postgresql-usage-remote-server)=
### 進階 PostgreSQL 使用情況（遠端伺服器）

```{warning}

以下的範例適用於未開放的專用網路中的伺服器
  網際網路。  在進行任何更改之前，請務必瞭解詳細資訊
  可存取 Internet 的伺服器。
```

上面的討論是針對託管本地伺服器的。在某些設定中，將資料庫託管在遠離執行 Evennia 的伺服器上可能是有意義的。一個範例是多個使用者可以在多臺機器上完成程式碼開發。在此設定中，本機資料庫（例如SQLite3）不可行，因為所有電腦和開發人員都無法存取該檔案。

選擇一臺遠端電腦來託管資料庫和 PostgreSQl 伺服器。依照該伺服器上的[上述](#install-and-initial-setup-of-postgresql) 說明設定資料庫。根據發行版的不同，PostgreSQL 將僅接受本機電腦 (localhost) 上的連線。  為了啟用遠端訪問，需要更改兩個檔案。

首先，確定哪個叢集正在執行您的資料庫。使用`pg_lscluster`：

```bash
$ pg_lsclusters
Ver Cluster Port Status Owner    Data directory              Log file
12  main    5432 online postgres /var/lib/postgresql/12/main /var/log/postgresql/postgresql-12-main.log
```

接下來，編輯資料庫的`postgresql.conf`。  這可以在 Ubuntu 系統的 `/etc/postgresql/<ver>/<cluster>` 中找到，其中 `<ver>` 和 `<cluster>` 是 `pg_lscluster` 輸出中報告的內容。  因此，對於上面的範例，檔案是`/etc/postgresql/12/main/postgresql.conf`。

在此檔案中，尋找帶有 `listen_addresses` 的行。  例如：

```
listen_address = 'localhost'    # What IP address(es) to listen on;
                                # comma-separated list of addresses;
                                # defaults to 'localhost'; use '*' for all
```

```{warning}
錯誤設定錯誤的叢集可能會導致問題
  與現有叢集。
```

另外，請記下帶有 `port =` 的行並記住連線埠號碼。

將 `listen_addresses` 設定為 `'*'`。  這允許 postgresql 接受連線
在任何介面上。

```{warning}
將 `listen_addresses` 設定為 `'*'` 將在所有介面上開啟一個連線埠。  如果你的
  伺服器可以存取網際網路，確保您的防火牆已設定
  根據需要適當限制對此連線埠的存取。  （您也可以列出
  要偵聽的明確位址和子網路。  請參閱 postgresql 文件
  瞭解更多詳情。）
```

最後修改`pg_hba.conf`（與`postgresql.conf`同目錄）。尋找包含以下內容的行：
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
```
新增一行：
```
host    all             all             0.0.0.0/0               md5
```

```{warning}
這允許來自*所有* IP 的傳入連線。  參見
  有關如何限制此行為的 PosgreSQL 檔案。
```

現在，重新啟動叢集：
```bash
$ pg_ctlcluster 12 main restart
```

最後，更新 Evennia secret_settings.py 中的資料庫設定（如上所述）(#evennia-postgresql-configuration)，修改 `SERVER` 和 `PORT` 以符合您的伺服器。

現在您的 Evennia 安裝應該能夠連線遠端伺服器並與其通訊。

(mysql-mariadb)=
## MySQL / MariaDB

[MySQL](https://www.mysql.com/) 是常用的專有資料庫系統，與PostgreSQL 同等。有一個名為 [MariaDB](https://mariadb.org/) 的開源替代方案，它模仿了前者的所有功能和指令語法。所以本節涵蓋了兩者。

(installing-and-initial-setup-of-mysqlmariadb)=
### MySQL/MariaDB 的安裝和初始設定

首先，為您的特定伺服器安裝並設定 MariaDB 或 MySQL。 Linux 使用者應尋找各自發行版的 `mysql-server` 或 `mariadb-server` 軟體套件。 Windows/Mac 使用者可以從 [MySQL 下載](https://www.mysql.com/downloads/) 或 [MariaDB 下載](https://mariadb.org/download/) 頁面找到他們需要的內容。您還需要相應的資料庫使用者端（`mysql`、`mariadb-client`），以便您可以設定資料庫本身。當您安裝伺服器時，通常會要求您設定資料庫 root 使用者和密碼。

最後，您還需要一個 Python 介面來允許 Evennia 與資料庫對話。 Django 推薦`mysqlclient` 之一。使用 `pip install mysqlclient` 將其安裝到 evennia virtualenv 中。

啟動資料庫客戶端（mysql 和 mariadb 的名稱相同）：

```bash
mysql -u root -p
```

您應該輸入資料庫根密碼（在安裝資料庫伺服器時設定）。

資料庫客戶端介面內部：

```sql
CREATE USER 'evennia'@'localhost' IDENTIFIED BY 'somepassword';
CREATE DATABASE evennia;
ALTER DATABASE `evennia` CHARACTER SET utf8; -- note that it's `evennia` with back-ticks, not
quotes!
GRANT ALL PRIVILEGES ON evennia.* TO 'evennia'@'localhost';
FLUSH PRIVILEGES;
-- use 'exit' to quit client
```
[這裡](https://gist.github.com/hofmannsven/9164408) 是 mysql 指令備忘單。

上面我們建立了一個新的本地使用者和資料庫（我們在這裡將它們命名為“evennia”，您可以將它們命名為您喜歡的名稱）。我們將字元集設定為 `utf8` 以避免在某些安裝中可能出現的字首字元長度問題。接下來，我們授予「evennia」使用者對 `evennia` 資料庫的所有許可權，並確保應用這些許可權。退出客戶端使我們回到正常的終端機/控制檯。

> 如果您沒有將 MySQL 用於其他用途，您可以考慮使用 `GRANT ALL PRIVILEGES ON *.* TO 'evennia'@'localhost';` 授予「evennia」使用者完全許可權。如果這樣做，這意味著您可以稍後使用 `evennia dbshell` 連線到 mysql，刪除資料庫並重新建立它作為輕鬆重置的方式。如果沒有這個額外的許可權，您將能夠刪除資料庫，但在不先切換到資料庫根使用者的情況下無法重新建立它。

(add-mysqlmariadb-configuration-to-evennia)=
### 將 MySQL/MariaDB 設定新增至 Evennia

要告訴 Evennia 使用您的新資料庫，您需要編輯 `mygame/server/conf/settings.py` （如果您不希望您的資料庫資訊在 git 儲存庫上傳遞，則編輯 `secret_settings.py`）。

> Django 檔案建議使用外部 `db.cnf` 或其他外部設定檔。然而，Evennia 使用者發現這會導致問題（請參閱 e.g。[問題 #1184](https://git.io/vQdiN)）。為了避免麻煩，我們建議您只需將設定放入您的設定中，如下所示。

```python
    #
    # MySQL Database Configuration
    #
    DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'evennia',
           'USER': 'evennia',
           'PASSWORD': 'somepassword',
           'HOST': 'localhost',  # or an IP Address that your DB is hosted on
           'PORT': '', # use default port
       }
    }
```
`mysql` 後端也由 `MariaDB` 使用。

更改此設定以適合您的資料庫設定。接下來，執行：

    evennia migrate
    
填充您的資料庫。如果您想直接檢查資料庫，從現在開始也可以使用
 
    evennia dbshell

作為進入正確資料庫和使用者的 postgres 指令列的捷徑。

透過資料庫設定，您現在應該能夠正常啟動新資料庫的 Evennia。

(resetting-mysqlmariadb)=
### 正在重置MySQL/MariaDB

如果您想重設 MySQL/MariaDB 資料庫，請參閱[此處](./Updating-Evennia.md#mysql-mariadb)。

(other-databases)=
## 其他資料庫

尚未使用 Oracle 進行測試，但也透過 Django 支援。有 [MS SQL](https://code.google.com/p/django-mssql/) 以及可能還有其他一些社群維護的驅動程式。如果您嘗試其他資料庫，請考慮為此頁面提供說明。