(nicks)=
# 尼克隊


*Nicks*，*Nicknames* 的縮寫，是一個允許物件（通常是[帳戶](./Accounts.md)）
為其他遊戲實體指派自訂替換名稱。

請勿將暱稱與*別名*混淆。在遊戲實體上設定別名實際上會改變
該實體固有的attribute，遊戲中的每個人都可以使用該別名
此後對實體進行定址。另一方面，*尼克* 用於對映*您的不同方式
alone* 可以指該實體。暱稱也常用於替換您的輸入文字，這意味著
您可以為預設指令建立自己的別名。

預設 Evennia 使用三種風格的 Nicks 來確定 Evennia 何時實際嘗試執行該操作
替代。

- inputline - 每當您在指令列上寫入任何內容時都會嘗試替換。這是
預設.
- 物件 - 僅在引用物件時嘗試替換
- 帳戶 - 僅在引用帳戶時嘗試更換

以下介紹如何在預設指令集中使用它（使用`nick`指令）：

     nick ls = look

對於習慣在日常使用`ls`指令的unix/linux使用者來說這是一個很好的選擇
生活。相當於`nick/inputline ls = look`。

     nick/object mycar2 = The red sports car 

在此範例中，僅針對需要物件的指令專門進行替換
參考，例如

     look mycar2 

相當於“`look The red sports car`”。

     nick/accounts tom = Thomas Johnsson

這對於明確搜尋帳戶的指令很有用：

     @find *tom 

可以使用缺刻來加快輸入速度。下面我們為自己新增了一個更快的方法來建立紅色按鈕。在
未來只需編寫 *rb* 就足以執行整個長字串。

     nick rb = @create button:examples.red_button.RedButton

Nicks 也可以用作構建適用於 RP 泥漿的「識別」系統的起點。

     nick/account Arnold = The mysterious hooded man

缺口替換器還支援 unix 風格的*模板化*：

     nick build $1 $2 = @create/drop $1;$2

這將捕獲空格分隔的引數並將它們儲存在 tags `$1` 和 `$2` 中，以便
插入替換字串中。此範例可讓您執行 `build box crate` 並擁有 Evennia
見`@create/drop box;crate`。您可以使用 1 到 99 之間的任何 `$` 數字，但標記必須
刻痕圖案與替換圖案之間的匹配。

> 如果您想捕獲指令引數的“其餘部分”，請確保放置 `$` tag *，不含空格
在它的右側* - 然後它將接收直到該行末尾的所有內容。

您也可以使用[shell型別萬用字元](http://www.linfo.org/wildcard.html)：

- \* - 符合所有內容。
- ？ - 匹配單一字元。
- [seq] - 匹配序列中的所有內容，e.g。 [xyz] 將會符合 x、y 和 z
- [!seq] - 匹配序列中*不*的所有內容。 e.g。 [!xyz] 將符合 x,y z 以外的所有內容。

(coding-with-nicks)=
## 有缺口的編碼

暱稱儲存為 `Nick` 資料庫模型，並從正常的 Evennia 引用
[物件](./Objects.md) 透過 `nicks` 屬性 - 這稱為 *NickHandler*。 NickHandler
提供有效的錯誤檢查、搜尋和轉換。

```python
    # A command/channel nick:
      obj.nicks.add("greetjack", "tell Jack = Hello pal!")
    
    # An object nick:  
      obj.nicks.add("rose", "The red flower", nick_type="object")
    
    # An account nick:
      obj.nicks.add("tom", "Tommy Hill", nick_type="account")
    
    # My own custom nick type (handled by my own game code somehow):
      obj.nicks.add("hood", "The hooded man", nick_type="my_identsystem")
    
    # get back the translated nick:
     full_name = obj.nicks.get("rose", nick_type="object")
    
    # delete a previous set nick
      object.nicks.remove("rose", nick_type="object")
```

在指令定義中，您可以透過 `self.caller.nicks` 存取缺口處理程式。請參閱`nick`
`evennia/commands/default/general.py` 中的指令以獲取更多範例。

最後一點，Evennia [頻道](./Channels.md) 別名系統正在使用帶有
`nick_type="channel"`，以便允許使用者為頻道建立自己的自訂別名。

(advanced-note)=
## 進階註釋

在內部，缺口是[屬性](./Attributes.md)儲存的，`db_attrype`設定為「缺口」（正常
屬性將此設為`None`）。

缺口將替換資料儲存在 Attribute.db_value 欄位中作為具有四個欄位的元組
`(regex_nick, template_string, raw_nick, raw_template)`。這裡 `regex_nick` 是轉換後的正規表示式
`raw_nick` 和 `template-string` 的表示形式是 `raw_template` 的一個版本
準備有效替換任何`$`-型標記。 `raw_nick` 和 `raw_template` 是
基本上是您輸入到 `nick` 指令中的未更改的字串（帶有未解析的 `$` 等）。

如果您出於某種原因需要存取該元組，請按以下方法操作：

```python
tuple = obj.nicks.get("nickname", return_tuple=True)
# or, alternatively
tuple = obj.nicks.get("nickname", return_obj=True).value
```