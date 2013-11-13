from rest_framework import serializers
from models import Node


class NodeSerializer(serializers.ModelSerializer):
    path = serializers.Field(source='path')
    thumbnail_url = serializers.Field(source='thumbnail_url')
    has_children = serializers.Field(source='has_children')

    class Meta:
        model = Node
        fields = ('name', 'thumbnail_url', 'id', 'parent', 'has_children')