from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from .models import Profile
from notification.tasks import send_workout_notification


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def schedule_user_workout_task(sender, instance, **kwargs):
    print(f"Profile saved - workout_time: {instance.workout_time_per_day}")
    
    if not instance.workout_time_per_day:
        print("No workout time set, skipping")
        return

    # delete old task if exists
    old_tasks = PeriodicTask.objects.filter(name=f"workout-task-{instance.user.id}")
    print(f"Found {old_tasks.count()} old tasks to delete")
    old_tasks.delete()

    # extract hour & minute
    workout_time = instance.workout_time_per_day
    print(f"Creating task for time: {workout_time.hour}:{workout_time.minute}")
    
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=workout_time.minute,
        hour=workout_time.hour,
        timezone="Asia/Damascus" 
    )

    task = PeriodicTask.objects.create(
        crontab=schedule,
        name=f"workout-task-{instance.user.id}",
        task="notification.tasks.send_workout_notification",
        args=json.dumps([instance.user.id]),
    )
    print(f"Created periodic task: {task.name}")