from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import User, Goal, Recent, TurnOn, HomeConnect
from .serializers import UserSerializer, GoalSerializer, MealSerializer, ExerciseSerializer, CleanSerializer, \
    RecentSerializer, TurnOnSerializer, HomeConnectSerializer
from models import Recent, User,
from django.contrib import auth

@api_view(['POST'])
def homeconnectAPI(request):
    serializer = HomeConnectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
def turnonAPI(request, turnon_id):
    if request.method == 'POST':
        serializer = TurnOnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    elif request.method == 'PUT':
        data = TurnOn.objects.get(turnon_id=turnon_id)
        serializer = TurnOnSerializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
            turnonAPI.serializer.save()
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


@api_view(['POST'])
def loginAPI(request):
    if request.method == "POST":
        req_id = request.POST.get('user_id')
        req_pw = request.POST.get('pw')





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


#처음에 recent 채워놔야 put으로 수정 가능, 디폴트 채워놔서 아이디만 보내도 괜찮음
@api_view(['POST'])
def recentAPI(request):
    serializer = RecentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def recent_mealAPI(request, resent_meal_id):
    reqData = request.data
    data = Recent.objects.get(resent_meal_id=resent_meal_id)
    serializer = MealSerializer(instance=data, data=reqData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def recent_exerciseAPI(request, resent_exercise_id):
    reqData = request.data
    data = Recent.objects.get(resent_meal_id=resent_exercise_id)
    serializer = ExerciseSerializer(instance=data, data=reqData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def recent_cleanAPI(request, resent_clean_id):
    reqData = request.data
    data = Recent.objects.get(resent_clean_id=resent_clean_id)
    serializer = CleanSerializer(instance=data, data=reqData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

