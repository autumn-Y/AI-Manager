from django.urls import path, include
from .views import userAPI, usersAPI, loginAPI, goalAPI, goalsAPI, \
    recentAPI, recent_mealAPI, recent_exerciseAPI, recent_cleanAPI, homeconnectAPI, turnonAPI

urlpatterns = [
    path("users/", usersAPI),
    path("user/<str:user_id>", userAPI),
    path("login/", loginAPI),
    path("goals/", goalsAPI),
    path("goal/<str:goal_id>", goalAPI),
    path("recent", recentAPI),
    path("meal/<str:goal_id>", recent_mealAPI),
    path("exercise/<str:goal_id>", recent_exerciseAPI),
    path("clean/<str:goal_id>", recent_cleanAPI),
    path("connect/<str:home_id>", homeconnectAPI),
    path("turnon/<str:turnon_id>", turnonAPI),

]