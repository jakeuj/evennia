(part-3-how-we-get-there-example-game)=
# 第 3 部分：我們如何實現這一目標（範例遊戲）

```{warning}
教學遊戲正在開發中，尚未完成，也未經過測試。使用現有的課程作為靈感並幫助您繼續前進，但此時不要指望從中獲得開箱即用的完美。
```

```{sidebar} 初學者教學部分
- [簡介](../Beginner-Tutorial-Overview.md)
<br>正在設定。
- 第1部分：[我們擁有什麼](../Part1/Beginner-Tutorial-Part1-Overview.md)
<br>Evennia 概覽，以及如何使用這些工具，包括 Python 簡介。
- 第二部分：[我們想要什麼](../Part2/Beginner-Tutorial-Part2-Overview.md)
<br>規劃我們的教學遊戲以及規劃您自己的遊戲時要考慮的事項。
- *第 3 部分：[我們如何實現目標](./Beginner-Tutorial-Part3-Overview.md)*
<br>開始著手擴充Evennia來製作你的遊戲。
- 第 4 部分：[使用我們建立的內容](../Part4/Beginner-Tutorial-Part4-Overview.md)
<br>建立一個技術演示和世界內容以配合我們的程式碼。
- 第五部分：[向世界展示](../Part5/Beginner-Tutorial-Part5-Overview.md)
<br>將我們的新遊戲上線並讓玩家嘗試。
```

在 Evennia 初學者教學的第三部分中，我們將實際建立
我們的教學遊戲_EvAdventure_，基於 [Knave](https://www.drivethrurpg.com/product/250888/Knave) RPG 規則集。

如果您遵循了本教學系列的前幾部分，您將對 Python 以及在哪裡查詢和使用 Evennia 中的內容有一些概念。我們也很清楚我們將建立的遊戲型別。

即使這不是你感興趣的遊戲風格，跟著一起走也會帶給你很多
使用 Evennia 的經驗，對以後做自己的事情非常有幫助！ EvAdventure 遊戲程式碼也被建構為易於擴充套件。

我們在這部分中編寫的所有程式碼的完整編碼範例可以在
[evennia/contrib/tutorials/evadventure](../../../api/evennia.contrib.tutorials.evadventure.md) 套件。有以下三種常見的學習方法：

1. 按順序遵循教學課程並使用它來編寫您自己的程式碼，將現成的程式碼作為額外的幫助、上下文或作為檢查自己的「事實」。
2. 通讀包中的程式碼並參閱每個部分的教學課程，以獲取有關您所看到內容的更多資訊。
3. 兩者的一些混合。

您選擇哪種方法是因人而異的——我們都以不同的方式學習。

無論哪種方式，這都是一個重要的部分。您將看到大量程式碼並且有大量課程需要學習。畢竟我們是從頭開始製作整個遊戲。慢慢來！

(lessons)=
## 教訓


```{toctree} 
:numbered:
:maxdepth: 2

Beginner-Tutorial-Utilities
Beginner-Tutorial-Rules
Beginner-Tutorial-Characters
Beginner-Tutorial-Objects
Beginner-Tutorial-Equipment
Beginner-Tutorial-Chargen
Beginner-Tutorial-Rooms
Beginner-Tutorial-NPCs
Beginner-Tutorial-Combat-Base
Beginner-Tutorial-Combat-Twitch
Beginner-Tutorial-Combat-Turnbased
Beginner-Tutorial-AI
Beginner-Tutorial-Dungeon
Beginner-Tutorial-Monsters
Beginner-Tutorial-Quests
Beginner-Tutorial-Shops
Beginner-Tutorial-Commands
```
