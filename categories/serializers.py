from rest_framework import serializers
from .models import Category


# ModelSerializer 사용
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )
        # exclude = ("created_at",)
