from celery import shared_task
from .models import UserChallenge 
from notification.models import FCMDevice
from exercise.models import ChallengeDay
from firebase_admin import messaging
from django.utils import timezone
from notification.views import send_notification

@shared_task
def unlock_next_day(user_challenge_id):
    try:
        user_challenge = UserChallenge.objects.get(id=user_challenge_id)
        current_day = user_challenge.current_day or 1
        next_day = current_day + 1
        
        if next_day <= 28:
            challenge_day = ChallengeDay.objects.filter(
                challenge=user_challenge.challenge,
                day_number=next_day
            ).first()

            if challenge_day:
                challenge_day.is_available = True
                challenge_day.save()
                user_challenge.current_day = next_day
                user_challenge.save()
                
                user = user_challenge.user
                
                try:
                    user_tokens = FCMDevice.objects.filter(user=user).values_list('token', flat=True)
                    
                    if user_tokens:
                        title = "New Day Available!"
                        body = f"Day {next_day} of the challenge is now available. Let's get started!"
                        send_notification(user_tokens, title, body)
                except Exception as e:
                    print(f"Error sending notification: {e}")

    except UserChallenge.DoesNotExist:
        pass