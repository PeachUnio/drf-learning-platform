from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "course", "auth")
    list_filter = ("course", "auth")
    search_fields = ("name", "description")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "auth")
