from celery import shared_task
from .models import UserChallenge
from exercise.models import ChallengeDay

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

    except UserChallenge.DoesNotExist:
        pass