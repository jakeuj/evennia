(puzzles-system)=
# 謎題系統

Henddher 2018 年的貢獻

適用於冒險遊戲風格的組合謎題，例如組合水果
和攪拌機來製作冰沙。為物件提供typeclass和指令
可以組合（i.e。一起使用）。與 `crafting` contrib 不同，每個
拼圖是由獨特的物件建構的，而不是使用 tags 並且建構者可以建立
謎題完全來自遊戲內。

`Puzzle` 是玩家必須組合哪些物件（也稱為零件）的配方，以便
自動建立一組新的物件（也稱為結果）。

(installation)=
## 安裝

將`PuzzleSystemCmdSet`新增到所有玩家（e.g。在他們​​的角色typeclass中）。

或（用於快速測試）：

    py self.cmdset.add('evennia.contrib.game_systems.puzzles.PuzzleSystemCmdSet')

(usage)=
## 用法

考慮這個簡單的難題：

    orange, mango, yogurt, blender = fruit smoothie

作為建造者：

    create/drop orange
    create/drop mango
    create/drop yogurt
    create/drop blender
    create/drop fruit smoothie

    puzzle smoothie, orange, mango, yogurt, blender = fruit smoothie
    ...
    Puzzle smoothie(#1234) created successfuly.

    destroy/force orange, mango, yogurt, blender, fruit smoothie

    armpuzzle #1234
    Part orange is spawned at ...
    Part mango is spawned at ...
    ....
    Puzzle smoothie(#1234) has been armed successfully

作為玩家：

    use orange, mango, yogurt, blender
    ...
    Genius, you blended all fruits to create a fruit smoothie!

(details)=
## 細節

謎題是根據現有物體建立的。給定的
物件被內省以建立原型
拼圖部分和結果。這些原型成為
拼圖食譜。 （參見PuzzleRecipe和`puzzle`
指令）。建立配方後，所有部分和結果
可以處置（i.e。銷毀）。

稍後，建造者或 Script 可以裝備拼圖
並在各自的位置產生所有拼圖部分
位置（參見臂謎）。

普通玩家可以收集拼圖部件並組合
他們（請參閱使用指令）。如果玩家已指定
所有碎片，拼圖被視為已解決並且所有
當謎題結果時，它的謎題部分被破壞
產卵在其對應的位置。


----

<small>此檔案頁面是從`evennia\contrib\game_systems\puzzles\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
