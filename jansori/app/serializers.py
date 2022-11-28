from rest_framework import serializers
from .models import User, Recent, Goal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'user_id', 'pw', 'location']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['goal_id', 'meal', 'exercise', 'clean']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_meal_id', 'recent_meal']


class ExeerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_exercise_id', 'recent_exercise']


class CleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_clean_id', 'recent_clean']





