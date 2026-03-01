from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonsTestCase(APITestCase):
    """Тесты для CURD урока"""

    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.course = Course.objects.create(name="Курс о тестах")
        self.lesson = Lesson.objects.create(
            name="Тестовый урок 1", linc="youtube.com/test/1/", course=self.course, auth=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест просмотра урока"""
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тест создание урока"""
        url = reverse("materials:lesson-list")
        data = {"name": "Созданный урок 1", "linc": "youtube.com/create/1/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест обновления урока"""
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        data = {
            "name": "Воссозданный урок 1",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Воссозданный урок 1")

    def test_lesson_delete(self):
        """Тест удаления урока"""
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест для просмотра списка уроков"""
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "linc": self.lesson.linc,
                    "name": self.lesson.name,
                    "description": None,
                    "image": None,
                    "course": self.course.pk,
                    "auth": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
