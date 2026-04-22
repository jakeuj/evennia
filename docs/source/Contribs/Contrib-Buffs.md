(buffs)=
# 增益

Tegiminis 2022 年的貢獻

buff 是一個定時物件，附加到遊戲實體。它能夠修改值、觸發程式碼或兩者兼而有之。 
這是RPGs中常見的設計模式，尤其是動作遊戲。

特徵：

- `BuffHandler`：應用於物件的 buff 處理程式。
- `BaseBuff`：一個 buff 類，可以擴充套件它來建立你自己的 buff。
- `BuffableProperty`：範例屬性類，展示如何自動檢查修飾符。
- `CmdBuff`：應用增益的指令。
- `samplebuffs.py`：一些可供學習的範例 buff。

(quick-start)=
## 快速入門
將處理程式指派給物件的屬性，如下所示。

```python
@lazy_property
def buffs(self) -> BuffHandler:
    return BuffHandler(self)
```

然後，您可以呼叫處理程式來新增或操作 buff，如下所示：`object.buffs`。請參閱**使用處理程式**。

(customization)=
### 客製化

如果您想自訂處理程式，可以為建構函式提供兩個引數：
- `dbkey`：您希望用作 buff 資料庫的 attribute 鍵的字串。預設為“buff”。這允許您保留單獨的增益池 - 例如，“增益”和“特權”。
- `autopause`：如果您希望此處理程式在其所屬物件解除操縱時自動暫停遊戲時間增益。

> **注意**：如果啟用自動暫停，則 MUST 會在您擁有的物件的
> `at_init` 鉤子。否則，熱過載可能會導致遊戲時間增益無法正確更新
> 在木偶/解除木偶上。您已被警告！

假設您想要一個物件 `perks` 的另一個處理程式，它有一個單獨的資料庫並且
尊重遊戲愛好者。您可以這樣指派這個新屬性：

```python
class BuffableObject(Object):
    @lazy_property
    def perks(self) -> BuffHandler:
        return BuffHandler(self, dbkey='perks', autopause=True)

    def at_init(self):
        self.perks
```

(using-the-handler)=
## 使用處理程式

以下是如何使用新的處理程式。

(apply-a-buff)=
### 應用增益

呼叫處理程式的 `add` 方法。這需要一個類別引用，也包含一些
用於自訂 buff 持續時間、堆疊等的可選引數。您也可以儲存任意值
透過 `to_cache` 可選引數傳遞字典來儲存在 buff 的快取中。這不會覆蓋正常的
快取上的值。

```python
self.buffs.add(StrengthBuff)                            # A single stack of StrengthBuff with normal duration
self.buffs.add(DexBuff, stacks=3, duration=60)          # Three stacks of DexBuff, with a duration of 60 seconds
self.buffs.add(ReflectBuff, to_cache={'reflect': 0.5})  # A single stack of ReflectBuff, with an extra cache value
```

應用 buff 時會檢查 buff 上的兩個重要屬性：`refresh` 和 `unique`。
- `refresh`（預設值：True）決定增益效果的計時器在重新套用時是否會重新整理。
- `unique`（預設值：True）決定此增益是否唯一；也就是說，物件上只存在其中之一。

這兩個布林值的組合會建立三種鍵之一：
- `Unique is True, Refresh is True/False`：buff的預設鍵。
- `Unique is False, Refresh is True`：預設鍵與應用程式的資料庫引用混合。這使得增益效果“對每個玩家都是唯一的”，因此您可以透過重新應用來重新整理。
- `Unique is False, Refresh is False`：預設金鑰與隨機數混合。

(get-buffs)=
### 獲得增益

這個處理程式有幾個傳回例項化 buff 的 getter 方法。您不需要將它們用於基本功能，但如果您想操作
應用後的buff非常有用。處理程式的 `check`/`trigger` 方法利用其中一些 getter，而其他 getter 只是為了開發人員的方便。

`get(key)` 是最基本的 getter。它會傳回單一 buff 例項，如果處理程式中不存在 buff，則傳回 `None`。它也是唯一的吸氣劑
傳回單一 buff 例項，而不是字典。

> **注意**：處理程式方法 `has(buff)` 允許您檢查處理程式快取中是否存在匹配的鍵（如果是字串）或 buff 類別（如果是類別），而無需實際例項化 buff。您應該使用此方法來進行基本的“此增益是否存在？”檢查。

下面列出的組 getter 傳回格式為 `{buffkey: instance}` 的值字典。如果你想迭代所有這些增益，
您應該透過 `dict.values()` 方法來執行此操作。

