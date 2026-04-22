(changelog)=
# 變更日誌

(main-branch)=
## 主要分行

- 壯舉：新增 AGENTS.md 和.agents 上下文檔案以幫助 AI 代理開發 (Griatch)
- 壯舉：為想要使用 `uv` 工具的 Evennia 庫開發人員新增 `uv.lock` (Griatch)
- [專長][pull3867]：依據[MUD標準提案][mudstandards-ws]新增WebSocket子協定協商。
支援`json.mudstandards.org`、`gmcp.mudstandards.org`、`terminal.mudstandards.org` 和
  `v1.evennia.com`（evennia自己的webclient）。新的 `WEBSOCKET_SUBPROTOCOLS` 設定。
  現有客戶不受影響。 （戴姆斯）
- [專長][pull3511]：將`article`和`format` kwargs加入`$You()`/`$you()`/`$Your()`/`$your()`。
`$You()` 現在自動將第三人稱接收者的名稱大寫。 （千津津）
- [修正][pull3866]：修正 Evennia 啟動日誌中顯示「無」的問題 (jaborsh)
- [修正][pull3869]：處理非 Windows 系統的 `evennia -l &` (jaborsh)
- 修復：改進東亞語言的縮排/格式（Griatch，靈感來自 hhsiao）
- [修正][pull3875]：修正指令堆疊傳送位元組時 telnet HTTP 檢查中的 TypeError (aMiss-aWry)
- [修正][pull3877]：修正多重配對編號顯示不區分大小寫的問題 (InspectorCaracal)
- [修復][pull3883]：任務處理程式：修復 TaskHandlerTask 陳舊引用並清理 (jaborsh)
- [Feat][pull3884]：正式支援 psycopg3 (jaborsh) PostgreSQL
- [修復][pull3885]：Is_ooc()：執行緒 session 透過 lock 系統以多 session 模式 (jaborsh)
- 修復：為缺少 `session` kwarg (Griatch) 的自訂 cmdparsers 新增棄用警告
- [修復][pull3888]：在第一次查詢之前關閉過時的 DB 連線 (jaborsh)
- [修正][pull3898]：將呼叫者傳遞到 CmdStateCC cc 指令中的 purge_processor (saschabuehrle)
- [修正][pull3899]：修正 @teleport 在搜尋失敗時顯示雙重錯誤訊息 (blongden)
- [修正][pull3900]：當 args 包含非字串值時，修正 MSDP 編碼中的 TypeError (blongden)
- [修復][pull3901]：透過對鍵而不是常數（blongden）進行雜湊指令來修復 O(N²) cmdset 合併
- [修復][pull3905]：修正合併CmdSets (kvmet) 中重複的系統指令
- [修正][pull3909]：修正 funcparser 將 $" 視為格式錯誤的函式呼叫 (aMiss-aWry)
- [修正][pull3910]：修正 MXP 解析以不將周圍文字轉義為 HTML 實體 (aMiss-aWry)
- [修復][pull3504]：郵件contrib現在顯示玩家本地時區的日期/時間（chiizujin）
- [修復][pull3600]：在 evadventure chargen 中不處理盔甲和頭盔/盾牌箱 (jzmiller1)
- [修正][pull3850]：修正 `DefaultObject.copy` (InspectorCaracal) 中克隆編號邏輯的潛在錯誤
- [修正][pull3769]：退出多重符合現在顯示退出的顯示名稱而不是搜尋查詢 (JohniFi)
- [修復][issue3895]：更新過時的批次指令處理器路徑並刪除過時的
遊戲模板佔位符 (Griatch)
- [修正][issue3890]：登入時自動傀儡期間記錄 RuntimeErrors，而不是靜默記錄
吞掉它們（格里奇）
- 修復：MSSP 遊戲名稱現在使用設定。 SERVERNAME 而非硬編碼的「Mygame」預設值（Griatch）
- 檔案：格里奇，BigJMoney

[pull3866]: https://github.com/evennia/evennia/pull/3866
[pull3867]: https://github.com/evennia/evennia/pull/3867
[pull3869]: https://github.com/evennia/evennia/pull/3869
[pull3875]: https://github.com/evennia/evennia/pull/3875
[pull3877]: https://github.com/evennia/evennia/pull/3877
[pull3883]: https://github.com/evennia/evennia/pull/3883
[pull3884]: https://github.com/evennia/evennia/pull/3884
[pull3885]: https://github.com/evennia/evennia/pull/3885
[pull3888]: https://github.com/evennia/evennia/pull/3888
[pull3898]: https://github.com/evennia/evennia/pull/3898
[pull3899]: https://github.com/evennia/evennia/pull/3899
[pull3900]: https://github.com/evennia/evennia/pull/3900
[pull3901]: https://github.com/evennia/evennia/pull/3901
[pull3905]: https://github.com/evennia/evennia/pull/3905
[pull3909]: https://github.com/evennia/evennia/pull/3909
[pull3910]: https://github.com/evennia/evennia/pull/3910
[pull3504]: https://github.com/evennia/evennia/pull/3504
[pull3511]: https://github.com/evennia/evennia/pull/3511
[pull3600]: https://github.com/evennia/evennia/pull/3600
[pull3769]: https://github.com/evennia/evennia/pull/3769
[pull3850]: https://github.com/evennia/evennia/pull/3850
[issue3890]: https://github.com/evennia/evennia/issues/3890
[issue3895]: https://github.com/evennia/evennia/issues/3895
[mudstandards-ws]: https://mudstandards.org/websocket/

(evennia-600)=
## Evennia 6.0.0

2026 年 2 月 15 日

- 功能（向後不相容）：刪除 Python 3.11 支援（支援：Python 3.12、3.13、3.14 (req)）。 （格里奇）
- 安全性：Django >=6.0.2 (<6.1)，Django RestFramework 3.16 (Griatch)
- 更新：`XYZGrid` contrib 現在需要 scipy 1.15->1.17。註：尋路可能會選擇不同的
由於 scipy Dijkstra 演演算法（Griatch）的私人更改，先前的最短路線
- [Feat][pull3599]：使 `at_pre_cmd` 在單元測試中可測試 (blongden)
- [修復]：API /openapi/setattribute 端點皆為 POST 和 PUT，導致架構
錯誤；現在僅更改為 PUT。 （格里奇）
- [Feat][issue2627]：增加 `settings.AUDIT_MASKS` 來自訂 Evennia 應該做什麼
混淆伺服器錯誤日誌（例如來自自訂登入指令的密碼）(Griatch)
- [修復][pull3799]：修正初學者教學中的 `basic_tc.py` contrib 中的拼字錯誤 (Tharic99)
- [修復][pull3806]：退出時EvMore不會將Session傳遞給下一個cmd（gas-public-wooden-clean）
- [修復][pull3809]：管理頁面 - 修復帳戶按鈕連結 (UserlandAlchemist)
- [修正][pull3811]：嘗試登入之前顯示網站登入橫幅 (UserlandAlchemist)
- [修復][pull3817]: `ingame_reports` i18n 修復 (peddn)
- [修復][pull3818]：更新產生掛鉤以使用 `new_prototype` (InspectorCaracal)
- [修復][pull3815]：大型 cmdset 合併中的效能改進 (blongden)
- [修復][pull3831]：ANSIString中的效能最佳化，大彩色的效能提升
字串（無窮大）
- [修復][pull3832]：修復原型中導致使用同質鎖的拼字錯誤
錯誤地回退（無窮大）
- [修復][pull3834]：修復 `$obj(#123)` 行內函數在原型產生中起作用（無限大）
- [修正][pull3836]：正確處理使用 `key=None` 呼叫 `create_object`（無限大）
- [修正][pull3852]：未正確偵測到 Django 5.2+。修復 distutils 問題
在 py3.12 中刪除了新安裝（計數無窮大）
- [修復][pull3845]：修復切片時指數ANSI標記爆炸
重置後ANSIString（加速EvForm其他字串操作，修復相容性）（無限大）
- [修復][pull3853]：使用本機破折號正確處理多重匹配分隔，例如
't-shirt-1'（無窮大）
- [修復][pull3733]: 允許`CmdSetAttribute`使用類別，按鍵檢視字典 (InspectorCaracal)
- [修正][issue3858]：修正骰子 contrib 中的解析問題 (Griatch)
- 修復：`Typeclass.objects.get_by_tag()` 現在總是將 tag 鍵/類別轉換為整數，以
避免與 PostgreSQL 資料庫不一致 (Griatch)
- [修復][issue3813]：修正了 OnDemandHandler 可以追溯的問題
無法pickle的物件並在伺服器關閉時導致錯誤（Griatch）
- [修正][issue3649]：EvEditor 中的 `:j` 指令會壓縮空白行 (Griatch)
- [修復][issue3560]：伺服器重新啟動後無法載入教學QuestHandler (Griatch)
- [修正][issue3601]：`CmdSet.add(..., allow_duplicates=True)` 不允許重複的 cmd 鍵 (Griatch)
- [修復][issue3194]：使 AttributeProperties 上的過濾在 typeclasses 上保持一致 (Griatch)
- [修正][issue2774]：正確支援`evennia connections`長描述中的`\n` (Griatch)
- [修復][issue3312]：處理所有破壞 `monitor/monitored` `input_funcs` 的邊緣情況 (Griatch)
- [修正][issue3154]：持久EvMenu在重新載入時導致多個cmdsets（Griatch）
- [修正][issue3193]：內部巢狀 evtable 的格式會中斷 (Griatch)
- [修復][issue3082]：MXP 連結破壞了 EvTable 格式 (Griatch)
- [修復][issue3693]：在EvTable中使用`|/`破壞了填充（Griatch）
- [修正][pull3864]：正確使用 XYZGrid 的快取 dijkstra 結果 (jaborsh)
- [修復][pull3863]：傳送器搜尋 (jaborsh) 中的 `XYZGrid` 效能改進
- [修復][pull3862]：`TraitHandler` 拼字錯誤/錯誤修復 (jaborsh)
- [檔案][pull3801]：將 Evennia 檔案建置系統移至最新的 Sphinx/myST
（PowershellNinja，亦榮譽提及電畫）
- [Doc][pull3800]：在 HAProxy 檔案中描述對 Telnet SSH 的支援 (holl0wstar)
- [Doc][pull3825]：更新葡萄牙文翻譯 (marado)
- [檔案][pull3826]：修正 README 中損壞的連結 (marado)
- 檔案：marado、Griatch、Hasna878、count-infinity

[pull3799]: https://github.com/evennia/evennia/pull/3799
[pull3800]: https://github.com/evennia/evennia/pull/3800
[pull3801]: https://github.com/evennia/evennia/pull/3801
[pull3806]: https://github.com/evennia/evennia/pull/3806
[pull3809]: https://github.com/evennia/evennia/pull/3809
[pull3811]: https://github.com/evennia/evennia/pull/3811
[pull3815]: https://github.com/evennia/evennia/pull/3815
[pull3817]: https://github.com/evennia/evennia/pull/3817
[pull3818]: https://github.com/evennia/evennia/pull/3818
[pull3825]: https://github.com/evennia/evennia/pull/3825
[pull3826]: https://github.com/evennia/evennia/pull/3826
[pull3831]: https://github.com/evennia/evennia/pull/3831
[pull3832]: https://github.com/evennia/evennia/pull/3832
[pull3834]: https://github.com/evennia/evennia/pull/3834
[pull3836]: https://github.com/evennia/evennia/pull/3836
[pull3599]: https://github.com/evennia/evennia/pull/3599
[pull3852]: https://github.com/evennia/evennia/pull/3852
[pull3853]: https://github.com/evennia/evennia/pull/3853
[pull3733]: https://github.com/evennia/evennia/pull/3733
[pull3864]: https://github.com/evennia/evennia/pull/3864
[pull3863]: https://github.com/evennia/evennia/pull/3863
[pull3845]: https://github.com/evennia/evennia/pull/3845
[pull3862]: https://github.com/evennia/evennia/pull/3862
[issue3858]: https://github.com/evennia/evennia/issues/3858
[issue3813]: https://github.com/evennia/evennia/issues/3813
[issue3649]: https://github.com/evennia/evennia/issues/3649
[issue3560]: https://github.com/evennia/evennia/issues/3560
[issue3601]: https://github.com/evennia/evennia/issues/3601
[issue3194]: https://github.com/evennia/evennia/issues/3194
[issue2774]: https://github.com/evennia/evennia/issues/2774
[issue3312]: https://github.com/evennia/evennia/issues/3312
[issue3154]: https://github.com/evennia/evennia/issues/3154
[issue3193]: https://github.com/evennia/evennia/issues/3193
[issue3082]: https://github.com/evennia/evennia/issues/3082
[issue3693]: https://github.com/evennia/evennia/issues/3693
[issue2627]: https://github.com/evennia/evennia/issues/2627


(evennia-501)=
## Evennia 5.0.1

2025 年 7 月 2 日

- [Fix][issue3796]: 修正 Django 版本最小字串過於挑剔，導致
啟動時令人困惑的警告訊息 (Griatch)

[issue3796]: https://github.com/evennia/evennia/issues/3796


(evennia-500)=
## Evennia 5.0.0

2025 年 7 月 1 日

更新的依賴項：Django >5.2 (<5.3), Twisted >24 (<25)。
Python 版本：3.11、3.12、3.13。

此升級需要在現有資料庫上執行 `evennia migrate`
（忽略任何執行`evennia makemigrations`的提示）。

- 壯舉（向後不相容）：RUN MIGRATIONS (`evennia migrate`)：現在需要 Django 5.1 (Griatch)
- 壯舉（向後不相容）：放棄對 Python 3.10 的支援和測試（Griatch）
- [功能][pull3719]：支援Python 3.13。 （電圖）
- [Feat][pull3633]：預設物件的預設描述現在取自 `default_description`
    class variable instead of the `desc` Attribute always being set (count-infinity)
