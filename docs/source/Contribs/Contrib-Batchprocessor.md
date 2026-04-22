(batch-processor-examples)=
# 批處理器範例

格里奇的貢獻，2012

批處理器的簡單範例。批處理器用於生成
來自一個或多個靜態檔案的遊戲內容。檔案可以與版本一起儲存
控制然後“應用”到遊戲中以建立內容。

有兩種批處理器型別：

- Batch-cmd 處理器：正在執行的 `#` 分隔的 Evennia 指令列表
依序，例如 `create`、`dig`、`north` 等。執行 script 時
  這種型別（檔案名稱以`.ev`結尾），script的呼叫者將是
  執行 script 操作的人。
- 批次程式碼處理器：一個完整的 Python script（檔案名稱以 `.py` 結尾，
執行 Evennia api 呼叫來構建，例如 `evennia.create_object` 或
  `evennia.search_object`等，可分為註釋分隔
  區塊，因此一次只能執行 script 的一部分（這樣就可以了
  與普通 Python 檔案略有不同）。

(usage)=
## 用法

要測試兩個範例批次檔案，您需要 `Developer` 或 `superuser`
許可權，登入遊戲並執行

    > batchcommand/interactive tutorials.batchprocessor.example_batch_cmds
    > batchcode/interactive tutorials.batchprocessor.example_batch_code

`/interactive` 會讓您進入互動模式，這樣您就可以按照操作進行操作
scripts 這樣做。跳過它來一次性構建它。

兩個指令產生相同的結果 - 它們建立一個紅色按鈕物件，
一張桌子和一張椅子。如果您使用 `/debug` 開關執行，物件將
之後刪除（用於快速測試您不想傳送垃圾郵件的語法）
例如，物件）。


----

<small>此檔案頁面是從`evennia\contrib\tutorials\batchprocessor\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
