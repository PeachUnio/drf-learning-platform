from django.urls import path

from users.apps import UsersConfig
from users.views import UserProfileView, PaymentListAPIView


app_name = UsersConfig.name

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    # платежи
    path("payments/", PaymentListAPIView.as_view(), name="payment_list")
]