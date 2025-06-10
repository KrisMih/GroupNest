from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import FriendRequest
from .serializers import FriendRequestSerializer

User = get_user_model()

class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        to_user_id = self.request.data.get('to_user_id')
        if not to_user_id:
            raise ValidationError({"error": "to_user_id is required."})
        if int(to_user_id) == self.request.user.id:
            raise ValidationError({"error": "You cannot send a friend request to yourself."})
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            raise ValidationError({"error": "User not found."})
        if FriendRequest.objects.filter(from_user=self.request.user, to_user=to_user).exists():
            raise ValidationError({"error": "Friend request already sent."})
        if FriendRequest.objects.filter(from_user=to_user, to_user=self.request.user, accepted=True).exists():
            raise ValidationError({"error": "You are already friends."})
        serializer.save(from_user=self.request.user, to_user=to_user)

class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, accepted=False)

class FriendRequestAcceptView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            raise PermissionDenied({"error": "You cannot accept this friend request."})
        if instance.accepted:
            raise ValidationError({"error": "Friend request already accepted."})
        instance.accepted = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class FriendRequestDeleteView(generics.DestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user and instance.from_user != request.user:
            raise PermissionDenied({"error": "You cannot delete this friend request."})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
