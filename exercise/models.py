from django.db import models
from django.conf import settings 
from userprofile.models import MuscleGroup
from django.core.validators import MaxValueValidator

class LevelChoicesMixin:
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('daily', 'Daily'),
        ('stretching', 'Stretching'),
        ('warming up', 'Warming up'),
    ]

    name = models.CharField(max_length=225)
    description = models.TextField(null=True , blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True , help_text="Duration in seconds")
    repetitions = models.PositiveIntegerField(null=True, blank=True, help_text="Number of repetitions (optional)")
    muscle_group = models.ManyToManyField(MuscleGroup, blank=True)
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned per session")
    level = models.CharField(max_length=25, choices=LevelChoicesMixin.LEVEL_CHOICES,null=True, blank=True)
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)
    type = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    
    def __str__(self):
        return self.name
    

class Challenge(models.Model):
    name = models.CharField(max_length=100)
    duration_weeks = models.PositiveIntegerField()
    level = models.CharField(max_length=25, choices=LevelChoicesMixin.LEVEL_CHOICES,null=True, blank=True)
    def __str__(self):
        return self.name
    

class ChallengeDay(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    week_number =  models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    day_number =  models.PositiveIntegerField(validators=[MaxValueValidator(28)])
    def __str__(self):
        return f"Week {self.week_number}, Day {self.day_number} of {self.challenge.name}"


class DayExercise(models.Model):
    challenge_day = models.ForeignKey(ChallengeDay, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.exercise.name} on {self.challenge_day}"

