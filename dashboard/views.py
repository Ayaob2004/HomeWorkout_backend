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
      
       





User = get_user_model()

class DashboardAPIView(APIView):
    permission_classes = [AllowAny]   # Allow all users (authenticated or not)
    authentication_classes = []       # No authentication required

    def get(self, request):
        count = User.objects.count()
        serializer = UserCountSerializer({'user_count': count})
        return Response(serializer.data)



class MostTargetedMusclesAPIView(APIView):
    permission_classes = [AllowAny] 
    authentication_classes = [] 

    def get(self, request):
        muscles = MuscleGroup.objects.annotate(
            user_count=Count('profile')
        ).order_by('-user_count')

        most_targeted_names = [
            muscle.name for muscle in muscles if muscle.user_count > 0
        ]
        return Response({'most_targeted_muscles': most_targeted_names})    


class AvgCaloriesBurnedAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes =[]  

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
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        count = UserChallenge.objects.filter(is_completed=True).count()
        return Response({'completed_challenges': count})        