from rest_framework import serializers
from .models import Exercise

class ExerciseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'