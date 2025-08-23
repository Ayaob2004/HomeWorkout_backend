from rest_framework import serializers
from .models import CustomUser,UserChallenge ,Wallet, WalletTransaction
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


class WalletTopUpSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=255, required=False, default='Wallet Top-up')        


class WalletSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Wallet
        fields = ['username', 'balance']        