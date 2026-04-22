(guest-logins)=
# 訪客登入


Evennia 支援開箱即用的*來賓登入*。訪客登入是一種匿名、低訪問許可權的帳戶，如果您希望使用者有機會嘗試您的遊戲而無需建立真實帳戶，那麼訪客登入會很有用。

預設情況下，訪客帳戶處於關閉狀態。要啟用，請將其新增到您的 `game/settings.py` 檔案中：

    GUEST_ENABLED = True

從此使用者可以使用`connect guest`（在預設指令集中）以訪客帳號登入。您可能需要更改您的[連線畫面](../Components/Connection-Screen.md)以告知他們這種可能性。來賓帳戶的工作方式與普通帳戶不同 - 每當使用者登出或伺服器重設（但不會在重新載入期間）時，它們都會自動「刪除」。它們實際上是可重複使用的一次性帳戶。

您可以在 `settings.py` 檔案中新增更多變數來自訂您的客人：

- `BASE_GUEST_TYPECLASS` - 訪客預設 [typeclass](../Components/Typeclasses.md) 的 python 路徑。預設為`"typeclasses.accounts.Guest"`。
- `PERMISSION_GUEST_DEFAULT` - 來賓帳戶的[許可權等級](../Components/Locks.md)。預設為 `"Guest"`，這是層次結構中的最低許可權等級（低於 `Player`）。
- `GUEST_START_LOCATION` - 新登入訪客應出現的起始位置的 `#dbref`。預設為 `"#2` (Limbo)。
- `GUEST_HOME` - 賓客之家位置。也預設為 Limbo。
- `GUEST_LIST` - 這是一個包含進入遊戲時可能使用的客人姓名的清單。此清單的長度也設定了可以同時登入的訪客數量。預設情況下，這是從 `"Guest1"` 到 `"Guest9"` 的九個名稱的清單。