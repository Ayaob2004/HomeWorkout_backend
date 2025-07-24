# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAdminUser
# from rest_framework.authentication import TokenAuthentication
# from .models import *
# from .serializers import ExerciseSerializers, SimpleUserChallengeSerializer, DayExerciseSerializer ,HealthArticleSerializer
# from django.utils.translation import gettext_lazy as _  
# from rest_framework.decorators import api_view ,permission_classes , authentication_classes
# from django.views.decorators.csrf import csrf_exempt  
# from rest_framework.permissions import IsAuthenticated
# from account.models import UserChallenge
# from .serializers import UserChallengeDetailSerializer
# from django.shortcuts import get_object_or_404
# from rest_framework import generics
# from exercise.serializers import ChallengeSerializer, ChallengeDaySerializer
# from account.serializers import UserChallengeSerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from exercise.models import Challenge, ChallengeDay, DayExercise, Exercise
# from userprofile.models import Profile
# from django.contrib.auth import get_user_model
# from datetime import datetime
# import random
# from account.tasks import unlock_next_day
# from django.utils import timezone
# from rest_framework import status
# from account.models import UserChallenge, UserState
# from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

# Local application imports
from .models import Exercise, Challenge, ChallengeDay, DayExercise, HealthArticle, MuscleGroup
from .serializers import ExerciseSerializers, SimpleUserChallengeSerializer, DayExerciseSerializer, HealthArticleSerializer
from exercise.serializers import ChallengeSerializer, ChallengeDaySerializer
from account.models import UserChallenge, UserState
from userprofile.models import Profile
from account.tasks import unlock_next_day

# Rest of your views code...

#  for admin

