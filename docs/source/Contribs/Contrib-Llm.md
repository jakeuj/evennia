(large-language-model-chat-bot-ai-integration)=
# 大型語言模型（“聊天機器人AI”）整合

Griatch 2023 的貢獻

這會增加一個 LLMClient，允許 Evennia 向 LLM 伺服器傳送提示（大語言模型，與 ChatGPT 類似）。範例使用本地 OSS LLM 安裝。其中包括一個 NPC，您可以使用新的 `talk` 指令與之聊天。 NPC 將使用來自 LLM 伺服器的 AI 回應進行回應。所有呼叫都是非同步的，因此如果 LLM 很慢，Evennia 不會受到影響。

    > create/drop villager:evennia.contrib.rpg.llm.LLMNPC
    You create a new LLMNPC: villager

    > talk villager Hello there friend, what's up?
    You say (to villager): Hello there friend, what's up?
    villager says (to You): Hello! Not much going on, really.

    > talk villager Do you know where we are?
    You say (to villager): Do you know where we are?
    villager says (to You): We are in this strange place called 'Limbo'. Not much to do here.

(installation)=
## 安裝

您需要兩個元件來實現此contrib - Evennia，以及一個操作並向LLM AI 模型提供API 的LLM webserver。

(llm-server)=
### LLM 伺服器

