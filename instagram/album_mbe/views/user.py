from album_mbe.models import User
from album_mbe.serializers.user import UserRegistrationSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class UserRegistrationCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
