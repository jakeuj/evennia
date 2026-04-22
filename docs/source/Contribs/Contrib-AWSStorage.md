(awsstorage-system)=
# AWSstorage系統

Contrib 作者：尊敬的牧師 (trhr)，2020

該外掛遷移 Evennia 的基於 Web 的部分，即影象，
javascript 以及位於 Amazon AWS (S3) 靜態檔案內的其他專案
雲端託管。非常適合透過遊戲提供媒體服務的人。

S3 上託管的檔案“在雲端”，而您的個人檔案
伺服器可能足以向最少數量的使用者提供多媒體服務，
該外掛的完美用例是：

- 支援基於 Web 的大量流量的伺服器（webclient 等）...
- 擁有相當數量的使用者...
- 使用者分佈在全球...
- 多媒體檔案作為遊戲玩法的一部分提供給使用者

底線 - 如果您在玩家每次穿過某個區域時向他們傳送影象
地圖，使用此功能將顯著減少頻寬。如果沒有的話，可能
跳過這個contrib。

(on-costs)=
## 關於成本

請注意，透過 S3 儲存和提供檔案在技術上並不是免費的
亞馬遜的「免費套餐」產品，您可能有資格或沒有資格；
使用此 contrib 設定普通 evennia 伺服器目前需要 1.5MB
S3 上的儲存空間，使得目前執行此外掛程式的總成本
每年約 0.0005 美元。如果您擁有大量媒體資產並打算服務
對於許多使用者來說，買者自負的總擁有成本 - 檢查 AWS 的
定價結構。

(technical-details)=
## 技術細節

這是一個直接替換，其操作比 Evennia 的所有程式碼更深，
因此您的現有程式碼根本不需要更改即可支援它。

例如，當Evennia（或Django）嘗試永久儲存檔案時（例如，
使用者上傳的影象），儲存（或載入）通訊遵循以下路徑：

    Evennia -> Django
    Django -> Storage backend
    Storage backend -> file storage location (e.g. hard drive)

