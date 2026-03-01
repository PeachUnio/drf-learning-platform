from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from materials.models import Course
from users.models import Payment, User, Subscription
from users.serializer import PaymentSerializer, UserCreateSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


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


class SubscriptionView(APIView):
    """API для подписки/отписки от курса"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "Не указан ID курса"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course).first()

        if subscription:
            subscription.delete()
            message = f"Подписка на курс '{course.name}' удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = f"Подписка на курс '{course.name}' оформлена"

        return Response({"message": message})