- [Feat][pull3718]：刪除 Windows 的 twistd.bat 建立，不再需要（電圖）
- [壯舉][pull3756]：更新了德語翻譯 (JohnFi)
- [Feat][pull3757]：將更多 i18n 字串加入 `DefaultObject` 以便於翻譯 (JohnFi)
- [Feat][pull3783]：透過在 `pyproject.toml` 中新增相容設定來支援 `ruff` linter 使用者 (jaborsh)
- [Feat][pull3777]：新的 contrib `debugpy` 用於除錯 Evennia，在 VSCode 中使用 `debugpy` 介面卡（電訊號）
- [Feat][pull3795]：支援 evennia 啟動器與 `uv` 安裝一起使用 (TehomCD)
- [修復][pull3677]：確保 `DefaultAccount.create` 標準化為空
如果未提供名稱，則使用字串而不是 `None`，也強制執行字串型別 (InspectorCaracal)
- [修復][pull3682]：允許遊戲內協助搜尋本機啟動的指令
與 `*` （這是 Lunr 搜尋萬用字元）（無限大）
- [修正][pull3684]：Web使用者端開啟設定後停止自動對焦輸入框（無限大）
- [修復][pull3689]：預設搜尋中的部分匹配修復，確保e.g。 `b sw` 唯一
即使周圍有其他型別的劍也能找到`big sword` (InspectorCaracal)
- [修復][pull3690]：在搜尋中，僅允許特殊的「這裡」和「我」關鍵字為有效查詢
除非目前位置和/或呼叫者分別位於有效的搜尋候選者中 (InspectorCaracal)
- [修正][pull3694]：Funcparser 在 `\`-轉義（計數無窮大）後吞嚥其餘行
- [修正][pull3705]：正確序列化 `IntFlag` 列舉型別（電字形）
- [修正][pull3707]：`about` 指令中的正確連結（電訊號）
- [修復][pull3710]：清除`at_server_cold_start`（InspectorCaracal）中的冗餘session
- [修復][pull3711]：Discord 整合中的可用性改進 (InspectorCaracal)
- [修復][pull3721]：避免載入不需要檢查的cmdsets，避免
在有大量物體的房間中載入 cmdsets 會導致效能下降 (InspectorCaracal)
- [修復][issue3688]：無需成為超級使用者即可乾淨地建立 TutorialWorld (Griatch)
- [修復][issue3687]：修正了批次指令/與開發人員許可權互動（Griatch）
- [修正][pull3723]：使用序數別名時 `ingame-map-display` contrib 中的錯誤 (aMiss-aWry)
- [修復][pull3726]：修正 Twisted v25 的 returnValue() 問題
- [修正][pull3729]: Godot 用戶端 text2bbcode mxp 連結轉換錯誤 (ChrisLR)
- [修正][pull3737]：`evennia --gamedir` 指令沒有正確設定 alt gamedir (Russel-Jones)
- [修復][pull3739]：修正 i18n 的 account.py 中的 f 字串 (JohnFi)
- [修正][pull3744]：修正了 i18n 中未擷取格式字串的問題 (JohnFi)
- [修正][pull3743]：記錄物件建立失敗的完整堆疊追蹤 (aMiss-aWry)
- [修復][pull3747]：TutorialWorld橋房沒有正確隨機化天氣影響 (SpyrosRoum)
- [修復][pull3765]：在資料庫 attribute 中儲存 TickerHandler `store_key` 不會
工作正常（電圖）
- [修正][pull3753]：確保 `AttributeProperty`s 在父類別中也使用預設值進行初始化 (JohnFi)
- [修復][pull3751]：如果在沒有帳戶的角色上執行，`access` 和 `inventory` 指令將回溯 (EliasWatson)
- [修正][pull3768]：確保`CmdCopy`指令複製物件類別，
因為否則複數就會遺失 (jaborsh)
- [修正][issue3788]: `GLOBAL_SCRIPTS.all()` 引發錯誤 (Griatch)
- [修正][issue3790]：修正因啟動器中新的資料庫初始化檢查程式碼而導致的遷移問題 (Griatch)
- [修復][issue3794]：確保將 `move_type` kwarg 傳遞到 `at_pre_object_receive|leave` 鉤子 (Griatch)
- 修正：`options` 設定 `NOPROMPTGOAHEAD` 無法設定 (Griatch)
- 修復：使 `\\` 在 funcparser (Griatch) 中正確保留一個反沖
- 修復：測試'echo'inputfunc無法正常工作；現在返回 args/kwargs (Griatch)
- 修復：當一個物件被用作按需任務的類別，然後該物件被刪除時，
它導致重新載入時出現 OnDemandHandler 儲存錯誤。現在將在儲存時進行清理。 （格里奇）
  用作任務的類別 (Griatch)
- 修復：更正 aws contrib 對舊版 django 字串實用程式 (Griatch) 的使用
- [檔案]：來自 InspectorCaracal、Griatch、ChrisLR、JohnFi、Electroglyph、jaborsh、有問題、BlaneWins 的修復

[pull3633]: https://github.com/evennia/evennia/pull/3633
[pull3677]: https://github.com/evennia/evennia/pull/3677
[pull3682]: https://github.com/evennia/evennia/pull/3682
[pull3684]: https://github.com/evennia/evennia/pull/3684
[pull3689]: https://github.com/evennia/evennia/pull/3689
[pull3690]: https://github.com/evennia/evennia/pull/3690
[pull3705]: https://github.com/evennia/evennia/pull/3705
[pull3707]: https://github.com/evennia/evennia/pull/3707
[pull3710]: https://github.com/evennia/evennia/pull/3710
[pull3711]: https://github.com/evennia/evennia/pull/3711
[pull3718]: https://github.com/evennia/evennia/pull/3718
[pull3719]: https://github.com/evennia/evennia/pull/3719
[pull3721]: https://github.com/evennia/evennia/pull/3721
[pull3723]: https://github.com/evennia/evennia/pull/3723
[pull3726]: https://github.com/evennia/evennia/pull/3726
[pull3729]: https://github.com/evennia/evennia/pull/3729
[pull3737]: https://github.com/evennia/evennia/pull/3737
[pull3739]: https://github.com/evennia/evennia/pull/3739
[pull3743]: https://github.com/evennia/evennia/pull/3743
[pull3744]: https://github.com/evennia/evennia/pull/3744
[pull3747]: https://github.com/evennia/evennia/pull/3747
[pull3765]: https://github.com/evennia/evennia/pull/3765
[pull3753]: https://github.com/evennia/evennia/pull/3753
[pull3751]: https://github.com/evennia/evennia/pull/3751
[pull3756]: https://github.com/evennia/evennia/pull/3756
[pull3757]: https://github.com/evennia/evennia/pull/3757
[pull3768]: https://github.com/evennia/evennia/pull/3768
[pull3783]: https://github.com/evennia/evennia/pull/3783
[pull3777]: https://github.com/evennia/evennia/pull/3777
[pull3694]: https://github.com/evennia/evennia/pull/3694
[issue3794]: https://github.com/evennia/evennia/issues/3794
[pull3795]: https://github.com/evennia/evennia/pull/3795
[issue3688]: https://github.com/evennia/evennia/issues/3688
[issue3687]: https://github.com/evennia/evennia/issues/3687
[issue3788]: https://github.com/evennia/evennia/issues/3788
[issue3790]: https://github.com/evennia/evennia/issues/3790



(evennia-450)=
## Evennia 4.5.0

2024 年 11 月 12 日

- [壯舉][pull3634]：房間中遊戲內 `storage` 物品的新 contrib (aMiss-aWry)
- [Feat][pull3636]：使`cpattr`指令也支援Attribute類別（aMiss-aWry）
- [Feat][pull3653]：更新了中文翻譯（Pridell）。
- [修復][pull3635]：修復 Portal Telnet 連線中的記憶體洩漏，強制弱
參考 Telnet 協商，在斷開連線時停止 LoopingCall (a-rodian-jedi)
- [修復][pull3626]：evadventure 教學中 `defense_type` 中的拼字錯誤 (feyrkh)
- [修正][pull3632]：正確設定後備許可權 (InspectorCaracal)
- [修復][pull3639]：當環境使用以下語言時修復`system`指令
小數點逗號 (aMiss-aWry)
- [修正][pull3645]：更正`character_creator` contrib的錯誤回傳(InspectorCaracal)
- [修復][pull3640]：共軛動詞的拼字錯誤修復（aMiss-aWry）
- [修復][pull3647]：內容快取在使用 `init` 掛鉤時未重置內部型別快取 (InspectorCaracal)
- [修復][issue3627]：從 contrib `in-game reports` `help manage` 指令回溯 (Griatch)
- [修復][issue3643]：修正解釋 e.g 的指令元類別。 `usercmd:false()` 鎖定為
a `cmd:` 型別 lock 用於預設存取回退 (Griatch)。
- [修復][pull3651]：EvEditor `:j` 預設為「完全」對齊而不是「左」對齊
已記錄（willmofield）
- [修復][pull3657]：修復 `do_search` 中導致 `FileHelpEntries`
回溯（a-rodian-jedi）
- [修正][pull3660]：物件重新命名後編號別名不會重新整理，除非
端點鉤子被重新呼叫；現在自動觸發呼叫（無窮大）
- [修復][pull3664]：當使用者
已斷開連線，這沒有用(InspectorCaracal)
- [修正][pull3665]：刪除「offer」的錯誤動詞變形例外，
自動動詞變形引擎中的「阻礙」與「改變」(aMiss-aWry)
- [修正][pull3669]：`page` 指令針對某些輸入組合進行回溯 (InspectorCaracal)
- [修復][pull3642]：如果 EvMore 物件不可用，則給出更友善的錯誤
既不在物件上，也不在帳號後備上。 (InspectorCaracal)
- [檔案][pull3655]：修復了在 `file.py` 名稱上錯誤建立的許多連結
檔案（馬拉多）
- [文件][pull3576]：[Pycharm howto][doc-pycharm] 的返工文件
- 檔案更新：feykrh、Griatch、marado、jaborsh

[pull3626]: https://github.com/evennia/evennia/pull/3626
[pull3634]: https://github.com/evennia/evennia/pull/3634
[pull3632]: https://github.com/evennia/evennia/pull/3632
[pull3636]: https://github.com/evennia/evennia/pull/3636
[pull3639]: https://github.com/evennia/evennia/pull/3639
[pull3645]: https://github.com/evennia/evennia/pull/3645
[pull3640]: https://github.com/evennia/evennia/pull/3640
[pull3647]: https://github.com/evennia/evennia/pull/3647
[pull3635]: https://github.com/evennia/evennia/pull/3635
[pull3651]: https://github.com/evennia/evennia/pull/3651
[pull3655]: https://github.com/evennia/evennia/pull/3655
[pull3657]: https://github.com/evennia/evennia/pull/3657
[pull3653]: https://github.com/evennia/evennia/pull/3653
[pull3660]: https://github.com/evennia/evennia/pull/3660
[pull3664]: https://github.com/evennia/evennia/pull/3664
[pull3665]: https://github.com/evennia/evennia/pull/3665
[pull3669]: https://github.com/evennia/evennia/pull/3669
[pull3642]: https://github.com/evennia/evennia/pull/3642
[pull3576]: https://github.com/evennia/evennia/pull/3576
[issue3627]: https://github.com/evennia/evennia/issues/3627
[issue3643]: https://github.com/evennia/evennia/issues/3643
[doc-pycharm]: https://www.evennia.com/docs/latest/Coding/Setting-up-PyCharm.html

(evennia-441)=
## Evennia 4.4.1

2024 年 10 月 1 日

- [修正][issue3629]：恢復預設 Sqlite3 PRAGMA 設定的更改，將其更改為
現有資料庫導致資料庫損壞。對於空資料庫，仍然可以更改
  `SQLITE3_PRAGMAS`設定。 （格里奇）

[issue3629]: https://github.com/evennia/evennia/issues/3629


(evennia-440)=
## Evennia 4.4.0

2024 年 9 月 29 日

> WARNING：由於預設的Sqlite3 PRAGMA設定中存在錯誤，因此
> 如果您使用的是 Sqlite3，建議不要升級到此版本。
> 請改用 `4.4.1` 或更高版本。

- 壯舉：支援`scripts key:typeclass`建立全域scripts
使用動態鍵（而非僅依賴 typeclass' 鍵）(Griatch)
- [Feat][pull3595]：調整 Sqlite3 PRAGMAs 以獲得更好的效能（電圖）
- 壯舉：透過設定使 Sqlite3 PRAGMAs 可設定 (Griatch)
- [Feat][pull3592]：修改了德語定位（“Du”而不是“Sie”，
清理）（Drakon72）
- [Feat][pull3541]：重新設計主要物件搜尋以尊重部分匹配，空
現在搜尋部分匹配所有候選者，整體清理（InspectorCaracal）
- [Feat][pull3588]：新的`DefaultObject`鉤子：`at_object_post_creation`，之後呼叫一次
首次建立但在應用任何原型之後，以及
`at_object_post_spawn(prototype)`，僅在使用原型建立/更新後呼叫（InspectorCaracal）
- [修復][pull3594]：更新/清理一些 Evennia 依賴項（電字形）
- [修復][issue3556]：如果嘗試將 ObjectDB 視為 typeclass (Griatch)，則會出現更好的錯誤
- [修正][issue3590]：使 `examine` 指令正確顯示 `strattr` 型別
Attribute 值 (Griatch)
- [修復][issue3519]：`GLOBAL_SCRIPTS` 容器未列出全域 scripts
明確定義為在 `settings.py` 中重新啟動/重新建立 (Griatch)
- 修正：將已例項化的 Script 傳遞給 `obj.scripts.add` (`ScriptHandler.add`)
沒有將其加入處理程式的物件中（Griatch）
- [修正][pull3533]：修正 Lunr 搜尋問題，導致無法找到類似的幫助條目
姓名 (chiizyjin)
- [修復][pull3603]：修復遠端 APIs 的 LLM contrib 的用戶端標頭 (InspectorCaracal)
- [修正][pull3605]：透過 `@list_node` 修飾的 evmenu 節點正確傳遞節點 kwargs
(InspectorCaracal)
- [修復][pull3597]：解決測試 `new_task_waiting_input ` 的計時問題
窗戶（電畫）
- [修復][pull3611]：修正並更新報告 contrib (InspectorCaracal)
- [修復][pull3625]：狼人教學頁面存在一些問題 (feyrkh)
- [修正][pull3622]：修正了檢查指令回溯時出現 strvalue 錯誤的問題
（失誤）
- [修復][issue3612]：確保幫助條目'`subtopic_separator_char`是
受人尊敬（格里奇）
- [修復][issue3624]：使用整數名稱設定 tags 導致 postgres 上出現錯誤 (Griatch)
- [修復][issue3615]：在 `py` 中使用 `print()` 導致無限迴圈 (Griatch)
- [修復][issue3620]：更好地處理針對 attribute 執行的 TaskHandler
自上次重新載入後已刪除（Griatch）
- [修正][issue3616]：`color ansi` 指令輸出已損壞 (Griatch)
- 修復：使用範例擴充套件了 `color truecolor` 顯示。也更新了檔案（Griatch）
- [檔案][issue3591]：修正NPC反應教學程式碼（Griatch）
- 檔案：教學修復（Griatch、aMiss-aWry、feyrkh）

[issue3591]: https://github.com/evennia/evennia/issues/3591
[issue3590]: https://github.com/evennia/evennia/issues/3590
[issue3556]: https://github.com/evennia/evennia/issues/3556
[issue3519]: https://github.com/evennia/evennia/issues/3519
[issue3612]: https://github.com/evennia/evennia/issues/3612
[issue3624]: https://github.com/evennia/evennia/issues/3624
[issue3615]: https://github.com/evennia/evennia/issues/3615
[issue3620]: https://github.com/evennia/evennia/issues/3620
[issue3616]: https://github.com/evennia/evennia/issues/3616
[pull3595]: https://github.com/evennia/evennia/pull/3595
[pull3533]: https://github.com/evennia/evennia/pull/3533
[pull3594]: https://github.com/evennia/evennia/pull/3594
[pull3592]: https://github.com/evennia/evennia/pull/3592
[pull3603]: https://github.com/evennia/evennia/pull/3603
[pull3605]: https://github.com/evennia/evennia/pull/3605
[pull3597]: https://github.com/evennia/evennia/pull/3597
[pull3611]: https://github.com/evennia/evennia/pull/3611
[pull3541]: https://github.com/evennia/evennia/pull/3541
[pull3588]: https://github.com/evennia/evennia/pull/3588
[pull3625]: https://github.com/evennia/evennia/pull/3625
[pull3622]: https://github.com/evennia/evennia/pull/3622


(evennia-430)=
## Evennia 4.3.0

2024 年 8 月 11 日

- [專長][pull3531]：新contrib；`in-game reports`用於處理使用者報告，
遊戲中的錯誤等(InspectorCaracal)
- [Feat][pull3586]：增加 ANSI 顏色支援 `|U`、`|I`、`|i`、`|s`、`|S`
底線重置、斜體/重置和刪除線/重置（電子字形）
- 壯舉：新增 `Trait.traithandler` 反向引用，以便從 Traits 自訂 Traits
contrib可以找到並引用其他特徵。 （格里奇）
- [Feat][pull3582]：為 ANSIString 新增真彩色解析/後備（電字形）
- [修正][pull3571]：部分多重配對搜尋結果的視覺顯示效果較好
(InspectorCaracal)
- [修正][issue3578]：原型「別名」鍵未正確同質化為列表
（格里奇）
- [修正][pull3550]：rpsystem contrib 搜尋將執行全域搜尋的問題
    of local search on multimatch (InspectorCaracal)
- [修正][pull3585]：`TagCmd.switch_options` 命名錯誤（不穩定模式）
- [修正][pull3580]：修正導致 `find/loc` 在結果中顯示錯誤 dbref 的拼字錯誤（不穩定模式）
- [修正][pull3589]：修正未來 Python 版本的 `utils.py` 中的正規表示式轉義 (hhsiao)
- [檔案]：為顏色檔案新增真彩色描述（電圖）
- [檔案]：檔案修復（Griatch、InspectorCaracal、電圖）

[pull3585]: https://github.com/evennia/evennia/pull/3585
[pull3580]: https://github.com/evennia/evennia/pull/3580
[pull3586]: https://github.com/evennia/evennia/pull/3586
[pull3550]: https://github.com/evennia/evennia/pull/3550
[pull3531]: https://github.com/evennia/evennia/pull/3531
[pull3571]: https://github.com/evennia/evennia/pull/3571
[pull3582]: https://github.com/evennia/evennia/pull/3582
[pull3589]: https://github.com/evennia/evennia/pull/3589
[issue3578]: https://github.com/evennia/evennia/issues/3578

(evennia-420)=
## Evennia 4.2.0

2024 年 6 月 27 日

- [功能][pull3470]：新增`exit_order` kwarg
`DefaultObject.get_display_exits` 更容易自訂順序
  標準出口顯示在房間內（chiizujin）
- [功能][pull3498]: 用戶端正確更新Evennia的螢幕寬度
更改寬度（假設用戶端正確支援 NAWS）(michaelfaith84)
- [功能][pull3502]：新`sethelp/locks`允許編輯幫助條目
首次建立後鎖定 (chiizujin)
- [功能][pull3514]：支援`$pron(pronoun, key)`及新`$pconj(verb, key)`
（代名詞詞形變化）演員立場 (InspectorCaracal)
- [功能][pull3521]：允許 GMCP 指令名稱包含 `WORD`（完全大寫）
而不是僅`Word`（標題）更好地支援特定客戶（InspectorCaracal）
- [功能][pull3447]：新Contrib：成就（InspectorCaracal）
- [功能][pull3494]：Xterm truecolor hex 支援`|#0f0` 樣式。擴充
`color true` 進行測試 (michaelFaith84)
- [功能][pull3497]：使用下列指令將可選寬度新增至 EvEditor 洪水填充指令中
新的 `=` 引數，例如 `:f=40` 或 `:j 1:2 l = 60` (chiizujin)
- [功能][pull3549]：重新載入伺服器時執行`collectstatic`指令
自動維持遊戲資產同步(InspectorCaracal)
- [功能][issue3522]：（也是一個修復）在所有模型屬性返回上設定 `.created_date` 屬性
根據`settings.TIME_ZONE`（Griatch）調整的時間
- [語言][pull3523]：更新了波蘭語翻譯（Moonchasered）
- [修復][pull3495]：修復特徵 contribs 重新載入後不更新的問題 (jaborsh)
- [修正][pull3491]：修正使用格式錯誤的正規表示式搜尋時 EvEditor 中的回溯 (chiizujin)
- [修復][pull3489]：超級使用者可能會破壞荒野contrib退出（t34lbytes）
- [修正][pull3496]：EvEditor 無法正確顯示搜尋和取代回饋
更換顏色時（Chiizujin）
- [修復][pull3499]：挖掘/隧道指令沒有回顯新的typeclass
正確建立房間（chiizujin）
- [修復][pull3501]：使用 `sethelp` 建立與
指令名稱使得該條目稍後無法編輯/刪除 (chiizujin)
- [修復][pull3506]：修正在遊戲中OLC精靈設定原型父級時的回溯（chiizujin）
- [修正][pull3507]：如果中止原型精靈將不會儲存變更
更新現有的衍生例項 (chiizujun)
- [修復][pull3516]：退出 chargen contrib 選單現在將觸發自動尋找 (InspectorCaracal)
- [修復][pull3517]：提供 `Object.search` 時導致 `candidates` 清單為空
預設使用而不是找不到任何內容(InspectorCaracal)
- [修復][pull3518]：`GlobalScriptsContainer.all()` 引發了回溯 (InspectorCaracal)
- [修正][pull3520]：未正確列出退出排序順序中未包含的退出 (chiizujin)
- [修正][pull3529]：修正頁面/清單指令未正確顯示接收到的頁面 (chiizujin)
- [修復][pull3530]：EvEditor cmdset 優先順序增加，因此不回應
在編輯器中的移動指令 (chiizujin)
- [修復][pull3537]: 元件 contrib (ChrisLR) 中的 Bug 設定 `_fields`
- [修復][pull3542]：更新 `character_creator` contrib 以使用帳戶的外觀
模板正確 (InspectorCaracal)
- [修正][pull3545]：修正本地物件 cmdsets (InspectorCaracal) 的 cmdhandler 中的回退問題
- [修復][pull3554]：修復/讀取自訂 `ic` 指令到 `character_creator` contrib (InspectorCaracal)
- [修復][pull3566]：確保 `website/base.html` 網站庫已被定位
明確地這樣它就不會被應用程式中其他地方的相同檔案名稱覆蓋（InspectorCaracal）
- [修復][issue3387]：將所有遊戲模板檔案字串更新為最新
（格里奇）
- [檔案]：檔案修復（Griatch、chiizujin、InspectorCaracal、iLPDev）

