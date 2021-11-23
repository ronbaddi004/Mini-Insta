from rest_framework import serializers

from album_mbe.models import Caption, Picture, Album


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
