from rest_framework.routers import SimpleRouter
from django.urls import path

from materials.apps import MaterialsConfig
from materials.views import LessonViewSet, CourseCreateAPIView, CourseListAPIView, CourseUpdateAPIView, CourseRetrieveAPIView, CourseDestroyAPIView


app_name = MaterialsConfig.name
router = SimpleRouter()
router.register("", LessonViewSet)

urlpatterns = [
    path("courses/", CourseListAPIView.as_view(), name="courses_list"),
    path("courses/<int:pk>/", CourseRetrieveAPIView.as_view(), name="courses_retrieve"),
    path("courses/create/", CourseCreateAPIView.as_view(), name="courses_create"),
    path("courses/<int:pk>/update/", CourseUpdateAPIView.as_view(), name="courses_update"),
    path("courses/<int:pk>/del/", CourseDestroyAPIView.as_view(), name="courses_del")
]

urlpatterns += router.urls
