from album_mbe.serializers.album import PictureSerializer

from django.db import transaction

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class PictureCreateAPIView(CreateAPIView):
    serializer_class = PictureSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {"view": self}

    def perform_create(self, serializer):

        if serializer.is_valid(raise_exception=True):

            with transaction.atomic():

                # save model
                serializer.save()
