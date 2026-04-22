(contribs)=
# Contribs

```{sidebar} 更多貢獻
可以找到額外的 Evennia 程式碼片段和貢獻
在[社群Contribs和片段][forum]論壇中。
```
_Contribs_ 是可選的程式碼片段和系統貢獻者
Evennia 社群。它們的大小和複雜性各不相同
可能比「核心」Evennia 更具體地說明遊戲型別和風格。
此頁面是自動產生的，總結了目前包含的所有 **53** contribs
具有 Evennia 分佈。

所有contrib類別均從`evennia.contrib`匯入，例如

    from evennia.contrib.base_systems import building_menu

每個contrib都包含有關如何整合它的安裝說明
與你的其他程式碼。如果你想調整 contrib 的程式碼，只需
將其整個資料夾複製到您的遊戲目錄並從那裡修改/使用它。

如果您想加contrib，請參閱[contrib指南](./Contribs-Guidelines.md)！

[forum]: https://github.com/evennia/evennia/discussions/categories/community-contribs-snippets

(index)=
## 指數
| | | | | | | |
|---|---|---|---|---|---|---|
| [base_systems](#base_systems) | [full_systems](#full_systems) | [game_systems](#game_systems) | [網格](#grid) | [角色](#rpg) | [教學](#tutorials) | [實用程式](#utils) |

| | | | | |
|---|---|---|---|---|
| [成就](#achievements) | [審核](#auditing) | [aws儲存](#awsstorage) | [以物易物](#barter) | [批次程式](#batchprocessor) |
| [身體功能](#bodyfunctions) | [增益](#buffs) | [building_menu](#building_menu) | [character_creator](#character_creator) | [服裝](#clothing) |
| [color_markups](#color_markups) | [成分](#components) | [容器](#containers) | [冷卻時間](#cooldowns) | [製作](#crafting) |
| [custom_gametime](#custom_gametime) | [除錯](#debugpy) | [骰子](#dice) | [email_login](#email_login) | [evadventure](#evadventure) |
| [evscaperoom](#evscaperoom) | [extended_room](#extended_room) | [欄位填充](#fieldfill) | [性別子](#gendersub) | [git_integration](#git_integration) |
| [godotwebsocket](#godotwebsocket) | [health_bar](#health_bar) | [ingame_map_display](#ingame_map_display) | [ingame_python](#ingame_python) | [ingame_reports](#ingame_reports) |
| [llm](#llm) | [郵件](#mail) | [地圖建構器](#mapbuilder) | [menu_login](#menu_login) | [映象](#mirror) |
| [多解析度](#multidescer) | [mux_comms_cmds](#mux_comms_cmds) | [name_generator](#name_generator) | [謎題](#puzzles) | [random_string_generator](#random_string_generator) |
| [red_button](#red_button) | [rp系統](#rpsystem) | [簡單門](#simpledoor) | [slow_exit](#slow_exit) | [儲存](#storage) |
| [talking_npc](#talking_npc) | [性狀](#traits) | [tree_select](#tree_select) | [逆轉戰](#turnbattle) | [tutorial_world](#tutorial_world) |
| [unix指令](#unixcommand) | [荒野](#wilderness) | [xyz格](#xyzgrid) |



(base_systems)=
## base_systems

_系統不一定與特定的系統相關
遊戲中的機制，但對整個遊戲很有用。例子包括
登入系統、新指令語法和建置 helpers._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-AWSStorage.md
Contrib-Building-Menu.md
Contrib-Color-Markups.md
Contrib-Components.md
Contrib-Custom-Gametime.md
Contrib-Email-Login.md
Contrib-Godotwebsocket.md
Contrib-Ingame-Python.md
Contrib-Ingame-Reports.md
Contrib-Menu-Login.md
Contrib-Mux-Comms-Cmds.md
Contrib-Unixcommand.md
```


(awsstorage)=
### `awsstorage`

_尊敬的牧師 (trhr) 的貢獻，2020_

該外掛遷移 Evennia 的基於 Web 的部分，即影象，
javascript 以及位於 Amazon AWS (S3) 靜態檔案內的其他專案
雲端託管。非常適合透過遊戲提供媒體服務的人。

[閱讀檔案](./Contrib-AWSStorage.md) - [瀏覽程式碼](evennia.contrib.base_systems.awsstorage)



(building_menu)=
### `building_menu`

_vincent-lg 的貢獻，2018_

建築選單是遊戲中的選單，與 `EvMenu` 不同，儘管使用
不同的方法。建築選單經過特別設計，可以編輯
作為建設者的資訊。在指令中建立建置選單允許
建構者可以快速編輯給定的物件，例如房間。如果您遵循
新增 contrib 的步驟，您將有權存取 `edit` 指令
這將編輯任何預設物件，提供更改其鍵和描述。

[閱讀檔案](./Contrib-Building-Menu.md) - [瀏覽程式碼](evennia.contrib.base_systems.building_menu)



(color_markups)=
### `color_markups`

_Griatch 的貢獻，2017 年_

Evennia 的附加顏色標記樣式（擴充或取代預設值
`|r`、`|234`）。新增對 MUSH 樣式（`%cr`、`%c123`）和/或舊版Evennia 的支援
（`{r`，`{123`）。

[閱讀檔案](./Contrib-Color-Markups.md) - [瀏覽程式碼](evennia.contrib.base_systems.color_markups)



(components)=
### `components`

_貢獻者：ChrisLR，2021_

使用元件/組合方法擴充套件typeclasses。

[閱讀檔案](./Contrib-Components.md) - [瀏覽程式碼](evennia.contrib.base_systems.components)



(custom_gametime)=
### `custom_gametime`

_vlgeoff 的貢獻，2017 年 - 基於 Griatch 的核心原創_

這重新實現了 `evennia.utils.gametime` 模組，但帶有 _custom_
您的遊戲世界的日曆（每週/每月/每年的異常天數等）。
與原始版本一樣，它允許安排事件在給定的時間發生
遊戲中的時間，但現在考慮到這個自訂日曆。

[閱讀檔案](./Contrib-Custom-Gametime.md) - [瀏覽程式碼](evennia.contrib.base_systems.custom_gametime)



(email_login)=
### `email_login`

_Griatch 的貢獻，2012 年_

這是登入系統的變體，要求提供電子郵件地址
而不是使用者名稱來登入。請注意，它不會驗證電子郵件，
它只是將其用作識別符號而不是使用者名稱。

[閱讀檔案](./Contrib-Email-Login.md) - [瀏覽程式碼](evennia.contrib.base_systems.email_login)



(godotwebsocket)=
### `godotwebsocket`

_ChrisLR 貢獻，2022_

這個contrib允許你將Godot用戶端直接連線到你的mud，
並使用 BBCode 以 Godot RichTextLabel 的顏色顯示常規文字。
您可以使用 Godot 提供具有適當 Evennia 支援的進階功能。

[閱讀檔案](./Contrib-Godotwebsocket.md) - [瀏覽程式碼](evennia.contrib.base_systems.godotwebsocket)



(ingame_python)=
### `ingame_python`

_Vincent Le Goff 2017 年貢獻_

這 contrib 增加了 script 在遊戲中使用 Python 的能力。它允許可信
工作人員/建構者動態新增功能和觸發器到單一物件
無需在外部 Python 模組中執行此操作。在遊戲中使用自訂Python，
特定的房間、出口、角色、物件等可以表現得與
它的「表兄弟」。這類似於軟程式碼對於 MU 或 MudProgs 對於 DIKU 的工作方式。
但請記住，允許在遊戲中使用 Python 會帶來嚴重的後果
安全問題（您必須深深信任您的建造者），因此請閱讀中的警告
在繼續之前請仔細閱讀此模組。

[閱讀檔案](./Contrib-Ingame-Python.md) - [瀏覽程式碼](evennia.contrib.base_systems.ingame_python)



(ingame_reports)=
### `ingame_reports`

_貢獻者：InspectorCaracal，2024_

這個contrib提供了一個遊戲內報告系統，預設處理錯誤報告、玩家報告和想法提交。它還支援新增您自己的報告型別，或刪除任何預設報告型別。

[閱讀檔案](./Contrib-Ingame-Reports.md) - [瀏覽程式碼](evennia.contrib.base_systems.ingame_reports)



(menu_login)=
### `menu_login`

_Vincent-lg 2016 年貢獻。由 Griatch 重新設計為現代 EvMenu，2019 年。 _

這將Evennia登入更改為要求輸入帳戶名稱和密碼作為一系列
問題，而不是要求您同時輸入兩個問題。它使用Evennia的
選單系統 `EvMenu` 在引擎蓋下。

[閱讀檔案](./Contrib-Menu-Login.md) - [瀏覽程式碼](evennia.contrib.base_systems.menu_login)



(mux_comms_cmds)=
### `mux_comms_cmds`

_Griatch 2021 貢獻_

在 Evennia 1.0+ 中，舊的 Channel 指令（最初受 MUX 啟發）是
替換為執行所有這些功能的單一 `channel` 指令。
這個contrib（摘自Evennia 0.9.5）將功能分解為
MU* 使用者更熟悉的單獨指令。這只是為了展示，
main `channel` 指令仍然在後臺呼叫。

[閱讀檔案](./Contrib-Mux-Comms-Cmds.md) - [瀏覽程式碼](evennia.contrib.base_systems.mux_comms_cmds)



(unixcommand)=
### `unixcommand`

_Vincent Le Geoff (vlgeoff) 的貢獻，2017 年_

該模組包含一個指令類，帶有一個替代語法解析器，實現
遊戲中的 Unix 風格指令語法。這意味著`--options`，位置引數
以及像 `-n 10` 這樣的東西。對普通玩家來說這可能不是最好的語法
但當建構者需要使用單一指令執行操作時，這對他們來說非常有用
很多事情有很多選擇。它使用Python標準中的`ArgumentParser`
引擎蓋下的圖書館。

[閱讀檔案](./Contrib-Unixcommand.md) - [瀏覽程式碼](evennia.contrib.base_systems.unixcommand)






(full_systems)=
## full_systems

_‘完整’的遊戲引擎，可直接用於開始建立內容
無需進一步新增（除非您願意）._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-Evscaperoom.md
```


(evscaperoom)=
### `evscaperoom`

_Griatch 的貢獻，2019 年_

用於在 Evennia 中建立多人逃脫室的完整引擎。允許玩家
生成並加入獨立追蹤其狀態的謎題房間。任意數量的玩家
可以一起解決房間問題。這是為“EvscapeRoom”建立的引擎，它贏得了
2019 年 4 月至 5 月舉行的 MUD Coders Guild“One Room”Game Jam。 contrib 僅
非常小的遊戲內容，它包含實用程式和基類以及一個空的範例房間。

[閱讀檔案](./Contrib-Evscaperoom.md) - [瀏覽程式碼](evennia.contrib.full_systems.evscaperoom)






(game_systems)=
## game_systems

_遊戲內的遊戲系統，如製作、郵件、戰鬥等等。
每個系統都應該逐步採用並用於您的遊戲。
這不包括特定於角色扮演的系統，這些系統可以在
`rpg` category._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-Achievements.md
Contrib-Barter.md
Contrib-Clothing.md
Contrib-Containers.md
Contrib-Cooldowns.md
Contrib-Crafting.md
Contrib-Gendersub.md
Contrib-Mail.md
Contrib-Multidescer.md
Contrib-Puzzles.md
Contrib-Storage.md
Contrib-Turnbattle.md
```


(achievements)=
### `achievements`

_一個簡單但相當全面的成就追蹤系統。成就是使用普通的 Python 字典定義的，讓人想起核心原型系統，雖然預計您只會在角色或帳戶上使用它，但可以追蹤任何型別分類的object._

contrib 提供了多種用於追蹤和存取成就的功能，以及用於檢視成就狀態的基本遊戲內指令。

[閱讀檔案](./Contrib-Achievements.md) - [瀏覽程式碼](evennia.contrib.game_systems.achievements)



(barter)=
### `barter`

_Griatch 的貢獻，2012 年_

這實現了完整的以物易物系統 - 讓玩家安全地進行交易的方式
用程式碼而不是簡單的`give/get`相互之間交易物品
指令。這增加了安全性（任何時候一個玩家都不會
貨物和付款在手）和速度，因為約定的貨物將
自動移動）。只需用硬幣物體替換一側，
（或硬幣和商品的混合），這也適用於普通貨幣
交易。

[閱讀檔案](./Contrib-Barter.md) - [瀏覽程式碼](evennia.contrib.game_systems.barter)



(clothing)=
### `clothing`

_蒂姆·阿什利·詹金斯貢獻，2017 年_

提供 typeclass 和可穿戴服裝的指令。這些
這些衣服的外觀會附加到角色穿著時的描述中。

[閱讀檔案](./Contrib-Clothing.md) - [瀏覽程式碼](evennia.contrib.game_systems.clothing)



(containers)=
### `containers`

_透過提供容器typeclass並擴充套件某些基礎commands._，增加將物件放入其他容器物件的能力

(installation)=
## 安裝

[閱讀檔案](./Contrib-Containers.md) - [瀏覽程式碼](evennia.contrib.game_systems.containers)



(cooldowns)=
### `cooldowns`

_owllex 的貢獻，2021 年_

冷卻時間用於對速率限制的操作進行建模，例如
角色可以執行給定的動作；直到過了一定的時間
指令無法再次使用。這個contrib提供了一個簡單的冷卻時間
可以附加到任何 typeclass 的處理程式。冷卻時間是輕量級的永續性
非同步計時器，您可以查詢該計時器以檢視是否已經過了某個時間。

[閱讀檔案](./Contrib-Cooldowns.md) - [瀏覽程式碼](evennia.contrib.game_systems.cooldowns)



(crafting)=
### `crafting`

_Griatch 2020 的貢獻_

這實現了完整的製作系統。原則就是“食譜”，
您將物品（標記為成分）組合起來創造出新的東西。食譜還可以
需要某些（非消耗性）工具。一個例子是使用“麵包配方”
將「麵粉」、「水」和「酵母」與「烤箱」結合起來烘烤「一條麵包」。

[閱讀檔案](./Contrib-Crafting.md) - [瀏覽程式碼](evennia.contrib.game_systems.crafting)



(gendersub)=
### `gendersub`

_Griatch 2015 年貢獻_

這是一個簡單的性別感知角色類，允許使用者
在文字中插入自訂標記以表示性別意識
訊息傳遞。它依賴於修改後的 msg() 並且意味著
如何做這樣的事情的靈感和起點。

[閱讀檔案](./Contrib-Gendersub.md) - [瀏覽程式碼](evennia.contrib.game_systems.gendersub)



(mail)=
### `mail`

_grungie1138 2016 年貢獻_

一個簡單的 Brandymail 風格的郵件系統，使用來自 Evennia 的 `Msg` 類
核心。它有兩個指令用於在帳戶之間傳送郵件（遊戲外）
或角色之間（遊戲中）。這兩種型別的郵件可以一起使用或
靠他們自己。

[閱讀檔案](./Contrib-Mail.md) - [瀏覽程式碼](evennia.contrib.game_systems.mail)



(multidescer)=
### `multidescer`

_Griatch 2016 年貢獻_

「multidescer」是來自 MUSH 世界的概念。它允許
將您的描述分成任意命名的“部分”，您可以
然後隨意交換。這是一種快速管理您的外觀的方法（例如當
更自由的角色扮演系統中的換衣服）。這也將
與 `rpsystem` contrib 配合良好。

[閱讀檔案](./Contrib-Multidescer.md) - [瀏覽程式碼](evennia.contrib.game_systems.multidescer)



(puzzles)=
### `puzzles`

_Henddher 2018 年貢獻_

適用於冒險遊戲風格的組合謎題，例如組合水果
和攪拌機來製作冰沙。為物件提供typeclass和指令
可以組合（i.e。一起使用）。與 `crafting` contrib 不同，每個
拼圖是由獨特的物件建構的，而不是使用 tags 並且建構者可以建立
謎題完全來自遊戲內。

[閱讀檔案](./Contrib-Puzzles.md) - [瀏覽程式碼](evennia.contrib.game_systems.puzzles)



(storage)=
### `storage`

_helpme 的貢獻 (2024)_

此模組允許將某些房間標記為存放位置。

[閱讀檔案](./Contrib-Storage.md) - [瀏覽程式碼](evennia.contrib.game_systems.storage)



(turnbattle)=
### `turnbattle`

_蒂姆·阿什利·詹金斯貢獻，2017 年_

這是一個簡單的回合製戰鬥系統的框架，類似
用於 D&D 風格的桌上角色扮演遊戲中的那些。它允許
任何角色在房間內發動戰鬥，此時主動
捲動並建立回合順序。每一個參與戰鬥的人
決定該回合行動的時間有限（30 秒
預設），戰鬥按照回合順序進行，迴圈
參與者直到戰鬥結束。

[閱讀檔案](./Contrib-Turnbattle.md) - [瀏覽程式碼](evennia.contrib.game_systems.turnbattle)






(grid)=
## 網格

_與遊戲世界的拓樸和結構相關的系統。 Contribs相關
到房間、出口和地圖building._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-Extended-Room.md
Contrib-Ingame-Map-Display.md
Contrib-Mapbuilder.md
Contrib-Simpledoor.md
Contrib-Slow-Exit.md
Contrib-Wilderness.md
Contrib-XYZGrid.md
```


(extended_room)=
### `extended_room`

_貢獻 - Griatch 2012、vincent-lg 2019、Griatch 2023_

這擴充套件了正常的 `Room` typeclass 以允許其描述隨
一天中的時間和/或季節以及任何其他狀態（如洪水或黑暗）。
在描述中嵌入 `$state(burning, This place is on fire!)` 將
允許根據房間狀態變更描述。房間還支援
`details` 供玩家在房間中檢視（無需建立新的
每個的遊戲內物件），以及對隨機迴聲的支援。房間
附帶一組用於 `look` 和 `@desc` 的備用指令，以及新指令
指令`detail`、`roomstate` 和`time`。

[閱讀檔案](./Contrib-Extended-Room.md) - [瀏覽程式碼](evennia.contrib.grid.extended_room)



(ingame_map_display)=
### `ingame_map_display`

_貢獻 - helpme 2022_

這會將 ascii `map` 新增到給定房間，可以使用 `map` 指令檢視該房間。
您可以輕鬆地更改它以新增特殊字元、房間顏色等。顯示的地圖是
使用時動態生成，並支援所有羅盤方向和向上/向下。其他
方向被忽略。

[閱讀檔案](./Contrib-Ingame-Map-Display.md) - [瀏覽程式碼](evennia.contrib.grid.ingame_map_display)



(mapbuilder)=
### `mapbuilder`

_Cloud_Keeper 2016 的貢獻_

根據 2D ASCII 地圖的繪製建立遊戲地圖。

[閱讀檔案](./Contrib-Mapbuilder.md) - [瀏覽程式碼](evennia.contrib.grid.mapbuilder)



(simpledoor)=
### `simpledoor`

_Griatch 的貢獻，2016 年_

一個簡單的雙向出口，代表一扇可以開啟和關閉的門
從兩側關閉。可以輕鬆擴充套件以使其可鎖定，
可破壞等

[閱讀檔案](./Contrib-Simpledoor.md) - [瀏覽程式碼](evennia.contrib.grid.simpledoor)



(slow_exit)=
### `slow_exit`

_Griatch 2014 年貢獻_

延遲其遍歷的退出型別的範例。這模擬了
緩慢的移動，在許多遊戲中很常見。 contrib 也
包含兩個指令，`setspeed` 和 `stop` 用於改變移動速度
並分別中止正在進行的遍歷。

[閱讀檔案](./Contrib-Slow-Exit.md) - [瀏覽程式碼](evennia.contrib.grid.slow_exit)



(wilderness)=
### `wilderness`

_titeuf87 的貢獻，2017 年_

這contrib提供了荒野地圖，而沒有實際建立大量
房間數 - 當您移動時，您最終會回到同一個房間，但其描述
變化。這意味著您可以使用很少的資料庫來建立巨大的區域，例如
只要房間相對相似（e.g。僅名稱/描述發生變化）。

[閱讀檔案](./Contrib-Wilderness.md) - [瀏覽程式碼](evennia.contrib.grid.wilderness)



(xyzgrid)=
### `xyzgrid`

_Griatch 2021 貢獻_

將 Evennia 的遊戲世界放置在 xy（z 是不同的地圖）座標網格上。
網格是透過繪製和解析 2D ASCII 地圖在外部建立和維護的，
包括傳送、地圖轉換和幫助尋路的特殊標記。
支援在每個地圖上非常快速的最短路徑尋路。還包括一個
快速檢視功能，僅檢視距離您有限的步數
目前位置（對於將網格顯示為遊戲中的更新地圖很有用）。

[閱讀檔案](./Contrib-XYZGrid.md) - [瀏覽程式碼](evennia.contrib.grid.xyzgrid)






(rpg)=
## 角色扮演遊戲

_專門與角色扮演相關的系統
以及規則實施，例如性格特徵、擲骰子和emoting._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-Buffs.md
Contrib-Character-Creator.md
Contrib-Dice.md
Contrib-Health-Bar.md
Contrib-Llm.md
Contrib-RPSystem.md
Contrib-Traits.md
```


(buffs)=
### `buffs`

_Tegiminis 2022 年的貢獻_

buff 是一個定時物件，附加到遊戲實體。它能夠修改值、觸發程式碼或兩者兼而有之。 
這是RPGs中常見的設計模式，尤其是動作遊戲。

[閱讀檔案](./Contrib-Buffs.md) - [瀏覽程式碼](evennia.contrib.rpg.buffs)



(character_creator)=
### `character_creator`

_InspectorCaracal 貢獻，2022_

用於管理和啟動遊戲內角色建立選單的指令。

[閱讀檔案](./Contrib-Character-Creator.md) - [瀏覽程式碼](evennia.contrib.rpg.character_creator)



(dice)=
### `dice`

_Griatch 貢獻，2012 年、2023 年_

適用於任意數量和麵的骰子的骰子滾輪。新增遊戲中的骰子滾動
（如 `roll 2d10 + 1`）以及條件（低於/高於/等於目標）
以及程式碼中擲骰子的函式。指令還支援隱藏或秘密
供人類遊戲大師使用的捲。

[閱讀檔案](./Contrib-Dice.md) - [瀏覽程式碼](evennia.contrib.rpg.dice)



(health_bar)=
### `health_bar`

_蒂姆·阿什利·詹金斯貢獻，2017 年_

此模組提供的功能可讓您輕鬆展示視覺效果
條或米作為彩色條而不僅僅是數字。一個“健康棒”
這只是最明顯的用途，但該欄是高度可自訂的
並且可以用於玩家健康以外的任何型別的適當資料。

[閱讀檔案](./Contrib-Health-Bar.md) - [瀏覽程式碼](evennia.contrib.rpg.health_bar)



(llm)=
### `llm`

_Griatch 2023 的貢獻_

這會增加一個 LLMClient，允許 Evennia 向 LLM 伺服器傳送提示（大語言模型，與 ChatGPT 類似）。範例使用本地 OSS LLM 安裝。其中包括一個 NPC，您可以使用新的 `talk` 指令與之聊天。 NPC 將使用來自 LLM 伺服器的 AI 回應進行回應。所有呼叫都是非同步的，因此如果 LLM 很慢，Evennia 不會受到影響。

[閱讀檔案](./Contrib-Llm.md) - [瀏覽程式碼](evennia.contrib.rpg.llm)



(rpsystem)=
### `rpsystem`

_Griatch 的貢獻，2015 年_

完整的角色扮演表情系統。簡短的描述和識別（在給他們指定名字之前只能透過外表來認識他們）。房間姿勢。面具/偽裝（隱藏您的描述）。直接用表情說話，可選擇語言模糊（如果您不懂該語言，單字會出現亂碼，您也可以使用不同的語言，並具有不同的「發音」亂碼）。從遠處就可以聽到部分耳語。一個非常強大的表情內參考系統，用於參考和區分目標（包括物件）。

[閱讀檔案](./Contrib-RPSystem.md) - [瀏覽程式碼](evennia.contrib.rpg.rpsystem)



(traits)=
### `traits`

_Griatch 2020 年貢獻，基於 Whitenoise 和 Ainneve contribs 的程式碼，2014 年_

`Trait` 代表（通常）角色的可修改屬性。他們可以
用來表示從屬性（力量、敏捷等）到技能的一切
（狩獵 10，劍 14 等）和動態變化的東西，如 HP、XP 等。
特徵與普通屬性的不同之處在於它們追蹤其變化和限制
自己到特定的值範圍。人們可以輕鬆地新增/減去它們，並且
它們甚至可以以特定的速率動態變化（例如你中毒了或
痊癒了）。

[閱讀檔案](./Contrib-Traits.md) - [瀏覽程式碼](evennia.contrib.rpg.traits)






(tutorials)=
## 教學

_幫助資源專門用於教授開發概念或
以 Evennia 系統為例。與檔案相關的任何額外資源
教學可以在這裡找到。也是教學世界和Evadventure的所在地
演示codes._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-Batchprocessor.md
Contrib-Bodyfunctions.md
Contrib-Evadventure.md
Contrib-Mirror.md
Contrib-Red-Button.md
Contrib-Talking-Npc.md
Contrib-Tutorial-World.md
```


(batchprocessor)=
### `batchprocessor`

_Griatch 的貢獻，2012 年_

批處理器的簡單範例。批處理器用於生成
來自一個或多個靜態檔案的遊戲內容。檔案可以與版本一起儲存
控制然後“應用”到遊戲中以建立內容。

[閱讀檔案](./Contrib-Batchprocessor.md) - [瀏覽程式碼](evennia.contrib.tutorials.batchprocessor)



(bodyfunctions)=
### `bodyfunctions`

_Griatch 的貢獻，2012 年_

用於測試的範例 script。這新增了一個簡單的計時器，其中包含您的
人物會不定期地進行一些小小的口頭觀察。

[閱讀檔案](./Contrib-Bodyfunctions.md) - [瀏覽程式碼](evennia.contrib.tutorials.bodyfunctions)



(evadventure)=
### `evadventure`

_Griatch 2023 年的貢獻-_


```{warning}
NOTE - 本教學已完成 WIP 和 NOT！你仍然會學習
從中得到一些東西，但不要期望完美。
```

[閱讀檔案](./Contrib-Evadventure.md) - [瀏覽程式碼](evennia.contrib.tutorials.evadventure)



(mirror)=
### `mirror`

_Griatch 的貢獻，2017 年_

一個簡單的鏡子物件進行實驗。它會對被注視做出反應。

[閱讀檔案](./Contrib-Mirror.md) - [瀏覽程式碼](evennia.contrib.tutorials.mirror)



(red_button)=
### `red_button`

_Griatch 貢獻，2011 年_

一個紅色按鈕，按下即可產生效果。這是一個更高階的例子
具有自己的功能和狀態追蹤的物件。

[閱讀檔案](./Contrib-Red-Button.md) - [瀏覽程式碼](evennia.contrib.tutorials.red_button)



(talking_npc)=
### `talking_npc`

_Griatch 2011 年貢獻。由 grungies1138 更新，2016 年_

這是一個靜態 NPC 物件的範例，能夠容納簡單的選單驅動
談話。例如適合作為任務提供者或商人。

[閱讀檔案](./Contrib-Talking-Npc.md) - [瀏覽程式碼](evennia.contrib.tutorials.talking_npc)



(tutorial_world)=
### `tutorial_world`

_Griatch 2011、2015 年貢獻_

用於未修改的 Evennia 安裝的獨立教學區域。
將其視為一種單人冒險而不是
成熟的多人遊戲世界。各種房間和物體
旨在炫耀 Evennia 的功能，而不是成為
非常具有挑戰性（也不長）的遊戲體驗。既然如此，那當然是
只瀏覽了可能發生的事情的表面。把這個拆開
是開始學習該系統的好方法。

[閱讀檔案](./Contrib-Tutorial-World.md) - [瀏覽程式碼](evennia.contrib.tutorials.tutorial_world)






(utils)=
## 實用程式

_Miscellaneous，用於操作文字、安全審核的工具以及more._


```{toctree}
:hidden:
Contribs-Guidelines.md
```
```{toctree}
:maxdepth: 1

Contrib-Auditing.md
Contrib-Debugpy.md
Contrib-Fieldfill.md
Contrib-Git-Integration.md
Contrib-Name-Generator.md
Contrib-Random-String-Generator.md
Contrib-Tree-Select.md
```


(auditing)=
### `auditing`

_Johnny 的貢獻，2017 年_

實用程式可以竊聽並攔截傳送到/從用戶端傳送的所有資料以及
伺服器並將其傳遞給您選擇的回撥。這是為了
品質保證、事故後調查和除錯。

[閱讀檔案](./Contrib-Auditing.md) - [瀏覽程式碼](evennia.contrib.utils.auditing)



(debugpy)=
### `debugpy`

_ Electroglyph 的貢獻，2025 年_

這會註冊一個遊戲內指令 `debugpy`，該指令啟動 debugpy 偵錯器並偵聽連線埠 5678。
目前，這僅適用於 Visual Studio Code (VS Code)。

[閱讀檔案](./Contrib-Debugpy.md) - [瀏覽程式碼](evennia.contrib.utils.debugpy)



(fieldfill)=
### `fieldfill`

_ Tim Ashley Jenkins 貢獻，2018 年_

該模組包含一個為您產生 `EvMenu` 的函式 - 這
選單向玩家呈現一種可以填滿的欄位形式
以任意順序輸出（e.g.用於角色生成或建構）。每個欄位的值可以
進行驗證，該功能可以輕鬆檢查文字和整數輸入，
最小值和最大值/字元長度，甚至可以由自訂驗證
功能。提交表單後，表單的資料將作為字典提交
到您選擇的任何可呼叫物件。

[閱讀檔案](./Contrib-Fieldfill.md) - [瀏覽程式碼](evennia.contrib.utils.fieldfill)



(git_integration)=
### `git_integration`

_helpme 的貢獻 (2022)_

一個在遊戲中整合 git 精簡版本的模組，讓開發人員可以檢視其 git 狀態、更改分支以及提取本地 mygame 儲存庫和 Evennia 核心的更新程式碼。成功拉取或簽出後，git 指令將重新載入遊戲：可能需要手動重新啟動才能套用某些會影響持久scripts 等的變更。

[閱讀檔案](./Contrib-Git-Integration.md) - [瀏覽程式碼](evennia.contrib.utils.git_integration)



(name_generator)=
### `name_generator`

_InspectorCaracal 的貢獻 (2022)_

用於產生隨機名稱的模組，包括現實世界和幻想世界。現實世界
名稱可以產生為名字、姓氏或
全名（名字、可選的中間名和姓氏）。姓名資料來自[姓名背後](https://www.behindthename.com/)
並在 [CC BY-SA 4.0 許可證](https://creativecommons.org/licenses/by-sa/4.0/) 下使用。

[閱讀檔案](./Contrib-Name-Generator.md) - [瀏覽程式碼](evennia.contrib.utils.name_generator)



(random_string_generator)=
### `random_string_generator`

_Vincent Le Goff (vlgeoff) 的貢獻，2017 年_

此實用程式可用於產生偽隨機資訊字串
具有特定的標準。  例如，您可以使用它來生成
電話號碼、車牌號碼、驗證碼、遊戲內安全
密碼等。產生的字串將被儲存並且不會重複。

[閱讀檔案](./Contrib-Random-String-Generator.md) - [瀏覽程式碼](evennia.contrib.utils.random_string_generator)



(tree_select)=
### `tree_select`

_蒂姆·阿什利·詹金斯貢獻，2017 年_

該實用程式可讓您建立並初始化整個分支EvMenu
傳遞給一個函式的多行字串的例項。

[閱讀檔案](./Contrib-Tree-Select.md) - [瀏覽程式碼](evennia.contrib.utils.tree_select)







----

<small>此檔案頁面是自動產生的。手動更改
將被覆蓋。 </small>
