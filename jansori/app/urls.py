from django.urls import path, include
from .views import userAPI, usersAPI, goalAPI, goalsAPI, recent_mealAPI

urlpatterns = [
    path("users/", usersAPI),
    path("user/<str:user_id>", userAPI),
    path("goals/", goalsAPI),
    path("goal/<str:goal_id>", goalAPI),
    path("meal/<str:goal_id>", recent_mealAPI),

]