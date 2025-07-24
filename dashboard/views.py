from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from account.serializers import RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from userprofile.models import Profile 
from userprofile.models import MuscleGroup 
from django.db.models import Count
from django.utils.timezone import now
from account.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class DashboardAPIView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        count = User.objects.count()
        return Response({'user_count': count})

class MostTargetedMusclesAPIView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication] 

    def get(self, request):
        muscles = MuscleGroup.objects.annotate(
            user_count=Count('profile')
        ).order_by('-user_count')
        most_targeted_names = [
            muscle.name for muscle in muscles if muscle.user_count > 0
        ]
        return Response({'most_targeted_muscles': most_targeted_names})    


class AvgCaloriesBurnedAPIView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]  

    def get(self, request):
        user_states = UserState.objects.exclude(total_calories__isnull=True)
        total_avg = 0
        count = 0
        for state in user_states:
            if state.updated_at:
                days = (now().date() - state.updated_at.date()).days
                days = max(days, 1)  
                daily_avg = state.total_calories / days
                total_avg += daily_avg
                count += 1

        avg_calories_per_day = total_avg / count if count > 0 else 0

        return Response({
            "average_daily_calories_burned": round(avg_calories_per_day, 2),
        })   

class CompletedChallengesCountAPIView(APIView):
    permission_classes = [IsAdminUser] 
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        count = UserChallenge.objects.filter(is_completed=True).count()
        return Response({'completed_challenges': count})        