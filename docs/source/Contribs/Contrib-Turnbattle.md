(turn-based-battle-system-framework)=
# 回合製戰鬥系統框架

蒂姆·阿什利·詹金斯 (Tim Ashley Jenkins) 貢獻，2017 年

這是一個簡單的回合製戰鬥系統的框架，類似
用於 D&D 風格的桌上角色扮演遊戲中的那些。它允許
任何角色在房間內發動戰鬥，此時主動
捲動並建立回合順序。每一個參與戰鬥的人
決定該回合行動的時間有限（30 秒
預設），戰鬥按照回合順序進行，迴圈
參與者直到戰鬥結束。

該資料夾包含多個範例，說明如何建置這樣的系統
實施與客製化：

    tb_basic.py - The simplest system, which implements initiative and turn
            order, attack rolls against defense values, and damage to hit
            points. Only very basic game mechanics are included.

    tb_equip.py - Adds weapons and armor to the basic implementation of
            the battle system, including commands for wielding weapons and
            donning armor, and modifiers to accuracy and damage based on
            currently used equipment.

    tb_items.py - Adds usable items and conditions/status effects, and gives
        a lot of examples for each. Items can perform nearly any sort of
        function, including healing, adding or curing conditions, or
        being used to attack. Conditions affect a fighter's attributes
        and options in combat and persist outside of fights, counting
        down per turn in combat and in real time outside combat.

    tb_magic.py - Adds a spellcasting system, allowing characters to cast
        spells with a variety of effects by spending MP. Spells are
        linked to functions, and as such can perform any sort of action
        the developer can imagine - spells for attacking, healing and
        conjuring objects are included as examples.

    tb_range.py - Adds a system for abstract positioning and movement, which
            tracks the distance between different characters and objects in
            combat, as well as differentiates between melee and ranged
            attacks.

該系統旨在作為一個基本框架，並對其進行建模
遵循流行的桌上角色扮演遊戲的戰鬥系統而不是
許多MMOs和一些MUDs使用的即時戰鬥系統。因此，它
可能更適合角色扮演或更注重故事的遊戲，或者遊戲
旨在密切模擬玩桌上遊戲的體驗RPG。

每個模組都包含戰鬥系統的全部功能
新增了不同的自訂專案 - 安裝每個專案的說明
一個包含在模組本身中。建議您安裝
並且先測試`tb_basic`，這樣你就可以更瞭解其他
模組對其進行擴充套件，並更好地瞭解如何自訂
根據您的喜好自訂系統並將此處介紹的子系統整合到
你自己的戰鬥系統。


----

<small>此檔案頁面是從`evennia\contrib\game_systems\turnbattle\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
