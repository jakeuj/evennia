(internationalization)=
# 國際化

*國際化*（通常縮寫為 *i18n* 因為有 18 個字元
在該單字中的第一個“i”和最後一個“n”之間）允許 Evennia 的核心
伺服器傳回英語以外的其他語言的文字 - 無需任何人
編輯原始碼。

語言翻譯是由志願者完成的，因此支援可能會有很大差異
取決於給定語言的上次更新時間。以下是所有語言
（除了英語）有一定程度的支援。一般來說，任何語言都不能
2022 年 9 月後更新將缺少一些翻譯。

```{eval-rst}

+---------------+----------------------+--------------+
| Language Code | Language             | Last updated |
+===============+======================+==============+
| de            | German               | Aug 2024     |
+---------------+----------------------+--------------+
| es            | Spanish              | Aug 2019     |
+---------------+----------------------+--------------+
| fr            | French               | Dec 2022     |
+---------------+----------------------+--------------+
| it            | Italian              | Oct 2022     |
+---------------+----------------------+--------------+
| ko            | Korean (simplified)  | Sep 2019     |
+---------------+----------------------+--------------+
| la            | Latin                | Feb 2021     |
+---------------+----------------------+--------------+
| pl            | Polish               | Apr 2024     |
+---------------+----------------------+--------------+
| pt            | Portugese            | Oct 2022     |
+---------------+----------------------+--------------+
| ru            | Russian              | Apr 2020     |
+---------------+----------------------+--------------+
| sv            | Swedish              | Sep 2022     |
+---------------+----------------------+--------------+
| zh            | Chinese (simplified) | Oct 2024     |
+---------------+----------------------+--------------+
```

語言翻譯可在 [evennia/locale](github:evennia/locale/) 中找到
資料夾。如果您想協助改進現有的翻譯，請閱讀以下內容
貢獻一份新的。

(changing-server-language)=
## 更改伺服器語言

透過將以下內容新增至您的 `mygame/server/conf/settings.py` 來變更語言
檔案：

```python
    USE_I18N = True
    LANGUAGE_CODE = 'en'

```

這裡的`'en'`（預設英文）應該改為一的縮寫
在 `locale/`（以及上面的列表中）找到的支援語言。重新啟動
伺服器啟動 i18n。

```{important}

即使對於“完全翻譯”的語言，您仍然會看到英文文字
當你開始Evennia時，很多地方。這是因為我們期望您（
開發人員）瞭解英語（畢竟您正在閱讀本手冊）。所以我們
翻譯*最終玩家可能看到的硬編碼字串* - 您的東西
無法輕鬆地從您的 mygame/ 資料夾進行更改。指令的輸出和
Typeclasses 通常*未*翻譯，控制檯/日誌輸出也未翻譯。

為了減少工作量，您可以考慮僅翻譯面向玩家的指令（檢視、獲取等），並將預設管理指令保留為英文。要更改某些指令的語言（例如 `look`），您需要覆蓋 Typeclasses 上的相關掛鉤方法（檢視預設指令的程式碼以瞭解它呼叫的內容）。
```

```{sidebar} Windows使用者

如果您在 Windows 上收到有關 `gettext` 或 `xgettext` 的錯誤，
請參閱[Django 檔案](https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#gettext-on-windows)。
適用於 Windows（32/64 位元）的 gettext 的自動安裝最新版本是
在 Github 上可用 [gettext-iconv-windows](https://github.com/mlocati/gettext-iconv-windows)。

```

(translating-evennia)=
## 翻譯Evennia

翻譯可在核心 `evennia/` 庫中找到，位於
`evennia/evennia/locale/`。您必須確保已克隆此儲存庫
從 [Evennia 的 github](github:evennia) 開始，然後才能繼續。

如果您在 `evennia/evennia/locale/` 中找不到您的語言，那是因為沒有人
已經翻譯了。  或者，您可能有該語言，但找不到
翻譯不好...歡迎您幫忙改善這個情況！

要開始新翻譯，您需要先克隆 Evennia 儲存庫
使用 GIT 並啟動了 python virtualenv，如上所述
[安裝快速入門](../Setup/Installation.md) 頁面。

