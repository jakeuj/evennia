
(evennia-server-lifecycle)=
# Evennia 伺服器生命週期

作為遊戲設計的一部分，您可能想要更改 Evennia 在啟動或停止時的行為。一個常見的用例是啟動一些您希望在伺服器啟動後始終可用的自訂程式碼。

Evennia 有三個主要生命週期，您可以為所有這些生命週期新增自訂行為：

- **資料庫生命週期**：Evennia使用資料庫。這與您所做的程式碼變更同時存在。該資料庫一直存在，直到您選擇重置或刪除它為止。這樣做不需要重新下載Evennia。
- **重啟生命週期**：從Evennia開始到完全關閉，這表示Portal和伺服器都停止了。在這個週期結束時，所有玩家都斷開連線。
- **重新載入生命週期：** 這是主要執行時，直到發生「重新載入」事件。重新載入會重新整理遊戲程式碼，但不會踢任何玩家。

(when-evennia-starts-for-the-first-time)=
## 當Evennia第一次啟動時

這是**資料庫生命週期**的開始，就在資料庫第一次建立和遷移之後（或在資料庫被刪除和重建之後）。如果您想在第一次後重新執行此序列，請參閱[選擇資料庫](../Setup/Choosing-a-Database.md)，以瞭解有關如何重設資料庫的說明。

鉤子按順序呼叫：

1.  `evennia.server.initial_setup.handle_setup(last_step=None)`：Evennia的核心初始化函式。這就是為什麼建立 #1 角色（與超級使用者帳戶繫結）和 `Limbo` 房間的原因。它會呼叫下面的下一個掛鉤，如果出現問題，也會在最後一個失敗的步驟處重新啟動。通常你不應該重寫這個函式，除非你_真的_知道你在做什麼。要覆蓋，請將 `settings.INITIAL_SETUP_MODULE` 更改為您自己的模組，其中包含 `handle_setup` 函式。
2. `mygame/server/conf/at_initial_setup.py` 包含一個函式 `at_initial_setup()`，將在不帶引數的情況下呼叫函式。它是由上述函式在設定序列中最後呼叫的。使用它來新增您自己的自訂行為或調整初始化。例如，如果您想要變更自動產生的 Limbo 房間，您應該從這裡進行。如果您想更改此函式的位置，可以透過更改 `settings.AT_INITIAL_SETUP_HOOK_MODULE` 來實現。

(when-evennia-starts-and-shutdowns)=
## 當 Evennia 啟動和關閉時

這是**重新啟動生命週期**的一部分。 Evennia 由兩個主要程式組成，[Portal 和伺服器](../Components/Portal-And-Server.md)。重新啟動或關閉時，Portal 和伺服器都會關閉，這意味著所有玩家都將斷開連線。

每個程式呼叫位於`mygame/server/conf/at_server_startstop.py`的一系列鉤子。您可以自訂與 `settings.AT_SERVER_STARTSTOP_MODULE` 一起使用的模組 - 這甚至可以是模組列表，如果是這樣，將從每個模組中按順序呼叫適當命名的函式。

所有鉤子的呼叫都不帶引數。

> 在鉤子名稱中使用術語「伺服器」表示整個 Evennia，而不僅僅是 `Server` 元件。

(server-cold-start)=
### 伺服器冷啟動

完全停止後從零啟動伺服器。這是透過終端的 `evennia start` 完成的。

1. `at_server_init()` - 始終在啟動順序中先呼叫。
2. `at_server_cold_start()` - 僅在冷啟動時呼叫。
3. `at_server_start()` - 始終在啟動序列中最後呼叫。

(server-cold-shutdown)=
### 伺服器冷關機

關閉一切。在遊戲中使用 `shutdown` 或從終端使用 `evennia stop` 完成。

1. `at_server_cold_stop()` - 僅在冷站時呼叫。
2. `at_server_stop()` - 始終在停止序列中最後呼叫。

(server-reboots)=
### 伺服器重新啟動

這是透過 `evennia reboot` 完成的，並有效地構成自動冷關閉，然後由 `evennia` 啟動器控製冷啟動。沒有特殊的 `reboot` 鉤子，相反，它看起來像您所期望的：

1. `at_server_cold_stop()`
2. `at_server_stop()`（此後，`Server` + `Portal` 均已關閉）
3. `at_server_init()`（如冷啟動）
4. `at_server_cold_start()`
5. `at_server_start()`

(when-evennia-reloads-and-resets)=
## 當Evennia重新載入並重置時

這就是**重新載入生命週期**。如上所述，Evennia 由兩個元件組成，[Portal 和伺服器](../Components/Portal-And-Server.md)。重新載入期間，僅 `Server` 元件關閉並重新啟動。由於 Portal 保持開啟狀態，因此玩家不會斷開連線。

所有鉤子的呼叫都不帶引數。

(server-reload)=
### 伺服器重新載入

重新載入是透過遊戲中的 `reload` 指令啟動的，或者透過終端使用 `evennia reload` 啟動的。

1. `at_server_reload_stop()` - 僅在重新載入停止時呼叫。
2. `at_server_stop` - 始終在停止序列中最後呼叫。
3. `at_server_init()` - 始終在啟動順序中先呼叫。
4. `at_server_reload_start()` - 僅在重新載入（重新）啟動時呼叫。
5. `at_server_start()` - 始終在啟動序列中最後呼叫。

(server-reset)=
### 伺服器重置

「重置」是一種混合重新載入狀態，其中重新載入被視為冷關閉，只是為了執行掛鉤（玩家不會斷開連線）。它在遊戲中使用 `reset` 執行，或從終端使用 `evennia reset` 執行。

1. `at_server_cold_stop()`
2. `at_server_stop()`（此後，只有`Server`關閉）
3. `at_server_init()`（`Server` 即將恢復）
4. `at_server_cold_start()`
5. `at_server_start()`
