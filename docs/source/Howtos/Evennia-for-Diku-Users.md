(evennia-for-diku-users)=
# 迪庫使用者Evennia


Evennia 代表了曾經在上面寫程式碼的人的學習曲線
[Diku](https://en.wikipedia.org/wiki/DikuMUD) 輸入MUDs。雖然用 Python 編碼很容易，但如果你
已經瞭解C，主要努力是改掉舊的C程式設計習慣。嘗試編寫 Python 程式碼
你用 C 寫的程式碼不僅看起來很難看，而且會導致程式碼不太最佳化並且更難維護。
閱讀 Evennia 範例程式碼是瞭解如何解決不同問題的好方法
在Python中。

總的來說，Python 提供了廣泛的資源庫、安全的記憶體管理和優秀的
錯誤的處理。雖然 Python 程式碼的執行速度不如原始 C 程式碼，但差異並不在於
對於基於文字的遊戲來說這一切都很重要。 Python 的主要優點是速度極快
開發週期和建立遊戲系統的簡單方法。對 C 執行同樣的操作可能需要多次
程式碼越多，就越難穩定和維護。

(core-differences)=
## 核心差異

- 如前所述，Evennia 和 Diku 派生的程式碼庫之間的主要區別在於 Evennia 是
純粹用Python編寫。由於Python是一種解釋性語言，因此沒有編譯階段。它是
由伺服器在執行時載入Python模組來修改和擴充。它也可以在所有計算機上執行
Python 執行的平臺（基本上無所不在）。
- Vanilla Diku 型別引擎將其資料儲存在自訂*平面檔案*型別儲存解決方案中。經過
相反，Evennia 將所有遊戲資料儲存在多個支援的 SQL 資料庫之一中。而平面檔案
具有更容易實施的優點，但它們（通常）缺乏許多預期的安全功能
以及有效提取儲存資料子集的方法。例如，如果伺服器斷電
寫入平面檔案時，它可能會損壞並且資料遺失。正確的資料庫解決方案是
不受此影響 - 資料在任何時候都不會處於無法恢復的狀態。資料庫
也針對高效查詢大型資料集進行了高度最佳化。

(some-familiar-things)=
## 一些熟悉的事情

Diku 表示通常引用的字元物件：

`struct char ch*`則`ch->`可以存取所有與字元相關的欄位。在Evennia中，必須
注意您正在使用的物件，以及當您透過背景存取另一個物件時
處理，您正在存取正確的物件。在Diku C中，存取角色物件通常是
完成者：

```c
/* creating pointer of both character and room struct */

void(struct char ch*, struct room room*){
    int dam;
    if (ROOM_FLAGGED(room, ROOM_LAVA)){
        dam = 100;
        ch->damage_taken = dam;
    }
}
```

作為透過 `from evennia import Command` 字元在 Evennia 中建立指令的範例
呼叫該指令的物件由類別屬性表示為 `self.caller`。在這個例子中
`self.caller` 本質上是呼叫指令的“物件”，但大多數時候它是一個
帳戶物件。為了獲得更熟悉的 Diku 感覺，建立一個成為帳戶物件的變數，如下所示：

```python
#mygame/commands/command.py

from evennia import Command

class CmdMyCmd(Command):
    """
    This is a Command Evennia Object
    """

    [...]

    def func(self):
        ch = self.caller
        # then you can access the account object directly by using the familiar ch.
        ch.msg("...")
        account_name = ch.name
        race = ch.db.race

```

如上所述，必須注意您正在處理的具體物件。如果專注於一個
room 物件，您需要存取 account 物件：

```python
#mygame/typeclasses/room.py

from evennia import DefaultRoom

class MyRoom(DefaultRoom):
    [...]

    def is_account_object(self, object):
        # a test to see if object is an account
        [...]

    def myMethod(self):
        #self.caller would not make any sense, since self refers to the
        # object of 'DefaultRoom', you must find the character obj first:
        for ch in self.contents:
            if self.is_account_object(ch):
                # now you can access the account object with ch:
                account_name = ch.name
                race = ch.db.race
```


(emulating-evennia-to-look-and-feel-like-a-dikurom)=
## 模仿 Evennia 使其外觀和感覺像 Diku/ROM

要在 Evennia 上模擬 Diku Mud，必須事先完成一些工作。如果有什麼事情都是
程式設計師和建構者從 Diku/Rom 時代就記得 VNUMs 的存在。基本上所有資料都是
儲存在平面檔案中並按 VNUMs 建立索引以便於存取。 Evennia有能力模仿VNUMS
達到將 rooms/mobs/objs/trigger/zones[...] 分類到 vnum 範圍的程度。

Evennia 具有名為 Scripts 的物件。根據定義，它們是「遊戲外」例項
存在於泥漿中，但從未直接與之相互作用。 Scripts可用於計時器，生物AI，
甚至獨立的資料庫。

由於其奇妙的結構，所有生物、房間、區域、觸發器等..資料都可以儲存在
獨立建立全域scripts。

這是來自 Diku Derived 平面檔案的範例 mob 檔案。

```text
#0
mob0~
mob0~
mob0
~
   Mob0
~
10 0 0 0 0 0 0 0 0 E
1 20 9 0d0+10 1d2+0
10 100
8 8 0
E
#1
Puff dragon fractal~
Puff~
Puff the Fractal Dragon is here, contemplating a higher reality.
~
   Is that some type of differential curve involving some strange, and unknown
calculus that she seems to be made out of?
~
516106 0 0 0 2128 0 0 0 1000 E
34 9 -10 6d6+340 5d5+5
340 115600
8 8 2
BareHandAttack: 12
E
T 95
```
每行代表 MUD 讀入的內容並對其執行某些操作。這並不容易
閱讀，但讓我們看看是否可以將其模擬為儲存在已建立的資料庫 script 上的字典
在Evennia中。

首先，讓我們建立一個絕對不執行任何操作且不附加任何內容的全域 script。你
可以使用 @py 指令直接在遊戲中建立它，也可以在另一個檔案中建立它來執行一些操作
檢查和平衡是否出於某種原因需要再次建立 script。它
可以這樣做：

```python
from evennia import create_script

mob_db = create_script("typeclasses.scripts.DefaultScript", key="mobdb",
                       persistent=True, obj=None)
mob_db.db.vnums = {}
```
只需建立一個簡單的 script 物件並為其分配一個 'vnums' attribute 作為型別字典即可。
接下來我們必須建立生物佈局..

```python
# vnum : mob_data

mob_vnum_1 = {
            'key' : 'puff',
            'sdesc' : 'puff the fractal dragon',
            'ldesc' : 'Puff the Fractal Dragon is here, ' \
                      'contemplating a higher reality.',
            'ddesc' : ' Is that some type of differential curve ' \
                      'involving some strange, and unknown calculus ' \
                      'that she seems to be made out of?',
            [...]
        }

# Then saving it to the data, assuming you have the script obj stored in a variable.
mob_db.db.vnums[1] = mob_vnum_1
```

這是一個非常「穴居人」的例子，但它傳達了這個想法。您可以使用中的按鍵
`mob_db.vnums` 充當 mob vnum，而其餘部分則包含資料。

閱讀和編輯更加簡單。如果您打算走這條路線，您必須記住，
例如，當使用 `look` 指令時，預設 evennia “檢視”不同的屬性。如果你
建立該生物的一個例項並使其`self.key = 1`，預設為evennia會說：

`Here is: 1`

您必須重構所有預設指令，以便 mud 檢視定義在
你的暴民。
