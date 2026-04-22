(using-commands-and-building-stuff)=
# 使用指令和建立東西

在本課中，我們將測試我們可以在遊戲中開箱即用地執行哪些操作。 Evennia 附帶
[大約 90 個預設指令](../../../Components/Default-Commands.md)，雖然您可以隨意覆寫這些指令，但預設值可能非常有用。

連線並登入您的新遊戲。你會發現自己處於「地獄邊境」位置。這個
是此時遊戲中唯一的房間。讓我們稍微探討一下預設指令。

預設指令的語法[類似MUX](../../../Coding/Default-Command-Syntax.md)：

     command[/switch/switch...] [arguments ...]

一個例子是：

     create/drop box

_/switch_ 是一個特殊的可選標誌，用於使指令表現不同。開關始終直接放在指令名稱後面，並以正斜線 (`/`) 開頭。 _引數_是指令的一個或多個輸入。將某些內容分配給物件時，通常會使用等號 (`=`)。

> 您是否習慣以@開頭的指令，例如@create？那也行。 Evennia 簡單地忽略前面的@。

(getting-help)=
## 尋求協助

    help

將為您提供所有可用指令的清單。使用

    help <commandname>

檢視該指令的遊戲內幫助。

(looking-around)=
## 環顧四周

最常見的指令是

    look

這將顯示當前位置的描述。 `l` 是look 指令的別名。

當在指令中定位物件時，您可以使用兩個特殊標籤：`here` 表示目前房間，或 `me`/`self` 指向您自己。因此，

    look me

將為您提供您自己的描述。在這種情況下，`look here` 與普通的 `look` 相同。


(stepping-down-from-godhood)=
## 從神位退下來

如果您剛安裝了Evennia，您的第一個玩家帳號稱為使用者#1 –也稱為_超級使用者_或_上帝使用者_。這個使用者很厲害——如此強大以至於它可以超越許多遊戲限制（例如鎖）。這可能很有用，但它也隱藏了您可能想要測試的一些功能。

若要暫時退出超級使用者位置，您可以在遊戲中使用 `quell` 指令：

    quell

這將使您開始使用目前角色等級的許可權，而不是超級使用者等級的許可權。如果您沒有更改任何設定，您的初始遊戲角色應該具有_開發者_級別許可權 –在不像超級使用者那樣繞過鎖的情況下盡可能高。這對於本頁上的範例來說效果很好。使用

    unquell

完成後再次獲得超級使用者狀態。

(creating-an-object)=
## 建立物件

基本物件可以是任何東西——劍、花和非玩家角色。它們是使用 `create` 指令建立的。例如：

    create box

這會在您的庫存中建立一個新的「盒子」（預設物件型別）。使用指令`inventory`（或`i`）檢視它。現在，「box」是一個相當短的名稱，所以讓我們重新命名它並新增一些別名：

    name box = very large box;box;very;crate

```{warning} MUD 用戶端和分號：
一些傳統的 MUD 用戶端使用分號 `;` 來分隔用戶端輸入。如果是這樣，上面的行將給出錯誤，您需要更改用戶端以使用另一個指令分隔符號或將其置於「逐字」模式。如果仍然遇到問題，請改用 Evennia Web 使用者端。
```

我們現在已將該盒子重新命名為“非常大的盒子”——這就是我們在觀察它時將看到的。但是，我們也可以透過我們為上面的 name 指令提供的任何其他名稱來識別它（i.e.、_crate_ 或像以前一樣簡單地使用 _box_）。我們也可以在初始 `create` 物件指令中直接在名稱後面給出這些別名。對於所有建立指令都是如此 –您始終可以為新物件的名稱提供 `;` 分隔的別名清單。在我們的範例中，如果您不想更改框物件的名稱本身，而只想新增別名，則可以使用 `alias` 指令。

在搭建教學的此時，我們的角色正在攜帶盒子。讓我們放棄它：

    drop box

嘿，快點，&mdash;它就在地面上，一切正常。還有一種快捷方式可以使用 `/drop` 開關（e.g、`create/drop box`）一次性建立和刪除物件。

讓我們仔細看看我們的新盒子：

    examine box

檢查指令將顯示有關框物件的一些技術細節。現在，我們將忽略這是什麼
資訊手段。

嘗試在框中輸入 `look` 以檢視（預設）描述：

    > look box
    You see nothing special.

預設的描述不是很令人興奮。讓我們來新增一些味道：

    desc box = This is a large and very heavy box.