有許多 LLM 伺服器，但安裝和設定它們可能非常技術性。這個contrib是用[text- Generation-webui](https://github.com/oobabooga/text-generation-webui)測試的。它具有很多功能，同時也易於安裝。 |

1. [前往安裝部分](https://github.com/oobabooga/text-generation-webui#installation) 並取得適用於您的OS 的「一鍵安裝程式」。
2. 將檔案解壓縮到硬碟上某個資料夾中（如果您不想，則不必將其放在 evennia 內容旁邊）。
3. 在終端機/控制檯中，`cd` 進入資料夾並以 OS 執行的任何方式執行原始檔（例如 Linux 為 `source start_linux.sh`，對於 Windows 為 `.\start_windows`）。這是一個安裝程式，它將獲取並安裝 conda 虛擬環境中的所有內容。當詢問時，請確保選擇您的GPU（NVIDIA/AMD 等）（如果您有的話），否則使用CPU。
4. 全部載入完畢後，使用`Ctrl-C`（或`Cmd-C`）停止伺服器並開啟檔案`webui.py`（它是您解壓縮的檔案中最上面的檔案之一）。找到頂部附近的文字字串 `CMD_FLAGS = ''` 並將其變更為 `CMD_FLAGS = '--api'`。然後儲存並關閉。這使得伺服器自動啟動其 api。
4. 現在只需再次從 script（`start_linux.sh` 等）開始執行該伺服器即可。今後您將用它來啟動 LLM 伺服器。
5. 伺服器執行後，將瀏覽器指向 http://127.0.0.1:7860 以檢視正在執行的文字產生 Web UI。如果您開啟 API，您會發現它現在在連線埠 5000 上處於活動狀態。除非您進行了更改，否則這不應與預設的 Evennia 連線埠發生衝突。
6. 此時您已擁有伺服器和 API，但它實際上尚未執行任何大型語言模型 (LLM)。在 Web UI 中，轉到 `models` 選項卡並在 `Download custom model or LoRA` 欄位中輸入 github 樣式的路徑。  若要測試一切正常，請輸入 `DeepPavlov/bart-base-en-persona-chat` 並下載。這是一個小型模型（3.5 億個引數），因此應該可以只使用 CPU 在大多數機器上執行。更新左側下拉清單中的模型並選擇它，然後使用 `Transformers` 載入器載入它。它應該載入得很快。如果您想每次都載入，可以選取`Autoload the model`核取方塊；否則，您需要在每次啟動 LLM 伺服器時選擇並載入模型。
7. 為了進行實驗，您可以在 [huggingface.co/models](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending) 上找到數千個其他開源文字產生 LLM 模型。注意不要下載太大的模型；您的機器可能無法載入它！如果您嘗試大型模型，請_不要_設定 `Autoload the model` 核取方塊，以防模型在啟動時導致伺服器崩潰。

為了排除故障，您可以檢視`text-generation-webui`伺服器的終端輸出；它會向您顯示您對其所做的請求，並列出所有錯誤。有關更多詳細資訊，請參閱 text- Generation-webui 主頁。

(evennia-config)=
### Evennia設定

為了能夠與 NPCs 對話，請將 `evennia.contrib.rpg.llm.llm_npc.CmdLLMTalk` 匯入並新增到 `mygame/commands/default_cmdsets.py` 中的預設 cmdset：

```py
# in mygame/commands/default_cmdsets.py

# ... 
from evennia.contrib.rpg.llm import CmdLLMTalk  # <----

class CharacterCmdSet(default_cmds.CharacterCmdSet): 
    # ...
    def at_cmdset_creation(self): 
        # ... 
        self.add(CmdLLMTalk())     # <-----


```

有關詳細資訊，請參閱[新增指令教學](../Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Adding-Commands.md)。

預設的 LLM api 設定應該與在連線埠 5000 上執行其 API 的 `text-generation-webui` LLM 伺服器一起使用。您也可以透過設定對其進行自訂（如果未新增設定，則使用以下預設設定）：

```python
# in mygame/server/conf/settings.py

# path to the LLM server
LLM_HOST = "http://127.0.0.1:5000"
LLM_PATH = "/api/v1/generate"

# if you wanted to authenticated to some external service, you could
# add an Authenticate header here with a token
# note that the content of each header must be an iterable
LLM_HEADERS = {"Content-Type": ["application/json"]}

# this key will be inserted in the request, with your user-input
LLM_PROMPT_KEYNAME = "prompt"

# defaults are set up for text-generation-webui and most models
LLM_REQUEST_BODY = {
    "max_new_tokens": 250,  # set how many tokens are part of a response
    "temperature": 0.7, # 0-2. higher=more random, lower=predictable
}
# helps guide the NPC AI. See the LLNPC section.
LLM_PROMPT_PREFIX = (
  "You are roleplaying as {name}, a {desc} existing in {location}. "
  "Answer with short sentences. Only respond as {name} would. "
  "From here on, the conversation between {name} and {character} begins."
)
```
如果您進行任何更改，請不要忘記重新載入 Evennia（遊戲中的 `reload`，或從終端載入 `evennia reload`）。

同樣重要的是要注意，每個模型所需的 `PROMPT_PREFIX` 取決於它們的訓練方式。有很多不同的格式。因此，您需要研究一下您嘗試的每個模型應該使用什麼。報告你的發現！

(usage)=
## 用法

隨著 LLM 伺服器執行並新增了新的 `talk` 指令，建立一個新的 LLM-已連線 NPC 並在遊戲中與其對話。

    > create/drop girl:evennia.contrib.rpg.llm.LLMNPC
    > talk girl Hello!
    You say (to girl): Hello
    girl ponders ...
    girl says (to You): Hello! How are you?

房間裡的每個人都會聽到談話內容。如果伺服器回應速度慢於 2 秒（預設），NPC 將顯示思考/思考訊息。

(primer-on-open-source-llm-models)=
## 開源 LLM 模式入門

[抱臉](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending)正在成為下載OSS模型的一種標準。在 `text generation` 類別（這就是我們想要的聊天機器人）中，有大約 20k 個模型可供選擇（2023 年）。為了幫助您入門，請檢視 [TheBloke](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending&search=TheBloke) 提供的模型。 TheBloke 採用了其他人發布的「量化」（降低解析度）模型，以適應消費性硬體。 TheBloke 的型號大致遵循以下命名標準：

TheBloke/ModelName-ParameterSize-其他-GGML/GPTQ

例如

TheBloke/Llama-2-7B-聊天-GGML
	TheBloke/StableBeluga-13B-GPTQ

這裡，`Llama-2` 是 Meta 開源發布的“基本模型”，供免費（也可商業）使用。一個基本模型需要數百萬美元和一臺超級電腦來從頭開始訓練。然後其他人“微調”該基本模型。 `StableBeluga` 模型是由某人對 `Llama-2` 進行部分重新訓練而建立的，以使其更加專注於某些特定領域，例如以特定風格聊天。
 
模型有大小，以它們擁有的引數數量給出，就像它們大腦中有多少“神經元”一樣。在上面的兩個範例中，第一個範例有 `7B` - 70 億個引數，第二個範例有 `13B` - 130 億個引數。相比之下，我們建議在安裝過程中嘗試的小型型號僅為`0.35B`。

如果沒有像 TheBloke 這樣的人「量化」它們，從根本上降低它們的精度，以基本形式執行這些模型仍然是不可能的。量化以位元組精度給出。因此，如果原始超級電腦版本使用 32 位元精度，那麼您實際可以在機器上執行的模型通常只使用 8 位元或 4 位元解析度。人們普遍認為，能夠在低解析度下執行具有更多引數的模型比在高解析度下執行較小的模型更好。

您將看到 TheBloke 的量化模型有 GPTQ 或 GGML 結尾。簡化後，GPTQ是主要的量化模型。要執行此模型，您需要有足夠強大的 GPU 才能在 VRAM 中容納整個模型。相反，GGML 允許您將部分型號解除安裝到正常的 RAM 並使用您的 CPU 代替。由於您的 RAM 可能多於 VRAM，這意味著您可以透過這種方式執行更大的模型，但它們的執行速度會慢得多。

此外，您需要額外的記憶體空間來儲存模型的_context_。如果您正在聊天，這將是聊天記錄。雖然這聽起來只是一些文字，但上下文的長度決定了 AI 必須「記住」多少才能得出結論。這是用「標記」（大約是單字的一部分）來衡量的。常見的上下文長度為 2048 個標記，模型必須經過專門訓練才能處理更長的上下文。

以下是對最常見模型大小和 2048 個令牌上下文的硬體要求的一些粗略估計。如果您的 GPU 上有足夠的 VRAM，請使用 GPTQ 模型，否則使用 GMML 模型也能夠將部分或全部資料放入 RAM 中。

| 型號尺寸 | 大約需要VRAM或RAM（4位/8位） |
| --- | --- |
| 3B | 1.5 GB / 3 GB
| 7B  | 3.5GB / 7GB | 
| 13B | 7GB/13GB | 
| 33B | 14GB / 33GB |
| 70B | 35GB / 70GB |

7B 甚至 3B 模型的結果可能令人震驚！但設定你的期望。目前（2023 年）頂級消費者遊戲 GPUs 擁有 24GB 或 VRAM，最多可全速容納 33B 4 位元量化模型 (GPTQ)。

相比之下，Chat-GPT 3.5 是 175B 型號。我們不知道Chat-GPT 4有多大，但可能達到1700B。因此，您也可以考慮向商業提供者支付超過 API 的費用來為您執行模型。稍後會對此進行討論，但首先嘗試在本地執行一個小模型，以瞭解一切情況。


(using-an-ai-cloud-service)=
## 使用 AI 雲端服務

您也可以呼叫外部API，例如OpenAI（聊天-GPT）或Google。大多數雲端託管服務都是商業性的並且需要花錢。但由於他們擁有執行更大模型（或他們自己的專有模型）的硬體，因此他們可能會給出更好更快的結果。

```{warning}
呼叫外部 API 目前未經測試，因此請報告任何發現。由於 Evennia 伺服器（不是 Portal）正在執行呼叫，因此如果您像這樣呼叫，建議您在您和網路之間放置一個代理。

```
以下是用於呼叫 [OpenAI's v1/completions API](https://platform.openai.com/docs/api-reference/completions) 的 Evennia 設定的未經測試的範例：

```python
LLM_HOST = "https://api.openai.com"
LLM_PATH = "/v1/completions"
LLM_HEADERS = {"Content-Type": ["application/json"],
               "Authorization": ["Bearer YOUR_OPENAI_API_KEY"]}
LLM_PROMPT_KEYNAME = "prompt"
LLM_REQUEST_BODY = {
                        "model": "gpt-3.5-turbo",
                        "temperature": 0.7,
                        "max_tokens": 128,
                   }

```

> TODO：OpenAI 較現代的 [v1/chat/completions](https://platform.openai.com/docs/api-reference/chat) API 目前無法正常運作，因為它有點複雜。

(the-llmnpc-class)=
## LLMNPC 類

LLM-able NPC 類別有一個新方法 `at_talked_to`，它連線到 LLM 伺服器並回應。這由新的 `talk` 指令呼叫。請注意，所有這些呼叫都是非同步的，這意味著緩慢的回應不會阻塞 Evennia。

NPC 的 AI 由一些額外的屬性和屬性控制，其中大部分可以由建構者在遊戲中直接自訂。

(prompt_prefix)=
### `prompt_prefix`

`prompt_prefix` 非常重要。這將新增在您的提示前面並幫助 AI 知道如何回應。請記住，LLM 模型基本上是一種自動完成機制，因此透過在字首中提供範例和說明，您可以幫助它以更好的方式回應。

用於給定 NPC 的字首字串從以下位置之一查詢，順序為：

1. Attribute `npc.db.chat_prefix` 儲存在 NPC 上（預設未設定）
2. LLMNPC 類別上的屬性 `chat_prefix`（預設為 `None`）。
3. `LLM_PROMPT_PREFIX` 設定（預設未設定）
4. 如果以上位置均未設定，則使用以下預設值：

       "You are roleplaying as {name}, a {desc} existing in {location}.
       Answer with short sentences. Only respond as {name} would.
       From here on, the conversation between {name} and {character} begins."

在這裡，格式 tag `{name}` 被替換為 NPCs 的名稱，`desc` 被替換為描述，`location` 被替換為當前位置的名稱，`character` 被替換為與之交談的人。所有字元名稱均由 `get_display_name(looker)` 呼叫給出，因此這可能會有所不同
從一個人到另一個人。

根據模型的不同，擴充套件字首以提供有關角色的更多資訊以及通訊範例可能非常重要。在產生類似人類語言的東西之前，可能需要進行大量的調整。

(response-template)=
### 回覆模板

`response_template` AttributeProperty 預設為

    $You() $conj(say) (to $You(character)): {response}"

遵循常見的 `msg_contents` [FuncParser](../Components/FuncParser.md) 語法。 `character` 字串將對應到與 NPC 對話的字串，`response` 將是 NPC 所說的內容。

(memory)=
### 記憶

NPC 會記住每個玩家對它說過的話。此記憶將包含在 LLM 的提示中，並幫助其理解對話的上下文。此記憶體的長度由 `max_chat_memory_size` AttributeProperty 給出。預設值為 25 則訊息。  一旦達到記憶體最大值，較舊的訊息就會被忘記。每個與 NPC 交談的玩家的記憶體是單獨儲存的。

(thinking)=
### 思維

如果 LLM 伺服器響應緩慢，NPC 將回顯隨機的“思考訊息”，以表明它沒有忘記您（例如“村民思考您的話...”）。

它們由 LLMNPC 類上的兩個 `AttributeProperties` 控制：

- `thinking_timeout`：顯示訊息之前等待的時間（以秒為單位）。預設值為 2 秒。
- `thinking_messages`：可隨機選擇的訊息清單。每個訊息字串可以包含 `{name}`，它將被 NPCs 名稱取代。


(todo)=
## TODO

這個contrib 有很大的擴充套件潛力。一些想法：

- 更輕鬆支援不同的雲端 LLM 供應商 API 結構。
- 更多有用提示和適合 MUD 使用的模型的範例。


----

<small>此檔案頁面是從`evennia\contrib\rpg\llm\README.md`產生的。對此的更改
檔案將被覆蓋，因此請編輯該檔案而不是此檔案。 </small>
