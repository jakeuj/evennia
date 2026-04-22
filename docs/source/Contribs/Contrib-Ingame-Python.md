(evennia-in-game-python-system)=
# Evennia遊戲內Python系統

Contrib 作者：文森‧勒戈夫 2017

這 contrib 增加了 script 在遊戲中使用 Python 的能力。它允許可信
工作人員/建構者動態新增功能和觸發器到單一物件
無需在外部 Python 模組中執行此操作。在遊戲中使用自訂Python，
特定的房間、出口、角色、物件等可以表現得與
它的「表兄弟」。這類似於軟程式碼對於 MU 或 MudProgs 對於 DIKU 的工作方式。
但請記住，允許在遊戲中使用 Python 會帶來嚴重的後果
安全問題（您必須深深信任您的建造者），因此請閱讀中的警告
在繼續之前請仔細閱讀此模組。

(a-warning-regarding-security)=
## WARNING REGARDING SECURITY

Evennia 的遊戲內 Python 系統將執行任意 Python 程式碼，無需太多
限制。  這樣的系統既強大又有潛在的危險，而你
在決定安裝之前必須記住以下幾點：

1. 不受信任的人可以使用此係統在您的遊戲伺服器上執行 Python 程式碼。
請注意誰可以使用該系統（請參閱下面的許可權）。
2. 您可以在遊戲之外使用 Python 完成所有這些操作。  遊戲中的Python系統
並不是要取代您的所有遊戲功能。

(extra-tutorials)=
## 額外教學

這些教學涵蓋了使用 ingame python 的範例。一旦你擁有了系統
安裝（見下文）它們可能是比閱讀完整內容更容易的學習方法
從頭到尾的文件。

- [對話事件](./Contrib-Ingame-Python-Tutorial-Dialogue.md)，其中
NPCs 對所說的話做出反應。
- [語音電梯](./Contrib-Ingame-Python-Tutorial-Elevator.md)
使用 ingame-python 事件。

(basic-structure-and-vocabulary)=
## 基本結構和詞彙

- 遊戲內 Python 系統的基礎是**事件**。  **事件**
定義我們想要呼叫一些任意程式碼的上下文。  對於
例如，事件在退出時定義，並且每次角色出現時都會觸發
穿過這個出口。  事件在 [typeclass](../Components/Typeclasses.md) 上描述
（在我們的範例中為[退出](../Components/Exits.md)）。  所有繼承於此的物件
typeclass 將有權訪問此活動。
- **回呼**可以在單一物件上、在程式碼中定義的事件上設定。
這些**回呼**可以包含任意程式碼並描述特定的
物件的行為。  當事件觸發時，所有回撥都連線到此
物件的事件被執行。

若要在上下文中檢視系統，當擷取物件時（使用預設值
`get` 指令），會觸發特定事件：

1. 事件「get」在物件上設定（在`Object` typeclass 上）。
2. 當使用“get”指令拾取物體時，該物體的`at_get`
稱為鉤子。
3. DefaultObject 的修改掛鉤由事件系統設定。  這個鉤子將
在此物件上執行（或呼叫）“get”事件。
4. 與該物件的「get」事件相關的所有回呼都將按順序執行。
這些回撥可作為包含您可以編寫的 Python 程式碼的函式
   在遊戲中，使用編輯回撥時將列出的特定變數
   本身。
5. 在各個回撥中，您可以新增多行 Python 程式碼，這些程式碼將
此時將被解僱。  在此範例中，`character` 變數將
   包含拾取物體的角色，而 `obj` 將包含
   被拾取的物體。

按照此範例，如果您在物件“劍”上建立回撥“get”，
並放入：

```python
character.msg("You have picked up {} and have completed this quest!".format(obj.get_display_name(character)))

```

當你拿起這個物體時，你應該看到類似的東西：

    You pick up a sword.
    You have picked up a sword and have completed this quest!

(installation)=
## 安裝

由於位於單獨的 contrib 中，遊戲中的 Python 系統不是由
預設。  您需要按照以下步驟手動執行此操作：

這是快速總結。向下捲動以獲取有關每個步驟的更詳細幫助。

1. 啟動主script（重要！）：

        py evennia.create_script("evennia.contrib.base_systems.ingame_python.scripts.EventHandler")

2. 設定許可權（可選）：
   - `EVENTS_WITH_VALIDATION`：可以編輯回呼的群組，但需要批准（預設為
     `None`).
   - `EVENTS_WITHOUT_VALIDATION`：有權編輯回呼的群組，無需
     validation (default to `"immortals"`).
   - `EVENTS_VALIDATING`：可以驗證回呼的組別（預設為`"immortals"`）。
   - `EVENTS_CALENDAR`：要使用的日曆型別（`None`、`"standard"` 或 `"custom"`，
     default to `None`).