如果您嘗試`get`指令，我們將撿起盒子。到目前為止，一切都很好。但是，如果我們真的希望這是一個又大又重的盒子，人們就不應該那麼容易帶著它逃跑。為了防止這種情況，我們必須將其lock下來。這是透過為其分配_lock_來完成的。 TO這樣做，首先確保盒子被扔到房間裡，然後使用lock指令：

    lock box = get:false()

鎖代表了一個相當[大的主題](../../../Components/Locks.md)，但是現在，這將實現我們想要的。上面的指令將lock這個盒子，這樣就沒有人可以抬起它——但有一個例外。請記住，超級使用者會覆蓋所有鎖，並且無論如何都會拿起它。確保您正在取消超級使用者許可權，然後嘗試再次取得它：

    > get box
    You can't get that.

認為這個預設錯誤訊息看起來很乏味嗎？ `get` 指令尋找名為 `get_err_msg` 的 [Attribute](../../../Components/Attributes.md) 以自訂錯誤訊息傳回。我們使用 `set` 指令設定屬性：

    set box/get_err_msg = It's way too heavy for you to lift.

現在嘗試獲取該框，您應該會看到一條更相關的錯誤訊息回顯給您。將來要檢視該訊息字串是什麼，可以使用「檢查」。

    examine box/get_err_msg

`Examine` 將傳回屬性值，包括顏色程式碼。例如，`examine here/desc` 將傳回目前房間的原始描述（包括顏色程式碼），以便您可以複製並貼上以將其描述設為其他內容。

您建立新指令 –或修改現有的－在遊戲外的Python程式碼中。我們稍後將在[指令教學](./Beginner-Tutorial-Adding-Commands.md) 中探討這樣做。

(get-a-personality)=
## 獲得個性

[Scripts](../../../Components/Scripts.md) 是強大的異常物件，對許多「幕後」事物很有用。他們的可選能力之一是按計時器做事。為了嘗試我們的第一個 script，讓我們將其應用到我們自己身上。 `evennia/contrib/tutorials/bodyfunctions/bodyfunctions.py` 中有一個範例 script 稱為 `BodyFunctions`。要將其新增到我們自己中，我們可以使用 `script` 指令：

    script self = tutorials.bodyfunctions.BodyFunctions

上面的字串告訴Evennia在我們指定的地方挖掘Python程式碼。它已經知道要查詢 `contrib/` 資料夾，因此我們不必提供完整路徑。

