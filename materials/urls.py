from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import LessonViewSet

app_name = MaterialsConfig.name
router = SimpleRouter()
router.register("", LessonViewSet)

urlpatterns = []
urlpatterns += router.urls
