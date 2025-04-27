from django.urls import path
from .views import ProfileBasicInfoViews , Moredetailsviews, MuscleGroupListCreateAPIView , DaysAndTimeViews , ProfileViews


urlpatterns = [
    path('basic-info/', ProfileBasicInfoViews.as_view(), name='profile-basic-info'),
    path('more-details/', Moredetailsviews.as_view(), name='profile-more-details'),
    path('days-time/', DaysAndTimeViews.as_view(), name='profile-days-time'),
    path('muscle-groups/', MuscleGroupListCreateAPIView.as_view(), name='muscle-group-create'),
    path('details/', ProfileViews.as_view(), name='profile-details'),

]
