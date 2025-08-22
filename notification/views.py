from firebase_admin import messaging
from .models import FCMDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



def register_fcm_token(user, token):
    if not token:
        return
    FCMDevice.objects.update_or_create(
        token=token,
        defaults={'user': user}
    )


def send_notification(tokens, title, body):
    if not tokens:
        return None

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
    )
    response = messaging.send_multicast(message)
    print(f"Successfully sent: {response.success_count}, Failed: {response.failure_count}")
    return response


