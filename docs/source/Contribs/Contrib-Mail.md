(in-game-mail-system)=
# 遊戲內郵件系統

grungies1138 2016 的貢獻

一個簡單的 Brandymail 風格的郵件系統，使用來自 Evennia 的 `Msg` 類
核心。它有兩個指令用於在帳戶之間傳送郵件（遊戲外）
或角色之間（遊戲中）。這兩種型別的郵件可以一起使用或
靠他們自己。

   - `CmdMail` - 這應該位於帳戶 cmdset 上並執行 `mail` 指令
    available both IC and OOC. Mails will always go to Accounts (other players).
   - `CmdMailCharacter` - 這應該位於角色 cmdset 上並使 `mail`
    command ONLY available when puppeting a character. Mails will be sent to other
    Characters only and will not be available when OOC.
   - 如果將*兩個*指令新增到各自的cmdsets，您將得到兩個單獨的
    IC and OOC mailing systems, with different lists of mail for IC and OOC modes.

(installation)=
## 安裝：

安裝以下一項或兩項（見上文）：

- CmdMail（IC + OOC 郵件，在玩家之間傳送）

    ```python
    # mygame/commands/default_cmds.py

    from evennia.contrib.game_systems import mail

    # in AccountCmdSet.at_cmdset_creation:
        self.add(mail.CmdMail())
    ```
- CmdMailCharacter（可選，IC僅郵件，在字元之間傳送）

    ```python
    # mygame/commands/default_cmds.py

    from evennia.contrib.game_systems import mail

    # in CharacterCmdSet.at_cmdset_creation:
        self.add(mail.CmdMailCharacter())
    ```
安裝後，在遊戲中使用 `help mail` 來取得郵件指令的協助。使用
ic/ooc 切換到 IC/OOC 模式。


----

<small>此檔案頁面是從`evennia\contrib\game_systems\mail\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
