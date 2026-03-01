from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from materials.models import Course, Lesson
from materials.validators import validate_youtube_linc
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    linc = CharField(validators=[validate_youtube_linc])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonForCourseSerializer(ModelSerializer):
    """Отдельный сериализатор для уроков внутри курса"""

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "linc"]


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonForCourseSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_count", "lessons")
