from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Comment
from posts.models import Post
from serializers import CommentSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
        return Comment.objects.filter(post = post)
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
        serializer.save(author = self.request.user, post = post)