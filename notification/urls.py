from django.urls import path

from notification.views import NewChallengeNotificationView

urlpatterns = [
  path('NewChallenge/', NewChallengeNotificationView.as_view(), name='NewChallenge'),
]
