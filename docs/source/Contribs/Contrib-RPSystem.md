(roleplaying-base-system-for-evennia)=
# Evennia 的角色扮演基礎系統

Griatch 的貢獻，2015 年

完整的角色扮演表情系統。簡短的描述和識別（在給他們指定名字之前只能透過外表來認識他們）。房間姿勢。面具/偽裝（隱藏您的描述）。直接用表情說話，可選擇語言模糊（如果您不懂該語言，單字會出現亂碼，您也可以使用不同的語言，並具有不同的「發音」亂碼）。從遠處就可以聽到部分耳語。一個非常強大的表情內參考系統，用於參考和區分目標（包括物件）。

該系統包含兩個主要模組——角色扮演表情系統和語言模糊模組。

(roleplaying-emotes)=
## 角色扮演表情

此模組包含ContribRPObject、ContribRPRoom 和ContribRPCharacter typeclasses。  如果您從這些繼承您的物件/房間/角色（或將它們設為預設值），您將獲得以下功能：

- 物件/房間將能夠擁有姿勢並報告其內部物品的姿勢（後者對房間最有用）。
- 角色將獲得姿勢和 sdesc（簡短描述），這些將用來代替他們的按鍵。他們將獲得管理識別的指令（自訂 sdesc 替換）、隱藏自己以及高階的自由形式表情指令。

更詳細地說，這個 RP 基本系統為遊戲引入了以下功能，這是許多 RP- 中心遊戲所共有的：

- 使用導演姿態表情的表情系統（名稱/sdescs）。  這使用可自訂的替換名詞（/me、@等）來代表您的表情。您可以使用 /sdesc、/nick、/key 或 /alias 來引用房間中的物件。您可以使用任意數量的 sdesc 子部分來區分本地 sdesc，或使用 /1-sdesc 等來區分它們。該表情還識別巢狀的說並分隔大小寫。
- sdesc 隱藏真實角色名稱，用於表情和任何引用，例如 object.search()。  這依賴於在角色上設定的 SdescHandler `sdesc` 並使用自訂角色。 get_display_name 掛鉤。如果未設定 sdesc，則使用字元的 `key`。這尤其用於情緒系統。
- 識別系統為角色分配您自己的暱稱，然後可以用於參考。使用者可以識別使用者並向他們分配任何個人暱稱。這將在描述中顯示並用於引用它們。這是利用 Evennia 的暱稱功能。
- 隱藏您身分的面具（使用簡單的lock）。
- 姿勢系統設定房間持久姿勢，在房間描述中以及在檢視人/物體時可見。  這是一個簡單的Attribute，它以 sdesc + 姿勢修改角色在房間中的觀看方式。
- in-emote 表示，包括與語言模糊例程的無縫整合（例如 contrib/rplanguage.py）

(installation)=
### 安裝：

將此模組中的 `RPSystemCmdSet` 新增到您的 CharacterCmdSet：

```python
# mygame/commands/default_cmdsets.py

# ...

from evennia.contrib.rpg.rpsystem import RPSystemCmdSet  <---

class CharacterCmdSet(default_cmds.CharacterCmdset):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(RPSystemCmdSet())  # <---

```

您還需要使您的角色/物件/房間繼承自
該模組中的typeclasses：

```python
# in mygame/typeclasses/characters.py

from evennia.contrib.rpg.rpsystem import ContribRPCharacter

class Character(ContribRPCharacter):
    # ...

```

```python
# in mygame/typeclasses/objects.py

from evennia.contrib.rpg.rpsystem import ContribRPObject

class Object(ContribRPObject):
    # ...

```

```python
# in mygame/typeclasses/rooms.py

from evennia.contrib.rpg.rpsystem import ContribRPRoom

class Room(ContribRPRoom):
    # ...

```
您需要設定Evennia以使用RPsystem的形式來分離
sdescs (`3-tall`) 之間，使其與 Evennia 的其餘部分相容
分隔其他多重符合的搜尋/指令：

    SEARCH_MULTIMATCH_REGEX = r"(?P<number>[0-9]+)-(?P<name>[^-]*)(?P<args>.*)"
    SEARCH_MULTIMATCH_TEMPLATE = " {number}-{name}{aliases}{info}\n"

最後，您將需要重新載入伺服器並可能強制重新載入
你的物件，如果你最初建立它們時沒有使用它。

您的角色範例：

    > type/reset/force me = typeclasses.characters.Character


(usage)=
### 用法

(sdescs)=
#### 描述

    > look

    Tavern
    The tavern is full of nice people

    *A tall man* is standing by the bar.

上面是一個 sdesc“a high man”的玩家範例。這也是一個靜態*姿勢*的例子：「站在吧檯旁」是由高個子的玩家設定的，這樣人們一看他就知道發生了什麼。

    > emote /me looks at /Tall and says "Hello!"

我懂了：

    Griatch looks at Tall man and says "Hello".

高個子男人（假設他的名字是湯姆）看到：

    The godlike figure looks at Tom and says "Hello".

請注意，預設情況下，tag 的大小寫很重要，因此 `/tall` 將導致“tall man”，而 `/Tall` 將變為“Tall man”，而 /TALL 將變為 /TALL MAN。如果您不希望出現此行為，可以將 case_sensitive=False 傳遞給 `send_emote` 函式。

(language-integration)=
#### 語言整合

