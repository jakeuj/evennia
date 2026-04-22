(easy-fillable-form)=
# 易於填寫的表格

蒂姆·阿什利·詹金斯 (Tim Ashley Jenkins) 貢獻，2018 年

該模組包含一個為您產生 `EvMenu` 的函式 - 這
選單向玩家呈現一種可以填滿的欄位形式
以任意順序輸出（e.g.用於角色生成或建構）。每個欄位的值可以
進行驗證，該功能可以輕鬆檢查文字和整數輸入，
最小值和最大值/字元長度，甚至可以由自訂驗證
功能。提交表單後，表單的資料將作為字典提交
到您選擇的任何可呼叫物件。

(usage)=
## 用法

初始化可填寫表單選單的函式相當簡單，且
包括呼叫者、表單範本和回呼（呼叫者，結果）
提交後，表單資料將傳送到該地址。

    init_fill_field(formtemplate, caller, formcallback)

表單範本被定義為字典列表 - 每個字典
代表表單中的一個欄位，包含欄位名稱和資料
行為。例如，這個基本表單範本將允許玩家填寫
簡短的人物簡介：

    PROFILE_TEMPLATE = [
        {"fieldname":"Name", "fieldtype":"text"},
        {"fieldname":"Age", "fieldtype":"number"},
        {"fieldname":"History", "fieldtype":"text"},
    ]

這將為玩家呈現一個 EvMenu 顯示此基本形式：

```
      Name:
       Age:
   History:
```

在此選單中，玩家可以使用以下指令為任何欄位指派新值：
語法 <field> = <new value>，如下所示：

```
    > name = Ashley
    Field 'Name' set to: Ashley
```

單獨輸入“look”將顯示表單及其目前值。

```
    > look

      Name: Ashley
       Age:
    History:
```

數字欄位需要整數輸入，並且將拒絕任何不能輸入的文字
轉換為整數。

```
    > age = youthful
    Field 'Age' requires a number.
    > age = 31
    Field 'Age' set to: 31
```

表單資料顯示為 EvTable，因此任何長度的文字都會乾淨地換行。

```
    > history = EVERY MORNING I WAKE UP AND OPEN PALM SLAM[...]
    Field 'History' set to: EVERY MORNING I WAKE UP AND[...]
    > look

      Name: Ashley
       Age: 31
   History: EVERY MORNING I WAKE UP AND OPEN PALM SLAM A VHS INTO THE SLOT.
            IT'S CHRONICLES OF RIDDICK AND RIGHT THEN AND THERE I START DOING
            THE MOVES ALONGSIDE WITH THE MAIN CHARACTER, RIDDICK. I DO EVERY
            MOVE AND I DO EVERY MOVE HARD.
```

當玩家輸入「提交」（或您指定的提交指令）時，選單
退出並且表單的資料會作為字典傳遞到您指定的函式，
像這樣：

    formdata = {"Name":"Ashley", "Age":31, "History":"EVERY MORNING I[...]"}

您可以在函式中使用這些資料做任何您喜歡的事情 - 可以使用表單
設定角色資料，幫助建構者建立物件，或讓玩家
製作物品或執行其他涉及許多變數的複雜動作。

您的表單將接受的資料也可以在表單範本中指定 -
例如，假設您不接受 18 歲以下或 100 歲以上的年齡。您可以
透過在欄位字典中指定“min”和“max”值來執行此操作：

```
    PROFILE_TEMPLATE = [
    {"fieldname":"Name", "fieldtype":"text"},
    {"fieldname":"Age", "fieldtype":"number", "min":18, "max":100},
    {"fieldname":"History", "fieldtype":"text"}
    ]
```

現在，如果玩家嘗試輸入超出範圍的值，表單將不會接受
給定值。

```
    > age = 10
    Field 'Age' reqiures a minimum value of 18.
    > age = 900
    Field 'Age' has a maximum value of 100.
```

為文字欄位設定“min”和“max”將充當最小值或
玩家輸入的最大字元長度。

有很多方法可以向玩家呈現表單 - 欄位可以有預設值
值或顯示自訂訊息來代替空白值，且玩家輸入可以
透過自訂函式進行驗證，具有很大的靈活性。那裡
也是「bool」欄位的選項，它只接受 True / False 輸入，並且
可以自訂以代表玩家的選擇，無論你喜歡什麼（例如
是/否、開/關、啟用/停用等）

這個模組包含一個簡單的範例表單，演示了所有包含的內容
功能 - 允許玩家向另一個玩家撰寫訊息的指令
線上角色並讓它在自訂延遲後傳送。你可以透過以下方式測試它
將此模組匯入到您遊戲的 `default_cmdsets.py` 模組中並新增
CmdTestMenu 到你的預設角色的指令集。

(field-template-keys)=
## FIELD TEMPLATE KEYS:

(required)=
### 必需的：

```
    fieldname (str): Name of the field, as presented to the player.
    fieldtype (str): Type of value required: 'text', 'number', or 'bool'.
```

(optional)=
### 選修的：

- max (int)：最大字元長度（如果是文字）或值（如果是數字）。
- min (int)：最小字元長度（如果是文字）或值（如果是數字）。
- truestr (str)：布林欄位中「True」值的字串。
（例如「開啟」、「啟用」、「是」）
- falsestr (str)：布林欄位中「False」值的字串。
（例如“關閉”、“禁用”、“否”）
- 預設值（str）：初始值（如果未給出則為空）。
- Blankmsg (str)：當欄位為空時顯示代替值的訊息。
- cantclear (bool)：如果為 True，則無法清除欄位。
- required (bool)：如果為 True，則欄位為空時無法提交表單。
- verifyfunc（可呼叫）：用於驗證輸入的可呼叫名稱 - 需要
（呼叫者，值）作為引數。如果函式傳回 True，
  玩家的輸入被認為是有效的 - 如果它返回 False，
  輸入被拒絕。傳回的任何其他值將充當
  此欄位的新值，替換玩家的輸入。這個
  允許使用非字串或整數的值（例如
  物件資料庫引用）。對於布林欄位，返回“0”或“1”進行設定
  欄位設定為 False 或 True。


----

<small>此檔案頁面是從`evennia\contrib\utils\fieldfill\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
