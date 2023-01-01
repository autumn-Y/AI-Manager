from django.urls import path
from .views import base_views, weather_views, athome_views, congest_veiws

urlpatterns = [
    # base_views.py
    path('nugu.test', base_views.test),
    path('health', base_views.health, name='health'),
    path('answer.jansori', base_views.alert_info),
    path('LG', base_views.lg_connect),  
    
    # weather_views.py
    path('answer.weather', weather_views.odd_weather),
    path('1_temp', weather_views.give_temp),
    path('2_rain', weather_views.give_rain_probability),
    path('3_dust', weather_views.give_dust),

    # congest_views.py
    path('answer.congestion', congest_veiws.answer_congest),
    
    # athome_views.py
    path('answer.athome', athome_views.answer_athome),
]