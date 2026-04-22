(adding-a-command-prompt)=
# 新增指令提示符

*提示*在 MUDs 中很常見：

    HP: 5, MP: 2, SP: 8
    > 

該提示顯示有關您的角色的有用詳細資訊，您可能希望始終密切關注這些資訊。它可以是生命值、魔力、金幣和當前位置。它還可能顯示遊戲時間、天氣等資訊。

傳統上，提示（無論是否更改）都會隨伺服器的每個回復一起返回，並且僅顯示在其自己的行上。許多現代 MUD 用戶端（包括 Evennia 自己的 webclient）允許識別提示並將其顯示在就地更新的固定位置（通常就在輸入行上方）。

(a-fixed-location-prompt)=
## 固定位置提示

使用 `prompt` 關鍵字將提示傳送到物件上的 `msg()` 方法。提示將是
傳送時沒有任何換行符。

```python
self.msg(prompt="HP: 5, MP: 2, SP: 8")
```
您可以將普通文字的傳送與傳送（提示的更新）結合：

```python
self.msg("This is a text", prompt="This is a prompt")
```

您可以根據需要更新提示，這通常使用 [OOB](../Concepts/OOB.md) 來完成 - 追蹤相關
屬性（如角色的健康狀況）。您也可以確保攻擊指令更新
例如，當它們導致健康狀況發生變化時進行提示。

以下是從指令類別傳送/更新的提示的簡單範例：

```python
    from evennia import Command

    class CmdDiagnose(Command):
        """
        see how hurt your are

        Usage: 
          diagnose [target]

        This will give an estimate of the target's health. Also
        the target's prompt will be updated. 
        """ 
        key = "diagnose"
        
        def func(self):
            if not self.args:
                target = self.caller
            else:
                target = self.caller.search(self.args)
                if not target:
                    return
            # try to get health, mana and stamina
            hp = target.db.hp
            mp = target.db.mp
            sp = target.db.sp

            if None in (hp, mp, sp):
                # Attributes not defined          
                self.caller.msg("Not a valid target!")
                return 
             
            text = f"You diagnose {target} as having {hp} health, {mp} mana and {sp} stamina."
            prompt = f"{hp} HP, {mp} MP, {sp} SP"
            self.caller.msg(text, prompt=prompt)
```
(a-prompt-with-every-command)=
## 每個指令都有提示

如上所述傳送的提示使用標準 telnet 指令（Evennia Web 使用者端獲得特殊標誌）。大多數 MUD telnet 使用者端會理解並允許使用者捕獲此資訊並保留提示直到其更新。所以*原則上*您不需要更新每個指令的提示。

然而，由於使用者群不同，可能不清楚使用了哪些用戶端以及使用者具有何種技能水平。因此，為每個指令傳送提示是一個安全的包羅永珍的方法。不過，您不需要手動進入並編輯您擁有的每個指令。相反，您可以編輯自訂指令的基本指令類別（例如 `mygame/commands/command.py` 資料夾中的 `MuxCommand`）並過載 `at_post_cmd()` 掛鉤。此掛鉤始終在指令的主要 `func()` 方法*之後呼叫。

```python
from evennia import default_cmds

class MuxCommand(default_cmds.MuxCommand):
    # ...
    def at_post_cmd(self):
        "called after self.func()."
        caller = self.caller        
        prompt = f"{caller.db.hp} HP, {caller.db.mp} MP, {caller.db.sp} SP"
        caller.msg(prompt=prompt)

```

(modifying-default-commands)=
### 修改預設指令

如果你想將像這樣的小東西新增到 Evennia 的預設指令中而不直接修改它們，最簡單的方法是將那些具有多重繼承的指令包裝到你自己的基類中：

```python
# in (for example) mygame/commands/mycommands.py

from evennia import default_cmds
# our custom MuxCommand with at_post_cmd hook
from commands.command import MuxCommand

# overloading the look command
class CmdLook(default_cmds.CmdLook, MuxCommand):
    pass
```

這樣做的結果是，自訂 `MuxCommand` 中的鉤子將混合到預設值中
`CmdLook` 透過多重繼承。接下來，您只需將其新增至預設指令集中：

```python
# in mygame/commands/default_cmdsets.py

from evennia import default_cmds
from commands import mycommands

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    # ...
    def at_cmdset_creation(self):
        # ...
        self.add(mycommands.CmdLook())
```

這將自動用您自己的版本替換遊戲中預設的 `look` 指令。