from rest_framework.generics import RetrieveUpdateAPIView

from users.models import User
from users.serializer import UserSerializer


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user