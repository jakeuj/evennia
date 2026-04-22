(installing-with-docker)=
# 使用 Docker 安裝

Evennia 發布 [docker 映像](https://hub.docker.com/r/evennia/evennia/) 作為常規提交和發布的一部分。這使得在 Docker 容器中執行基於 Evennia 的遊戲變得容易。

首先，安裝 `docker` 程式，以便可以執行 Evennia 容器。您可以從[docker.com](https://www.docker.com/)免費獲得它。 Linux 使用者也可以透過普通的套件管理器來取得它。

若要取得最新的 evennia docker 映像，請執行：

    docker pull evennia/evennia

這將獲得最新的穩定影像。

    docker pull evennia/evennia:develop 

取得基於 Evennia 的不穩定 `develop` 分支的影像。

接下來，`cd` 到您的遊戲目錄所在的位置，或您想要建立它的位置。然後執行：

```bash
docker run -it --rm -p 4000:4000 -p 4001:4001 -p 4002:4002 --rm -v $PWD:/usr/src/game --user $UID:$GID evennia/evennia
```

執行此指令後（請參閱下一節以瞭解具體內容），您將看到內部提示
碼頭貨櫃：

```bash
evennia|docker /usr/src/game $
```

這是一個正常的 shell 提示字元。我們位於 docker 容器內的 `/usr/src/game` 位置。如果您開始的資料夾中有任何內容，您應該在這裡看到它（帶有 `ls`），因為我們將當前目錄安裝到 `usr/src/game`（上面帶有 `-v`）。您可以使用 `evennia` 指令，現在可以按照正常的 [遊戲設定](./Installation.md) 說明繼續建立新遊戲（不需要 virtualenv）。

如果你願意的話，你可以從這個容器內執行Evennia，就像你是一個小東西的root一樣
隔離的Linux環境。若要退出容器及其中的所有程式，請按 `Ctrl-D`。如果你
建立一個新的遊戲資料夾，你會發現它已經出現在磁碟上。

> 遊戲資料夾或您在容器內建立的任何新檔案將顯示為`root` 所有。如果您想編輯容器外部的檔案，您應該更改所有權。在 Linux/Mac 上，您可以使用 `sudo chown myname:myname -R mygame` 執行此操作，其中將 `myname` 替換為您的使用者名稱，將 `mygame` 替換為遊戲資料夾的名稱。

以下是我們使用的 `docker run` 指令的解釋：

- `docker run... evennia/evennia` 告訴我們要基於 `evennia/evennia` docker 映像執行一個新容器。介於兩者之間的所有內容都是此目的的選擇。 `evennia/evennia` 是我們的[dockerhub 儲存庫上的官方 docker 映像](https://hub.docker.com/r/evennia/evennia/) 的名稱。如果您沒有先執行`docker pull evennia/evennia`，則執行此指令時將下載映像，否則將使用您已下載的版本。它包含執行 Evennia 所需的一切。
- `-it` 與在我們啟動的容器內建立互動式 session 有關。
- `--rm` 將確保在關閉時刪除容器。保持東西整潔很好
在你的驅動器上。
- `-p 4000:4000 -p 4001:4001 -p 4002:4002` 表示我們將 docker 容器內部的連線埠 `4000`、`4001` 和 `4002` *對映* 到主機上相同編號的連線埠。這些是 telnet、webserver 和 websockets 的連線埠。這就是允許從容器外部存取您的 Evennia 伺服器（例如透過您的 MUD 使用者端）！
- `-v $PWD:/usr/src/game` 將目前目錄（容器*外部*）安裝到容器*內部*路徑`/usr/src/game`。這表示當您在容器中編輯該路徑時，您實際上將修改硬碟上的「真實」位置。如果您不這樣做，任何變更只會存在於容器內部，如果我們建立新容器，則這些變更將消失。請注意，在 Linux 中，目前目錄的捷徑是 `$PWD`。如果您的 OS 沒有這個，您可以將其替換為當前磁碟目錄的完整路徑（例如 `C:/Development/evennia/game` 或您希望 evennia 檔案出現的任何位置）。
- `--user $UID:$GID` 確保容器對 `$PWD` 的修改是使用您的使用者和群組 ID 而不是 root 的 ID 完成的（root 是在容器內執行 evennia 的使用者）。這可以避免容器重新啟動之間的檔案系統中出現陳舊的 `.pid` 檔案，您必須在每次啟動之前使用 `sudo rm server/*.pid` 強制刪除這些檔案。

(running-your-game-as-a-docker-image)=
## 作為 docker 映像執行你的遊戲

如果您從遊戲目錄執行上一節中給出的 `docker` 指令，您就可以輕鬆啟動 Evennia 並擁有一個正在執行的伺服器，而無需任何進一步的麻煩。

但除了易於安裝之外，在容器中執行基於 Evennia 的遊戲的主要好處是簡化其在公共生產環境中的部署。大多數基於雲端的託管
如今，提供者支援執行基於容器的應用程式的能力。這使得部署
或者更新您的遊戲，就像在本地建立新的容器映像一樣簡單，將其推送到您的 Docker Hub 帳戶，然後從 Docker Hub 拉取到您的 AWS/Azure/其他支援 docker 的託管帳戶。該容器無需安裝 Python、設定 virtualenv 或執行 pip 來安裝依賴項。

(start-evennia-and-run-through-docker)=
### 啟動Evennia並透過docker執行

對於遠端或自動部署，您可能希望在 docker 容器啟動後立即啟動 Evennia。如果您已經有一個設定了資料庫的遊戲資料夾，您也可以啟動 docker 容器並將指令直接傳遞給它。您傳遞的指令將是在容器中執行的主程式。例如，從您的遊戲目錄執行以下指令：

    docker run -it --rm -p 4000:4000 -p 4001:4001 -p 4002:4002 --rm -v $PWD:/usr/src/game evennia/evennia evennia start -l

這將啟動 Evennia 作為前臺程式，將日誌回顯到終端。關閉
終端將終止伺服器。請注意，您*必須*使用像 `evennia start -l` 這樣的前臺指令
或 `evennia ipstart` 啟動伺服器 - 否則前臺程式將立即完成
然後容器就會下降。

(create-your-own-game-image)=
## 建立您自己的遊戲影象

這些步驟假設您已經建立或以其他方式取得了遊戲目錄。首先，`cd` 到您的遊戲目錄並建立一個名為 `Dockerfile` 的新空文字檔案。將以下兩行儲存到其中：

```
FROM evennia/evennia:latest

ENTRYPOINT evennia start -l
```

這些是建置新 docker 映像的說明。這個是根據官方的
`evennia/evennia` 影像，但也確保在執行時啟動 evennia （所以我們不需要
輸入它並執行指令）。

建構影象：

```bash
    docker build -t mydhaccount/mygame .
```

（不要忘記末尾的句點，它將使用當前位置的`Dockerfile`）。這裡 `mydhaccount` 是您 `dockerhub` 帳戶的名稱。如果您沒有 dockerhub 帳戶，則只能在本機建置映像（在這種情況下，將容器命名為您喜歡的任何名稱，例如 `mygame`）。

Docker 映像集中儲存在您的電腦上。您可以使用 `docker images` 檢視本地可用的內容。建置完成後，您有幾個選項來執行遊戲。

(run-container-from-your-game-image-for-development)=
### 從您的遊戲映像執行容器以進行開發

要在本地執行基於您的遊戲映象的容器進行開發，請像以前一樣掛載本地遊戲目錄：

```
docker run -it --rm -p 4000:4000 -p 4001:4001 -p 4002:4002 -v $PWD:/usr/src/game --user $UID:$GID
mydhaccount/mygame
```

Evennia 將啟動，您將在終端中獲得輸出，非常適合開發。你應該是
能夠與客戶端正常連線遊戲。

(deploy-game-image-for-production)=
### 部署遊戲映象進行生產

每次您按照上述說明重建 docker 映像時，都會獲得遊戲的最新副本
目錄實際上被複製到影象內部（位於`/usr/src/game/`）。如果您沒有掛載到磁碟上
資料夾，將使用內部資料夾。因此，若要在伺服器上部署 evennia，請省略 `-v`
選項並只需給出以下指令：

```
docker run -it --rm -d -p 4000:4000 -p 4001:4001 -p 4002:4002 --user $UID:$GID mydhaccount/mygame
```

您的遊戲將從您的 docker-hub 帳戶下載，並將使用該映像建立新容器並在伺服器上啟動！如果您的伺服器環境強制您使用不同的埠，您可以在上面的指令中以不同的方式對應普通埠。

上面我們新增了 `-d` 選項，它以 *daemon* 模式啟動容器 - 你不會看到任何
在控制檯中返回。您可以看到它以 `docker ps` 執行：

```bash
$ docker ps

CONTAINER ID     IMAGE       COMMAND                  CREATED              ...
f6d4ca9b2b22     mygame      "/bin/sh -c 'evenn..."   About a minute ago   ...
```

請注意容器ID，這是您在容器執行時管理容器的方式。

```
   docker logs f6d4ca9b2b22      
```
檢視容器的STDOUT輸出（i.e。正常伺服器日誌）
```
   docker logs -f f6d4ca9b2b22   
```
追蹤日誌（以便它“實時”更新到您的螢幕）。
```
   docker pause f6d4ca9b2b22     
```
暫停容器的狀態。
```
   docker unpause f6d4ca9b2b22   
```
暫停後再次取消暫停。它將準確地拾取原來的位置。
```
   docker stop f6d4ca9b2b22      
```
停止容器。要再次啟動，您需要使用 `docker run`，指定連線埠等。一個新的
容器將獲得一個新的容器 ID 來引用。

(how-it-works)=
## 它是如何運作的

`evennia/evennia` docker 映像包含 evennia 庫及其所有相依性。它還有一個 `ONBUILD` 指令，該指令在建立派生的影象期間觸發。此 `ONBUILD` 指令負責設定磁碟區並將遊戲目錄程式碼複製到容器內的正確位置。

在大多數情況下，基於 Evennia 的遊戲的 Dockerfile 僅需要 `FROM evennia/evennia:latest` 指令，如果您打算在 Docker Hub 上發布映像並希望提供聯絡資訊，則還可以選擇 `MAINTAINER` 指令。

有關 Dockerfile 指令的更多資訊，請參閱 [Dockerfile 參考](https://docs.docker.com/engine/reference/builder/)。

有關捲和 Docker 容器的更多資訊，請參閱 Docker 網站的 [管理資料
容器](https://docs.docker.com/engine/tutorials/dockervolumes/) 頁面。

(what-if-i-dont-want-latest)=
### 如果我不想要「LATEST」怎麼辦？

每當 Evennia 的 `main` 分支有新提交時，就會自動建立新的 `evennia/evennia` 映像。可以根據任意提交建立您自己的自訂 evennia 基本 docker 映像。

1. 使用 git 工具簽出您想要作為映像基礎的提交。 （在範例中
下面，我們正在檢查提交 a8oc3d5b。）
```
git checkout -b my-stable-branch a8oc3d5b 
```
2. 將工作目錄變更為包含`Dockerfile` 的`evennia` 目錄。注意
`Dockerfile` 隨著時間的推移而改變，所以如果你要回溯到提交歷史記錄，你可能會
想要隨身攜帶最新`Dockerfile`的副本並使用它而不是任何版本
當時使用的。
3. 使用 `docker build` 指令根據目前簽出的提交建置映像。
下面的範例假設您的 docker 帳戶是 **mydhaccount**。
```
docker build -t mydhaccount/evennia .
```
4. 現在您有了一個基於特定提交構建的基本 evennia docker 映像。要使用此影象
建立您的遊戲，您將修改遊戲目錄的 **Dockerfile** 中的 **FROM** 指令
成為：

```
FROM mydhacct/evennia:latest
``` 

注意：從此時起，您也可以使用 `docker tag` 指令在映像上設定特定的 tag 和/或將其上傳到您帳戶下的 Docker Hub。
5. 此時，像往常一樣使用相同的 `docker build` 指令來建立您的遊戲。改變你的
工作目錄是你的遊戲目錄並執行

```
docker build -t mydhaccountt/mygame .
```

(additional-creature-comforts)=
## 額外的物質享受

Docker 生態系統包括一個名為 `docker-compose` 的工具，它可以編排複雜的多容器應用程式，或者在我們的例子中，儲存我們每次執行容器時想要指定的預設連線埠和終端引數。用於執行開發中的容器化 Evennia 遊戲的範例 `docker-compose.yml` 檔案可能如下所示：
```
version: '2'

services:
  evennia:
    image: mydhacct/mygame
    stdin_open: true
    tty: true
    ports:
      - "4001-4002:4001-4002"
      - "4000:4000"
    volumes: 
      - .:/usr/src/game
```
將此檔案放在 `Dockerfile` 旁邊的遊戲目錄中，啟動容器就像這樣簡單
```
docker-compose up
```
有關`docker-compose`的更多資訊，請參閱[docker入門-
撰寫](https://docs.docker.com/compose/gettingstarted/)。

> 請注意，使用此設定您將丟失 `--user $UID` 選項。問題是變數 `UID` 在設定檔 `docker-compose.yml` 中不可用。解決方法是對您的使用者和群組 ID 進行硬編碼。在終端中執行 `echo  $UID:$GID`，例如，如果您得到 `1000:1000`，您可以在 `docker-compose.yml` 的 `image:...` 行下方新增一行 `user: 1000:1000`。