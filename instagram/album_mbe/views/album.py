from django.db import transaction
from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from album_mbe.models import Album
from album_mbe.serializers.album import AlbumSerializer


class AlbumListCreateAPIView(ListCreateAPIView):
    permission_classes: tuple = (IsAuthenticated,)
    serializer_class = AlbumSerializer

    def get_serializer_context(self):
        return {"view": self}

    def get_queryset(self):
        return Album.objects.filter(Q(user=self.request.user) | Q(draft=False)).filter(is_deleted=False)

    def perform_create(self, serializer):

        if serializer.is_valid(raise_exception=True):

            with transaction.atomic():

                # save model
                serializer.save()


class AlbumRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    
    permission_classes: tuple = (IsAuthenticated,)
    serializer_class = AlbumSerializer

    def get_serializer_context(self):
        return {"view": self}

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs.get("id"))

    def perform_update(self, serializer):

        if serializer.is_valid(raise_exception=True):

            with transaction.atomic():

                # save model
                serializer.save()

    def perform_destroy(self, instance):

        with transaction.atomic():

            # save model
            instance.is_deleted = True

            instance.save()
