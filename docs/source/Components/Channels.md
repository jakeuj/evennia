(channels)=
# 頻道

在多人遊戲中，玩家通常需要其他遊戲內交流方式
比移動到同一個房間並使用 `say` 或 `emote` 更好。

_Channels_ 允許 Evennia's 充當精美的聊天程式。當一個玩家在
連線到某個頻道，向該頻道傳送訊息會自動分發
將其傳送給所有其他訂閱者。

頻道既可用於[帳號](./Accounts.md)之間的聊天，也可用於[帳號](./Accounts.md)之間的聊天
[物件](./Objects.md)（通常是字元）。  聊天可能都是 OOC
（不符合性格）或 IC （符合性格）。  一些例子：

- 聯絡員工的支援管道 (OOC)
- 用於討論任何事情和培養社群的一般聊天 (OOC)
- 私人員工討論的管理頻道 (OOC)
- 用於規劃和組織的私人公會頻道（IC/OOC取決於遊戲）
- 賽博龐克風格的復古聊天室（IC）
- 遊戲內廣播頻道 (IC)
- 群體心靈感應(IC)
- 對講機 (IC)

```{versionchanged} 1.0

  Channel system changed to use a central 'channel' command and nicks instead of
  auto-generated channel-commands and -cmdset. ChannelHandler was removed.

```

(working-with-channels)=
## 使用管道

(viewing-and-joining-channels)=
### 檢視和加入頻道

在預設的指令集中，通道都是透過強大的[通道指令]（evennia.commands.default.comms.CmdChannel）、`channel`（或`chan`）來處理的。  預設情況下，該指令將假定所有處理通道的實體都是`Accounts`。

觀看頻道

    channel       - shows your subscriptions
    channel/all   - shows all subs available to you
    channel/who   - shows who subscribes to this channel

若要加入/取消訂閱頻道，請執行下列操作

    channel/sub channelname
    channel/unsub channelname

如果您暫時不想聽該頻道一段時間（實際上沒有
取消訂閱），您可以將其靜音：

    channel/mute channelname
    channel/unmute channelname

(talk-on-channels)=
### 在頻道上談論

若要在頻道上發言，請執行以下操作

    channel public Hello world!

如果頻道名稱中有空格，則需要使用「`=`」：

    channel rest room = Hello world!

現在，輸入的內容比我們想要的內容要多，因此當您加入頻道時，
系統會自動設定個人別名，因此您可以這樣做：

    public Hello world

```{warning}

如果頻道名稱中包含空格，則此捷徑將無法運作。
  因此，名稱較長的頻道應確保提供一個單字別名，如下所示
  好吧。
```

任何使用者都可以建立自己的頻道別名：

    channel/alias public = foo;bar

你現在可以做

    foo Hello world!
    bar Hello again!

如果他們不想使用預設的，甚至可以刪除它

    channel/unalias public
    public Hello    (gives a command-not-found error now)

但您也可以透過 `channel` 指令使用別名：

    channel foo Hello world!

> 當使用別名時會發生什麼，建立一個 [nick](./Nicks.md) 來對映您的
> 別名 + 引數呼叫 `channel` 指令。所以當你輸入`foo hello`時，
> 伺服器看到的實際上是`channel foo = hello`。該系統還
> 足夠聰明，知道每當您搜尋頻道時，您的頻道暱稱
> 還應該考慮將您的輸入轉換為現有的頻道名稱。

您可以透過檢視頻道的
向後滾動

    channel/history public

這會檢索最後 20 行文字（也來自您之前的時間）
離線）。您可以透過指定傳回開始的行數來進一步後退：

    channel/history public = 30

這再次檢索 20 行，但從 30 行開始（所以你會得到幾行
倒數 30-50）。


(channel-administration)=
### 通路管理

Evennia啟動時可以建立某些頻道。頻道還可以
在遊戲中即時建立。

(default-channels-from-settings)=
#### 設定中的預設頻道

您可以指定要從 Evennia 自動建立的「預設」頻道
設定。如果符合以下條件，新帳戶將自動訂閱此類「預設」頻道：
他們擁有正確的許可權。這是每個頻道一個字典的清單（範例是預設公共頻道）：

```python
# in mygame/server/conf/settings.py
DEFAULT_CHANNELS = [ 
	{
         "key": "Public",
         "aliases": ("pub",),
         "desc": "Public discussion",
         "locks": "control:perm(Admin);listen:all();send:all()",
     },
]
```

每個字典都以 `**channeldict` 饋送到 [create_channel](evennia.utils.create.create_channel) 函式中，因此支援所有相同的關鍵字。

Evennia還有兩個與系統相關的通道：
 
