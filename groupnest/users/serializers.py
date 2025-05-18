from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required = False, allow_blank = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user = user, bio = bio)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username = data['username'], password = data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        data['user'] = user
        return data
