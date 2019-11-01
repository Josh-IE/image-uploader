from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    callback_url = serializers.URLField(required=False)
    image_url = serializers.URLField()
