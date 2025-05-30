from rest_framework import serializers
from exercise.models import Challenge, ChallengeDay, DayExercise, Exercise
from account.models import UserChallenge
from userprofile.models import MuscleGroup

class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['name']

class ExerciseSerializers(serializers.ModelSerializer):
    muscle_group = MuscleGroupSerializer(many=True)

    class Meta:
        model = Exercise
        fields = [
            'name', 'description', 'image', 'type', 'goal', 'muscle_group',
            'base_repetitions', 'base_duration_seconds', 'base_calories_burned'
        ]
        
class DayExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializers()

    class Meta:
        model = DayExercise
        fields = ['order', 'exercise']

class ChallengeDaySerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()

    class Meta:
        model = ChallengeDay
        fields = ['week_number', 'day_number', 'exercises']

    def get_exercises(self, obj):
        day_exercises = DayExercise.objects.filter(challenge_day=obj).order_by('order')
        return DayExerciseSerializer(day_exercises, many=True).data

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['name', 'duration_weeks', 'level']

class UserChallengeDetailSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer()
    current_day_info = serializers.SerializerMethodField()

    class Meta:
        model = UserChallenge
        fields = ['challenge', 'started_at', 'current_day', 'is_completed', 'current_day_info']

    def get_current_day_info(self, obj):
        challenge_days = ChallengeDay.objects.filter(
            challenge=obj.challenge,
            day_number=obj.current_day
        )
        return ChallengeDaySerializer(challenge_days, many=True).data