- `CHANNEL_MUDINFO` is a dict describing the "MudInfo" channel.假設它存在，並且是 Evennia 回顯重要伺服器資訊的地方。這個想法是伺服器管理員和工作人​​員可以訂閱此頻道以隨時瞭解最新情況。
- 預設未定義`CHANNEL_CONECTINFO`。它將接收連線/斷開連線訊息，並且普通玩家也可以看到。如果沒有給出，連線資訊將被悄悄記錄。

(managing-channels-in-game)=
#### 管理遊戲中的頻道

若要動態建立/銷毀新頻道，您可以執行下列操作

    channel/create channelname;alias;alias = description
    channel/destroy channelname

別名是可選的，但對於每個人都可能想要的明顯快捷方式很有用
使用。此描述用於頻道清單中。您將自動加入
您建立的頻道並將控制它。您也可以使用 `channel/desc` 來
稍後更改您擁有的頻道的描述。

如果您控制某個頻道，您也可以將其他人踢出該頻道：

    channel/boot mychannel = annoyinguser123 : stop spamming!

最後一部分是在使用者啟動之前傳送給使用者的可選原因。
您可以提供以逗號分隔的頻道列表，以將同一使用者從所有頻道中踢出
立即這些頻道。使用者將從頻道取消訂閱，並且所有
他們的別名將被刪除。但如果他們願意，他們仍然可以重新加入。

    channel/ban mychannel = annoyinguser123
    channel/ban      - view bans
    channel/unban mychannel = annoyinguser123

禁止將使用者加入頻道黑名單。這意味著他們不會
如果您啟動它們，您可以_重新加入_。您需要執行 `channel/boot` 才能
實際上把他們踢出去了。

有關更多詳細資訊，請參閱[頻道指令](evennia.commands.default.comms.CmdChannel) api 檔案（和遊戲內幫助）。

管理員級使用者也可以修改頻道的[鎖定](./Locks.md)：

    channel/lock buildchannel = listen:all();send:perm(Builders)

通道預設使用三種lock型別：

- `listen` - 誰可以收聽該頻道。沒有此存取許可權的使用者將不會
即使能夠加入頻道，它也不會出現在他們的清單中。
- `send` - 誰可以傳送到頻道。
- `control` - 這是在您建立頻道時自動分配給您的。和
控制頻道，您可以對其進行編輯、引導使用者以及執行其他管理任務。


(restricting-channel-administration)=
#### 限制通路管理

預設情況下，每個人都可以使用頻道指令（[evennia.commands.default.comms.CmdChannel](evennia.commands.default.comms.CmdChannel)）來建立頻道，然後控制他們建立的頻道（以引導/禁止人員等）。如果您作為開發人員不希望普通玩家執行此操作（也許您希望只有工作人員能夠產生新頻道），您可以覆蓋 `channel` 指令並更改其 `locks` 屬性。

預設 `help` 指令具有以下 `locks` 屬性：

```python
    locks = "cmd:not perm(channel_banned); admin:all(); manage:all(); changelocks: perm(Admin)"
```

這是一個常規的[鎖定字串](./Locks.md)。

- `cmd: pperm(channel_banned)` - `cmd` 鎖定型別是用於所有指令的標準鎖定型別。
失敗的存取物件甚至不知道該指令存在。 `pperm()` lockfunc
  檢查分期付款 [許可權](Building Permissions) 'channel_banned' - `not` 表示
  如果他們_擁有_該“許可權”，他們將無法使用 `channel` 指令。你通常
  不需要改變這個lock。
- `admin:all()` - 這是在 `channel` 指令本身中檢查的 lock。它控制對
`/boot`、`/ban` 和 `/unban` 開關（預設讓每個人都使用它們）。
- `manage:all()` - 這控制對 `/create`、`/destroy`、`/desc` 開關的存取。
- `changelocks: perm(Admin)` - 這控制對 `/lock` 和 `/unlock` 開關的存取。經過
預設情況下，只有[管理員](Building Permissions) 可以更改。

> 注意 - 雖然 `admin:all()` 和 `manage:all()` 會讓每個人都使用這些開關，但使用者
> 仍然只能管理或銷毀他們實際控制的頻道！

如果您只想（例如）建構者及更高版本能夠建立和管理
您可以覆蓋 `help` 指令並將鎖定字串變更為：

```python
  # in for example mygame/commands/commands.py

  from evennia import default_cmds

  class MyCustomChannelCmd(default_cmds.CmdChannel):
      locks = "cmd: not pperm(channel_banned);admin:perm(Builder);manage:perm(Builder);changelocks:perm(Admin)"

```

