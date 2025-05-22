from django.db import models
from django.conf import settings 
from datetime import datetime
# Create your models here.

class MuscleGroup(models.Model):
    name = models.CharField(max_length=50, choices=[
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('glutes', 'Glutes'),
        ('full_body', 'Full Body'),
    ])

    def __str__(self):
        return self.name


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    GOAL_CHOICES = (
        ('hypertrophy', 'Hypertrophy'),
        ('muscle_definition', 'Muscle Definition'),
        ('lose_weight', 'Lose Weight'),
    )
    
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  
    weight_goal = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES , blank=True) 
    level = models.CharField(max_length=20 , choices=LEVEL_CHOICES)
    focused_muscle_groups = models.ManyToManyField(MuscleGroup, blank=True)
    workout_days = models.JSONField(default=list, help_text="List of days like ['Monday', 'Wednesday']")
    workout_time_per_day = models.TimeField(null=True, blank=True)  

    def __str__(self):
        return f"Profile of {self.user.email}"