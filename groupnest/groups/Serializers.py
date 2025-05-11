from rest_framework import serializers
from .models import Group
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class GroupSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only = True)
    members = UserSerializer(many = True, read_only = True) 

    class Meta: 
        model = Group
        fields = ['id', 'name', 'description', 'admin', 'members']

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group 
        fields = ['name', 'description']

