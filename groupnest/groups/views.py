from rest_framework import generics
from .models import Group
from .serializers import GroupSerializer
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

class DeleteGroupView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def delete(self, request, pk):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status=status.HTTP_403_FORBIDDEN)
        group.delete()
        return Response({"message": "Group deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UpdateGroupView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddMemberView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id = pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status = status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status = status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:   
            return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)
        if user in group.members.all():
            return Response({"error": "User is already a member of this group"}, status = status.HTTP_400_BAD_REQUEST)
        group.members.add(user)
        return Response({"message": "User added to the group"}, status = status.HTTP_200_OK)
        
    
class RemoveMemberView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id = pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status = status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status = status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)
        if user not in group.members.all():
            return Response({"error": "User is not a member of this group"}, status = status.HTTP_400_BAD_REQUEST)
        group.members.remove(user)
        return Response({"message": "User removed from the group"}, status = status.HTTP_200_OK)

class JoinGroupView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id = pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status = status.HTTP_404_NOT_FOUND)
        if request.user in group.members.all():
            return Response({"error": "You are already a member of this group"}, status = status.HTTP_400_BAD_REQUEST)
        if group.admin == request.user:
            return Response({"error": "You cannot join a group you are an administrator of"}, status = status.HTTP_400_BAD_REQUEST)
        if request.user in group.join_requests.all():
            return Response({"error": "You have already sent a join request to this group"}, status = status.HTTP_400_BAD_REQUEST)
        
        if group.is_private and request.user not in group.join_requests.all():
            group.join_requests.add(request.user)
            return Response({"error": "Join request sent. Waiting for the admin's approval!"}, status = status.HTTP_403_FORBIDDEN)
        else:
            group.members.add(request.user)
            return Response({"message": "You have joined the group"}, status = status.HTTP_200_OK)
        
class LeaveGroupView(generics.GenericAPIView):  
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        if group.admin == request.user:
            return Response({"error": "You cannot leave a group you are an administrator"}, status = status.HTTP_400_BAD_REQUEST)
        if request.user not in group.members.all():
            return Response({"error": "You are not a member of this group"}, status = status.HTTP_400_BAD_REQUEST)
        group.members.remove(request.user)
        return Response({"message": "You have left the group"}, status = status.HTTP_200_OK)

class AcceptJoinRequestView(generics.GenericAPIView):  
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id = pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status = status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status = status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)
        if user not in group.join_requests.all():
            return Response({"error": "User has not requested to join this group"}, status = status.HTTP_400_BAD_REQUEST)
        group.members.add(user)
        group.join_requests.remove(user)
        return Response({"message": "Join request accepted"}, status = status.HTTP_200_OK)
    
class RejectJoinRequestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(id = pk)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status = status.HTTP_404_NOT_FOUND)
        if group.admin != request.user:
            return Response({"error": "You are not the admin of this group"}, status = status.HTTP_403_FORBIDDEN)
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status = status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)
        if user not in group.join_requests.all():
            return Response({"error": "User has not requested to join this group"}, status = status.HTTP_400_BAD_REQUEST)
        group.join_requests.remove(user)
        return Response({"message": "Join request rejected"}, status = status.HTTP_200_OK)