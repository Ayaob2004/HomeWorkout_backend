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

class ExerciseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},status=status.HTTP_403_FORBIDDEN)
    
        name = request.data.get('name')
        level = request.data.get('level')  

        if Exercise.objects.filter(name=name, level=level).exists():
            return Response(
                {"detail": f"Exercise with name '{name}' and level '{level}' already exists."},
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

class UserChallengeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_challenge = get_object_or_404(UserChallenge, user=user)
        serializer = UserChallengeDetailSerializer(user_challenge)
        return Response(serializer.data)
