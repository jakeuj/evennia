(extending-the-rest-api)=
# 延長 REST API

```{sidebar}
像 _worn_ 或 _carried_ 這樣的概念並沒有內建在核心 Evennia 中，但這是一個常見的新增內容。本指南使用 `.db.worn` attribute 來識別裝備，但也會解釋如何引用您自己的機械師。
```
預設情況下，Evennia [REST API](../Components/Web-API.md) 提供標準實體的端點。  其中一個端點是 `/api/characters/`，傳回有關角色的資訊。在本教學中，我們將透過向 `/characters` 端點新增 `inventory` 操作來擴充套件它，顯示角色_磨損_和_攜帶_的所有物件。

(creating-your-own-viewset)=
## 建立您自己的檢視集

```{sidebar} 檢視和模板
*檢視* 是告訴 django 在頁面上放置哪些資料的 python 程式碼，而 *模板* 告訴 django 如何顯示該資料。如需更深入的資訊，您可以閱讀 django [檢視檔案](https://docs.djangoproject.com/en/4.1/topics/http/views/) 和 [範本檔案](https://docs.djangoproject.com/en/4.1/topics/templates/)。
```
您需要做的第一件事是定義您自己的 `views.py` 模組。

建立一個空白檔案：`mygame/web/api/views.py`

預設 REST API 端點由 `evennia/web/api/views.py` 中的類別控制 - 您可以複製整個檔案並使用它，但我們將專注於更改最小值。

首先，我們將重新實作處理來自 `characters/` 端點的請求的預設 [CharacterViewSet](CharacterViewSet)。這是 `objects` 端點的子端點，只能存取字元。

```python
# in mygame/web/api/views.py

# we'll need these from django's rest framework to make our view work
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# this implements all the basic Evennia Object endpoint logic, so we're inheriting from it
from evennia.web.api.views import ObjectDBViewSet

# and we need this to filter our character view
from evennia.objects.objects import DefaultCharacter

# our own custom view
class CharacterViewSet(ObjectDBViewSet):
    """
    A customized Character view that adds an inventory detail
    """
    queryset = DefaultCharacter.objects.all_family()
```

(setting-up-the-urls)=
## 設定 url

現在我們有了自己的檢視集，我們可以建立自己的 urls 模組並更改 `characters` 端點路徑以指向我們的端點路徑。

```{sidebar}
Evennia 的 [遊戲網站](../Components/Website.md) 頁面示範如何使用主網站的 `urls.py` 模組 - 如果您還沒有瀏覽該頁面，現在是個好時機。
```
API 路由比網站或 webclient 路由更複雜，因此您需要將整個模組從 evennia 複製到您的遊戲中，而不是修補變更。將檔案從 `evennia/web/api/urls.py` 複製到您的資料夾 `mygame/web/api/urls.py` 並在編輯器中開啟它。

匯入新的檢視模組，然後尋找並更新 `characters` 路徑以使用您自己的檢視集。

```python
# mygame/web/api/urls.py

from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from evennia.web.api.root import APIRootRouter
from evennia.web.api import views

from . import views as my_views # <--- NEW

app_name = "api"

router = APIRootRouter()
router.trailing_slash = "/?"
router.register(r"accounts", views.AccountDBViewSet, basename="account")
router.register(r"objects", views.ObjectDBViewSet, basename="object")
router.register(r"characters", my_views.CharacterViewSet, basename="character") # <--- MODIFIED
router.register(r"exits", views.ExitViewSet, basename="exit")
router.register(r"rooms", views.RoomViewSet, basename="room")
router.register(r"scripts", views.ScriptDBViewSet, basename="script")
router.register(r"helpentries", views.HelpViewSet, basename="helpentry")

urlpatterns = router.urls

urlpatterns += [
    # openapi schema
    path(
        "openapi",
        get_schema_view(title="Evennia API", description="Evennia OpenAPI Schema", version="1.0"),
        name="openapi",
    ),
    # redoc auto-doc (based on openapi schema)
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="rest_framework/redoc.html", extra_context={"schema_url": "api:openapi"}
        ),
        name="redoc",
    ),
]
```

現在我們幾乎已經得到它指向我們的新觀點了。最後一步是將您自己的 API url - `web.api.urls` - 新增到您的 Web 根 url 模組。否則它將繼續指向預設的 API 路由器，我們將永遠不會看到我們的變更。

在編輯器中開啟 `mygame/web/urls.py` 並為「api/」新增路徑，指向 `web.api.urls`。最終檔案應如下所示：