> 另請注意我們如何使用 `.` 而不是 `/`（或 Windows 上的 `\`）。這個約定就是所謂的「Python 路徑」。在 Python 路徑中，您可以使用 `.` 分隔路徑的各個部分，並跳過 `.py` 檔案結尾。重要的是，它還允許您指向 Python 程式碼_內部_檔案，如我們的範例所示，其中 `BodyFunctions` 類位於 `bodyfunctions.py` 檔案內部。我們稍後再去上課。這些「Python 路徑」在 Evennia 中被廣泛使用。

等一會兒，你會發現自己開始進行隨機觀察...

    script self =

上面的指令將顯示給定物件（在本例中是您自己）上有關 scripts 的詳細資訊。 `examine` 指令也包含此類詳細資訊。

您將看到距離下次「觸發」還有多長時間。如果倒數計時達到零時沒有任何反應，請不要驚慌 –這個特定的 script 有一個隨機發生器來確定它是否會說些什麼。所以你不會在每次觸發時看到輸出。

當您厭倦了角色的「見解」時，請使用以下指令停止 script：

    script/stop self = tutorials.bodyfunctions.BodyFunctions

您可以在遊戲之外用 Python 建立自己的scripts；您給 `script` 的路徑實際上是 script 檔案的 Python 路徑。 [Scripts](../../../Components/Scripts.md) 頁面說明瞭更多詳細資訊。

(pushing-your-buttons)=
## 按下你的按鈕

如果我們回到我們製作的盒子，此時您能享受到的樂趣就只有這麼多了。它只是一個愚蠢的通用物件。如果您將其重新命名為 `stone` 並更改了其描述，那麼沒有人會更明智。然而，結合使用自訂的[Typeclasses](../../../Components/Typeclasses.md)、[Scripts](../../../Components/Scripts.md)和基於物件的[指令](../../../Components/Commands.md)，您可以擴充套件它——和其他物品——隨心所欲地變得獨特、複雜和互動。

So, let's work though just such an example.到目前為止，我們只建立了使用預設物件 typeclass 的物件，簡單命名為 `Object`。讓我們建立一個更有趣的物件。下
`evennia/contrib/tutorials` there is a module `red_button.py`. It contains the enigmatic `RedButton` class.

讓我們成為其中的一員吧！

    create/drop button:tutorials.red_button.RedButton

使用 Python-path 輸入上述指令，然後就可以了 -一個紅色按鈕！如前面的 Script 範例一樣，我們指定了希望 Evennia 用於建立物件的 Python 程式碼的 Python 路徑。

RedButton 是一個範例物件，旨在展示 Evennia 的一些功能。你會發現控制它的[Typeclass](../../../Components/Typeclasses.md)和[指令](../../../Components/Commands.md)在[evennia/contrib/tutorials/red_button](../../../api/evennia.contrib.tutorials.red_button.md)裡面。

如果您等待一段時間（確保您已將其放下！），該按鈕將閃爍迷人。

為什麼不嘗試推動它...？

當然，應該按下一個紅色的大按鈕。

你知道你想要。

```{warning} 不要按下那個閃爍著誘人光芒的紅色按鈕。
```

(making-yourself-a-house)=
## 為自己打造一棟房子

塑造遊戲世界的主要指令是`dig`。例如，如果你站在地獄邊境，你可以像這樣挖掘一條通往新房子位置的路線：

    dig house = large red door;door;in,to the outside;out

上面的指令將建立一個名為「house」的新房間。它還會在你目前位置建立一個名為“大紅門”的出口，並在新房間中建立一個名為“到外面”的相應出口，通往地獄邊境。在上面，我們也為這些出口定義了一些別名，以便玩家不需要輸入完整的出口名稱。

如果您想使用常規羅盤方向（北、西、西南等），您也可以使用 `dig` 來實現。但是，Evennia 還具有 `dig` 的專用版本，可協助確定基本方向（以及上/下和進/出）。它被稱為`tunnel`：

    tunnel sw = cliff

這將建立一個名為“懸崖”的新房間，有一個通往那裡的“西南”出口，以及一條從懸崖返回到您當前位置的“東北”路徑。

您可以使用 `open` 指令從您所在的位置建立新的出口：

    open north;n = house

這將開啟通往先前建立的房間 `house` 的出口 `north`（具有別名 `n`）。

如果您有多個名為 `house` 的房間，您將獲得一份匹配列表，並且必須選擇要連結到的特定房間。

接下來，沿著北出口向北步行到您的“房子”。你也可以`teleport`到它：

    north

或者：

    teleport house

若要手動開啟返回 Limbo 的出口（如果您沒有使用 `dig` 指令自動執行此操作）：

    open door = limbo

（你也可以使用 Limbo 的 `#dbref`，當你站在 Limbo 中時，可以使用 `examine here` 找到它。）

(reshuffling-the-world)=
## 重新洗牌世界

假設您回到`Limbo`，讓我們將_大盒子_傳送到我們的`house`：

    teleport box = house
        very large box is leaving Limbo, heading for house.
        Teleported very large box -> house.

你可以透過使用`find`指令來找出遊戲世界中的東西，例如我們的`box`：

    find box
        One Match(#1-#8):
        very large box(#8) - src.objects.objects.Object

知道了盒子的`#dbref`（本例中為#8），你就可以抓住盒子並將其放回此處，而無需實際先去`house`：

    teleport #8 = here

如前所述，`here` 是“您當前位置”的別名。盒子現在應該和你一起回到 Limbo 了。

我們已經厭倦了盒子。讓我們摧毀它：

    destroy box

發出 `destroy`` 指令將要求您確認。 Once you confirm, the box will be gone.

透過向指令提供以逗號分隔的物件清單（或 `#dbrefs` 範圍，如果它們不在同一位置），您可以一次性`destroy`多個物件。

(adding-a-help-entry)=
## 新增幫助條目

與指令相關的 `help` 條目是您在 Python 程式碼中修改的內容 –當我們解釋如何新增指令時，我們將介紹這一點 –但您也可以新增非指令相關的說明條目。例如，解釋一下你的遊戲世界的歷史：

    sethelp History = At the dawn of time ...

現在，您將在 `help` 清單中找到新的 `History` 條目，並且可以使用 `help History` 閱讀說明文字。

(adding-a-world)=
## 增加一個世界

在簡要介紹了建立和使用遊戲內指令之後，您可能已經準備好看到更充實的範例了。幸運的是，Evennia 附帶了一個教學世界供您探索 –我們將在下一課中嘗試。
