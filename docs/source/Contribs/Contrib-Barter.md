(barter-system)=
# 以物易物系統

Griatch 的貢獻，2012 年

這實現了完整的以物易物系統 - 讓玩家安全地進行交易的方式
用程式碼而不是簡單的`give/get`相互之間交易物品
指令。這增加了安全性（任何時候一個玩家都不會
貨物和付款在手）和速度，因為約定的貨物將
自動移動）。只需用硬幣物體替換一側，
（或硬幣和商品的混合），這也適用於普通貨幣
交易。

(installation)=
## 安裝

只需將 CmdsetTrade 指令匯入（例如）預設值
cmdset。這將使交易（或以物易物）指令可用
遊戲中。

```python
# in mygame/commands/default_cmdsets.py

from evennia.contrib.game_systems import barter  # <---

# ...
class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at cmdset_creation(self):
        # ...
        self.add(barter.CmdsetTrade)  # <---

```

(usage)=
## 用法

在本模組中，「以物易物」通常被稱為「貿易」。

以下是易貨序列的範例。 A、B 為當事人。
`A>` 和 `B>` 是他們的輸入。

1) 開倉交易

    A> trade B: Hi, I have a nice extra sword. You wanna trade?

    B sees:
    A says: "Hi, I have a nice extra sword. You wanna trade?"
       A wants to trade with you. Enter 'trade A <emote>' to accept.

    B> trade A: Hm, I could use a good sword ...

    A sees:
    B says: "Hm, I could use a good sword ...
       B accepts the trade. Use 'trade help' for aid.

    B sees:
    You are now trading with A. Use 'trade help' for aid.

2）談判

    A> offer sword: This is a nice sword. I would need some rations in trade.

    B sees: A says: "This is a nice sword. I would need some rations in trade."
       [A offers Sword of might.]

    B> evaluate sword
    B sees:
    <Sword's description and possibly stats>

    B> offer ration: This is a prime ration.

    A sees:
    B says: "This is a prime ration."
      [B offers iron ration]

    A> say Hey, this is a nice sword, I need something more for it.

    B sees:
    A says: "Hey this is a nice sword, I need something more for it."

    B> offer sword,apple: Alright. I will also include a magic apple. That's my last offer.

    A sees:
    B says: "Alright, I will also include a magic apple. That's my last offer."
      [B offers iron ration and magic apple]

    A> accept: You are killing me here, but alright.

    B sees: A says: "You are killing me here, but alright."
      [A accepts your offer. You must now also accept.]

    B> accept: Good, nice making business with you.
      You accept the deal. Deal is made and goods changed hands.

    A sees: B says: "Good, nice making business with you."
      B accepts the deal. Deal is made and goods changed hands.

此時退出交易系統，協商的專案
雙方之間自動交換。在此範例中，B 是
唯一改變報價的人，而且 A 也可以改變他們的報價
直到雙方找到可以達成協議的東西。的
表情是可選的，但對於 RP- 重的世界很有用。

(technical-info)=
## 科技資訊

交易是透過使用TradeHandler來實現的。這個物件是一個
儲存當前談判狀態的公共場所。它是
在發起交易的物件上建立，並儲存在
一旦另一方同意交易。交易請求時間
在一定時間後退出 - 這是由 Script 處理的。一旦交易
開始，CmdsetTrade cmdset 在雙方啟動
與交易相關的指令。

(ideas-for-npc-bartering)=
## NPC以物易物的想法

此模組主要用於兩個玩家之間的交易。但是
原則上它也可以用於玩家與
AI-控制了NPC。如果 NPC 使用普通指令，他們可以使用它
直接 - 但更有效的是讓 NPC 物件傳送其
直接透過交易處理程式回覆玩家。一個人可能想要
為拒絕指令新增一些功能，以便玩家可以
拒絕 NPC 報價中的特定物件（拒絕 <object>）並允許
AI 也許可以提供其他東西並將其變成適當的
以物易物。  伴隨著「需要」東西或有某種東西的AI
交易中的個性，這至少可以與NPCs進行以物易物
比簡單的「購買」更有趣。


----

<small>此檔案頁面是從`evennia\contrib\game_systems\barter\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
