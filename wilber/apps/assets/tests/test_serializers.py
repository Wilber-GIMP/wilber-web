from rest_framework import serializers
from assets.models import Like
from assets.models import Asset

class AssetSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for Asset model.
    """

    class Meta:
        model = Asset
        fields = ('id', 'created', 'modified', 'owner', 'category', 'name', 'slug', 'description', 'source', 'file', 'filesize', 'image', 'num_likes', 'num_downloads', 'num_views', 'created_at', 'updated_at')


class LikeSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for Like model.
    """

    class Meta:
        model = Like
        fields = ('id', 'user', 'asset', 'timestamp')
