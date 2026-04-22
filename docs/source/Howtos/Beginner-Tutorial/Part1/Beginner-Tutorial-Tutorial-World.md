(the-tutorial-world)=
# 教學世界

*教學世界*是一個小型的、功能齊全的MUD-風格的遊戲世界，附帶Evennia。
這是可能性的小展示。對於那些比較容易的人來說，它也可能很有用
透過解構現有程式碼來學習。

若要安裝教學世界，請站在 Limbo 房間並輸入：

    batchcommand tutorial_world.build

此指令在 [evennia/contrib/tutorials/tutorial_world/build.ev](github:evennia/contrib/tutorials/tutorial_world/build.ev) 中執行建置 script。
基本上，這個 script 是由 `batchcommand` 指令依序執行的建置指令清單。等待建築完成，不要運作兩次。

> 執行批次指令後，`intro` 指令在 Limbo 中變為可用。使用 [EvMenu](../../../Components/EvMenu.md)、Evennia 內建的範例嘗試取得遊戲內協助
> 選單生成系統！

教學世界由單人任務組成，並有大約 20 個房間可供探索，同時您還需要探索神秘武器的下落。

應該會出現一個名為_Tutorial_ 的新出口。輸入`tutorial`進入教學世界。

當您進入時，您將自動`quell`（當您離開時，`unquell`），因此您可以按照預期的方式進行遊戲。無論你是勝利還是使用`give up`指令，你最終都會回到地獄邊境。

```{important}
只有LOSERS 和QUITTERS 使用`give up` 指令。
```

(gameplay)=
## 遊戲玩法

![沼澤附近的城堡](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/22916c25-6299-453d-a221-446ec839f567/da2pmzu-46d63c6d-9cdc-41dd-87d6-1106db5a5e1a.jpg/v1/fill/w_600,h_849,q_75,strp/the_castle_off_the_moor_by_griatch_art_da2pmzu-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD04NDkiLCJwYXRoIjoiXC9mXC8yMjkxNmMyNS02Mjk5LTQ1M2QtYTIyMS00NDZlYzgzOWY1NjdcL2RhMnBtenUtNDZkNjNjNmQtOWNkYy00MWRkLTg3ZDYtMTEwNmRiNWE1ZTFhLmpwZyIsIndpZHRoIjoiPD02MDAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.omuS3D1RmFiZCy9OSXiIita-HxVGrBok3_7asq0rflw)
（格里奇攝）

*為了進入我們的微型任務的氛圍，想像你是一位尋找名譽和財富的冒險家。您聽說過關於海岸邊一座古老城堡廢墟的傳聞。在它的深處，埋葬著一位武士公主和她強大的魔法武器——如果屬實的話，這是一筆寶貴的獎項。當然，這是一個您無法拒絕的冒險機會！ *

*你在猛烈的雷暴中到達了大海。風雨在你臉上呼嘯，你站在荒野與大海交會的地方，沿著高高的岩石海岸…*

---

(gameplay-hints)=
### 遊戲提示

- 使用指令 `tutorial` 取得每個房間幕後的程式碼洞察。
- 看看一切。雖然是演示版，但教學世界並不一定很容易解決 - 這取決於您對基於文字的冒險遊戲的經驗。請記住，一切都可以解決或繞過。
- 有些物件以不只一種方式進行互動。使用普通的 `help` 指令來瞭解在任何給定時間哪些指令可用。
- 為了戰鬥，你需要先找到某種型別的武器。
    - *斜線*是普通攻擊
    - *stab* 發動攻擊，造成更多傷害，但擊中機率較低。
    - *防禦*將降低敵人下次攻擊時受到傷害的機率。
- 有些東西_不能_被普通武器傷害。那樣的話逃跑就是OK了。預計會被追...
- 失敗是經歷的一部分。你實際上不可能死，但會被擊倒
意味著被留在黑暗中......

(once-you-are-done-or-had-enough)=
## 一旦你完成（或受夠了）

之後，你要麼征服了古老的廢墟，並帶著榮耀和勝利歸來……要麼
你使用`give up`指令從挑戰中一瘸一拐地嗚咽著回來。
不管怎樣，你現在應該回到地獄邊境，能夠反思這段經歷。

教學世界舉例說明瞭一些功能：

- 具有顯示細節的自訂功能的房間（例如在黑暗的房間裡看牆壁）
- 隱藏或無法通行的出口，直到您滿足某些條件
- 具有多個自訂互動的物件（如劍、井、方尖碑......）
- 房間面積大（那座橋其實只有一個房間！）
- 帶有天氣訊息的室外氣象室（雨打在你身上）
- 黑暗的房間，需要光源才能顯露出來（燃燒的碎片甚至會在一段時間後燃盡）
- 拼圖物體（黑暗牢房裡的葡萄酒；希望你沒有被卡住！）
- 多房間謎題（方尖碑和地窖）
- 具有漫遊、追擊和戰鬥狀態引擎的攻擊性移動AI（相當致命，直到你找到合適的武器）
- 武器，也被暴徒使用（誠然，大多數武器對於對付大壞人來說沒有那麼有用）
- 帶有攻擊/防禦指令的簡單戰鬥系統（失敗時傳送）
- 物體生成（桶中的武器和最終武器實際上是隨機的）
- 傳送陷阱室（如果方尖碑謎題失敗）

```{sidebar} 額外學分

如果您已經熟悉 Python 並希望儘早體驗，那麼深入瞭解教學世界以瞭解它如何實現其功能可能會很有建設性。該程式碼有大量文件記錄。您可以在[evennia/contrib/tutorials/tutorial_world](../../../api/evennia.contrib.tutorials.tutorial_world.md)中找到所有程式碼。
構建-script 位於[此處](github:evennia/contrib/tutorials/tutorial_world/build.ev)。


在閱讀教學世界程式碼時，請注意教學世界的設計目的是為了輕鬆安裝，並且不會永久修改遊戲的其餘部分。因此，它確保只使用臨時解決方案並自行清理。在製作自己的遊戲時，這不是您經常需要擔心的事情。
```

這麼小的地方塞了這麼多東西！

(uninstall-the-tutorial-world)=
## 解除安裝教學世界

當你玩完教學世界後，讓我們解除安裝它。解除安裝教學世界基本上意味著刪除它所包含的所有房間和物件。然後確保你回到了 Limbo

     find tut#01
     find tut#16

這應該會找到由 `build.ev` 建立的第一個和最後一個房間 - *Intro* 和 *Outro*。如果您正常安裝，這兩個數字之間建立的所有內容都應該是教學的一部分。記下它們的 #dbref 編號，例如 5 和 80。接下來我們刪除該範圍內的所有物件：

     del 5-80

您將看到一些錯誤，因為某些物件是自動刪除的，因此當刪除機製到達它們時無法找到它們。沒關係。  指令完成後，您應該完全刪除教學。

即使教學世界的遊戲風格與您感興趣的遊戲風格不相似，它也應該能讓您嚐到Evennia的一些可能性。現在我們將繼續討論如何透過程式碼存取此功能。