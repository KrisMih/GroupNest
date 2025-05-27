from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
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

        group = post.group
        if self.request.user not in group.members.all():
            raise PermissionDenied("You are not a member of this group!")

        serializer.save(author = self.request.user, post = post)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment_id = self.kwargs.get('pk')
        try:
            return Comment.objects.get(id = comment_id)
        except Comment.DoesNotExist:
            raise ValidationError({"error": "Comment does not exist."})

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("You are not the author of this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        group = instance.post.group
        if instance.author != self.request.user and group.admin != self.request.user:
            raise PermissionDenied("Only the author or group admin can delete this comment.")
        instance.delete()
