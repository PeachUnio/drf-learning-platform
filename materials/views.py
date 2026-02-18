from rest_framework.viewsets import ModelViewSet

from materials.models import Lesson
from materials.serializer import LessonSerializer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
