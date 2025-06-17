from rest_framework import serializers
from .models import CustomUser,UserChallenge
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from exercise.serializers import ChallengeSerializer

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # This should reference your CustomUser model
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)  # Create the user properly
        return user

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer()
    
    class Meta:
        model = UserChallenge
        fields = ['challenge']