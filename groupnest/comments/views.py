from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Comment
from .serializers import CommentSerializer
from posts.models import Post
from groups.models import Group

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Post not found"})
        serializer.save(author=self.request.user, post=post)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            comment = Comment.objects.get(id=self.kwargs.get('pk'))
        except Comment.DoesNotExist:
            raise ValidationError({"error": "Comment does not exist."})
        return comment

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise ValidationError({"error": "You cannot edit this comment"})
        serializer.save()

    def perform_destroy(self, instance):
        group = instance.post.group
        if instance.author != self.request.user and group.admin != self.request.user:
            raise ValidationError({"error": "You cannot delete this comment"})
        instance.delete()