- `get_all()` 傳回此處理程式上的所有增益。您也可以使用 `handler.all` 屬性。
- `get_by_type(BuffClass)` 傳回指定型別的增益。
- `get_by_stat(stat)` 傳回 `mods` 清單中具有指定 `stat` 字串的 `Mod` 物件的 buff。
- `get_by_trigger(string)` 傳回 `triggers` 清單中具有指定字串的增益。
- `get_by_source(Object)` 傳回指定 `source` 物件應用的增益效果。
- `get_by_cachevalue(key, value)` 返回快取中具有匹配 `key: value` 對的增益。 `value` 是可選的。

除 `get_all()` 之外的所有組 getter 都可以透過可選的 `to_filter` 引數「切片」現有字典。

```python
dict1 = handler.get_by_type(Burned)                     # This finds all "Burned" buffs on the handler
dict2 = handler.get_by_source(self, to_filter=dict1)    # This filters dict1 to find buffs with the matching source
```

> **注意**：這些 getter 中的大多數也有關聯的處理程式屬性。例如`handler.effects`回傳所有可以觸發的buff，即
> 然後透過 `get_by_trigger` 方法迭代。

(remove-buffs)=
### 移除增益

去除方法也有很多種。一般來說，它們遵循與 getter 相同的格式。

- `remove(key)` 移除指定鍵的 buff。
- `clear()` 移除所有增益。
- `remove_by_type(BuffClass)` 移除指定型別的增益效果。
- `remove_by_stat(stat)` 刪除 `mods` 清單中指定 `stat` 字串的 `Mod` 物件的增益。
- `remove_by_trigger(string)` 刪除 `triggers` 清單中具有指定字串的增益。
- `remove_by_source(Object)` 移除指定來源應用的增益效果
- `remove_by_cachevalue(key, value)` 刪除快取中匹配的 `key: value` 對的增益。 `value` 是可選的。

您也可以透過呼叫例項的 `remove` 輔助方法來刪除增益。您可以在傳回的字典上執行此操作
上面列出了吸氣劑。

```python
to_remove = handler.get_by_trigger(trigger)     # Finds all buffs with the specified trigger
for buff in to_remove.values():                 # Removes all buffs in the to_remove dictionary via helper methods
    buff.remove()   
```

(check-modifiers)=
### 檢查修飾符

當您想檢視修改後的值時，請呼叫處理程式 `check(value, stat)` 方法。 
這將返回`value`，由處理程式所有者的任何相關增益修改（由
`stat` 字串）。

例如，假設您想要修改所承受的傷害。這可能看起來像這樣：

```python
# The method we call to damage ourselves
def take_damage(self, source, damage):
    _damage = self.buffs.check(damage, 'taken_damage')
    self.db.health -= _damage
```

此方法在過程中的相關點呼叫 `at_pre_check` 和 `at_post_check` 方法。你可以使用這個品牌
對被檢查有反應的增益；例如，移除自身、改變其值或與遊戲狀態互動。

> **注意**：您也可以在檢查相關增益的同時觸發相關增益，方法是確保 `check` 方法中的可選引數 `trigger` 為 True。

修飾符是相加計算的 - 也就是說，所有相同型別的修飾符在應用之前會相加。他們那時
透過以下公式應用。

```python
(base + total_add) / max(1, 1.0 + total_div) * max(0, 1.0 + total_mult)
```

(multiplicative-buffs-advanced)=
#### 倍增增益（進階）

預設情況下，此增益系統中的乘法/除法修改器是相加的。這意味著兩個 +50% 修飾符將等於 +100% 修飾符。但是如果您想乘法應用 mods 該怎麼辦？

首先，您應該仔細考慮是否真的需要乘法修飾符。這裡有一些需要考慮的事情。

- 它們對一般使用者來說並不直觀，因為兩個 +50% 傷害增益等於 +125%，而不是 +100%。
- 它們會導致“力量爆炸”，以正確的方式堆疊增益可以將角色變成不可阻擋的力量

進行純加法乘法器可以讓您更好地控制遊戲的平衡。相反，進行乘法運算可以實現非常有趣的構建工藝，其中明智地使用增益和技能可以將您變成一次性強者。每個都有它的位置。

乘法增益的最佳設計實踐是將乘數分成“層”，其中每個層單獨應用。您可以透過多次 `check` 呼叫輕鬆完成此操作。

```python
damage = damage
damage = handler.check(damage, 'damage')
damage = handler.check(damage, 'empower')
damage = handler.check(damage, 'radiant')
damage = handler.check(damage, 'overpower')
```

(buff-strength-priority-advanced)=
#### 增益強度優先（進階）

