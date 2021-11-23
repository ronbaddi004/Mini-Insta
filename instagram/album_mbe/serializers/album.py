from typing import Dict, List
from rest_framework import serializers

from album_mbe.models import Album, User, HashTag, Caption
from album_mbe.models import Caption, Picture


class HashTagSerializer(serializers.ModelSerializer):
    name                    = serializers.CharField(max_length=100)

    class Meta:
        model = HashTag
        fields = ["name"]


class CaptionSerializer(serializers.ModelSerializer):
    id                      = serializers.IntegerField(read_only=True)

    text                    = serializers.CharField(max_length=100)
    color                   = serializers.CharField(max_length=16)
    x_pos                   = serializers.IntegerField()
    y_pos                   = serializers.IntegerField()
    size                    = serializers.IntegerField()

    class Meta:
        model = Caption
        fields = [
            "id",

            "text",
            "color",
            "x_pos",
            "y_pos",
            "size"
        ]


class PictureSerializer(serializers.ModelSerializer):
    id                      = serializers.IntegerField(read_only=True)

    image                   = serializers.ImageField(max_length=1000)

    captions                = CaptionSerializer(many=True)

    class Meta:
        model = Picture
        fields = [
            "id",

            "image",

            "captions"
        ]

    def validate(self, data):

        if not Album.objects.filter(
            user=self.context.get("view").request.user,
            id=self.context.get("view").kwargs.get("id")
        ).exists():

            raise serializers.ValidationError(detail=f"Album id: {self.context.get('view').kwargs.get('id')} provided doesn't exists.")

        return data

    def create(self, validated_data):

        # Popping Captions
        captions_set: list = validated_data.pop("captions")

        picture_obj: Picture = Picture.objects.create(album=self.context.get("view").kwargs.get("id"), **validated_data)

        # Preparing Captions objects for Picture
        captions_objs = list(map(lambda caption_data: Caption(picture=picture_obj, **caption_data), captions_set))

        Caption.objects.bulk_create(captions_objs)

        return picture_obj


class AlbumSerializer(serializers.ModelSerializer):
    id                      = serializers.IntegerField(read_only=True)

    title                   = serializers.CharField(max_length=200, allow_blank=True)

    user                    = serializers.PrimaryKeyRelatedField(read_only=True)
    # hash_tags               = serializers.ListField(child=serializers.CharField(max_length=100), required=False, allow_null=True)
    hash_tags               = HashTagSerializer(many=True, read_only=True)
    draft                   = serializers.BooleanField(default=True, required=False)

    pictures                = PictureSerializer(many=True, read_only=True, allow_null=True)

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

        # # Popping Picture Data
        # pictures: None | Dict = validated_data.pop("pictures")

        # # Initializing Captions List
        # captions_objs: List | List[Caption] = []

        # pictures_objs: List | List[Picture] = []

        # for picture_data in pictures:

        #     # Popping Captions
        #     captions_set: list = picture_data.pop("captions")

        #     picture_obj: Picture = Picture(**picture_data)

        #     # Preparing Captions objects for each Picture
        #     captions_objs += list(map(lambda caption_data: Caption(picture=picture_obj, **caption_data), captions_set))

        #     # Appending Picture object to the List
        #     pictures_objs.append(picture_obj)

        HashTag.objects.bulk_create(hash_tags_objs, ignore_conflicts=True)

        obj: Album = Album.objects.create(user=self.context.get("view").request.user, **validated_data)

        obj.hash_tags.add(*hash_tags_objs)

        # Picture.objects.bulk_create(pictures_objs)

        # Caption.objects.bulk_create(captions_objs)

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