透過在語音前面加上語言鍵字首，可以將語音辨識為特定語言。

    emote says with a growl, orcish"Hello".

這會將語音「Hello」識別為獸人語，然後將該訊息傳遞給您角色上的 `process_language`。預設情況下，它不會做太多事情，但是您可以掛鉤語言系統（例如下面的 `rplanguage` 模組）來做更多有趣的事情。


(language-and-whisper-obfuscation-system)=
## 語言和耳語混淆系統

此模組旨在與表情系統（例如`contrib/rpg/rpsystem.py`）一起使用。它提供了以各種方式混淆遊戲中口頭單字的能力：

- 語言：語言功能定義了到任意數量語言的偽語言對映。  該字串將根據縮放比例進行混淆，該縮放比例（最有可能）將作為說話者和聽眾語言技能的加權平均值輸入。
- 耳語：耳語功能將按照 0-1 級逐漸「淡出」耳語，其中淡出是基於逐漸刪除（據說）更容易無意中聽到的耳語部分（例如，即使無法確定其他含義，「s」聲音也往往是可聽見的）。


(installation-1)=
### 安裝

該模組沒有新增新指令；將其嵌入到您的 say/emote/whisper 指令中。

(usage-1)=
### 用法：

```python
from evennia.contrib.rpg.rpsystem import rplanguage

# need to be done once, here we create the "default" lang
rplanguage.add_language()

say = "This is me talking."
whisper = "This is me whispering.

print rplanguage.obfuscate_language(say, level=0.0)
<<< "This is me talking."
print rplanguage.obfuscate_language(say, level=0.5)
<<< "This is me byngyry."
print rplanguage.obfuscate_language(say, level=1.0)
<<< "Daly ly sy byngyry."

result = rplanguage.obfuscate_whisper(whisper, level=0.0)
<<< "This is me whispering"
result = rplanguage.obfuscate_whisper(whisper, level=0.2)
<<< "This is m- whisp-ring"
result = rplanguage.obfuscate_whisper(whisper, level=0.5)
<<< "---s -s -- ---s------"
result = rplanguage.obfuscate_whisper(whisper, level=0.7)
<<< "---- -- -- ----------"
result = rplanguage.obfuscate_whisper(whisper, level=1.0)
<<< "..."

```

若要設定新語言，請匯入並使用此模組中的 `add_language()` 輔助方法。這允許您自訂您正在建立的半隨機語言的“感覺”。特別是 `word_length_variance` 有助於改變翻譯單字與原始單字的長度，並有助於改變您正在建立的語言的「感覺」。您還可以新增自己的字典並“修復”輸入單字列表中的隨機單字。

下面是「elvish」的一個例子，使用了「rounder」母音和發音：

```python
# vowel/consonant grammar possibilities
grammar = ("v vv vvc vcc vvcc cvvc vccv vvccv vcvccv vcvcvcc vvccvvcc "
           "vcvvccvvc cvcvvcvvcc vcvcvvccvcvv")

# all not in this group is considered a consonant
vowels = "eaoiuy"

# you need a representative of all of the minimal grammars here, so if a
# grammar v exists, there must be atleast one phoneme available with only
# one vowel in it
phonemes = ("oi oh ee ae aa eh ah ao aw ay er ey ow ia ih iy "
            "oy ua uh uw y p b t d f v t dh s z sh zh ch jh k "
            "ng g m n l r w")

# how much the translation varies in length compared to the original. 0 is
# smallest, higher values give ever bigger randomness (including removing
# short words entirely)
word_length_variance = 1

# if a proper noun (word starting with capitalized letter) should be
# translated or not. If not (default) it means e.g. names will remain
# unchanged across languages.
noun_translate = False

# all proper nouns (words starting with a capital letter not at the beginning
# of a sentence) can have either a postfix or -prefix added at all times
noun_postfix = "'la"

# words in dict will always be translated this way. The 'auto_translations'
# is instead a list or filename to file with words to use to help build a
# bigger dictionary by creating random translations of each word in the
# list *once* and saving the result for subsequent use.
manual_translations = {"the":"y'e", "we":"uyi", "she":"semi", "he":"emi",
                      "you": "do", 'me':'mi','i':'me', 'be':"hy'e", 'and':'y'}

rplanguage.add_language(key="elvish", phonemes=phonemes, grammar=grammar,
                         word_length_variance=word_length_variance,
                         noun_translate=noun_translate,
                         noun_postfix=noun_postfix, vowels=vowels,
                         manual_translations=manual_translations,
                         auto_translations="my_word_file.txt")

```

這將產生一種比預設語言更加“圓潤”和“柔和”的語言。這幾個`manual_translations`也確保至少表面上看起來「合理」。

`auto_translations` 關鍵字很有用，它接受清單或文字檔案的路徑（每行一個單字）。該單字清單用於根據語法規則「修復」這些單字的翻譯。只要語言存在，這些翻譯就會永久儲存。

這樣可以快速建立一個永不改變的大型翻譯單字語料庫。這產生了一種看起來相當一致的語言，因為像「the」這樣的字總是會被翻譯成相同的東西。  缺點（或優點，取決於您的遊戲）是玩家最終可以瞭解單字的含義，即使他們的角色不知道該語言。


----

<small>此檔案頁面是從`evennia\contrib\rpg\rpsystem\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
