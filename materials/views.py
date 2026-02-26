from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializer import CourseDetailSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsAuth, IsNotModer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.auth = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsAuth,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsAuth,)
        return super().get_permissions()


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        course = serializer.save()
        course.auth = self.request.user
        course.save()


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsModer | IsAuth)


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (IsAuthenticated, IsModer | IsAuth)


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsModer | IsAuth)


class CourseDestroyAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsAuth | ~IsModer)
