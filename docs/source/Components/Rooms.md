
(rooms)=
# 客房

**繼承樹：**
```
┌─────────────┐
│DefaultObject│
└─────▲───────┘
      │
┌─────┴─────┐
│DefaultRoom│
└─────▲─────┘
      │       ┌────────────┐
      │ ┌─────►ObjectParent│
      │ │     └────────────┘
    ┌─┴─┴┐
    │Room│
    └────┘
```

[房間](evennia.objects.objects.DefaultRoom) 是遊戲中的[物件](./Objects.md)，代表所有其他物件的根容器。

從技術上講，房間與任何其他物件的唯一區別是它們沒有自己的 `location`，並且像 `dig` 這樣的預設指令會建立此類物件 - 因此，如果您想使用更多功能擴充套件房間，只需從 `evennia.DefaultRoom` 繼承即可。

若要變更`dig`、`tunnel`和其他預設指令所建立的預設房間，請在設定中變更：

    BASE_ROOM_TYPECLASS = "typeclases.rooms.Room"

`mygame/typeclasses/rooms.py` 中的空類別是一個很好的起點！

雖然預設的 Room 非常簡單，但有幾個 Evennia [contribs](../Contribs/Contribs-Overview.md) 可以自訂和擴充套件具有更多功能的 Room。