有時您只想對統計資料套用最強的修飾符。這是由處理程式的檢查方法中可選的 `strongest` bool arg 支援的

```python
def take_damage(self, source, damage):
    _damage = self.buffs.check(damage, 'taken_damage', strongest=True)
    self.db.health -= _damage
```

(trigger-buffs)=
### 觸發增益

當您想要事件呼叫時，呼叫處理程式的 `trigger(string)` 方法。這將在所有具有相關觸發器 `string` 的 buff 上呼叫 `at_trigger` 鉤子方法。

例如，假設您想在攻擊擊中目標時觸發「引爆」增益。
你會寫一個可能看起來像這樣的 buff：

```python
class Detonate(BaseBuff):
    ...
    triggers = ['take_damage']
    def at_trigger(self, trigger, *args, **kwargs)
        self.owner.take_damage(100)
        self.remove()
```

然後在你用來承受傷害的方法中呼叫`handler.trigger('take_damage')`。

> **注意** 如果您願意，您也可以透過 mods 和 `at_post_check` 來完成此操作，具體取決於要如何新增傷害。

(ticking)=
### 滴答作響

滴答聲增益有點特別。它們與觸發增益類似，因為它們執行程式碼，但不是
在事件觸發器上這樣做，他們在週期性的滴答聲上這樣做。像這樣的增益效果的常見用例是毒藥，
或隨著時間的推移而痊癒。

```python
class Poison(BaseBuff):
    ...
    tickrate = 5
    def at_tick(self, initial=True, *args, **kwargs):
        _dmg = self.dmg * self.stacks
        if not initial:
            self.owner.location.msg_contents(
                "Poison courses through {actor}'s body, dealing {damage} damage.".format(
                    actor=self.owner.named, damage=_dmg
                )
            )
```

要使 buff 生效，請確保 `tickrate` 為 1 或更高，並且其 `at_tick` 中有程式碼
方法。將其新增到處理程式後，它就會開始滴答作響！

> **注意**：當 `initial` 為 `True` 時，勾選增益總是在初始應用時勾選。如果你不想讓你的鉤子在那時觸發
> 確保檢查 `at_tick` 方法中 `initial` 的值。

(context)=
### 情境

每個重要的處理程式方法都可以選擇接受 `context` 字典。

上下文對於這個處理程式來說是一個重要的概念。每個檢查、觸發或勾選 buff 的方法都會透過此方法
字典（預設值：空）作為關鍵字引數傳遞給 buff hook 方法（`**kwargs`）。它不用於其他用途。這可以讓你做那些
方法透過將相關資料儲存在您提供給方法的字典中來「事件感知」。

例如，假設您想要一個“荊棘”增益來傷害攻擊您的敵人。讓我們採用 `take_damage` 方法
並新增上下文。

```python
def take_damage(attacker, damage):
    context = {'attacker': attacker, 'damage': damage}
    _damage = self.buffs.check(damage, 'taken_damage', context=context)
    self.buffs.trigger('taken_damage', context=context)
    self.db.health -= _damage
```
現在我們使用上下文傳遞給 buff kwargs 的值來自訂我們的邏輯。
```python
class ThornsBuff(BaseBuff):
    ...
    triggers = ['taken_damage']
    # This is the hook method on our thorns buff
    def at_trigger(self, trigger, attacker=None, damage=0, **kwargs):
        if not attacker: 
            return
        attacker.db.health -= damage * 0.2
```
應用增益效果，承受傷害，然後觀看荊棘增益效果發揮作用！

(viewing)=
### 觀看

處理程式上有兩種輔助方法，可讓您取得有用的 buff 資訊。

- `view`：傳回格式為`{buffkey: (buff.name, buff.flavor)}`的元組字典。預設會尋找所有增益，但也可以選擇接受增益字典進行篩選。對於基本的增益讀數很有用。
- `view_modifiers(stat)`：傳回影響指定統計資料的修飾符資訊的巢狀字典。第一層是修飾符型別(`add/mult/div`)，第二層是值型別(`total/strongest`)。不傳回導致這些修飾符的增益，僅傳回修飾符本身（類似於使用 `handler.check` 但不實際修改值）。對於統計表很有用。

您還可以透過各種處理程式 getter 建立自己的自訂檢視方法，該方法將始終傳回整個 buff 物件。

(creating-new-buffs)=
## 創造新的增益

建立新的 buff 非常簡單：將 `BaseBuff` 擴充套件到一個新類別，並填寫所有相關的 buff 詳細資料。
然而，有許多單獨的活動部件需要加強。以下是重要內容的逐步介紹。

(basics)=
### 基礎知識

