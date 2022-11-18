from django.urls import path
from . import views

urlpatterns = [
    path('nugu.test', views.test),
    path('health', views.health, name='health'),
    path('answer.weather', views.odd_weather),
    path('1_temp', views.give_temp),
    path('2_rain', views.give_rain_probability),
    path('3_dust', views.give_dust),
    path('answer.jansori', views.alert_info),
    path('LG', views.lg_connect),    
]