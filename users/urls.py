from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserProfileView, UserCreateAPIView, UserDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/delite/", UserDestroyAPIView.as_view(), name="profile_delite"),
    # платежи
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
]
