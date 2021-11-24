from typing import Dict, List
from rest_framework import serializers

from album_mbe.models import Album, User, HashTag
from album_mbe.serializers.picture import PictureSerializer


class HashTagSerializer(serializers.ModelSerializer):
    name                    = serializers.CharField(max_length=100)

    class Meta:
        model = HashTag
        fields = ["name"]


class AlbumSerializer(serializers.ModelSerializer):
    id                      = serializers.IntegerField(read_only=True)

    title                   = serializers.CharField(max_length=200, allow_blank=True)

    user                    = serializers.PrimaryKeyRelatedField(read_only=True)
    hash_tags               = HashTagSerializer(many=True, read_only=True)
    draft                   = serializers.BooleanField(default=True, required=False)

    pictures                = PictureSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",

            "title",

            "user",
            "hash_tags",
            "draft",

            "pictures"
        ]

    def validate(self, data):

        hash_tags = self.context.get("view").request.data.get("hash_tags", [])

        if type(hash_tags) != list:
            # Raise Error if hash_tags is not a list
            raise serializers.ValidationError("Expecting a list of string tags. eg ['abc', 'foo', 'bar'")

        # Updating data
        data["hash_tags"] = hash_tags

        return data

    def create(self, validated_data: Dict):
        # Popping Hash Tag data
        hash_tags_set: None | Dict = validated_data.pop("hash_tags")

        # Preparing HashTag Objects
        hash_tags_objs: List | List[HashTag] = list(map(lambda hash_tag_data: HashTag(name=hash_tag_data), hash_tags_set))

        HashTag.objects.bulk_create(hash_tags_objs, ignore_conflicts=True)

        obj: Album = Album.objects.create(user=self.context.get("view").request.user, **validated_data)

        obj.hash_tags.add(*hash_tags_objs)

        return obj

    def update(self, instance: Album, validated_data: Dict):
        # Popping Hash Tag data
        hash_tags_set: None | Dict = validated_data.pop("hash_tags")

        # Preparing HashTag Objects
        hash_tags_objs: List | List[HashTag] = list(map(lambda hash_tag_data: HashTag(name=hash_tag_data), hash_tags_set))

        HashTag.objects.bulk_create(hash_tags_objs, ignore_conflicts=True)

        instance.title      = validated_data.get("title", instance.title)
        instance.draft      = validated_data.get("draft", instance.draft)

        instance.save()

        # This will Clear all the HashTags from the instance
        instance.hash_tags.clear()

        # Adding HashTags
        instance.hash_tags.add(*hash_tags_objs)

        return instance
