from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    preview = models.ImageField(
        upload_to="materials/preview/course", blank=True, null=True, verbose_name="Превью курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    image = models.ImageField(
        upload_to="materials/preview/lesson",
        blank=True,
        null=True,
        verbose_name="Превью урока",
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Курс", related_name="lessons"
    )
    linc = models.CharField(max_length=150, unique=True, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