無論任何其他功能為何，所有增益效果都具有以下類別屬性：

- 它們具有可自訂的 `key`、`name` 和 `flavor` 字串。
- 它們有一個`duration`（浮動），並在最後自動清理。使用 -1 表示無限持續時間，使用 0 立即清理。 （預設值：-1）
- 它們有一個`tickrate`（浮點數），如果大於1則自動勾選（預設值：0）
- 如果 `maxstacks` (int) 不等於 1，它們可以疊加。如果為 0，則 buff 會永遠疊加。 （預設值：1）
- 它們可以是 `unique` (bool)，這決定它們是否有唯一的名稱空間。 （預設值：真）
- 它們可以`refresh`（布林值），這會在堆疊或重新應用時重置持續時間。 （預設值：真）
- 它們可以是 `playtime` (bool) buff，其中持續時間僅在活躍遊戲期間倒數。 （預設值：假）

增益還有一些有用的屬性：

- `owner`：此增益效果所附加的物件
- `ticknum`: buff 已經經過多少個刻度
- `timeleft`: buff還剩多少時間
- `ticking`/`stacking`：如果此增益效果勾選/疊加（檢查`tickrate`和`maxstacks`）

(buff-cache-advanced)=
#### 增益快取（進階）

buffs總是在快取中儲存一些關於它們自己的有用的可變資訊（儲存在擁有物件的資料庫attribute上）。 buff的快取對應於`{buffkey: buffcache}`，其中`buffcache`是包含__at least__以下資訊的字典：

- `ref` (class)：我們用來建構buff的buff類路徑。
- `start` (float): 應用增益的時間戳記。
- `source`（物件）：如果指定；這可以讓你追蹤誰或什麼應用了增益效果。
- `prevtick`（浮點數）：前一個刻度的時間戳記。
- `duration`（浮點數）：快取持續時間。這可能與課程持續時間不同，具體取決於持續時間是否已修改（暫停、延長、縮短等）。
- `tickrate` (float): buff 的滴答率。不能低於 0。改變已應用增益的滴答率不會導致它開始滴答（如果之前沒有滴答）。 （`pause` 和 `unpause` 開始/停止現有增益效果）
- `stacks` (int): 他們有多少堆疊。
- `paused` (bool): 暫停的增益不會清理、修改值、勾選或觸發任何鉤子方法。

有時您會希望在執行時動態更新 buff 的快取，例如更改鉤子方法中的滴答率，或更改 buff 的持續時間。 
您可以使用介面 `buff.cachekey` 來執行此操作。只要attribute名稱與快取字典中的某個鍵匹配，就會更新儲存的
快取新值。

如果沒有匹配的金鑰，則不會執行任何操作。如果你想新增一個新的key到快取中，你必須使用`buff.update_cache(dict)`方法，
這將使用提供的字典正確更新快取（包括新增新鍵）。

> **範例**：您想要將 buff 的持續時間增加 30 秒。您使用`buff.duration += 30`。這個新的持續時間現在反映在例項和快取上。

buff快取還可以儲存任意資訊。為此，請透過處理程式 `add` 方法傳遞字典 (`handler.add(BuffClass, to_cache=dict)`)，
在你的buff類上設定`cache`字典attribute，或使用前面提到的`buff.update_cache(dict)`方法。

> **範例**：您將 `damage` 作為值儲存在 buff 快取中，並將其用於毒藥 buff。您希望隨著時間的推移增加它，因此您在tick方法中使用`buff.damage += 1`。

(modifiers)=
### 修飾符

Mod 儲存在 `mods` 清單 attribute 中。含有一個或多個 Mod 物件的增益可以修改統計資料。您可以使用處理程式方法來檢查所有
特定統計字串的 mods 並將其修改應用於該值；但是，建議您在 getter/setter 中使用 `check`，以便於存取。

Mod 物件僅包含四個值，由建構函式依下列順序指派：

- `stat`：您要修改的統計資料。當`check`被呼叫時，這個字串用於尋找所有要收集的mod。
- `mod`：修飾符。預設值為 `add`（加法/減法）、`mult`（乘法）和 `div`（除法）。修飾符是相加計算的（更多資訊請參見 `_calculate_mods`）
- `value`：無論堆疊如何，修飾符都會提供多少價值
- `perstack`：修飾符為每個堆疊授予多少價值，**INCLUDING** 第一個。 （預設值：0）

將 Mod 新增至 buff 的最基本方法是在 buff 類別定義中執行此操作，如下所示：

```python
class DamageBuff(BaseBuff):
    mods = [Mod('damage', 'add', 10)]
```

