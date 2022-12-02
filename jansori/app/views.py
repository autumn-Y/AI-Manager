from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import User, Goal, Recent
from .serializers import UserSerializer, GoalSerializer, MealSerializer, ExeerciseSerializer, CleanSerializer
from django.contrib.auth import authenticate

@api_view(['GET', 'POST'])
def usersAPI(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
class UserAPI(APIView):
    def get(self, requset, user_id):
        user = get_object_or_404(User, user_id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
@api_view(['GET'])
def userAPI(request, user_id):
    user = User.objects.get(user_id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def goalsAPI(request):
    if request.method == 'GET':
        goals = Goal.objects.all()
        serializer = GoalSerializer(goals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def goalAPI(request, goal_id):
    goal = Goal.objects.get(goal_id=goal_id)
    serializer = GoalSerializer(goal)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def recent_mealAPI(request, resent_meal_id):
    reqData = request.data
    data = Recent.objects.get(resent_meal_id=resent_meal_id)
    serializer = MealSerializer(instance=data, data=reqData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

