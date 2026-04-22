(character-creator)=
# 角色創造者

貢獻者 InspectorCaracal, 2022

用於管理和啟動遊戲內角色建立選單的指令。

(installation)=
## 安裝

在你的遊戲資料夾`commands/default_cmdsets.py`中，匯入並新增
`ContribChargenCmdSet` 到你的`AccountCmdSet`。

例子：
```python
from evennia.contrib.rpg.character_creator.character_creator import ContribChargenCmdSet

class AccountCmdSet(default_cmds.AccountCmdSet):

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(ContribChargenCmdSet)
```

在您的遊戲資料夾`typeclasses/accounts.py`中，匯入並繼承自`ContribChargenAccount`
在您的帳戶類別上。

（或者，您可以將 `at_look` 方法直接複製到您自己的類別中。）

(example)=
### 例子：

```python
from evennia.contrib.rpg.character_creator.character_creator import ContribChargenAccount

class Account(ContribChargenAccount):
    # your Account class code
```

在您的設定檔`server/conf/settings.py`中，新增以下設定：

```python
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
AUTO_PUPPET_ON_LOGIN = False
```

（如果你想讓玩家創造多個角色，你可以
使用設定 `MAX_NR_CHARACTERS` 進行自訂。）

預設情況下，新的 `charcreate` 指令將引用範例選單
由 contrib 提供，因此您可以在建立自己的選單之前對其進行測試。
您可以參考
[此處的範例選單](github:develop/evennia/contrib/rpg/character_creator/example_menu.py) 用於
關於如何建構自己的想法。

擁有自己的選單後，只需將其新增到您的設定即可使用。 e.g。如果你的選單在
`mygame/word/chargen_menu.py`，您需要將以下內容新增至您的設定檔：

```python
CHARGEN_MENU = "world.chargen_menu"
```

(usage)=
## 用法

(the-evmenu)=
### EvMenu

為了使用contrib，您需要建立自己的chargen EvMenu。
包含的 `example_menu.py` 提供了許多有用的選單節點技術
有基本的attribute範例供您參考。它可以按原樣執行
為您自己/您的開發人員提供教學，或用作您自己的選單的基礎。

範例選單包括以下型別的程式碼、提示和說明
決策節點數：

(informational-pages)=
#### 資訊頁面

一小組節點，可讓您在做出選擇之前翻閱不同選擇的資訊。

(option-categories)=
#### 選項類別

一對節點，可讓您將任意數量的選項分割為不同的類別。

基本節點有一個類別清單作為選項，子節點顯示實際的字元選擇。

(multiple-choice)=
#### 多項選擇

允許玩家從清單中選擇和取消選擇選項，以便選擇多個選項。

(starting-objects)=
#### 起始物件

允許玩家從一系列起始物件中進行選擇，然後在充電完成時建立這些起始物件。

(choosing-a-name)=
#### 選擇名字

contrib 假設玩家將在角色建立期間選擇他們的名字，
所以當然包括這樣做所需的程式碼！


(charcreate-command)=
### `charcreate`指令

contrib 覆蓋角色建立指令 - `charcreate` - 以使用
角色建立器選單，以及支援退出/恢復過程。在
另外，與核心指令不同，它是為角色名稱設計的
稍後透過選單選擇，因此它不會解析傳遞給它的任何引數。

(changes-to-account)=
### 更改為`Account`

contrib 版本的工作原理與核心 evennia 基本上相同，但修改了 `ooc_appearance_template`
匹配 contrib 的指令語法，以及 `at_look` 方法來識別正在進行的程式
性格。

如果您修改了自己的 `at_look` 掛鉤，則新增更改很容易：只需將此部分新增到
可玩角色列表迴圈。

```python
    # the beginning of the loop starts here
    for char in characters:
        # ...
        # contrib code starts here
        if char.db.chargen_step:
            # currently in-progress character; don't display placeholder names
            result.append(" - |Yin progress|n (|wcharcreate|n to continue)")
            continue
        # the rest of your code continues here
```



----

<small>此檔案頁面是從`evennia\contrib\rpg\character_creator\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
