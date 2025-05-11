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
        group = Group.objects.get(id=pk)
        user = User.objects.get(username=request.data['username'])
        group.members.add(user)
        return Response({"message": "User added to the group"}, status=status.HTTP_200_OK)
    
class RemoveMemberView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        user = User.objects.get(username=request.data['username'])
        group.members.remove(user)
        return Response({"message": "User removed from the group"}, status=status.HTTP_200_OK)