3. 新增`call`指令。
4. 繼承遊戲內Python系統的自訂typeclasses。
   - `evennia.contrib.base_systems.ingame_python.typeclasses.EventCharacter`：替換`DefaultCharacter`。
   - `evennia.contrib.base_systems.ingame_python.typeclasses.EventExit`：替換`DefaultExit`。
   - `evennia.contrib.base_systems.ingame_python.typeclasses.EventObject`：替換`DefaultObject`。
   - `evennia.contrib.base_systems.ingame_python.typeclasses.EventRoom`：替換`DefaultRoom`。

以下部分詳細描述了安裝的每個步驟。

> 注意：如果您在未啟動主要script的情況下開始遊戲（例如當
重置資料庫）您很可能在登入時面臨回溯，告訴您
未定義“回撥”屬性。執行步驟 `1` 後，錯誤將消失。

(starting-the-event-script)=
### 開始活動script

要啟動事件script，您只需要一個指令，使用`@py`。

    py evennia.create_script("evennia.contrib.base_systems.ingame_python.scripts.EventHandler")

該指令將建立一個全域script（即獨立於任何物件的script）。  這個
script 將儲存基本設定、單獨回撥等。  您可以直接訪問它，
但您可能會使用回撥處理程式。  建立這個 script 也會創造一個 `callback`
所有物件的處理程式（有關詳細資訊，請參閱下文）。

(editing-permissions)=
### 編輯許可權

這個 contrib 帶有它自己的一組許可權。  他們定義了誰可以編輯回撥，而無需
驗證，以及誰可以編輯回撥但需要驗證。  驗證是一個過程，其中
管理員（或受信任的人）將檢查其他人產生的回撥，並將
接受或拒絕他們。  如果接受，則連線回撥，否則它們永遠不會執行。

預設情況下，回呼只能由神仙建立：除了神仙之外沒有人可以編輯
回撥，且不朽不需要驗證。  它可以透過設定輕鬆更改
或透過更改使用者的許可權來動態地進行。

ingame-python contrib 在設定中新增了三個[許可權](../Components/Permissions.md))。  你可以
透過將設定變更到 `server/conf/settings.py` 檔案中來覆蓋它們（請參閱下面的
範例）。  事件 contrib 中定義的設定是：

- `EVENTS_WITH_VALIDATION`：這定義了可以編輯回呼的許可權，但需要
贊同。  例如，如果將其設定為`"wizards"`，則具有許可權`"wizards"`的使用者
將能夠編輯回撥。  不過，這些回撥不會被連線，而且需要
經管理員檢查並批准。  此設定可以包含`None`，表示沒有使用者
允許編輯帶有驗證的回撥。
- `EVENTS_WITHOUT_VALIDATION`：此設定定義允許編輯回呼的許可權
無需驗證。  預設情況下，此設定設定為 `"immortals"`。  這意味著
神仙可以編輯回撥，離開編輯器就會連線，無需
批准。
- `EVENTS_VALIDATING`：最後一個設定定義誰可以驗證回呼。  預設情況下，這是
設定為`"immortals"`，意味著只有不朽者才能看到需要驗證、接受或
拒絕他們。

您可以覆蓋 `server/conf/settings.py` 檔案中的所有這些設定。  例如：

```python
# ... other settings ...

# Event settings
EVENTS_WITH_VALIDATION = "wizards"
EVENTS_WITHOUT_VALIDATION = "immortals"
EVENTS_VALIDATING = "immortals"
```

此外，如果您打算使用與時間相關的事件，則必須設定另一個設定
（在特定的遊戲時間安排的事件）。  您需要指定型別
您正在使用的日曆。  預設情況下，停用與時間相關的事件。  您可以更改
`EVENTS_CALENDAR` 將其設定為：

- `"standard"`：標準日曆，有標準日、月、年等。
- `"custom"`：將使用 `custom_gametime` contrib 來安排事件的自訂日曆。

此 contrib 定義了可以對單一使用者設定的兩個附加許可權：

- `events_without_validation`：這將授予該使用者編輯回呼的許可權，但不
連線之前需要驗證。
- `events_validating`：此許可權允許該使用者對回呼執行驗證檢查
需要驗證。

例如，要授予玩家“kaldara”無需批准即可編輯回撥的權利，
你可能會這樣做：

    perm *kaldara = events_without_validation

要刪除相同的許可權，只需使用 `/del` 開關：

    perm/del *kaldara = events_without_validation

使用`call`指令的許可權與這些許可權直接相關：預設情況下，僅
具有 `events_without_validation` 許可權或屬於（或以上）中定義的群組的使用者
`EVENTS_WITH_VALIDATION` 設定將能夠呼叫指令（使用不同的開關）。

