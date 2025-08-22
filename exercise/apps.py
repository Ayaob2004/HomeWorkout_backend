from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exercise'



class ExerciseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exercise'

    def ready(self):
        import exercise.signals
