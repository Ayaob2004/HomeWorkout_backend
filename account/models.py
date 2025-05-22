from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
import random
from datetime import datetime
from exercise.models import Challenge
from django.core.validators import MaxValueValidator


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"

    def generate_code(self):
        self.code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.save()


class UserState(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_calories = models.FloatField(null=True)
    total_minutes = models.FloatField(null=True)
    bmi = models.FloatField(null=True)
    updated_at = models.DateTimeField(null = True, default = datetime.now)


class UserChallenge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    started_at = models.DateField(null=True, default=datetime.now())
    current_day = models.PositiveIntegerField(null=True,validators=[MaxValueValidator(28)])
    is_completed = models.BooleanField(null=True)