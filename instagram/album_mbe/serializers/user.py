from typing import Dict
from album_mbe.models import User, UserSimilarity

from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    id                  = serializers.IntegerField(read_only=True)

    username            = serializers.CharField(max_length=150)
    password            = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",

            "username",
            "password"
        ]

    def validate_username(self, value: str):

        if User.objects.filter(username=value).exists():

            raise serializers.ValidationError(f"User with username: {value} already exists!")

        return value

    def create(self, validated_data: Dict):

        obj = User(username=validated_data.get("username"))
        obj.set_password(validated_data["password"])
        obj.save()

        return obj


class UserSimilaritySerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(read_only=True)

    similar_user                    = serializers.PrimaryKeyRelatedField(read_only=True)
    similar_user__name              = serializers.SerializerMethodField()

    similarity_score                = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserSimilarity
        fields = [
            "id",

            "similar_user",
            "similar_user__name",

            "similarity_score"
        ]

    def get_similar_user__name(self, instance):

        return f"{instance.first_name if instance.first_name is not None else ''}" + f"{instance.last_name if instance.last_name is not None else ''}" 
