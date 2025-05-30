from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .models import Exercise
from .serializers import ExerciseSerializers
from django.utils.translation import gettext_lazy as _  
from rest_framework.decorators import api_view ,permission_classes , authentication_classes
from django.views.decorators.csrf import csrf_exempt  
from rest_framework.permissions import IsAuthenticated
from account.models import UserChallenge
from .serializers import UserChallengeDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from exercise.serializers import ChallengeSerializer, ChallengeDaySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from exercise.models import Challenge, ChallengeDay, DayExercise, Exercise
from userprofile.models import Profile
from django.contrib.auth import get_user_model
from datetime import datetime
import random

# for admin

class ExerciseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)
        name = request.data.get('name')
        if Exercise.objects.filter(name=name).exists():
            return Response(
                {"detail": f"Exercise with name '{name}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ExerciseSerializers(data=request.data)
        if serializer.is_valid():
            exercise = serializer.save()
            return Response(ExerciseSerializers(exercise).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
        except Exercise.DoesNotExist:
            return Response({"detail": "Exercise not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExerciseSerializers(exercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
        except Exercise.DoesNotExist:
            return Response({"detail": "Exercise not found."}, status=status.HTTP_404_NOT_FOUND)

        exercise.delete()  
        return Response({"detail": "Exercise deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request,pk):
        try:
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseSerializers(exercise)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            return Response({"detail": "Exercise not found."}, status=status.HTTP_404_NOT_FOUND)
    

class ExerciseListView(APIView):
    def get(self, request):
        try:
            exercises = Exercise.objects.all()
            serializer = ExerciseSerializers(exercises, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            return Response({"detail":"Exercise not found"},status=status.HTTP_404_NOT_FOUND)    


class ExerciseFilterView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        muscle_group_ids = request.query_params.get('muscle_group', None)
        level = request.query_params.get('level', None)

        try:
            exercises = Exercise.objects.all()

            if muscle_group_ids:
                ids = muscle_group_ids.split(',')
                exercises = exercises.filter(muscle_group__id__in=ids)

            if level:
                exercises = exercises.filter(level=level)

            serializer = ExerciseSerializers(exercises.distinct(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def generate_level_values(exercise, level):
    base_r = exercise.base_repetitions or 0
    base_d = exercise.base_duration_seconds or 0
    base_c = exercise.base_calories_burned or 0

    if level == 'beginner':
        return base_r, base_d, base_c
    elif level == 'intermediate':
        return base_r + 5, base_d + 15, base_c + 20
    elif level == 'advanced':
        return base_r + 10, base_d + 30, base_c + 40
    else:
        return base_r, base_d, base_c




#for user

class UserChallengeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_challenge = get_object_or_404(UserChallenge, user=user)
        serializer = UserChallengeDetailSerializer(user_challenge)
        return Response(serializer.data)


class ChallengeListView(generics.ListAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengeDetailView(generics.ListAPIView):
    serializer_class = ChallengeDaySerializer
    def get_queryset(self):
        challenge_id = self.kwargs['pk']
        return ChallengeDay.objects.filter(challenge_id=challenge_id).order_by('week_number', 'day_number')


class ChallengeDayDetailView(APIView):
    def get(self, request, pk, day_number):
        challenge_day = get_object_or_404(ChallengeDay, challenge_id=pk, day_number=day_number)
        day_exercises = DayExercise.objects.filter(challenge_day=challenge_day).order_by('order')
        total_duration = sum(ex.duration_seconds or 0 for ex in day_exercises) / 60  # minutes
        total_exercises = day_exercises.count()
        exercises_data = [
            {
                'name': ex.exercise.name,
                'image': request.build_absolute_uri(ex.exercise.image.url) if ex.exercise.image else None,
                'repetitions': ex.repetitions,
            }
            for ex in day_exercises
        ]
        return Response({
            'day_number': challenge_day.day_number,
            'total_duration_minutes': round(total_duration, 2),
            'total_exercises': total_exercises,
            'exercises': exercises_data
        })



class ExerciseDetailView(generics.RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializers
    lookup_field = 'pk'


User = get_user_model()

class GenerateChallengeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if UserChallenge.objects.filter(user=user, is_completed=False).exists():
            return Response(
                {"error": "User already has an active challenge"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            profile = Profile.objects.get(user=user)
            if not self.check_exercises_available(profile):
                return Response(
                    {
                        "error": "No suitable exercises found for your profile. "
                                "Please contact support or try different profile settings."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            challenge = self.generate_challenge_for_user(user)
            return Response({
                "message": "Challenge created successfully",
                "challenge_id": challenge.id,
                "challenge_name": challenge.name
            }, status=status.HTTP_201_CREATED)
        except Profile.DoesNotExist:
            return Response(
                {"error": "User profile not found. Please complete your profile first."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def check_exercises_available(self, profile):
        level = profile.level
        exercises_count = Exercise.objects.filter(
            goal=profile.goal,
            type='daily'
        ).count()
        return exercises_count >= 4

    def generate_challenge_for_user(self, user):
        profile = Profile.objects.get(user=user)
        level = profile.level
        challenge_name = f"{user.first_name}'s Personalized Challenge" if user.first_name else f"{user.username}'s Challenge"
        challenge = Challenge.objects.create(
            name=challenge_name,
            duration_weeks=4,
            level=level
        )

        for week in range(1, 5):
            for day in range(1, 8):
                challenge_day = ChallengeDay.objects.create(
                    challenge=challenge,
                    week_number=week,
                    day_number=day + ((week - 1) * 7)
                )

                exercises = Exercise.objects.filter(
                    goal=profile.goal,
                    type='daily'
                ).order_by('?')

                if exercises.count() < 4:
                    raise ValueError(
                        f"Not enough exercises found for goal {profile.goal}"
                    )

                selected_exercises = exercises[:4]
                for order, exercise in enumerate(selected_exercises, start=1):
                    reps, duration, calories = generate_level_values(exercise, level)
                    DayExercise.objects.create(
                        challenge_day=challenge_day,
                        exercise=exercise,
                        order=order,
                        repetitions=reps,
                        duration_seconds=duration,
                        calories_burned=calories
                    )

        UserChallenge.objects.create(
            user=user,
            challenge=challenge,
            started_at=datetime.now(),
            current_day=1,
            is_completed=False
        )
        return challenge