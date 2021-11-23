from django.urls import path

from album_mbe.views.album import AlbumListCreateAPIView, AlbumRetrieveUpdateDestroyAPIView
from album_mbe.views.picture import PictureCreateAPIView
from album_mbe.views.user import UserRegistrationCreateAPIView, UserSimilarListAPIView, UserFollowCreateAPIView


urlpatterns = [
    path("registration", UserRegistrationCreateAPIView.as_view()),

    path("user-similar", UserSimilarListAPIView.as_view()),
    path("user-follow/<int:id>/toggle", UserFollowCreateAPIView),

    path("album", AlbumListCreateAPIView.as_view()),
    path("album/<int:id>", AlbumRetrieveUpdateDestroyAPIView.as_view()),
    path("album/<int:id>/upload", PictureCreateAPIView.as_view())
]
