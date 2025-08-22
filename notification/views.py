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

    for token in tokens:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        try:
            response = messaging.send(message)
            print(f"Successfully sent to {token}: {response}")
        except Exception as e:
            print(f"Failed to send to {token}: {e}")
