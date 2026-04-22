(messages-varying-per-receiver)=
# 每個接收者的訊息各不相同

向某個位置中的所有人傳送訊息由 [msg_contents](evennia.objects.objects.DefaultObject.msg_contents) 方法處理
所有[物件](../Components/Objects.md)。它最常被稱為房間。

```python
room.msg_contents("Anna walks into the room.")
```

您也可以在字串中嵌入引用：

```python

room.msg_contents("{anna} walks into the room.",
                  from_obj=caller,
                  mapping={'anna': anna_object})
```

使用 `exclude=object_or_list_of_object` 跳過向一個或多個目標傳送訊息。

這樣做的好處是每個圍觀的人都會叫`anna_object.get_display_name(looker)`；這允許 `{anna}` 節根據誰看到字串而有所不同。這是如何運作的取決於你的遊戲的_立場_。

立場顯示你的遊戲如何向玩家傳達其訊息。知道你想要怎樣
對於文字遊戲來說，掌握好姿勢很重要。通常考慮的主要立場有兩種，_演員立場_和_導演立場_。

| 姿態     | 你看    |    同一位置的其他人請參閱 |
| --- | --- | --- |
| 演員姿態 | 你撿起石頭 | 安娜撿起石頭 |
|導演立場 | 安娜撿起石頭 | 安娜撿起石頭 |

混合兩種姿勢並非聞所未聞 - 遊戲中的指令以演員姿勢傳達，而導演姿勢則用於複雜的情感和角色扮演。然而，人們通常應該努力保持一致。

(director-stance)=
## 導演立場

雖然導演的立場不像演員的立場那麼常見，但它的優點是簡單，尤其是
在角色扮演 MUDs 中使用較長的角色扮演表情。這也是一個非常簡單的立場
從技術上實施，因為無論觀點如何，每個人都會看到相同的文字。

這是一個展示房間的有趣文字的範例：

    Tom picks up the gun, whistling to himself.

每個人都會看到這個字串，包括湯姆和其他人。以下是如何將其傳送給每個人
房間。

```python
text = "Tom picks up the gun, whistling to himself."
room.msg_contents(text)
```

人們可能想透過讓不同的人對 `Tom` 這個名字有不同的看法來擴充套件它，
但句子的英文文法沒有改變。這不僅很容易做到
從技術上來說，對於玩家來說編寫起來也很容易。

(actor-stance)=
## 演員姿態

這意味著遊戲在做事時會針對「你」。在演員的立場上，每當你執行一個動作時，你應該得到與那些_觀察_你執行該動作的人不同的訊息。

    Tom picks up the gun, whistling to himself.

這是_其他_應該看到的。玩家自己應該會看到這一點：

    You pick up the gun, whistling to yourself.

您不僅需要將上面的“Tom”對映到“You”，而且還存在語法差異 - “Tom walks”與“You walks”以及“himself”與“yourself”。這處理起來要複雜得多。對於製作簡單的“你/湯姆撿起石頭”訊息的開發人員來說，原則上您可以從每個角度手工製作字串，但有更好的方法。

`msg_contents` 方法透過使用 [FuncParser 函式](../Components/FuncParser.md) 和一些非常具體的 `$inline-functions` 解析傳入字串來提供協助。行內函數基本上為您提供了一種用於構建_one_字串的迷你語言，該字串將根據誰看到它而適當地更改。

```python
text = "$You() $conj(pick) up the gun, whistling to $pron(yourself)."
room.msg_contents(text, from_obj=caller, mapping={"gun": gun_object})
```

這些是可用的行內函數：

- `$You()/$you()` - 這是文字中對“您”的引用。它將被替換為“你/你”
傳送簡訊並從 `caller.get_display_name(looker)` 返回給其他人的人。
- `$conj(verb)` - 這將根據誰看到該字串來結合給定的動詞（例如 `pick`
到`picks`）。輸入動詞的字根形式。
- `$pron(pronoun[,options])` - 代名詞是您想要用來代替專有名詞的單詞，例如
_他_、_她自己_、_它_、_我_、_我_、_他們_等等。 `options` 是空格或逗號分隔的
  一組選項可幫助系統將代名詞從第一/第二人稱對映到第三人稱，反之亦然。請參閱下一節。

(more-on-pron)=
### 更多關於 $pron()

`$pron()` 行內函數在第一/第二人（我/你）到第三人（他/她等）之間對映。簡而言之，
它在這張表之間翻譯...

| |  主詞代名詞 | 賓語代名詞 | 所有格形容詞 | 所有格代名詞 | 反身代名詞 |
| --- | --- | --- | --- | --- | --- |
|    **第一個人**          |   我    |    我   |    我的    |   礦    |  我      |
|    **第一人稱複數**   |   我們   |    我們   |    我們的   |    我們的   |   我們自己  |
|    **第二人**          |   你  |    你  |    你的  |    你的  |   你自己   |
|    **第二人稱複數**   |   你  |    你  |    你的  |    你的  |   你們自己  |

....到此表（雙向）：

| | 主詞代名詞 | 賓語代名詞 | 所有格形容詞 | 所有格代名詞 | 反身代名詞 |
| --- | --- | --- | --- | --- | --- |
|    **第三人稱男性**     |   他   |    他  |    他的   |    他的    |   他自己  |
|    **第三人稱女性**   |   她  |    她  |    她   |    她的   |   她自己  |
|    **第三人稱中立**  |   它   |    它   |    它是   |   他們的*  |   本身   |
|    **第三人稱複數**   |   他們 |   他們  |    他們的 |    他們的 |   他們自己 |