[django 檔案](https://docs.djangoproject.com/en/4.1/ref/settings/#std:setting-STATICFILES_STORAGE)

該外掛啟用後會覆蓋預設儲存後端，
預設將檔案儲存在 mygame/website/ 中，相反，
透過此處定義的儲存後端將檔案傳送到 S3。

沒有辦法（或不需要）直接存取或使用這裡的功能
其他貢獻或自訂程式碼。簡單地像平常一樣工作，Django
將處理其餘的事情。


(installation)=
## 安裝

(set-up-aws-account)=
### 設定 AWS 帳戶

如果您沒有 AWS S3 帳戶，您應該建立一個
https://aws.amazon.com/ - AWS S3 的檔案位於：
https://docs.aws.amazon.com/AmazonS3/latest/gsg/GetStartedWithS3.html

應用程式內所需的憑證為 AWS IAM 存取金鑰和秘密金鑰，
可以在 AWS 控制檯中產生/找到。

下面的範例IAM控制策略許可權可以加入到
AWS 內的 IAM 服務。可以在此處找到相關檔案：
https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html

請注意，只有當您想嚴格保護角色時才需要這樣做
該外掛可以訪問。

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "evennia",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR_BUCKET_NAME/*",
                "arn:aws:s3:::YOUR_BUCKET_NAME"
            ]
        }
    ],
    [
      {
         "Sid":"evennia",
         "Effect":"Allow",
         "Action":[
            "s3:CreateBucket",
         ],
         "Resource":[
            "arn:aws:s3:::*"
         ]
       }
    ]
}
```

進階使用者：僅需要第二個IAM語句CreateBucket
用於初始安裝。您可以稍後將其刪除，也可以
在繼續之前，請自行建立儲存桶並設定 ACL。

(dependencies)=
## 依賴關係


該套件需要依賴“boto3 >= 1.4.4”，官方
AWS python 包。要安裝，最簡單的方法是安裝 Evennia's
額外要求；

    pip install evennia[extra]

如果您安裝了 Evennia 和 `git`，您還可以

- `cd` 到 Evennia 儲存庫的根目錄。
- `pip install --upgrade -e.[extra]`

(configure-evennia)=
## 設定Evennia

自訂下面`secret_settings.py`中定義的變數。沒有進一步的
需要設定。請注意您需要設定為您的
實際值。

```python
# START OF SECRET_SETTINGS.PY COPY/PASTE >>>

AWS_ACCESS_KEY_ID = 'THIS_IS_PROVIDED_BY_AMAZON'
AWS_SECRET_ACCESS_KEY = 'THIS_IS_PROVIDED_BY_AMAZON'
AWS_STORAGE_BUCKET_NAME = 'mygame-evennia' # CHANGE ME! I suggest yourgamename-evennia

# The settings below need to go in secret_settings,py as well, but will
# not need customization unless you want to do something particularly fancy.

AWS_S3_REGION_NAME = 'us-east-1' # N. Virginia
AWS_S3_OBJECT_PARAMETERS = { 'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
                            'CacheControl': 'max-age=94608000', }
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % settings.AWS_BUCKET_NAME
AWS_AUTO_CREATE_BUCKET = True
STATICFILES_STORAGE = 'evennia.contrib.base_systems.awsstorage.aws-s3-cdn.S3Boto3Storage'

# <<< END OF SECRET_SETTINGS.PY COPY/PASTE
```

您也可以將這些鍵儲存為同名的環境變數。
有關進階設定，請參閱 django-storages 的文件。

複製上述內容後，執行`evennia reboot`。

(check-that-it-works)=
## 檢查它是否有效

透過造訪您的網站確認網路資產正在從 S3 提供服務，然後
檢查任何影象的來源（例如徽標）。  它應該讀
`https://your-bucket-name.s3.amazonaws.com/path/to/file`。如果是這樣，系統
有效，您不需要做任何其他事情。

(uninstallation)=
## 解除安裝

如果您尚未更改靜態檔案（上傳的影象等），
您只需刪除新增至 `secret_settings.py` 的行即可。如果你
已進行更改並希望稍後解除安裝，您可以匯出
您的 S3 儲存桶中的檔案並將它們放入 /static/ 中的 evennia
目錄。


(license)=
## 執照

大量借鑒 django-storages 提供的程式碼，這些貢獻者
作者是：

馬蒂·阿爾欽 (S3)
大衛拉雷特 (S3)
阿恩‧布羅多夫斯基 (S3)
塞巴斯蒂安·塞拉諾 (S3)
安德魯McClain (MogileFS)
拉法爾瓊卡 (FTP)
克里斯McCormick（S3 與 Boto）
伊凡諾夫 E.（資料庫）
阿里爾·努涅斯（包裝）
Wim Leers（SymlinkOrCopy + 補丁）
Michael Elsdörfer（覆蓋 + PEP8 相容性）
克里斯蒂安·克萊因 (CouchDB)
Rich Leland（Mosso 雲端檔案）
傑森·克里斯塔（補丁）
亞當·尼爾森（補丁）
Erik CW（S3 加密）
Axel Gembe（雜湊路徑）
瓦爾德馬·科內瓦爾德 (MongoDB)
Russell Keith-Magee（Apache LibCloud 補丁）
Jannis Leidel（S3 和 GS 與 Boto）
安德烈·科曼（Azure）
Chris Streeter（S3 與 Boto）
Josh Schneier（Fork 維護者、Bug 修復、Py3K）
安東尼蒙特 (Dropbox)
EunPyo (安德魯) 洪 (Azure)
麥可‧巴里恩託斯 (S3 with Boto3)
Piglei（補丁）
馬特·布雷默-海耶斯（S3 與 Boto3）
Eirik Martiniussen Sylliaas（Google 雲端儲存本機支援）
Jody McIntyre（Google Cloud Storage 原生支援）
Stanislav Kaledin（SFTPStorage 中的錯誤修復）
Filip Vavera（Google Cloud MIME 型別支援）
Max Malysh（Dropbox 大檔案支援）
懷特（Google Cloud 更新）
Alex Watt（Google雲端儲存補丁）
吉村純平（S3 文件）
喬恩·杜弗雷納
Rodrigo Gadea（Dropbox 修復）
馬蒂杜杜
克里斯溜冰場
程尚 (S3 檔案)
安德魯佩裡（SFTPStorage 中的錯誤修復）

django-storages 中的重新調整用途的程式碼在 BSD 3-Clause 下發布，
與Evennia相同，因此有關詳細許可，請參閱Evennia許可證。

(versioning)=
## 版本控制

這已被證實適用於 Django 2 和 Django 3。


----

<small>此檔案頁面是從`evennia\contrib\base_systems\awsstorage\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
