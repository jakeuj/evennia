(godot-websocket)=
# Godot Websocket

貢獻者 ChrisLR, 2022

這個contrib允許你將Godot用戶端直接連線到你的mud，
並使用 BBCode 以 Godot RichTextLabel 的顏色顯示常規文字。
您可以使用 Godot 提供具有適當 Evennia 支援的進階功能。


(installation)=
## 安裝

您需要在 `settings.py` 中新增以下設定並重新啟動 evennia。

```python
PORTAL_SERVICES_PLUGIN_MODULES.append('evennia.contrib.base_systems.godotwebsocket.webclient')
GODOT_CLIENT_WEBSOCKET_PORT = 4008
GODOT_CLIENT_WEBSOCKET_CLIENT_INTERFACE = "127.0.0.1"
```

這將使 evennia 監聽 Godot 的連線埠 4008。
您可以根據需要變更連線埠和介面。


(usage)=
## 用法

簡而言之，它是使用上面定義的連線埠使用 Godot Websocket 進行連線。
它可以讓你將資料從 Evennia 傳輸到 Godot，讓你
在啟用 bbcode 的情況下取得 RichTextLabel 中的樣式文字或處理
根據需要從 Evennia 給出的額外資料。


本節假設您具有如何使用 Godot 的基本知識。
您可以閱讀以下網址以瞭解有關 Godot Websockets 的更多詳細資訊
並實現一個最小的用戶端或檢視本頁底部的完整範例。

https://docs.godotengine.org/en/stable/tutorials/networking/websocket.html

本文件的其餘部分將針對 Godot 4。
請注意，此處顯示的部分程式碼部分取自官方 Godot 文件

godot 中的一個非常基本的設定需要

- 一個 RichTextLabel 節點顯示 Evennia 輸出，確保在其上啟用 bbcode。
- 您的 websocket 使用者端程式碼的一個節點，附加了新的 Script。
- 1個TextEdit節點輸入指令
- 一鍵節點按下並傳送指令
- 佈局控制元件，在本例中我使用了
面板
   VBoxContainer
     RichTextLabel
     HBoxContainer
       TextEdit
       Button

我不會詳細介紹佈局的工作原理，但可以在 godot 檔案中輕鬆存取它們的檔案。


開啟您的用戶端程式碼的script。

我們需要定義通往您的 mud 的 url，使用您在 Evennia 設定中使用的相同值。
接下來我們編寫一些基本程式碼來建立連線。
當場景準備好時，它將連線，當我們收到資料時輪詢並列印資料，當場景退出時關閉。
```
extends Node

# The URL we will connect to.
var websocket_url = "ws://127.0.0.1:4008"
var socket := WebSocketPeer.new()

func _ready():
	if socket.connect_to_url(websocket_url) != OK:
		print("Unable to connect.")
		set_process(false)


func _process(_delta):
	socket.poll()
	match socket.get_ready_state():
		WebSocketPeer.STATE_OPEN:
			while socket.get_available_packet_count():
				print(socket.get_packet().get_string_from_ascii())
		
		WebSocketPeer.STATE_CLOSED:
			var code = socket.get_close_code()
			var reason = socket.get_close_reason()
			print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
			set_process(false)

func _exit_tree():
	socket.close()

```

此時，您可以啟動 evennia 伺服器，執行 godot，它應該會列印預設回應。
之後你需要妥善處理evennia傳送的資料。
為此，我們將新增一個新函式來正確傳送訊息。

這是一個例子
```
func _handle_data(data):
	print(data)  # Print for debugging
	var data_array = JSON.parse_string(data)
	# The first element can be used to see if its text
	if data_array[0] == 'text':
		# The second element contains the messages
		for msg in data_array[1]: 			write_to_rtb(msg)

func write_to_rtb(msg):
	output_label.append_text(msg)
```

第一個元素是型別，如果是訊息則為`text`
它可以是您提供給 Evennia `msg` 函式的任何內容。
第二個元素是與訊息型別相關的資料，在本例中它是要顯示的文字清單。
由於它被解析為 BBCode，我們可以透過呼叫它的 append_text 方法將其直接新增到 RichTextLabel 中。

如果你想要比 Godot 中花哨的文字更好的東西，你將會有
利用Evennia的OOB傳送額外的資料。

您可以[在此閱讀有關 OOB 的更多資訊](https://www.evennia.com/docs/latest/OOB.html#oob)。


現在要傳送資料，我們將按鈕按下訊號連線到一個方法，
讀取標籤輸入並透過 websocket 傳送它，然後清除標籤。
```
func _on_button_pressed():
	var msg = text_edit.text
	var msg_arr = ['text', [msg], {}]
	var msg_str = JSON.stringify(msg_arr)
	socket.send_text(msg_str)
	text_edit.text = ""
```



(known-issues)=
## 已知問題

- 直接從 Evennia.DB 傳送 SaverDicts 和類似物件會導致問題，
在此之前將它們轉換為 dict() 或 list() 。


(full-example-script)=
## 完整範例Script
```
extends Node

# The URL we will connect to.
var websocket_url = "ws://127.0.0.1:4008"
var socket := WebSocketPeer.new()

@onready var output_label = $"../Panel/VBoxContainer/RichTextLabel"
@onready var text_edit = $"../Panel/VBoxContainer/HBoxContainer/TextEdit"


func _ready():
	if socket.connect_to_url(websocket_url) != OK:
		print("Unable to connect.")
		set_process(false)

func _process(_delta):
	socket.poll()
	match socket.get_ready_state():
		WebSocketPeer.STATE_OPEN:
			while socket.get_available_packet_count():
				var data = socket.get_packet().get_string_from_ascii()
				_handle_data(data)
		
		WebSocketPeer.STATE_CLOSED:
			var code = socket.get_close_code()
			var reason = socket.get_close_reason()
			print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
			set_process(false)

func _handle_data(data):
	print(data)  # Print for debugging
	var data_array = JSON.parse_string(data)
	# The first element can be used to see if its text
	if data_array[0] == 'text':
		# The second element contains the messages
		for msg in data_array[1]: 			write_to_rtb(msg)

func write_to_rtb(msg):
	output_label.append_text(msg)

func _on_button_pressed():
	var msg = text_edit.text
	var msg_arr = ['text', [msg], {}]
	var msg_str = JSON.stringify(msg_arr)
	socket.send_text(msg_str)
	text_edit.text = ""

func _exit_tree():
	socket.close()

```


----

<small>此檔案頁面是從`evennia\contrib\base_systems\godotwebsocket\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
