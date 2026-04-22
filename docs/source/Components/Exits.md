(exits)=
# 退出

**繼承樹：**
```
┌─────────────┐
│DefaultObject│
└─────▲───────┘
      │
┌─────┴─────┐
│DefaultExit│
└─────▲─────┘
      │       ┌────────────┐
      │ ┌─────►ObjectParent│
      │ │     └────────────┘
    ┌─┴─┴┐
    │Exit│
    └────┘
```

*出口*是遊戲中的[物件](./Objects.md)，將其他物件（通常是[房間](./Rooms.md)）連線在一起。

> 請注意，出口是單向物件，因此為了使兩個房間雙向連結，需要有兩個出口。

名為 `north` 或 `in` 的物件可能是出口，以及 `door`、`portal` 或 `jump out the window`。

出口有兩個東西將它們與其他物件分開。
1. 它們的 `.destination` 屬性已設定並指向有效的目標位置。這一事實使得在資料庫中定位出口變得容易和快速。
2. 出口在建立時為其自身定義了一個特殊的[傳輸指令](./Commands.md)。該指令的名稱與出口物件相同，並且在呼叫時將處理將角色移動到出口的 `.destination` 的實用性 - 這允許您只需輸入出口的名稱即可四處移動，正如您所期望的那樣。

預設退出功能均在 [DefaultExit](DefaultExit) typeclass 上定義。原則上你可以透過覆蓋這個來完全改變退出在你的遊戲中的工作方式 - 但不建議這樣做，除非你真的知道你在做什麼）。

使用稱為*遍歷*的`access_type`[鎖定](./Locks.md)退出，並且還使用一些鉤子方法在遍歷失敗時提供回饋。  有關詳細資訊，請參閱 `evennia.DefaultExit`。

出口通常會根據具體情況進行覆蓋，但如果您想更改 `dig`、`tunnel` 或 `open` 等房間建立的預設出口，您可以在設定中更改它：

    BASE_EXIT_TYPECLASS = "typeclasses.exits.Exit"

在`mygame/typeclasses/exits.py`中有一個空的`Exit`類供您修改。

(exit-details)=
### 退出詳情

遍歷出口的過程如下：

1. 遍歷 `obj` 傳送與 Exit 物件上的 Exit-command 名稱相符的指令。 [cmdhandler](./Commands.md) 偵測到這一點並觸發在 Exit 上定義的指令。遍歷始終涉及「來源」（目前位置）和 `destination`（儲存在 Exit 物件上）。
1. Exit 指令檢查 Exit 物件上的 `traverse` lock
1. Exit 指令在 Exit 物件上觸發 `at_traverse(obj, destination)`。
1. 在`at_traverse`中，`object.move_to(destination)`被觸發。這將按順序觸發以下鉤子：
    1. `obj.at_pre_move(destination)` - 如果傳回 False，移動將中止。
    1. `origin.at_pre_leave(obj, destination)`
    1. `obj.announce_move_from(destination)`
    1. 透過將 `obj.location` 從來源位置變更為 `destination` 來執行移動。
    1. `obj.announce_move_to(source)`
    1. `destination.at_object_receive(obj, source)`
    1. `obj.at_post_move(source)`
1. 在 Exit 物件上，`at_post_traverse(obj, source)` 被觸發。

如果移動因某種原因失敗，退出將在其自身上查詢 Attribute `err_traverse` 並將其顯示為錯誤訊息。如果沒有找到，Exit 將自行呼叫 `at_failed_traverse(obj)`。

(creating-exits-in-code)=
### 在程式碼中建立退出

有關如何以程式設計方式建立退出的範例，請參閱[本指南](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Creating-Things.md#linking-exits-and-rooms-in-code)。
