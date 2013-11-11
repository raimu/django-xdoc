from rest_framework import serializers
from models import Node


class NodeSerializer(serializers.ModelSerializer):
    path = serializers.Field(source='path')
    thumbnail_url = serializers.Field(source='thumbnail_url')

    class Meta:
        model = Node
        fields = ('name', 'thumbnail_url', 'path', 'id', 'parent')