from .models import Profile , MuscleGroup
from rest_framework import serializers


class MuscleGroupSer(serializers.ModelSerializer):
    class Meta:
        model=MuscleGroup
        fields = ['id','name']

class ProfileBasicInfo(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'date_of_birth','height','weight','weight_goal']


class Moredetails(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['goal', 'focused_muscle_groups','level']        


class DaysAndTime(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['workout_days', 'workout_time_per_day']


class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'                