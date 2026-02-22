from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_curse", "paid_lesson", "type_of_payment")
    ordering_fields = ("date",)

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
