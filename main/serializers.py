from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Interest
        fields = [
            "id",
            "name",
            "category",
            "description",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_name(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Interest name cannot be empty."
            )

        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(
            user.username for user in obj.starred_by.all()
        )