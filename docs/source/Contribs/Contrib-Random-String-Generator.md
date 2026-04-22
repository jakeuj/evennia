(pseudo-random-generator-and-registry)=
# 偽隨機產生器和登錄檔

Vincent Le Goff (vlgeoff) 的貢獻，2017 年

此實用程式可用於產生偽隨機資訊字串
具有特定的標準。  例如，您可以使用它來生成
電話號碼、車牌號碼、驗證碼、遊戲內安全
密碼等。產生的字串將被儲存並且不會重複。

(usage-example)=
## 使用範例

這是一個非常簡單的例子：

```python

from evennia.contrib.utils.random_string_generator import RandomStringGenerator

# Create a generator for phone numbers
phone_generator = RandomStringGenerator("phone number", r"555-[0-9]{3}-[0-9]{4}")

# Generate a phone number (555-XXX-XXXX with X as numbers)
number = phone_generator.get()

# `number` will contain something like: "555-981-2207"
# If you call `phone_generator.get`, it won't give the same anymore.phone_generator.all()
# Will return a list of all currently-used phone numbers
phone_generator.remove("555-981-2207")

# The number can be generated again
```

(importing)=
## 輸入

1. 從 contrib 匯入 `RandomStringGenerator` 類別。
2. 建立帶有兩個引數的此類別的例項：
   - 發電機的名稱（如“電話號碼”、“車牌”...）。
   - 表示預期結果的正規表示式。
3. 使用生成器的 `all`、`get` 和 `remove` 方法，如上所示。

若要了解如何讀取和建立正規表示式，可以參考
[re 模組的文件](https://docs.python.org/2/library/re.html)。
您可以使用的一些正規表示式範例：

- `r"555-\d{3}-\d{4}"`：555，一個破折號，3 位數字，另一個破折號，4 位數字。
- `r"[0-9]{3}[A-Z][0-9]{3}"`：3位數字，一個大寫字母，3位數字。
- `r"[A-Za-z0-9]{8,15}"`：8 到 15 個字母和數字。
- ...

在幕後，建立了一個script來儲存產生的資訊
對於單一發電機。  `RandomStringGenerator` 對像也會
讀取您提供給它的正規表示式以檢視資訊是什麼
必需（字母、數字、更受限制的類別、簡單字元...）...
更複雜的正規表示式（例如帶有分支）可能不是
可用。


----

<small>此檔案頁面是從`evennia\contrib\utils\random_string_generator\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
