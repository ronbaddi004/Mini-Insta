from django.db import models

from django.contrib.auth import get_user_model

from uuid import uuid4, UUID
from django.db.models.fields import IntegerField

from django.db.models.fields.files import ImageField


User = get_user_model()


class HashTag(models.Model):
    """
    HashTag for Albums.
    """
    name: str           = models.CharField(max_length=100, primary_key=True, editable=False)

    def __str__(self):

        return self.name


class Album(models.Model):
    user: User          = models.ForeignKey(User, on_delete=models.PROTECT)

    title               = models.CharField(max_length=200, null=True, blank=True)

    hash_tags           = models.ManyToManyField(HashTag)
    draft: bool         = models.BooleanField(default=True)
    is_deleted: bool    = models.BooleanField(default=False)


def picture_directory_path(instance, filename: str):
    # type: (Picture, str) -> str
    return f"user_{instance.album.user.id}/album_{instance.album_id}/{filename}"


class Picture(models.Model):
    album: Album        = models.ForeignKey(Album, on_delete=models.PROTECT, related_name="pictures")

    image               = models.ImageField(upload_to=picture_directory_path, max_length=1000)


class Caption(models.Model):
    picture: Picture    = models.ForeignKey(Picture, on_delete=models.PROTECT, related_name="captions")

    # Caption Properties
    text: str           = models.CharField(max_length=100)
    color: str          = models.CharField(max_length=16)
    x_pos: int          = models.IntegerField()
    y_pos: int          = models.IntegerField()
    size: int           = models.IntegerField()


class UserSimilarity(models.Model):
    user                = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    similar_user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="similar_user")

    similarity_score    = models.IntegerField()


class UserFollows(models.Model):
    user                = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    follows             = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="followed_by")
