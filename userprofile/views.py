from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Profile, MuscleGroup
from .serializers import ProfileBasicInfo, Moredetails, DaysAndTime , MuscleGroupSer , ProfileSer
from rest_framework import generics
from django.utils.translation import gettext_lazy as _  
from rest_framework.permissions import AllowAny  




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
    # permissions_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        try:
            
            profile = request.user.profile
        except profile.DoesNotExist:
            return Response({"message":_("Profile not found")}, status=status.HTTP_404_NOT_FOUND)    
        serializer=ProfileSer(profile)
        return Response(serializer.data)
                
                

class AllProfilesView(generics.ListAPIView):
    serializer_class = ProfileSer
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            return Profile.objects.all()
        except Exception as e:
            # Optionally log the error or customize behavior
            return Profile.objects.none()  # return empty queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Failed to retrieve profiles", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )                