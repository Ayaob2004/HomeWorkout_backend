from django.contrib import admin
from .models import Exercise,Challenge,ChallengeDay,DayExercise,HealthArticle

admin.site.register(Exercise)
admin.site.register(Challenge)
admin.site.register(ChallengeDay)
admin.site.register(DayExercise)
admin.site.register(HealthArticle)

