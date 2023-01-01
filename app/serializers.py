from rest_framework import serializers
from .models import User, Recent, Goal, HomeConnect, TurnOn


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'user_id', 'pw', 'location']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['goal_id', 'meal', 'exercise', 'clean']


class RecentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_id']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_meal']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_exercise']


class CleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recent
        fields = ['recent_clean']


class TurnOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurnOn
        fields = ['turnon_id', 'air_conditioner', 'air_purifier', 'tv', 'robot_clean']


class HomeConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeConnect
        fields = ['home_id', 'air_conditioner_name', 'air_purifier_name', 'tv_name', 'robot_clean_name']