(adding-the-call-command)=
### 新增`call`指令

您還必須將 `@call` 指令新增至您的角色 CmdSet。  該指令允許您的使用者
在遊戲中新增、編輯和刪除回撥。  在你的`commands/default_cmdsets`中，它可能看起來像
這個：

```python
from evennia import default_cmds
from evennia.contrib.base_systems.ingame_python.commands import CmdCallback

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `PlayerCmdSet` when a Player puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CmdCallback())
```

(changing-parent-classes-of-typeclasses)=
### 更改 typeclasses 的父類

最後，要使用遊戲中的Python系統，您需要讓您的typeclasses繼承自修改過的事件
類。  例如，在您的 `typeclasses/characters.py` 模組中，您應該更改繼承
像這樣：

```python
from evennia.contrib.base_systems.ingame_python.typeclasses import EventCharacter

class Character(EventCharacter):

    # ...
```

您應該對您的房間、出口和物體做同樣的事情。  請注意，
遊戲中的 Python 系統透過覆蓋一些鉤子來運作。  其中一些功能
如果您在以下情況下不呼叫父方法，則可能無法在您的遊戲中訪問
壓倒一切的鉤子。

(using-the-call-command)=
## 使用`call`指令

遊戲中的Python系統在很大程度上依賴它的`call`指令。
誰可以執行此指令，以及誰可以用它做什麼，將取決於您的
許可權集。

`call` 指令允許新增、編輯和刪除特定物件事件的回呼。  活動內容
系統可用於大多數 Evennia 物件，主要是型別分類物件（不包括玩家）。  的
`call` 指令的第一個引數是要編輯的物件的名稱。  也可以是
用於瞭解該特定物件有哪些事件可用。

(examining-callbacks-and-events)=
### 檢查回撥和事件

若要檢視連線到物件的事件，請使用 `call` 指令並給出物件的名稱或 ID
物件進行檢查。  例如，`call here` 檢查您目前位置的事件。  或者
`call self` 檢視您自己的事件。

該指令將顯示一個表，其中包含：

- 第一列中每個事件的名稱。
- 該名稱的回呼數，以及這些回呼的總行數
第二欄。
- 第三列中有一個簡短的幫助，告訴您事件何時被觸發。

例如，如果執行 `call #1`，您可能會看到如下表：

```
+------------------+---------+-----------------------------------------------+
| Event name       |  Number | Description                                   |
+~~~~~~~~~~~~~~~~~~+~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
| can_delete       |   0 (0) | Can the character be deleted?                 |
| can_move         |   0 (0) | Can the character move?                       |
| can_part         |   0 (0) | Can the departing character leave this room?  |
| delete           |   0 (0) | Before deleting the character.                |
| greet            |   0 (0) | A new character arrives in the location of    |
|                  |         | this character.                               |
| move             |   0 (0) | After the character has moved into its new    |
|                  |         | room.                                         |
| puppeted         |   0 (0) | When the character has been puppeted by a     |
|                  |         | player.                                       |
| time             |   0 (0) | A repeated event to be called regularly.      |
| unpuppeted       |   0 (0) | When the character is about to be un-         |
|                  |         | puppeted.                                     |
+------------------+---------+-----------------------------------------------+
```

(creating-a-new-callback)=
### 建立一個新的回撥

`/add` 開關應該用於新增回撥。  它需要兩個超出物件的引數
姓名/DBREF:

1. = 號後是要編輯的事件名稱（如果未提供，將顯示事件清單）
可能發生的事件，如上所述）。
2. 引數（可選）。

稍後我們將看到帶有引數的回撥。  現在我們先嘗試阻止一個角色
從這個房間的「北」出口：

```
call north
+------------------+---------+-----------------------------------------------+
| Event name       |  Number | Description                                   |
+~~~~~~~~~~~~~~~~~~+~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+
| can_traverse     |   0 (0) | Can the character traverse through this exit? |
| msg_arrive       |   0 (0) | Customize the message when a character        |
|                  |         | arrives through this exit.                    |
| msg_leave        |   0 (0) | Customize the message when a character leaves |
|                  |         | through this exit.                            |
| time             |   0 (0) | A repeated event to be called regularly.      |
| traverse         |   0 (0) | After the character has traversed through     |
|                  |         | this exit.                                    |
+------------------+---------+-----------------------------------------------+
```

如果我們想阻止角色穿過這個出口，對我們來說最好的事件是
“can_traverse”。

> 為什麼不「穿越」呢？  如果您閱讀了這兩個事件的描述，您會看到「traverse」被稱為
**在**角色穿過此出口之後。  想要阻止它就太晚了。  在
> 另一方面，「can_traverse」顯然是在字元遍歷之前進行檢查的。

