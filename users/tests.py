from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    """Тесты для подписки на обновления курса"""

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com")
        self.other_user = User.objects.create(email="other@mail.com")
        self.course = Course.objects.create(name="Курс для подписки")
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест создания подписки (подписаться на курс)"""
        url = reverse("users:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], f"Подписка на курс '{self.course.name}' оформлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_delete(self):
        """Тест удаления подписки (отписаться от курса)"""
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("users:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], f"Подписка на курс '{self.course.name}' удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_without_auth(self):
        """Тест подписки без аутентификации"""
        self.client.force_authenticate(user=None)
        url = reverse("users:subscription")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_wrong_course(self):
        """Тест подписки на несуществующий курс"""
        url = reverse("users:subscription")
        data = {"course_id": 99999}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscription_no_course_id(self):
        """Тест подписки без указания course_id"""
        url = reverse("users:subscription")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionInCourseSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com")
        self.other_user = User.objects.create(email="other@mail.com")
        self.course = Course.objects.create(name="Курс с подпиской")
        Subscription.objects.create(user=self.user, course=self.course)

    def test_course_list_with_subscription_flag(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:courses_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data["results"][0]["is_subscribed"])

    def test_course_list_without_subscription(self):
        """Тест, что у пользователя без подписки is_subscribed = False"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("materials:courses_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(data["results"][0]["is_subscribed"])

    def test_course_list_unauth(self):
        """Тест, что неавторизованный пользователь получает 401"""
        self.client.force_authenticate(user=None)  # явно убираем авторизацию
        url = reverse("materials:courses_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