class ExerciseView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

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
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            exercises = Exercise.objects.all()
            serializer = ExerciseSerializers(exercises, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            return Response({"detail":"Exercise not found"},status=status.HTTP_404_NOT_FOUND)    


class ExerciseFilterView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

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


class ChallengeView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)
    
        name = request.data.get('name')
        level = request.data.get('level')  

        if Challenge.objects.filter(name=name, level=level).exists():
            return Response(
                {"detail": f"Challenge with name '{name}' and level '{level}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            challenge = serializer.save()
            return Response(ChallengeSerializer(challenge).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response({"detail": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChallengeSerializer(challenge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response({"detial":"Challenge not found."}, status=status.HTTP_404_NOT_FOUND)
        challenge.delete()
        return Response({"detial":"Challenge deleted successfully."},status=status.HTTP_204_NO_CONTENT)

    def get(self,request,pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
            serializer = ChallengeSerializer(challenge)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response({"detail": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)
    

class ChallengeListView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            challenge = Challenge.objects.all()
            serializer = ChallengeSerializer(challenge, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response({"detail":"Challenge not found"},status=status.HTTP_404_NOT_FOUND)    
        


class ChallengeDayView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    
    def post(self,request,*args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)
        
        
        serializer = ChallengeDaySerializer(data=request.data)
        if serializer.is_valid():
            challengeDay = serializer.save()
            return Response(ChallengeDaySerializer(challengeDay).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            challengeDay = ChallengeDay.objects.get(pk=pk)
        except ChallengeDay.DoesNotExist:
            return Response({"detail": "Challenge day not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChallengeDaySerializer(challengeDay, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def delete(self, request,pk):
        try:
            challengeDay = ChallengeDay.objects.get(pk=pk)
        except ChallengeDay.DoesNotExist:
            return Response({"detial":"Challenge day not found."}, status=status.HTTP_404_NOT_FOUND)
        challengeDay.delete()
        return Response({"detial":"Challenge day deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request,pk):
        try:
            challengeDay = ChallengeDay.objects.get(pk=pk)
            serializer = ChallengeDaySerializer(challengeDay)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChallengeDay.DoesNotExist:
            return Response({"detail": "Challenge day not found."}, status=status.HTTP_404_NOT_FOUND)


class ChallengeDayListView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            challengeday = ChallengeDay.objects.all()
            serializer = ChallengeDaySerializer(challengeday, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChallengeDay.DoesNotExist:
            return Response({"detail":"Challenge day not found"},status=status.HTTP_404_NOT_FOUND)    


class DayExerciseView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

    def post(self,request,*args,**kwargs):
        if not request.user.is_staff:
            return Response({"detail":"You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)   
        
        serializer = DayExerciseSerializer(data=request.data)
        if serializer.is_valid():
            dayExercise = serializer.save()
            return Response(DayExerciseSerializer(dayExercise).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            dayExercise = DayExercise.objects.get(pk=pk)
        except DayExercise.DoesNotExist:
            return Response({"detail": "day exercise not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DayExerciseSerializer(dayExercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def delete(self, request,pk):
        try:
            dayExercise = DayExercise.objects.get(pk=pk)
        except DayExercise.DoesNotExist:
            return Response({"detial":"day exercise not found."}, status=status.HTTP_404_NOT_FOUND)
        dayExercise.delete()
        return Response({"detial":"day exercise deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request,pk):
        try:
            dayExercise = DayExercise.objects.get(pk=pk)
            serializer = DayExerciseSerializer(dayExercise)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DayExercise.DoesNotExist:
            return Response({"detail": "day exercise not found."}, status=status.HTTP_404_NOT_FOUND)


class ExerciseDayListView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            dayExercise = DayExercise.objects.all()
            serializer = DayExerciseSerializer(dayExercise, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DayExercise.DoesNotExist:
            return Response({"detail":"day exercise not found"},status=status.HTTP_404_NOT_FOUND)    


class HealthArticleView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

    def post(self,request,*args,**kwargs):
        if not request.user.is_staff:
            return Response({"detail":"You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)   
        
        title = request.data.get('title')
        if HealthArticle.objects.filter(title=title).exists():
            return Response(
                {"detail": f"Article with title '{title}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = HealthArticleSerializer(data=request.data)
        if serializer.is_valid():
            health_article = serializer.save()
            return Response(HealthArticleSerializer(health_article).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            health_article = HealthArticle.objects.get(pk=pk)
        except HealthArticle.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HealthArticleSerializer(health_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        try:
            health_article = HealthArticle.objects.get(pk=pk)
        except HealthArticle.DoesNotExist:
            return Response({"detial":"article not found."}, status=status.HTTP_404_NOT_FOUND)
        health_article.delete()
        return Response({"detial":"Article deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    
    def get(request,self,pk):
        try:
            health_article = HealthArticle.objects.get(pk=pk)
            serializer = HealthArticleSerializer(health_article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HealthArticle.DoesNotExist:
            return Response({"detial":"Article not found."},status=status.HTTP_404_NOT_FOUND)

class HealthArticleListView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            health_article = HealthArticle.objects.all()
            serializer = HealthArticleSerializer(health_article, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HealthArticle.DoesNotExist:
            return Response({"detail":"Articles not found"},status=status.HTTP_404_NOT_FOUND)    


class VisibleArticlesView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            visible_articles = HealthArticle.objects.filter(is_visible=True)
            serializer = HealthArticleSerializer(visible_articles, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except HealthArticle.DoesNotExist:
            return Response({"detail":"Articles not found"},status=status.HTTP_404_NOT_FOUND)

class HiddenArticlesView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            hidden_articles = HealthArticle.objects.filter(is_visible=False)
            serializer = HealthArticleSerializer(hidden_articles,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HealthArticle.DoesNotExist:
            return Response({"detail":"Articles not found"},status=status.HTTP_404_NOT_FOUND)

class ToggleArticleVisibilityView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    def post(self, request, pk):
        try:
            article = HealthArticle.objects.get(pk=pk)
            article.is_visible = not article.is_visible
            article.save()
            
            state = "shown" if article.is_visible else "hidden"
            return Response({"message": f"Article is now {state}."}, status=status.HTTP_200_OK)
        except HealthArticle.DoesNotExist:
            return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)        


#for user

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

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    if height_m == 0:
        return {"error": "Height cannot be zero"}

    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 2)
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 25:
        status = "Normal"
    elif 25 <= bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"
    return {
        "bmi": bmi,
        "status": status
    }


class ChallengeDayDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, day_number):
        challenge_day = get_object_or_404(ChallengeDay, challenge_id=pk, day_number=day_number)
        day_exercises = DayExercise.objects.filter(challenge_day=challenge_day).order_by('order')
        total_duration = sum(ex.duration_seconds or 0 for ex in day_exercises) / 60  # minutes
        total_exercises = day_exercises.count()
        exercises_data = [
            {
                'day_exercise_id': ex.id,
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

class DayExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            day_exercise = DayExercise.objects.select_related('exercise', 'challenge_day').get(pk=pk)
            exercise = day_exercise.exercise
            data = {
                "day_exercise_id": day_exercise.id,
                "exercise": {
                    "id": exercise.id,
                    "name": exercise.name,
                    "description": exercise.description,
                    "goal": exercise.goal,
                    "type": exercise.type,
                    "repetitions": day_exercise.repetitions,
                    "duration_seconds": day_exercise.duration_seconds,
                    "calories_burned": day_exercise.calories_burned,
                    "image": request.build_absolute_uri(exercise.image.url) if exercise.image else None,
                },
            }
            return Response(data)
        except DayExercise.DoesNotExist:
            return Response({"error": "DayExercise not found."}, status=status.HTTP_404_NOT_FOUND)

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
                "challenge_name": challenge.name,
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
                day_number=day + ((week - 1) * 7)
                challenge_day = ChallengeDay.objects.create(
                    challenge=challenge,
                    week_number=week,
                    day_number=day_number,
                    is_available=(day_number == 1)
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

class AllChallengesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        user_challenge = UserChallenge.objects.filter(user=user).select_related('challenge').first()
        user_challenge_data = {
            'id': user_challenge.challenge.id,
            'name': user_challenge.challenge.name
        } if user_challenge else None
        public_challenges = Challenge.objects.exclude(
            id__in=UserChallenge.objects.values_list('challenge_id', flat=True)
        )
        public_challenges_data = ChallengeSerializer(public_challenges, many=True).data
        return Response({
            'user_challenge': user_challenge_data,
            'public_challenges': public_challenges_data
        })
    
class StartChallengeDayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, challenge_id):
        user = request.user

        try:
            user_challenge = UserChallenge.objects.get(user=user, challenge_id=challenge_id)
            current_day = user_challenge.current_day or 1
            challenge_day = ChallengeDay.objects.get(challenge_id=challenge_id, day_number=current_day)
            # Calculate calories and duration
            day_exercises = DayExercise.objects.filter(challenge_day=challenge_day)
            total_duration = sum([ex.duration_seconds or 0 for ex in day_exercises])
            total_calories = sum([ex.calories_burned or 0 for ex in day_exercises])
            # Update UserState
            user_state, _ = UserState.objects.get_or_create(user=user)
            user_state.total_minutes = (user_state.total_minutes or 0) + (total_duration / 60)
            user_state.total_calories = (user_state.total_calories or 0) + total_calories
            user_state.updated_at = timezone.now()
            user_state.save()

            unlock_next_day.apply_async(args=[user_challenge.id], countdown=86400)  # 24 hours

            return Response({
                "message": f"Workout for day {current_day} has started. The next day will be unlocked in 24 hours."
            }, status=status.HTTP_200_OK)
        except UserChallenge.DoesNotExist:
            return Response({"error": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)
        except ChallengeDay.DoesNotExist:
            return Response({"error": "Challenge day not found."}, status=status.HTTP_404_NOT_FOUND)


class CheckDayAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id, day_number):
        try:
            challenge_day = ChallengeDay.objects.get(challenge_id=challenge_id, day_number=day_number)
            return Response({
                "challenge_id": challenge_id,
                "day_number": day_number,
                "is_available": challenge_day.is_available
            }, status=status.HTTP_200_OK)
        except ChallengeDay.DoesNotExist:
            return Response({"error": "Challenge day not found"}, status=status.HTTP_404_NOT_FOUND)


class ExercisesByMuscleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, muscle_id):
        muscle = get_object_or_404(MuscleGroup, id=muscle_id)
        exercises = Exercise.objects.filter(muscle_group=muscle)
        total_duration = sum([ex.base_duration_seconds or 0 for ex in exercises]) / 60  # بالدقائق
        exercises_data = [
            {
                'id': ex.id,
                'name': ex.name,
                'image': request.build_absolute_uri(ex.image.url) if ex.image else None,
                'duration_seconds': ex.base_duration_seconds
            }
            for ex in exercises
        ]
        return Response({
            'muscle': muscle.name,
            'total_duration_minutes': round(total_duration, 2),
            'total_exercises': exercises.count(),
            'exercises': exercises_data
        })

class ExerciseByTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exercise_type = request.query_params.get('type')
        if not exercise_type:
            return Response({"error": "type is required"}, status=400)
        exercises = Exercise.objects.filter(type=exercise_type)
        total_duration = sum(ex.base_duration_seconds or 0 for ex in exercises)
        count = exercises.count()
        data = []
        for ex in exercises:
            data.append({
                "id": ex.id,
                "name": ex.name,
                "image": request.build_absolute_uri(ex.image.url) if ex.image else None,
                "duration": ex.base_duration_seconds,
            })
        return Response({
            "exercises": data,
            "total_duration": total_duration,
            "count": count
        })
