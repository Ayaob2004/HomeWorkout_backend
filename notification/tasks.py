# notifications/tasks.py
from celery import shared_task
from django.contrib.auth import get_user_model
from notification.models import FCMDevice
from notification.views import send_notification

User = get_user_model()

@shared_task
def send_workout_notification(user_id):
    print(f"Task triggered for user_id: {user_id}")
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        print(f"User found: {user.username}, workout_time: {profile.workout_time_per_day}")

        tokens = list(
            FCMDevice.objects.filter(user=user).values_list("token", flat=True)
        )
        print(f"Found {len(tokens)} tokens for user")

        if tokens and profile.workout_time_per_day:
            title = "⏰ Time to workout!"
            body = f"Hi {user.username}, it's your training time. Let's move 💪"
            print(f"Sending notification: {title} - {body}")
            send_notification(tokens, title, body)
        else:
            print("No tokens or workout time not set")

    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist")
    except Exception as e:
        print(f"Error in task: {e}")