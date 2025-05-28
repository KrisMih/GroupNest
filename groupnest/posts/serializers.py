from rest_framework import serializers
from .models import Post
from groups.models import Group

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'group', 'group_name', 'author_username']
        read_only_fields = ['id', 'author', 'group_name', 'author_username', 'group']
