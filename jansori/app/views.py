from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import User, Goal, Recent
from .serializers import UserSerializer, GoalSerializer, MealSerializer, ExeerciseSerializer, CleanSerializer


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


@api_view(['GET'])
def userAPI(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
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
def goalAPI(request, user_id):
    goal = get_object_or_404(User, user_id=user_id)
    serializer = UserSerializer(goal)
    return Response(serializer.data, status=status.HTTP_200_OK)
