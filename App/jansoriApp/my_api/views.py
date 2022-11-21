from django.shortcuts import render

from rest_framework import viewsets
from serializers import MembersSerializer, ExerciseSerializer
from models import Members, Exercise


class MembersViewSet(viewsets.ModelViewSet):
   queryset = Members.objects.all()
   serializer_class = MembersSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
   queryset = Exercise.objects.all()
   serializer_class = ExerciseSerializer