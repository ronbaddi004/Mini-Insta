from typing import Dict
from album_mbe.models import User

from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    username            = serializers.CharField(max_length=150)
    password            = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
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