前往 `evennia/evennia/` - 也就是說，不是您的遊戲目錄，而是在 `evennia/` 內
回購本身。如果您看到 `locale/` 資料夾，那麼您來對地方了。  製造
確保您的 `virtualenv` 處於活動狀態，以便 `evennia` 指令可用。然後執行

     evennia makemessages --locale <language-code>

其中 `<language-code>` 是[兩個字母的區域設定程式碼](http://www.science.co.il/Language/Codes.asp)
您要翻譯的語言，例如瑞典語的“sv”或瑞典語的“es”
西班牙語。過了一會兒，它會告訴您語言已被處理。  為了
例項：

     evennia makemessages --locale sv

如果您開始使用新語言，則會出現該語言的新資料夾
在`locale/`資料夾中。否則系統只會更新
現有翻譯以及最終在伺服器中找到的新字串。執行這個
指令不會覆蓋任何現有字串，因此您可以盡可能多地執行它
想要。

接下來前往 `locale/<language-code>/LC_MESSAGES` 並編輯您的 `**.po` 檔案
在那裡找到。您可以使用普通的文字編輯器對其進行編輯，但如果
您使用網路上的特殊 po 檔案編輯器（在網路上搜尋“po editor”
對於許多免費的替代品），例如：

- [g翻譯](https://wiki.gnome.org/Apps/Gtranslator)
- [編輯](https://poeditor.com/)

翻譯的概念很簡單，就是取英文的問題
您在 `django.po` 檔案中找到的字串並新增您的語言的最佳翻譯
你可以。完成後，執行

    evennia compilemessages

這將編譯所有語言。檢查您的語言並檢查您的
`.po` 檔案，以防程式更新它 - 您可能需要填寫一些缺少的內容
標頭欄位，通常應註明翻譯者是誰。

完成後，請確保每個人都能從您的翻譯中受益！
使用更新的 `django.po` 檔案針對 Evennia 建立 PR。不太理想（如果 git 是
不是你的事）你也可以將其附加到我們論壇的新帖子中。

(hints-on-translation)=
### 翻譯提示

許多翻譯字串使用 `{... }` 佔位符。這是因為他們
將在 `.format()` python 操作中使用。雖然您可以更改
如果這些內容在您的語言中更有意義，則_順序_，您一定_不_
翻譯這些格式的變數 tags - Python 將尋找它們！

    Original: "|G{key} connected|n"
    Swedish:  "|G{key} anslöt|n"

您還必須在訊息的_開頭和結尾_保留換行符（如果有）
（如果你不這樣做，你的po編輯應該阻止你）。嘗試也以相同的方式結束
句子分隔符號（如果這對您的語言有意義）。

    Original: "\n(Unsuccessfull tried '{path}')."
    Swedish: "\nMisslyckades med att nå '{path}')."

最後，試著感受一下字串的用途。如果有特殊的技術術語
使用它可能會更令人困惑，而不是翻譯它，即使它是
`{...}` tag 之外。英語和您的語言混合可能會更清晰
比你強行對每個人通常讀到的術語進行一些臨時翻譯
反正是英語。

    Original: "\nError loading cmdset: No cmdset class '{classname}' in '{path}'.
               \n(Traceback was logged {timestamp})"
    Swedish:  "Fel medan cmdset laddades: Ingen cmdset-klass med namn '{classname}' i {path}.
               \n(Traceback loggades {timestamp})"

(marking-strings-in-code-for-translation)=
## 在程式碼中標記字串以進行翻譯

如果修改 Python 模組程式碼，則可以透過將字串傳遞給 `gettext()` 方法來標記要翻譯的字串。在 Evennia 中，為了方便起見，通常會將其匯入為 `_()`：

```python
from django.utils.translation import gettext as _
string = _("Text to translate")
```

(formatting-considerations)=
### 格式化注意事項

使用格式化字串時，請確保先將「原始」字串傳遞給 `gettext` 進行翻譯，然後格式化輸出。否則，佔位符將在翻譯之前被替換，從而阻止在 `.po` 檔案中找到正確的字串。也建議使用命名佔位符（e.g.、`{char}`）而不是位置佔位符（e.g.、`{}`），以獲得更好的可讀性和可維護性。

```python
# incorrect:
string2 = _("Hello {char}!".format(char=caller.name))

# correct:
string2 = _("Hello {char}!").format(char=caller.name)
```

這也是 f 字串不能與 `gettext` 一起使用的原因：

```python
# will not work
string = _(f"Hello {char}!")
```
