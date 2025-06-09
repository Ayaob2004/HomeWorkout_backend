from django.urls import path
from userprofile.views import AllUsersView, AdminProfileDetailView
from .views import (
    ChallengeDayListView,
    ChallengeDayView,
    ChallengeListView,
    ChallengeDetailView,
    ChallengeDayDetailView,
    ChallengeView,
    DayExerciseView,
    ExerciseDayListView,
    ExerciseView,
    ExerciseListView,
    ExerciseFilterView,
    GenerateChallengeView,
    UserChallengeDetailView,
    DayExerciseDetailView
)

urlpatterns = [
    path('create_exercise/',ExerciseView.as_view() , name='create_exercise'),
    path('update_exercise/<int:pk>/',ExerciseView.as_view(),name='update_exersice'),
    path('delete_exercise/<int:pk>/',ExerciseView.as_view(),name='delete_exercise'),
    path('retrieve_exercise/<int:pk>/',ExerciseView.as_view(),name='retrieve_exercise'),
    path('retrieve_all/',ExerciseListView.as_view(),name='retrieve_exercise'),
    path('users/', AllUsersView.as_view(), name='all-users'),
    path('profile/<int:pk>/', AdminProfileDetailView.as_view(), name='admin-profile-detail'),
    path('profile/<int:pk>/update/', AdminProfileDetailView.as_view(), name='admin-update-profile'),
    path('exercises/filter/', ExerciseFilterView.as_view(), name='exercise-filter'),
    
    path('user-challenge-detail/', UserChallengeDetailView.as_view(), name='user-challenge-detail'),
    path('challenges/', ChallengeListView.as_view(), name='challenge-list'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('challenges/<int:pk>/day/<int:day_number>/', ChallengeDayDetailView.as_view(), name='challenge-day-detail'),
    path('generate-challenge/', GenerateChallengeView.as_view(), name='generate-challenge'),
    path('get-exercise-day/<int:pk>/', DayExerciseDetailView.as_view(), name='get-exercise-day'),

    path('create-challenge/',ChallengeView.as_view(),name='create-challenge'),
    path('update-challenge/<int:pk>/',ChallengeView.as_view(),name='update-challenge'),
    path('delete-challenge/<int:pk>/',ChallengeView.as_view(),name = 'delete-challenge'),
    path('retrieve-challenge/<int:pk>/',ChallengeView.as_view(),name = 'retrieve-challenge'),
    path('retrieve-all-challenge/',ChallengeListView.as_view(),name='retrieve-all'),
    
    path('create-challenge-day/',ChallengeDayView.as_view(),name='create-challenge-day'),
    path('update-challenge-day/<int:pk>/',ChallengeDayView.as_view(),name='update-challenge-day'),
    path('delete-challenge-day/<int:pk>/',ChallengeDayView.as_view(),name='detete-challenge-day'),
    path('retrieve-challenge-day/<int:pk>/',ChallengeDayView.as_view(),name='retrieve-challenge-day'),
    path('retrieve-all-challenge-day/',ChallengeDayListView.as_view(),name='retrieve-all'),
    
    path('create-day-exercise/',DayExerciseView.as_view(),name='create-day-exercise'),
    path('update-day-exercise/<int:pk>/',DayExerciseView.as_view(),name='update-day-exercise'),
    path('delete-day-exercise/<int:pk>/',DayExerciseView.as_view(),name='detete-day-exercise'),
    path('retrieve-day-exercise/<int:pk>/',DayExerciseView.as_view(),name='retrieve-day-exercise'),
    path('retrieve-all-day-exercise/',ExerciseDayListView.as_view(),name='retrieve-all'),
]