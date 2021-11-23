from django.urls import path

from album_mbe.views.album import AlbumListCreateAPIView, AlbumRetrieveUpdateDestroyAPIView
from album_mbe.views.picture import PictureCreateAPIView
from album_mbe.views.user import UserRegistrationCreateAPIView


urlpatterns = [
    path("registration", UserRegistrationCreateAPIView.as_view()),

    path("album", AlbumListCreateAPIView.as_view()),
    path("album/<int:id>", AlbumRetrieveUpdateDestroyAPIView.as_view()),
    path("album/<int:id>/upload", PictureCreateAPIView.as_view())
]
