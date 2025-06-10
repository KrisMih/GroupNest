from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Post
from .serializers import PostSerializer
from groups.models import Group

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise ValidationError({"error": "Group not found"})
        if not (self.request.user in group.members.all() or self.request.user == group.admin):
            raise PermissionDenied({"error": "You can't view the list of posts for a group you are not a member of"})
        return Post.objects.filter(group_id = group_id)

    def perform_create(self, serializer):
        group_id = self.kwargs.get('group_id')
        try:
            group = Group.objects.get(id = group_id)
        except Group.DoesNotExist:
            raise ValidationError({"error": "Group not found"})
        if not (self.request.user in group.members.all() or self.request.user == group.admin):
            raise PermissionDenied({"error": "You are not a member or an admin of this group!"})
        serializer.save(author=self.request.user, group=group)

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        group = post.group
        if not (request.user == post.author or request.user == group.admin):
            return Response({"error": "You can't update this post."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostListDestroyView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        group = instance.group
        if not (request.user == instance.author or request.user == group.admin):
            raise PermissionDenied({"error": "You can't delete this post."})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
 
    
