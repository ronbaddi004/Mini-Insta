from django.contrib import admin

# Register your models here.
from album_mbe.models import Album, UserFollows, UserSimilarity, Picture, Caption, HashTag


admin.site.register(Album)
admin.site.register(UserFollows)
admin.site.register(UserSimilarity)
admin.site.register(Picture)
admin.site.register(Caption)
admin.site.register(HashTag)