應用於該值的任何修改都不會以任何方式永久存在。所有計算都在執行時完成，並且 mod 值從不儲存
除了有問題的buff之外的任何地方。換句話說：您不需要追蹤特定統計模型的起源，並且您將
永遠不要永久改變 buff 修改的統計資料。若要刪除修改，只需從物件中刪除 buff 即可。

> **注意**：您可以透過過載 `_calculate_mods` 方法來新增自己的修飾符型別，該方法包含基本的修飾符應用邏輯。

(generating-mods-advanced)=
#### 生成 Mod（高階）

製作 mod 的一種高階方法是在初始化 buff 時產生它們。這使您可以即時建立對遊戲狀態做出反應的模組。

```python
class GeneratedStatBuff(BaseBuff):
    ...
    def at_init(self, *args, **kwargs) -> None:
        # Finds our "modgen" cache value, and generates a mod from it
        modgen = list(self.cache.get("modgen"))
        if modgen:
            self.mods = [Mod(*modgen)]
```

(triggers)=
### 觸發器

`triggers` attribute 中有一個或多個字串的增益可以由事件觸發。

當處理程式的 `trigger` 方法被呼叫時，它會在處理程式上的所有 buff 中搜尋任何具有匹配觸發器的，
然後呼叫它們的 `at_trigger` 鉤子。增益可以有多個觸發器，你可以知道哪個觸發器被使用了
鉤子中的 `trigger` 引數。

```python 
class AmplifyBuff(BaseBuff):
    triggers = ['damage', 'heal'] 

    def at_trigger(self, trigger, **kwargs):
        if trigger == 'damage': print('Damage trigger called!')
        if trigger == 'heal': print('Heal trigger called!')
```

(ticking-1)=
### 滴答作響

滴答的增益效果與觸發的增益效果沒有太大差異。您仍在執行任意掛鉤
增益等級。要勾選，buff 的 `tickrate` 必須為 1 或更高。

```python
class Poison(BaseBuff):
    ...
    # this buff will tick 6 times between application and cleanup.
    duration = 30
    tickrate = 5
    def at_tick(self, initial, **kwargs):
        self.owner.take_damage(10)
```
> **注意**：應用時，增益效果總是會勾選一次。對於**僅第一個刻度**，`initial` 在 `at_tick` 掛鉤方法中將為 True。 `initial` 在後續價格變動中將為 False。

蜱蟲利用持續的延遲，因此它們應該是可醃製的。只要您不為 buff 類別新增屬性，就不必擔心。
如果您**新增**新屬性，請嘗試確保它們不會以指向其物件或處理程式的迴圈程式碼路徑結束，因為這將導致酸洗錯誤。

(extras)=
### 附加功能

Buffs 有一個額外的功能，可以讓您增加設計的複雜性。

(conditionals)=
#### 條件句

您可以透過定義 `conditional` 鉤子來限制 buff 是否為 `check`、`trigger` 或 `tick`。只要
當它傳回一個「真實」值時，增益效果將自行應用。這對於使增益取決於遊戲狀態非常有用 - 對於
例如，如果你想要一個讓玩家在著火時受到更多傷害的增益：

```python
class FireSick(BaseBuff):
    ...
    def conditional(self, *args, **kwargs):
        if self.owner.buffs.has(FireBuff): 
            return True
        return False
```

當對應操作的處理程式方法收集 buff 時，會檢查 `check`/`trigger` 的條件。 `Tick`
每次勾選都會檢查條件。

(helper-methods)=
#### 輔助方法

Buff 例項有許多輔助方法。

- `remove`/`dispel`：允許你移除或消除增益效果。呼叫 `at_remove`/`at_dispel`，視可選引數而定。
- `pause`/`unpause`：暫停和取消暫停增益。呼叫 `at_pause`/`at_unpause`。
- `reset`：將buff的開始時間重設為目前時間；與「重新整理」相同。
- `alter_cache`：使用提供的字典中的`{key:value}`對更新buff的快取。可以覆蓋預設值，所以要小心！

(playtime-duration)=
#### 遊戲時長

如果您的處理程式啟用了`autopause`，則任何具有真實`playtime`值的增益將自動暫停
並在處理程式所附加的物件被操縱或取消操縱時取消暫停。這甚至適用於滴答聲愛好者，
不過，如果剩餘的滴答持續時間少於 1 秒，則會四捨五入為 1 秒。

> **注意**：如果您想更好地控制此過程，您可以註解掉處理程式上的訊號訂閱並移動自動暫停邏輯
> 到你的物件的 `at_pre/post_puppet/unpuppet` 鉤子。

----

<small>此檔案頁面是從`evennia\contrib\rpg\buffs\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
