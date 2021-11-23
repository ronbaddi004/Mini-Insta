from album_mbe.models import User, UserSimilarity
from album_mbe.serializers.user import UserRegistrationSerializer
from instagram.album_mbe.models import UserFollows

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class UserRegistrationCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserSimilarListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        return UserSimilarity.objects.filter(user=self.request.user, similarity_score__gte=70)


class UserFollowCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        follow_user_id = kwargs.get("id")

        ###########################################
        # Checking if Followed User id is correct #
        ###########################################
        if not User.objects.filter(id=follow_user_id).exists():

            return Response(data={"detail": "Followed User not found!"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = UserFollows.objects.filter(user=request.user, follow_id=follow_user_id)

        # If already followed
        if queryset.exists():

            # Then unfollow
            queryset.delete()

            # Return response
            return Response(data={"detail": "Unfollowed Successfully!"}, status=status.HTTP_200_OK)

        # Else following
        UserFollows.objects.create(user=request.user, follows_id=follow_user_id)

        # Return response
        return Response(data={"detail": "Followed Successfully!"}, status=status.HTTP_200_OK)
