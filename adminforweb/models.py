from django.db import models
from django.conf import settings 
from userprofile.models import MuscleGroup

class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('strength', 'Strength'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
    ]
    name = models.CharField(max_length=225)
    description = models.TextField(null=True , blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True , help_text="Duration in seconds")
    repetitions = models.PositiveIntegerField(null=True, blank=True, help_text="Number of repetitions (optional)")
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned per session")
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    
    def __str__(self):
        return self.name