```python
# mygame/web/urls.py

from django.urls import path, include

# default evennia patterns
from evennia.web.urls import urlpatterns as evennia_default_urlpatterns

# add patterns
urlpatterns = [
    # website
    path("", include("web.website.urls")),
    # webclient
    path("webclient/", include("web.webclient.urls")),
    # web admin
    path("admin/", include("web.admin.urls")),
        
    # the new API path
    path("api/", include("web.api.urls")),
]

# 'urlpatterns' must be named such for django to find it.
urlpatterns = urlpatterns + evennia_default_urlpatterns
```

重新啟動您的 evennia 遊戲 - 從指令列 `evennia reboot` 完全重新啟動遊戲 AND portal - 並再次嘗試獲取 `/api/characters/`。如果它的工作原理與以前完全一樣，那麼您就可以繼續下一步了！

(adding-a-new-detail)=
## 新增細節

返回您的角色檢視類別 - 是時候開始新增我們的庫存了。

REST API 中常見的「頁面」稱為*端點*，是您通常造訪的內容。 e.g。 `/api/characters/` 是「字元」端點，`/api/characters/:id` 是單一字元的端點。

```{sidebar} 那個冒號是什麼？
API 路徑中的 `:` 意味著它是一個*變數* - 您不能直接訪問該確切路徑。相反，您可以使用您的角色 ID (e.g.1) 並使用它：`/api/characters/1`
```

然而，端點也可以有一個或多個「詳細」檢視，其功能類似於子點。我們將新增 *inventory* 作為我們的角色端點的詳細資訊，它看起來像 `/api/characters/:id/inventory`

使用 django REST 框架，新增新細節就像在檢視集合類別中新增裝飾方法一樣簡單 - `@action` 裝飾器。由於檢查您的庫存只是資料檢索，因此我們只想允許 `GET` 方法，並且我們將此操作新增為 API 詳細資訊，因此我們的裝飾器將如下所示：
```python
@action(detail=True, methods=["get"])
```

