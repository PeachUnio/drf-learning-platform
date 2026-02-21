from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from materials.models import Lesson, Course


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Почта не введена")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен быть сотрудником.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен быть разрешен доступ.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    city = models.CharField(max_length=56, blank=True, null=True, verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", related_name="payments")
    date = models.ForeignKey(auto_now_add=True, verbose_name="Дата платежа")
    paid_curse = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Оплаченный курс", related_name="payments")
    paid_lesson = models.OneToOneField(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Оплаченный урок", related_name="payments")
    payment_amount = models.IntegerField(verbose_name="Сумма оплаты")

    PAYMENT_CASH = "cash"
    PAYMENT_TRANSFER = "transfer"

    PAYMENT_CHOICES = [
        (PAYMENT_CASH, "Оплата наличными"),
        (PAYMENT_TRANSFER, "Оплата переводом на счет")
    ]

    type_of_payment = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name="Статус")