將此自訂指令新增至預設cmdset，普通使用者現在將獲得
嘗試使用這些開關時出現存取被拒絕錯誤。

(using-channels-in-code)=
## 在程式碼中使用通道

對於大多數常見的更改，預設通道、接收者掛鉤以及可能的
覆蓋 `channel` 指令會讓你走得很遠。但你也可以調整
渠道本身。

(allowing-characters-to-use-channels)=
### 允許角色使用頻道

預設 `channel` 指令 ([evennia.commands.default.comms.CmdChannel](evennia.commands.default.comms.CmdChannel)) 位於 `Account` [指令集](./Command-Sets.md) 中。它被設定為始終在 `Accounts` 上執行，即使您將其新增到 `CharacterCmdSet` 也是如此。

只需一行變更即可使該指令接受非帳戶呼叫者。但為了方便起見，我們提供了字元/物件的版本。只需匯入 [evennia.commands.default.comms.CmdObjectChannel](evennia.commands.default.comms.CmdObjectChannel) 並從中繼承即可。

(customizing-channel-output-and-behavior)=
### 自訂通道輸出和行為

當分發訊息時，通道會呼叫自身的一系列鉤子
（更重要的是）每個收件者。所以你可以透過以下方式自訂很多東西
只需修改正常物件/帳戶 typeclasses 上的掛鉤即可。

在內部，訊息透過
`channel.msg(message, senders=sender, bypass_mute=False, **kwargs)`，其中
`bypass_mute=True` 表示該訊息忽略靜音（適用於警報或如果您
刪除頻道等）和 `**kwargs` 是您可能想要傳遞的任何額外訊息
到鉤子。 `senders`（在預設實作中始終只有一個）
但原則上可以是多個）並且 `bypass_mute` 是 `kwargs` 的一部分
下面：

  1. `channel.at_pre_msg(message, **kwargs)`
  2. 對於每位收件者：
      - `message = recipient.at_pre_channel_msg(message, channel, **kwargs)` -
         allows for the message to be tweaked per-receiver (for example coloring it depending
         on the users' preferences). If this method returns `False/None`, that
         recipient is skipped.
      - `recipient.channel_msg(message, channel, **kwargs)` - actually sends to recipient.
      - `recipient.at_post_channel_msg(message, channel, **kwargs)` - any post-receive effects.
  3. `channel.at_post_channel_msg(message, **kwargs)`

請注意，`Accounts` 和 `Objects` 都有各自獨立的鉤子組。
因此，請確保修改訂閱者（或兩者）實際使用的集合。
預設頻道均使用 `Account` 訂閱者。

(channel-class)=
### 頻道類

通道是[型別分類](./Typeclasses.md)實體。這意味著它們在資料庫中是持久的，可以具有[屬性](./Attributes.md)和[Tags](./Tags.md)並且可以輕鬆擴充套件。

若要變更 typeclass Evennia 用於預設指令的頻道，請變更 `settings.BASE_CHANNEL_TYPECLASS`。基本指令類別是 [`evennia.comms.comms.DefaultChannel`](evennia.comms.comms.DefaultChannel)。 `mygame/typeclasses/channels.py` 中有一個空子類，與其他 typelass-base 相同。

在程式碼中，您使用 `evennia.create_channel` 建立一個新通道或
`Channel.create`：

```python
  from evennia import create_channel, search_object
  from typeclasses.channels import Channel

  channel = create_channel("my channel", aliases=["mychan"], locks=..., typeclass=...)
  # alternative
  channel = Channel.create("my channel", aliases=["mychan"], locks=...)

  # connect to it
  me = search_object(key="Foo")[0]
  channel.connect(me)

  # send to it (this will trigger the channel_msg hooks described earlier)
  channel.msg("Hello world!", senders=me)

  # view subscriptions (the SubscriptionHandler handles all subs under the hood)
  channel.subscriptions.has(me)    # check we subbed
  channel.subscriptions.all()      # get all subs
  channel.subscriptions.online()   # get only subs currently online
  channel.subscriptions.clear()    # unsub all

  # leave channel
  channel.disconnect(me)

  # permanently delete channel (will unsub everyone)
  channel.delete()

```

頻道的 `.connect` 方法將接受 `Account` 和 `Object` 訂閱者
並將透明地處理它們。

該通道還有更多鉤子，這兩個鉤子與所有 typeclasses 共享，以及與靜音/禁止等相關的特殊鉤子。請參閱通道類
詳細資訊。

(channel-logging)=
### 頻道記錄

```{versionchanged} 0.7

  Channels changed from using Msg to TmpMsg and optional log files.
```
```{versionchanged} 1.0

  Channels stopped supporting Msg and TmpMsg, using only log files.
```

頻道訊息不會儲存在資料庫中。相反，通道始終記錄到常規文字日誌檔案 `mygame/server/logs/channel_<channelname>.log`。這是 `channels/history channelname` 獲取資料的地方。當頻道的日誌變得太大時，它會輪換，這也會自動限制使用者可以檢視的最大歷史記錄量
`/history`。

日誌檔案名稱在通道類別上設定為 `log_file` 屬性。這個
是一個字串，它將格式化標記 `{channelname}` 替換為
頻道的（小寫）名稱。預設情況下，日誌寫入
通道的 `at_post_channel_msg` 方法。

(properties-on-channels)=
### 通道屬性

通道具有型別分類實體的所有標準屬性（`key`，
`aliases`、`attributes`、`tags`、`locks` 等）。這並不是一份詳盡的清單；
有關詳細資訊，請參閱[頻道 API 檔案](evennia.comms.comms.DefaultChannel)。

- `send_to_online_only` - 此類布林值預設為 `True` 且是
明智的最佳化，因為離線的人無論如何都不會看到該訊息。
- `log_file` - 這是一個確定通道日誌檔案名稱的字串。預設
是`"channel_{channelname}.log"`。日誌檔案將出現在`settings.LOG_DIR`中（通常
  `mygame/server/logs/`）。您通常不應更改此設定。
- `channel_prefix_string` - 此屬性是一個字串，可輕鬆變更方式
該頻道是有字首的。它採用 `channelname` 格式鍵。預設為`"[{channelname}] "`
  並產生類似 `[public]...` 的輸出。
- `subscriptions` - 這是 [SubscriptionHandler](evennia.comms.models.SubscriptionHandler)，
具有方法 `has`、`add`、`remove`、`all`、`clear` 以及 `online`（獲取
  僅實際線上通路成員）。
- `wholist`、`mutelist`、`banlist` 是返回訂閱者清單的屬性，
以及目前被靜音或禁止的人。
- `channel_msg_nick_pattern` - 這是用於執行就地缺刻的正規表示式模式
替換（檢測 `channelalias <msg` 表示您想要向通道傳送訊息）。
  此模式接受 `{alias}` 格式標記。不要搞亂這個，除非你真的
  想要改變通路的運作方式。
- `channel_msg_nick_replacement` - 這是 [nick replacement] 上的字串
- 形式](./Nicks.md)。它接受`{channelname}`格式tag。這與
`channel` 指令，預設為 `channel {channelname} = $1`。

