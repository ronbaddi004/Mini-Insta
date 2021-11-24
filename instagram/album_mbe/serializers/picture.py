from rest_framework import serializers

from PIL import Image, ImageDraw, ImageFont

from album_mbe.models import Picture, Album


class CaptionSerializer(serializers.Serializer):
    id                      = serializers.IntegerField(read_only=True)

    text                    = serializers.CharField(max_length=100)
    color                   = serializers.ListField(child=serializers.IntegerField(max_value=255), max_length=3)
    x_pos                   = serializers.IntegerField()
    y_pos                   = serializers.IntegerField()
    size                    = serializers.IntegerField()

    class Meta:
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

    captions                = CaptionSerializer(many=True, write_only=True)

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

        img = validated_data.pop("image")

        I1 = ImageDraw.Draw(img)

        for caption_data in captions_set:

            font_type = ImageFont.truetype(size=caption_data.get("size"))

            I1.text((caption_data.get("x_pos"), caption_data.get("y_pos")), caption_data.get("text"), caption_data.get("color"), font=font_type)

        img.save()

        picture_obj: Picture = Picture.objects.create(album=self.context.get("view").kwargs.get("id"), image=img, **validated_data)

        return picture_obj
