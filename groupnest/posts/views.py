from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
            raise ValidationError({"error": "You can't view the list of posts for a group you are not a member of"})
        return Post.objects.filter(group_id = group_id)

    def perform_create(self, serializer):
        group_id = self.kwargs.get('group_id')
        try:
            group = Group.objects.get(id = group_id)
        except Group.DoesNotExist:
            raise ValidationError({"error": "Group not found"})
        if not (self.request.user in group.members.all() or self.request.user == group.admin):
            raise ValidationError({"error": "You are not a member or an admin of this group!"})
        serializer.save(author=self.request.user, group=group)

class PostListDestroyView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        group = instance.group
        if not (request.user == instance.author or request.user == group.admin):
            raise ValidationError({"error": "You can't delete this post."})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
 
    