[pull3470]: https://github.com/evennia/evennia/pull/3470
[pull3495]: https://github.com/evennia/evennia/pull/3495
[pull3491]: https://github.com/evennia/evennia/pull/3491
[pull3489]: https://github.com/evennia/evennia/pull/3489
[pull3496]: https://github.com/evennia/evennia/pull/3496
[pull3498]: https://github.com/evennia/evennia/pull/3498
[pull3499]: https://github.com/evennia/evennia/pull/3499
[pull3501]: https://github.com/evennia/evennia/pull/3501
[pull3502]: https://github.com/evennia/evennia/pull/3502
[pull3506]: https://github.com/evennia/evennia/pull/3506
[pull3507]: https://github.com/evennia/evennia/pull/3507
[pull3514]: https://github.com/evennia/evennia/pull/3514
[pull3516]: https://github.com/evennia/evennia/pull/3516
[pull3517]: https://github.com/evennia/evennia/pull/3517
[pull3518]: https://github.com/evennia/evennia/pull/3518
[pull3520]: https://github.com/evennia/evennia/pull/3520
[pull3521]: https://github.com/evennia/evennia/pull/3521
[pull3447]: https://github.com/evennia/evennia/pull/3447
[pull3494]: https://github.com/evennia/evennia/pull/3494
[pull3497]: https://github.com/evennia/evennia/pull/3497
[pull3529]: https://github.com/evennia/evennia/pull/3529
[pull3530]: https://github.com/evennia/evennia/pull/3530
[pull3537]: https://github.com/evennia/evennia/pull/3537
[pull3542]: https://github.com/evennia/evennia/pull/3542
[pull3545]: https://github.com/evennia/evennia/pull/3545
[pull3549]: https://github.com/evennia/evennia/pull/3549
[pull3554]: https://github.com/evennia/evennia/pull/3554
[pull3523]: https://github.com/evennia/evennia/pull/3523
[pull3566]: https://github.com/evennia/evennia/pull/3566
[issue3522]: https://github.com/evennia/evennia/issues/3522
[issue3387]: https://github.com/evennia/evennia/issues/3387


(evennia-411)=
## Evennia 4.1.1

2024 年 4 月 6 日

- [修正][pull3483]：第三人稱風格中的「you」對映錯誤
`msg_contents` (InspectorCaracal)
- [修復][pull3472]: 新的`filter_visible`預設沒有排除自己
(InspectorCaracal)
- 修復：`find #dbref` 結果不包括以下結果
`.get_extra_display_name_info`（預設顯示#dbref）（Griatch）
- 修復：為 API 新增 `DefaultAccount.get_extra_display_name_info` 方法
遵守指令中的`DefaultObject`。 （格里奇）
- 修復：當 repr() 時顯示 `XYZRoom` 子類別。 （格里奇）
- [修正][pull3485]：`sethome` 訊息中的拼字錯誤 (chiizujin)
- [修復][pull3487]：修正使用 `get`、`drop` 和 `give` 時的回溯
引數 (InspectorCaracal)
- [修正][issue3476]：不要忽略大小寫錯誤的 EvEditor 指令 (Griatch)
- [修復][issue3477]：`at_server_reload_start()` 鉤子未觸發
重新載入（回歸）。
- [修復][issue3488]: `AttributeProperty(<default>, autocreate=False)`，其中
`<default>` 是可變的，無法就地正確更新/儲存 (Griatch)
- [檔案] 新增了新的 [Server-Lifecycle][doc-server-lifecycle] 頁面來描述
伺服器啟動/停止/重新載入時呼叫的鉤子 (Griatch)
- [檔案] 檔案拼字錯誤修復（Griatch、chiizujin）

[pull3472]: https://github.com/evennia/evennia/pull/3472
[pull3483]: https://github.com/evennia/evennia/pull/3483
[pull3485]: https://github.com/evennia/evennia/pull/3485
[pull3487]: https://github.com/evennia/evennia/pull/3487
[issue3476]: https://github.com/evennia/evennia/issues/3476
[issue3477]: https://github.com/evennia/evennia/issues/3477
[issue3488]: https://github.com/evennia/evennia/issues/3488
[doc-server-lifecycle]: https://www.evennia.com/docs/latest/Concepts/Server-Lifecycle.html


(evennia-410)=
## Evennia 4.1.0

2024 年 4 月 1 日

- [棄用]：`DefaultObject.get_visible_contents` - 在核心中未使用，將被
已刪除。將新的 `.filter_visible` 與 `.get_display_*` 方法一起使用。
- [棄用]：`DefaultObject.get_content_names` - 在核心中未使用，將被
已刪除。請改用 `DefaultObject.get_display_*` 方法。

- [功能][pull3421]：新的 `utils.compress_whitespace` 實用程式與
預設物件的 `.format_appearance` 使其更容易過載而無需
  在鉤子返回中新增換行符。 (InspectorCaracal)
- [功能][pull3458]：用於更改幫助主題的新 `sethelp/category` 開關
建立後的類別 (chiizujin)
- [功能][pull3467]：新增 `alias/delete` 開關以刪除物件別名
從遊戲中使用預設指令（chiizujin）
- [功能][issue3450]：預設的 `page` 指令現在 tags 其 `Msg` 物件
與tag'頁面'（類別'通訊'），並檢查`Msg`''讀取'lock。
  向後相容舊頁 (Griatch)
- [功能][pull3466]：新增可選的`no_article` kwarg
`DefaultObject.get_numbered_name`為系統跳過自動新增
  文章。 （千津津）
- [功能][pull3433]：新增預設取得/丟棄的能力以影響堆疊
項，例如自訂類別父項的 `get/drop 3 rock` (InspectorCaracal)
- 功能：清理指令執行時顯示的預設指令變數列表
未定義 `func()` (Griatch)
- [功能][issue3461]：新增`DefaultObject.filter_display_visible`輔助方法
以便更輕鬆地自訂物件可見性規則。 （格里奇）
- [修復][pull3446]：在中使用複數（'no apples'）而不是單數（'no apples'）
`get_numbered_name` 以獲得更好的語法形式 (InspectorCaracal)
- [修正][pull3453]：物件別名未顯示在搜尋多重配對中
消歧顯示 (chiizujin)
- [修復][pull3455]：沒有 `= text` 的 `sethelp/edit <topic>` 建立了 `None`
會遺失編輯的條目。 （赤子金）
- [修正][pull3456]：`format_grid` 實用程式用於 `help` 指令引發的指令
對於更寬的用戶端寬度消失（chiizujin）
- [修正][pull3457]：不同大小寫的說明主題類別顯示為
重複項 (chiizujin)
- [修復][pull3454]：製作 contrib 的 `recipe.msg` 時出現回溯
(InspectorCaracal)
- [修正][pull3459]：EvEditor 線回顯壓縮空白錯誤 (chiizujin)
- [修復][pull3463]: EvEditor:help 描述了錯誤的:paste 操作
方式（chiizujin）
- [修正][pull3464]：EvEditor範圍：範圍規格未回傳正確的
範圍（chiizujin）
- [修正][issue3462]: EvEditor:UU 和:DD 等指令不正確
有別於他們的小寫替代品 (Griatch)
- [修正][issue3460]：`menu_login` contrib 回歸導致錯誤
建立新角色時（Griatch）
- 檔案：新增了[怪物和NPC AI][docAI]的初學者教學課程，
[任務][docQuests]和[製作程式地下城][docDungeon] (Griatch)
- 檔案修復（Griatch、InspectorCaracal、homeofpoe）

[pull3421]: https://github.com/evennia/evennia/pull/3421
[pull3446]: https://github.com/evennia/evennia/pull/3446
[pull3453]: https://github.com/evennia/evennia/pull/3453
[pull3455]: https://github.com/evennia/evennia/pull/3455
[pull3456]: https://github.com/evennia/evennia/pull/3456
[pull3457]: https://github.com/evennia/evennia/pull/3457
[pull3458]: https://github.com/evennia/evennia/pull/3458
[pull3454]: https://github.com/evennia/evennia/pull/3454
[pull3459]: https://github.com/evennia/evennia/pull/3459
[pull3463]: https://github.com/evennia/evennia/pull/3463
[pull3464]: https://github.com/evennia/evennia/pull/3464
[pull3466]: https://github.com/evennia/evennia/pull/3466
[pull3467]: https://github.com/evennia/evennia/pull/3467
[pull3433]: https://github.com/evennia/evennia/pull/3433
[issue3450]: https://github.com/evennia/evennia/issues/3450
[issue3462]: https://github.com/evennia/evennia/issues/3462
[issue3460]: https://github.com/evennia/evennia/issues/3460
[issue3461]: https://github.com/evennia/evennia/issues/3461
[docAI]: https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Part3/Beginner-Tutorial-AI.html
[docQuests]: https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Part3/Beginner-Tutorial-Quests.html
[docDungeon]: https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Part3/Beginner-Tutorial-Dungeon.html

(evennia-400)=
## Evennia 4.0.0

2024 年 3 月 17 日

- 功能：支援Python 3.12（Griatch）。目前支援3.10、3.11和
3.12.請注意，未來版本將刪除 3.10 支援。
- 功能：將 `evennia[extra]` scipy 依賴項更新至 1.12 以支援最新版本
Python。請注意，這可能會改變在以下情況下選擇的（等效）路徑：
  遵循 xyzgrid contrib 尋路。
