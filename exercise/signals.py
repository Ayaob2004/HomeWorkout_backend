from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Challenge
from notification.models import FCMDevice
from notification.views import send_notification

@receiver(post_save, sender=Challenge)
def send_new_challenge_notification(sender, instance, created, **kwargs):
    if created:
        tokens = list(
            FCMDevice.objects.exclude(token__isnull=True).values_list("token", flat=True)
        )
        if tokens:
            title = "🏋️ New Challenge Available!"
            body = f"The challenge '{instance.name}' is now available."
            send_notification(tokens, title, body)   