有些對映很簡單。例如，如果您寫`$pron(yourselves)`，則第三人稱形式始終為`themselves`。但由於英文文法就是這樣，並非所有對映都是 1:1。例如，如果您寫`$pron(you)`，Evennia 將不知道這應該對映到哪個第三人稱 - 您需要提供更多資訊來幫助解決。這可以作為 `$pron` 的第二個空格分隔選項提供，或者係統將嘗試自行解決。

- `pronoun_type` - 這是表中的欄位之一，可以設定為 `$pron` 選項。

   - `subject pronoun`（別名`subject`或`sp`）
   - `object pronoun`（別名`object`或`op`）
   - `possessive adjective`（別名`adjective`或`pa`）
   - `possessive pronoun`（別名`pronoun`或`pp`）。

（無需指定反身代名詞，因為它們
  全部按 1:1 唯一對映）。使用`you`時主要需要指定代名詞型別，
  因為在英語文法中同一個「you」用來表示各種事物。
  如果未指定且對映不清楚，則假定為「主詞代名詞」（他/她/它/他們）。
- `gender` - 在 `$pron` 選項中設定為

   - `male`，或`m`
   - `female'` 或 `f`
   - `neutral`，或`n`
   - `plural` 或 `p`（是的，出於此目的，複數被視為「性別」）。

如果未設定為選項，系統將
  在當前 `from_obj` 上尋找可呼叫或屬性 `.gender`。一個可呼叫的將被呼叫
  不含引數，預計回傳字串「male/female/neutral/plural」。如果沒有
  如果發現，則假定為中性性別。
- `viewpoint`- 在 `$pron` 選項中設定為

   - `1st person`（別名`1st`或`1`）
   - `2nd person`（別名`2nd`或`2`）

僅當您想要第一人稱視角時才需要 - 如果
   不是，只要觀點不明確，就假定第二人稱。

`$pron()` 例：

| 輸入            |   你看  |  別人看到 |  筆記 |
| --- | --- | ---| --- |
| `$pron(I, male)`    |         我           |     他       |   |
| `$pron(I, f)`    |         我           |     她       |   |
| `$pron(my)` | 我的 | 它是 | 發現這是一個所有格形容詞，假設為中性 |
| `$pron(you)`   |         你         |  它     | 假定中性主詞代名詞 |
| `$pron(you, f)`   |        你         |     她  | 指定女性，採用主詞代名詞 |
| `$pron(you,op f)`   |      你         |     她 | |
| `$pron(you,op p)`   |      你         |     他們 | |
| `$pron(you, f op)` | 你 | 她 | 指定女性和客觀代名詞|
| `$pron(yourself)`  |       你自己    |     本身 | |
| `$pron(its)`        |      你的        |     它是  | |
| `$Pron(its)`        |      你的        |     它是 | 使用 $Pron 總是大寫 |
| `$pron(her)`        |      你        |     她  | 第三人→第二人 |
| `$pron(her, 1)`        |   我        |       她  | 第三人 -> 第一人 |
| `$pron(its, 1st)`      |  我的        |       它是  | 第三人 -> 第一人  |

請注意最後三個範例 - 您也可以指定第三人稱形式並執行「反向」查詢，而不是指定第二人稱形式 - 您仍然會看到正確的第一/第二文字。因此，寫 `$pron(her)` 而不是 `$pron(you, op f)` 會得到相同的結果。

[$pron inlinefunc api 可以在這裡找到](evennia.utils.funcparser.funcparser_callable_pronoun)

(referencing-other-objects)=
## 引用其他物件

還有一個 `msg_contents` 可以理解的 inlinefunc。這可以本地使用來修飾
你的弦（導演和演員的立場）：

- `$Obj(name)/$obj(name)` 引用另一個實體，必須提供該實體
在 `msg_contents` 的 `mapping` 關鍵字引數中。該物件的 `.get_display_name(looker)` 將是
  而是呼叫並插入。這本質上與我們使用的 `{anna}` 標記相同
  在本頁頂部的第一個範例中，但使用 `$Obj/$obj` 可以讓您輕鬆地
  控制大小寫。

這是這樣使用的：

```python
# director stance
text = "Tom picks up the $obj(gun), whistling to himself"

# actor stance
text = "$You() $conj(pick) up the $obj(gun), whistling to $pron(yourself)"

room.msg_contents(text, from_obj=caller, mapping={"gun": gun_object})
```
根據你的遊戲，湯姆現在可能會看到自己撿起`A rusty old gun`，而具有高槍械史密斯技能的旁觀者可能會看到他撿起`A rare-make Smith & Wesson model 686 in poor condition"...`

(recog-systems-and-roleplaying)=
## 識別系統和角色扮演

`$funcparser` 行內函數對於遊戲開發者來說非常強大，但是它們可能
對於普通玩家來說寫得有點太多了。

[rpsystem contrib](evennia.contrib.rpg.rpsystem) 實現了一個完整的動態表情/姿勢和識別系統，具有簡短的描述和偽裝。它使用帶有自訂標記語言的導演姿態，例如 `/me` `/gun` 和 `/tall man` 來引用該位置中的玩家和物件。值得一試以獲得靈感。
