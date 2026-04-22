# Evennia 簡介

> *MUD（原意為 Multi-User Dungeon，後來也延伸出 Multi-User Dimension、Multi-User Domain 等說法）是一種主要以文字描述的多人即時虛擬世界。MUD 結合了角色扮演、砍殺、玩家對戰、互動小說與線上聊天等元素。玩家可以閱讀或查看房間、物件、其他玩家、非玩家角色，以及虛擬世界中發生的動作描述。玩家通常透過輸入近似自然語言的指令來與彼此和世界互動。* - [Wikipedia](https://en.wikipedia.org/wiki/MUD)

如果你正在讀這頁，那很可能代表你也夢想過打造並營運一款屬於自己的文字式大型多人遊戲，也就是 [MUD/MUX/MUSH](https://tinyurl.com/c5sc4bm) 之類的世界。也許你才剛開始動念，也許那個*完美*的遊戲已經在你腦中盤旋很多年了……你非常清楚它能有多精彩，只差還沒把它真正做出來。

我們懂那種感覺。也正因如此，Evennia 才會誕生。

## Evennia 是什麼？

Evennia 是一個用來打造 MU\* 的 framework：它提供一套精簡的 Python 程式碼基礎與伺服器，設計目標是讓你能高度延伸成各種風格的遊戲。

### Bare-bones？

Evennia 所謂的「bare-bones」，意思是它盡量少替你預設任何特定遊戲內容。我們不替你規定戰鬥規則、怪物 AI、種族、技能、職業，或其他世界觀元素。

因為我們認為，你多半會想親手把它們做成自己真正想要的樣子。

### Framework？

Evennia 雖然精簡，但也沒有精簡到什麼都不給。它仍然提供物件、角色、房間、內建頻道等基本積木，也附帶不少對建造與管理很實用的指令。

開箱之後，你會得到一個「Talker」類型的遊戲：它是空的，但已經是一個完整可運作的社交型遊戲，你可以在裡面建房間、四處走動、聊天與 roleplay。Evennia 會幫你處理所有線上遊戲都少不了、卻又常常很無聊的資料庫、網路與幕後管理工作。它就像一張空白畫布，等你把自己的遊戲畫上去。

我們也持續提供一系列可選用的 [contribs](Contribs/Contribs-Overview.md)。這些內容會更偏向特定遊戲用途，能拿來當靈感來源，也能作為你的起點。

### Server？

Evennia 本身就內建 webserver。當你啟動 Evennia 時，你的伺服器同時會提供遊戲網站與瀏覽器 webclient。這讓玩家既能用瀏覽器遊玩，也能用傳統 MUD client 連線。在你準備好把遊戲公開給全世界之前，這些都不會直接暴露在網際網路上。

### Python？

[Python](https://en.wikipedia.org/wiki/Python_(programming_language)) 不只是現今最流行的程式語言之一，也普遍被認為是最容易上手的語言之一。在 Evennia 社群裡，有很多人就是透過做遊戲才學會 Python 或學會寫程式；甚至有人因為在 Evennia 上累積的能力而找到工作。

你在遊戲裡寫的所有東西，從物件定義、自訂指令，到 AI script 與經濟系統，全部都是用標準 Python module 完成，而不是某種臨時拼湊的腳本語言。

## 我可以先在哪裡試試看？

Evennia 的展示伺服器位於 [https://demo.evennia.com](https://demo.evennia.com)。如果你使用傳統 MUD client，也可以連到 `demo.evennia.com` 的 `4000` port。

安裝 Evennia 之後，你也可以用一個指令建立一個教學用 mini-game。更多說明請看 [這裡](Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Tutorial-World.md)。

## 想使用 Evennia，我需要會什麼？

當你[安裝好 Evennia](Setup/Installation.md) 並成功連線後，接下來就該決定你想怎麼使用它。

### 我不會寫程式，或者不想寫，我只想把遊戲跑起來！

Evennia 內建一套預設指令，專門照顧 Python 新手，以及那些想*立刻*把遊戲跑起來的人。

原生 Evennia 足以支撐一個簡單的「Talker」型遊戲：你可以建造與描述房間、建立基本物件、開聊天頻道、做 emote，還有各種適合社交型或自由型 MU\* 的功能。

但戰鬥、怪物與其他遊戲性系統並沒有預設內建，所以如果你完全不打算寫哪怕*一點點*程式，最後做出來的遊戲會非常基礎。

### 我懂一點 Python，或者願意學

先從小地方開始。Evennia 的 [Beginner Tutorial](Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.md) 就是一個很好的起點。

```{sidebar}
也可以順便看看我們的[連結頁](./Links.md)，裡面整理了一些值得延伸閱讀的資源。
```

雖然 Python 被認為是很容易入門的程式語言，但如果你以前沒寫過程式，還是會有一段學習曲線要爬。新手教學裡已經包含一份 [Python 基礎介紹](Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Python-basic-introduction.md)，但如果你完全是新手，還是很建議你另外找一套完整的 Python 入門教材坐下來好好學。網路上其實有很多。

想用 Evennia 寫出你夢想中的遊戲，你不需要是 Python 大師，但至少要能讀懂包含以下基礎概念的範例程式：

- 匯入並使用 Python [modules](https://docs.python.org/3.11/tutorial/modules.html)
- 使用 [variables](https://www.tutorialspoint.com/python/python_variable_types.htm)、[conditional statements](https://docs.python.org/tutorial/controlflow.html#if-statements)、[loops](https://docs.python.org/tutorial/controlflow.html#for-statements) 與 [functions](https://docs.python.org/tutorial/controlflow.html#defining-functions)
- 使用 [lists、dictionaries 與 list comprehensions](https://docs.python.org/tutorial/datastructures.html)
- 進行 [string handling 與 formatting](https://docs.python.org/tutorial/introduction.html#strings)
- 對 [object-oriented programming](https://www.tutorialspoint.com/python/python_classes_objects.htm) 有基本理解，知道怎麼使用 [Classes](https://docs.python.org/tutorial/classes.html)、它們的方法與屬性

你越熟悉這些東西，往後摸索起來自然就越輕鬆。

只要具備這些基礎，你就已經可以從擴充 Evennia 的範例開始，逐步把自己的遊戲做出來。

### 我很熟 Python，而且願意好好用上它！

就算你一開始是 Python 新手，只要持續做一陣子遊戲，多半也會走到這一步。

當你對 Python 的一般能力更成熟後，Evennia 的完整威力就會真正打開。除了修改指令、物件與 script 之外，你還能開發從進階怪物 AI、經濟系統，到複雜戰鬥、社交 mini-game，甚至重寫指令、玩家、房間或頻道本身的運作方式。由於你的遊戲就是透過匯入一般 Python module 來撰寫，可做的事情幾乎沒有太多硬限制。

如果你*剛好*還懂一些 web 開發（HTML、CSS、Javascript），那 Evennia 的網站與 MUD web client 也有很多可以發揮的空間。

## 接下來往哪裡走？

如果你想先從高層次理解 Evennia，可以先看看 [Evennia 圖解](./Evennia-In-Pictures.md)。

接著很適合直接跳進 [Beginner Tutorial](Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.md)。你可以一課一課照順序走，也可以先挑你覺得有趣的部分閱讀。另外也還有更多 [Tutorials and Howto's](Howtos/Howtos-Overview.md#howtos) 可以參考。

你也可以閱讀主要開發者的 [dev blog](https://www.evennia.com/devblog/index.html)，裡面有許多關於 Evennia 開發與架構的零碎心得與片段。

有時候，直接開口求助會更快。你可以加入我們的 [Discord](https://discord.gg/AJJpcRUhtF) 取得即時協助，也可以到 [Discussion forum](https://github.com/evennia/evennia/discussions) 發一篇自我介紹順便打個招呼。更多如何取得協助與如何協助專案的方式，請看[這裡](./Contributing.md)。

歡迎來到 Evennia！
