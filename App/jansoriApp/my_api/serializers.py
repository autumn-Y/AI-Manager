from rest_framework import serializers
from models import Members, Exercise


class MembersSerializer(serializers.ModelSerializer):
   class Meta:
       model = Members
       fields = ('id', 'pswd', 'name', 'email', 'location')


class ExerciseSerializer(serializers.ModelSerializer):
   class Meta:
       model = Exercise
       fields = ('user_id', 'stretching', 'home_training', 'dance', 'yoga')