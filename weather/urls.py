from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='weather'),
    path('history/', views.search_history, name='history'),
    path('last/', views.last_search, name='last'),
    path('autocompletion/', views.autocompletion, name='autocompletion'),
    path('request_count/', views.city_request_count, name='request_count'),
    path('all_request_counts/', views.all_city_request_counts, name='all_request_counts'),
]
