from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'post', 'post_title', 'is_read', 'created_at']