from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Room
from users.serializers import TinyUserSerializer


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            # "rating",
            "is_owner",
            "photos",
        )
        depth = 1


class RoomDetailSerializer(ModelSerializer):

    # DRF가 owner를 serialize하려 하면, TinyUserSerializer를 사용하라고 알려줌
    owner = TinyUserSerializer()

    class Meta:
        model = Room
        fields = "__all__"
