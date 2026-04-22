(components)=
# 成分

Contrib，ChrisLR，2021 年

使用元件/組合方法擴充套件typeclasses。

(the-components-contrib)=
## 組成部分Contrib

這contrib 向Evennia 介紹了元件和成分。
每個「元件」類別代表將在 typeclass 例項上「啟用」的功能。
您可以在執行時在整個 typeclass 或單一物件上註冊這些元件。
它透過使用 Evennia 的 AttributeHandler 支援持久屬性和記憶體屬性。

(pros)=
## 優點
- 您可以在多個 typeclasses 之間重複使用某個功能，而無需繼承
- 您可以將每個功能清楚地組織到一個獨立的類別中。
- 您可以檢查物件是否支援某個功能，而無需檢查其例項。

(cons)=
## 缺點
- 它引入了額外的複雜性。
- 需要主機 typeclass 例項。

(how-to-install)=
## 如何安裝

要啟用對 typeclass 的元件支援，
匯入並繼承ComponentHolderMixin，與此類似
```python
from evennia.contrib.base_systems.components import ComponentHolderMixin
class Character(ComponentHolderMixin, DefaultCharacter):
# ...
```

元件需要繼承Component類，並且需要唯一的名稱。
元件可以繼承自其他元件，但必須指定另一個名稱。
您可以將相同的“槽”指派給兩個元件以獲得替代實作。
```python
from evennia.contrib.base_systems.components import Component


class Health(Component):
    name = "health"

    
class ItemHealth(Health):
    name = "item_health"
    slot = "health"
```

元件可以在類別層級定義 DBFields 或 NDBFields。
DBField 將使用字首鍵將其值儲存在主機的 DB 中。
NDBField 會將其值儲存在主機的 NDB 中並且不會保留。
使用的金鑰將為“component_name::field_name”。
他們在幕後使用AttributeProperty。

例子：
```python
from evennia.contrib.base_systems.components import Component, DBField

class Health(Component):
    health = DBField(default=1)
```

請注意，預設值是可選的，預設為“無”。

將元件新增至主機也會出現類似的名稱tag，其中「元件」作為類別。
名為 health 的元件將顯示為 key="health,category="components"。
這允許您透過使用 tag 搜尋來檢索具有特定元件的物件。

也可以使用 TagField 以相同的方式新增元件 Tags。
TagField 接受預設值，可用於儲存單一或多個tags。
新增元件時會自動新增預設值。
如果刪除元件，則元件 Tags 將從主機中清除。

例子：
```python
from evennia.contrib.base_systems.components import Component, TagField

class Health(Component):
    resistances = TagField()
    vulnerability = TagField(default="fire", enforce_single=True)
```

本例中的「resistances」欄位可以設定多次，並且它將保留新增的tags。
本例中的「漏洞」欄位將用新欄位覆蓋先前的 tag。



每個typeclass使用ComponentHolderMixin可以宣告它的元件
透過 ComponentProperty 在班級中。
這些元件將始終出現在 typeclass 中。
您也可以傳遞 kwargs 來覆寫預設值
範例
```python
from evennia.contrib.base_systems.components import ComponentHolderMixin
class Character(ComponentHolderMixin, DefaultCharacter):
    health = ComponentProperty("health", hp=10, max_hp=50)
```

然後您可以使用character.components.health 來訪問它。
也存在縮寫形式 character.cmp.health。
character.health 也可以訪問，但僅限於 typeclasses
該元件定義在類別上。

或者，您可以在執行時新增這些元件。
您必須透過元件處理程式存取它們。
例子
```python
character = self
vampirism = components.Vampirism.create(character)
character.components.add(vampirism)

...

vampirism = character.components.get("vampirism")

# Alternatively
vampirism = character.cmp.vampirism
```

請記住，必須匯入所有元件才能在清單中可見。
因此，我建議將它們重新組合到一個包中。
然後，您可以匯入該套件的 __init__ 中的所有元件

由於 Evennia import typeclasses 以及 python 匯入的行為
我建議將元件包放在 typeclass 包內。
換句話說，在 typeclass 資料夾中建立一個名為 Components 的資料夾。
然後，在「typeclasses/__init__.py」檔案內將匯入新增至資料夾中，例如
```python
from typeclasses import components
```
這樣可以確保匯入typeclasses時元件包也會被匯入。
您還需要匯入包自己的“typeclasses/components/__init__.py”檔案中的每個元件。
您只需要從那裡匯入每個模組/檔案，但匯入正確的類別是一個很好的做法。
```python
from typeclasses.components.health import Health
```
```python
from typeclasses.components import health
```
上面的兩個例子都可以工作。

(known-issues)=
## 已知問題

將可變預設值（例如列表）分配給 DBField 將在例項之間共用它。
為了避免這種情況，您必須在欄位上設定 autocreate=True，如下所示。
```python
health = DBField(default=[], autocreate=True)
```

(full-example)=
## 完整範例
```python
from evennia.contrib.base_systems import components


# This is the Component class
class Health(components.Component):
    name = "health"

    # Stores the current and max values as Attributes on the host, defaulting to 100
    current = components.DBField(default=100)
    max = components.DBField(default=100)

    def damage(self, value):
        if self.current <= 0:
            return

        self.current -= value
        if self.current > 0:
            return

        self.current = 0
        self.on_death()

    def heal(self, value):
        hp = self.current
        hp += value
        if hp >= self.max_hp:
            hp = self.max_hp

        self.current = hp

    @property
    def is_dead(self):
        return self.current <= 0

    def on_death(self):
        # Behavior is defined on the typeclass
        self.host.on_death()


# This is how the Character inherits the mixin and registers the component 'health'
class Character(ComponentHolderMixin, DefaultCharacter):
    health = ComponentProperty("health")


# This is an example of a command that checks for the component
class Attack(Command):
    key = "attack"
    aliases = ('melee', 'hit')

    def at_pre_cmd(self):
        caller = self.caller
        targets = self.caller.search(args, quiet=True)
        valid_target = None
        for target in targets:
            # Attempt to retrieve the component, None is obtained if it does not exist.
            if target.components.health:
                valid_target = target

        if not valid_target:
            caller.msg("You can't attack that!")
            return True
```


----

<small>此檔案頁面是從`evennia\contrib\base_systems\components\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
