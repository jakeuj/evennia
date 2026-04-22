(inputoutput-auditing)=
# 輸入/輸出審核

Johnny 的貢獻，2017 年

實用程式可以竊聽並攔截傳送到/從用戶端傳送的所有資料以及
伺服器並將其傳遞給您選擇的回撥。這是為了
品質保證、事故後調查和除錯。

請注意，應謹慎使用，因為它顯然可能被濫用。全部
資料以明文形式記錄。請保持道德，如果您不願意
妥善處理記錄使用者密碼或隱私的影響
通訊時，請不要啟用該模組。

已經實施了一些檢查來保護使用者的隱私。

此模組包含的檔案：

    outputs.py - Example callback methods. This module ships with examples of
            callbacks that send data as JSON to a file in your game/server/logs
            dir or to your native Linux syslog daemon. You can of course write
            your own to do other things like post them to Kafka topics.

    server.py - Extends the Evennia ServerSession object to pipe data to the
            callback upon receipt.

	tests.py - Unit tests that check to make sure commands with sensitive
	        arguments are having their PII scrubbed.


(installationconfiguration)=
## 安裝/設定：

透過設定server.conf中的一些設定即可完成部署。這條線
需要：

    SERVER_SESSION_CLASS = 'evennia.contrib.utils.auditing.server.AuditedServerSession'

這告訴 Evennia 使用這個 ServerSession 而不是它自己的。以下是
其他可能的選項以及未設定時將使用的預設值。

    # Where to send logs? Define the path to a module containing your callback
    # function. It should take a single dict argument as input
    AUDIT_CALLBACK = 'evennia.contrib.utils.auditing.outputs.to_file'

    # Log user input? Be ethical about this; it will log all private and
    # public communications between players and/or admins (default: False).
    AUDIT_IN = False

    # Log server output? This will result in logging of ALL system
    # messages and ALL broadcasts to connected players, so on a busy game any
    # broadcast to all users will yield a single event for every connected user!
    AUDIT_OUT = False

    # The default output is a dict. Do you want to allow key:value pairs with
    # null/blank values? If you're just writing to disk, disabling this saves
    # some disk space, but whether you *want* sparse values or not is more of a
    # consideration if you're shipping logs to a NoSQL/schemaless database.
    # (default: False)
    AUDIT_ALLOW_SPARSE = False

    # If you write custom commands that handle sensitive data like passwords,
    # you must write a regular expression to remove that before writing to log.
    # AUDIT_MASKS is a list of dictionaries that define the names of commands
    # and the regexes needed to scrub them.
    # The system already has defaults to filter out sensitive login/creation
    # commands in the default command set. Your list of AUDIT_MASKS will be appended
    # to those defaults.
    #
    # In the regex, the sensitive data itself must be captured in a named group with a
    # label of 'secret' (see the Python docs on the `re` module for more info). For
    # example: `{'authentication': r"^@auth\s+(?P<secret>[\w]+)"}`
    AUDIT_MASKS = []


----

<small>此檔案頁面是從`evennia\contrib\utils\auditing\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