- 功能：*向後不相容*：`DefaultObject.get_numbered_name` 現在取得物件的
透過 `.get_display_name` 命名，以便更好地與識別系統相容。
- 功能：*向後不相容*：刪除了 (#dbref) 顯示
`DefaultObject.get_display_name`，而不是使用新的`.get_extra_display_name_info`
  獲取此資訊的方法。物件的顯示範本已擴充套件為
  可選擇新增此資訊。這使得顯示額外的物件訊息
  管理顯式操作並開放 `get_display_name` 供一般用途。
- 特徵：新增 `ON_DEMAND_HANDLER.set_dt(key, category, dt)` 和
`.set_stage(key, category, stage)` 允許手動調整任務時間，
  例如加速植物生長的咒語 (Griatch)
- 特徵：新增`ON_DEMAND_HANDLER.get_dt/stages(key,category, **kwargs)`，其中
kwargs 被傳遞到階段定義的任何階段可呼叫中。 （格里奇）
- 功能：將 `use_assertequal` kwarg 加入 `EvenniaCommandTestMixin` 測試中
班級;這使用 django 的 `assertEqual` 代替預設的更寬鬆的檢查器，
  這對於測試表空白很有用（Griatch）
- 功能：新的 `utils.group_objects_by_key_and_desc` 用於對清單進行分組
基於可見鍵和描述的物件。對於庫存清單很有用（Griatch）
- 功能：新增 `DefaultObject.get_numbered_name` `return_string` bool kwarg，僅用於
根據計數傳回單數/複數，而不是同時傳回單數/複數 (Griatch)
- [修復][issue3443] 刪除了 `@reboot` 別名到 `@reset` 以免誤導人們
認為你可以從遊戲中重新啟動portal+伺服器（你不能）（Griatch）
- 修復：`DefaultObject.get_numbered_name` 使用 `.name` 而不是
`.get_display_name` 破壞了辨識系統。可能導致物件的#dbref
  將在更多地方向管理員顯示 (Griatch)
- [修復][pull3420]：重構服裝contrib的庫存指令與
Evennia 核心版本（michaelfaith84、Griatch）
- [修正][issue3438]：以 tag 限制搜尋並未將搜尋字串納入其中
帳戶（格里奇）
- [修正][issue3411]：SSH 連線導致協定中的回溯 (Griatch)
- 修正：解決從資料庫載入按需處理程式資料時的錯誤（Griatch）
- 安全性：rpsystem 正規表示式中潛在的 O(n2) 正規表示式漏洞 (Griatch)
- 安全性：修正角色頁面重新導向中潛在的重定向漏洞（Griatch）
- 檔案修復（iLPdev、Griatch、CloudKeeper）

[pull3420]: https://github.com/evennia/evennia/pull/3420
[issue3438]: https://github.com/evennia/evennia/issues/3438
[issue3411]: https://github.com/evennia/evennia/issues/3411
[issue3443]: https://github.com/evennia/evennia/issues/3443

(evennia-320)=
## Evennia 3.2.0

2024 年 2 月 25 日

- 特點：新增[`evennia.ON_DEMAND_HANDLER`][new-ondemandhandler]來製作
更容易實施按需運算的變更 (Griatch)
- [功能][pull3412]：可以在中加入自訂webclient css
`webclient/css/custom.css`，與網站相同 (InspectorCaracal)
- [特徵][pull3367]：[元件contrib][pull3367extra]變得更好
繼承、用於選擇 attr 儲存的插槽名稱、加速和修復 (ChrisLR)
- 功能：將 `DefaultObject.search` 方法分解為幾個助手來製作
更容易覆蓋（Griatch）
- 修正：使用 rpsystem contrib 解決多重配對錯誤 (Griatch)
- 修復：刪除 `AMP_ENABLED` 設定，因為它沒有真正的目的，並且
如果設定錯誤，它會變得更加無用（Griatch）。
- 功能：刪除 Evennia 登入的過於嚴格的密碼限制，使用
django 預設使用具有更多不同字元的密碼。
- 修正沒有引數的 `services` 指令會回溯（回歸）(Griatch)
- [修復][pull3423]：修復荒野contrib移動到已存在的錯誤
荒野房間(InspectorCaracal)
- [修復][pull3425]：不總是包含製作配方的範例
使用製作contrib (InspectorCaracal)
- [修復][pull3426]：回溯禁止僅使用一個缺口的通道
(InspectorCaracal)
- [修正][pull3434]：調整 lunr 搜尋權重以避免 cmd 別名衝突
導致某些幫助條目遮蓋其他條目的按鍵 (InspectorCaracal)
- 修復：使 `menu/email_login` contribs 榮譽 `NEW_ACCOUNT_REGISTRATION_ENABLED`
設定（格里奇）
- 檔案修復（InspectorCaracal，Griatch）

[new-ondemandhandler]: https://www.evennia.com/docs/latest/Components/OnDemandHandler.html
[pull3412]: https://github.com/evennia/evennia/pull/3412
[pull3423]: https://github.com/evennia/evennia/pull/3423
[pull3425]: https://github.com/evennia/evennia/pull/3425
[pull3426]: https://github.com/evennia/evennia/pull/3426
[pull3434]: https://github.com/evennia/evennia/pull/3434
[pull3367]: https://github.com/evennia/evennia/pull/3367
[pull3367extra]: https://www.evennia.com/docs/latest/Contribs/Contrib-Components.html

(evennia-311)=
## Evennia 3.1.1

2024 年 1 月 14 日

- [修復][pull3398]：修復為e.g。 `elvish"Hello"` 在 rp 語言中正常運作
contrib (InspectorCaracal)
- [修復][pull3405]：修復/更新 Godot 使用者端 contrib 以支援 Godot4 和
最新 Evennia portal 更改 (ChrisLR)
- 更新了 wiki 安裝檔案 (InspectorCaracal)
- 檔案字串修復（bradleymarques、Griatch）
- 檔案教學修復 (Griatch)

[pull3398]: https://github.com/evennia/evennia/pull/3398
[pull3405]: https://github.com/evennia/evennia/pull/3405


(evennia-310)=
## Evennia 3.1.0

2024 年 1 月 8 日

- [功能][pull3393]: EvMenu 只會使用其中的一列選項
螢幕閱讀器模式 (InspectorCaracal)
- [功能][pull3386]: 新增 VS 程式碼檔案到預設 gitignore (InspectorCaracal)
- [修正][pull3373]：使用預設`create`指令(InspectorCaracal)時發生錯誤。
- [修正][pull3375]：`tunnel` 指令不適用於自訂字首（色度儀）。
- [修正][pull3376]：回退到預設 cmdset 回退時出錯
(InspectorCaracal)
- [修復][pull3377]：`character_creator` 使用新的 Chargen 系統重構進行了更新
在 Evennia 3.0.0 中；修復不尊重 `START_LOCATION` 的問題
(InspectorCaracal)
- [修復][pull3378]：預設新增“where”作為 LUNR 搜尋例外，因為它是
不應忽視的常見泥漿指令。 （脂肪酸）
- [修正][pull3382]：確保全域 scripts 在重新啟動時正確啟動
(InspectorCaracal)
- [修復][pull3394]：修復 ExpandedRoom contrib (jaborsh) 中的時間問題
- 檔案修復（homeofpoe、gas-public-wooden-clean、InspectorCaracal、Griatch）

[pull3373]: https://github.com/evennia/evennia/pull/3373
[pull3375]: https://github.com/evennia/evennia/pull/3375
[pull3376]: https://github.com/evennia/evennia/pull/3376
[pull3377]: https://github.com/evennia/evennia/pull/3377
[pull3378]: https://github.com/evennia/evennia/pull/3378
[pull3382]: https://github.com/evennia/evennia/pull/3382
[pull3393]: https://github.com/evennia/evennia/pull/3393
[pull3394]: https://github.com/evennia/evennia/pull/3394
[pull3386]: https://github.com/evennia/evennia/pull/3386


(evennia-300)=
## Evennia 3.0.0

2023 年 12 月 20 日

- 依賴性：扭曲 23.10 (<24) 以解決上游 CVE 警報。
- 依賴項（可能向後不相容）：Django 4.2 (<4.3)。增加
最低支援版本MariaDB、MySQL 和PostgreSQL，
  參見[django發布節點][django-release-notes]
- [功能][pull3313]（向後不相容）：`OptionHandler.set` 現在返回
`BaseOption` 而不是 `.value`。而是訪問 `.value` 或 `.display()`
  在此迴歸上獲得更多控制。 （沃倫德）
- [功能][pull3278]：（向後不相容）：將主頁重構為多個子部分以方便使用
重寫和組合 (johnnyvoruz)
- [功能][pull3180]：（可能向後不相容）：製作建置指令
使用新的實用掛鉤（Volund）更容易覆蓋
- [功能][issue3273]：允許將 `text_kwargs` kwarg 傳遞到 `EvMore.msg` 以進行擴充套件
用於每個evmore頁面的outputfunc。
- [功能][pull3286]：允許 Discord 機器人更改使用者的暱稱並分配
給定伺服器 (holl0wstar) 上使用者的角色。
- [功能][pull3301]：使EvenniaAdminSite更好地包含自訂模型；新增
`DJANGO_ADMIN_APP_ORDER` 和 `DJANGO_ADMIN_APP_EXCLUDE` 可修改
  設定。 （Volund）
- [功能][pull3179]：`.db._playable_characters` 助手的處理
方法。還新增了事件掛鉤，以便在此列表更改時修改效果 (Volund)
  在伺服器啟動之前避免競爭條件 (Volund)
- [功能][pull3281]：為演員姿態表情新增`$your()`和`$Your()`（Volund）
- [功能][pull3177]：加`Account.get_character_slots()`，
`.get_available_character_slots()`、`.check_available_slots` 和
  `at_post_create_character` 允許更好地自訂角色建立的方法 (Volund)
- [功能][pull3319]：重構/清理Evennia伺服器/portal啟動檔案
進入服務以便更容易覆蓋（Volund）
- [功能][issue3307]：使用監視器處理程式時新增對Attribute-類別的支援
使用輸入函式來監視 Attribute 的變化。
- [特徵][pull3342]：新增`Command.cmdset_source`，分別指cmdset
指令最初是從 (Volund) 中提取的
- [功能][pull3343]：將`access_type`作為可選kwarg新增到lockfuncs（Volund）
- [功能][pull3344]：用於檢查請求中的IP/子網路的新中介軟體。新的
工具 `evennia.utils.match_ip` 和 `utils.ip_from_request` 提供協助。 （沃倫德）
- [功能][pull3349]：重構了幾乎所有預設指令以使用
`Command.msg` 超過 `command.caller.msg` 直接呼叫（更靈活）（Volund）
- [功能][pull3346]：重構cmdhandler使其更具可擴充套件性；讓cmd合併
更具確定性（Volund）
- [功能][pull3348]：讓 Fallback AJAX Web 使用者端更加可自訂（與
websocket 用戶端）（Volund）
- [功能][pull3353]：為每個webclient例項新增唯一id，分隔播放
sessions 從同一瀏覽器執行。 (InpsectorCaracal)
- [功能][pull3365]：使rpsystem為contrib的字首（預設為`/`）
可透過設定進行設定（過去是硬編碼的）(InspectorCaracal)
- 修復（向後不相容）：將 `settings._TEST_ENVIRONMENT` 更改為
`settings.TEST_ENVIRONMENT` 解決重構啟動序列期間的問題。
- [修復][pull3347]：typeclasses 上的新 `generate_default_locks()` 方法；
`.create` 和 `lockhandler.add()` 現在將正確處理空字串
（沃倫德）
- [修復][pull3197]：確保全域scripts只從一個地方開始，
- [修正][pull3324]：使帳戶登入失敗訊號正確觸發。新增
`CUSTOM_SIGNAL` 用於新增自己的訊號（Volund）
- [修復][pull3267]：ObjectSessionHandler (InspectorCaracal) 中缺少重新快取步驟
- [修復][pull3270]：Evennia 現在是它自己的 MSSP 系列，所以我們應該返回它
而不是「自訂」(InspectorCaracal)
- [修正][pull3274]：建立初始值為 nattributes 的物件時回溯
(InspectorCaracal)
- [修復][issue3272]：確保 `ScriptHandler.add` 在透過時不會失敗
例項化script。 （沃倫德）
- [修正][pull3350]：`CmdHelp` 在使用錯誤的協定金鑰識別碼時
路由到 ajax Web 使用者端。
- [修正][pull3338]：解決 XYZGrid contrib 啟動指令中的 if/elif 錯誤
（賈博什）
- [修正][issue3331]：以不區分大小寫的方式進行 XYZGrid 查詢 zcoords。
- [修復][pull3322]：修復`BaseOption.display`始終回傳字串。
- [修復][pull3358]：修復 Portal 在具有時重置 `server_restart_mode` 標誌
重啟後成功重新連線到伺服器。 (InspectorCaracal)
- [修正][pull3359]：修正gendersub contrib以在引用時使用正確的代名詞
除了自己之外的其他物體（InspectorCaracal）
- [修復][pull3361]：修正帶有類別的監控屬性（scyfris）
- 檔案和檔案字串：大量拼字錯誤和其他修復（iLPdev、InspectorCaracal、jaborsh、
HouseOfPoe、格里奇等）
- 初學者教學：清理並提前開始解釋如何新增
預設cmdsets (Griatch)。

[pull3267]: https://github.com/evennia/evennia/pull/3267
[pull3270]: https://github.com/evennia/evennia/pull/3270
[pull3274]: https://github.com/evennia/evennia/pull/3274
[pull3278]: https://github.com/evennia/evennia/pull/3278
[pull3286]: https://github.com/evennia/evennia/pull/3286
[pull3301]: https://github.com/evennia/evennia/pull/3301
[pull3179]: https://github.com/evennia/evennia/pull/3179
[pull3197]: https://github.com/evennia/evennia/pull/3197
[pull3313]: https://github.com/evennia/evennia/pull/3313
[pull3281]: https://github.com/evennia/evennia/pull/3281
[pull3322]: https://github.com/evennia/evennia/pull/3322
[pull3177]: https://github.com/evennia/evennia/pull/3177
[pull3180]: https://github.com/evennia/evennia/pull/3180
[pull3319]: https://github.com/evennia/evennia/pull/3319
[pull3324]: https://github.com/evennia/evennia/pull/3324
[pull3338]: https://github.com/evennia/evennia/pull/3338
[pull3342]: https://github.com/evennia/evennia/pull/3342
[pull3343]: https://github.com/evennia/evennia/pull/3343
[pull3344]: https://github.com/evennia/evennia/pull/3344
[pull3349]: https://github.com/evennia/evennia/pull/3349
[pull3350]: https://github.com/evennia/evennia/pull/3350
[pull3346]: https://github.com/evennia/evennia/pull/3346
[pull3348]: https://github.com/evennia/evennia/pull/3348
[pull3358]: https://github.com/evennia/evennia/pull/3358
[pull3359]: https://github.com/evennia/evennia/pull/3359
[pull3361]: https://github.com/evennia/evennia/pull/3361
[pull3347]: https://github.com/evennia/evennia/pull/3347
[pull3353]: https://github.com/evennia/evennia/pull/3353
[pull3365]: https://github.com/evennia/evennia/pull/3365
[issue3272]: https://github.com/evennia/evennia/issues/3272
[issue3273]: https://github.com/evennia/evennia/issues/3273
[issue3307]: https://github.com/evennia/evennia/issues/3307
[issue3331]: https://github.com/evennia/evennia/issues/3331

[django-release-notes]: https://docs.djangoproject.com/en/4.2/releases/4.2/#backwards-incompatible-changes-in-4-2

(evennia-230)=
## Evennia 2.3.0

2023 年 9 月 3 日

- 功能：節點中多個幫助類別的EvMenu工具提示（Seannio）。
- 功能：預設 `examine` 指令現在也顯示帳戶的 `last_login`
（邁克爾費斯84）
- 修正：Portal 會意外啟動全域 scripts。 （布隆登）
- 修正：列印 CounterTrait contrib 物件時回溯。 (InspectorCaracal)
- 修復：evadventure 抽搐戰鬥的 `create_combathandler` 召喚中的拼字錯誤。
- 檔案：修正 evadventure Equipmenthandler 中封鎖建立 NPC 的錯誤。
遊戲中（Griatch）。
- 檔案：大量的拼字錯誤修復（iLPDev、moldikins、Griatch）等）

(evennia-220)=
## Evennia 2.2.0

2023 年 8 月 6 日

- Contrib：大語言模型（LLM）AI整合；允許 NPCs 使用
來自 LLM 伺服器的回應。
- 修復：確保在非重複的 Scripts 上也呼叫 `at_server_reload`。
- 修正：Webclient 在向其傳送未知的輸出函式時沒有給出正確的錯誤。
- 修復：除非設定了 `client_raw` 標誌，否則使 `py` 指令始終傳送字串。
- 修復：`Script.start` 與整數 `start_delay` 導致回溯。
- 修正：從許可權層次結構設定中刪除「訪客」會導致存取混亂。
- 檔案：刪除 Travis/TeamCity CI 工具的檔案頁面，它們都非常多
已經過時了，Travis 不再免費 OSS 了。
- 檔案：教學中的大量拼字錯誤和錯誤修復。

(evennia-210)=
## Evennia 2.1.0

2023 年 7 月 14 日

- 修復：新的`ExtendedRoom` contrib在沒有描述的情況下挖掘時有錯誤。
- 修復：清理 evadventure 教學中的 `get_sides` 函式也返回
呼叫戰鬥者及其`allies`返回，以使其更容易推理。
- 功能：新增`SSL_CERTIFICATE_ISSUERS`自訂Telnet+SSL設定。
- Contrib：重構`dice.roll` contrib 函式以使用`safe_eval`。現在可以
可選擇用作 `dice.roll("2d10 + 4 > 10")`。老方法也有效。
- 很多文件更新。

(evennia-201)=
## Evennia 2.0.1

2023 年 6 月 17 日

- 修復：`ExtendedRoom` contrib (InspectorCaracal) 中的外觀錯誤

(evennia-200)=
## Evennia 2.0.0

2023 年 6 月 10 日

- **可能向後不相容**：現已更新 contrib `ExtendedRoom`
支援任意房間狀態、基於狀態的描述、嵌入式 funcparser
  tags，詳細資料和隨機訊息。  雖然此功能是為了
  盡可能向後相容，所以很多人依賴這個contrib類
  我們正在更新主要Evennia版本以顯示重大變更。
- 新Contrib：`Container` typeclass，帶有用於儲存和檢索的新指令
裡面的東西(InspectorCaracal)
- 功能：為具有多個tags的設定類別新增`TagCategoryProperty`
直接作為物件的屬性。補充`TagProperty`。
- 功能：Attribute-支援儲存/載入`deques`並設定`maxlen=`。
- 功能：重構以提供 `evennia.SESSION_HANDLER` 以便更容易過載
迴圈進口問題的風險較小（Volund）
- 修正：允許webclient的goldlayout UI（預設）理解`msg`
`cls` kwarg 用於為每個結果 `div` 客製化 CSS 類 (friarzen)
- 修復：`AttributeHandler.all()` 現在實際上接受 `category=` 作為
關鍵字 arg，就像我們的檔案已經聲稱的那樣（Volund）
- 修正：`TickerHandler` 儲存金鑰更新已重構，修復了以下問題
更新間隔（InspectorCaracal）
- 檔案：刪除了有關 Windows 上的 Python3.11 的警告；現在上游 Twistd
在 Windows 上支援 3.11。
- 檔案：NPCs、Base-Combat Twitch-Combat 和的新初學者教學課程
回合製戰鬥（注意初級教學還是WIP）。
- 穩定如何在檔案中進行重大更新。
- 修復：修復了許多其他小錯誤。


(evennia-130)=
## Evennia 1.3.0

2023 年 4 月 29 日

- 功能：更好的 ANSI 顏色回退 (InspectorCaracal)。
- 功能：新增將 `deque` 和 `maxlen` 儲存到屬性的支援（之前
`maxlen` 被忽略）。
- 修正：使用者名稱驗證器在網頁中無法正確顯示錯誤
報名錶。
- 修復：元件 contrib 有繼承 typeclasses 的問題 (ChrisLR)
- 修復：衣服中的 f 弦修復 contrib (aMiss-aWry)
- 修復：`EvenniaTestCase` 正確重新整理 idmapper 快取 (bradleymarques)
- 工具：scripts 的更多單元測試 (Storsorken)
- 檔案：為出口、角色和房間製作單獨的文件頁面。擴充套件瞭如何
使用模板更改遊戲內物件的描述。
- 檔案：修復了大量檔案問題和拼字錯誤。

(evennia-121)=
## Evennia 1.2.1

2023 年 2 月 26 日

- 錯誤修復：確保指令解析器優先考慮較長的 cmd 別名。所以
如果傳送 `smile at` 且 cmd `smile` 有別名 `smile at`，則符合為
  已排序，因此結果永遠不會被解釋為帶有引數 `at` 的 `smile`。
- 錯誤修復：|| （轉義顏色tags）在幫助條目中解析得太早，
當想要一個 | 時導致顏色分隔符
- 錯誤修復：確保產生的物件 `typeclass_path` 指向 true
地點而不是別名（符合`create_object`）。
- 錯誤修復：建立選單 contrib 選單無法使用 Replace over Union 合併型別來
建置時避免與遊戲內指令發生衝突
- 功能：RPSystem contrib `sdesc` 指令現在可以檢視/刪除您的 sdesc。
- Bug 修復：更改為需要 `script obj = [scriptname|id]` 才能操作
scripts 在物件上； `script scriptname|id` 僅適用於全域 scripts。
- 檔案：新增有關 `Django-wiki` 的警告（在 wiki 教學中）僅支援
姜戈<4.0。
- 檔案：擴充套件了 `XYZGrid` 檔案字串以澄清 `MapLink` 類別本身不會
產生任何東西，孩子必須明確定義他們的原型。
- 檔案：解釋了為什麼 `AttributeProperty.at_get/set` 不會被呼叫，如果
從 `AttributeHandler` 訪問 Attribute（繞過該屬性）
- 錯誤修復：如果未設定 desc，Evtable 選項會顯示虛假空白行
- 使用修復：`teleport:` 和 `teleport_here:` 鎖定已簽入
`CmdTeleport`，但實際上並未在任何實體上設定。這些鎖現在
  對所有物件、角色、房間和出口設定預設值。

(evennia-120)=
## Evennia 1.2.0

2023 年 2 月 25 日

- 錯誤修復：`TagHandler.get` 沒有一致地轉換為字串 (aMiss-aWry)
- 錯誤修復：如果在不同情況下給出通道很難管理（aMiss-aWry）
- 功能：`logger.delete_log`功能用於從內部刪除自訂日誌
伺服器（失誤）
- 檔案：Nginx 設定 (InspectorCaracal)
- 功能：將 `fly/dive` 指令新增至 `XYZGrid` contrib 以展示對其的處理
Z 軸作為完整的 3D 網格。也修正了使用時 `XYZGrid` contrib 中的小錯誤
  使用整數而不是字串命名的 Z 軸。
- 錯誤修復：`$an()` inlinefunc 不明白如何使用以 a 開頭的“an”單字
大寫母音
- 錯誤修復：「重複的 Discord 機器人連結」錯誤的另一種情況
(InspectorCaracal)
- 修復：使 XYZGrid contrib 的 MapParserErrors 更簡潔

(evennia-111)=
## Evennia 1.1.1

2023 年 1 月 15 日

- 錯誤修正：為 nickhandler 提供更好的處理程式格式錯誤的別名正規表示式。一個
通道別名中的正規表示式相關字元可能會導致伺服器無法重新啟動。
- 功能：將`attr`關鍵字新增至`create_channel`。這允許設定
建立時頻道上的屬性，也來自 `DEFAULT_CHANNELS` 定義。

(evennia-110)=
## Evennia 1.1.0
2023 年 1 月 7 日

- 使用 `settings.NEW_ACCOUNT_REGISTRATION_ENABLED` 停止新註冊
（卡拉卡爾督察）
- 錯誤修復。

(evennia-102)=
## Evennia 1.0.2
2022 年 12 月 21 日

- 錯誤修復版本。修復了不和諧機器人重新連線的更多問題。一些文件
更新。

(evennia-101)=
## Evennia 1.0.1
2022 年 12 月 7 日

- 錯誤修復版本。主要問題是不和諧機器人的重新連線錯誤。

(evennia-100)=
## Evennia 1.0.0

2019-2022

_更改為使用 `main` 分支以遵循 github 標準。舊的 `master` 分支仍然存在
目前但不會再使用，以免在 transition._ 期間中斷安裝

在此版本中也變更為使用語意版本控制。

增加需求：Django 4.1+、Twisted 22.10+ Python 3.10、3.11。  PostgreSQL 11+。

- 新的 `drop:holds()` lock 預設值限制丟棄無意義的東西。訪問檢查
在 0.9 中向後相容預設為 True，在 1.0 中為 False
- REST API 允許您透過 HTTP 要求從外部存取資料庫物件 (Tehom)
- `Object.normalize_name` 和 `.validate_name` 加到（預設）強制 latinify
關於字元名稱並使用巧妙的 Unicode 字元避免潛在的漏洞 (trhr)
- 新的 `utils.format_grid` 用於輕鬆顯示區塊中的長專案清單。
- 使用 `lunr` 搜尋索引以獲得更好的 `help` 匹配和建議。還改善
主幫助指令的預設清單輸出。
- 已將 `content_types` 索引新增至 DefaultObject 的 ContentsHandler。 （沃倫德）
- 完成了大部分網路類，例如協定和SessionHandlers
改裝愛好者可透過 `settings.py` 更換。 （沃倫德）
- 現在可以在 `settings.py` 中替換 `initial_setup.py` 檔案以進行自訂
初始遊戲資料庫狀態。 （沃倫德）
- 新增了新的特徵contrib，從Ainneve專案轉換和擴充套件。
- 新增了新的 `requirements_extra.txt` 檔案，以便輕鬆取得所有可選依賴項。
- 將預設多重匹配語法從 1-obj, 2-obj 更改為 obj-1, obj-2。
- 使 `object.search` 支援 'stacks=0' 關鍵字 - 如果 ``>0``，則該方法將返回
N 個相同的匹配，而不是觸發多重匹配錯誤。
- 增加 `tags.has()` 方法來檢查物件是否具有 tag 或 tags（PR by ChrisLR）
- 讓IP節流使用基於Django的快取系統來實現可選的永續性（PR by strikaco）
- 將教學類別「Weapon」和「WeaponRack」重新命名為「TutorialWeapon」並
「TutorialWeaponRack」防止與 mygame 中的類別發生衝突
- 新增 `crafting` contrib，加入完整的 crafting 子系統（Griatch 2020）
- `rplanguage` contrib 現在自動將句子大寫並保留省略號 (...)。這
更改意味著句子開頭的專有名詞將不再被視為名詞。
- 使 MuxCommand `lhs/rhslist` 始終為列表，即使為空（曾經是空字串）
- 修正 UnixCommand contrib 中的拼字錯誤，其中 `help` 被指定為 `--hel`。
- 拉丁文 (la) i18n 譯 (jamalainm)
- 使 `evennia` 目錄可以在沒有 gamedir 的情況下使用以產生檔案。
- 使Scripts'計時器元件獨立於script物件刪除；現在可以啟動/停止
計時器而不刪除Script。 `.persistent` 標誌現在僅控制計時器是否存活
  重新載入 - Script 必須像其他型別分類實體一樣與 `.delete()` 一起刪除。
- 新增`utils.repeat`和`utils.unrepeat`作為TickerHandler新增/刪除的快捷方式，類似
`utils.delay` 是如何新增 TaskHandler 的捷徑。
- 重構經典的 `red_button` 範例以使用 `utils.delay/repeat` 和現代推薦
程式碼風格和範例，而不是一切都依賴 `Scripts`。
- 擴充套件`CommandTest`，能夠檢查多個訊息接收者；受到 PR 的啟發
使用者 davewiththenichat。也新增新的檔案字串。
- 新增中央`FuncParser`作為舊`parse_inlinefunc`的更強大的替代品
功能。
- Attribute/NAttribute 使用介面獲得了同質表示，兩者
`AttributeHandler` 和 `NAttributeHandler` 現在具有相同的 api。
- 加入 `evennia/utils/verb_conjugation` 以實現自動動詞變形（僅限英文）。這
對於實現演員立場表情以將字串傳送到不同的目標非常有用。
- 新版義大利文翻譯（rpolve）
- `utils.evmenu.ask_yes_no` 是一個輔助函式，可以輕鬆提出是/否問題
給使用者並回應他們的輸入。這補充了現有的 `get_input` 幫助程式。
- 如果目標名稱不包含空格，則允許傳送帶有 `page/tell` 且不帶 `=` 的訊息。
- 新的FileHelpStorage系統允許透過外部檔案新增幫助條目。
- `sethelp` 指令現在會在建立新說明型別時警告是否要隱藏其他說明型別
入口。
- 幫助指令現在使用 `view` lock 來確定 cmd/entry 是否顯示在索引和
`read` lock 判斷是否可以讀取。角色中曾經是`view`
  後者。遷移交換了這些。
- 在 `settings.PROTOTYPE_MODULES` 給出的模組中，spawner 現在將首先尋找全域性
在將模組中的所有字典載入為原型之前列出 `PROTOTYPE_LIST` 的字典。
- 使用 `channel` 指令和缺口的新通道系統。刪除了 `ChannelHandler` 和
動態建立的 `ChannelCmdSet` 的概念。
- 新增 `Msg.db_receiver_external` 欄位以允許外部字串 ID 訊息接收者。
- 為了保持一致性，已將 `app.css` 重新命名為 `website.css`。刪除了舊的 prosimii-css 檔案。
- 刪除`mygame/web/static_overrides`和-`template_overrides`，重新組織website/admin/client/api
變成一個更一致的覆蓋結構。大大擴充套件了網頁文件。
- REST API 清單檢視被縮短 (#2401)。新CSS/HTML。為 API autodoc 頁面新增 ReDoc。
- 使用更清晰的程式碼和設定更新並修復 dummyrunner。
- 使用牛津逗號使 `iter_to_str` 格式的字串更漂亮。
- 新增了 MXP 錨點 tag 以支援可點選的 Web 連結。
- 用於管理任務的新`tasks`指令以`utils.delay`開始（PR由davewiththenicehat）
- 使 `help` 索引輸出可供 webclient/MXP 的使用者端點選（PR 由 davewiththenicehat 提供）
- 自訂`evennia`啟動器指令（e.g。`evennia mycmd foo bar`）。新增指令作為可呼叫指令
接受 `*args`，如 `settings.EXTRA_LAUNCHER_COMMANDS = {'mycmd': 'path.to.callable',...}`。
- 新增 `XYZGrid` contrib，加入 x、y、z 網格座標與遊戲內地圖和
尋路。透過自訂 evennia 啟動器指令在遊戲外進行控制。
- `Script.delete` 有新的 kwarg `stop_task=True`，可用於避免
當想要將 Script 設定為停止時刪除時，無限遞迴。
- 現在在副本上執行指令以確保 `yield` 不會導致交叉。新增
`Command.retain_instance` 標誌用於重複使用相同的指令例項。
- `typeclass` 指令現在將正確搜尋目標的正確資料庫表
obj（避免錯誤地將 AccountDB-typeclass 分配給角色等）。
- 將 `script` 和 `scripts` 指令合併為一個，用於管理全域和
對像上Scripts。已將 `CmdScripts` 和 `CmdObjects` 移至 `commands/default/building.py`。
- 如果 outputfunc 以大寫字母開頭，則保留 GMCP 函式大小寫（因此 `cmd_name` -> `Cmd.Name`
但`Cmd_nAmE` -> `Cmd.nAmE`）。這有助於 e.g Mudlet 的遺留 `Client_GUI` 實施）
- 原型現在允許直接將 `prototype_parent` 設定為原型字典。
這使得動態建構模組內原型變得更加容易。
- `RPSystem contrib` 已擴充套件以支援案例，因此 /tall 變為“高個子男人”
而 /Tall 則變成「高個子男人」。如果想要舊風格，可以將其關閉。
- 更改 `EvTable` 固定高度重新平衡演演算法以在末尾填充空白行
列而不是根據單元格大小插入行（可能會被誤認為是錯誤）。
- 使用輔助方法拆分 `return_appearance` 鉤子並讓它使用模板
字串，以便更容易覆蓋。
- 將驗證問題新增至預設帳戶建立。
- 新增 `LOCALECHO` 使用者端選項，為用戶端新增伺服器端回顯
不支援這一點（對於獲取完整日誌很有用）。
- 讓 `@lazy_property` 裝飾器建立讀取/刪除保護的屬性。這是
因為它用於處理程式和e.g。 self.locks=[] 是初學者常見的錯誤。
- 使用 `$pron()` inlinefunc 在演員立場字串中加入代名詞解析
`msg_contents`。
- 更新 defauklt 網站以顯示 Telnet/SSL/SSH 連線資訊。新增
`SERVER_HOSTNAME` 設定用於 server:port 節。
- 為了保持一致性，將所有 `at_before/after_*` 掛鉤更改為 `at_pre/post_*`
跨Evennia（舊名稱仍然有效，但已棄用）
- 將 `settings.COMMAND_DEFAULT_ARG_REGEX` 預設值從 `None` 變更為正規表示式，這表示
必須用空格或 `/` 分隔 cmdname 和 args。這更符合普遍的期望。
- 將確認問題新增至 `ban`/`unban` 指令。
- 檢查 `teleport` 指令中的新 `teleport` 和 `teleport_here` lock-型別以可選
允許限制物體的傳送或傳送到特定的目的地。
- 新增 `settings.MXP_ENABLED=True` 和 `settings.MXP_OUTGOING_ONLY=True` 作為合理的預設值，
以避免玩家輸入 MXP 連結時出現已知的安全問題。
- 將瀏覽器名稱新增至`session.protocol_flags`、e.g 中的webclient `CLIENT_NAME`。
`"Evennia webclient (websocket:firefox)"` 或 `"evennia webclient (ajax:chrome)"`。
- 為了保持一致性，`TagHandler.add/has(tag=...)` kwarg 更改為 `add/has(key=...)`
與其他處理程式。
- 使 `DefaultScript.delete`、`DefaultChannel.delete` 和 `DefaultAccount.delete` 返回
bool True/False 如果刪除成功（如前面的`DefaultObject.delete`）
- `contrib.custom_gametime` 天/週/月現在總是從 1 開始（以匹配
標準日曆形式…畢竟每年沒有 0 月）。
- `AttributeProperty`/`NAttributeProperty` 允許管理屬性/NAttributes
與 Django 欄位相同的方式在 typeclasses 上。
- 如果使用非 @ 名稱，則為建置/系統指令提供 `@name` 以回退
透過另一個指令（如 `open` 和 `@open`）。如果沒有重複，@ 是可選的。
- 將舊版頻道管理指令（`ccreate`、`addcom` 等）移至 contrib
因為他們的工作現在完全由單一 `channel` 指令處理。
- 將 `examine` 指令的程式碼擴充套件為更具可擴充套件性和模組化。展示
attribute 類別和值型別（當不是字串時）。
- `AttributeHandler.remove(key, return_exception=False, category=None,...)` 已更改
到`.remove(key, category=None, return_exception=False,...)`以保持一致性。
- 新的 `command cooldown` contrib 使管理指令變得更容易
使用之間的動態冷卻時間（owllex）
- 重組`contrib/`資料夾，將所有contribs作為單獨的包放置在
子資料夾。所有匯入都需要更新。
- 使 `MonitorHandler.add/remove` 支援 `category` 用於監視屬性
帶有類別（在僅使用鍵之前，完全忽略類別）。
- 將 `create_*` 函式移至資料庫管理器，僅剩下 `utils.create`
包裝函式（與`utils.search`一致）。否則不改變 api。
- 分配 Attribute 值時加入對 `$dbref()` 和 `$search` 的支援
使用 `set` 指令。這允許分配遊戲中的真實物件。
- 新增使用 `examine` 指令檢查 `/script` 和 `/channel` 實體的功能。
- 統一管理器搜尋方法以傳回查詢集而不是清單。
- 重組單元測試以始終遵循預設設定；讓新手父母
位於遊戲目錄中以便於使用。
- 幫助使用的`Lunr`搜尋引擎排除了常用字詞；設定列表
`LUNR_STOP_WORD_FILTER_EXCEPTIONS` 可以擴充以確保包含常用名稱。
- 將 `.deserialize()` 方法新增到 `_Saver*` 結構以完全幫助
將結構與資料庫解耦，無需單獨匯入。
- 新增 `run_in_main_thread` 作為那些想要編寫伺服器程式碼的幫助者
從網頁檢視來看。
- 更新 `evennia.utils.logger` 以使用 Twisted 的新日誌記錄 API。 Evennia API 沒有變化
除了現在可以使用更多標準別名 logger.error/info/exception/debug 等。
- 將 `type/force` 預設為 `update`-模式而不是 `reset` 模式並新增更多詳細資訊
使用重置模式時發出警告。
- Attribute儲存支援defaultdics (Hendher)
- 將 ObjectParent mixin 新增到預設遊戲資料夾模板中，作為一個簡單的現成的
輕鬆覆寫所有 ObjectDB 繼承物件上的功能的方法。
  來源位置，模仿 `at_pre_move` 鉤子的行為 - 返回 False 將中止移動。
- 新增 `TagProperty`、`AliasProperty` 和 `PermissionProperty` 來分配這些
資料的方式與 django 欄位類似。
- 物件上的新 `at_pre_object_receive(obj, source_location)` 方法。被召喚
目的地，模仿 `at_pre_move` 鉤子的行為 - 返回 False 將中止移動。
- 物件上的新 `at_pre_object_leave(obj, destination)` 方法。被召喚
- db pickle-serializer 現在檢查方法 `__serialize_dbobjs__` 和 `__deserialize_dbobjs__`
允許自訂打包/解包巢狀的 dbobj，允許儲存在 Attribute 中。
- 最佳化 rpsystem contrib 效能。重大變更：`.get_sdesc()` 將
如果未設定 sdesc，現在返回 `None` 而不是 `.db.desc`；鉤子中的後備（inspectorCaracal）
- 重新設計了 text2html 解析器以避免狀態顏色 tags 的問題 (inspectorCaracal)
- 簡化的 `EvMenu.options_formatter` 鉤子使用 `EvColumn` 和 f 字串 (inspectorcaracal)
- 批次程式碼中允許 `# CODE`、`# HEADER` 等以及 `#CODE`/`#HEADER`
檔案 - 這對於黑色絨毛效果更好。
- 新增了 `move_type` str kwarg 到 `move_to()` 呼叫，可選擇標識型別
正在完成的移動（「傳送」、「下船」、「給予」等）。 （沃倫德）
- 使 RPSystem contrib 訊息呼叫將 `pose` 或 `say` 作為訊息-`type` 傳遞以用於
e.g。 webclient 在需要時進行窗格過濾。 （沃倫德）
- 增加 `Account.uses_screenreader(session=None)` 作為快捷方式
尋找使用者是否使用螢幕閱讀器（並相應地調整顯示）。
- 修正了`cmdset.remove()`中`key`無法刪除指令的錯誤，
儘管醫生建議可以（ChrisLR）
- 新的 contrib `name_generator` 用於建立隨機的基於現實世界或幻想的名稱
基於語音規則。
- 在屬性中啟用 dict 子類別的正確序列化 (aogier)
- `object.search` 模糊配對現在使用 `icontains` 而不是 `istartswith`
更符合其他地方的搜尋工作方式 (volund)
- `.at_traverse` 鉤子現在接收 `exit_obj` kwarg，連結回
退出觸發鉤子（volund）
- Contrib `buffs` 用於管理臨時和永久 RPG 狀態增益效果 (tegiminis)
- 在所有其他啟動掛鉤之前呼叫新的 `at_server_init()` 掛鉤
啟動模式。用於更通用的覆蓋（volund）
- 新的 `search` lock 型別用於完全隱藏物件以使其不被發現
`DefaultObject.search` (`caller.search`) 方法。 (CloudKeeper)
- 將設定 `MULTISESSION_MODE` 更改為現在僅控制 sessions，而不控制多少
角色可以同時被傀儡。現在新的設定可以控制這一點。
- 新增設定`AUTO_CREATE_CHARACTER_WITH_ACCOUNT`，一個布林值決定是否
新帳戶還應該獲得匹配的字元（舊版 MUD 樣式）。
- 新增設定 `AUTO_PUPPET_ON_LOGIN`，布林值決定是否應該
自動傀儡連線上的最後一個/可用字元（舊版 MUD 樣式）
- 新增設定 `MAX_NR_SIMULTANEUS_PUPPETS` - 帳戶有多少個木偶
可以同時執行。用於限制多人遊戲。
- 使設定 `MAX_NR_CHARACTERS` 與上面的新設定更好地互動。
- 允許 `$search` funcparser func 搜尋 tags 並接受 kwargs 以獲取更多資訊
強大的搜尋傳遞到常規搜尋功能。
- `spawner.spawn` 和連結方法現在有一個 kwarg `protfunc_raise_errors`
（預設 True）停用格式錯誤/未找到的 protfunc 上的嚴格錯誤
- 透過快取擁有許多基於 DB- 的原型時提高搜尋效能。
- 刪除 `evennia.prototypes.spawner.spawn` 的 `return_parents` kwarg，因為它
效率低且未使用。
- 使所有資料庫的所有 id 欄位都為 BigAutoField。 （歐萊克斯）
- `EvForm` 重構。新的 `literals` 對映，用於文字對映到
主模板（e.g.用於單字元替換）。
- `EvForm` `cells` kwarg 現在接受自訂格式選項的 `EvCells`
（主要用於自訂align/valign）。 `EvCells` 現在使用 `utils.justify`。
- `utils.justify` 現在支援 `align="a"` （絕對對齊。這可以保持
給定的左縮排，但裁切/填滿寬度。用於EvCells。
- `EvTable` 現在支援直接將 `EvColumn`s 作為清單傳遞，(`EvTable(table=[colA,colB])`)
- 將 `tags=` 搜尋條件新增至 `DefaultObject.search`。
- 增加 `AT_EXIT_TRAVERSE` 訊號，在穿過出口時觸發。
- 增加 Evennia 和 Discord 頻道之間的整合（PR 由 Inspector Cararacal 完成）
- 支援使用由 Evennia 驅動的 Godot 使用者端（PR by ChrisLR）
- 新增了德語翻譯（由 Zhuraj 修補）

(evennia-095)=
## Evennia 0.9.5

> 2019-2020
> 釋出時間：2020 年 11 月 14 日。
> 過渡版本，包括新的檔案系統。

從開發向後移植：Python 3.8、3.9 支援。 Django 3.2+ 支援，Twisted 21+ 支援。

- `is_typeclass(obj (Object), exact (bool))` 現在預設為exact=False
- `py` 指令現在重新路由標準輸出以在遊戲使用者端中輸出結果。 `py`
不含引數啟動完整的互動式 Python 控制檯。
- Webclient 預設為單一輸入窗格而不是兩個。現在預設沒有幫助彈出視窗。
- Webclient修復提示顯示
- Webclient多媒體支援透過以下方式轉發影像、影片和聲音
`.msg(image=URL)`, `.msg(video=URL)`
  和`.msg(audio=URL)`
- 新增西班牙文翻譯 (fermuch)
- 展開 `GLOBAL_SCRIPTS` 容器以始終啟動 scripts 並包含所有
全域 scripts 無論它們是如何建立的。
- 更改設定以始終使用列表而不是元組，以使其可變
設定更容易新增。 (#1912)
- 為指定 mudinfo 通道進行新的 `CHANNEL_MUDINFO` 設定
- 使`CHANNEL_CONNECTINFO`採用完整的通道定義
- 使 `DEFAULT_CHANNELS` 清單自動建立頻道在重新載入時遺失
- Webclient `ANSI->HTML` 解析器已更新。 Webclient 線寬從 1.6em 改為 1.1em
更好地使 ANSI 圖形看起來與第三方用戶端相同
- 如果沒有則`AttributeHandler.get(return_list=True)`將回傳`[]`
屬性而不是`[None]`。
- 刪除 `pillow` 要求（特別是在使用映像欄位時安裝）
- 加入簡體韓文翻譯（aceamro）
- 如果設定包含對生產不安全的值，則在 `start -l` 上顯示警告。
- 使用黑色使程式碼自動格式化。
- 使預設 `set` 指令能夠編輯巢狀結構（PR 由 Aaron McMillan 撰寫）
- 允許使用 `make test` 從核心儲存庫執行 Evennia 測試套件。
- 從 `TickerHandler.add` 返回 `store_key` 並將 `store_key` 作為 kwarg 加入
`TickerHandler.remove` 方法。這使得管理程式碼變得更加容易。
- EvMore 自動對齊現在預設為 False，因為這對所有型別都有效
文字（例如表格）。新的 `justify` 布林值。舊的 `justify_kwargs` 仍然存在
  但現在僅用於將額外的 kwargs 傳遞到 justify 函式中。
- EvMore `text` 引數現在也可以是清單或查詢集。查詢集將是
切片以僅傳回每頁所需的資料。
- 提高大型資料集上 `find` 和 `objects` 指令的效能 (strikaco)
- 新的 `CHANNEL_HANDLER_CLASS` 設定允許完全替換 ChannelHandler。
- 使 `py` 互動模式支援常規 quit() 和更詳細。
- 讓 `Account.options.get` 接受 `default=None` kwarg 模仿 get 的其他用法。放
新的 `raise_exception` 布林值（如果在遺失的金鑰上咆哮以提高 KeyError）。
- 已將未修改的 `Command` 和 `MuxCommand` `.func()` 的行為移至新的
`.get_command_info()` 方法更容易過載和存取。 （沃倫德）
- 刪除了未使用的 `CYCLE_LOGFILES` 設定。新增`SERVER_LOG_DAY_ROTATION`
和 `SERVER_LOG_MAX_SIZE`（以及 PORTAL 的等效項）來控制日誌輪替。
- 增加了 `inside_rec` lockfunc - 如果房間被鎖定，正常的 `inside()` lockfunc 將
失敗e.g。對於你的庫存物件（因為它們的位置是你），而這會過去。
- 如果沒有給出引數，RPSystem contrib 的 CmdRecog 現在將列出所有識別。還有多個
錯誤修復。
- 取消設定時刪除 `dummy@example.com` 作為預設帳戶電子郵件，字串不再
Django 要求的。
- 修復了`spawn`，使更新現有原型/物件工作得更好。新增`/raw`開關
`spawn` 指令提取原始原型字典以進行手動編輯。
- `list_to_string` 現在是 `iter_to_string`（但舊名稱仍用作舊別名）。它將
現在接受任何輸入，包括生成器和單一值。
- EvTable 現在應該正確處理其中包含更廣泛的亞洲字元的列。
- 將 Twisted 要求更新為 >=2.3.0 以消除安全漏洞
- 增加 `$random` inlinefunc，支援 minval、maxval 引數，可以是整數和浮點數。
- 新增 `evennia.utils.inlinefuncs.raw(<str>)` 作為輔助函式以轉義字串中的行內函數。
- 如果 `obj.move_to` 回傳 `False`，則使 CmdGet/Drop/Give 給予正確的錯誤。
- 使 `Object/Room/Exit.create` 的 `account` 引數可選。如果沒有給出，將設定許可權
物件本身的許可權（以及正常的管理員/開發許可權）。
- 使 `INLINEFUNC_STACK_MAXSIZE` 預設在 `settings_default.py` 中可見。
- 更改 `ic` 尋找木偶的方式；非特權使用者將使用 `_playable_characters` 清單作為
對於候選人，Builders+ 將使用清單、本地搜尋，如果未找到匹配項，則僅使用全域搜尋。
- 使 `cmd.at_post_cmd()` 始終在 `cmd.func()` 之後執行，即使後者使用延遲
與產量。
- `EvMore` 支援資料庫查詢和 django 分頁器，並且更容易覆蓋自訂
分頁（e.g。為每一頁建立EvTables，而不是分割一個表）
- 使用`EvMore pagination`，顯著提高`spawn/list`和`scripts`清單的效能
（顯示 1000 多個原型時速度提高 100 倍/scripts）。
- `EvMenu` 現在使用更符合邏輯的名稱 `.ndb._evmenu` 而不是 `.ndb._menutree` 來儲存自己。
兩者仍然可以向後相容，但 `_menutree` 已被棄用。
- `EvMenu.msg(txt)` 新增為向使用者傳送文字的中心位置，使其更容易覆蓋。
預設 `EvMenu.msg` 使用 OOB type="menu" 傳送，用於 OOB 和 webclient 窗格重定向。
- 新的 EvMenu 模板系統，無需太多程式碼即可快速建立更簡單的 EvMenus。
- 新增 `Command.client_height()` 方法以匹配現有的 `.client_width` (stricako)
- 在 `session.protocol_flags` 中包含更多 Web 使用者端資訊。
- 修復了多重匹配情況 - 不允許在以下情況下查詢/列出 3-box 的多重匹配
位置上只有兩個盒子。
- 修復TaskHandler，並提供適當的延期回報/取消能力等（PR by davewiththenicehat）
- 新增 `PermissionHandler.check` 方法進行直字串永久檢查，無需鎖定字串。
- 新增 `evennia.utils.utils.strip_unsafe_input` 以從使用者輸入中刪除 html/newlines/tags。這
`INPUT_CLEANUP_BYPASS_PERMISSIONS` 是繞過此安全剝離的許可權清單。
- 使預設 `set` 和 `examine` 指令識別 Attribute 類別。

(evennia-09)=
## Evennia 0.9

> 2018-2019
> 2019 年 10 月發布

(distribution)=
### 分配

- 新要求：Python 3.7（刪除了 py2.7 支援）
- 薑戈2.1
- 扭曲19.2.1
- Autobahn websockets（刪除了舊的 tmwx）
- Docker 映像已更新

(commands)=
### 指令

- 從所有預設指令中刪除 `@`-字首（字首仍然有效，可選）
- 刪除了預設的 `@delaccount` 指令，合併為 `@account/delete`。新增確認
問題。
- 新增的 `@force` 指令以使另一個物件執行指令。
- 將 Portal 正常運作時間新增至 `@time` 指令。
- 讓 `@link` 指令先進行本機搜尋，然後再進行全域搜尋。
- 讓預設的 Unloggedin-look 指令尋找可呼叫的可選 `connection_screen()`
`mygame/server/conf/connection_screen.py`。這允許更靈活的歡迎螢幕
  是即時計算的。
- 當在 webclient 中檢視時，`@py` 指令現在預設在其輸出中轉義 html tags。
使用新的 `/clientraw` 開關來取得舊行為（問題＃1369）。
- 更短、資訊更豐富、動態的指令變數清單（如果沒有）
在子指令類別中設定 func() 。
- 新的指令輔助方法
  - `.client_width()` 傳回執行指令的 session 的用戶端寬度。
  - `.styled_table(*args, **kwargs)` 傳回依使用者選項設定樣式的格式化 evtable
  - `.style_header(*args, **kwargs)` 建立樣式標題條目
  - `.style_separator(*args, **kwargs)`“分隔符
  - `.style_footer(*args, **kwargs)` "頁尾

(web)=
### 網路

- 將 webclient 從舊 txws 版本更改為使用更多受支援/功能豐富的 Autobahn websocket 庫

(evennia-game-index)=
#### Evennia遊戲索引

- 使 Evennia 遊戲索引用戶端成為核心的一部分 - 現在從設定檔設定（舊設定
需要移動）
- `evennia connections` 指令啟動一個嚮導，幫助您將遊戲連線到遊戲索引。
- 遊戲索引現在接受沒有公共 telnet/webclient 資訊的遊戲（對於早期原型）。

(new-golden-layout-based-webclient-ui-friarzen)=
#### 基於新的黃金佈局 Webclient UI (@friarzen)
- 特徵
  - 更圓滑的行為和更專業的外觀
  - 允許在任何網格位置進行選項卡切換以及按一下和拖曳窗格
  - 重新命名選項卡、資料 tags 分配和輸出型別現在都是簡單的每窗格選單
  - 任意數量的輸入窗格，具有單獨的歷史記錄
  - 按鈕 UI（預設在 JS 中停用）

(webdjango-standard-initiative-strikaco)=
#### Web/Django 標準倡議 (@strikaco)
- 特徵
  - 新增一系列基於 Web 的表單和基於類別的通用檢視
    - 帳戶
      - 註冊 - 增強註冊功能；允許選擇性收集電子郵件地址
      - 表單 - 新增通用 Django 表單，用於從網路建立帳戶
    - 人物
      - 建立 - 經過身份驗證的使用者可以從網站建立新角色（需要關聯表格）
      - 詳細資訊 - 經過身份驗證和授權的使用者可以檢視有關角色的選定詳細資訊
      - 列表 - 經過驗證和授權的使用者可以瀏覽所有字元的列表
      - 管理 - 經過身份驗證的使用者可以從網路上編輯或刪除擁有的角色
      - 表單 - 新增通用 Django 表單，用於從網路建立角色
    - 頻道
      - 詳細資訊 - 授權使用者可以從網路檢視頻道日誌
      - 列表 - 授權使用者可以瀏覽所有頻道的列表
    - 幫助條目
      - 詳細資訊 - 授權使用者可以從網路檢視幫助條目
      - 列表 - 授權使用者可以從網路瀏覽所有說明條目的列表
  - 導覽列更改
    - 角色 - 連結到角色列表
    - 頻道 - 連結到頻道列表
    - 幫助 - 幫助條目列表的連結
    - 木偶戲
      - 使用者可以在網站的上下文中操縱自己的角色
    - 下拉式選單
      - 建立角色的連結
      - 管理角色的連結
      - 連結到快速選擇人偶
      - 連結到密碼更改工作流程
- 功能
  - 將 Bootstrap 更新至 v4 穩定版本
  - 允許使用 Django Messages 框架在瀏覽器中與使用者通訊
  - 作為 Django 中介軟體實現 webclient/網站 `_shared_login` 功能
  - 「account」和「puppet」被加入到經過驗證的使用者的所有請求上下文中
  - 為所有 Web 檢視新增單元測試
- 化妝品
  - 美化 Django「忘記密碼」工作流程（需要 SMTP 才能實際運作）
  - 美化 Django「更改密碼」工作流程
- 錯誤修正
  - 修正了登入頁面上未顯示錯誤訊息的錯誤
  - 從管理中刪除 strvalue 欄位；作為一個最佳化領域，這裡沒有任何意義
    for internal use.

(prototypes)=
### 原型

- `evennia.prototypes.save_prototype`現在將原型視為正常
引數 (`prototype`) 而不必將其指定為 `**prototype`。
- `evennia.prototypes.search_prototype` 有一個新的 kwarg `require_single=False`
如果查詢給出 0 或 >1 個結果，則會引發 KeyError 異常。
- `evennia.prototypes.spawner` 現在可以透過傳遞 `prototype_key` 來生成

(typeclasses)=
### Typeclasses

- 在所有 typeclasses 上新增方法，特別適合來自網站/管理員的物件處理：
  + `web_get_admin_url()`：傳回管理後端物件詳細資料頁面的路徑。
  + `web_get_create_url()`：返回網站上typeclass'建立頁面的路徑（如果已實現）。
  + `web_get_absolute_url()`：返回網站上物件詳細資訊頁面的路徑（如果已實現）。
  + `web_get_update_url()`：返回網站上物件更新頁面的路徑（如果已實現）。
  + `web_get_delete_url()`：返回網站上物件刪除頁面的路徑（如果已實現）。
- 所有 typeclasses 都有新的輔助類方法 `create`，其中包含有用的功能
過去嵌入在相應的 `@create` 或 `@connect` 指令中。
- DefaultAccount 現在有了新的類別方法，實現了許多先前在 unloggedin 中實現的功能
指令（現在可以在類別上自訂這些指令）：
  + `is_banned()`：檢查給定的使用者名稱或IP是否被禁止。
  + `get_username_validators`：傳回用於使用者名稱驗證的驗證器清單（請參閱
    `settings.AUTH_USERNAME_VALIDATORS`)
  + `authenticate`：檢查給定使用者名稱/密碼的方法。
  + `normalize_username`：標準化名稱，以便（對於 Unicode 環境）使用者無法透過視覺上相似的 Unicode 字元替換選定字元來模仿現有使用者名稱。
  + `validate_username`：基於預先定義的 Django 驗證器驗證使用者名稱的機制。
  + `validate_password`：基於預先定義的 Django 驗證器驗證密碼的機制。
  + `set_password`：使用驗證檢查將密碼套用至帳戶。
- `AttributeHandler.remove` 和 `TagHandler.remove` 現在可用於按類別刪除。如果兩者都不是
     key nor category is given, they now work the same as .clear().

(protocols)=
### 協定

- 支援`Grapevine` MUD-聊天網路（支援「頻道」）

(server)=
### 伺服器

- 轉換 ServerConf 模型以將其值儲存為 Picklefield（與
    Attributes) instead of using a custom solution.
- OOB：新增對 MSDP LIST、REPORT、UNREPORT 指令的支援（重新對應到 `msdp_list`，
`msdp_report`、`msdp_unreport`、行內函數）
- 將 `evennia.ANSIString` 加到平面 API。
- Server/Portal 日誌檔案現在會迴圈到 `server_.log_19_03_08_` 形式的名稱而不是 `server.log___19.3.8`，保留
unix 檔案排序順序。
- Django 為重要事件發出火訊號：Puppet/Unpuppet、物件建立/重新命名、登入、
登出、登入失敗、中斷連線、帳戶建立/重新命名

(settings)=
### 設定

- `GLOBAL_SCRIPTS` - 定義全域 scripts 的 typeclasses 的字典以儲存在新的上
`evennia.GLOBAL_SCRIPTS` 容器。這些將在 Evennia 啟動時自動啟動，並且始終
  存在。
- `OPTIONS_ACCOUNTS_DEFAULT` - 帶有選項預設值和選項類別的選項字典
- `OPTION_CLASS_MODULES` - 代表帳戶選項的類，採用特殊形式
- `VALIDATOR_FUNC_MODULES` - （通用）文字驗證器函式，用於驗證輸入
是在一個特定的表格上。

(utilities)=
### 公用事業

- `evennia` 啟動器現在可以完全處理所有 django-admin 指令，例如並行執行測試。
- `evennia.utils.create.account` 現在也採用 `tags` 和 `attrs` 關鍵字。
- `evennia.utils.interactive`裝飾器現在可以允許您使用yield(secs)來暫停操作
在任何函式中，而不僅僅是在 Command.func 中。同樣，response = Yield(question) 也可以
  如果修飾函式有引數或 kwarg `caller`。
- 增加了更多單元測試。
- 將 `evennia.set_trace` 的引數順序交換為 `set_trace(term_size=(140, 40), debugger='auto')`
因為大小更有可能在指令列上更改。
- `utils.to_str(text, session=None)` 現在充當舊的 `utils.to_unicode`（已刪除）。
這會轉換為 str() 型別（而不是像 Evennia 0.8 中那樣轉換為位元組字串），嘗試不同的
  編碼。該函式還將強制將傳遞給它的任何物件轉換為字串（因此
  `force_string` 標誌已刪除並假定始終設定）。
- `utils.to_bytes(text, session=None)` 取代舊的 `utils.to_str()` 功能並進行轉換
str 到位元組。
- `evennia.MONITOR_HANDLER.all` 現在採用關鍵字引數 `obj` 僅擷取來自該特定的監視器
物件（而不是整個處理程式中的所有監視器）。
- 支援在指令檔案字串中新增 `\f` 以強制在 EvMore 處放置分頁符號。
- 驗證函式現在新增了標準 API 以統一使用者輸入驗證。
- 新增了選項類，使儲存使用者選項變得更容易、更順暢。
- 新增`evennia.VALIDATOR_CONTAINER` 和`evennia.OPTION_CONTAINER` 來載入這些。

(new-contribs)=
### 新Contribs

- Evscaperoom - 一個完整的益智引擎，用於在 Evennia 中製作多人逃脫室。用來製作
MUD-Coder's Guild 2019 年 Game Jam 主題為「One Room」的參賽作品，排名第一。
- Evennia 遊戲索引用戶端不再是 contrib - 移至伺服器核心並設定了新的
設定`GAME_INDEX_ENABLED`。
- `extended_room` contrib 看到了一些向後不相容的重構：
  + 現在所有指令都以 `CmdExtendedRoom` 開頭。所以之前是`CmdExtendedLook`，現在
     it's `CmdExtendedRoomLook` etc.
  + `detail` 指令已從 `desc` 指令中分離出來，現在是一個新的獨立指令
     `CmdExtendedRoomDetail`.  This was done to make things easier to extend and to mimic how the detail
     command works in the tutorial-world.
  + `detail` 指令現在也支援刪除詳細資料（如教學世界版本）。
  + 新的 `ExtendedRoomCmdSet` 包括所有擴充套件房間指令，現在是推薦的方式
     to install the extended-room contrib.
- 重新設計了 `menu_login` contrib 以使用最新的 EvMenu 標準。現在也支援訪客登入。
- 郵件 contrib 已重構為具有用於 OOC+IC 郵件的可選指令類別 `CmdMail`（新增
    to the CharacterCmdSet and `CmdMailCharacter` for IC-only mailing between chars (added to CharacterCmdSet)

(translations)=
### 翻譯

- 簡體中文，由使用者 MaxAlex 提供。


(evennia-08)=
## Evennia 0.8

> 2017-2018
> 2018 年 11 月發布

(requirements)=
### 要求

- 要求提高到 Django 1.11.x、Twisted 18 和 Pillow 5.2.0
- 新增 `inflect` 依賴項以自動複數物件名稱。

(serverportal)=
### 伺服器/Portal

- 刪除了`evennia_runner`，完全重構了`evennia_launcher.py`（「evennia」程式）
具有不同的功能）。
- Portal/Server 現在都是獨立程式（易於作為守護程式執行）
- 將 Portal 設為 AMP 伺服器以啟動/重新啟動伺服器（AMP 用戶端）
- 動態日誌記錄現在使用 `evennia -l` 而不是透過互動模式進行。
- 使 AMP 免受錯誤連線埠上的錯誤 HTTP 請求的影響（傳回錯誤訊息）。
- `evennia istart` 選項將在前臺（互動）模式下啟動/切換伺服器，並在其中記錄
到終端並且可以使用 Ctrl-C 停止。使用`evennia reload`，或在遊戲中重新載入，將會
  將伺服器返回正常的守護程式操作。
- 為了驗證密碼，請使用安全的 Django 密碼驗證後端而不是自訂的 Evennia 後端。
- 別名 `evennia restart` 與 `evennia reload` 意義相同。

(prototype-changes)=
### 原型變更

- 新的 OLC 從 `olc` 指令開始，用於在選單中載入/儲存/操作原型。
- 將 evennia/utils/spawner.py 與所有新的一起移動到新的 evennia/prototypes/ 中
圍繞原型的功能。
- 新增了一種新形式的原型 - 資料庫儲存的原型，可在遊戲中編輯。舊的，
模組建立的原型仍然是唯讀原型。
- 所有原型都必須有一個金鑰 `prototype_key` 來識別清單中的原型。這是
檢查為伺服器唯一。在模組中建立的原型將使用它們的全域變數名稱
  如果沒有給出 `prototype_key` 則分配給。
- 原型欄位 `prototype` 已重新命名為 `prototype_parent` 以避免混合術語。
- 所有原型必須定義`typeclass` 或`prototype_parent`。如果使用
`prototype_parent`、`typeclass` 必須在繼承鏈中的某個位置定義。這是一個
  從 Evennia 0.7 更改，允許「混合」原型而無需 `typeclass`/`prototype_key`。至
  現在製作一個mixin，給它一個預設的typeclass，例如`evennia.objects.objects.DefaultObject`，然後
  根據需要覆蓋孩子。
- 使用原型產生物件會自動為其分配一個新的tag，命名與
`prototype_key` 和類別 `from_prototype`。
- 生成指令已擴充套件為在一行上接受完整的原型。
- spawn 指令使用 /save 開關來儲存定義的原型及其金鑰
- 指令spawn/menu現在將啟動OLC（OnLine建立）選單來載入/儲存/編輯/生成原型。

(evmenu)=
### EvMenu

- 新增了 `EvMenu.helptext_formatter(helptext)` 以允許自訂每個節點幫助的格式。
- 新增了 `evennia.utils.evmenu.list_node` 裝飾器，用於將 EvMenu 節點轉換為多頁清單。
- `goto` 可呼叫選項會傳回 None （而不是下一個節點的名稱）現在將重新執行
當前節點而不是失敗。
- 更好地處理節點內語法錯誤。
- 改進預設文字/幫助文字格式化程式的縮排。右側去除空格。
- 建立選單時新增 `debug` 選項 - 這會關閉永續性並使 `menudebug`
指令可用於檢查目前選單狀態。


(webclient)=
### Webclient

- Webclient 現在使用外掛系統從 html 檔案注入新元件。
- 分割視窗 - 將輸入欄位劃分為任意數量的水平/垂直窗格，
為它們分配不同型別的伺服器訊息。
- 大量清理和錯誤修復。
- 熱按鈕外掛（friarzen）（預設為停用）。

(locks)=
### 鎖具

- 新功能`evennia.locks.lockhandler.check_lockstring`。這允許檢查一個物件
針對任意鎖定字串，無需先將 lock 儲存在物件上。
- 新函式 `evennia.locks.lockhandler.validate_lockstring` 允許獨立驗證
鎖弦的。
- 新函式 `evennia.locks.lockhandler.get_all_lockfuncs` 給予一個字典 {"name": lockfunc}
所有可用的 lock 函式。這對於動態清單很有用。


(utils)=
### 實用程式

- 新增了新的 `columnize` 函式，可以輕鬆地將文字拆分為多列。此時它
然而，對於 ansi 彩色文字來說效果不太好。
- 使用新的 `baseline_index` kwarg 擴充套件 `dedent` 函式。這允許強制所有線路
給定行給出的縮排，無論其他行是否已經是 0 縮排。
  這消除了原始 `textwrap.dedent` 的問題，該問題只會減少到最少
  文字的縮排部分。
- 新增了 `exit_cmd` 到 EvMore 尋呼機，以允許在離開尋呼機時呼叫指令（e.g.'look'）。
- `get_all_typeclasses` 將為所有可用的 typeclasses 返回字典 `{"path": typeclass,...}`
在系統中。這由新的 `@typeclass/list` 子指令使用（對於建構器等有用）。
- `evennia.utils.dbserialize.deserialize(obj)` 是一個新的輔助函式，用於「完全」斷開連線
從資料庫的 Attribute 還原的可變值。這將轉換所有巢狀的`_Saver*`
  類別與其普通 Python 對應類別的關係。

(general)=
### 一般的

- 開始建立 `CHANGELOG` 以更詳細地列出功能。
- Docker 映像 `evennia/evennia:develop` 現已自動構建，追蹤開發分支。
- 預設房間中多個物件的變形和分組（一個盒子，三個盒子）
- `evennia.set_trace()` 現在是在 Evennia 事件迴圈中的一行上啟動 pdb/pudb 的捷徑。
- 預設刪除了 `MULTISESSION_MODE` `0` 和 `1` 的 `MAX_NR_CHARACTERS=1` 強制執行。
- 新增 `evennia.utils.logger.log_sec` 用於記錄與安全相關的訊息（在日誌中標記為 SS）。

(more-contribs)=
### 更多Contribs

- `Auditing` (Johnny)：出於安全目的記錄和過濾伺服器輸入/輸出
- `Build Menu` (vincent-lg)：新的 @edit 指令用於在選單中編輯物件屬性。
- `Field Fill` (Tim Ashley Jenkins)：包裝 EvMenu 以建立可提交的表單。
- `Health Bar` (Tim Ashley Jenkins)：輕鬆建立彩色條/儀表。
- `Tree select` (Fluttersprite)：包裹 EvMenu 以從字串建立常見型別的選單。
- `Turnbattle suite`（蒂姆·阿什利·詹金斯）- 舊的 `turnbattle.py` 已移入其自己的位置
`turnbattle/` 打包並重新設計了許多不同風格的戰鬥系統：
 - `tb_basic` - 基本回合戰系統，具有先攻/回合順序攻擊/防禦/傷害。
 - `tb_equip` - 新增武器和盔甲、揮舞、準確性修改器。
 - `tb_items` - 透過具有條件/狀態效果的物品使用來擴充套件`tb_equip`。
 - `tb_magic` - 透過施法延長`tb_equip`。
 - `tb_range` - 增加抽象定位和移動系統。
 - `extended_room` contrib 看到了一些向後不相容的重構：
   - 現在所有指令都以 `CmdExtendedRoom` 開頭。所以之前是`CmdExtendedLook`，現在
     it's `CmdExtendedRoomLook` etc.
   - `detail` 指令已從 `desc` 指令中分離出來，現在是一個新的獨立指令
     `CmdExtendedRoomDetail`.  This was done to make things easier to extend and to mimic how the detail
     command works in the tutorial-world.
   - `detail` 指令現在也支援刪除詳細資料（如教學世界版本）。
   - 新的 `ExtendedRoomCmdSet` 包括所有擴充套件房間指令，現在是推薦的方式
     to install the extended-room contrib.
- 更新並清理現有的 contribs。


(internationalization)=
### 國際化

- 使用者 ogotai 的波蘭文翻譯

(overview-changelogs)=
# 概述-變更日誌

> 這些是我們使用正式版本號碼之前的變更日誌。

(sept-2017)=
## 2017 年 9 月：
釋放Evennia0.7；升級到 Django 1.11，將 'Player' 更改為
“帳戶”，重新設計網站範本和一系列其他更新。
有關更改內容以及如何遷移的資訊可在此處找到：
https://groups.google.com/forum/#!msg/evennia/0JYYNGY-NfE/cDFaIwmPBAAJ

(feb-2017)=
## 2017 年 2 月：
建立新的開發分支，領先 Evennia 0.7。

(dec-2016)=
## 2016 年 12 月：
許多錯誤修復和貢獻者的顯著增加。單元測試覆蓋率
以及 PEP8 採用和重構。

(may-2016)=
## 2016 年 5 月：
Evennia 0.6 完全重新設計的帶外系統，使得
訊息路徑完全靈活並且圍繞輸入/輸出函式建構。
一個全新的 webclient，分為 evennia.js 庫和
gui 庫，使其更容易自訂。

(feb-2016)=
## 2016 年 2 月：
增加了新的 EvMenu 和 EvMore 實用程式，更新了 EvEdit 並進行了清理
很多批次指令功能。開始新的開發分支的工作。

(sept-2015)=
## 2015 年 9 月：
Evennia 0.5。合併開發分支，實現完整的庫格式。

(feb-2015)=
## 2015 年 2 月：
目前正在開發/分支中開發。已將 typeclasses 移至使用
django 的代理功能。將 Evennia 資料夾佈局變更為
帶有獨立啟動器的庫格式，準備製作
'evennia' pypy 套件並使用版本控制。我們將要發布的版本
合併可能是 0.5。還有一個擴充的工作
測試結構和使用執行緒進行儲存。我們現在也
使用 Travis 進行自動建置檢查。

(sept-2014)=
## 2014 年 9 月：
更新到 Django 1.7+，這意味著 South 依賴項被刪除並且
最低 Python 版本升至 2.7。 MULTISESSION_MODE=3 已新增
並且使用最新的網路定製系統進行了徹底改造
Django 的功能。否則，主要是錯誤修復和
當我們習慣後，實現各種較小的功能請求
到github。許多新使用者出現了。

(jan-2014)=
## 2014 年 1 月：
已將 Evennia 專案從 Google 程式碼移至 github.com/evennia/evennia。

(nov-2013)=
## 2013 年 11 月：
將內部 webserver 移至伺服器並新增了對
帶外協議（最初為 MSDP）。這巨大的發展推動
也意味著修復和清理屬性的處理方式。
增加了Tags，以及適當的許可權處理程式、缺口
和別名。

(may-2013)=
## 2013 年 5 月：
讓玩家能夠同時控制多個角色
時間，透過MULTISESSION_MODE=2加法。這導致了很多
伺服器的內部變更。

(oct-2012)=
## 2012 年 10 月：
將 Evennia 從 Modified Artistic 1.0 授權更改為 more
標準和寬鬆的 BSD 許可證。許多更新和錯誤修復
更多的人開始以新的方式使用它。許多新的快取和
加速。

(march-2012)=
## 2012 年 3 月：
Evennia 的 API 已稍微更改和簡化，因為
基本模組已從 game/gamesrc 中刪除。相反，管理員是
鼓勵在 game/gamesrc/ 下明確建立新模組
他們想要實現他們的遊戲 - gamesrc/ 預設為空
除了包含要使用的範本檔案的範例資料夾之外
這個目的。我們還新增了 `ev.py` 檔案，實現了一個新的、扁平的
API。  正在努力增加對特定泥漿遠端登入的支援
擴充套件，特別是 MSDP 和 GMCP 帶外擴充套件。  上
社群方面，evennia 的開發部落格已在星球上啟動並連結
Mud-dev 聚合器。

(nov-2011)=
## 2011 年 11 月：
在建立了幾個不同的概念驗證遊戲系統之後（在
contrib 和私下）以及測試很多東西以確保
實施基本上是合理的，我們宣佈 Evennia 超出
阿爾法。誠然，這可以根據你的意思來決定——
開發工作仍然繁重，但問題清單處於歷史最低水平
隨著人們嘗試不同的事情，伺服器正在慢慢穩定
與它。所以它就是貝塔！

(aug-2011)=
## 2011 年 8 月：
將 Evennia 拆分為兩個程式：Portal 和 Server。經過很多
努力讓記憶體中的程式碼重新載入工作，很明顯這一點
不是Python的強項－它不可能捕獲所有異常，
特別是在像這樣的非同步程式碼中。  嘗試這樣做會導致
駭客、古怪和不穩定的程式碼。透過 Portal-伺服器拆分，
當玩家連線到 Portal 時，只需重新啟動伺服器即可
保持連線。兩者透過twisted的AMP協定進行通訊。

(may-2011)=
## 2011 年 5 月：
Evennia 的新版本最初於 2010 年 8 月上線，現為
成熟。 8 月之前版本的所有指令，包括 IRC/IMC2
支援再次發揮作用。今年早些時候新增了 ajax Web 使用者端，
包括將 Evennia 移至自己的 webserver （不再需要
Apache 或 django-testserver）。 Contrib-已新增資料夾。

(aug-2010)=
## 2010 年 8 月：
Evennia-griatch-branch 已準備好與主幹合併。這標誌著一個
伺服器內部工作方式發生了相當大的變化，例如
引入TypeClasses和Scripts（與舊的相比
ScriptParents 和事件）但希望能帶來一切
隨著程式碼開發的繼續，將它們合併到一個一致的套件中。

(may-2010)=
## 2010 年 5 月：
Evennia 目前正在進行大量修改和清理
逐步零碎發展的歲月。因此它處於一個非常
目前處於“阿爾法”階段。這意味著舊的程式碼片段
將無法向後相容。變化幾乎觸及一切
Evennia 的內部部分，來自物件的處理方式
事件、指令和許可權。

(april-2010)=
## 2010 年 4 月：
Griatch 接管 Evennia 專案的維護權
最初的創作者格雷格泰勒。

(older)=
# 年長的

先前的維護者的早期修訂在 Google 程式碼上使用了 SVN
並且沒有變更日誌。

第一次提交（Evennia 的生日）是 2006 年 11 月 20 日。
