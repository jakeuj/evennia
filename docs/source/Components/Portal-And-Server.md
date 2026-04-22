(portal-and-server)=
# Portal 和伺服器

```
Internet│  ┌──────────┐ ┌─┐           ┌─┐ ┌─────────┐
        │  │Portal    │ │S│   ┌───┐   │S│ │Server   │
    P   │  │          │ │e│   │AMP│   │e│ │         │
    l ──┼──┤ Telnet   ├─┤s├───┤   ├───┤s├─┤         │
    a   │  │ Webclient│ │s│   │   │   │s│ │ Game    │
    y ──┼──┤ SSH      ├─┤i├───┤   ├───┤i├─┤ Database│
    e   │  │ ...      │ │o│   │   │   │o│ │         │
    r ──┼──┤          ├─┤n├───┤   ├───┤n├─┤         │
    s   │  │          │ │s│   └───┘   │s│ │         │
        │  └──────────┘ └─┘           └─┘ └─────────┘
        │Evennia
```

_Portal_和_Server_構成Evennia的兩個主要部分。

這是兩個獨立的 `twistd` 程式，可以從遊戲內部或從指令列進行控制，如 [Running-Evennia 檔案](../Setup/Running-Evennia.md) 中所述。

- Portal 瞭解有關網際網路協定（telnet、websockets 等）的一切，但對遊戲知之甚少。
- 伺服器瞭解遊戲的一切。它知道玩家已連線，但現在知道他們_如何_連線。

這樣做的效果是您可以完全`reload`伺服器並且讓玩家仍然連線到遊戲。一旦伺服器恢復，它將重新連線到 Portal 並重新同步所有玩家，就像什麼都沒發生一樣。

Portal 和伺服器旨在始終在同一臺電腦上執行。它們透過AMP（非同步訊息協定）連線黏合在一起。這使得兩個程式能夠無縫通訊。