值得注意的 `Channel` 鉤子：

- `at_pre_channel_msg(message, **kwargs)` - 在傳送訊息之前呼叫，以
修改它。預設不使用。
- `msg(message, senders=..., bypass_mute=False, **kwargs)` - 將訊息傳送到
頻道。 `**kwargs` 被傳遞到其他呼叫掛鉤（也在接收者上）。
- `at_post_channel_msg(message, **kwargs)` - 預設用於儲存訊息
到日誌檔。
- `channel_prefix(message)` - 呼叫它是為了允許通道新增字首。這就是所謂的
在建立訊息時透過物件/帳戶，所以如果想要其他東西，可以
  也只是刪除該呼叫。
- 每個頻道的訊息。預設情況下它只回傳`channel_prefix_string`。
- `has_connection(subscriber)` - 檢查實體是否訂閱的捷徑
這個頻道。
- `mute/unmute(subscriber)` - 這會使該使用者的頻道靜音。
- `ban/unban(subscriber)` - 從禁止清單中新增/刪除使用者。
- `connect/disconnect(subscriber)` - 新增/刪除訂閱者。
- `add_user_channel_alias(user, alias, **kwargs)` - 為此頻道設定使用者暱稱。這是
什麼對映e.g。 `alias <msg>` 至 `channel channelname = <msg>`。
- `remove_user_channel_alias(user, alias, **kwargs)` - 刪除別名。請注意，這是
一個類別方法，它將愉快地從連結到 _any_ 的使用者中刪除找到的頻道別名
  通道，不僅僅是從呼叫該方法的通道。
- `pre_join_channel(subscriber)` - 如果返回 `False`，連線將被拒絕。
- `post_join_channel(subscriber)` - 預設情況下，這會設定使用者的頻道暱稱/別名。
- `pre_leave_channel(subscriber)` - 如果返回`False`，則不允許使用者離開。
- `post_leave_channel(subscriber)` - 這將清除使用者的所有頻道別名/暱稱。
- `delete`標準typeclass-刪除機制也會自動取消訂閱所有
訂閱者（從而擦除他們所有的別名）。

