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

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
        
        group = post.group
        if self.request.user not in group.members.all() and self.request.user != group.admin:
            raise PermissionDenied({"error": "You are not allowed to unlike this post"})

        try:
            like = Like.objects.get(post=post, user=self.request.user)
        except Like.DoesNotExist:
            raise ValidationError({"error": "You haven't liked this post"})
        
        return like
    
class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
    
        group = post.group
        if not (self.request.user in group.members.all() or self.request.user == group.admin):
            raise PermissionDenied({"error": "You are not member of this group!"})

        return Like.objects.filter(post = post)