當我們編輯事件時，我們有更多資訊：

    call/add north = can_traverse

角色可以透過這個出口嗎？
當角色即將遍歷此事件時呼叫此事件
退出。  您可以使用 deny() eventfunc 來拒絕來自的字元
這次退出。

您可以在此事件中使用的變數：

    - 角色：想要穿過此出口的角色。
    - exit：要經過的出口。
    - room：角色移動前所站立的房間。

專門介紹 [eventfuncs](#the-eventfuncs) 的部分將詳細說明 `deny()` 函式和
其他事件函式。  暫時讓我們說，它可以阻止某個動作（在本例中，它
可以阻止角色穿過這個出口）。  在您開啟時開啟的編輯器中
使用 `call/add`，您可以輸入以下內容：

```python
if character.id == 1:
    character.msg("You're the superuser, 'course I'll let you pass.")
else:
    character.msg("Hold on, what do you think you're doing?")
    deny()
```

現在您可以輸入 `:wq` 透過儲存回撥來離開編輯器。

如果您輸入 `call north`，您應該會看到「can_traverse」現在有活動回撥。  你可以
使用 `call north = can_traverse` 檢視連線回呼的更多詳細資訊：

```
call north = can_traverse
+--------------+--------------+----------------+--------------+--------------+
|       Number | Author       | Updated        | Param        | Valid        |
+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~+~~~~~~~~~~~~~~+
|            1 | XXXXX        | 5 seconds ago  |              | Yes          |
+--------------+--------------+----------------+--------------+--------------+
```

左列包含回撥號碼。  您可以使用它們來獲取有關某個物件的更多資訊
具體事件。  在這裡，例如：

```
call north = can_traverse 1
Callback can_traverse 1 of north:
Created by XXXXX on 2017-04-02 17:58:05.
Updated by XXXXX on 2017-04-02 18:02:50
This callback is connected and active.
Callback code:
if character.id == 1:
    character.msg("You're the superuser, 'course I'll let you pass.")
else:
    character.msg("Hold on, what do you think you're doing?")
    deny()
```

然後嘗試穿過這個出口。  如果可能的話，也與另一個角色一起做，以檢視
差異。

(editing-and-removing-a-callback)=
### 編輯和刪除回撥

您可以使用 `/edit` 開關到 `@call` 指令來編輯回呼。  您應該在之後提供
要編輯的物件的名稱和等號：

1. 事件的名稱（如上圖）。
2. 如果在此位置連線了多個回撥，則為數字。

您可以輸入 `call/edit <object> = <event name>` 檢視連結到此的回撥
位置。  如果只有一個回撥，則會在編輯器中開啟；如果定義了更多，您
將要求提供一個數字（例如，`call/edit north = can_traverse 2`）。

指令 `call` 還提供了 `/del` 開關來刪除回撥。  它需要相同的引數
作為 `/edit` 開關。

刪除後，回呼將被記錄，因此管理員可以檢索其內容，假設
`/del` 是個錯誤。

(the-code-editor)=
### 程式碼編輯器

新增或編輯回呼時，事件編輯器應以程式碼模式開啟。  額外的
在此模式下編輯器支援的選項在[EvEditor 的專用部分中描述
檔案](https://github.com/evennia/evennia/wiki/EvEditor#the-eveditor-to-edit-code)。

(using-events)=
## 使用事件

以下部分描述如何使用事件來執行各種任務，從最簡單的到最複雜的
最複雜。

(the-eventfuncs)=
### 事件函式

為了讓開發更簡單，遊戲中的Python系統提供了eventfuncs來使用
回撥本身。  您不必使用它們，它們只是快捷方式。  eventfunc 只是一個
可以在回撥程式碼中使用的簡單函式。

功能|論證|描述 |範例
-----------|--------------------------------|------------------------------------------------|--------
否認| `()` |阻止某個動作的發生。 | `deny()`
得到| `(**kwargs)` |取得單一物件。              | `char = get(id=1)`
call_event | `(obj, name, seconds=0)` |呼叫另一個事件。               | `call_event(char, "chain_1", 20)`

(deny)=
#### 否定

`deny()` 函式允許中斷回撥和呼叫它的操作。  在
`can_*`事件，它可以用來阻止該動作的發生。  例如，在 `can_say` 上
房間，它可以阻止角色在房間裡說話。  一個人可能有`can_eat`
在食物上設定的事件將阻止該角色吃這種食物。

在幕後，`deny()` 函式引發了一個異常，該異常被
事件處理程式。  然後處理程式將報告操作已取消。

(get)=
#### 得到

`get` eventfunc 是取得具有特定識別的單一物件的捷徑。  它經常被使用
檢索具有給定 ID 的物件。  在專門討論[鍊式
events](#chained-events)，您將看到此函式的具體範例。

(call_event)=
#### call_event

有些回撥會呼叫其他事件。  它對於[鍊式
事件](#chained-events)，在專門的部分中進行了描述。  這個eventfunc用來呼叫
立即或在規定時間內發生的另一事件。

您需要將包含事件的物件指定為第一個引數。  第二個引數是
要呼叫的事件的名稱。  第三個引數是呼叫此事件之前的秒數。
預設情況下，此引數設定為 0（立即呼叫事件）。

(variables-in-callbacks)=
### 回撥中的變數

在您將輸入單獨回撥的 Python 程式碼中，您將可以存取您的變數中的變數
當地人。  這些變數將取決於事件，並且在您新增或編輯事件時會清楚列出
回撥。  正如您在前面的範例中所看到的，當我們操作字元或字元時
動作，我們通常有一個 `character` 變數來儲存執行動作的角色。

在大多數情況下，當觸發事件時，會呼叫該事件的所有回撥。  變數是
為每個事件建立。  然而，有時，回撥將執行，然後請求一個變數
在你的本地：換句話說，一些回撥可以透過改變來改變正在執行的操作
變數的值。  這總是在事件的幫助中明確指定的。

說明該系統的一個範例是可以在退出時設定的“msg_leave”事件。
此事件可以更改當有人離開時傳送給其他角色的訊息
這個出口。

    call/add down = msg_leave

哪個應該顯示：

```
Customize the message when a character leaves through this exit.
This event is called when a character leaves through this exit.
To customize the message that will be sent to the room where the
character came from, change the value of the variable "message"
to give it your custom message.  The character itself will not be
notified.  You can use mapping between braces, like this:
    message = "{character} falls into a hole!"
In your mapping, you can use {character} (the character who is
about to leave), {exit} (the exit), {origin} (the room in which
the character is), and {destination} (the room in which the character
is heading for).  If you need to customize the message with other
information, you can also set "message" to None and send something
else instead.

Variables you can use in this event:
    character: the character who is leaving through this exit.
    exit: the exit being traversed.
    origin: the location of the character.
    destination: the destination of the character.
    message: the message to be displayed in the location.
    mapping: a dictionary containing additional mapping.
```

如果您在活動中寫下這樣的內容：

```python
message = "{character} falls into a hole in the ground!"

```

如果角色威爾弗雷德從這個出口出去，房間裡的其他人會看到：

    Wildred falls into a hole in the ground!

在這種情況下，遊戲中的 Python 系統將變數「message」放置在回撥區域性變數中，但會讀取
事件執行後從中獲取。

(callbacks-with-parameters)=
### 帶引數的回撥

某些回撥的呼叫不帶引數。  我們見過的所有例子都是如此
之前。  在某些情況下，您可以建立僅在某些條件下觸發的回呼。  一個
典型的例子就是房間的「say」事件。  當有人在其中說了某事時會觸發此事件
房間。  在此事件上設定的個別回撥可以設定為僅在某些單字出現時觸發
用在句子中。

例如，假設我們想要建立一個很酷的語音操作電梯。  您進入
搭乘電梯並說出樓層號...電梯就會朝正確的方向移動。  在這種情況下，
我們可以使用引數“one”來建立一個回撥：

    call/add here = say one

僅當使用者說出包含“one”的句子時才會觸發此回撥。

但是，如果我們想要一個在使用者說 1 或 1 時觸發的回撥該怎麼辦？  我們可以提供
多個引數，以逗號分隔。

    call/add here = say 1, one

或者，還有更多關鍵字：

    call/add here = say 1, one, ground

這次，使用者可以說「帶我去一樓」（「ground」是我們的
上述回呼中定義的關鍵字）。

並非所有事件都可以帶引數，而這些事件有不同的處理方法。  那裡
並不是可以應用於所有事件的引數的單一意義。  參考活動
檔案瞭解詳細資訊。

> 如果您對回呼變數和引數感到困惑，請將引數視為檢查
> 在回撥執行之前執行。  帶有引數的事件只會觸發一些特定的事件
> 回撥，不是全部。

(time-related-events)=
### 與時間相關的事件

正如我們之前所見，事件通常與指令相關聯。  然而，情況並非總是如此。
事件可以由其他操作觸發，正如我們稍後將看到的，甚至可以從內部呼叫
其他活動！

所有物件上都有一個可以在特定時間觸發的特定事件。  這是一個事件
強制引數，這是您期望此事件觸發的時間。

例如，讓我們在此房間中新增一個事件，該事件應該每天在 12:00 PM 精確觸發
（時間為遊戲時間，非即時）：

    call here = time 12:00

```python
# This will be called every MUD day at 12:00 PM
room.msg_contents("It's noon, time to have lunch!")

```

現在，在每 MUD 天的中午，此事件將觸發並執行此回撥。  您可以使用
此事件針對每種型別分類的物件，每 MUD 天執行一次特定操作
同一時間。

與時間相關的事件可能比這複雜得多。  他們可以在遊戲中的每個小時或更長時間觸發
經常（在許多物件上經常觸發事件可能不是一個好主意）。  你可以
遊戲中每週、每月或每年都會舉辦活動。  它會根據不同的情況而有很大差異
遊戲中使用的日曆型別。  遊戲中描述了時間單位的數量
設定。

例如，對於標準日曆，您可以使用以下單位：分鐘、小時、天、月
和歲月。  您可以將它們指定為由冒號 (:)、空格 ( ) 或破折號分隔的數字
(-)。  選擇任何感覺更合適的（通常，我們用冒號分隔小時和分鐘，
其他有破折號的單位）。

一些語法範例：

- `18:30`：每天6:30 PM。
- `01 12:00`：每個月的第一天，12PM。
- `06-15 09:58`：每年 6 月 15 日（月在日之前），9:58 AM。
- `2025-01-01 00:00`：2025年1月1日午夜（顯然，這只會觸發一次）。

請注意，我們以相反的順序指定單位（年、月、日、小時和分鐘）並分開
它們帶有邏輯分隔符號。  未定義的最小單位將設定頻率
事件應該觸發。  這就是為什麼，如果您使用 `12:00`，未定義的最小單位是「天」：
該事件將在每天的指定時間觸發。

> 您可以將鍊式事件（見下文）與時間相關的事件結合使用來建立更多
事件中的隨機或頻繁動作。

(chained-events)=
### 連鎖事件

回撥可以立即或稍後呼叫其他事件。  它的潛力非常強大。

要使用鍊式事件，只需使用 `call_event` eventfunc。  它需要 2-3 個引數：

- 包含事件的物件。
- 要呼叫的事件的名稱。
- （可選）呼叫此事件之前等待的秒數。

所有物件都具有不是由指令或遊戲相關操作觸發的事件。  他們是
稱為“chain_X”，如“chain_1”、“chain_2”、“chain_3”等。  你可以給他們更具體的訊息
名稱，只要以“chain_”開頭即可，例如“chain_flood_room”。

與其進行冗長的解釋，讓我們來看一個例子：一條從一個地方到另一個地方的地鐵
下一個定期。  連線出口（開啟門），等一下，關閉它們，
繞了一圈，停在另一個車站。  這是一組非常複雜的回撥，因為它
是的，但我們只看開啟和關閉門的部分：

    call/add here = time 10:00

```python
# At 10:00 AM, the subway arrives in the room of ID 22.
# Notice that exit #23 and #24 are respectively the exit leading
# on the platform and back in the subway.
station = get(id=22)
to_exit = get(id=23)
back_exit = get(id=24)

# Open the door
to_exit.name = "platform"
to_exit.aliases = ["p"]
to_exit.location = room
to_exit.destination = station
back_exit.name = "subway"
back_exit.location = station
back_exit.destination = room

# Display some messages
room.msg_contents("The doors open and wind gushes in the subway")
station.msg_contents("The doors of the subway open with a dull clank.")

# Set the doors to close in 20 seconds
call_event(room, "chain_1", 20)
```

此回撥將：

1. 在 10:00 AM 被呼叫（指定 22:00 將其設為 10:00 PM）。
2. 在地鐵和車站之間設定一個出口。  請注意，出口已經存在（您將
不必建立它們），但它們不需要有特定的位置和目的地。
3. 在地鐵和月臺上顯示訊息。
4. 呼叫事件“chain_1”在20秒內執行。

現在，「chain_1」中應該有什麼？

    call/add here = chain_1

```python
# Close the doors
to_exit.location = None
to_exit.destination = None
back_exit.location = None
back_exit.destination = None
room.msg_content("After a short warning signal, the doors close and the subway begins moving.")
station.msg_content("After a short warning signal, the doors close and the subway begins moving.")
```

在幕後，`call_event` 函式凍結所有變數（「房間」、「車站」、「to_exit」、
在我們的範例中為“back_exit”），因此您無需再次定義它們。

關於呼叫鍊式事件的回呼的警告：回呼並非不可能呼叫
本身處於某種遞迴層級。  如果 `chain_1` 呼叫 `chain_2` 則呼叫 `chain_3` 則呼叫
`chain_`，特別是如果它們之間沒有暫停，您可能會遇到無限迴圈。

在處理可能在遊戲過程中移動的角色或物體時也要小心。
事件呼叫之間暫停。  當您使用 `call_event()` 時，MUD 不會暫停，指令可以
幸運的是，有玩家進入。  這也意味著，一個角色可以啟動一個暫停的事件
一段時間，但當呼叫鍊式事件時就消失了。  您需要檢查一下，即使 lock
當你暫停時角色就位（某些動作應該需要鎖定）或至少，
檢查角色是否仍在房間內，因為如果您這樣做，可能會造成不合邏輯的情況
不。

> 鍊式事件是一種特殊情況：與標準事件相反，它們是在遊戲中建立的，而不是
透過程式碼。  它們通常只包含一個回撥，儘管沒有什麼可以阻止您建立
 同一物件中的多個連鎖事件。

(using-events-in-code)=
## 在程式碼中使用事件

本節介紹程式碼中的回呼和事件、如何建立新事件以及如何呼叫它們
指令，以及如何處理引數等特定情況。

在本節中，我們將看到如何實作以下範例：我們想建立一個
“push”指令可用於推送物件。  物件可以對此指令做出反應並具有
觸發的特定事件。

(adding-new-events)=
### 新增事件

新增事件應該在您的 typeclasses 中完成。  事件包含在 `_events` 類別中
變數，事件名稱作為鍵的字典，以及將這些事件描述為值的元組。  你
還需要註冊這個類，告訴遊戲內的Python系統它包含要新增的事件
這typeclass。

在這裡，我們要在物件上新增「推送」事件。  在你的 `typeclasses/objects.py` 檔案中，你應該
寫一些類似的東西：

```python
from evennia.contrib.base_systems.ingame_python.utils import register_events
from evennia.contrib.base_systems.ingame_python.typeclasses import EventObject

EVENT_PUSH = """
A character push the object.
This event is called when a character uses the "push" command on
an object in the same room.

Variables you can use in this event:
    character: the character that pushes this object.
    obj: the object connected to this event.
"""

@register_events
class Object(EventObject):
    """
    Class representing objects.
    """

    _events = {
        "push": (["character", "obj"], EVENT_PUSH),
    }
```

- 第 1-2 行：我們從遊戲中的 Python 系統匯入一些我們需要的東西。  請注意，我們使用
`EventObject` 作為父級而不是 `DefaultObject`，如安裝所述。
- 第4-12行：我們通常將事件的幫助定義在一個單獨的變數中，這樣更具可讀性，
儘管沒有規則禁止以其他方式進行操作。  通常，幫助應該包含一個簡短的內容
單行解釋，多行較長解釋，然後是變數列表
並附有解釋。
- 第 14 行：我們在類別上呼叫裝飾器來指示它包含事件。  如果你不熟悉
使用裝飾器，您實際上不必擔心它，只需記住將這一行放在
如果您的類別包含事件，則位於類別定義之上。
- 第 15 行：我們建立繼承自 `EventObject` 的類別。
- 第 20-22 行：我們在 `_events` 類別變數中定義物件的事件。  它是一個
字典。  鍵是事件名稱。  值是一個元組，包含：
  - 變數名稱列表（str 列表）。  這將確定什麼時候需要什麼變數
    the event triggers.  These variables will be used in callbacks (as we'll see below).
  - 事件幫助（一個 str，我們在上面定義的那個）。

如果您新增此程式碼並重新載入遊戲，請建立一個物件並使用 `@call` 檢查其事件，您
應該在其幫助下看到“push”事件。  當然，目前該事件存在，但還沒有
被解僱了。

(calling-an-event-in-code)=
### 在程式碼中呼叫事件

遊戲中的 Python 系統可透過所有物件上的處理程式進行存取。  該處理程式名為 `callbacks`
並且可以從任何型別分類的物件（你的角色、房間、出口...）存取。  這個處理程式
提供了多種方法來檢查和呼叫該物件上的事件或回呼。

若要呼叫事件，請在物件中使用 `callbacks.call` 方法。  它作為引數：

- 要呼叫的事件的名稱。
- 事件中可作為位置引數存取的所有變數。  他們應該是
依照[建立新事件](#adding-new-events)時選擇的順序指定。

按照相同的範例，到目前為止，我們已經在所有物件上建立了一個事件，稱為「push」。  這個
事件暫時不會被觸發。  我們可以新增一個「push」指令，以名稱作為引數
一個物體的。  如果該物件有效，它將呼叫其“push”事件。

```python
from commands.command import Command

class CmdPush(Command):

    """
    Push something.

    Usage:
        push <something>

    Push something where you are, like an elevator button.

    """

    key = "push"

    def func(self):
        """Called when pushing something."""
        if not self.args.strip():
            self.msg("Usage: push <something>")
            return

        # Search for this object
        obj = self.caller.search(self.args)
        if not obj:
            return

        self.msg("You push {}.".format(obj.get_display_name(self.caller)))

        # Call the "push" event of this object
        obj.callbacks.call("push", self.caller, obj)
```

這裡我們使用 `callbacks.call` 和以下引數：

- `"push"`：要呼叫的事件的名稱。
- `self.caller`：按下按鈕的人（這是我們的第一個變數，`character`）。
- `obj`：被推送的物件（我們的第二個變數，`obj`）。

在物件的「push」回呼中，我們可以使用「character」變數（包含一個
誰推送了物件），以及「obj」變數（包含被推送的物件）。

(see-it-all-work)=
### 檢視一切工作

要檢視上面兩個修改（新增的事件和「push」指令）的效果，讓我們
建立一個簡單的物件：

    @create/drop rock
    @desc rock = It's a single rock, apparently pretty heavy.  Perhaps you can try to push it though.
    @call/add rock = push

在回撥中你可以這樣寫：

```python
from random import randint
number = randint(1, 6)
character.msg("You push a rock... is... it... going... to... move?")
if number == 6:
    character.msg("The rock topples over to reveal a beautiful ant-hill!")
```

現在你可以嘗試「推石頭」。  你會嘗試推石頭，六次就有一次，你會
看到一則關於「美麗的蟻丘」的訊息。

(adding-new-eventfuncs)=
### 新增新的事件函式

Eventfuncs，如 `deny()`，定義於
`contrib/base_systesm/ingame_python/eventfuncs.py`。  您可以新增自己的
eventfuncs 透過在 `world` 目錄中建立名為 `eventfuncs.py` 的檔案來實現。
在該檔案中定義的函式將作為幫助程式新增。

您還可以決定在另一個位置建立 eventfuncs，甚至在
幾個地點。  為此，請編輯您的 `EVENTFUNCS_LOCATION` 設定
`server/conf/settings.py` 檔案，指定 python 路徑或列表
定義輔助函式的 Python 路徑。  例如：

```python
EVENTFUNCS_LOCATIONS = [
        "world.events.functions",
]
```

(creating-events-with-parameters)=
### 使用引數建立事件

如果您想建立帶有引數的事件（如果您建立「耳語」或「詢問」指令，例如
例項，並且需要有一些字元自動對單字做出反應），您可以設定一個額外的
typeclass' `_events` 類別變數的事件元組中的引數。  這第三個論點
必須包含一個回撥，當事件發生時將呼叫該回撥來過濾回撥列表
火災。  常用的引數型別有兩種（但您可以定義更多引數型別，儘管
這超出了本文件的範圍）。

- 關鍵字引數：該事件的回呼將根據特定的關鍵字進行過濾。  這是
如果您希望使用者指定一個單字並將該單字與清單進行比較，則很有用。
- 短語引數：將使用整個短語並檢查其所有單字來過濾回撥。
「say」指令使用短語引數（您可以設定「say」回撥，以在短語出現時觸發）
包含一個特定的單字）。

在這兩種情況下，您都需要從以下位置匯入函式
`evennia.contrib.base_systems.ingame_python.utils` 並將其用作您的第三個引數
事件定義。

- `keyword_event` 應用於關鍵字引數。
- `phrase_event` 應用於短語引數。

例如，以下是「say」事件的定義：

```python
from evennia.contrib.base_systems.ingame_python.utils import register_events, phrase_event
# ...
@register_events
class SomeTypeclass:
    _events = {
        "say": (["speaker", "character", "message"], CHARACTER_SAY, phrase_event),
    }
```

當您使用`obj.callbacks.call`方法呼叫事件時，您也應該提供引數，
使用 `parameters` 關鍵字：

```python
obj.callbacks.call(..., parameters="<put parameters here>")
```

需要專門帶引數呼叫事件，否則系統不會
能夠知道如何過濾回撥清單。

(disabling-all-events-at-once)=
## 立即停用所有事件

例如，當回呼在無限迴圈中執行時，或將不需要的資訊傳送到
玩家或其他來源，作為遊戲管理員，您有權在沒有事件的情況下重新啟動。
執行此操作的最佳方法是在設定檔中使用自訂設定
(`server/conf/settings.py`):

```python
# Disable all events
EVENTS_DISABLED = True
```

遊戲中的 Python 系統仍然可以存取（您將可以存取 `call` 指令進行偵錯），
但不會自動呼叫任何事件。


```{toctree}
:hidden:

Contrib-Ingame-Python-Tutorial-Dialogue
Contrib-Ingame-Python-Tutorial-Elevator

```


----

<small>此檔案頁面是從`evennia\contrib\base_systems\ingame_python\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
