from django.urls import path
# from . import views
from .views import ExerciseView , ExerciseListView ,ExerciseFilterView,UserChallengeDetailView
from userprofile.views import AllUsersView, AdminProfileDetailView


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




]