(npcs-that-listen-to-what-is-said)=
# NPCs 表示聽話

    > say hi 
    You say, "hi"
    The troll under the bridge answers, "well, well. Hello."

本指南解釋如何製作一個 NPC 對角色在當前位置說話做出反應。此原則適用於其他情況，例如敵人加入戰鬥或對角色拔出武器做出反應。

```python
# mygame/typeclasses/npc.py

from characters import Character

class Npc(Character):
    """
    A NPC typeclass which extends the character class.
    """
    def at_heard_say(self, message, from_obj):
        """
        A simple listener and response. This makes it easy to change for
        subclasses of NPCs reacting differently to says.       

        """ 
        # message will be on the form `<Person> says, "say_text"`
        # we want to get only say_text without the quotes and any spaces
        message = message.split('says, ')[1].strip(' "')

        # we'll make use of this in .msg() below
        return f"{from_obj} said: '{message}'"
```

我們加入一個簡單的方法 `at_heard_say` 來格式化它聽到的內容。我們假設輸入的訊息採用 `Someone says, "Hello"` 的形式，並且我們確保在該範例中僅獲取 `Hello`。

我們實際上還沒有呼叫`at_heard_say`。接下來我們會處理這個問題。

當房間裡有人對這個 NPC 說話時，它的 `msg` 方法將會被呼叫。我們將修改
NPCs `.msg` 捕獲方法表示 NPC 可以回應。


```{code-block} python
:linenos:
:emphasize-lines:

# mygame/typeclasses/npc.py

from characters import Character
class Npc(Character):

    # [at_heard_say() goes here]

    def msg(self, text=None, from_obj=None, **kwargs):
        "Custom msg() method reacting to say."

        if from_obj != self:
            # make sure to not repeat what we ourselves said or we'll create a loop
            try:
                # if text comes from a say, `text` is `('say_text', {'type': 'say'})`
                say_text, is_say = text[0], text[1]['type'] == 'say'
            except Exception:
                is_say = False
            if is_say:
                # First get the response (if any)
                response = self.at_heard_say(say_text, from_obj)
                # If there is a response
                if response != None:
                    # speak ourselves, using the return
                    self.execute_cmd(f"say {response}")   
    
        # this is needed if anyone ever puppets this NPC - without it you would never
        # get any feedback from the server (not even the results of look)
        super().msg(text=text, from_obj=from_obj, **kwargs) 
```

因此，如果 NPC 獲得發言權，並且該發言權不是來自 NPC 本身，它將使用
`at_heard_say` 鉤子。上面的例子中有一些值得注意的地方：

- **第 15 行** `text` 輸入可以採用多種不同的形式，取決於呼叫 `msg` 的位置。如果您檢視[“say”指令的程式碼](evennia.commands.default.general.CmdSay)，您會發現它將使用 `("Hello", {"type": "say"})` 呼叫 `.msg`。  我們利用這些知識來確定這是否來自 `say`。
- **第 24 行**：我們使用 `execute_cmd` 觸發 NPCs 自己的 `say` 指令。這是有效的，因為 NPC 實際上是 `DefaultCharacter` 的子級 - 所以它上面有 `CharacterCmdSet`！  通常你應該謹慎使用`execute_cmd`；直接呼叫指令使用的實際程式碼通常更有效。對於本教學，呼叫指令的編寫時間較短，同時確保呼叫所有掛鉤
- **第26行**：注意最後關於`super`的註解。這也將觸發“預設”`msg`（在父類別中）。只要沒有人傀儡NPC（`@ic <npcname>`），這並不是真的必要，但明智的做法是留在那兒，因為如果`msg()`從不向他們返回任何東西，傀儡玩家將完全失明！

現在已經完成了，讓我們建立一個 NPC 並看看它本身有什麼含義。

```
reload
create/drop Guild Master:npc.Npc
```

（您也可以將路徑指定為 `typeclasses.npc.Npc`，但 Evennia 將檢視 `typeclasses`
自動資料夾，所以這有點短）。

    > say hi
    You say, "hi"
    Guild Master says, "Anna said: 'hi'"

(assorted-notes)=
## 什錦筆記

有很多方法可以實現這種功能。覆蓋的替代範例
`msg` 將改為修改 *Character* 上的 `at_say` 掛鉤。它可以檢測到它是
傳送到 NPC 並直接呼叫 `at_heard_say` 掛鉤。

雖然教學解決方案的優點是僅包含在 NPC 類別中，
將此與使用 Character 類別結合可以更直接地控制 NPC 將如何反應。選擇哪種方式取決於特定遊戲的設計要求。