from django.urls import path
from .views import DashboardAPIView ,MostTargetedMusclesAPIView , AvgCaloriesBurnedAPIView , CompletedChallengesCountAPIView

urlpatterns = [
    path('user-count/', DashboardAPIView.as_view(), name='user-count'),
    path('most-targeted-muscles/', MostTargetedMusclesAPIView.as_view(),name='most-targeted-muscles'),
    path('average-calories/', AvgCaloriesBurnedAPIView.as_view(), name='average-calories'),
    path('completed-challenges/', CompletedChallengesCountAPIView.as_view(), name='completed-challenges'),


]
