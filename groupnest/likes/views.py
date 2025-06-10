from django.shortcuts import render
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from posts.models import Post
from groups.models import Group

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
        
        group = post.group
        
        if not (self.request.user in group.members.all() or self.request.user == group.admin):
            raise PermissionDenied({"error": "You are not member of this group!"})
        
        if Like.objects.filter(user = self.request.user, post = post).exists():
            raise ValidationError({"error": "You have already liked this post."})
        
        serializer.save(user = self.request.user, post = post)

class LikeDestroyView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        post = instance.post
        group = post.group
        if self.request.user != instance.user:
            raise PermissionDenied({"error": "You are not the person who liked the post"})
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)