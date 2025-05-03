from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Profile, MuscleGroup
from .serializers import ProfileBasicInfo, Moredetails, DaysAndTime , MuscleGroupSer , ProfileSer
from rest_framework import generics
from django.utils.translation import gettext_lazy as _  




class MuscleGroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = MuscleGroup.objects.all()
    serializer_class = MuscleGroupSer
     

class ProfileBasicInfoViews(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    
    def patch(self , request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({"message": _("Profile not found")}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileBasicInfo(profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Moredetailsviews(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    
    def patch(self,request):
        try:
            profile_details=request.user.profile
        except profile_details.DoesNotExist:
            return Response({"message" : _("Profile not found")}, status= status.HTTP_404_NOT_FOUND)
        
        serializer=Moredetails(profile_details,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DaysAndTimeViews(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    
    def patch(self,request):
        try:
            Profile_day = request.user.profile
        except Profile_day.DoesNotExist:
            return Response({"message":_("Profile not found")}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=DaysAndTime(Profile_day,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
class ProfileViews(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        profile = request.user.profile
        serializer=ProfileSer(profile)
        return Response(serializer.data)        