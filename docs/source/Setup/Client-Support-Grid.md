(client-support-grid)=
# 客戶支援網格

與 Evennia 一起使用時，此網格嘗試收集有關不同 MU 客戶端的資訊。
如果您想報告問題、更新條目或新增使用者端，請建立
新的[檔案問題](github:issue)。鼓勵每個人報告他們的發現。

(client-grid)=
## 客戶端網格

傳奇：

 - **姓名**：客戶的姓名。另請注意它是否是OS-特定的。
 - **版本**：測試了哪個版本或客戶端版本範圍。
 - **評論**：使用此客戶端與 Evennia 的任何怪癖都應在此處新增。


| 姓名 | 已測試版本 | 評論 |
| --- | --- | --- |
| [Evennia Webclient][1]    | 1.0+      | Evennia特定 |
| [丁丁++][2]             |   2.0+    | 不支援MXP  |
| [微小賦格曲][3]            | 5.0+      | 不支援UTF-8                                               |
| [MUSHclient][4]（贏）     | 4.94      | NAWS報告全文區域                                    |
| [Zmud][5]（獲勝）           | 7.21      | *UNTESTED*                                                     |
| [Cmud][6]（贏）           | v3        | *UNTESTED*                                                     |
| [馬鈴薯][7]              | 2.0.0b16  | 沒有MXP、MCCP 支援。 Win 32位看不懂            |
|                           |           | “localhost”，必須使用`127.0.0.1`。                             |
| [小泥巴][8]               | 3.4+      | 沒有已知問題。一些舊版本將 <> 顯示為 html         |
|                           |           | MXP 以下。                                                     |
| [SimpleMU][9]（贏）       | 滿的      | 已停產。 NAWS 報告畫素大小。                         |
| [亞特蘭提斯][10] (Mac)      | 0.9.9.4   | 沒有已知問題。                                               |
| [GMUD][11]                | 0.0.1     | 無法處理任何 telnet 握手。不推薦。          |
| [BeipMU][12]（贏）        | 3.0.255   | 沒有MXP支援。最好啟用“MUD提示處理”，停用  |
|                           |           | 「控制代碼 HTML tags」。                                            |
| [MudRammer][13] (IOS)     | 1.8.7     | Telnet 協定合規性不良：顯示虛假字元。  |
| [MUDMaster][14]           | 1.3.1     | *UNTESTED*                                                     |
| [BlowTorch][15]（安德烈）    | 1.1.3     | Telnet NOP 顯示為虛假字元。                     |
| [穆克魯克][16]（安德烈）       | 2015.11.20| Telnet NOP 顯示為虛假字元。有UTF-8/表情符號     |
|                           |           | 支援。                                                       |
| [Gnome-MUD][17] (Unix)    | 0.11.2    | Telnet 握手錯誤。第一次（唯一）嘗試登入    |
|                           |           | 失敗。                                                         |
| [精靈][18]              | 0.4       | 沒有MXP、OOB 支援。                                           |
| [JamochaMUD][19]          | 5.2       | 不支援 MXP 文字中的 ANSI。                         |
| [DuckClient][20]（鉻） | 4.2       | 沒有MXP支援。顯示 Telnet 繼續和                   |
|                           |           | WILL SUPPRESS-GO-AHEAD 作為 ù 字元。好像也跑了       |
|                           |           | 連線上的 `version` 指令，該指令在以下情況下不起作用    |
|                           |           | `MULTISESSION_MODES` 高於 1。                                  |
| [KildClient][21]          | 2.11.1    | 沒有已知問題。                                               |


[1]: ../Components/Webclient
[2]: http://tintin.sourceforge.net/
[3]: http://tinyfugue.sourceforge.net/
[4]: https://mushclient.com/
[5]: http://forums.zuggsoft.com/index.php?page=4&action=file&file_id=65
[6]: http://forums.zuggsoft.com/index.php?page=4&action=category&cat_id=11
[7]: https://www.potatomushclient.com/
[8]: https://www.mudlet.org/
[9]: https://archive.org/details/tucows_196173_SimpleMU_MU_Client
[10]: https://www.riverdark.net/atlantis/
[11]: https://sourceforge.net/projects/g-mud/
[12]: http://www.beipmu.com/
[13]: https://itunes.apple.com/us/app/mudrammer-a-modern-mud-client/id597157072
[14]: https://itunes.apple.com/us/app/mudmaster/id341160033
[15]: https://bt.happygoatstudios.com/
[16]: https://play.google.com/store/apps/details?id=com.crap.mukluk
[17]: https://github.com/GNOME/gnome-mud
[18]: https://spyrit.ierne.eu.org/
[19]: https://jamochamud.org/
[20]: http://duckclient.com/
[21]: https://www.kildclient.org/

(workarounds-for-client-issues)=
## 客戶端問題的解決方法：

(issue-telnet-nop-displays-as-spurious-character)=
### 問題：Telnet NOP 顯示為虛假字元。

已知客戶：

* BlowTorch（安德烈）
* 穆克魯克（安德烈）

解決方法：

* 遊戲中：使用`@option NOPKEEPALIVE=off`取代session，或使用`/save`
引數以永久停用該 Evennia 帳戶。
* 客戶端：在NOP字元上設定一個gag型別的觸發器，使其對客戶端不可見。
