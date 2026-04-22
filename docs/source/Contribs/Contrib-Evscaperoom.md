(evscaperoom)=
# EvscapeRoom

Griatch 的貢獻，2019 年

用於在 Evennia 中建立多人逃脫室的完整引擎。允許玩家
生成並加入獨立追蹤其狀態的謎題房間。任意數量的玩家
可以一起解決房間問題。這是為“EvscapeRoom”建立的引擎，它贏得了
2019 年 4 月至 5 月舉行的 MUD Coders Guild“One Room”Game Jam。 contrib 僅
非常小的遊戲內容，它包含實用程式和基類以及一個空的範例房間。

(introduction)=
## 介紹

Evscaperoom，顧名思義，就是一個文字形式的【逃脫室】(https://en.wikipedia.org/wiki/Escape_room)。你開始被鎖定
一個房間，必須弄清楚如何出去。這contrib包含了一切
製作此類型別的全功能益智遊戲所需。它還包含一個
「大廳」用於建立新房間，允許玩家加入另一個人的房間
共同解決！

這是原版 _EvscapeRoom_ 的遊戲引擎。它
允許您重新建立相同的遊戲體驗，但它不包含任何
為遊戲即興創作的故事內容。如果你想看完整的比賽
（你必須逃離一個非常狡猾的小丑女孩的小屋，否則就會失去
村裡的吃派比賽...），你可以在Griatch的github頁面[這裡]（https://github.com/Griatch/evscaperoom）找到它，
（但建議的版本是用於在 Evennia 演示伺服器上執行的版本，該伺服器具有
更多錯誤修復，[此處](https://github.com/evennia/evdemo/tree/master/evdemo/evscaperoom))。

如果您想了解有關 _EvscapeRoom_ 是如何建立和設計的更多資訊，您可以閱讀
開發部落格，[第 1 部分](https://www.evennia.com/devblog/2019.html#2019-05-18-creating-evscaperoom-part-1) 和 [第 2 部分](https://www.evennia.com/devblog/2019.html#2019-05-26-creating-evscaperoom-part-2)。

(installation)=
## 安裝

透過將 `evscaperoom` 指令新增到您的
字元cmdset。當您在遊戲中執行該指令時，您就可以開始玩了！

在`mygame/commands/default_cmdsets.py`中：

```python

from evennia.contrib.full_systems.evscaperoom.commands import CmdEvscapeRoomStart

class CharacterCmdSet(...):

  # ...

  self.add(CmdEvscapeRoomStart())

```

重新載入伺服器，`evscaperoom` 指令將可用。 contrib
以配備小型（非常小的）逃脫室為例。

(making-your-own-evscaperoom)=
## 打造自己的逃脫室

為此，您需要建立自己的狀態。首先確保您可以玩
上面安裝的簡單範例房間。

將 `evennia/contrib/full_systems/evscaperoom/states` 複製到遊戲資料夾中的某個位置（讓我們
假設您將其放在 `mygame/world/` 下）。

接下來，您需要重新指向 Evennia 以在這個新位置找到狀態。新增
將以下內容新增至您的 `mygame/server/conf/settings.py` 檔案：

```python
  EVSCAPEROOM_STATE_PACKAGE = "world.states"

```

重新載入，範例 evscaperoom 應該仍然可以工作，但您現在可以修改並
從您的遊戲目錄中展開它！

(other-useful-settings)=
### 其他有用的設定

還有一些其他可能有用的設定：

- `EVSCAPEROOM_START_STATE` - 預設為 `state_001_start` 且是名稱
從其開始的狀態模組（不帶`.py`）。如果您可以更改此設定
  想要一些其他的命名方案。
- `HELP_SUMMARY_TEXT` - 這是輸入 `help` 時顯示的幫助簡介
房間沒有爭論。原文位於頂部
  `evennia/contrib/full_systems/evscaperoom/commands.py`。

(playing-the-game)=
## 玩遊戲

您應該從`look`周圍和物體開始。

`examine <object>` 指令允許您「聚焦」某個物件。當你這樣做時
您將學習可以針對您關注的物件嘗試的操作，例如
轉動它，閱讀上面的文字或將其與其他物體一起使用。請注意
多個玩家可以專注於同一物件，因此您不會阻止任何人
當你集中註意力時。聚焦在另一個物件或再次使用 `examine` 將刪除
焦點。

還有一個完整的提示系統。

(technical)=
## 技術的

連線到遊戲時，使用者可以選擇加入現有房間
（可能已經處於某種持續進展的狀態），或者可能創造一個新的
為他們提供了開始自己解決問題的空間（但任何人都可以稍後加入他們）。

隨著玩家的進展，房間將經歷一系列“狀態”
它的挑戰。這些狀態被描述為.states/ 中的模組，並且
room 將載入並執行每個模組內的狀態物件以進行設定
並隨著玩家的進步在狀態之間進行轉換。這允許隔離
彼此之間的狀態，並有望使其更容易跟蹤
邏輯並（原則上）稍後注入新的謎題。

一旦沒有玩家留在房間中，房間及其狀態將被擦除。

(design-philosophy)=
## 設計理念

一些基本前提啟發了這個設計。

- 你應該能夠獨自解決房間問題。所以任何謎題都不需要
多個玩家的協作。這只是因為無從得知
  其他人是否在給定時間實際上線上（或始終保持線上）。
- 你不應該被其他玩家的作為/不作為所阻礙。這
這就是為什麼你不能拿起任何東西（沒有庫存系統），但只能
  聚焦/操作專案。這避免了玩家接聽的煩人情況
  拼圖的關鍵部分，然後登出。
- 每個人的房間狀態都會立即改變。我的第一個想法是給定一個
房間有不同的狀態取決於誰看（所以箱子可以開啟
  並且同時對兩個不同的玩家關閉）。但這不僅
  增加了很多額外的複雜性，它也違背了擁有多個的目的
  玩家。這樣人們就可以像「真實」一樣互相幫助和協作
  逃生室。對於那些想自己做這一切的人來說，我做到了
  輕鬆啟動“新鮮”房間供他們使用。

所有其他設計決策都源自於這些。


----

<small>此檔案頁面是從`evennia\contrib\full_systems\evscaperoom\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
