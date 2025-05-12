from rest_framework import generics
from .models import Group
from .Serializers import GroupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class AddMemberView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status=status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:   
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user in group.members.all():
            return Response({"error": "User is already a member of this group"}, status=status.HTTP_400_BAD_REQUEST)
        group.members.add(user)
        return Response({"message": "User added to the group"}, status=status.HTTP_200_OK)
        
    
class RemoveMemberView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status=status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status=status.HTTP_400_BAD_REQUEST)
        group.members.remove(user)
        return Response({"message": "User removed from the group"}, status=status.HTTP_200_OK)

