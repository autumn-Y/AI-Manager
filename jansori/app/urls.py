from django.urls import path, include
from .views import userAPI, usersAPI, goalAPI, goalsAPI

urlpatterns = [
    path("users/", usersAPI),
    path("user/", userAPI),
    path("goals/", goalsAPI),
    path("goal/", goalAPI),

]