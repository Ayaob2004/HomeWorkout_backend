from celery import shared_task
from django.utils import timezone
from exercise.models import Profile
from notification.models import FCMDevice
from notification.views import send_notification

@shared_task
def send_daily_workout_notifications():
    now = timezone.localtime().time().replace(second=0, microsecond=0)

    profiles = Profile.objects.filter(workout_time_per_day=now)

    for profile in profiles:
        tokens = list(
            FCMDevice.objects.filter(user=profile.user).values_list("token", flat=True)
        )
        if tokens:
            title = "⏰ Time to workout!"
            body = f"Hi {profile.user.username}, it's your training time. Let's move 💪"
            send_notification(tokens, title, body)
