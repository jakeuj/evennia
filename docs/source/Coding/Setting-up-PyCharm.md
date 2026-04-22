(setting-up-pycharm-with-evennia)=
# 使用 Evennia 設定 PyCharm

[PyCharm](https://www.jetbrains.com/pycharm/) 是來自 Jetbrains 的 Python 開發人員的 IDE，可用於 Windows、Mac 和 Linux。 
它是一個商業產品，但提供免費試用、縮小版社群版本以及針對 OSS 專案（例如 Evennia）的慷慨授權。

首先，下載並安裝您選擇的IDE版本。
社群版應該有你需要的一切，
但專業版整合了對 Django 的支援，這可以提供幫助。

(from-an-existing-project)=
## 來自現有專案

如果您想將 PyCharm 與現有的 Evennia 遊戲一起使用，請使用此選項。
首先，請確保您已完成[此處]所列的步驟(https://www.evennia.com/docs/latest/Setup/Installation.html#requirements)。
特別是 virtualenv 部分，這將使設定 IDE 變得更加容易。

1. 開啟Pycharm，點選開啟按鈕，開啟`mygame/`對應的根資料夾。
2. 點選檔案 -> 設定 -> 專案 -> Python 直譯器 -> 新增直譯器 -> 新增本機直譯器
![例](https://imgur.com/QRo8O1C.png)
3. 點選 VirtualEnv -> 現有解譯器 -> 選擇現有的 virtualenv 資料夾，
如果您遵循預設安裝，則應為 `evenv`。

![例](https://imgur.com/XDmgjTw.png)

(from-a-new-project)=
## 來自一個新專案

如果您從頭開始或想要製作新的 Evennia 遊戲，請使用此選項。
1. 點選新專案按鈕。
2. 選擇您的專案的位置。
您應該建立兩個新資料夾，一個用於專案的根目錄，另一個用於
直接進行evennia遊戲。它應該看起來像`/location/projectfolder/gamefolder`
3. 選擇 `Custom environment` 解譯器型別，使用 `Generate New` 型別 `Virtual env` 使用
https://www.evennia.com/docs/latest/Setup/Installation.html#requirements 中推薦的相容基本 python 版本
然後為您的虛擬環境選擇一個資料夾作為專案資料夾的子資料夾。

![新專案設定範例](https://imgur.com/R5Yr9I4.png)

點選“建立”按鈕，它將帶您進入具有基本虛擬環境的新專案。
要安裝 Evennia，您可以在專案資料夾中克隆 evennia 或透過 pip 安裝它。
最簡單的方法是使用 pip。

點選`terminal`按鈕

![終端按鈕](https://i.imgur.com/fDr4nhv.png)

1. 輸入`pip install evennia`
2. 關閉 IDE 並導航至專案資料夾
3. 將遊戲資料夾重新命名為臨時名稱，並使用先前的名稱建立新的空白資料夾
4. 開啟 OS 終端，導航至專案資料夾並啟動 virtualenv。
在 Linux 上，`source.evenv/bin/activate`
在 Windows 上，`evenv\Scripts\activate`
5. 輸入`evennia --init mygame`
6. 將檔案從臨時資料夾（應包含 `.idea/` 資料夾）移至
您在步驟 3 中建立的資料夾並刪除現在為空的臨時資料夾。
7. 在終端機中，移至資料夾並輸入 `evennia migrate`
8. 啟動evennia以確保它與`evennia start`一起工作並與`evennia stop`停止它

此時，您可以重新開啟 IDE，它應該可以正常運作。
[檢視此處以瞭解更多資訊](https://www.evennia.com/docs/latest/Setup/Installation.html)


(debug-evennia-from-inside-pycharm)=
## 從 PyCharm 內部除錯 Evennia

(attaching-to-the-process)=
### 附加到程式
1. 在pycharm終端中啟動Evennia
2. 嘗試啟動它兩次，這將為您提供伺服器的程式 ID
3. 在PyCharm選單中，選擇`Run > Attach to Process...`
4. 從清單中選擇相應的程式ID，它應該是帶有`server.py`引數的`twistd`程式（例如：`twistd.exe --nodaemon --logfile=\<mygame\>\server\logs\server.log --python=\<evennia repo\>\evennia\server\server.py`）

如果您想偵錯 Evennia 啟動器，您也可以附加到 `portal` 程式
或出於某種原因執行（或只是瞭解它們如何工作！），請參閱下面的執行設定。

> NOTE：每當您重新載入Evennia時，舊的伺服器程式就會終止，並啟動一個新的程式。因此，當您重新啟動時，您必須與舊程式分離，然後重新附加到已建立的新程式。


(run-evennia-with-a-rundebug-configuration)=
### 使用執行/除錯設定執行 Evennia

此設定可讓您從 PyCharm 內部啟動 Evennia。 
除了方便之外，它還允許暫停和除錯evennia_launcher或evennia_runner
比您在外部執行它們並附加的時間更早。
事實上，當伺服器和/或 portal 執行時，啟動器已經退出。

(on-windows)=
#### 在 Windows 上
1. 前往`Run > Edit Configutations...`
2. 點選加號新增設定並選擇 Python
3. 新增script：`\<yourprojectfolder>\.evenv\Scripts\evennia_launcher.py`（如果未命名為`evenv`，請替換您的virtualenv）
4. 將 script 引數設定為：`start -l`（-l 啟用控制檯日誌記錄）
5. 確保所選的直譯器是您的 virtualenv
6. 將工作目錄設定為您的 `mygame` 資料夾（不是您的專案資料夾，也不是 evennia）
7. 您可以參閱 PyCharm 檔案以獲取一般資訊，但您至少需要設定一個設定名稱（例如“MyMUD start”或類似名稱）。

儲存新設定的下拉框應該會出現在 PyCharm 執行按鈕旁邊。 
選擇它啟動並按除錯圖示開始除錯。

(on-linux)=
#### 在 Linux 上
1. 前往`Run > Edit Configutations...`
2. 點選加號新增設定並選擇 Python
3. 新增script：`/<yourprojectfolder>/.evenv/bin/twistd`（如果未命名為`evenv`，請替換您的virtualenv）
4. 將 script 引數設定為：`--python=/<yourprojectfolder>/.evenv/lib/python3.11/site-packages/evennia/server/server.py --logger=evennia.utils.logger.GetServerLogObserver --pidfile=/<yourprojectfolder>/<yourgamefolder>/server/server.pid --nodaemon`
5. 新增環境變數`DJANGO_SETTINGS_MODULE=server.conf.settings`
6. 確保所選的直譯器是您的 virtualenv
7. 將工作目錄設定為您的遊戲資料夾（不是您的專案資料夾，也不是evennia）
8. 您可以參閱 PyCharm 檔案以獲取一般資訊，但您至少需要設定一個設定名稱（例如“MyMUD Server”或類似名稱）。

儲存新設定的下拉框應該會出現在 PyCharm 執行按鈕旁邊。 
選擇它啟動並按除錯圖示開始除錯。
請注意，這只會啟動伺服器程式，您可以手動啟動 portal 或設定
portal 的設定。步驟與上面的非常相似。

1. 前往`Run > Edit Configutations...`
2. 點選加號新增設定並選擇 Python
3. 新增script：`/<yourprojectfolder>/.evenv/bin/twistd`（如果未命名為`evenv`，請替換您的virtualenv）
4. 將 script 引數設定為：`--python=/<yourprojectfolder>/.evenv/lib/python3.11/site-packages/evennia/server/portal/portal.py --logger=evennia.utils.logger.GetServerLogObserver --pidfile=/<yourprojectfolder>/<yourgamefolder>/server/portal.pid --nodaemon`
5. 新增環境變數`DJANGO_SETTINGS_MODULE=server.conf.settings`
6. 確保所選的直譯器是您的 virtualenv
7. 將工作目錄設定為您的遊戲資料夾（不是您的專案資料夾，也不是evennia）
8. 您可以參閱 PyCharm 檔案以瞭解一般資訊，但您至少需要設定一個設定名稱（例如“MyMUD Portal”或類似名稱）。

現在您應該能夠啟動這兩種模式並進行完整的除錯。
如果您想更進一步，可以新增另一個設定來自動啟動兩者。

1. 前往`Run > Edit Configutations...`
2. 點選加號新增設定並選擇複合
3. 新增先前的兩個設定，適當命名並按“確定”。

現在您可以一鍵啟動遊戲並啟用完整除錯。