> 在某些情況下，您可能需要的詳細資訊或端點不僅僅是資料檢索：例如，拍賣行清單中的「購買」或「出售」。在這些情況下，您可以使用 *put* 或 *post* 來代替。若要進一步瞭解 `@action` 和 ViewSets 的用途，請造訪 [django REST 框架檔案](https://www.django-rest-framework.org/api-guide/viewsets/)

當新增函式作為詳細資訊操作時，函式的名稱將與詳細資訊相同。由於我們想要 `inventory` 操作，因此我們將定義一個 `inventory` 函式。

```python
"""
mygame/web/api/views.py

Customized views for the REST API
"""
# we'll need these from django's rest framework to make our view work
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# this implements all the basic Evennia Object endpoint logic, so we're inheriting from it
from evennia.web.api.views import ObjectDBViewSet

# and we need this to filter our character view
from evennia.objects.objects import DefaultCharacter

# our own custom view
class CharacterViewSet(ObjectDBViewSet):
    """
    A customized Character view that adds an inventory detail
    """
    queryset = DefaultCharacter.objects.all_family()

    # !! NEW
    @action(detail=True, methods=["get"])
    def inventory(self, request, pk=None):
        return Response("your inventory", status=status.HTTP_200_OK )
```

獲得你的角色的 ID - 它與你的 dbref 相同，但沒有 # - 然後再次 `evennia reboot` 。現在您應該能夠呼叫新角色操作：`/api/characters/1/inventory`（假設您正在檢視角色#1），它將返回字串“您的庫存”

(creating-a-serializer)=
## 建立序列化器

不過，簡單的字串並不是很有用。我們想要的是角色的實際庫存 - 為此，我們需要設定我們自己的*序列化器*。

```{sidebar} Django 序列化器
您可以在 [django REST 框架序列化器檔案](https://www.django-rest-framework.org/api-guide/serializers/) 中更深入地瞭解 django 序列化器。
```
一般來說，*序列化器*將一組資料轉換為可以在資料流中傳送的特殊格式的字串 - 通常是JSON。 Django REST 序列化器是特殊的類別和函式，它們接受 python 物件並將其轉換為 API- 就緒格式。因此，就像檢視集一樣，django 和 evennia 已經為我們完成了許多繁重的工作。

我們不會編寫自己的序列化程式，而是繼承 evennia 預先存在的序列化程式並出於我們自己的目的擴充套件它們。為此，請建立一個新檔案 `mygame/web/api/serializers.py` 並首先新增您需要的匯入。

```python
# the base serializing library for the framework
from rest_framework import serializers

# the handy classes Evennia already prepared for us
from evennia.web.api.serializers import TypeclassSerializerMixin, SimpleObjectDBSerializer

# and the DefaultObject typeclass, for the necessary db model information
from evennia.objects.objects import DefaultObject
```

接下來，我們將定義我們自己的序列化器類別。由於它用於檢索庫存資料，因此我們將對其進行適當的命名。

```python
class InventorySerializer(TypeclassSerializerMixin, serializers.ModelSerializer):
    """
    Serializing an inventory
    """
    
    # these define the groups of items
    worn = serializers.SerializerMethodField()
    carried = serializers.SerializerMethodField()
    
    class Meta:
        model = DefaultObject
        fields = [
            "id", # required field
            # add these to match the properties you defined
            "worn",
            "carried",
        ]
        read_only_fields = ["id"]
```
`Meta` 類別定義了最終序列化字串中將使用哪些欄位。 `id` 欄位來自基礎 ModelSerializer，但您會注意到其他兩個 - `worn` 和 `carried` - 定義為 `SerializerMethodField` 的屬性。這告訴框架在序列化時尋找 `get_X` 形式的匹配方法名稱。

這就是為什麼我們的下一步是新增這些方法！我們定義了屬性 `worn` 和 `carried`，因此我們將新增的方法是 `get_worn` 和 `get_carried`。它們將是靜態方法 - 也就是說，它們不包含 `self` - 因為它們不需要引用序列化器類別本身。

```python
    # these methods filter the character's contents based on the `worn` attribute
    def get_worn(character):
        """
        Serializes only worn objects in the target's inventory.
        """
        worn = [obj for obj in character.contents if obj.db.worn]
        return SimpleObjectDBSerializer(worn, many=True).data
    
    def get_carried(character):
        """
        Serializes only non-worn objects in the target's inventory.
        """
        carried = [obj for obj in character.contents if not obj.db.worn]
        return SimpleObjectDBSerializer(carried, many=True).data
```

對於本指南，我們假設物件是否被磨損儲存在 `worn` 資料庫 attribute 中，並基於該 attribute 進行過濾。這可以很容易地以不同的方式完成，以匹配您自己的遊戲機制：根據 tag 進行過濾，在您的角色上呼叫返回正確列表的自訂方法等。

如果您想新增更多詳細資訊 - 透過輸入將攜帶的物品分組，或分割盔甲與武器，您只需要新增或變更屬性、欄位和方法。

> 請記住：`worn = serializers.SerializerMethodField()` 是 API 知道如何使用 `get_worn`，`Meta.fields` 是實際將其放入最終 JSON 的欄位清單。

您的最終檔案應如下所示：

```python
# mygame/web/api/serializers.py

# the base serializing library for the framework
from rest_framework import serializers

# the handy classes Evennia already prepared for us
from evennia.web.api.serializers import TypeclassSerializerMixin, SimpleObjectDBSerializer

# and the DefaultObject typeclass, for the necessary db model information
from evennia.objects.objects import DefaultObject

class InventorySerializer(TypeclassSerializerMixin, serializers.ModelSerializer):
    """
    Serializing an inventory
    """
    
    # these define the groups of items
    worn = serializers.SerializerMethodField()
    carried = serializers.SerializerMethodField()
    
    class Meta:
        model = DefaultObject
        fields = [
            "id", # required field
            # add these to match the properties you defined
            "worn",
            "carried",
        ]
        read_only_fields = ["id"]

    # these methods filter the character's contents based on the `worn` attribute
    def get_worn(character):
        """
        Serializes only worn objects in the target's inventory.
        """
        worn = [obj for obj in character.contents if obj.db.worn]
        return SimpleObjectDBSerializer(worn, many=True).data
    
    def get_carried(character):
        """
        Serializes only non-worn objects in the target's inventory.
        """
        carried = [obj for obj in character.contents if not obj.db.worn]
        return SimpleObjectDBSerializer(carried, many=True).data
```

(using-your-serializer)=
## 使用你的序列化器

現在讓我們回到我們的檢視檔案，`mygame/web/api/views.py`。新增我們的新序列化器和其餘的匯入：

```python
from .serializers import InventorySerializer
```

然後，更新我們的 `inventory` 詳細資訊以使用我們的序列化器。
```python
    @action(detail=True, methods=["get"])
    def inventory(self, request, pk=None):
        obj = self.get_object()
        return Response( InventorySerializer(obj).data, status=status.HTTP_200_OK )
```

您的檢視檔案現在應如下所示：

```python
"""
mygame/web/api/views.py

Customized views for the REST API
"""
# we'll need these from django's rest framework to make our view work
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# this implements all the basic Evennia Object endpoint logic, so we're inheriting from it
from evennia.web.api.views import ObjectDBViewSet

# and we need this to filter our character view
from evennia.objects.objects import DefaultCharacter

from .serializers import InventorySerializer # <--- NEW

# our own custom view
class CharacterViewSet(ObjectDBViewSet):
    """
    A customized Character view that adds an inventory detail
    """
    queryset = DefaultCharacter.objects.all_family()

    @action(detail=True, methods=["get"])
    def inventory(self, request, pk=None):
        return Response( InventorySerializer(obj).data, status=status.HTTP_200_OK ) # <--- MODIFIED
```

這將使用我們新的序列化器來獲取角色的庫存。除了……不完全是。

繼續嘗試：`evennia reboot`，然後像以前一樣`/api/characters/1/inventory`。您應該收到一條錯誤訊息，指出您沒有許可權，而不是返回字串「您的庫存」。別擔心 - 這意味著它已成功引用新的序列化程式。我們只是還沒有授予它存取物件的許可權。

(customizing-api-permissions)=
## 自訂API許可權

Evennia 附帶自己的自訂 API 許可權類，將 API 許可權連線到遊戲內許可權層次結構並鎖定係統。由於我們現在嘗試存取物件的資料，因此我們需要透過 `has_object_permission` 檢查以及常規許可權檢查 - 並且預設許可權類別將操作硬編碼到物件許可權檢查中。

由於我們為角色端點新增了一個新操作 - `inventory`，因此我們還需要在角色端點上使用我們自己的自訂許可權。再建立一個模組檔：`mygame/web/api/permissions.py`

與前面的類別一樣，我們將從原始類別繼承並擴充套件它，以利用 Evennia 已經為我們完成的所有工作。

```python
# mygame/web/api/permissions.py

from evennia.web.api.permissions import EvenniaPermission

class CharacterPermission(EvenniaPermission):
    
    def has_object_permission(self, request, view, obj):
        """
        Checks object-level permissions after has_permission
        """
        # our new permission check
        if view.action == "inventory":
            return self.check_locks(obj, request.user, self.view_locks)

        # if it's not an inventory action, run through all the default checks
        return super().has_object_permission(request, view, obj)
```

這就是整個許可權類別！對於我們的最後一步，我們需要透過匯入它並設定 `permission_classes` 屬性來在角色檢視中使用它。

完成後，最終的 `views.py` 應如下：

```python
"""
mygame/web/api/views.py

Customized views for the REST API
"""
# we'll need these from django's rest framework to make our view work
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# this implements all the basic Evennia Object endpoint logic, so we're inheriting from it
from evennia.web.api.views import ObjectDBViewSet

# and we need this to filter our character view
from evennia.objects.objects import DefaultCharacter

from .serializers import InventorySerializer
from .permissions import CharacterPermission # <--- NEW

# our own custom view
class CharacterViewSet(ObjectDBViewSet):
    """
    A customized Character view that adds an inventory detail
    """
    permission_classes = [CharacterPermission] # <--- NEW
    queryset = DefaultCharacter.objects.all_family()

    @action(detail=True, methods=["get"])
    def inventory(self, request, pk=None):
        obj = self.get_object()
        return Response( InventorySerializer(obj).data, status=status.HTTP_200_OK )
```

最後`evennia reboot` - 現在你應該能夠獲得`/api/characters/1/inventory`並看到你的角色擁有的一切，整齊地分為「磨損」和「攜帶」。

(next-steps)=
## 下一步

```{sidebar} Django REST 框架
要更深入地瞭解 django REST 框架，您可以閱讀[他們的教學](https://www.django-rest-framework.org/tutorial/1-serialization/) 或直接訪問[django REST 框架 API 檔案](https://www.django-rest-framework.org/api-guide/requests/)。
```
就是這樣！您已經瞭解如何為 Evennia 自訂您自己的 REST 端點、新增新的端點詳細資訊以及為 REST API 序列化來自遊戲物件的資料。藉助這些工具，您可以獲得所需的任何遊戲內資料，並使用 API 使其可用，甚至可以修改。

如果您想要挑戰，請嘗試利用您學到的知識並實施新的 `desc` 細節，這將使您 `GET` 現有字元 desc _或_ `PUT` 一個新 desc。 （提示：檢視 evennia 的 REST 許可權模組如何運作，以及預設 evennia REST API 檢視中的 `set_attribute` 方法。）

