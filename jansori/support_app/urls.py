from django.urls import path, include
from .views import giveGoal_API

urlpatterns = [
    path("goal/", giveGoal_API)
]