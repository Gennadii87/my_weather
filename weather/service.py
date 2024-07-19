import os

import requests
from geopy.geocoders import Nominatim
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import CitySearch


class CityNotFoundError(Exception):
    pass


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent='weather_app')
    location = geolocator.geocode(city_name)
    if location is None:
        raise CityNotFoundError(f'Город «{city_name}» не найден.')
    return {'latitude': location.latitude, 'longitude': location.longitude}


def get_weather(city):
    try:
        coordinates = get_coordinates(city)
    except CityNotFoundError as e:
        return None, str(e)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates['latitude']}&longitude={coordinates['longitude']}&hourly=temperature_2m"
    response = requests.get(url)
    return response.json(), None


@require_GET
def autocompletion(request):
    query = request.GET.get('q', '')

    if len(query) > 1:
        cities = CitySearch.objects.filter(city_name__icontains=query).values_list('city_name', flat=True)
        autocomplete = list(cities)

        if not autocomplete:

            file_path = os.path.join(os.path.dirname(__file__), 'cities.txt')
            with open(file_path, 'r', encoding='utf-8') as file:
                all_cities = file.readlines()
                autocomplete = [city.strip() for city in all_cities if query.lower() in city.lower()]

    return JsonResponse({'autocomplete': autocomplete})
