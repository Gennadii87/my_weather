from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import CitySearchViewSet, CityAllSearchViewSet
from .service import autocompletion

router = DefaultRouter()
router.register(r'history', CityAllSearchViewSet, basename='city_search')
router.register(r'history', CitySearchViewSet, basename='city_search')

urlpatterns = [
    path('', views.weather_view, name='weather'),
    path('last/',  views.last_search, name='last'),
    path('history/',  views.search_history, name='history'),
    path('autocompletion/', autocompletion, name='autocompletion'),
    path('request_count/', views.city_request_count, name='request_count'),
    path('all_request_counts/', views.all_city_request_counts, name='all_request_counts'),

    path("api/", include(router.urls)),
]
