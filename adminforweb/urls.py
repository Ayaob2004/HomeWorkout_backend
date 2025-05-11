from django.urls import path
# from . import views
from .views import ExerciseView , ExerciseListView
from userprofile.views import AllProfilesView


urlpatterns = [
    path('create_exercise/',ExerciseView.as_view() , name='create_exercise'),
    path('update_exercise/<int:pk>/',ExerciseView.as_view(),name='update_exersice'),
    path('delete_exercise/<int:pk>/',ExerciseView.as_view(),name='delete_exercise'),
    path('retrieve_exercise/<int:pk>/',ExerciseView.as_view(),name='retrieve_exercise'),
    path('retrieve_all/',ExerciseListView.as_view(),name='retrieve_exercise'),
    path('profiles/', AllProfilesView.as_view(), name='all-profiles'),

]