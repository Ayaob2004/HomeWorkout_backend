from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Profile, MuscleGroup
from .serializers import ProfileBasicInfo, Moredetails, DaysAndTime , MuscleGroupSer , ProfileSer
from rest_framework import generics
from django.utils.translation import gettext_lazy as _  
from rest_framework.permissions import AllowAny  
from rest_framework.permissions import IsAdminUser





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
    def get(self,request):
        try:
            
            profile = request.user.profile
        except profile.DoesNotExist:
            return Response({"message":_("Profile not found")}, status=status.HTTP_404_NOT_FOUND)    
        serializer=ProfileSer(profile)
        return Response(serializer.data)
                
                

class AllUsersView(generics.ListAPIView):
    serializer_class = ProfileSer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Profile.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if request.user.is_staff:
                data = list(queryset.values('user__username')) 
                return Response(data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Failed to retrieve profiles", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminProfileDetailView(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Failed to retrieve profile", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSer(profile, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)