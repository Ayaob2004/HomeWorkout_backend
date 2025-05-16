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
    
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    name = models.CharField(max_length=225)
    description = models.TextField(null=True , blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True , help_text="Duration in seconds")
    repetitions = models.PositiveIntegerField(null=True, blank=True, help_text="Number of repetitions (optional)")
    muscle_group = models.ManyToManyField(MuscleGroup, blank=True)
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned per session")
    level = models.CharField(max_length=25 , choices=LEVEL_CHOICES,null=True, blank=True)
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    
    def __str__(self):
        return self.name

