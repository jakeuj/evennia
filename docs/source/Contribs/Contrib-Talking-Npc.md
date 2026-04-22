(talkative-npc-example)=
# 多嘴NPC示例

Griatch 2011 年貢獻。由 grungies1138 更新，2016 年

這是一個靜態 NPC 物件的範例，能夠容納簡單的選單驅動
談話。例如適合作為任務提供者或商人。

(installation)=
## 安裝

透過建立 typeclass `contrib.tutorials.talking_npc.TalkingNPC` 的物件來建立 NPC，
例如：

    create/drop John : contrib.tutorials.talking_npc.TalkingNPC

在與 NPC 相同的房間中使用 `talk` 開始對話。

如果同一個房間裡有很多說話的NPC，你可以選擇哪一個
一個人的通話指令（Evennia 自動處理此問題）。

EvMenu的這種用法非常簡單；請參閱 EvMenu 以瞭解更複雜的情況
的可能性。


----

<small>此檔案頁面是從`evennia\contrib\tutorials\talking_npc\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
