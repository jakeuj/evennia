(characters)=
# 人物
**繼承樹：
```
┌─────────────┐
│DefaultObject│
└─────▲───────┘
      │
┌─────┴──────────┐
│DefaultCharacter│
└─────▲──────────┘
      │           ┌────────────┐
      │ ┌─────────►ObjectParent│
      │ │         └────────────┘
  ┌───┴─┴───┐
  │Character│
  └─────────┘
```

_Characters_是遊戲中的[物件](./Objects.md)，通常用於代表玩家在遊戲中的頭像。在 `mygame/typeclasses/characters.py` 中找到空的 `Character` 類。它繼承自 [DefaultCharacter](evennia.objects.objects.DefaultCharacter) 和（預設為空）`ObjectParent` 類別（如果想要在所有遊戲內物件之間新增共享屬性，則使用）。

當新的[帳戶](./Accounts.md)第一次登入Evennia時，會建立一個新的`Character`物件，並且[帳戶](./Accounts.md)將被設定為_傀儡_它。預設情況下，第一個角色將獲得與帳戶相同的名稱（但如果需要，Evennia 支援[替代連線樣式](../Concepts/Connection-Styles.md)）。

`Character` 物件通常會在建立時為其自身設定一個[預設指令集](./Command-Sets.md)，否則該帳戶將無法發出任何遊戲內指令！

如果你想更改預設指令建立的預設字元，可以在設定中更改：

    BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
    
這個預設指向 `mygame/typeclasses/characters.py` 中的空類，你可以隨意修改。